"""
Tests for expression evaluator.
"""

import time

import pytest

from qdata_expr import (
    CompiledExpression,
    ExpressionEngine,
    ExpressionEvalError,
    ExpressionParseError,
    SafeEvaluator,
    UndefinedFunctionError,
    UndefinedVariableError,
    evaluate,
    get_default_engine,
    register_function,
    validate,
)


class TestExpressionEngine:
    """Test ExpressionEngine class."""

    def test_engine_creation(self):
        """Test engine creation with default settings."""
        engine = ExpressionEngine()
        assert engine is not None
        assert engine.cache_stats is not None

    def test_engine_creation_no_cache(self):
        """Test engine creation without cache."""
        engine = ExpressionEngine(enable_cache=False)
        assert engine.cache_stats is None

    def test_engine_creation_no_sandbox(self):
        """Test engine creation without sandbox."""
        engine = ExpressionEngine(enable_sandbox=False)
        assert engine is not None

    def test_basic_arithmetic(self, expression_engine: ExpressionEngine):
        """Test basic arithmetic operations."""
        test_cases = [
            ("2 + 3", 5),
            ("10 - 4", 6),
            ("3 * 4", 12),
            ("10 / 2", 5.0),
            ("10 // 3", 3),
            ("10 % 3", 1),
            ("2 ** 3", 8),
            ("-5", -5),
            ("+10", 10),
        ]

        for expr, expected in test_cases:
            result = expression_engine.evaluate(expr)
            assert result == expected, f"Failed for {expr}: expected {expected}, got {result}"

    def test_operator_precedence(self, expression_engine: ExpressionEngine):
        """Test operator precedence."""
        result = expression_engine.evaluate("2 + 3 * 4")
        assert result == 14  # 2 + (3 * 4)

        result = expression_engine.evaluate("(2 + 3) * 4")
        assert result == 20  # (2 + 3) * 4

        result = expression_engine.evaluate("2 ** 3 * 2")
        assert result == 16  # (2 ** 3) * 2

    def test_comparison_operations(self, expression_engine: ExpressionEngine):
        """Test comparison operations."""
        test_cases = [
            ("5 == 5", True),
            ("5 != 3", True),
            ("5 > 3", True),
            ("3 < 5", True),
            ("5 >= 5", True),
            ("3 <= 5", True),
            ("'a' == 'a'", True),
            ("'a' != 'b'", True),
            ("'apple' < 'banana'", True),
        ]

        for expr, expected in test_cases:
            result = expression_engine.evaluate(expr)
            assert result == expected, f"Failed for {expr}"

    def test_logical_operations(self, expression_engine: ExpressionEngine):
        """Test logical operations."""
        test_cases = [
            ("True and True", True),
            ("True and False", False),
            ("True or False", True),
            ("False or False", False),
            ("not True", False),
            ("not False", True),
            ("5 > 3 and 2 < 4", True),
            ("5 > 3 and 2 > 4", False),
            ("5 > 3 or 2 > 4", True),
            ("not (5 > 3)", False),
        ]

        for expr, expected in test_cases:
            result = expression_engine.evaluate(expr)
            assert result == expected, f"Failed for {expr}"

    def test_variables(self, expression_engine: ExpressionEngine, sample_context: dict):
        """Test variable evaluation."""
        result = expression_engine.evaluate("user.name", sample_context)
        assert result == "Alice"

        result = expression_engine.evaluate("order.total", sample_context)
        assert result == 1059.97

        result = expression_engine.evaluate("config.tax_rate", sample_context)
        assert result == 0.1

    def test_undefined_variable(self, expression_engine: ExpressionEngine):
        """Test undefined variable error."""
        # The engine wraps UndefinedVariableError in ExpressionEvalError
        with pytest.raises((UndefinedVariableError, ExpressionEvalError)):
            expression_engine.evaluate("undefined_var")

    def test_builtin_functions(self, expression_engine: ExpressionEngine):
        """Test built-in functions."""
        test_cases = [
            ("abs(-5)", 5),
            ("abs(5)", 5),
            ("round(3.14159, 2)", 3.14),
            ("round(2.5)", 2),
            ("min(1, 2, 3)", 1),
            ("max(1, 2, 3)", 3),
            ("sum([1, 2, 3, 4])", 10),
            ("len([1, 2, 3])", 3),
            ("len('hello')", 5),
            ("upper('hello')", "HELLO"),
            ("lower('WORLD')", "world"),
            ("trim('  hello  ')", "hello"),
        ]

        for expr, expected in test_cases:
            result = expression_engine.evaluate(expr)
            assert result == expected, f"Failed for {expr}"

    def test_math_functions(self, expression_engine: ExpressionEngine):
        """Test math functions."""
        result = expression_engine.evaluate("pow(2, 3)")
        assert result == 8

        result = expression_engine.evaluate("sqrt(16)")
        assert result == 4.0

        result = expression_engine.evaluate("floor(3.7)")
        assert result == 3

        result = expression_engine.evaluate("ceil(3.2)")
        assert result == 4

    def test_string_functions(self, expression_engine: ExpressionEngine):
        """Test string functions."""
        result = expression_engine.evaluate("concat('hello', ' ', 'world')")
        assert result == "hello world"

        result = expression_engine.evaluate("substring('hello world', 0, 5)")
        assert result == "hello"

        result = expression_engine.evaluate("replace('hello world', 'world', 'Python')")
        assert result == "hello Python"

    def test_conditional_expression(self, expression_engine: ExpressionEngine):
        """Test conditional expressions."""
        context = {"age": 25}
        result = expression_engine.evaluate("'adult' if age >= 18 else 'minor'", context)
        assert result == "adult"

        context = {"age": 15}
        result = expression_engine.evaluate("'adult' if age >= 18 else 'minor'", context)
        assert result == "minor"

    def test_complex_expressions(self, expression_engine: ExpressionEngine, math_context: dict):
        """Test complex expressions."""
        result = expression_engine.evaluate("a + b * c", math_context)
        expected = 10 + 20 * 3.14
        assert result == expected

        result = expression_engine.evaluate("sum(prices) * (1 - 0.1)", math_context)
        expected = sum(math_context["prices"]) * 0.9
        assert result == expected

    def test_function_with_context(self, expression_engine: ExpressionEngine, sample_context: dict):
        """Test functions with context variables."""
        result = expression_engine.evaluate(
            "round(order.total * config.tax_rate, 2)", sample_context
        )
        expected = round(1059.97 * 0.1, 2)
        assert result == expected

    def test_nested_function_calls(self, expression_engine: ExpressionEngine):
        """Test nested function calls."""
        result = expression_engine.evaluate("upper(trim('  hello world  '))")
        assert result == "HELLO WORLD"

        result = expression_engine.evaluate("round(abs(-3.14159), 2)")
        assert result == 3.14

    def test_list_operations(self, expression_engine: ExpressionEngine):
        """Test list operations."""
        result = expression_engine.evaluate("[1, 2, 3] + [4, 5]")
        assert result == [1, 2, 3, 4, 5]

        result = expression_engine.evaluate("len([1, 2, 3])")
        assert result == 3

        result = expression_engine.evaluate("sum([1, 2, 3, 4])")
        assert result == 10

    def test_dict_operations(self, expression_engine: ExpressionEngine):
        """Test dictionary operations."""
        result = expression_engine.evaluate("{'a': 1, 'b': 2}['a']")
        assert result == 1

        result = expression_engine.evaluate("len({'a': 1, 'b': 2, 'c': 3})")
        assert result == 3

    def test_custom_function_registration(self, expression_engine: ExpressionEngine):
        """Test custom function registration."""

        def multiply(a, b):
            return a * b

        expression_engine.register_function("multiply", multiply)
        result = expression_engine.evaluate("multiply(4, 5)")
        assert result == 20

    def test_custom_function_with_context(self, expression_engine: ExpressionEngine):
        """Test custom function with context."""

        def calculate_tax(amount, rate=0.1):
            return amount * rate

        expression_engine.register_function("tax", calculate_tax)
        context = {"amount": 1000}
        result = expression_engine.evaluate("amount + tax(amount, 0.08)", context)
        assert result == 1080.0

    def test_function_override_builtin(self, expression_engine: ExpressionEngine):
        """Test overriding built-in functions."""

        def custom_abs(x):
            return x if x >= 0 else -x

        expression_engine.register_function("abs", custom_abs)
        result = expression_engine.evaluate("abs(-10)")
        assert result == 10

    def test_undefined_function(self, expression_engine: ExpressionEngine):
        """Test undefined function error."""
        # The engine wraps UndefinedFunctionError in ExpressionEvalError
        with pytest.raises((UndefinedFunctionError, ExpressionEvalError)):
            expression_engine.evaluate("undefined_function(1, 2, 3)")

    def test_expression_validation(self, expression_engine: ExpressionEngine):
        """Test expression validation."""
        # Valid expression
        errors = expression_engine.validate("2 + 3 * 4")
        assert len(errors) == 0

        # Invalid expression
        errors = expression_engine.validate("2 +")
        assert len(errors) > 0

    def test_get_variables(self, expression_engine: ExpressionEngine):
        """Test variable extraction."""
        variables = expression_engine.get_variables("price * quantity + tax")
        assert "price" in variables
        assert "quantity" in variables
        assert "tax" in variables

        variables = expression_engine.get_variables("2 + 3 * 4")
        assert len(variables) == 0

    def test_cache_functionality(self, expression_engine: ExpressionEngine):
        """Test expression caching."""
        # First evaluation
        result1 = expression_engine.evaluate("2 + 3 * 4")

        # Second evaluation (same result)
        result2 = expression_engine.evaluate("2 + 3 * 4")

        assert result1 == result2
        assert result1 == 14

    def test_clear_cache(self, expression_engine: ExpressionEngine):
        """Test clearing cache."""
        expression_engine.evaluate("2 + 3")

        # Cache may or may not be used depending on implementation
        if expression_engine.cache_stats:
            expression_engine.clear_cache()
            stats_after = expression_engine.cache_stats
            assert stats_after["size"] == 0


