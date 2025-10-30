"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="API de Gestión de Listas de Precios",
        default_version='v1',
        description="""
        API REST para el Sistema de Gestión de Listas de Precios y Políticas Comerciales.
        
        ## Funcionalidades principales:
        
        - **Empresas y Sucursales**: Gestión de empresas y sus sucursales
        - **Catálogo de Productos**: Líneas, grupos y artículos
        - **Listas de Precios**: Múltiples listas por empresa/sucursal
        - **Precios Base**: Precios de artículos por lista
        - **Reglas Comerciales**: Descuentos por canal, volumen, monto
        - **Cálculo Dinámico**: Endpoint para calcular precios finales
        
        ## Endpoint Principal:
        
        **POST /api/precios/calcular/**
        
        Calcula el precio final de un artículo aplicando todas las reglas comerciales.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@empresa.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    
    # Documentación Swagger/OpenAPI
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-root'),  # Página principal
]