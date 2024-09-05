from main.utils.env_loader import default_env
from main.utils.logger import log_trigger, log_writer

# Model Basic Functions
class Model():
    "Inference Functions"

    def __init__(self, model_path):
        "the function to load model."
        self.model = load_model(model_path)

    def inference(self, input_data):
        "the function to do inference."
        result = self.model.predict(input_data)
        return result

# Called by Actor
class InferenceService():
    model = None

    @staticmethod
    def load_model():
        if InferenceService.model is None:
            model_path = default_env.MODEL_SAVE_PATH + default_env.MODEL_FILE_NAME
            InferenceService.model = Model(model_path)
        return InferenceService.model

    @staticmethod
    def input_data_transform(input_data):
        # data processing here
        transformed_data = input_data
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
