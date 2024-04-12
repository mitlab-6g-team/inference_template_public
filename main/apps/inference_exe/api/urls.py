from django.urls import path
from main.apps.inference_exe.actors import InferenceServiceHandler

module_name = 'inference_exe'

urlpatterns = [
    path(f'{module_name}/InferenceServiceHandler/get_inference_result', InferenceServiceHandler.get_inference_result),
    path(f'{module_name}/InferenceServiceHandler/get_model_info', InferenceServiceHandler.get_model_info)
]
