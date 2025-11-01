from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, SucursalViewSet, LineaArticuloViewSet,
    GrupoArticuloViewSet, ArticuloViewSet, ListaPrecioViewSet,
    PrecioArticuloViewSet, ReglaPrecioViewSet, CombinacionProductoViewSet,
    DetalleOrdenCompraClienteViewSet, PrecioCalculoViewSet, PedidoCalculoViewSet,
    # Vistas HTML
    home, empresas_view, dashboard_empresa, calcular_precio_view, calcular_pedido_view
)

# Crear el router de DRF
router = DefaultRouter()

# Registrar los ViewSets
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'sucursales', SucursalViewSet, basename='sucursal')
router.register(r'lineas-articulos', LineaArticuloViewSet, basename='linea-articulo')
router.register(r'grupos-articulos', GrupoArticuloViewSet, basename='grupo-articulo')
router.register(r'articulos', ArticuloViewSet, basename='articulo')
router.register(r'listas-precios', ListaPrecioViewSet, basename='lista-precio')
router.register(r'precios-articulos', PrecioArticuloViewSet, basename='precio-articulo')
router.register(r'reglas-precios', ReglaPrecioViewSet, basename='regla-precio')
router.register(r'combinaciones-productos', CombinacionProductoViewSet, basename='combinacion-producto')
router.register(r'ordenes-compra', DetalleOrdenCompraClienteViewSet, basename='orden-compra')
router.register(r'precios', PrecioCalculoViewSet, basename='precio-calculo')
router.register(r'pedidos', PedidoCalculoViewSet, basename='pedido-calculo')

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),
    
    # Rutas HTML Frontend
    path('', home, name='home'),
    path('empresas/', empresas_view, name='empresas'),
    path('empresa/<int:empresa_id>/dashboard/', dashboard_empresa, name='dashboard-empresa'),
    path('calcular-precio/', calcular_precio_view, name='calcular-precio'),
    path('calcular-pedido/', calcular_pedido_view, name='calcular-pedido'),
]