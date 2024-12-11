import os, json
from confluent_kafka import Producer, KafkaError, KafkaException

def update_position_status(status):
    
    position_uid = os.environ.get('POSITION_UID')
    application_uid = os.environ.get('APPLICATION_UID')
    if status == "InService":
        # update position status
        payload = {
            "position_uid": position_uid,
            "status": "InService",
            "message": "Inference host ready"
        }
    else: 
        # update position status
        payload = {
            "position_uid": position_uid,
            "status": "OutOfService",
            "message": "Error from inference host"
        }

    publish(
        f"applications.{application_uid}", "position_status_modify", payload
    )

def upload_position_data(data_type, packet_uid, inference_client_name, value):
    
    position_uid = os.environ.get('POSITION_UID')
    application_uid = os.environ.get('APPLICATION_UID')
    model_uid = os.environ.get('MODEL_UID')
    
    if data_type == "raw_data":
        # upload raw_data to agent kafka
        payload = {
            "position_uid": position_uid,
            "packet_uid": packet_uid,
            "inference_client_name": inference_client_name,
            "model_uid": model_uid, 
            "value": value
        }
        publish(
            f"applications.{application_uid}", "raw_data_add", payload
        )
    elif data_type == "inference_result":
        # upload inference_result to agent kafka
        payload = {
            "position_uid": position_uid,
            "packet_uid": packet_uid,
            "inference_client_name": inference_client_name,
            "value": value
        }
        
        publish(
            f"applications.{application_uid}", "inference_result_add", payload
        )   

    

def publish(topic_name_str, status_str, message):
    """ Publish the message to the topic in the form of key and value.
    Arguments:
        topic_name_str (string): name of the topic
        status_str (string): the key of the message in the topic
        message (dictionary or str): the value of the message in the topic
        prefix_error_response_str (string): prefix of the error response
    """
    if (not eval(os.environ.get('KAFKA_ENABLE'))):
        return 0
    kafka_ip_str = os.environ.get('DEPLOYMENT_PF_HOST_IP')
    kafka_port_list = os.environ.get('AGENT_KAFKA_PORT').split(',')
    kafka_servers_str = ''
    for i in kafka_port_list:
        kafka_servers_str = kafka_servers_str + f'{kafka_ip_str}:{i},'
    
    prefix_error_response_str = status_str
    response_str = "success"
    status_code_int = 200

    kafka_config = {
        'bootstrap.servers': kafka_servers_str
    }

    try:
        producer = Producer(kafka_config)

        status = status_str.encode()

        if isinstance(message, dict):
            message = json.dumps(message)

        if message is not None:
            message = message.encode()

        producer.produce(topic_name_str, key=status, value=message)

        # 等待所有消息被發送
        producer.flush()

    except KafkaException as error:
        if error.args:
            kafka_error = error.args[0]
            kafka_error_code_int = kafka_error.code()
            if kafka_error_code_int == KafkaError.UNKNOWN_TOPIC_OR_PART:
                response_str = prefix_error_response_str + "UNKNOWN_TOPIC_OR_PART"
                status_code_int = 509
            elif kafka_error_code_int == KafkaError.REQUEST_TIMED_OUT:
                response_str = prefix_error_response_str + "REQUEST_TIMED_OUT"
                status_code_int = 510
            elif kafka_error_code_int == KafkaError._TIMED_OUT:
                response_str = prefix_error_response_str + "TIMED_OUT"
                status_code_int = 511
            elif kafka_error_code_int == KafkaError.TOPIC_AUTHORIZATION_FAILED:
                response_str = prefix_error_response_str + "TOPIC_AUTHORIZATION_FAILED"
                status_code_int = 512
            elif kafka_error_code_int == KafkaError.BROKER_NOT_AVAILABLE:
                response_str = prefix_error_response_str + "BROKER_NOT_AVAILABLE"
                status_code_int = 513
            elif kafka_error_code_int == KafkaError.MSG_SIZE_TOO_LARGE:
                response_str = prefix_error_response_str + "MSG_SIZE_TOO_LARGE"
                status_code_int = 514
            else:
                response_str = kafka_error.str()
                status_code_int = 515

    return response_str, status_code_int
