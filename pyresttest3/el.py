"""
el means expression language.
in pyresttest3, el is simply a ${variable_name }, the variable_name should be a result generated from former tests.
Runner from runner model will provide a runtime container, whitch will record result generated by the tests.
Each result will be named like name.result_name. name is name of the test. result is a value in results list.
If the value of a variable is not found, an Exception will be raised and this test will be skipped.
"""
from jinja2 import Template


# _ELRE = "\${\s*([^\s]+)\s*}"
# _REPLACE_FORMAT = "(\${\s*%s\s*})"
# _EXCEPTION_FORMAT = "variable {0} is not in arguments"


# def resolve_el(row_str, args) -> "calculated str":
#    variables = re.findall(_ELRE, test_str)
#    variables = set(variables)
#    for var in variables:
#        if var not in args:
#            raise Exception(_EXCEPTION_FORMAT.format(var))
#        value = args[var]
#        row_str = re.sub(_REPLACE_FORMAT % var, value, row_str)
#    return row_str


def _resolve_str(row_str, args) -> "calculated str":
    """
    resolve el in row str value
    :param row_str:
    :param args: runtime args extracted from former test results
    :return:
    """
    t = Template(row_str)
    return t.render(args)


def _resolve_dict(dic, args):
    """
    resolve a dict, resolve every el in every value.
    :param dic:
    :param args:
    :return: resolved dict
    """
    new_dic = {}
    for key in dic.keys():
        value = dic[key]
        new_dic[key] = resolve(value, args)
    return new_dic


def _resolve_list(ls, args):
    """
    resolve a list, resolve every el in every value.
    :param ls:
    :param args:
    :return: resolved list
    """
    new_list = []
    for i in ls:
        value = resolve(i, args)
        new_list.append(value)
    return new_list


def resolve(value, args):
    if isinstance(value, dict):
        v = _resolve_dict(value, args)
    elif isinstance(value, list):
        v = _resolve_list(value, args)
    elif isinstance(value, str):
        v = _resolve_str(value, args)
    else:
        v = value
    return v


def get_value(name, args):
    """
    this method is used when generation reports. It needs to extract value from runtime args by key witch may be nested.
    :param name:
    :param args:
    :return:
    """
    name = "{{" + name + "}}"
    return _resolve_str(name, args)


if __name__ == "__main__":
    test_str = "test{{one}},test{{two}}, test {{one}}, test {{three.four}}"
    vs = {"one": " is one", "two": " is tow", "three": {"four": "nested"}}
    result = _resolve_str(test_str, vs)
    print(result)
    v = get_value("three.four", vs)
    print(v)
    dic = {"a": "{{one}}", "b": ["{{two}}"], "c": {"three": "{{three.four}}"}}
    print(resolve(dic, vs))