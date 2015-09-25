"""
this model is aim to offer easy http request interface and return string result for later use.
"""
import requests

from data_model import HttpMethod
from data_model import ContentType
from utils.type_checking import type_check


def get(url, params=None, headers=None):
    r = requests.get(url, params=params, headers=headers)
    return r


def post(url, content_type=ContentType.json, body=None, headers={}, files=None):
    if files is not None and len(files) > 0:
        r = requests.post(url, data=body, headers=headers, files=files)
    else:
        headers['content-type'] = 'application/' + content_type.name
        r = requests.post(url, data=body, headers=headers)
    return r


def put(url, content_type=ContentType.json, body=None, headers={}, files=None):
    if files is not None:
        r = requests.put(url, data=body, headers=headers, files=files)
    else:
        headers['content-type'] = 'application/' + content_type.name
        r = requests.put(url, data=body, headers=headers)
    return r


# a delete method only relies on it's url.
def delete(url, headers={}):
    r = requests.get(url, headers=headers)
    return r


@type_check
def request(url, method: HttpMethod = HttpMethod.get, content_type: ContentType = ContentType.json,
            body: dict = None, headers: dict = {}, files: dict = None) -> str:
    if method == HttpMethod.get:
        r = get(url, body, headers)
    elif method == HttpMethod.post:
        r = post(url, content_type, body, headers, files)
    elif method == HttpMethod.put:
        r = put(url, content_type, body, headers, files)
    else:
        r = delete(url, headers)
    r.raise_for_status()
    return r.text


if __name__ == "__main__":
    r = request('http://www.ifhzj.com/api/navigations', HttpMethod.get)
    print(r)
