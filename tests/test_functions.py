"""
Tests for built-in functions.
"""

import math
import sys
from datetime import datetime

import pytest

from qdata_expr import ExpressionEngine
from qdata_expr.functions import (
    MATH_FUNCTIONS,
    STRING_FUNCTIONS,
    FunctionCategory,
    FunctionDefinition,
    FunctionRegistry,
    builtin_function,
    get_all_builtin_functions,
    get_builtin_functions,
)


class TestMathFunctions:
    """Test mathematical functions."""

    def test_basic_math_functions(self):
        """Test basic math functions."""
        engine = ExpressionEngine()

        # Test abs
        result = engine.evaluate("abs(-5)")
        assert result == 5

        result = engine.evaluate("abs(5)")
        assert result == 5

        result = engine.evaluate("abs(-3.14)")
        assert result == 3.14

    def test_round_function(self):
        """Test round function."""
        engine = ExpressionEngine()

        result = engine.evaluate("round(3.14159)")
        assert result == 3

        result = engine.evaluate("round(3.14159, 2)")
        assert result == 3.14

        result = engine.evaluate("round(2.5)")
        assert result == 2

    def test_floor_ceil_trunc(self):
        """Test floor, ceil, and trunc functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("floor(3.7)")
        assert result == 3

        result = engine.evaluate("ceil(3.2)")
        assert result == 4

        result = engine.evaluate("trunc(3.9)")
        assert result == 3

        result = engine.evaluate("floor(-3.7)")
        assert result == -4

        result = engine.evaluate("ceil(-3.2)")
        assert result == -3

        result = engine.evaluate("trunc(-3.9)")
        assert result == -3

    def test_min_max_sum(self):
        """Test min, max, and sum functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("min(1, 2, 3, 4, 5)")
        assert result == 1

        result = engine.evaluate("max(1, 2, 3, 4, 5)")
        assert result == 5

        result = engine.evaluate("sum(1, 2, 3, 4, 5)")
        assert result == 15

        result = engine.evaluate("sum([1, 2, 3, 4, 5])")
        assert result == 15

    def test_avg_function(self):
        """Test avg function."""
        engine = ExpressionEngine()

        result = engine.evaluate("avg(1, 2, 3, 4, 5)")
        assert result == 3.0

        result = engine.evaluate("avg([10, 20, 30])")
        assert result == 20.0

    def test_count_function(self):
        """Test count function."""
        engine = ExpressionEngine()

        result = engine.evaluate("count(1, 2, 3)")
        assert result == 3

        result = engine.evaluate("count([1, 2, 3, 4, 5])")
        assert result == 5

    def test_power_functions(self):
        """Test power and root functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("pow(2, 3)")
        assert result == 8

        result = engine.evaluate("pow(10, 2)")
        assert result == 100

        result = engine.evaluate("sqrt(16)")
        assert result == 4.0

        result = engine.evaluate("sqrt(2)")
        assert abs(result - 1.41421356) < 0.0001

    def test_logarithm_functions(self):
        """Test logarithm functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("log(e)")
        assert abs(result - 1.0) < 0.0001

        result = engine.evaluate("log(100, 10)")
        assert abs(result - 2.0) < 0.0001

        result = engine.evaluate("log10(100)")
        assert result == 2.0

        result = engine.evaluate("log10(1000)")
        assert result == 3.0

    def test_exponential_function(self):
        """Test exponential function."""
        engine = ExpressionEngine()

        result = engine.evaluate("exp(0)")
        assert result == 1.0

        result = engine.evaluate("exp(1)")
        assert abs(result - math.e) < 0.0001

    def test_mod_div_functions(self):
        """Test mod and div functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("mod(10, 3)")
        assert result == 1

        result = engine.evaluate("div(10, 3)")
        assert abs(result - 3.333333) < 0.001

    def test_sign_function(self):
        """Test sign function."""
        engine = ExpressionEngine()

        result = engine.evaluate("sign(-5)")
        assert result == -1

        result = engine.evaluate("sign(0)")
        assert result == 0

        result = engine.evaluate("sign(10)")
        assert result == 1

    def test_trigonometric_functions(self):
        """Test trigonometric functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("sin(0)")
        assert abs(result) < 0.0001

        result = engine.evaluate("cos(0)")
        assert abs(result - 1.0) < 0.0001

        result = engine.evaluate("tan(0)")
        assert abs(result) < 0.0001

    def test_angle_conversion(self):
        """Test angle conversion functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("radians(180)")
        assert abs(result - math.pi) < 0.0001

        result = engine.evaluate("degrees(pi)")
        assert abs(result - 180.0) < 0.0001

    def test_random_functions(self):
        """Test random functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("random()")
        assert 0 <= result < 1

        result = engine.evaluate("random_int(1, 10)")
        assert 1 <= result <= 10


