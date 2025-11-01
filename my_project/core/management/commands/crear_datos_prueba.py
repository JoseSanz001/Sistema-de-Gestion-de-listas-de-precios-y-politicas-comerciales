from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from core.models import (
    Empresa, Sucursal, LineaArticulo, GrupoArticulo, Articulo,
    ListaPrecio, PrecioArticulo, ReglaPrecio, CombinacionProducto, Usuario
)


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de listas de precios'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando creación de datos de prueba...'))

        # Limpiar datos existentes
        self.stdout.write('Limpiando datos existentes...')
        CombinacionProducto.objects.all().delete()
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
# 1.5. Crear Usuarios para cada Empresa
        self.stdout.write('Creando usuarios...')
        
        # Usuario Administrador para Empresa 1
        usuario_admin_emp1 = Usuario.objects.create_user(
            username='admin_elsol',
            email='admin@elsol.com',
            password='admin123',
            first_name='Carlos',
            last_name='Administrador',
            empresa=empresa1,
            rol='ADMIN',
            telefono='01-1234567',
            is_staff=True,
            activo=True
        )
        
        # Usuario Gerente para Empresa 1
        usuario_gerente_emp1 = Usuario.objects.create_user(
            username='gerente_elsol',
            email='gerente@elsol.com',
            password='gerente123',
            first_name='María',
            last_name='Gerente',
            empresa=empresa1,
            rol='GERENTE',
            telefono='01-1234568',
            is_staff=True,
            activo=True
        )
        
        # Usuario Vendedor para Empresa 1
        usuario_vendedor_emp1 = Usuario.objects.create_user(
            username='vendedor_elsol',
            email='vendedor@elsol.com',
            password='vendedor123',
            first_name='Juan',
            last_name='Vendedor',
            empresa=empresa1,
            rol='VENDEDOR',
            telefono='01-1234569',
            is_staff=False,
            activo=True
        )
        
        # Usuario Administrador para Empresa 2
        usuario_admin_emp2 = Usuario.objects.create_user(
            username='admin_laluna',
            email='admin@laluna.com',
            password='admin123',
            first_name='Ana',
            last_name='Administrador',
            empresa=empresa2,
            rol='ADMIN',
            telefono='044-123456',
            is_staff=True,
            activo=True
        )
        
        # Usuario Gerente para Empresa 2
        usuario_gerente_emp2 = Usuario.objects.create_user(
            username='gerente_laluna',
            email='gerente@laluna.com',
            password='gerente123',
            first_name='Pedro',
            last_name='Gerente',
            empresa=empresa2,
            rol='GERENTE',
            telefono='044-123457',
            is_staff=True,
            activo=True
        )
        
        # Superusuario sin empresa (puede ver todo)
        superuser = Usuario.objects.create_superuser(
            username='superadmin',
            email='super@admin.com',
            password='super123',
            first_name='Super',
            last_name='Admin',
            empresa=None,
            rol='ADMIN'
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

        # 3. Crear Líneas de Artículos para EMPRESA 1
        self.stdout.write('Creando líneas de artículos para Empresa 1...')
        linea_abarrotes_emp1 = LineaArticulo.objects.create(
            empresa=empresa1,
            nombre='Abarrotes',
            codigo='LIN-001',
            descripcion='Productos de abarrotes y consumo masivo',
            activo=True
        )

        linea_bebidas_emp1 = LineaArticulo.objects.create(
            empresa=empresa1,
            nombre='Bebidas',
            codigo='LIN-002',
            descripcion='Bebidas alcohólicas y no alcohólicas',
            activo=True
        )

        linea_limpieza_emp1 = LineaArticulo.objects.create(
            empresa=empresa1,
            nombre='Limpieza',
            codigo='LIN-003',
            descripcion='Productos de limpieza y aseo',
            activo=True
        )

        # 4. Crear Líneas de Artículos para EMPRESA 2
        self.stdout.write('Creando líneas de artículos para Empresa 2...')
        linea_abarrotes_emp2 = LineaArticulo.objects.create(
            empresa=empresa2,
            nombre='Abarrotes',
            codigo='LIN-001',
            descripcion='Productos de abarrotes',
            activo=True
        )

        linea_lacteos_emp2 = LineaArticulo.objects.create(
            empresa=empresa2,
            nombre='Lácteos',
            codigo='LIN-002',
            descripcion='Productos lácteos',
            activo=True
        )

        # 5. Crear Grupos de Artículos para EMPRESA 1
        self.stdout.write('Creando grupos de artículos para Empresa 1...')
        grupo_arroz_emp1 = GrupoArticulo.objects.create(
            empresa=empresa1,
            linea=linea_abarrotes_emp1,
            nombre='Arroz',
            codigo='GRP-001',
            descripcion='Arroz de diferentes marcas',
            activo=True
        )

        grupo_fideos_emp1 = GrupoArticulo.objects.create(
            empresa=empresa1,
            linea=linea_abarrotes_emp1,
            nombre='Fideos',
            codigo='GRP-002',
            descripcion='Fideos y pastas',
            activo=True
        )

        grupo_gaseosas_emp1 = GrupoArticulo.objects.create(
            empresa=empresa1,
            linea=linea_bebidas_emp1,
            nombre='Gaseosas',
            codigo='GRP-003',
            descripcion='Bebidas gaseosas',
            activo=True
        )

        grupo_detergentes_emp1 = GrupoArticulo.objects.create(
            empresa=empresa1,
            linea=linea_limpieza_emp1,
            nombre='Detergentes',
            codigo='GRP-004',
            descripcion='Detergentes para ropa',
            activo=True
        )

        # 6. Crear Grupos de Artículos para EMPRESA 2
        self.stdout.write('Creando grupos de artículos para Empresa 2...')
        grupo_azucar_emp2 = GrupoArticulo.objects.create(
            empresa=empresa2,
            linea=linea_abarrotes_emp2,
            nombre='Azúcar',
            codigo='GRP-001',
            descripcion='Azúcar blanca y rubia',
            activo=True
        )

        grupo_leche_emp2 = GrupoArticulo.objects.create(
            empresa=empresa2,
            linea=linea_lacteos_emp2,
            nombre='Leche',
            codigo='GRP-002',
            descripcion='Leche entera y descremada',
            activo=True
        )

        # 7. Crear Artículos para EMPRESA 1
        self.stdout.write('Creando artículos para Empresa 1...')
        articulos_emp1 = [
            # Arroz
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_arroz_emp1,
                codigo='ART-001',
                nombre='Arroz Superior x 5kg',
                descripcion='Arroz superior de primera calidad',
                unidad_medida='UND',
                ultimo_costo=Decimal('18.00'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_arroz_emp1,
                codigo='ART-002',
                nombre='Arroz Extra x 1kg',
                descripcion='Arroz extra en bolsa de 1kg',
                unidad_medida='UND',
                ultimo_costo=Decimal('4.50'),
                activo=True
            ),
            # Fideos
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_fideos_emp1,
                codigo='ART-003',
                nombre='Fideos Spaghetti x 500g',
                descripcion='Fideos tipo spaghetti',
                unidad_medida='UND',
                ultimo_costo=Decimal('2.80'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_fideos_emp1,
                codigo='ART-004',
                nombre='Fideos Corbata x 500g',
                descripcion='Fideos tipo corbata',
                unidad_medida='UND',
                ultimo_costo=Decimal('2.90'),
                activo=True
            ),
            # Gaseosas
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_gaseosas_emp1,
                codigo='ART-005',
                nombre='Gaseosa Cola 2L',
                descripcion='Gaseosa sabor cola de 2 litros',
                unidad_medida='UND',
                ultimo_costo=Decimal('5.50'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_gaseosas_emp1,
                codigo='ART-006',
                nombre='Gaseosa Naranja 2L',
                descripcion='Gaseosa sabor naranja de 2 litros',
                unidad_medida='UND',
                ultimo_costo=Decimal('5.20'),
                activo=True
            ),
            # Detergentes
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_detergentes_emp1,
                codigo='ART-007',
                nombre='Detergente en Polvo 1kg',
                descripcion='Detergente para ropa en polvo',
                unidad_medida='UND',
                ultimo_costo=Decimal('8.50'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa1,
                grupo=grupo_detergentes_emp1,
                codigo='ART-008',
                nombre='Detergente Líquido 900ml',
                descripcion='Detergente líquido para ropa',
                unidad_medida='UND',
                ultimo_costo=Decimal('12.00'),
                activo=True
            ),
        ]

        # 8. Crear Artículos para EMPRESA 2
        self.stdout.write('Creando artículos para Empresa 2...')
        articulos_emp2 = [
            Articulo.objects.create(
                empresa=empresa2,
                grupo=grupo_azucar_emp2,
                codigo='ART-001',
                nombre='Azúcar Blanca x 1kg',
                descripcion='Azúcar blanca refinada',
                unidad_medida='UND',
                ultimo_costo=Decimal('3.50'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa2,
                grupo=grupo_azucar_emp2,
                codigo='ART-002',
                nombre='Azúcar Rubia x 1kg',
                descripcion='Azúcar rubia orgánica',
                unidad_medida='UND',
                ultimo_costo=Decimal('4.00'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa2,
                grupo=grupo_leche_emp2,
                codigo='ART-003',
                nombre='Leche Entera 1L',
                descripcion='Leche entera larga vida',
                unidad_medida='UND',
                ultimo_costo=Decimal('4.80'),
                activo=True
            ),
            Articulo.objects.create(
                empresa=empresa2,
                grupo=grupo_leche_emp2,
                codigo='ART-004',
                nombre='Leche Descremada 1L',
                descripcion='Leche descremada light',
                unidad_medida='UND',
                ultimo_costo=Decimal('5.20'),
                activo=True
            ),
        ]

        # 9. Crear Listas de Precios
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

        # Lista Mayorista para Sucursal 1 (Empresa 1)
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

        # Lista para Empresa 2
        lista_general_emp2 = ListaPrecio.objects.create(
            empresa=empresa2,
            sucursal=None,
            nombre='Lista General Trujillo 2025',
            tipo='GENERAL',
            canal='TODOS',
            fecha_inicio=hoy - timedelta(days=20),
            fecha_fin=hoy + timedelta(days=345),
            activo=True
        )

        # 10. Crear Precios de Artículos para EMPRESA 1
        self.stdout.write('Creando precios de artículos para Empresa 1...')
        
        # Precios para Lista General Empresa 1
        for articulo in articulos_emp1:
            margen = Decimal('1.35')  # 35% de margen
            PrecioArticulo.objects.create(
                lista_precio=lista_general_emp1,
                articulo=articulo,
                precio_base=articulo.ultimo_costo * margen,
                bajo_costo=False,
                descuento_proveedor=Decimal('0.00')
            )

        # Precios para Lista Mayorista Empresa 1
        for articulo in articulos_emp1:
            margen = Decimal('1.20')  # 20% de margen
            PrecioArticulo.objects.create(
                lista_precio=lista_mayorista_suc1,
                articulo=articulo,
                precio_base=articulo.ultimo_costo * margen,
                bajo_costo=False,
                descuento_proveedor=Decimal('0.00')
            )

        # 11. Crear Precios de Artículos para EMPRESA 2
        self.stdout.write('Creando precios de artículos para Empresa 2...')
        for articulo in articulos_emp2:
            margen = Decimal('1.40')  # 40% de margen
            PrecioArticulo.objects.create(
                lista_precio=lista_general_emp2,
                articulo=articulo,
                precio_base=articulo.ultimo_costo * margen,
                bajo_costo=False,
                descuento_proveedor=Decimal('0.00')
            )

        # 12. Crear Reglas de Precio para EMPRESA 1
        self.stdout.write('Creando reglas de precio...')

        ReglaPrecio.objects.create(
            lista_precio=lista_mayorista_suc1,
            nombre='Descuento por Volumen - 10 a 50 unidades',
            tipo_regla='ESCALA_UNIDADES',
            tipo_ajuste='PORCENTAJE',
            cantidad_minima=10,
            cantidad_maxima=50,
            valor_ajuste=Decimal('5.00'),
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
            valor_ajuste=Decimal('10.00'),
            prioridad=1,
            activo=True
        )

        ReglaPrecio.objects.create(
            lista_precio=lista_general_emp1,
            nombre='Descuento por Pedido Mayor a S/. 1000',
            tipo_regla='MONTO_PEDIDO',
            tipo_ajuste='PORCENTAJE',
            monto_minimo=Decimal('1000.00'),
            monto_maximo=None,
            valor_ajuste=Decimal('3.00'),
            prioridad=2,
            activo=True
        )

        # 13. Crear Combinaciones de Productos para EMPRESA 1
        self.stdout.write('Creando combinaciones de productos...')
        
        CombinacionProducto.objects.create(
            lista_precio=lista_general_emp1,
            nombre='Combo Abarrotes - 3 productos',
            descripcion='Descuento por compra de 3 o más productos de abarrotes',
            linea_articulo=linea_abarrotes_emp1,
            cantidad_minima=3,
            tipo_descuento='PORCENTAJE',
            valor_descuento=Decimal('5.00'),
            activo=True
        )
        
        combo_bebidas = CombinacionProducto.objects.create(
            lista_precio=lista_mayorista_suc1,
            nombre='Combo Bebidas - 2x1',
            descripcion='Descuento especial por compra de 2 o más gaseosas',
            grupo_articulo=grupo_gaseosas_emp1,
            cantidad_minima=2,
            tipo_descuento='PORCENTAJE',
            valor_descuento=Decimal('8.00'),
            activo=True
        )
        
        combo_pack = CombinacionProducto.objects.create(
            lista_precio=lista_mayorista_suc1,
            nombre='Pack Limpieza Completo',
            descripcion='Pack de detergente + líquido con descuento',
            cantidad_minima=2,
            tipo_descuento='MONTO_FIJO',
            valor_descuento=Decimal('3.00'),
            activo=True
        )
        combo_pack.articulos.add(articulos_emp1[6], articulos_emp1[7])

        self.stdout.write(self.style.SUCCESS('✓ Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'  - {Empresa.objects.count()} empresas'))
        self.stdout.write(self.style.SUCCESS(f'  - {Usuario.objects.count()} usuarios'))
        self.stdout.write(self.style.SUCCESS(f'  - {Sucursal.objects.count()} sucursales'))
        self.stdout.write(self.style.SUCCESS(f'  - {LineaArticulo.objects.count()} líneas de artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {GrupoArticulo.objects.count()} grupos de artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {Articulo.objects.count()} artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {ListaPrecio.objects.count()} listas de precios'))
        self.stdout.write(self.style.SUCCESS(f'  - {PrecioArticulo.objects.count()} precios de artículos'))
        self.stdout.write(self.style.SUCCESS(f'  - {ReglaPrecio.objects.count()} reglas de precio'))
        self.stdout.write(self.style.SUCCESS(f'  - {CombinacionProducto.objects.count()} combinaciones de productos'))

        # Mostrar credenciales de acceso
        self.stdout.write(self.style.SUCCESS('\n=== CREDENCIALES DE ACCESO ==='))
        self.stdout.write(self.style.SUCCESS('Superadmin (acceso total):'))
        self.stdout.write(self.style.SUCCESS('  Usuario: superadmin | Contraseña: super123'))
        self.stdout.write(self.style.SUCCESS('\nDistribuidora El Sol SAC:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin_elsol | Contraseña: admin123'))
        self.stdout.write(self.style.SUCCESS('  Gerente: gerente_elsol | Contraseña: gerente123'))
        self.stdout.write(self.style.SUCCESS('  Vendedor: vendedor_elsol | Contraseña: vendedor123'))
        self.stdout.write(self.style.SUCCESS('\nComercial La Luna EIRL:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin_laluna | Contraseña: admin123'))
        self.stdout.write(self.style.SUCCESS('  Gerente: gerente_laluna | Contraseña: gerente123'))