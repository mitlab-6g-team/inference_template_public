"""
InferenceServiceHandler
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from main.utils.logger import log_trigger, log_writer
from main.apps.inference_exe.services.inference import InferenceService


@require_POST
@log_trigger("INFO")
def get_inference_result(request):
    """
    Processes an inference request by extracting the necessary information from the POST request and
    publishing both raw data and the inference result to Kafka topics. This function is responsible for
    generating new inference result based on the provided input value.

    REQUEST Format :
    {
        application_uid: "string" , // provided by Inference Host Manager
        position_uid: "string" , // provided by Inference Host Manager
        packet_uid:  "string" , // automatically provided by inference SDK
        inference_client_name:  "string" , // provided by Inference Host Manager
        value: <array, dictionary, int, float, nparray> // self defined
    }

    RESPONSE Format:
    {
        "status": "string" , // self define
        "value": <array, dictionary, int, float, nparray> // self define
    }
    """

    try:
        # convert data format from json to dictionary
        request_data = json.loads(request.body.decode('utf-8'))
        # generate inference
        inference_result = InferenceService.inference(request_data['value'])

        if inference_result['status'] == 'success':
            return JsonResponse(inference_result, status=200)
        else:
            return JsonResponse(inference_result, status=422)

    except json.JSONDecodeError:
        return JsonResponse({
            "status": "error",
            "message": "Invalid JSON in request body"
        }, status=400)

    except KeyError:
        return JsonResponse({
            "status": "error",
            "message": "Missing 'value' key in request data"
        }, status=400)

    except Exception as e:
        log_writer(log_level='ERROR',
                   func=get_inference_result, message=str(e))
        return JsonResponse({
            "status": "error",
            "message": "An unexpected error occurred"
        }, status=500)
