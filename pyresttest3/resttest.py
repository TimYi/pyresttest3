#!/usr/bin/env python
import sys
import argparse
import yaml

import config_resolver
from runner import Runner


def main(args):
    url = args.url
    test_files = args.test_files
    base_dir = args.dir
    test_configs = config_resolver.resolve_yaml_files(url, test_files, base_dir)
    runner = Runner(test_configs)
    runner()


def command_line_run():
    parser = argparse.ArgumentParser(usage="usage: %(prog)s base_url test_filename.yaml [options]")
    parser.add_argument('url', help='url where the rest service locate')
    parser.add_argument('test_files', nargs="+", help='test files ')
    parser.add_argument('--dir', dest='dir', nargs="+", help='test files ')
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    class TempConfig:
        def __init__(self):
            self.url = None
            self.test_files = None
            self.dir = None


    args = TempConfig()
    args.url = "http://ifhzj.com"
    args.test_files = ["test.yaml"]
    args.dir = r"E:\python\pyresttest3"
    main(args)
