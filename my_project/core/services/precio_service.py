from decimal import Decimal
from django.utils import timezone
from django.db.models import Q
from core.models import (
    ListaPrecio, PrecioArticulo, ReglaPrecio, 
    CombinacionProducto, Articulo
)
import json


class PrecioService:
    """
    Servicio para gestionar el cálculo de precios según las políticas comerciales.
    Implementa la lógica jerárquica: precio base → canal → escala → monto → combinación
    """

    @staticmethod
    def obtener_lista_vigente(empresa_id, sucursal_id=None, canal='TODOS', fecha=None):
        """
        Obtiene la lista de precios vigente para una empresa/sucursal en una fecha específica.
        
        Args:
            empresa_id: ID de la empresa
            sucursal_id: ID de la sucursal (opcional)
            canal: Canal de venta
            fecha: Fecha de consulta (por defecto hoy)
            
        Returns:
            ListaPrecio o None
        """
        if fecha is None:
            fecha = timezone.now().date()
        
        # Buscar lista vigente
        query = Q(empresa_id=empresa_id, activo=True, fecha_inicio__lte=fecha)
        query &= Q(fecha_fin__gte=fecha) | Q(fecha_fin__isnull=True)
        
        # Priorizar lista específica de sucursal
        if sucursal_id:
            lista = ListaPrecio.objects.filter(
                query, 
                sucursal_id=sucursal_id,
                canal__in=[canal, 'TODOS']
            ).order_by('-fecha_inicio').first()
            
            if lista:
                return lista
        
        # Si no hay lista de sucursal, buscar lista general de empresa
        lista = ListaPrecio.objects.filter(
            query,
            sucursal__isnull=True,
            canal__in=[canal, 'TODOS']
        ).order_by('-fecha_inicio').first()
        
        return lista

    @staticmethod
    def obtener_precio_base(lista_precio, articulo_id):
        """
        Obtiene el precio base de un artículo en una lista.
        
        Args:
            lista_precio: Instancia de ListaPrecio
            articulo_id: ID del artículo
            
        Returns:
            dict con precio_base, bajo_costo, descuento_proveedor
        """
        try:
            precio_articulo = PrecioArticulo.objects.get(
                lista_precio=lista_precio,
                articulo_id=articulo_id
            )
            
            return {
                'precio_base': precio_articulo.precio_base,
                'bajo_costo': precio_articulo.bajo_costo,
                'descuento_proveedor': precio_articulo.descuento_proveedor,
                'autorizado_por': precio_articulo.autorizado_por
            }
        except PrecioArticulo.DoesNotExist:
            return None

    @staticmethod
    def aplicar_reglas(lista_precio, articulo, cantidad, monto_pedido_total, canal):
        """
        Aplica las reglas de precio según la prioridad jerárquica.
        
        Args:
            lista_precio: Instancia de ListaPrecio
            articulo: Instancia de Articulo
            cantidad: Cantidad de unidades
            monto_pedido_total: Monto total del pedido
            canal: Canal de venta
            
        Returns:
            list de reglas aplicadas con sus ajustes
        """
        reglas_aplicadas = []
        
        # Obtener todas las reglas activas de la lista, ordenadas por prioridad
        reglas = ReglaPrecio.objects.filter(
            lista_precio=lista_precio,
            activo=True
        ).order_by('prioridad')
        
        for regla in reglas:
            # Verificar si la regla aplica al artículo
            if not PrecioService._regla_aplica_a_articulo(regla, articulo):
                continue
            
            ajuste = None
            
            # Regla por canal
            if regla.tipo_regla == 'CANAL':
                if lista_precio.canal == canal or lista_precio.canal == 'TODOS':
                    ajuste = PrecioService._calcular_ajuste(regla)
            
            # Regla por escala de unidades
            elif regla.tipo_regla == 'ESCALA_UNIDADES':
                if PrecioService._cantidad_en_rango(cantidad, regla.cantidad_minima, regla.cantidad_maxima):
                    ajuste = PrecioService._calcular_ajuste(regla)
            
            # Regla por escala de monto (del artículo)
            elif regla.tipo_regla == 'ESCALA_MONTO':
                monto_articulo = cantidad * articulo.ultimo_costo  # Monto estimado
                if PrecioService._monto_en_rango(monto_articulo, regla.monto_minimo, regla.monto_maximo):
                    ajuste = PrecioService._calcular_ajuste(regla)
            
            # Regla por monto total del pedido
            elif regla.tipo_regla == 'MONTO_PEDIDO':
                if PrecioService._monto_en_rango(monto_pedido_total, regla.monto_minimo, regla.monto_maximo):
                    ajuste = PrecioService._calcular_ajuste(regla)
            
            if ajuste:
                reglas_aplicadas.append({
                    'regla_id': regla.id,
                    'nombre': regla.nombre,
                    'tipo': regla.tipo_regla,
                    'tipo_ajuste': regla.tipo_ajuste,
                    'valor_ajuste': ajuste
                })
        
        return reglas_aplicadas

    @staticmethod
    def _regla_aplica_a_articulo(regla, articulo):
        """Verifica si una regla aplica a un artículo específico."""
        # Si la regla no tiene filtros, aplica a todos
        if not regla.linea_articulo and not regla.grupo_articulo:
            return True
        
        # Si tiene línea específica
        if regla.linea_articulo:
            if articulo.grupo.linea_id == regla.linea_articulo_id:
                return True
        
        # Si tiene grupo específico
        if regla.grupo_articulo:
            if articulo.grupo_id == regla.grupo_articulo_id:
                return True
        
        return False

    @staticmethod
    def _cantidad_en_rango(cantidad, minimo, maximo):
        """Verifica si una cantidad está en el rango especificado."""
        if minimo is not None and cantidad < minimo:
            return False
        if maximo is not None and cantidad > maximo:
            return False
        return True

    @staticmethod
    def _monto_en_rango(monto, minimo, maximo):
        """Verifica si un monto está en el rango especificado."""
        if minimo is not None and monto < minimo:
            return False
        if maximo is not None and monto > maximo:
            return False
        return True

    @staticmethod
    def _calcular_ajuste(regla):
        """Calcula el ajuste a aplicar según el tipo de regla."""
        return regla.valor_ajuste

    @staticmethod
    def validar_costo(precio_final, articulo, descuento_proveedor=0):
        """
        Valida que el precio final no sea menor al costo.
        Permite excepciones con descuentos de proveedor del 50-70%.
        
        Args:
            precio_final: Precio calculado
            articulo: Instancia de Articulo
            descuento_proveedor: Porcentaje de descuento del proveedor
            
        Returns:
            dict con es_valido, mensaje, bajo_costo
        """
        costo_con_descuento = articulo.ultimo_costo * (1 - descuento_proveedor / 100)
        
        if precio_final >= articulo.ultimo_costo:
            return {
                'es_valido': True,
                'mensaje': 'Precio válido',
                'bajo_costo': False
            }
        
        # Verificar si está en el rango permitido con descuento de proveedor
        if descuento_proveedor >= 50 and descuento_proveedor <= 70:
            if precio_final >= costo_con_descuento:
                return {
                    'es_valido': True,
                    'mensaje': f'Precio bajo costo autorizado (descuento proveedor: {descuento_proveedor}%)',
                    'bajo_costo': True
                }
        
        return {
            'es_valido': False,
            'mensaje': f'Precio inferior al costo mínimo permitido. Costo: {articulo.ultimo_costo}',
            'bajo_costo': True
        }

    @staticmethod
    def calcular_precio(empresa_id, sucursal_id, articulo_id, canal, cantidad, monto_pedido_total=0):
        """
        Método principal para calcular el precio final de un artículo.
        Sigue la jerarquía: precio base → canal → escala → monto → combinación → validación
        
        Args:
            empresa_id: ID de la empresa
            sucursal_id: ID de la sucursal
            articulo_id: ID del artículo
            canal: Canal de venta
            cantidad: Cantidad de unidades
            monto_pedido_total: Monto total del pedido
            
        Returns:
            dict con precio_base, precio_final, reglas_aplicadas, validacion
        """
        # 1. Obtener lista vigente
        lista_precio = PrecioService.obtener_lista_vigente(empresa_id, sucursal_id, canal)
        
        if not lista_precio:
            return {
                'error': 'No hay lista de precios vigente',
                'precio_base': None,
                'precio_final': None
            }
        
        # 2. Obtener precio base
        precio_info = PrecioService.obtener_precio_base(lista_precio, articulo_id)
        
        if not precio_info:
            return {
                'error': 'Artículo no encontrado en la lista de precios',
                'precio_base': None,
                'precio_final': None
            }
        
        precio_base = precio_info['precio_base']
        precio_final = precio_base
        
        # 3. Obtener artículo
        try:
            articulo = Articulo.objects.get(id=articulo_id)
        except Articulo.DoesNotExist:
            return {
                'error': 'Artículo no encontrado',
                'precio_base': None,
                'precio_final': None
            }
        
        # 4. Aplicar reglas de precio
        reglas_aplicadas = PrecioService.aplicar_reglas(
            lista_precio, articulo, cantidad, monto_pedido_total, canal
        )
        
        # 5. Calcular precio final aplicando ajustes
        for regla in reglas_aplicadas:
            if regla['tipo_ajuste'] == 'PORCENTAJE':
                descuento = precio_final * (regla['valor_ajuste'] / 100)
                precio_final -= descuento
            elif regla['tipo_ajuste'] == 'MONTO_FIJO':
                precio_final -= regla['valor_ajuste']
            elif regla['tipo_ajuste'] == 'PRECIO_FIJO':
                precio_final = regla['valor_ajuste']
        
        # Asegurar que el precio no sea negativo
        precio_final = max(precio_final, Decimal('0.00'))
        
        # 6. Validar contra costo
        validacion = PrecioService.validar_costo(
            precio_final, 
            articulo, 
            precio_info['descuento_proveedor']
        )
        
        return {
            'lista_precio_id': lista_precio.id,
            'lista_precio_nombre': lista_precio.nombre,
            'precio_base': float(precio_base),
            'precio_final': float(precio_final),
            'reglas_aplicadas': reglas_aplicadas,
            'validacion': validacion,
            'bajo_costo': precio_info['bajo_costo'] or validacion['bajo_costo'],
            'descuento_proveedor': float(precio_info['descuento_proveedor']),
            'autorizado_por': precio_info.get('autorizado_por', '')
        }
