import pika

from utils.config import RabbitMQConfig
from utils.logger import logger

from model.MQMessage import MQMessage


class RabbitMQServices:
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=RabbitMQConfig.RABBIT_MQ_HOST))

        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=RabbitMQConfig.QUEUE_NAME)

    def send_message(self, message: MQMessage):
        message_json = message.to_json()
        resp = self._channel.basic_publish(exchange='', routing_key=RabbitMQConfig.QUEUE_NAME, body=message_json)
        logger.debug(f"Pushed message to queue : {resp}")