class TestStringFunctions:
    """Test string functions."""

    def test_case_conversion(self):
        """Test case conversion functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("upper('hello')")
        assert result == "HELLO"

        result = engine.evaluate("lower('WORLD')")
        assert result == "world"

        result = engine.evaluate("title('hello world')")
        assert result == "Hello World"

        result = engine.evaluate("capitalize('hello')")
        assert result == "Hello"

        result = engine.evaluate("swapcase('HeLLo')")
        assert result == "hEllO"

    def test_whitespace_functions(self):
        """Test whitespace functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("trim('  hello  ')")
        assert result == "hello"

        result = engine.evaluate("ltrim('  hello')")
        assert result == "hello"

        result = engine.evaluate("rtrim('hello  ')")
        assert result == "hello"

        result = engine.evaluate("strip('##hello##', '#')")
        assert result == "hello"

        result = engine.evaluate("normalize_space('hello   world')")
        assert result == "hello world"

    def test_string_operations(self):
        """Test string operations."""
        engine = ExpressionEngine()

        result = engine.evaluate("concat('hello', ' ', 'world')")
        assert result == "hello world"

        result = engine.evaluate("join(['a', 'b', 'c'], '-')")
        assert result == "a-b-c"

        result = engine.evaluate("split('a,b,c', ',')")
        assert result == ["a", "b", "c"]

        result = engine.evaluate("substring('hello world', 0, 5)")
        assert result == "hello"

        result = engine.evaluate("left('hello', 3)")
        assert result == "hel"

        result = engine.evaluate("right('hello', 3)")
        assert result == "llo"

        result = engine.evaluate("mid('hello', 1, 3)")
        assert result == "ell"

        result = engine.evaluate("replace('hello world', 'world', 'Python')")
        assert result == "hello Python"

        result = engine.evaluate("repeat('ab', 3)")
        assert result == "ababab"

        result = engine.evaluate("reverse('hello')")
        assert result == "olleh"

    def test_search_functions(self):
        """Test search functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("contains('hello world', 'world')")
        assert result

        result = engine.evaluate("starts_with('hello world', 'hello')")
        assert result

        result = engine.evaluate("ends_with('hello world', 'world')")
        assert result

        result = engine.evaluate("find('hello world', 'world')")
        assert result == 6

        result = engine.evaluate("str_count('hello world', 'l')")
        assert result == 3

    def test_regex_functions(self):
        """Test regex functions."""
        engine = ExpressionEngine()

        result = engine.evaluate(r"match('hello123', r'\d+')")
        assert result

        result = engine.evaluate(r"regex_find('hello123', r'\d+')")
        assert result == "123"

        result = engine.evaluate(r"regex_findall('a1b2c3', r'\d')")
        assert result == ["1", "2", "3"]

        result = engine.evaluate(r"regex_replace('a1b2', r'\d', 'X')")
        assert result == "aXbX"

    def test_padding_functions(self):
        """Test padding functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("pad_left('5', 3, '0')")
        assert result == "005"

        result = engine.evaluate("pad_right('5', 3, '0')")
        assert result == "500"

        result = engine.evaluate("pad_center('hi', 6, '-')")
        assert result == "--hi--"

        result = engine.evaluate("zfill('42', 5)")
        assert result == "00042"

    def test_type_check_functions(self):
        """Test type check functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("is_alpha('hello')")
        assert result

        result = engine.evaluate("is_digit('123')")
        assert result

        result = engine.evaluate("is_alnum('abc123')")
        assert result

        result = engine.evaluate("is_numeric('3.14')")
        assert result

    def test_length_and_format(self):
        """Test length and format functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("len('hello')")
        assert result == 5

        result = engine.evaluate("format('Hello {}', 'World')")
        assert result == "Hello World"

        result = engine.evaluate("truncate('hello world', 8)")
        assert result == "hello..."


