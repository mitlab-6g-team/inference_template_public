import re
import json
import numpy as np
import tensorflow as tf
from main.utils.env_loader import default_env
from main.utils.logger import log_trigger, log_writer


class Model:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def inference(self, input_nplist):
        result = self.model.predict(input_nplist)
        return result

    def get_input_format(self):
        input_layer = self.model.layers[0]
        return input_layer.input_shape, input_layer.dtype

    def get_output_format(self):
        output_layer = self.model.layers[-1]
        return output_layer.output_shape, output_layer.dtype

    def get_model_summary(self):
        input_shape, input_dtype = self.get_input_format()
        output_shape, _ = self.get_output_format()
        model_info = {
            "model_type": type(self.model).__name__,
            "input_shape": str(input_shape),
            "input_dtype": str(input_dtype),
            "output_shape": str(output_shape),
            "layers": [],
            "total_number_of_parameters": self.model.count_params(),
            "trainable_params": sum([layer.trainable for layer in self.model.layers]),
            "non_trainable_params": sum([not layer.trainable for layer in self.model.layers])
        }

        for index, layer in enumerate(self.model.layers, start=1):
            layer_info = {
                "layer_index": index,
                "name": layer.name,
                "type": type(layer).__name__,
                "output_shape": str(layer.output_shape),
                "number_of_params": layer.count_params()
            }
            model_info["layers"].append(layer_info)

        return model_info
        # return json.dumps(model_info, indent=4)


class InferenceService:
    model = None

    @staticmethod
    def load_model():
        if InferenceService.model is None:
            model_path = default_env.MODEL_SAVE_PATH + default_env.MODEL_FILE_NAME
            print('model_path:', model_path)
            InferenceService.model = Model(model_path)
        return InferenceService.model

    @staticmethod
    def input_data_transform(input_data):
        _, model_input_dtype = InferenceService.model.get_input_format()
        return np.array(input_data).astype(model_input_dtype)

    @staticmethod
    def get_model_info():
        model_info = InferenceService.model.get_model_summary()
        return model_info

    @staticmethod
    def inference(input_data):
        try:
            transform_data = InferenceService.input_data_transform(input_data)
            inference_result = InferenceService.model.inference(transform_data)
            return {"status": "success", "data": str(inference_result.tolist())}

        except ValueError as ve:
            log_writer(log_level='ERROR',
                       func=InferenceService.inference, message=str(ve))
            match = re.search(
                r"Input \d+ of layer.*?is incompatible.*?\n", str(ve))
            if match:
                error_message = match.group(0).strip()
            else:
                error_message = str(ve)

            return {"status": "error", "message": str(error_message)}

        except KeyError as ke:
            log_writer(log_level='ERROR',
                       func=InferenceService.inference, message=str(ke))
            return {"status": "error", "message": "Key 'value' is missing in the input data."}

        except tf.errors.InvalidArgumentError as iae:
            log_writer(log_level='ERROR',
                       func=InferenceService.inference, message=str(iae))
            match = re.search(r"Node:.*", str(iae), re.DOTALL)
            if match:
                error = match.group(0).strip()
            else:
                error = str(iae)

            model_input_shape, _ = InferenceService.model.get_input_format()
            actual_input_shape = str(
                input_data.shape) if input_data is not None else "None"

            error_message = json.dumps({
                'error': error,
                'expected_input_shape': str(model_input_shape),
                'received_input_shape': actual_input_shape
            })
            return {"status": "error", "message": str(error_message)}

        except Exception as e:
            log_writer(log_level='ERROR',
                       func=InferenceService.inference, message=str(e))
            return {"status": "error", "message": str(e)}
