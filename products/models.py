from django.db import models

class ProductType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Categoria do produto'
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
        verbose_name = 'Categoria do Produto'
        verbose_name_plural = 'Categoria dos Produtos'

    def __str__(self):
        return self.name

class Product(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        related_name='product',
        verbose_name='Tipo do produto',
        on_delete=models.PROTECT
    )

    name_product = models.CharField(
        max_length=200,
        verbose_name='Nome do produto'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
    )

    quantity = models.IntegerField(
        verbose_name='Quantidade',
        default=0
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
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.name_product
    