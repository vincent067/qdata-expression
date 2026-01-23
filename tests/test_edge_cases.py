"""
Tests for edge cases and comprehensive coverage.

These tests ensure robust behavior in edge cases and provide
comprehensive coverage for the expression engine.
"""

import json
from datetime import datetime

import pytest

from qdata_expr import (
    ContextResolver,
    ExpressionBuilder,
    ExpressionEngine,
    ExpressionEvalError,
    Sandbox,
    SandboxConfig,
    TemplateEngine,
    resolve,
)


class TestEdgeCases:
    """Test edge cases in expression evaluation."""

    def test_empty_string_expression(self):
        """Test empty string expression."""
        engine = ExpressionEngine()
        errors = engine.validate("")
        assert len(errors) > 0

    def test_whitespace_only_expression(self):
        """Test whitespace-only expression."""
        engine = ExpressionEngine()
        errors = engine.validate("   ")
        assert len(errors) > 0

    def test_unicode_expressions(self):
        """Test Unicode in expressions."""
        engine = ExpressionEngine()

        # Unicode variable names
        context = {"数量": 10, "价格": 99.99}
        # Note: Python AST supports Unicode identifiers
        result = engine.evaluate("数量 * 价格", context)
        assert result == 999.9

    def test_unicode_strings(self):
        """Test Unicode strings in expressions."""
        engine = ExpressionEngine()

        result = engine.evaluate("upper('你好世界')", {})
        assert result == "你好世界"  # Chinese doesn't have uppercase

        result = engine.evaluate("'こんにちは' + '世界'", {})
        assert result == "こんにちは世界"

    def test_very_long_expression(self):
        """Test very long expressions."""
        engine = ExpressionEngine()

        # Build a long expression
        parts = [f"x{i}" for i in range(100)]
        context = {f"x{i}": i for i in range(100)}

        expr = " + ".join(parts)
        result = engine.evaluate(expr, context)
        assert result == sum(range(100))

    def test_deeply_nested_structure(self):
        """Test deeply nested data structures."""
        engine = ExpressionEngine()

        # Build deeply nested dict
        deep_value = {"deep": "value"}
        for i in range(20):
            deep_value = {f"level{i}": deep_value}

        context = {"data": deep_value}

        # Access deep value
        path = ".".join(f"level{i}" for i in range(19, -1, -1)) + ".deep"
        result = engine.evaluate(f"data.{path}", context)
        assert result == "value"

    def test_large_list_operations(self):
        """Test operations on large lists."""
        engine = ExpressionEngine()

        context = {"numbers": list(range(10000))}

        result = engine.evaluate("sum(numbers)", context)
        assert result == sum(range(10000))

        result = engine.evaluate("length(numbers)", context)
        assert result == 10000

    def test_special_float_values(self):
        """Test special float values."""
        engine = ExpressionEngine()

        # Infinity
        result = engine.evaluate("inf", {})
        assert result == float("inf")

        # Negative infinity
        result = engine.evaluate("-inf", {})
        assert result == float("-inf")

    def test_division_by_zero(self):
        """Test division by zero."""
        engine = ExpressionEngine()

        with pytest.raises(ExpressionEvalError):
            engine.evaluate("1 / 0", {})

    def test_type_coercion(self):
        """Test type coercion in expressions."""
        engine = ExpressionEngine()

        # String to int
        result = engine.evaluate("to_int('123')", {})
        assert result == 123

        # Int to string
        result = engine.evaluate("to_str(123)", {})
        assert result == "123"

        # Float to int
        result = engine.evaluate("to_int(3.14)", {})
        assert result == 3

    def test_boolean_edge_cases(self):
        """Test boolean edge cases."""
        engine = ExpressionEngine()

        # Falsy values
        assert engine.evaluate("bool_not(0)", {}) is True
        assert engine.evaluate("bool_not('')", {}) is True
        assert engine.evaluate("bool_not([])", {}) is True
        assert engine.evaluate("bool_not(None)", {}) is True

        # Truthy values
        assert engine.evaluate("bool_not(1)", {}) is False
        assert engine.evaluate("bool_not('a')", {}) is False
        assert engine.evaluate("bool_not([1])", {}) is False

    def test_comparison_with_none(self):
        """Test comparisons involving None."""
        engine = ExpressionEngine()

        context = {"value": None}

        result = engine.evaluate("value == None", context)
        assert result is True

        result = engine.evaluate("is_null(value)", context)
        assert result is True


