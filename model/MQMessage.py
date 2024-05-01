import json
import time
import uuid
from enum import Enum
from dataclasses import dataclass, fields
from typing import Optional


class EventTypeEnum(Enum):
    SAVE = "Save"
    DELETE = "Delete"
    SIMILAR = "Similar"
    RESET = "Reset"


@dataclass
class MQMessage:
    EventType: EventTypeEnum
    timestamp: time
    ImageURL: Optional[str] = None
    image_id: Optional[str] = None
    batch_id: Optional[str] = None
    user_id: Optional[str] = None

    @classmethod
    def from_json(cls, json_data):
        keys = [f.name for f in fields(cls)]
        normal_json_data = {key: json_data[key] for key in json_data if key in keys and key != "EventType"}
        normal_json_data["EventType"] = EventTypeEnum[json_data["EventType"].upper()]
        tmp = cls(**normal_json_data)
        return tmp

    @classmethod
    def return_keys(cls):
        return fields(cls)

    def to_json(self):
        return {
            "EventType": self.EventType.value,
            "timestamp": self.timestamp,
            "ImageURL": self.ImageURL,
            "image_id": self.image_id,
            "batch_id": self.batch_id,
            "user_id": self.user_id
        }
