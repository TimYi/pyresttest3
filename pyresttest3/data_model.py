from enum import Enum


class HttpMethod(Enum):
    get = 1
    post = 2
    put = 3
    delete = 4


class DataType(Enum):
    json = 1
    html = 2


class ContentType(Enum):
    json = 1
    xml = 2