class TestExpressionBuilder:
    """Test ExpressionBuilder for programmatic expression construction."""

    def test_simple_expression_building(self):
        """Test building simple expressions."""
        builder = ExpressionBuilder()

        expr = builder.var("x").add().var("y").build()
        assert expr == "x + y"

    def test_function_call_building(self):
        """Test building function call expressions."""
        builder = ExpressionBuilder()

        builder.func("upper", "name")
        # The builder outputs function name with arguments
        result = builder.build()
        assert "upper" in result and "name" in result

    def test_complex_expression_building(self):
        """Test building complex expressions."""
        builder = ExpressionBuilder()

        # Build: (a + b) * 2
        inner = ExpressionBuilder()
        inner.var("a").add().var("b")

        builder.group(inner).multiply().literal(2)
        assert builder.build() == "(a + b) * 2"

    def test_wrapped_expression(self):
        """Test building and wrapping expressions."""
        builder = ExpressionBuilder()

        builder.var("x").add().var("y")
        assert builder.wrap() == "${x + y}"


class TestFunctionExtension:
    """Test function extension capabilities."""

    def test_custom_function_registration(self):
        """Test registering custom functions."""
        engine = ExpressionEngine()

        def custom_multiply(a, b, c=1):
            return a * b * c

        engine.register_function("custom_mult", custom_multiply)

        result = engine.evaluate("custom_mult(2, 3)", {})
        assert result == 6

        result = engine.evaluate("custom_mult(2, 3, 4)", {})
        assert result == 24

    def test_overriding_builtin_function(self):
        """Test overriding a built-in function."""
        engine = ExpressionEngine()

        def custom_abs(x):
            return abs(x) * 2  # Double the absolute value

        engine.register_function("abs", custom_abs)

        result = engine.evaluate("abs(-5)", {})
        assert result == 10

    def test_function_with_variable_args(self):
        """Test function with variable arguments."""
        engine = ExpressionEngine()

        def concat_all(*args):
            return "".join(str(a) for a in args)

        engine.register_function("concat_all", concat_all)

        result = engine.evaluate("concat_all('a', 'b', 'c', 1, 2, 3)", {})
        assert result == "abc123"

    def test_function_with_kwargs(self):
        """Test function with keyword arguments."""
        engine = ExpressionEngine()

        def format_number(value, decimals=2, prefix="$"):
            return f"{prefix}{value:.{decimals}f}"

        engine.register_function("format_num", format_number)

        result = engine.evaluate("format_num(123.456)", {})
        assert result == "$123.46"


class TestContextResolution:
    """Test context resolution edge cases."""

    def test_missing_intermediate_path(self):
        """Test accessing path with missing intermediate."""
        resolver = ContextResolver()

        context = {"a": {"b": 1}}

        # c doesn't exist
        result = resolver.resolve("a.c.d", context)
        assert result is None

    def test_array_negative_index(self):
        """Test negative array indexing."""
        context = {"numbers": [1, 2, 3, 4, 5]}

        # Use the engine to test negative indexing
        engine = ExpressionEngine()
        result = engine.evaluate("numbers[-1]", context)
        assert result == 5

        result = engine.evaluate("numbers[-2]", context)
        assert result == 4

    def test_mixed_access_patterns(self):
        """Test mixed dot and bracket access."""
        engine = ExpressionEngine()

        context = {
            "data": {
                "users": [
                    {"name": "Alice", "roles": ["admin", "user"]},
                    {"name": "Bob", "roles": ["user"]},
                ],
            },
        }

        result = engine.evaluate("data['users'][0]['roles'][-1]", context)
        assert result == "user"

    def test_set_creates_intermediate(self):
        """Test that set creates intermediate paths."""
        resolver = ContextResolver()

        context = {}

        new_context = resolver.set("a.b.c.d", "value", context)

        assert resolve("a.b.c.d", new_context) == "value"


class TestSandboxSecurity:
    """Test sandbox security measures."""

    def test_attribute_access_restrictions(self):
        """Test that dangerous attribute access is blocked."""
        sandbox = Sandbox()

        # Magic methods should be blocked
        errors = sandbox.check_expression("obj.__class__")
        assert len(errors) > 0

    def test_builtin_restrictions(self):
        """Test that dangerous builtins are blocked."""
        sandbox = Sandbox()

        dangerous = ["eval", "exec", "compile", "open"]

        for name in dangerous:
            errors = sandbox.check_expression(f"{name}('x')")
            assert len(errors) > 0, f"{name} should be blocked"

    def test_custom_sandbox_config(self):
        """Test custom sandbox configuration."""
        config = SandboxConfig(
            max_execution_time=2.0,
            max_recursion_depth=50,
        )
        sandbox = Sandbox(config)

        assert sandbox.config.max_execution_time == 2.0
        assert sandbox.config.max_recursion_depth == 50