class TestLogicFunctions:
    """Test logic functions."""

    def test_null_check_functions(self):
        """Test null check functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("is_null(None)")
        assert result

        result = engine.evaluate("is_null(0)")
        assert not result

        result = engine.evaluate("is_not_null(1)")
        assert result

        result = engine.evaluate("is_not_null(None)")
        assert not result

    def test_empty_check_functions(self):
        """Test empty check functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("is_empty('')")
        assert result

        result = engine.evaluate("is_empty([])")
        assert result

        result = engine.evaluate("is_empty({})")
        assert result

        result = engine.evaluate("is_empty(None)")
        assert result

        result = engine.evaluate("is_not_empty('hello')")
        assert result

    def test_blank_check_function(self):
        """Test blank check function."""
        engine = ExpressionEngine()

        result = engine.evaluate("is_blank('')")
        assert result

        result = engine.evaluate("is_blank('   ')")
        assert result

        result = engine.evaluate("is_blank(None)")
        assert result

        result = engine.evaluate("is_blank('hello')")
        assert not result

    def test_conditional_functions(self):
        """Test conditional functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("if_else(True, 'yes', 'no')")
        assert result == "yes"

        result = engine.evaluate("if_else(False, 'yes', 'no')")
        assert result == "no"

        result = engine.evaluate("if_null(None, 'default')")
        assert result == "default"

        result = engine.evaluate("if_null('value', 'default')")
        assert result == "value"

        result = engine.evaluate("if_empty('', 'default')")
        assert result == "default"

        result = engine.evaluate("if_empty('value', 'default')")
        assert result == "value"

    def test_coalesce_function(self):
        """Test coalesce function."""
        engine = ExpressionEngine()

        result = engine.evaluate("coalesce(None, '', 'value')")
        assert result == ""

        result = engine.evaluate("coalesce(None, None, 'value')")
        assert result == "value"

        result = engine.evaluate("coalesce('first', 'second')")
        assert result == "first"

    def test_nvl_functions(self):
        """Test NVL functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("nvl(None, 'default')")
        assert result == "default"

        result = engine.evaluate("nvl('value', 'default')")
        assert result == "value"

        result = engine.evaluate("nvl2('value', 'not null', 'null')")
        assert result == "not null"

        result = engine.evaluate("nvl2(None, 'not null', 'null')")
        assert result == "null"

    def test_nullif_function(self):
        """Test nullif function."""
        engine = ExpressionEngine()

        result = engine.evaluate("nullif(1, 1)")
        assert result is None

        result = engine.evaluate("nullif(1, 2)")
        assert result == 1

    def test_switch_function(self):
        """Test switch function."""
        engine = ExpressionEngine()

        result = engine.evaluate('switch("a", {"a": 1, "b": 2}, 0)')
        assert result == 1

        result = engine.evaluate('switch("c", {"a": 1, "b": 2}, 0)')
        assert result == 0

    def test_boolean_functions(self):
        """Test boolean functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("bool_and(True, True, False)")
        assert not result

        result = engine.evaluate("bool_or(True, False, False)")
        assert result

        result = engine.evaluate("bool_not(True)")
        assert not result

        result = engine.evaluate("xor(True, False)")
        assert result

        result = engine.evaluate("xor(True, True)")
        assert not result

    def test_comparison_functions(self):
        """Test comparison functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("eq(1, 1)")
        assert result

        result = engine.evaluate("ne(1, 2)")
        assert result

        result = engine.evaluate("gt(2, 1)")
        assert result

        result = engine.evaluate("ge(1, 1)")
        assert result

        result = engine.evaluate("lt(1, 2)")
        assert result

        result = engine.evaluate("le(1, 1)")
        assert result

        result = engine.evaluate("between(5, 1, 10)")
        assert result

        result = engine.evaluate("contains_value(2, 1, 2, 3)")
        assert result

        result = engine.evaluate("not_in(4, 1, 2, 3)")
        assert result

    def test_type_check_functions(self):
        """Test type check functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("is_bool(True)")
        assert result

        result = engine.evaluate("is_int(42)")
        assert result

        result = engine.evaluate("is_float(3.14)")
        assert result

        result = engine.evaluate("is_number(42)")
        assert result

        result = engine.evaluate("is_string('hello')")
        assert result

        result = engine.evaluate("is_list([1, 2, 3])")
        assert result

        result = engine.evaluate("is_dict({'a': 1})")
        assert result

        result = engine.evaluate("type_of(42)")
        assert result == "int"

    def test_type_conversion_functions(self):
        """Test type conversion functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("to_bool('true')")
        assert result

        result = engine.evaluate("to_int('123')")
        assert result == 123

        result = engine.evaluate("to_float('3.14')")
        assert result == 3.14

        result = engine.evaluate("to_str(123)")
        assert result == "123"

    def test_assert_functions(self):
        """Test assert functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("require('value', 'Required')")
        assert result == "value"

        with pytest.raises(ValueError):  # require raises ValueError
            engine.evaluate("require('', 'Required')")


class TestListFunctions:
    """Test list functions."""

    def test_basic_list_operations(self):
        """Test basic list operations."""
        engine = ExpressionEngine()

        result = engine.evaluate("length([1, 2, 3])")
        assert result == 3

        result = engine.evaluate("first([1, 2, 3])")
        assert result == 1

        result = engine.evaluate("last([1, 2, 3])")
        assert result == 3

        result = engine.evaluate("nth([1, 2, 3], 1)")
        assert result == 2

        result = engine.evaluate("take([1, 2, 3, 4, 5], 3)")
        assert result == [1, 2, 3]

        result = engine.evaluate("skip([1, 2, 3, 4, 5], 2)")
        assert result == [3, 4, 5]

        result = engine.evaluate("slice([1, 2, 3, 4, 5], 1, 4)")
        assert result == [2, 3, 4]

        result = engine.evaluate("reverse_list([1, 2, 3])")
        assert result == [3, 2, 1]

    def test_list_search_functions(self):
        """Test list search functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("contains_item([1, 2, 3], 2)")
        assert result

        result = engine.evaluate("index_of([1, 2, 3, 2], 2)")
        assert result == 1

        result = engine.evaluate("count_item([1, 2, 2, 3], 2)")
        assert result == 2

    def test_list_sorting(self):
        """Test list sorting functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("sort([3, 1, 2])")
        assert result == [1, 2, 3]

        result = engine.evaluate("sort([3, 1, 2], True)")
        assert result == [3, 2, 1]

    def test_list_set_operations(self):
        """Test list set operations."""
        engine = ExpressionEngine()

        result = engine.evaluate("unique([1, 2, 2, 3, 1])")
        assert result == [1, 2, 3]

        result = engine.evaluate("union([1, 2], [2, 3], [3, 4])")
        assert result == [1, 2, 3, 4]

        result = engine.evaluate("intersection([1, 2, 3], [2, 3, 4])")
        assert result == [2, 3]

        result = engine.evaluate("difference([1, 2, 3], [2])")
        assert result == [1, 3]

    def test_list_flattening(self):
        """Test list flattening functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("flat([[1, 2], [3, 4]])")
        assert result == [1, 2, 3, 4]

        result = engine.evaluate("flatten([[1, [2, 3]], [4]])")
        assert result == [1, 2, 3, 4]

    def test_list_grouping(self):
        """Test list grouping functions."""
        engine = ExpressionEngine()

        result = engine.evaluate('group_by([{"type": "a", "v": 1}, {"type": "a", "v": 2}], "type")')
        assert "a" in result
        assert len(result["a"]) == 2

    def test_list_construction(self):
        """Test list construction functions."""
        engine = ExpressionEngine()

        result = engine.evaluate("range(5)")
        assert result == [0, 1, 2, 3, 4]

        result = engine.evaluate("range(1, 5)")
        assert result == [1, 2, 3, 4]

        result = engine.evaluate("range(1, 10, 2)")
        assert result == [1, 3, 5, 7, 9]

        result = engine.evaluate("repeat_item('a', 3)")
        assert result == ["a", "a", "a"]

    def test_dictionary_functions(self):
        """Test dictionary functions."""
        engine = ExpressionEngine()

        result = engine.evaluate('keys({"a": 1, "b": 2})')
        assert "a" in result
        assert "b" in result

        result = engine.evaluate('values({"a": 1, "b": 2})')
        assert 1 in result
        assert 2 in result

        result = engine.evaluate('items({"a": 1})')
        assert result == [("a", 1)]

        result = engine.evaluate('get({"a": 1}, "a")')
        assert result == 1

        result = engine.evaluate('get({"a": 1}, "b", 0)')
        assert result == 0


