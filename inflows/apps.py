from django.apps import AppConfig


class InflowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inflows'
    verbose_name = 'Entrada de produto'
    verbose_name_plural = 'Entrada de produtos'

    def ready(self):
        import inflows.signals