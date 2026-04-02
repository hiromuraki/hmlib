from ..DynamicObject import DynamicObject
import json


class Json:
    @classmethod
    def parse_file(cls, json_filepath: str) -> DynamicObject:
        with open(json_filepath, "r", encoding="utf8") as fp:
            return DynamicObject(json.loads(fp.read()))

    @classmethod
    def to_json(cls, obj: object) -> str:
        return json.dumps(obj)