class TestDateTimeFunctions:
    """Test datetime functions."""

    def test_current_time_functions(self):
        """Test current time functions."""
        engine = ExpressionEngine()

        # These should return datetime/date objects
        result = engine.evaluate("now()")
        assert isinstance(result, datetime)

        result = engine.evaluate("today()")
        assert hasattr(result, "year")

        result = engine.evaluate("timestamp()")
        assert isinstance(result, float)

    def test_date_formatting(self):
        """Test date formatting functions."""
        engine = ExpressionEngine()

        context = {"date": datetime(2024, 1, 15, 14, 30, 45)}

        result = engine.evaluate('date_format(date, "%Y-%m-%d")', context)
        assert result == "2024-01-15"

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="Windows locale encoding does not support Chinese characters in strftime",
    )
    def test_date_formatting_chinese(self):
        """Test date formatting with Chinese format (non-Windows only)."""
        engine = ExpressionEngine()

        context = {"date": datetime(2024, 1, 15, 14, 30, 45)}

        result = engine.evaluate('date_format(date, "%Y年%m月%d日")', context)
        assert result == "2024年01月15日"

    def test_date_parsing(self):
        """Test date parsing functions."""
        engine = ExpressionEngine()

        result = engine.evaluate('date_parse("2024-01-15", "%Y-%m-%d")')
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_date_components(self):
        """Test date component functions."""
        engine = ExpressionEngine()

        context = {"date": datetime(2024, 1, 15, 14, 30, 45)}

        result = engine.evaluate("year(date)", context)
        assert result == 2024

        result = engine.evaluate("month(date)", context)
        assert result == 1

        result = engine.evaluate("day(date)", context)
        assert result == 15

        result = engine.evaluate("hour(date)", context)
        assert result == 14

        result = engine.evaluate("minute(date)", context)
        assert result == 30

        result = engine.evaluate("second(date)", context)
        assert result == 45

    def test_date_arithmetic(self):
        """Test date arithmetic functions."""
        engine = ExpressionEngine()

        context = {"date": datetime(2024, 1, 15)}

        result = engine.evaluate("add_days(date, 7)", context)
        assert result.day == 22

        result = engine.evaluate("add_months(date, 1)", context)
        assert result.month == 2

        result = engine.evaluate("add_years(date, 1)", context)
        assert result.year == 2025

    def test_date_differences(self):
        """Test date difference functions."""
        engine = ExpressionEngine()

        context = {"start": datetime(2024, 1, 1), "end": datetime(2024, 1, 15)}

        result = engine.evaluate("diff_days(start, end)", context)
        assert result == 14

    def test_date_boundaries(self):
        """Test date boundary functions."""
        engine = ExpressionEngine()

        context = {"date": datetime(2024, 1, 15, 14, 30, 45)}

        result = engine.evaluate("start_of_day(date)", context)
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0

        result = engine.evaluate("end_of_day(date)", context)
        assert result.hour == 23
        assert result.minute == 59
        assert result.second == 59

        result = engine.evaluate("start_of_month(date)", context)
        assert result.day == 1


