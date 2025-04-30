from django.apps import AppConfig


class OutflowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'outflows'
    verbose_name = 'Saída de produto'
    verbose_name_plural = 'Saída de produtos'

    def ready(self):
        import outflows.signals