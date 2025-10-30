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


class GrupoArticuloViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar grupos de artículos"""
    queryset = GrupoArticulo.objects.all()
    serializer_class = GrupoArticuloSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar grupos por línea"""
        queryset = GrupoArticulo.objects.all()
        linea_id = self.request.query_params.get('linea_id', None)
        if linea_id:
            queryset = queryset.filter(linea_id=linea_id)
        return queryset


class ArticuloViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar artículos"""
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Permite filtrar artículos por grupo o línea"""
        queryset = Articulo.objects.all()
        grupo_id = self.request.query_params.get('grupo_id', None)
        linea_id = self.request.query_params.get('linea_id', None)
        
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