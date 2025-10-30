from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet, SucursalViewSet, LineaArticuloViewSet,
    GrupoArticuloViewSet, ArticuloViewSet, ListaPrecioViewSet,
    PrecioArticuloViewSet, ReglaPrecioViewSet, CombinacionProductoViewSet,
    DetalleOrdenCompraClienteViewSet, PrecioCalculoViewSet
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

urlpatterns = [
    path('', include(router.urls)),
]