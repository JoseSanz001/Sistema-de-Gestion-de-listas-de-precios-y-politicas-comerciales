# Sistema de Gestión de Listas de Precios y Políticas Comerciales

Sistema integral para la gestión de listas de precios y políticas comerciales dinámicas en empresas de distribución.

## Características

- ✅ Gestión de empresas y sucursales
- ✅ Catálogo de productos con líneas y grupos
- ✅ Múltiples listas de precios por empresa/sucursal
- ✅ Reglas de precio dinámicas:
  - Por canal de venta
  - Por escala de unidades
  - Por monto de pedido
  - Por combinación de productos
- ✅ Validación de precios contra costo
- ✅ Soporte para descuentos especiales de proveedores
- ✅ API REST completa
- ✅ Documentación Swagger/OpenAPI

## Tecnologías

- Python 3.x
- Django 5.x
- Django REST Framework
- PostgreSQL
- drf-yasg (Documentación API)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd GESTIONLISTASPEDIDOS
```

### 2. Crear entorno virtual
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Edita `my_project/settings.py` con tus credenciales de PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_listas_precios',
        'USER': 'postgres',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Crear base de datos en PostgreSQL
```sql
CREATE DATABASE gestion_listas_precios;
```

### 6. Ejecutar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario
```bash
python manage.py createsuperuser
```

### 8. Cargar datos de prueba (opcional)
```bash
python manage.py crear_datos_prueba
```

### 9. Iniciar servidor
```bash
python manage.py runserver
```

## URLs Principales

- **Admin Django:** http://127.0.0.1:8000/admin/
- **API Root:** http://127.0.0.1:8000/api/
- **Documentación Swagger:** http://127.0.0.1:8000/swagger/
- **Documentación ReDoc:** http://127.0.0.1:8000/redoc/

## Endpoints Principales

### Catálogo
- `GET /api/empresas/` - Lista de empresas
- `GET /api/sucursales/` - Lista de sucursales
- `GET /api/articulos/` - Lista de artículos
- `GET /api/lineas-articulos/` - Líneas de productos
- `GET /api/grupos-articulos/` - Grupos de productos

### Precios
- `GET /api/listas-precios/` - Listas de precios
- `GET /api/precios-articulos/` - Precios base de artículos
- `GET /api/reglas-precios/` - Reglas comerciales

### Cálculo de Precios
- `POST /api/precios/calcular/` - Calcula precio final

**Ejemplo de request:**
```json
{
    "empresa_id": 1,
    "sucursal_id": 1,
    "articulo_id": 1,
    "canal": "DISTRIBUIDOR",
    "cantidad": 25,
    "monto_pedido_total": 0
}
```

**Ejemplo de response:**
```json
{
    "lista_precio_id": 2,
    "lista_precio_nombre": "Lista Mayorista - Sede Lima",
    "precio_base": 21.6,
    "precio_final": 20.52,
    "reglas_aplicadas": [
        {
            "regla_id": 1,
            "nombre": "Descuento por Volumen - 10 a 50 unidades",
            "tipo": "ESCALA_UNIDADES",
            "tipo_ajuste": "PORCENTAJE",
            "valor_ajuste": "5.00"
        }
    ],
    "validacion": {
        "es_valido": true,
        "mensaje": "Precio válido",
        "bajo_costo": false
    }
}
```

## Estructura del Proyecto
```
GESTIONLISTASPEDIDOS/
├── core/                          # Aplicación principal
│   ├── management/
│   │   └── commands/
│   │       └── crear_datos_prueba.py
│   ├── services/
│   │   └── precio_service.py     # Lógica de negocio
│   ├── models.py                  # Modelos de datos
│   ├── serializers.py             # Serializers DRF
│   ├── views.py                   # ViewSets API
│   ├── admin.py                   # Configuración admin
│   └── urls.py                    # URLs de la app
├── my_project/                    # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Autores

Sánchez Flores Jose 
