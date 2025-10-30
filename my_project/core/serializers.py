from rest_framework import serializers
from .models import (
    Empresa, Sucursal, LineaArticulo, GrupoArticulo, Articulo,
    ListaPrecio, PrecioArticulo, ReglaPrecio, CombinacionProducto,
    DetalleOrdenCompraCliente
)


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class SucursalSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta:
        model = Sucursal
        fields = '__all__'


class LineaArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaArticulo
        fields = '__all__'


class GrupoArticuloSerializer(serializers.ModelSerializer):
    linea_nombre = serializers.CharField(source='linea.nombre', read_only=True)
    
    class Meta:
        model = GrupoArticulo
        fields = '__all__'


class ArticuloSerializer(serializers.ModelSerializer):
    grupo_nombre = serializers.CharField(source='grupo.nombre', read_only=True)
    linea_nombre = serializers.CharField(source='grupo.linea.nombre', read_only=True)
    
    class Meta:
        model = Articulo
        fields = '__all__'


class ListaPrecioSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True, allow_null=True)
    
    class Meta:
        model = ListaPrecio
        fields = '__all__'


class PrecioArticuloSerializer(serializers.ModelSerializer):
    articulo_nombre = serializers.CharField(source='articulo.nombre', read_only=True)
    articulo_codigo = serializers.CharField(source='articulo.codigo', read_only=True)
    lista_precio_nombre = serializers.CharField(source='lista_precio.nombre', read_only=True)
    
    class Meta:
        model = PrecioArticulo
        fields = '__all__'
    
    def validate_precio_base(self, value):
        """Valida que el precio base no sea negativo"""
        if value < 0:
            raise serializers.ValidationError("El precio base no puede ser negativo")
        return value


class ReglaPrecioSerializer(serializers.ModelSerializer):
    lista_precio_nombre = serializers.CharField(source='lista_precio.nombre', read_only=True)
    linea_nombre = serializers.CharField(source='linea_articulo.nombre', read_only=True, allow_null=True)
    grupo_nombre = serializers.CharField(source='grupo_articulo.nombre', read_only=True, allow_null=True)
    
    class Meta:
        model = ReglaPrecio
        fields = '__all__'
    
    def validate(self, data):
        """Validaciones personalizadas para reglas"""
        # Validar rangos de cantidad
        if data.get('cantidad_minima') and data.get('cantidad_maxima'):
            if data['cantidad_minima'] > data['cantidad_maxima']:
                raise serializers.ValidationError(
                    "La cantidad mínima no puede ser mayor que la máxima"
                )
        
        # Validar rangos de monto
        if data.get('monto_minimo') and data.get('monto_maximo'):
            if data['monto_minimo'] > data['monto_maximo']:
                raise serializers.ValidationError(
                    "El monto mínimo no puede ser mayor que el máximo"
                )
        
        return data


class CombinacionProductoSerializer(serializers.ModelSerializer):
    lista_precio_nombre = serializers.CharField(source='lista_precio.nombre', read_only=True)
    linea_nombre = serializers.CharField(source='linea_articulo.nombre', read_only=True, allow_null=True)
    grupo_nombre = serializers.CharField(source='grupo_articulo.nombre', read_only=True, allow_null=True)
    articulos_detalle = ArticuloSerializer(source='articulos', many=True, read_only=True)
    
    class Meta:
        model = CombinacionProducto
        fields = '__all__'


class DetalleOrdenCompraClienteSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(source='empresa.nombre', read_only=True)
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True, allow_null=True)
    articulo_nombre = serializers.CharField(source='articulo.nombre', read_only=True)
    articulo_codigo = serializers.CharField(source='articulo.codigo', read_only=True)
    
    class Meta:
        model = DetalleOrdenCompraCliente
        fields = '__all__'


# Serializer especial para el cálculo de precios
class CalculoPrecioRequestSerializer(serializers.Serializer):
    """Serializer para la petición de cálculo de precio"""
    empresa_id = serializers.IntegerField(required=True)
    sucursal_id = serializers.IntegerField(required=False, allow_null=True)
    articulo_id = serializers.IntegerField(required=True)
    canal = serializers.ChoiceField(
        choices=['TODOS', 'TIENDA', 'ONLINE', 'DISTRIBUIDOR', 'CORPORATIVO'],
        default='TODOS'
    )
    cantidad = serializers.IntegerField(required=True, min_value=1)
    monto_pedido_total = serializers.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        min_value=0
    )


class CalculoPrecioResponseSerializer(serializers.Serializer):
    """Serializer para la respuesta del cálculo de precio"""
    lista_precio_id = serializers.IntegerField(required=False)
    lista_precio_nombre = serializers.CharField(required=False)
    precio_base = serializers.FloatField(required=False)
    precio_final = serializers.FloatField(required=False)
    reglas_aplicadas = serializers.ListField(required=False)
    validacion = serializers.DictField(required=False)
    bajo_costo = serializers.BooleanField(required=False)
    descuento_proveedor = serializers.FloatField(required=False)
    autorizado_por = serializers.CharField(required=False, allow_blank=True)
    error = serializers.CharField(required=False)