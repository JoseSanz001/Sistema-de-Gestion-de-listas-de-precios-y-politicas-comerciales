from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Empresa(models.Model):
    """Modelo para representar empresas"""
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    """Modelo para representar sucursales de empresas"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='sucursales')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=20, unique=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sucursal'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return f"{self.empresa.nombre} - {self.nombre}"


class LineaArticulo(models.Model):
    """Modelo para representar líneas de artículos por empresa"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='lineas_articulos')  # NUEVO
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'linea_articulo'
        verbose_name = 'Línea de Artículo'
        verbose_name_plural = 'Líneas de Artículos'
        unique_together = ['empresa', 'codigo']  # Código único por empresa

    def __str__(self):
        return f"{self.empresa.nombre} - {self.nombre}"


class GrupoArticulo(models.Model):
    """Modelo para representar grupos de artículos por empresa"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='grupos_articulos')  # NUEVO
    linea = models.ForeignKey(LineaArticulo, on_delete=models.CASCADE, related_name='grupos')
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'grupo_articulo'
        verbose_name = 'Grupo de Artículo'
        verbose_name_plural = 'Grupos de Artículos'
        unique_together = ['empresa', 'codigo']  # Código único por empresa

    def __str__(self):
        return f"{self.empresa.nombre} - {self.linea.nombre} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        # Validar que la línea pertenezca a la misma empresa
        if self.linea.empresa != self.empresa:
            raise ValueError("La línea debe pertenecer a la misma empresa")
        super().save(*args, **kwargs)


class Articulo(models.Model):
    """Modelo para representar artículos/productos por empresa"""
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='articulos')  # NUEVO
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.CASCADE, related_name='articulos')
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(max_length=20, default='UND')
    ultimo_costo = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articulo'
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        unique_together = ['empresa', 'codigo']  # Código único por empresa

    def __str__(self):
        return f"{self.empresa.nombre} - {self.codigo} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        # Validar que el grupo pertenezca a la misma empresa
        if self.grupo.empresa != self.empresa:
            raise ValueError("El grupo debe pertenecer a la misma empresa")
        super().save(*args, **kwargs)

class ListaPrecio(models.Model):
    """Modelo para listas de precios por empresa/sucursal"""
    TIPO_LISTA_CHOICES = [
        ('GENERAL', 'General'),
        ('MAYORISTA', 'Mayorista'),
        ('MINORISTA', 'Minorista'),
        ('ESPECIAL', 'Especial'),
    ]
    
    CANAL_CHOICES = [
        ('TODOS', 'Todos'),
        ('TIENDA', 'Tienda Física'),
        ('ONLINE', 'Online'),
        ('DISTRIBUIDOR', 'Distribuidor'),
        ('CORPORATIVO', 'Corporativo'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='listas_precios')
    sucursal = models.ForeignKey(
        Sucursal, 
        on_delete=models.CASCADE, 
        related_name='listas_precios',
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_LISTA_CHOICES, default='GENERAL')
    canal = models.CharField(max_length=20, choices=CANAL_CHOICES, default='TODOS')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lista_precio'
        verbose_name = 'Lista de Precio'
        verbose_name_plural = 'Listas de Precios'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"


class PrecioArticulo(models.Model):
    """Precio base de artículos en una lista"""
    lista_precio = models.ForeignKey(ListaPrecio, on_delete=models.CASCADE, related_name='precios')
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='precios')
    precio_base = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    bajo_costo = models.BooleanField(default=False)
    descuento_proveedor = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    autorizado_por = models.CharField(max_length=200, blank=True)
    fecha_autorizacion = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'precio_articulo'
        verbose_name = 'Precio de Artículo'
        verbose_name_plural = 'Precios de Artículos'
        unique_together = ['lista_precio', 'articulo']

    def __str__(self):
        return f"{self.articulo.nombre} - {self.precio_base}"


class ReglaPrecio(models.Model):
    """Reglas de pricing dinámico"""
    TIPO_REGLA_CHOICES = [
        ('CANAL', 'Por Canal de Venta'),
        ('ESCALA_UNIDADES', 'Por Escala de Unidades'),
        ('ESCALA_MONTO', 'Por Escala de Monto'),
        ('MONTO_PEDIDO', 'Por Monto Total del Pedido'),
        ('COMBINACION', 'Por Combinación de Productos'),
    ]
    
    TIPO_AJUSTE_CHOICES = [
        ('PORCENTAJE', 'Porcentaje de Descuento'),
        ('MONTO_FIJO', 'Monto Fijo de Descuento'),
        ('PRECIO_FIJO', 'Precio Fijo'),
    ]

    lista_precio = models.ForeignKey(ListaPrecio, on_delete=models.CASCADE, related_name='reglas')
    nombre = models.CharField(max_length=200)
    tipo_regla = models.CharField(max_length=20, choices=TIPO_REGLA_CHOICES)
    tipo_ajuste = models.CharField(max_length=20, choices=TIPO_AJUSTE_CHOICES, default='PORCENTAJE')
    
    # Filtros opcionales
    linea_articulo = models.ForeignKey(
        LineaArticulo, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='reglas_precio'
    )
    grupo_articulo = models.ForeignKey(
        GrupoArticulo, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='reglas_precio'
    )
    
    # Condiciones
    cantidad_minima = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    cantidad_maxima = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    monto_minimo = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    monto_maximo = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    # Ajuste a aplicar
    valor_ajuste = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    prioridad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'regla_precio'
        verbose_name = 'Regla de Precio'
        verbose_name_plural = 'Reglas de Precios'
        ordering = ['prioridad']

    def __str__(self):
        return f"{self.nombre} - {self.tipo_regla}"


class CombinacionProducto(models.Model):
    """Combinaciones de productos para reglas especiales"""
    lista_precio = models.ForeignKey(ListaPrecio, on_delete=models.CASCADE, related_name='combinaciones')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    # Se puede definir por línea, grupo o artículos específicos
    linea_articulo = models.ForeignKey(
        LineaArticulo, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    grupo_articulo = models.ForeignKey(
        GrupoArticulo, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    articulos = models.ManyToManyField(Articulo, blank=True, related_name='combinaciones')
    
    cantidad_minima = models.IntegerField(validators=[MinValueValidator(1)])
    tipo_descuento = models.CharField(
        max_length=20,
        choices=[('PORCENTAJE', 'Porcentaje'), ('MONTO_FIJO', 'Monto Fijo')],
        default='PORCENTAJE'
    )
    valor_descuento = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'combinacion_producto'
        verbose_name = 'Combinación de Producto'
        verbose_name_plural = 'Combinaciones de Productos'

    def __str__(self):
        return self.nombre


class DetalleOrdenCompraCliente(models.Model):
    """Detalle de órdenes de compra de clientes"""
    numero_orden = models.CharField(max_length=50)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    lista_precio = models.ForeignKey(ListaPrecio, on_delete=models.CASCADE)
    
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    reglas_aplicadas = models.TextField(blank=True)  # JSON con las reglas aplicadas
    bajo_costo = models.BooleanField(default=False)
    
    fecha_orden = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'detalle_orden_compra_cliente'
        verbose_name = 'Detalle de Orden de Compra'
        verbose_name_plural = 'Detalles de Órdenes de Compra'

    def __str__(self):
        return f"Orden {self.numero_orden} - {self.articulo.nombre}"