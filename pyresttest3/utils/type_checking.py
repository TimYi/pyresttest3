from functools import wraps

__author__ = 'pc'
"""
TypeChecking provides an decorator to check if input satisfy parameter type constrain.
"""


def type_check(f):
    @wraps(f)
    def checked(*args, **kws):
        for i, name in enumerate(f.__code__.co_varnames):
            argtype = f.__annotations__.get(name)
            # Only check if annotation exists and it is as a type
            if isinstance(argtype, type):
                # First len(args) are positional, after that keywords
                if i < len(args):
                    assert isinstance(args[i], argtype)
                elif name in kws:
                    assert isinstance(kws[name], argtype)
        result = f(*args, **kws)
        returntype = f.__annotations__.get('return')
        if isinstance(returntype, type):
            assert isinstance(result, returntype)
        return result

    return checked
