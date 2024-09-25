from main.utils.env_loader import default_env
from main.utils.logger import log_trigger, log_writer
import tensorflow as tf
import numpy as np
import os


class Model():
    "Inference Functions"

    def __init__(self, model_path):
        "the function to load model."
        self.model = tf.keras.models.load_model(model_path)

    def inference(self, input_data):
        "the function to do inference."
        result = self.model.predict(input_data)
        return result


class InferenceService():
    model = None

    @staticmethod
    def load_model():
        if InferenceService.model is None:
            extension = os.environ.get('FILE_EXTENSION')
            model_path = default_env.MODEL_SAVE_PATH + f"model{extension}"
            InferenceService.model = Model(model_path)
        return InferenceService.model

    @staticmethod
    def input_data_transform(input_data):
        # data processing here
        input_data = np.array(input_data)

        if input_data.shape != (1, 100, 3):
            raise ValueError(
                f"Expected input shape (1, 100, 3), but got {input_data.shape}")

        transformed_data = input_data.astype(np.float32)
        return transformed_data

    @staticmethod
    def inference(input_data):
        try:
            transform_data = InferenceService.input_data_transform(input_data)
            inference_result = InferenceService.model.inference(transform_data)
            return {"status": "success", "value": str(inference_result.tolist())}

        except Exception as e:
            log_writer(log_level='ERROR',
                       func=InferenceService.inference, message=str(e))
            return {"status": "error", "message": str(e)}
