# -*- coding: utf-8 -*-

# import sys
# sys.path.insert(0, "..")
# print(sys.path)

import unittest

from cobra.base import compile
from .utils import norm


def test_basic_op_add():
    assert compile("2 + 2") == "2 + 2;"


def test_basic_op_mul():
    assert compile("2 * 2") == "2 * 2;"


def test_basic_op_sub():
    assert compile("2 - 2") == "2 - 2;"


def test_basic_op_div():
    assert compile("2 / 2") == "2 / 2;"


def test_basic_op_mod():
    assert compile("2 % 2") == "2 % 2;"


def test_simple_assignation():
    input = "x = 2"
    expected = """
    var x;
    x = 2;
    """
    assert compile(input) == norm(expected)


def test_nested_operations():
    input = "x = 2 * ((33 + 2.2) / 2)"
    expected = """
    var x;
    x = 2 * ((33 + 2.2) / 2);
    """
    assert compile(input) == norm(expected)


def test_none_assignation():
    input = "x = None"
    expected = """
    var x;
    x = null;
    """
    assert compile(input) == norm(expected)


def test_simple_multiple_assignation():
    input = "x = y = 2"
    expected = """
    var x, y;
    x = y = 2;
    """
    assert compile(input) == norm(expected)


def test_simple_function_declaration():
    input = """
    def foo():
        return 2
    """

    expected = """
    var foo;
    foo = function() {
        return 2;
    };
    """

    assert compile(input) == norm(expected)


def test_simple_function_declaration_with_args():
    input = """
    def foo(a, b):
        return a + b
    """

    expected = """
    var foo;
    foo = function(a, b) {
        return a + b;
    };
    """

    assert compile(input) == norm(expected)


def test_nested_function():
    input = """
    def foo(a, b):
        def bar():
            return 2
        return bar
    """

    expected = """
    var foo;
    foo = function(a, b) {
        var bar;
        bar = function() {
            return 2;
        };
        return bar;
    };
    """

    assert compile(input) == norm(expected)


def test_simple_function_call():
    input = """
    x = foo("Hello World")
    """

    expected = """
    var x;
    x = foo("Hello World");
    """

    assert compile(input) == norm(expected)


def test_simple_function_call_with_multiple_args():
    input = """
    x = foo("Hello World", 2, 2.3)
    """

    expected = """
    var x;
    x = foo("Hello World", 2, 2.3);
    """

    assert compile(input) == norm(expected)


def test_function_call_with_lambda_as_parameter():
    input = """
    x = jQuery(".span")
    x.on("click", lambda e: e.preventDefault())
    """

    expected = """
    var x;
    x = jQuery(".span");
    x.on("click", function(e) {
        e.preventDefault();
    });
    """

    assert compile(input) == norm(expected)


def test_assign_dict():
    input = """
    x = {"foo": 2, "bar": {"kk": 3}}
    """

    expected = """
    var x;
    x = {
        "foo": 2,
        "bar": {
            "kk": 3
        }
    };
    """

    assert compile(input) == norm(expected)


def test_assign_dict_with_lists():
    input = """
    x = {"foo": 2, "bar": {"kk": [1, 2, 3]}}
    """

    expected = """
    var x;
    x = {
        "foo": 2,
        "bar": {
            "kk": [1,2,3]
        }
    };
    """

    assert compile(input) == norm(expected)

def test_simple_if_statement():
    input = """
    def foo(a):
        if a is None:
            return None

        return a + 2
    """

    expected = """
    var foo;
    foo = function(a) {
        if (a === null) {
            return null;
        }
        return a + 2;
    };
    """

    assert compile(input) == norm(expected)

def test_simple_if_statement_with_else():
    input = """
    def foo(a):
        if a is None:
            return None
        else:
            return a + 2
    """

    expected = """
    var foo;
    foo = function(a) {
        if (a === null) {
            return null;
        } else {
            return a + 2;
        }
    };
    """

    assert compile(input) == norm(expected)


def test_simple_if_statement_with_elif():
    input = """
    def foo(a):
        if a is None:
            return None
        elif a == 0:
            return a + 2
    """

    expected = """
    var foo;
    foo = function(a) {
        if (a === null) {
            return null;
        } else if (a === 0) {
            return a + 2;
        }
    };
    """

    assert compile(input) == norm(expected)


# def test_basic_class():
#     input = """
#     class MyClass:
#         def foo(self):
#             return 2
#     """
#
#     expected = ""
#
#     assert compile(input) == norm(expected)