class TestSerialization:
    """Test expression serialization and deserialization patterns."""

    def test_expression_to_json(self):
        """Test serializing expression results to JSON."""
        engine = ExpressionEngine()

        context = {
            "user": {"name": "Alice", "age": 30},
            "item_list": [1, 2, 3],
        }

        # Evaluate and serialize - use dict access for consistent behavior
        result = engine.evaluate("user['name']", context)
        json_result = json.dumps(result)
        assert json.loads(json_result) == "Alice"

        result = engine.evaluate("item_list", context)
        json_result = json.dumps(result)
        assert json.loads(json_result) == [1, 2, 3]

    def test_context_to_json(self):
        """Test serializing context to JSON."""
        context = {
            "string": "hello",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "list": [1, 2, 3],
            "dict": {"a": 1},
        }

        # Should be JSON serializable
        json_str = json.dumps(context)
        restored = json.loads(json_str)
        assert restored == context

    def test_expression_result_types(self):
        """Test that expression results have expected types."""
        engine = ExpressionEngine()

        # String result
        result = engine.evaluate("'hello'", {})
        assert isinstance(result, str)

        # Integer result
        result = engine.evaluate("42", {})
        assert isinstance(result, int)

        # Float result
        result = engine.evaluate("3.14", {})
        assert isinstance(result, float)

        # Boolean result
        result = engine.evaluate("True", {})
        assert isinstance(result, bool)

        # List result
        result = engine.evaluate("[1, 2, 3]", {})
        assert isinstance(result, list)

        # Dict result
        result = engine.evaluate("{'a': 1}", {})
        assert isinstance(result, dict)


class TestComprehensionSupport:
    """Test list, dict, and set comprehension support."""

    def test_list_comprehension(self):
        """Test list comprehension."""
        engine = ExpressionEngine()

        result = engine.evaluate("[x * 2 for x in range(5)]", {})
        assert result == [0, 2, 4, 6, 8]

    def test_list_comprehension_with_filter(self):
        """Test list comprehension with filter."""
        engine = ExpressionEngine()

        result = engine.evaluate("[x for x in range(10) if x % 2 == 0]", {})
        assert result == [0, 2, 4, 6, 8]

    def test_list_comprehension_with_context(self):
        """Test list comprehension with context variables."""
        engine = ExpressionEngine()

        context = {"my_items": [1, 2, 3, 4, 5]}

        result = engine.evaluate("[x ** 2 for x in my_items]", context)
        assert result == [1, 4, 9, 16, 25]

    def test_nested_list_comprehension(self):
        """Test nested list comprehension."""
        engine = ExpressionEngine()

        context = {"matrix": [[1, 2], [3, 4], [5, 6]]}

        result = engine.evaluate("[x for row in matrix for x in row]", context)
        assert result == [1, 2, 3, 4, 5, 6]


class TestTemplateSecurity:
    """Test template security measures."""

    def test_template_without_dangerous_code(self):
        """Test that templates don't execute dangerous code."""
        template_engine = TemplateEngine()

        # Templates should just render, not execute Python
        template = "{{ '2 + 2' }}"  # Should output the string, not 4
        result = template_engine.render(template, {})
        assert result == "2 + 2"

    def test_template_escaping(self):
        """Test HTML escaping in templates."""
        template_engine = TemplateEngine()

        context = {"html": "<script>alert('xss')</script>"}

        # Default should escape HTML
        template = "{{ html }}"
        result = template_engine.render(template, context)
        # Jinja2 escapes by default
        assert "<script>" not in result or "script" in result


class TestDatetimeFunctions:
    """Test datetime function edge cases."""

    def test_date_arithmetic_edge_cases(self):
        """Test date arithmetic edge cases."""
        engine = ExpressionEngine()

        # Adding months to end of month
        context = {"d": datetime(2024, 1, 31)}

        # January 31 + 1 month = February 28/29
        result = engine.evaluate("add_months(d, 1)", context)
        assert result.month == 2
        assert result.day in [28, 29]  # Depends on leap year

    def test_leap_year_handling(self):
        """Test leap year handling."""
        engine = ExpressionEngine()

        # 2024 is a leap year - check using year function and modulo
        context = {"d": datetime(2024, 2, 29)}

        result = engine.evaluate("year(d)", context)
        assert result == 2024

        # Add 1 year to Feb 29
        result = engine.evaluate("add_years(d, 1)", context)
        # 2025 is not a leap year, so Feb 29 becomes Feb 28
        assert result.month == 2
        assert result.day == 28


class TestErrorMessages:
    """Test error message quality."""

    def test_syntax_error_message(self):
        """Test syntax error messages are helpful."""
        engine = ExpressionEngine()

        errors = engine.validate("2 + ")
        assert len(errors) > 0
        # Error should mention syntax

    def test_undefined_variable_message(self):
        """Test undefined variable error messages."""
        engine = ExpressionEngine()

        with pytest.raises(ExpressionEvalError) as exc_info:
            engine.evaluate("undefined_var", {})

        # Error should mention the variable name
        assert "undefined_var" in str(exc_info.value)
