from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Empresa, Sucursal, LineaArticulo, GrupoArticulo, Articulo,
    ListaPrecio, PrecioArticulo, ReglaPrecio, CombinacionProducto,
    DetalleOrdenCompraCliente, Usuario
)

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'empresa', 'rol', 'activo', 'is_staff']
    list_filter = ['activo', 'rol', 'empresa', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'empresa__nombre']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información de Empresa', {
            'fields': ('empresa', 'rol', 'telefono', 'activo')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información de Empresa', {
            'fields': ('empresa', 'rol', 'telefono', 'activo')
        }),
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
    list_display = ['nombre', 'codigo', 'empresa', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'empresa', 'fecha_creacion']
    search_fields = ['nombre', 'codigo', 'empresa__nombre']


@admin.register(GrupoArticulo)
class GrupoArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'empresa', 'linea', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'empresa', 'linea', 'fecha_creacion']
    search_fields = ['nombre', 'codigo', 'empresa__nombre']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filtrar líneas por empresa en el formulario"""
        if db_field.name == "linea":
            if request.GET.get('empresa'):
                kwargs["queryset"] = LineaArticulo.objects.filter(empresa_id=request.GET.get('empresa'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'empresa', 'grupo', 'unidad_medida', 'ultimo_costo', 'activo']
    list_filter = ['activo', 'empresa', 'grupo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'empresa__nombre']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filtrar grupos por empresa en el formulario"""
        if db_field.name == "grupo":
            if request.GET.get('empresa'):
                kwargs["queryset"] = GrupoArticulo.objects.filter(empresa_id=request.GET.get('empresa'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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