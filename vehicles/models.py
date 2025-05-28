from django.db import models
from customers.models import Customer

class VehiclesType(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nome',
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Tipo de Veículo'
        verbose_name_plural = 'Tipo de Veículos'

    def __str__(self):
        return self.name
    
class BrandTypes(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Marca do carro'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Marca do veículo'
        verbose_name_plural = 'Marcas dos veículos'

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('em_servico', 'Em Manutenção'),
    )
    
    vehicle_type = models.ForeignKey(
        VehiclesType,
        on_delete=models.PROTECT,
        verbose_name='Tipo do Veículo'
    )

    vehicle_name = models.CharField(
        max_length=100,
        verbose_name='Nome do veículo',
    )

    license_plate = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Placa',
        default=0
    )

    brand = models.ForeignKey(
        BrandTypes,
        on_delete=models.PROTECT,
        verbose_name='Marca do veículo'
        )

    color = models.CharField(
        max_length=50,
        verbose_name='Cor do carro',
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='vehicles',
        verbose_name='Proprietário',
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name='Status'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return self.vehicle_name