class TestCompiledExpression:
    """Test CompiledExpression class."""

    def test_compile_valid_expression(self):
        """Test compiling a valid expression."""
        expr = CompiledExpression.compile("2 + 3 * 4")
        assert expr.expression == "2 + 3 * 4"
        assert expr.ast_node is not None

    def test_compile_invalid_expression(self):
        """Test compiling an invalid expression."""
        with pytest.raises(ExpressionParseError):
            CompiledExpression.compile("2 +")

    def test_compiled_evaluation(self):
        """Test evaluating a compiled expression."""
        compiled = CompiledExpression.compile("x + y")
        result = compiled.evaluate({"x": 10, "y": 20})
        assert result == 30


class TestSafeEvaluator:
    """Test SafeEvaluator class."""

    def test_safe_evaluator_creation(self):
        """Test SafeEvaluator creation."""
        evaluator = SafeEvaluator()
        assert evaluator is not None

    def test_safe_evaluator_with_names(self):
        """Test SafeEvaluator with names."""
        names = {"x": 10, "y": 20}
        evaluator = SafeEvaluator(names=names)
        result = evaluator.eval("x + y")
        assert result == 30

    def test_safe_evaluator_with_functions(self):
        """Test SafeEvaluator with functions."""

        def custom_func(x):
            return x * 2

        functions = {"custom_func": custom_func}
        evaluator = SafeEvaluator(functions=functions)
        result = evaluator.eval("custom_func(5)")
        assert result == 10

    def test_safe_evaluator_error_handling(self):
        """Test SafeEvaluator error handling."""
        evaluator = SafeEvaluator()
        with pytest.raises(ExpressionEvalError):
            evaluator.eval("undefined_var")


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_evaluate_function(self):
        """Test evaluate convenience function."""
        result = evaluate("2 + 3 * 4")
        assert result == 14

        result = evaluate("x + y", {"x": 10, "y": 20})
        assert result == 30

    def test_validate_function(self):
        """Test validate convenience function."""
        errors = validate("2 + 3 * 4")
        assert len(errors) == 0

        errors = validate("2 +")
        assert len(errors) > 0

    def test_register_function_global(self):
        """Test register_function convenience function."""

        def double(x):
            return x * 2

        register_function("double", double)
        result = evaluate("double(5)")
        assert result == 10

    def test_get_default_engine(self):
        """Test get_default_engine function."""
        engine = get_default_engine()
        assert isinstance(engine, ExpressionEngine)

        # Should return the same instance
        engine2 = get_default_engine()
        assert engine is engine2


