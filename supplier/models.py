from django.db import models

class Supplier(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Nome do Fornecedor'
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
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'

    def __str__(self):
        return self.name