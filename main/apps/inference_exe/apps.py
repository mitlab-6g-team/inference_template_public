from django.apps import AppConfig
from main.utils.env_loader import customized_env
from main.apps.inference_exe.services.platform import update_position_status

# write test code here
class InferenceExeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main.apps.inference_exe'

    def ready(self):
        from .services.inference import InferenceService
        
        try: 
            model = InferenceService.load_model()
            test_data = {
                # put the data here as key-value based
            }
            inference_result = model.inference(test_data)
            
        except Exception as e:
            print(f"Error Msg: {str(e)}")
            
        if eval(customized_env.SELF_CHECK_FUNCTION): 
            update_position_status(inference_result["status"])
