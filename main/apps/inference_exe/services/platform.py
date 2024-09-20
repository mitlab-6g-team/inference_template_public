import os
import requests
from main.utils.env_loader import customized_env


def update_position_status(status):

    POSITION_UID = os.environ.get('POSITION_UID')
    DEPLOYMENT_PF_HOST_IP = os.environ.get('DEPLOYMENT_PF_HOST_IP')

    payload = {
        "position_uid": POSITION_UID,
        "status": status
    }
    url = f"http://{DEPLOYMENT_PF_HOST_IP}/api/{customized_env.DEPLOYMENT_PLATFORM_VERSION}/inference_operation/PositionManager/update"
    headers = {'Accept': 'application/json'}
    requests.post(url, json=payload, headers=headers)
