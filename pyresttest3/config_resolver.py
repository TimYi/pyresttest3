"""
This model is aim to resolve all kinds of config file to config.TestConfig
In the future, this model will offer extensible interface. One is (str,type)->TestConfig interface.
The other is (filePath)->TestConfig interface.
"""
import yaml
import urllib.parse
import os.path

from data_model import HttpMethod
from data_model import DataType
from data_model import ContentType
from config import TestConfig


def resolve_yaml(url, content, directory=None):
    config = yaml.safe_load(content)
    test_configs = config["tests"]
    tests = []
    for test_config in test_configs:
        test_url = test_config["url"]
        if not test_url.startswith("http"):
            test_url = urllib.parse.urljoin(url, test_url)
        name = test_config["name"]
        kws = {}
        method = test_config.get("method", "get")
        if method in HttpMethod:
            kws["method"] = HttpMethod[method]
        content_type = test_config.get("type", "json")
        if content_type in ContentType:
            kws["content_type"] = ContentType[content_type]
        if "body" in test_config:
            kws["body"] = test_config["body"]
        if "headers" in test_config:
            kws["headers"] = test_config["headers"]
        if "files" in test_config:
            kws["files"] = test_config["files"]
        data_type = test_config["data_type"]
        if data_type in DataType:
            kws["data_type"] = DataType[data_type]
        if "validates" in test_config:
            kws["validates"] = test_config["validates"]
        if "results" in test_config:
            kws["results"] = test_config["results"]
        test = TestConfig(test_url, name, **kws)
        tests.append(test)
    return tests


def resolve_yaml_file(url, file_path, directory=None):
    if directory is not None:
        file_path = os.path.join(directory, file_path)
    with open(file_path, 'r') as file:
        content = file.read()
    return resolve_yaml(url, content)


def resolve_yaml_files(url, file_paths, directory=None):
    tests = []
    for file_path in file_paths:
        test_list = resolve_yaml_file(url, file_path, directory)
        tests.extend(test_list)
    return tests


if __name__ == "__main__":
    from utils.test import to_json

    tests = resolve_yaml_files("http://github.com", [r"..\test.yaml"])
    result = to_json(tests)
    print(result)
