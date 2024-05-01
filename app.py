import json
import time

from flask import Flask, request, Response
from flask_cors import CORS

from model.MQMessage import EventTypeEnum, MQMessage

from services.app_services import request_to_create_batch, request_to_fetch_image_list
from services.rabbit_mq_services import RabbitMQServices

from utils.logger import logger

app = Flask(__name__)
CORS(app)

rabbitmq_client = RabbitMQServices()


@app.post("/save_image")
def save_image():
    try:
        req_json = request.json
        image_url = req_json.get("image_url")
        user_id = req_json.get("user_id")

        if not image_url:
            raise ValueError("Image Url is mandatory")

        if not user_id:
            raise ValueError("User ID is mandatory")

        message = MQMessage(
            EventType=EventTypeEnum.SAVE,
            user_id=user_id,
            timestamp=time.time(),
            ImageURL=image_url,
        )

        message.batch_id = request_to_create_batch(event_type=message.EventType, user_id=message.user_id)

        rabbitmq_client.send_message(message)

        return Response(
            status=200,
            response=json.dumps({
                "batch_id": message.batch_id
            })
        )

    except Exception as err:
        logger.error(f"Error in saving image : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "error": err
            })
        )


@app.post("/delete_image_by_id")
def delete_image_by_id():
    try:
        req_json = request.json
        image_id = req_json.get("image_id")
        user_id = req_json.get("user_id")

        if not image_id:
            raise ValueError("Image ID is mandatory")

        if not user_id:
            raise ValueError("User ID is mandatory")

        message = MQMessage(
            EventType=EventTypeEnum.DELETE,
            user_id=user_id,
            timestamp=time.time(),
            image_id=image_id,
        )

        message.batch_id = request_to_create_batch(event_type=message.EventType, user_id=message.user_id)

        rabbitmq_client.send_message(message)

        return Response(
            status=200,
            response=json.dumps({
                "batch_id": message.batch_id
            })
        )

    except Exception as err:
        logger.error(f"Error in deleting image : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "error": err
            })
        )


@app.post("/get_similar_image")
def get_similar_image():
    try:
        req_json = request.json
        image_id = req_json.get("image_id")
        user_id = req_json.get("user_id")

        if not image_id:
            raise ValueError("Image ID is mandatory")

        if not user_id:
            raise ValueError("User ID is mandatory")

        message = MQMessage(
            EventType=EventTypeEnum.SIMILAR,
            user_id=user_id,
            timestamp=time.time(),
            image_id=image_id,
        )

        message.batch_id = request_to_create_batch(event_type=message.EventType, user_id=message.user_id)

        rabbitmq_client.send_message(message)

        return Response(
            status=200,
            response=json.dumps({
                "batch_id": message.batch_id
            })
        )

    except Exception as err:
        logger.error(f"Error in getting similar image : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "error": err
            })
        )


@app.post("/reset_db_and_minio")
def reset_db_and_minio():
    try:
        req_json = request.json
        user_id = req_json.get("user_id")

        if not user_id:
            raise ValueError("User ID is mandatory")

        message = MQMessage(
            EventType=EventTypeEnum.RESET,
            user_id=user_id,
            timestamp=time.time()
        )

        message.batch_id = request_to_create_batch(event_type=message.EventType, user_id=message.user_id)

        rabbitmq_client.send_message(message)

        return Response(
            status=200,
            response=json.dumps({
                "batch_id": message.batch_id
            })
        )

    except Exception as err:
        logger.error(f"Error in Resetting DB and Minio : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "error": err
            })
        )


@app.post("/fetch_image_list")
def fetch_image_list():
    try:
        req_json = request.json
        user_id = req_json.get("user_id")

        if not user_id:
            raise ValueError("User ID is mandatory")

        resp = request_to_fetch_image_list(user_id=user_id)

        return Response(
            status=200,
            response=json.dumps({
                "image_list": resp
            })
        )

    except Exception as err:
        logger.error(f"Error in Fetching image list : {err}")
        return Response(
            status=500,
            response=json.dumps({
                "error": err
            })
        )


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8181)