class TestPerformance:
    """Performance tests."""

    def test_simple_expression_performance(self, expression_engine: ExpressionEngine):
        """Test simple expression performance."""
        start_time = time.time()
        for _ in range(1000):
            expression_engine.evaluate("2 + 3 * 4")
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / 1000

        # Should be less than 0.1ms per evaluation
        assert avg_time < 0.0001, f"Average time {avg_time} is too slow"

    def test_complex_expression_performance(self, expression_engine: ExpressionEngine):
        """Test complex expression performance."""
        context = {"a": 10, "b": 20, "c": 30}

        start_time = time.time()
        for _ in range(100):
            expression_engine.evaluate("(a + b) * c / 2 + max(a, b, c) - min(a, b, c)", context)
        end_time = time.time()

        elapsed = end_time - start_time
        avg_time = elapsed / 100

        # Should be less than 1ms per evaluation
        assert avg_time < 0.001, f"Average time {avg_time} is too slow"

    def test_cache_performance(self, expression_engine: ExpressionEngine):
        """Test repeated expression evaluation performance."""
        expr = "sum([x**2 for x in range(10)])"

        # First run
        result1 = expression_engine.evaluate(expr)

        # Second run should give same result
        result2 = expression_engine.evaluate(expr)

        assert result1 == result2
        assert result1 == sum([x**2 for x in range(10)])  # Verify correctness
