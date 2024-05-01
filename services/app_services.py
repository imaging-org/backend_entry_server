import time
import uuid

import requests

from utils.config import ServerURLS, Endpoints
from utils.logger import logger
from model.MQMessage import EventTypeEnum


def request_to_create_batch(event_type: EventTypeEnum, user_id: str):
    batch_id = str(uuid.uuid4())
    create_batch_url = f"{ServerURLS.MARIADB_SERVER_URL}{Endpoints.CREATE_BATCH}"

    body = {
        "batch_id": batch_id,
        "created_timestamp": time.time(),
        "event_type": event_type.value,
        "user_id": user_id
    }

    resp = requests.post(
        url=create_batch_url,
        json=body
    )

    if resp.status_code == 200:
        return batch_id

    logger.error(f"Error in creating batch : {resp.content}")
    raise Exception("Error in creating batch")


def request_to_fetch_image_list(user_id: str):
    fetch_image_list_url = f"{ServerURLS.MARIADB_SERVER_URL}{Endpoints.FETCH_IMAGE_LIST}"

    body = {
        "user_id": user_id
    }

    resp = requests.post(
        url=fetch_image_list_url,
        json=body
    )

    if resp.status_code == 200:
        return resp.json()

    logger.error(f"Error in fetching image list : {resp.content}")
    raise Exception("Error in fetching image list")