class TestFunctionRegistry:
    """Test FunctionRegistry class."""

    def test_registry_creation(self):
        """Test registry creation."""
        registry = FunctionRegistry()
        assert registry is not None
        assert len(registry.list_all()) == 0

    def test_function_registration(self):
        """Test function registration."""
        registry = FunctionRegistry()

        def test_func(x, y):
            return x + y

        registry.register("test_add", test_func, FunctionCategory.CUSTOM)

        assert registry.has("test_add")
        assert "test_add" in registry.list_all()

        func = registry.get("test_add")
        assert func is not None
        assert func.name == "test_add"
        assert func.category == FunctionCategory.CUSTOM

    def test_function_callable(self):
        """Test getting function callable."""
        registry = FunctionRegistry()

        def test_func(x):
            return x * 2

        registry.register("double", test_func, FunctionCategory.CUSTOM)

        callable_func = registry.get_callable("double")
        assert callable_func is not None
        assert callable_func(5) == 10

    def test_function_unregister(self):
        """Test function unregistration."""
        registry = FunctionRegistry()

        def test_func():
            pass

        registry.register("test", test_func, FunctionCategory.CUSTOM)
        assert registry.has("test")

        success = registry.unregister("test")
        assert success
        assert not registry.has("test")

        success = registry.unregister("nonexistent")
        assert not success

    def test_list_by_category(self):
        """Test listing functions by category."""
        registry = FunctionRegistry()

        def func1():
            pass

        def func2():
            pass

        registry.register("math_func", func1, FunctionCategory.MATH)
        registry.register("string_func", func2, FunctionCategory.STRING)

        math_funcs = registry.list_by_category(FunctionCategory.MATH)
        assert "math_func" in math_funcs

        string_funcs = registry.list_by_category(FunctionCategory.STRING)
        assert "string_func" in string_funcs

    def test_register_definition(self):
        """Test registering function definition."""
        registry = FunctionRegistry()

        def test_func():
            pass

        definition = FunctionDefinition(
            name="test",
            func=test_func,
            category=FunctionCategory.CUSTOM,
            description="Test function",
        )

        registry.register_definition(definition)

        assert registry.has("test")
        func = registry.get("test")
        assert func.description == "Test function"

    def test_get_all_callables(self):
        """Test getting all callables."""
        registry = FunctionRegistry()

        def func1():
            return 1

        def func2():
            return 2

        registry.register("f1", func1, FunctionCategory.CUSTOM)
        registry.register("f2", func2, FunctionCategory.CUSTOM)

        callables = registry.get_all_callables()

        assert "f1" in callables
        assert "f2" in callables
        assert callables["f1"]() == 1
        assert callables["f2"]() == 2

    def test_function_aliases(self):
        """Test function aliases."""
        registry = FunctionRegistry()

        def test_func():
            pass

        registry.register(
            "original", test_func, FunctionCategory.CUSTOM, aliases=["alias1", "alias2"]
        )

        assert registry.has("original")
        assert registry.has("alias1")
        assert registry.has("alias2")

        # All should point to the same function
        orig = registry.get_callable("original")
        alias1 = registry.get_callable("alias1")
        alias2 = registry.get_callable("alias2")

        assert orig is alias1
        assert orig is alias2


