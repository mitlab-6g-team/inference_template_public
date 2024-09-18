from django.apps import AppConfig
from main.apps.inference_exe.services.platform import update_position_status

# write test code here
class InferenceExeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main.apps.inference_exe'

    def ready(self):
        from .services.inference import InferenceService
        
        try: 
            InferenceService.load_model()
            update_position_status("InService")
            
        except Exception as e:
            print(f"Error Msg: {str(e)}")
            update_position_status("OutOfService")
