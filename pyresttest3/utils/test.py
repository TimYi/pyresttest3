"""
offer convenient method for tests.
"""
import json
from enum import Enum


class TestConfigJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Enum):
            return o.name
        jo = {}
        for attr in dir(o):
            if not attr.startswith("_"):
                jo[attr] = getattr(o, attr)
        return jo


def to_json(obj):
    encoder = TestConfigJsonEncoder()
    result = encoder.encode(obj)
    return result
