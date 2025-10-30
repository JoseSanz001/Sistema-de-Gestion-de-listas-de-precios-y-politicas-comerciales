from django.contrib import admin
from .models import (
    Empresa, Sucursal, LineaArticulo, GrupoArticulo, Articulo,
    ListaPrecio, PrecioArticulo, ReglaPrecio, CombinacionProducto,
    DetalleOrdenCompraCliente
)


#Username (leave blank to use 'joses'): admin
#Email address: admin@gmail.com 
#Password: admin

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ruc', 'telefono', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'ruc']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'empresa', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'empresa', 'fecha_creacion']
    search_fields = ['nombre', 'codigo']


@admin.register(LineaArticulo)
class LineaArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'codigo']


@admin.register(GrupoArticulo)
class GrupoArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'linea', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'linea', 'fecha_creacion']
    search_fields = ['nombre', 'codigo']


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'grupo', 'unidad_medida', 'ultimo_costo', 'activo']
    list_filter = ['activo', 'grupo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre']


@admin.register(ListaPrecio)
class ListaPrecioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'sucursal', 'tipo', 'canal', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['activo', 'tipo', 'canal', 'empresa', 'fecha_inicio']
    search_fields = ['nombre']
    date_hierarchy = 'fecha_inicio'


@admin.register(PrecioArticulo)
class PrecioArticuloAdmin(admin.ModelAdmin):
    list_display = ['articulo', 'lista_precio', 'precio_base', 'bajo_costo', 'descuento_proveedor']
    list_filter = ['bajo_costo', 'lista_precio', 'fecha_creacion']
    search_fields = ['articulo__nombre', 'articulo__codigo']


@admin.register(ReglaPrecio)
class ReglaPrecioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'lista_precio', 'tipo_regla', 'tipo_ajuste', 'valor_ajuste', 'prioridad', 'activo']
    list_filter = ['activo', 'tipo_regla', 'tipo_ajuste', 'lista_precio']
    search_fields = ['nombre']


@admin.register(CombinacionProducto)
class CombinacionProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'lista_precio', 'cantidad_minima', 'tipo_descuento', 'valor_descuento', 'activo']
    list_filter = ['activo', 'tipo_descuento', 'lista_precio']
    search_fields = ['nombre']
    filter_horizontal = ['articulos']


@admin.register(DetalleOrdenCompraCliente)
class DetalleOrdenCompraClienteAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'articulo', 'cantidad', 'precio_unitario', 'subtotal', 'bajo_costo', 'fecha_orden']
    list_filter = ['bajo_costo', 'empresa', 'fecha_orden']
    search_fields = ['numero_orden', 'articulo__nombre']
    date_hierarchy = 'fecha_orden'