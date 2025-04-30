from django.apps import AppConfig


class SupplierConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supplier'
    verbose_name = 'Fornecedor'
    verbose_name_plural = 'Fornecedores'
