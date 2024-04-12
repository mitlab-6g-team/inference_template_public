from django.apps import AppConfig


class InferenceExeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main.apps.inference_exe'

    def ready(self):
        from .services.inference import InferenceService
        InferenceService.load_model()