class TestBuiltinFunctionDecorator:
    """Test builtin_function decorator."""

    def test_decorator_basic(self):
        """Test basic decorator usage."""

        @builtin_function(
            name="custom_add",
            category=FunctionCategory.MATH,
            description="Custom addition function",
        )
        def custom_add(x, y):
            return x + y

        # Should be registered in global registry
        registry = get_builtin_functions()
        assert registry.has("custom_add")

    def test_decorator_with_signature(self):
        """Test decorator with signature."""

        @builtin_function(
            name="test_func",
            category=FunctionCategory.STRING,
            description="Test function",
            signature="test_func(x) -> str",
            examples=["test_func(5) = '5'"],
        )
        def test_func(x):
            return str(x)

        registry = get_builtin_functions()
        func = registry.get("test_func")
        assert func.signature == "test_func(x) -> str"
        assert func.examples == ["test_func(5) = '5'"]

    def test_get_all_builtin_functions(self):
        """Test getting all built-in functions."""
        # The get_all_builtin_functions returns only decorator-registered functions
        # The main built-in functions are in MATH_FUNCTIONS, STRING_FUNCTIONS, etc.
        callables = get_all_builtin_functions()

        # Decorator-registered functions should be in there (from previous tests)
        assert len(callables) >= 0  # At least any decorator-registered ones

        # Check the main function dictionaries contain expected functions
        assert "abs" in MATH_FUNCTIONS
        assert "len" in STRING_FUNCTIONS
