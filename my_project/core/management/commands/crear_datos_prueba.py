from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from core.models import (
    Empresa, Sucursal, LineaArticulo, GrupoArticulo, Articulo,
    ListaPrecio, PrecioArticulo, ReglaPrecio
)


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de listas de precios'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando creación de datos de prueba...'))

        # Limpiar datos existentes (opcional - comentar si no quieres borrar)
        self.stdout.write('Limpiando datos existentes...')
        ReglaPrecio.objects.all().delete()
        PrecioArticulo.objects.all().delete()
        ListaPrecio.objects.all().delete()
        Articulo.objects.all().delete()
        GrupoArticulo.objects.all().delete()
        LineaArticulo.objects.all().delete()
        Sucursal.objects.all().delete()
        Empresa.objects.all().delete()

        # 1. Crear Empresas
        self.stdout.write('Creando empresas...')
        empresa1 = Empresa.objects.create(
            nombre='Distribuidora El Sol SAC',
            ruc='20123456789',
            direccion='Av. Principal 123, Lima',
            telefono='01-1234567',
            email='contacto@elsol.com',
            activo=True
        )

        empresa2 = Empresa.objects.create(
            nombre='Comercial La Luna EIRL',
            ruc='20987654321',
            direccion='Jr. Comercio 456, Trujillo',
            telefono='044-123456',
            email='ventas@laluna.com',
            activo=True
        )

        # 2. Crear Sucursales
        self.stdout.write('Creando sucursales...')
        sucursal1 = Sucursal.objects.create(
            empresa=empresa1,
            nombre='Sede Central Lima',
            codigo='SUC-LIM-001',
            direccion='Av. Principal 123, Lima',
            telefono='01-1234567',
            activo=True
        )

        sucursal2 = Sucursal.objects.create(
            empresa=empresa1,
            nombre='Sucursal Callao',
            codigo='SUC-CAL-001',
            direccion='Av. Argentina 789, Callao',
            telefono='01-7654321',
            activo=True
        )

        sucursal3 = Sucursal.objects.create(
            empresa=empresa2,
            nombre='Sede Trujillo',
            codigo='SUC-TRU-001',
            direccion='Jr. Comercio 456, Trujillo',
            telefono='044-123456',
            activo=True
        )

        # 3. Crear Líneas de Artículos
        self.stdout.write('Creando líneas de artículos...')
        linea_abarrotes = LineaArticulo.objects.create(
            nombre='Abarrotes',
            codigo='LIN-001',
            descripcion='Productos de abarrotes y consumo masivo',
            activo=True
        )

        linea_bebidas = LineaArticulo.objects.create(
            nombre='Bebidas',
            codigo='LIN-002',
            descripcion='Bebidas alcohólicas y no alcohólicas',
            activo=True
        )

        linea_limpieza = LineaArticulo.objects.create(
            nombre='Limpieza',
            codigo='LIN-003',
            descripcion='Productos de limpieza y aseo',
            activo=True
        )

        # 4. Crear Grupos de Artículos
        self.stdout.write('Creando grupos de artículos...')
        grupo_arroz = GrupoArticulo.objects.create(
            linea=linea_abarrotes,
            nombre='Arroz',
            codigo='GRP-001',
            descripcion='Arroz de diferentes marcas',
            activo=True
        )

        grupo_fideos = GrupoArticulo.objects.create(
            linea=linea_abarrotes,
            nombre='Fideos',
            codigo='GRP-002',
            descripcion='Fideos y pastas',
            activo=True
        )

        grupo_gaseosas = GrupoArticulo.objects.create(
            linea=linea_bebidas,
            nombre='Gaseosas',
            codigo='GRP-003',
            descripcion='Bebidas gaseosas',
            activo=True
        )

        grupo_detergentes = GrupoArticulo.objects.create(
            linea=linea_limpieza,
            nombre='Detergentes',
            codigo='GRP-004',
            descripcion='Detergentes para ropa',
            activo=True
        )

        # 5. Crear Artículos
        self.stdout.write('Creando artículos...')
        articulos = [
            # Arroz
            Articulo.objects.create(
                grupo=grupo_arroz,
                codigo='ART-001',
                nombre='Arroz Superior x 5kg',
                descripcion='Arroz superior de primera calidad',
                unidad_medida='UND',
                ultimo_costo=Decimal('18.00'),
                activo=True
            ),
            Articulo.objects.create(
                grupo=grupo_arroz,
                codigo='ART-002',
                nombre='Arroz Extra x 1kg',
                descripcion='Arroz extra en bolsa de 1kg',
                unidad_medida='UND',
                ultimo_costo=Decimal('4.50'),
                activo=True
            ),
            # Fideos
            Articulo.objects.create(
                grupo=grupo_fideos,
                codigo='ART-003',
                nombre='Fideos Spaghetti x 500g',
                descripcion='Fideos tipo spaghetti',
                unidad_medida='UND',
                ultimo_costo=Decimal('2.80'),
                activo=True
            ),
            Articulo.objects.create(
                grupo=grupo_fideos,
                codigo='ART-004',
                nombre='Fideos Corbata x 500g',
                descripcion='Fideos tipo corbata',
                unidad_medida='UND',
                ultimo_costo=Decimal('2.90'),
                activo=True
            ),
            # Gaseosas
            Articulo.objects.create(
                grupo=grupo_gaseosas,
                codigo='ART-005',
                nombre='Gaseosa Cola 2L',
                descripcion='Gaseosa sabor cola de 2 litros',
                unidad_medida='UND',
                ultimo_costo=Decimal('5.50'),
                activo=True
            ),
            Articulo.objects.create(
                grupo=grupo_gaseosas,
                codigo='ART-006',
                nombre='Gaseosa Naranja 2L',
                descripcion='Gaseosa sabor naranja de 2 litros',
                unidad_medida='UND',
                ultimo_costo=Decimal('5.20'),
                activo=True
            ),
            # Detergentes
            Articulo.objects.create(
                grupo=grupo_detergentes,
                codigo='ART-007',
                nombre='Detergente en Polvo 1kg',
                descripcion='Detergente para ropa en polvo',
                unidad_medida='UND',
                ultimo_costo=Decimal('8.50'),
                activo=True
            ),
            Articulo.objects.create(
                grupo=grupo_detergentes,
                codigo='ART-008',
                nombre='Detergente Líquido 900ml',
                descripcion='Detergente líquido para ropa',
                unidad_medida='UND',
                ultimo_costo=Decimal('12.00'),
                activo=True
            ),
        ]

        # 6. Crear Listas de Precios
        self.stdout.write('Creando listas de precios...')
        hoy = timezone.now().date()
        
        # Lista General para Empresa 1
        lista_general_emp1 = ListaPrecio.objects.create(
            empresa=empresa1,
            sucursal=None,
            nombre='Lista General 2025',
            tipo='GENERAL',
            canal='TODOS',
            fecha_inicio=hoy - timedelta(days=30),
            fecha_fin=hoy + timedelta(days=335),
            activo=True
        )

        # Lista Mayorista para Sucursal 1
        lista_mayorista_suc1 = ListaPrecio.objects.create(
            empresa=empresa1,
            sucursal=sucursal1,
            nombre='Lista Mayorista - Sede Lima',
            tipo='MAYORISTA',
            canal='DISTRIBUIDOR',
            fecha_inicio=hoy - timedelta(days=15),
            fecha_fin=hoy + timedelta(days=350),
            activo=True
        )

        # Lista Minorista para Sucursal 2
        lista_minorista_suc2 = ListaPrecio.objects.create(
            empresa=empresa1,
            sucursal=sucursal2,
            nombre='Lista Minorista - Callao',
            tipo='MINORISTA',
            canal='TIENDA',
            fecha_inicio=hoy - timedelta(days=10),
            fecha_fin=hoy + timedelta(days=355),
            activo=True
        )

        # 7. Crear Precios de Artículos
        self.stdout.write('Creando precios de artículos...')
        
        # Precios para Lista General
        for articulo in articulos:
            margen = Decimal('1.35')  # 35% de margen
            PrecioArticulo.objects.create(
                lista_precio=lista_general_emp1,
                articulo=articulo,
                precio_base=articulo.ultimo_costo * margen,
                bajo_costo=False,
                descuento_proveedor=Decimal('0.00')
            )

        # Precios para Lista Mayorista (márgenes menores)
        for articulo in articulos:
            margen = Decimal('1.20')  # 20% de margen
            PrecioArticulo.objects.create(
                lista_precio=lista_mayorista_suc1,
                articulo=articulo,
                precio_base=articulo.ultimo_costo * margen,
                bajo_costo=False,
                descuento_proveedor=Decimal('0.00')
            )

        # Precios para Lista Minorista (márgenes mayores)
        for articulo in articulos:
            margen = Decimal('1.50')  # 50% de margen
            PrecioArticulo.objects.create(
                lista_precio=lista_minorista_suc2,
                articulo=articulo,
                precio_base=articulo.ultimo_costo * margen,
                bajo_costo=False,
                descuento_proveedor=Decimal('0.00')
            )

        # 8. Crear Reglas de Precio
        self.stdout.write('Creando reglas de precio...')

        # Regla: Descuento por volumen (Escala de Unidades)
        ReglaPrecio.objects.create(
            lista_precio=lista_mayorista_suc1,
            nombre='Descuento por Volumen - 10 a 50 unidades',
            tipo_regla='ESCALA_UNIDADES',
            tipo_ajuste='PORCENTAJE',
            cantidad_minima=10,
            cantidad_maxima=50,
            valor_ajuste=Decimal('5.00'),  # 5% de descuento
            prioridad=1,
            activo=True
        )

        ReglaPrecio.objects.create(
            lista_precio=lista_mayorista_suc1,
            nombre='Descuento por Volumen - Más de 50 unidades',
            tipo_regla='ESCALA_UNIDADES',
            tipo_ajuste='PORCENTAJE',
            cantidad_minima=51,
            cantidad_maxima=None,
            valor_ajuste=Decimal('10.00'),  # 10% de descuento
            prioridad=1,
            activo=True
        )

        # Regla: Descuento por monto total de pedido
        ReglaPrecio.objects.create(
            lista_precio=lista_general_emp1,
            nombre='Descuento por Pedido Mayor a S/. 1000',
            tipo_regla='MONTO_PEDIDO',
            tipo_ajuste='PORCENTAJE',
            monto_minimo=Decimal('1000.00'),
            monto_maximo=None,
            valor_ajuste=Decimal('3.00'),  # 3% de descuento
            prioridad=2,
            activo=True
        )

        # Regla: Descuento especial para línea de abarrotes
        ReglaPrecio.objects.create(
            lista_precio=lista_minorista_suc2,
            nombre='Promoción Abarrotes - Tienda',
            tipo_regla='CANAL',
            tipo_ajuste='PORCENTAJE',
            linea_articulo=linea_abarrotes,
            valor_ajuste=Decimal('2.00'),  # 2% de descuento
            prioridad=3,
            activo=True
        )

        self.stdout.write(self.style.SUCCESS('✓ Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'  - {Empresa.objects.count()} empresas'))
        self.stdout.write(self.style.SUCCESS(f'  - {Sucursal.objects.count()} sucursales'))
        self.stdout.write(self.style.SUCCESS(f'  - {LineaArticulo.objects.count()} líneas de artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {GrupoArticulo.objects.count()} grupos de artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {Articulo.objects.count()} artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {ListaPrecio.objects.count()} listas de precios'))
        self.stdout.write(self.style.SUCCESS(f'  - {PrecioArticulo.objects.count()} precios de artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {ReglaPrecio.objects.count()} reglas de precio'))