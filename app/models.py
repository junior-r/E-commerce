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

    def __str__(self):
        return self.nombre
