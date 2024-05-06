"""
InferenceServiceHandler
"""
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from main.utils.logger import log_trigger, log_writer
from main.apps.inference_exe.services.inference import InferenceService
from main.apps.inference_exe.services.kafka import publish

@require_POST
@log_trigger("INFO")
def get_inference_result(request):
    """
    Processes an inference request by extracting the necessary information from the POST request and
    publishing both raw data and the inference result to Kafka topics. This function is responsible for
    generating new inference result based on the provided input value.
    """
    
    request_data = json.loads(request.body.decode('utf-8'))
    is_multi_input = request_data.get('multi_input', False)

    # send raw data to kafka in Agent Layer
    payload = {
        "position_uid": f"{request_data['position_uid']}",
        "packet_uid": f"{request_data['packet_uid']}",
        "inference_client_name": f"{request_data['inference_client_name']}",
        "value": f"{request_data['value']}"
    }
    publish(f"applications.{request_data['application_uid']}", 'raw_data_add', payload)

    # generate inference
    inference_result = InferenceService.inference(request_data['value'], is_multi_input)
    if inference_result['status'] == "success":
        
        payload = {
            "position_uid": f"{request_data['position_uid']}",
            "packet_uid": f"{request_data['packet_uid']}",
            "inference_client_name": f"{request_data['inference_client_name']}",
            "value": inference_result['data']
        }
        publish(f"applications.{request_data['application_uid']}", 'inference_result_add', payload)
        return JsonResponse(inference_result)
    else:
        print(inference_result)
        return JsonResponse(inference_result)


@require_POST
@log_trigger("INFO")
def get_model_info(request):
    """
    Retrieves information about the current inference model and returns it in JSON format.

    Response JSON structure:
    {
        "model_type": "string",  // The class name of the model, e.g., "Sequential".
        "input_shape": "string",  // The expected input shape of the model, formatted as a string, e.g., "(None, 28, 28, 1)".
        "input_dtype": "string",  // Data type of the model input, e.g., "float32".
        "output_shape": "string",  // The shape of the model's output, formatted as a string, e.g., "(None, 10)".
        "layers": [
            {
                "layer_index": "int",  // Index of the layer in the model, starting from 1.
                "name": "string",  // Name of the layer, e.g., "conv2d_22".
                "type": "string",  // Class name of the layer, e.g., "Conv2D".
                "output_shape": "string",  // Output shape of the layer, formatted as a string.
                "number_of_params": "int"  // Number of parameters in the layer.
            }
            // More layers as needed
        ],
        "total_number_of_parameters": "int",  // Total number of parameters in the model, e.g., 1056010.
        "trainable_params": "int",  // Total count of trainable parameters in the model.
        "non_trainable_params": "int"  // Total count of non-trainable parameters in the model.
    }
    """
    model_info = InferenceService.get_model_info()
    formatted_json = json.dumps(model_info, indent=4)
    return HttpResponse(formatted_json, content_type='application/json')
