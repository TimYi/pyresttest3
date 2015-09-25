"""
this model is aim to offer a runtime container for test configs to run. It's an integrate model
"""
import rest_client
from config import TestConfig
import result_resolver


class Runner:
    def __init__(self, test_configs, base_dir=None):
        self.configs = test_configs
        self.dir = base_dir
        self.results = {}

    def __call__(self):
        for config in self.configs:
            self._run(config)

    def _run(self, config: TestConfig):
        config.resolve(self.results)
        result = rest_client.request(config.url, config.method, config.content_type, config.body, config.headers,
                                     config.files)
        resolver = result_resolver.get_resolver(result, config.data_type)
        validate_result = resolver.validate(config.validates)
        if validate_result['result']:
            print('success')
        else:
            print(validate_result)
        result_dic = resolver.get_results(config.results)
        self.results[config.name] = result_dic


if __name__ == "__main__":
    config = TestConfig('http://ifhzj.com/api/navigations', 'test', validates={"status": "200"})
    runner = Runner([config])
    runner()
