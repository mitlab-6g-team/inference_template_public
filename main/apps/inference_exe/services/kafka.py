""" Purpose: Publish messages to a topic.
Function Name:
1. publish
"""
import json
from confluent_kafka import Producer, KafkaError, KafkaException
from main.utils.env_loader import default_env

def publish(prefix_error_response_str, topic_name_str, status_str, message):
    """ Publish the message to the topic in the form of key and value.
    Arguments:
        topic_name_str (string): name of the topic
        status_str (string): the key of the message in the topic
        message (dictionary or str): the value of the message in the topic
        prefix_error_response_str (string): prefix of the error response
    """
    kafka_ip_str = default_env.HTTP_KAFKA_HOST
    kafka_port1_str = default_env.HTTP_KAFKA_PORT1
    kafka_port2_str = default_env.HTTP_KAFKA_PORT2
    kafka_port3_str = default_env.HTTP_KAFKA_PORT3
    kafka_servers_str = f'{kafka_ip_str}:{kafka_port1_str}, {kafka_ip_str}:{kafka_port2_str}, {kafka_ip_str}:{kafka_port3_str}'

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

        producer.produce(topic_name_str, key = status, value = message)

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
