#-*-coding:utf-8-*-

import unittest
import types

def both_instance_of(first, second, klass):
    return isinstance(first, klass) and isinstance(second, klass)

def update_function(old_func, new_func):
    if not both_instance_of(old_func, new_func, types.FunctionType):
        return

    if len(old_func.__code__.co_freevars) != len(new_func.__code__.co_freevars):
        return
    old_func.__doc__ = new_func.__doc__
    old_func.__dict__ = new_func.__dict__
    old_func.__defaults__ = new_func.__defaults__
    old_func.__code__ = new_func.__code__
    if not old_func.__closure__ or not new_func.__closure__:
        return
    for old_cell , new_cell in zip(old_func.__closure__, new_func.__closure__):
        if not both_instance_of(old_cell.cell_contents, new_cell.cell_contents,
                types.FunctionType):
            continue
        update_function(old_cell.cell_contents, new_cell.cell_contents)

def update_class(old_class, new_class):
    for name, new_attr in new_class.__dict__.items():
        if name not in old_class.__dict():
            setattr(old_class, name, new_attr)
        else:
            old_attr = old_class.__dict__[name]
        if both_instance_of(old_attr, new_attr, types.FunctionType):
            update_function(old_attr, new_attr)
        elif both_instance_of(old_attr, new_attr, staticmethod):
            update_function(old_attr.__func__, new_attr.__func__)
        elif both_instance_of(old_attr, new_attr, classmethod):
            update_function(old_attr.__func__, new_attr.__func__)
        elif both_instance_of(old_attr, new_attr, property):
            update_function(old_attr.fdel, new_attr.fdel)
            update_function(old_attr.fget, new_attr.fget)
            update_function(old_attr.fset, new_attr.fset)
        elif both_instance_of(old_attr, new_attr, (type, types.ClassType)):
            update_class(old_attr, new_attr)

def update_module(old_module, new_module):
    for name, new_val in new_module.__dict__.iteritems():
        if name not in old_module.__dict__:
            setattr(old_module, name, new_val)
        else:
            old_val = old_module.__dict__[name]
            if both_instance_of(old_val, new_val, types.FunctionType):
                update_function(old_val, new_val)
            elif both_instance_of(old_val, new_val, (type, types.ClassType)):
                update_class(old_val, new_val)

def old_foo():
    return "old_foo"

def new_foo():
    return "new_foo"

def decorator(func):
    def _(*args, **kwargs):
        return func(*args, **kwargs)
    return _

@decorator
def old_foo_with_decorator():
    return "old_foo"

@decorator
def new_foo_with_decorator():
    return 'new_foo'


class ReloadTest(unittest.TestCase):
    # def test_update_function(self):
    #     self.assertEqual("old_foo", old_foo())
    #     update_function(old_foo, new_foo)
    #     self.assertEqual("new_foo", old_foo())

    def test_update_function_with_decorator1(self):
        self.assertEqual('old_foo', old_foo_with_decorator())
        update_function(old_foo_with_decorator, new_foo_with_decorator)
        self.assertEqual('new_foo', old_foo_with_decorator())

    def test_update_function_with_decorator2(self):
        self.assertEqual('old_foo', old_foo())
        update_function(old_foo, old_foo_with_decorator)
        self.assertEqual('new_foo', old_foo())

if __name__ == "__main__":
    unittest.main()
