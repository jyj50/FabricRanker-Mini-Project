from django.apps import AppConfig


class FabricPredictionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fabricranker"
    verbose_name = "옷 재질 예측"
