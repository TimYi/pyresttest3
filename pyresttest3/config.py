"""
this model is aim to offer an abstract config protocol.
"""

from utils.type_checking import type_check
from data_model import HttpMethod
from data_model import DataType
from data_model import ContentType
import el


class TestConfig:
    @type_check
    def __init__(self, url: str, name, method: HttpMethod = HttpMethod.get,
                 content_type: ContentType = ContentType.json, body: dict = {}, headers: dict = {},
                 files: dict = {}, data_type: DataType = DataType.json, validates: dict = {}, results: dict = {}):
        """
        create a TestConfig
        :param url: absolute url
        :param name: name of this test, may be used as namespace
        :param method: http method in ["get","post","delete","put"], not case sensitive
        :param body: a dict contains request parameters
        :param headers: a dict contains request headers
        :param files: files to upload, if not empty, test method should be multi-part
        :param data_type: response data type in ["json", "html"], not case sensitive
        :param validates: a dict contains key-values to validate. every variable extract from response by key should equal value
        :param results: results to extract for later test to use by el. a el is formed like: ${variable_name }
        :return: TestConfig
        """

        self.url = url
        self.name = name
        self.method = method
        self.content_type = content_type
        self.body = body
        self.headers = headers
        self.files = files
        self.data_type = data_type
        self.validates = validates
        self.results = results

    def resolve(self, args):
        self.url = el.resolve(self.url, args)
        self.body = el.resolve(self.body, args)
        self.headers = el.resolve(self.headers, args)
        self.validates = el.resolve(self.validates, args)


if __name__ == "__main__":
    from config import TestConfig
    from utils.test import to_json


    def test_resolve():
        test_config = TestConfig('http://www.{{a}}', 'test',
                                 body={"key1": "{{b}}", "key2": ["{{c}}", {"key3": "{{d.e}}"}]})
        args = {"a": "variable_a", "b": "variable_b", "c": "variable_c", "d": {"e": "variable_e"}}
        test_config.resolve(args)
        result = to_json(test_config)
        print(result)


    test_resolve()
