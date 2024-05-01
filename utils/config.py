from dataclasses import dataclass
from os import getenv


@dataclass
class RabbitMQConfig:
    RABBIT_MQ_HOST = getenv("RABBIT_MQ_HOST", "localhost")
    QUEUE_NAME = getenv("QUEUE_NAME", "image_service_queue")
    RABBIT_MQ_EXCHANGE = getenv("RABBIT_MQ_EXCHANGE", "")


@dataclass
class ServerURLS:
    MARIADB_SERVER_URL = getenv("MARIADB_SERVER_URL", "")


@dataclass
class Endpoints:
    CREATE_BATCH = "/create_batch"
    FETCH_IMAGE_LIST = "/fetch_image_list"

