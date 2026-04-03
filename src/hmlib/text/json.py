from ..dynamic_object import DynamicObject
import json


class Json:
    @classmethod
    def parse(cls, json_text: str) -> DynamicObject:
        return DynamicObject(json.loads(json_text))

    @classmethod
    def to_json(cls, obj: object) -> str:
        return json.dumps(obj)
