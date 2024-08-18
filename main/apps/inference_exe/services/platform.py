import requests
from main.utils.env_loader import customized_env

def update_position_status(inference_result):
    
    if inference_result == "success":
        status="InService"
    else: 
        status="OutofService"
    
    payload={
        "application_uid": customized_env.APPLICATION_UID,
        "position_uid": customized_env.POSITION_UID,
        "status": status
    }
    url = f"http://{customized_env.DEPLOYMENT_PLATFORM_HOST}/api/{customized_env.DEPLOYMENT_PLATFORM_VERSION}/abstract_metadata/PositionMetadataWriter/update"  
    headers = {'Accept': 'application/json'}
    requests.post(url, json=payload, headers=headers)