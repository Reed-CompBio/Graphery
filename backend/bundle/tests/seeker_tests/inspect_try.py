import inspect
# import tests.multiple_instance_test
from importlib import import_module
# TODO use sys link so that import works propertly
md = import_module('multiple_instance_test')


if __name__ == '__main__':
    # print(inspect.getsource(tests.multiple_instance_test))
    print(inspect.getsource(md))
    # TODO use get source line hack to determine loops
    print(inspect.getsourcelines(md))
