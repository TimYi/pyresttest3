"""
this model is aim to resolve http response string. If a http request is failer, rest_client model should raise an
Exception. This model only resolve success response.
It will offer interface for result validates, return meaningful validate result for further use.
It will also offer interface for result extract. The result will be a dict.
"""

import abc
import json

from bs4 import BeautifulSoup

import el

from data_model import DataType


def _extract_nested_key(key: str, source):
    keys = key.split('.')
    value = source
    for k in keys:
        value = getattr(value, k)
    return value


class Resolver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, content: str):
        pass

    @abc.abstractmethod
    def _get_value(self, key: str) -> object:
        pass

    def validate(self, validates: dict) -> dict:
        """

        :param validates: dict indicates key-values to validate
        :return: a dict, first key is 'result' True or False. second key is 'error': {key:{expected_value:'',real_value:''}}
         indicates values not expected.
        """
        for key in validates.keys():
            expected_value = validates[key]
            value = self._get_value(key)
            if expected_value != value:
                return Resolver._validate_error(key, expected_value, value)
        return Resolver._validate_success()

    def get_results(self, results: dict) -> dict:
        extracted_result = {}
        for key in results.keys():
            alias = results[key]
            value = self._get_value(key)
            extracted_result[alias] = value
        return extracted_result

    @classmethod
    def _validate_error(cls, key, expected_value, value) -> dict:
        return {"result": False, "error": {key: {"expected_value": expected_value, "value": value}}}

    @classmethod
    def _validate_success(cls) -> dict:
        return {"result": True}


class _JsonResolver(Resolver):
    def __init__(self, content: str):
        self.content = json.loads(content)

    def _get_value(self, key: str):
        return el.get_value(key, self.content)


class _HtmlResolver(Resolver):
    def __init__(self, content):
        self.content = BeautifulSoup(content, 'html.parser')

    def _get_value(self, key: str):
        return _extract_nested_key(key, self.content)


_resolver_map = {DataType.json: _JsonResolver, DataType.html: _HtmlResolver}


def get_resolver(content, data_type: DataType) -> Resolver:
    resolver_class = _resolver_map[data_type]
    return resolver_class(content)


if __name__ == "__main__":
    html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
</body>
</html>
"""
    resolver = get_resolver(html_doc, DataType.html)
    key = "html.body.p"
    results = {key: "alias"}
    print(resolver.get_results(results))

    json_str = json.dumps({"html": {"body": {"p": "jsonp"}}})
    resolver = get_resolver(json_str, DataType.json)
    print(resolver.get_results(results))
