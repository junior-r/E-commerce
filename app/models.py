from django.db import models

# Create your models here.


class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Talla(models.Model):
    talla = models.CharField(max_length=5)

    def __str__(self):
        return f'Talla: {self.talla}'

    class Meta:
        ordering = ('id',)


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField()
    imagen = models.ImageField(upload_to='productos', null=True)
    talla = models.ManyToManyField(Talla, related_name='Talla')
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
