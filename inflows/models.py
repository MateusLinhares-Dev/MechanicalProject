from django.db import models
from supplier.models import Supplier
from products.models import Product

class Inflows(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='supplier',
        verbose_name='Fornecedor'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Produto',
        related_name='product_inflow'
    )

    quantity = models.IntegerField(
        verbose_name='Quantidade'
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
        ordering = ['-created_at']
        verbose_name = 'Entrada de produto'
        verbose_name_plural = 'Entrada de produtos'

    def __str__(self):
        return str(self.product)