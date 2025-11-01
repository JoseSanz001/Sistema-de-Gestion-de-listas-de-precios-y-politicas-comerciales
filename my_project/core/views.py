from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import (
    Empresa, Sucursal, LineaArticulo, GrupoArticulo, Articulo,
    ListaPrecio, PrecioArticulo, ReglaPrecio, CombinacionProducto,
    DetalleOrdenCompraCliente
)
from .serializers import (
    EmpresaSerializer, SucursalSerializer, LineaArticuloSerializer,
    GrupoArticuloSerializer, ArticuloSerializer, ListaPrecioSerializer,
    PrecioArticuloSerializer, ReglaPrecioSerializer, CombinacionProductoSerializer,
    DetalleOrdenCompraClienteSerializer, CalculoPrecioRequestSerializer,
    CalculoPrecioResponseSerializer
)
from .services.precio_service import PrecioService


class EmpresaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar empresas"""
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    # permission_classes = [IsAuthenticated]  # Descomentar para requerir autenticación


class SucursalViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar sucursales"""
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar sucursales por empresa"""
        queryset = Sucursal.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset


class LineaArticuloViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar líneas de artículos"""
    queryset = LineaArticulo.objects.all()
    serializer_class = LineaArticuloSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar líneas por empresa"""
        queryset = LineaArticulo.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        
        return queryset


class GrupoArticuloViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar grupos de artículos"""
    queryset = GrupoArticulo.objects.all()
    serializer_class = GrupoArticuloSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar grupos por empresa y/o línea"""
        queryset = GrupoArticulo.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        linea_id = self.request.query_params.get('linea_id', None)
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        if linea_id:
            queryset = queryset.filter(linea_id=linea_id)
        
        return queryset


class ArticuloViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar artículos"""
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar artículos por empresa, grupo o línea"""
        queryset = Articulo.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        grupo_id = self.request.query_params.get('grupo_id', None)
        linea_id = self.request.query_params.get('linea_id', None)
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        if grupo_id:
            queryset = queryset.filter(grupo_id=grupo_id)
        elif linea_id:
            queryset = queryset.filter(grupo__linea_id=linea_id)
        
        return queryset

class ListaPrecioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar listas de precios"""
    queryset = ListaPrecio.objects.all()
    serializer_class = ListaPrecioSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar listas por empresa o sucursal"""
        queryset = ListaPrecio.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        sucursal_id = self.request.query_params.get('sucursal_id', None)
        activo = self.request.query_params.get('activo', None)
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        if sucursal_id:
            queryset = queryset.filter(sucursal_id=sucursal_id)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def precios(self, request, pk=None):
        """Obtiene todos los precios de artículos de una lista"""
        lista = self.get_object()
        precios = PrecioArticulo.objects.filter(lista_precio=lista)
        serializer = PrecioArticuloSerializer(precios, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reglas(self, request, pk=None):
        """Obtiene todas las reglas de una lista"""
        lista = self.get_object()
        reglas = ReglaPrecio.objects.filter(lista_precio=lista)
        serializer = ReglaPrecioSerializer(reglas, many=True)
        return Response(serializer.data)


class PrecioArticuloViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar precios de artículos"""
    queryset = PrecioArticulo.objects.all()
    serializer_class = PrecioArticuloSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar precios por lista o artículo"""
        queryset = PrecioArticulo.objects.all()
        lista_id = self.request.query_params.get('lista_id', None)
        articulo_id = self.request.query_params.get('articulo_id', None)
        
        if lista_id:
            queryset = queryset.filter(lista_precio_id=lista_id)
        if articulo_id:
            queryset = queryset.filter(articulo_id=articulo_id)
        
        return queryset


class ReglaPrecioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar reglas de precio"""
    queryset = ReglaPrecio.objects.all()
    serializer_class = ReglaPrecioSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar reglas por lista"""
        queryset = ReglaPrecio.objects.all()
        lista_id = self.request.query_params.get('lista_id', None)
        activo = self.request.query_params.get('activo', None)
        
        if lista_id:
            queryset = queryset.filter(lista_precio_id=lista_id)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        
        return queryset


class CombinacionProductoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar combinaciones de productos"""
    queryset = CombinacionProducto.objects.all()
    serializer_class = CombinacionProductoSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar combinaciones por lista"""
        queryset = CombinacionProducto.objects.all()
        lista_id = self.request.query_params.get('lista_id', None)
        
        if lista_id:
            queryset = queryset.filter(lista_precio_id=lista_id)
        
        return queryset


class DetalleOrdenCompraClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar detalles de órdenes"""
    queryset = DetalleOrdenCompraCliente.objects.all()
    serializer_class = DetalleOrdenCompraClienteSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar detalles por número de orden"""
        queryset = DetalleOrdenCompraCliente.objects.all()
        numero_orden = self.request.query_params.get('numero_orden', None)
        
        if numero_orden:
            queryset = queryset.filter(numero_orden=numero_orden)
        
        return queryset


class PrecioCalculoViewSet(viewsets.ViewSet):
    """ViewSet para calcular precios dinámicamente"""
    
    @action(detail=False, methods=['post'])
    def calcular(self, request):
        """
        Calcula el precio final de un artículo según las políticas comerciales.
        
        Request body example:
        {
            "empresa_id": 1,
            "sucursal_id": 1,
            "articulo_id": 1,
            "canal": "TIENDA",
            "cantidad": 10,
            "monto_pedido_total": 5000.00
        }
        """
        # Validar datos de entrada
        request_serializer = CalculoPrecioRequestSerializer(data=request.data)
        
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = request_serializer.validated_data
        
        # Calcular precio usando el servicio
        resultado = PrecioService.calcular_precio(
            empresa_id=validated_data['empresa_id'],
            sucursal_id=validated_data.get('sucursal_id'),
            articulo_id=validated_data['articulo_id'],
            canal=validated_data['canal'],
            cantidad=validated_data['cantidad'],
            monto_pedido_total=validated_data.get('monto_pedido_total', 0)
        )
        
        # Verificar si hubo error
        if 'error' in resultado:
            return Response(
                resultado,
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializar respuesta
        response_serializer = CalculoPrecioResponseSerializer(data=resultado)
        response_serializer.is_valid()
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
# ============================================
# VISTAS PARA FRONTEND (HTML)
# ============================================

from django.shortcuts import render, get_object_or_404
from django.db.models import Count

def home(request):
    """Vista principal del sistema"""
    context = {
        'total_empresas': Empresa.objects.filter(activo=True).count(),
        'total_sucursales': Sucursal.objects.filter(activo=True).count(),
        'total_articulos': Articulo.objects.filter(activo=True).count(),
        'total_listas': ListaPrecio.objects.filter(activo=True).count(),
        'listas_activas': ListaPrecio.objects.filter(activo=True)[:5],
    }
    return render(request, 'core/index.html', context)


def empresas_view(request):
    """Vista de empresas"""
    empresas = Empresa.objects.filter(activo=True).annotate(
        total_sucursales=Count('sucursales'),
        total_listas=Count('listas_precios')
    )
    context = {
        'empresas': empresas,
    }
    return render(request, 'core/empresas.html', context)


def dashboard_empresa(request, empresa_id):
    """Dashboard de una empresa específica"""
    empresa = get_object_or_404(Empresa, id=empresa_id)
    
    context = {
        'empresa': empresa,
        'sucursales': empresa.sucursales.filter(activo=True),
        'listas_precios': empresa.listas_precios.filter(activo=True),
        'total_sucursales': empresa.sucursales.filter(activo=True).count(),
        'total_listas': empresa.listas_precios.filter(activo=True).count(),
    }
    return render(request, 'core/dashboard.html', context)


def calcular_precio_view(request):
    """Vista para calcular precios"""
    empresas = Empresa.objects.filter(activo=True)
    
    resultado = None
    if request.method == 'POST':
        # Procesar el formulario
        empresa_id = request.POST.get('empresa_id')
        sucursal_id = request.POST.get('sucursal_id') or None
        articulo_id = request.POST.get('articulo_id')
        canal = request.POST.get('canal', 'TODOS')
        cantidad = int(request.POST.get('cantidad', 1))
        monto_pedido = float(request.POST.get('monto_pedido_total', 0))
        
        # Calcular precio
        resultado = PrecioService.calcular_precio(
            empresa_id=int(empresa_id),
            sucursal_id=int(sucursal_id) if sucursal_id else None,
            articulo_id=int(articulo_id),
            canal=canal,
            cantidad=cantidad,
            monto_pedido_total=monto_pedido
        )
    
    context = {
        'empresas': empresas,
        'canales': ListaPrecio.CANAL_CHOICES,
        'resultado': resultado,
    }
    return render(request, 'core/calcular_precio.html', context)

class PedidoCalculoViewSet(viewsets.ViewSet):
    """ViewSet para calcular precios de pedidos completos con combinaciones"""
    
    @action(detail=False, methods=['post'])
    def calcular_pedido(self, request):
        """
        Calcula el precio final de un pedido completo evaluando combinaciones.
        
        Request body example:
        {
            "empresa_id": 1,
            "sucursal_id": 1,
            "canal": "TIENDA",
            "items": [
                {"articulo_id": 1, "cantidad": 5},
                {"articulo_id": 2, "cantidad": 3},
                {"articulo_id": 3, "cantidad": 10}
            ]
        }
        """
        try:
            empresa_id = request.data.get('empresa_id')
            sucursal_id = request.data.get('sucursal_id')
            canal = request.data.get('canal', 'TODOS')
            items = request.data.get('items', [])
            
            if not empresa_id or not items:
                return Response(
                    {'error': 'Debe proporcionar empresa_id e items'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calcular monto total del pedido (estimado con costos)
            monto_pedido_total = 0
            for item in items:
                try:
                    articulo = Articulo.objects.get(id=item['articulo_id'])
                    monto_pedido_total += float(articulo.ultimo_costo) * item['cantidad']
                except Articulo.DoesNotExist:
                    pass
            
            # Calcular precio de cada item
            resultados = []
            total_pedido = 0
            
            for item in items:
                resultado = PrecioService.calcular_precio(
                    empresa_id=empresa_id,
                    sucursal_id=sucursal_id,
                    articulo_id=item['articulo_id'],
                    canal=canal,
                    cantidad=item['cantidad'],
                    monto_pedido_total=monto_pedido_total,
                    items_pedido=items  # Pasar todos los items para evaluar combinaciones
                )
                
                if 'error' not in resultado:
                    subtotal = resultado['precio_final'] * item['cantidad']
                    total_pedido += subtotal
                    
                    resultado['cantidad'] = item['cantidad']
                    resultado['subtotal'] = round(subtotal, 2)
                    
                    # Obtener info del artículo
                    try:
                        articulo = Articulo.objects.get(id=item['articulo_id'])
                        resultado['articulo_codigo'] = articulo.codigo
                        resultado['articulo_nombre'] = articulo.nombre
                    except Articulo.DoesNotExist:
                        pass
                
                resultados.append(resultado)
            
            return Response({
                'items': resultados,
                'resumen': {
                    'total_items': len(items),
                    'monto_total': round(total_pedido, 2),
                    'monto_pedido_estimado': round(monto_pedido_total, 2)
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def calcular_pedido_view(request):
    """Vista para calcular pedidos completos"""
    empresas = Empresa.objects.filter(activo=True)
    
    context = {
        'empresas': empresas,
        'canales': ListaPrecio.CANAL_CHOICES,
    }
    return render(request, 'core/calcular_pedido.html', context)