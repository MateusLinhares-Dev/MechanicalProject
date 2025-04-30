from django.db import models
from products.models import Product
from django.core.exceptions import ValidationError

class Outflows(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Produto',
        related_name='product_outflow'
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
        verbose_name = 'Saída de produto'
        verbose_name_plural = 'Saída de produtos'

    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError(f"Estoque insuficiente: disponível {self.product.quantity}, tentou remover {self.quantity}.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product)