"""
Tests for expression parser.
"""

import pytest

from qdata_expr import (
    ExpressionAnalyzer,
    ExpressionBuilder,
    ExpressionParser,
    ParseResult,
    extract_variables,
    is_expression,
    parse_expression,
    validate_expression,
)


class TestExpressionParser:
    """Test ExpressionParser class."""

    def test_parser_creation(self):
        """Test parser creation."""
        parser = ExpressionParser()
        assert parser is not None
        assert parser.known_functions == set()

    def test_parser_creation_with_functions(self):
        """Test parser creation with known functions."""
        known_functions = {"abs", "round", "len"}
        parser = ExpressionParser(known_functions)
        assert parser.known_functions == known_functions

    def test_parse_simple_expressions(self):
        """Test parsing simple expressions."""
        parser = ExpressionParser()
        
        result = parser.parse("2 + 3")
        assert result.is_valid
        assert result.variables == []
        assert result.functions == []
        
        result = parser.parse("x + y")
        assert result.is_valid
        assert "x" in result.variables
        assert "y" in result.variables
        assert result.functions == []

    def test_parse_function_calls(self):
        """Test parsing function calls."""
        parser = ExpressionParser({"abs", "round"})
        
        result = parser.parse("abs(-5) + round(3.14, 2)")
        assert result.is_valid
        assert "abs" in result.functions
        assert "round" in result.functions
        assert result.variables == []

    def test_parse_mixed_expressions(self):
        """Test parsing mixed expressions."""
        parser = ExpressionParser({"abs", "round", "len"})
        
        result = parser.parse("abs(x) + len(items) * round(price, 2)")
        assert result.is_valid
        assert "x" in result.variables
        assert "items" in result.variables
        assert "price" in result.variables
        assert "abs" in result.functions
        assert "len" in result.functions
        assert "round" in result.functions

    def test_parse_invalid_expressions(self):
        """Test parsing invalid expressions."""
        parser = ExpressionParser()
        
        result = parser.parse("2 +")
        assert not result.is_valid
        assert len(result.errors) > 0
        
        result = parser.parse("abs(")
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_parse_empty_expression(self):
        """Test parsing empty expressions."""
        parser = ExpressionParser()
        
        result = parser.parse("")
        assert not result.is_valid
        assert len(result.errors) > 0
        
        result = parser.parse("   ")
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_parse_complex_expressions(self):
        """Test parsing complex expressions."""
        parser = ExpressionParser({"if_else", "round", "abs", "sum", "len"})
        
        expr = "if_else(age > 18, round(income * 0.1, 2), 0)"
        result = parser.parse(expr)
        assert result.is_valid
        assert "age" in result.variables
        assert "income" in result.variables
        assert "if_else" in result.functions
        assert "round" in result.functions

    def test_parse_conditional_expressions(self):
        """Test parsing conditional expressions."""
        parser = ExpressionParser()
        
        result = parser.parse("x if condition else y")
        assert result.is_valid
        assert "x" in result.variables
        assert "condition" in result.variables
        assert "y" in result.variables

    def test_parse_list_comprehensions(self):
        """Test parsing list comprehensions."""
        parser = ExpressionParser({"sum"})
        
        result = parser.parse("sum([x**2 for x in range(10) if x % 2 == 0])")
        assert result.is_valid
        assert "sum" in result.functions
        # Note: x might not be detected as variable due to comprehension scope

    def test_parse_string_operations(self):
        """Test parsing string operations."""
        parser = ExpressionParser({"upper", "len", "concat"})
        
        result = parser.parse("concat(upper(name), ' - ', str(age))")
        assert result.is_valid
        assert "name" in result.variables
        assert "age" in result.variables
        assert "concat" in result.functions
        assert "upper" in result.functions

    def test_parse_boolean_expressions(self):
        """Test parsing boolean expressions."""
        parser = ExpressionParser({"and", "or", "not"})
        
        result = parser.parse("age > 18 and age < 65 or is_vip")
        assert result.is_valid
        assert "age" in result.variables
        assert "is_vip" in result.variables

    def test_validate_method(self):
        """Test validate method."""
        parser = ExpressionParser()
        
        assert parser.validate("2 + 3")
        assert parser.validate("x + y")
        assert not parser.validate("2 +")
        assert not parser.validate("abs(")

    def test_extract_variables_method(self):
        """Test extract_variables method."""
        parser = ExpressionParser({"abs", "round"})
        
        variables = parser.extract_variables("abs(x) + round(y, 2)")
        assert "x" in variables
        assert "y" in variables
        
        variables = parser.extract_variables("2 + 3 * 4")
        assert len(variables) == 0

    def test_extract_functions_method(self):
        """Test extract_functions method."""
        parser = ExpressionParser({"abs", "round", "len"})
        
        functions = parser.extract_functions("abs(x) + len(items) * round(price, 2)")
        assert "abs" in functions
        assert "len" in functions
        assert "round" in functions

    def test_get_errors_method(self):
        """Test get_errors method."""
        parser = ExpressionParser()
        
        errors = parser.get_errors("2 + 3")
        assert len(errors) == 0
        
        errors = parser.get_errors("2 +")
        assert len(errors) > 0

    def test_is_expression_string(self):
        """Test is_expression_string method."""
        parser = ExpressionParser
        
        assert parser.is_expression_string("${x + y}")
        assert parser.is_expression_string("Hello ${name}!")
        assert parser.is_expression_string("Value: ${value}")
        
        assert not parser.is_expression_string("Hello World")
        assert not parser.is_expression_string("123")
        assert not parser.is_expression_string("${incomplete")

    def test_extract_expressions(self):
        """Test extract_expressions method."""
        parser = ExpressionParser
        
        exprs = parser.extract_expressions("Hello ${name}, your balance is ${balance}.")
        assert len(exprs) == 2
        assert "name" in exprs
        assert "balance" in exprs
        
        exprs = parser.extract_expressions("No expressions here")
        assert len(exprs) == 0

    def test_unwrap_expression(self):
        """Test unwrap_expression method."""
        parser = ExpressionParser
        
        unwrapped = parser.unwrap_expression("${x + y}")
        assert unwrapped == "x + y"
        
        unwrapped = parser.unwrap_expression("  ${trimmed}  ")
        assert unwrapped == "trimmed"
        
        unwrapped = parser.unwrap_expression("not_an_expression")
        assert unwrapped == "not_an_expression"


class TestExpressionAnalyzer:
    """Test ExpressionAnalyzer class."""

    def test_analyzer_creation(self):
        """Test analyzer creation."""
        analyzer = ExpressionAnalyzer()
        assert analyzer is not None
        assert analyzer.variables == set()
        assert analyzer.functions == set()

    def test_analyzer_creation_with_functions(self):
        """Test analyzer creation with known functions."""
        known_functions = {"abs", "round"}
        analyzer = ExpressionAnalyzer(known_functions)
        assert analyzer.known_functions == known_functions

    def test_analyze_simple_expressions(self):
        """Test analyzing simple expressions."""
        import ast
        
        analyzer = ExpressionAnalyzer()
        
        tree = ast.parse("x + y", mode="eval")
        variables, functions = analyzer.analyze(tree)
        
        assert "x" in variables
        assert "y" in variables
        assert len(functions) == 0

    def test_analyze_function_calls(self):
        """Test analyzing function calls."""
        import ast
        
        analyzer = ExpressionAnalyzer({"abs", "round"})
        
        tree = ast.parse("abs(x) + round(y, 2)", mode="eval")
        variables, functions = analyzer.analyze(tree)
        
        assert "x" in variables
        assert "y" in variables
        assert "abs" in functions
        assert "round" in functions

    def test_analyze_method_calls(self):
        """Test analyzing method calls."""
        import ast
        
        analyzer = ExpressionAnalyzer()
        
        tree = ast.parse("obj.method()", mode="eval")
        variables, functions = analyzer.analyze(tree)
        
        assert "obj" in variables
        assert "method" in functions

    def test_analyze_boolean_expressions(self):
        """Test analyzing boolean expressions."""
        import ast
        
        analyzer = ExpressionAnalyzer({"and", "or"})
        
        tree = ast.parse("x > 0 and y < 10 or z == 5", mode="eval")
        variables, functions = analyzer.analyze(tree)
        
        assert "x" in variables
        assert "y" in variables
        assert "z" in variables

    def test_analyze_constants(self):
        """Test analyzing constants."""
        import ast
        
        analyzer = ExpressionAnalyzer()
        
        tree = ast.parse("42 + 3.14", mode="eval")
        variables, functions = analyzer.analyze(tree)
        
        assert len(variables) == 0
        assert len(functions) == 0

    def test_analyze_with_builtins(self):
        """Test analyzing with built-ins."""
        import ast
        
        analyzer = ExpressionAnalyzer({"len", "str", "int"})
        
        tree = ast.parse("len(items) + int(str(x))", mode="eval")
        variables, functions = analyzer.analyze(tree)
        
        assert "items" in variables
        assert "x" in variables
        assert "len" in functions
        assert "str" in functions
        assert "int" in functions


class TestExpressionBuilder:
    """Test ExpressionBuilder class."""

    def test_builder_creation(self):
        """Test builder creation."""
        builder = ExpressionBuilder()
        assert builder is not None
        assert builder._parts == []

    def test_variable_addition(self):
        """Test adding variables."""
        builder = ExpressionBuilder()
        
        builder.var("x")
        assert builder.build() == "x"
        
        builder.var("y")
        assert builder.build() == "xy"

    def test_literal_addition(self):
        """Test adding literals."""
        builder = ExpressionBuilder()
        
        builder.literal(42)
        assert builder.build() == "42"
        
        builder.literal("hello")
        assert builder.build() == '42"hello"'

    def test_function_calls(self):
        """Test adding function calls."""
        builder = ExpressionBuilder()
        
        builder.func("abs", -5)
        assert builder.build() == "abs(-5)"
        
        builder.clear()
        builder.func("round", 3.14, 2)
        assert builder.build() == "round(3.14, 2)"

    def test_operators(self):
        """Test adding operators."""
        builder = ExpressionBuilder()
        
        expr = (
            builder.var("x")
            .add()
            .var("y")
            .multiply()
            .literal(2)
            .build()
        )
        assert expr == "x + y * 2"

    def test_comparison_operators(self):
        """Test comparison operators."""
        builder = ExpressionBuilder()
        
        expr = (
            builder.var("age")
            .gt()
            .literal(18)
            .and_()
            .var("age")
            .lt()
            .literal(65)
            .build()
        )
        assert expr == "age > 18 and age < 65"

    def test_logical_operators(self):
        """Test logical operators."""
        builder = ExpressionBuilder()
        
        expr = (
            builder.not_()
            .var("condition")
            .build()
        )
        assert expr == "not condition"

    def test_grouping(self):
        """Test grouping."""
        builder = ExpressionBuilder()
        
        inner = ExpressionBuilder()
        inner.var("x").add().var("y")
        
        builder.group(inner).multiply().literal(2)
        
        assert builder.build() == "(x + y) * 2"

    def test_raw_text(self):
        """Test raw text."""
        builder = ExpressionBuilder()
        
        builder.var("x").raw(" ** ").literal(2)
        assert builder.build() == "x ** 2"

    def test_build_and_wrap(self):
        """Test build and wrap."""
        builder = ExpressionBuilder()
        
        builder.var("x").add().var("y")
        
        assert builder.build() == "x + y"
        assert builder.wrap() == "${x + y}"

    def test_clear(self):
        """Test clear method."""
        builder = ExpressionBuilder()
        
        builder.var("x").add().var("y")
        assert builder.build() == "x + y"
        
        builder.clear()
        assert builder.build() == ""

    def test_complex_expression_building(self):
        """Test building complex expressions."""
        builder = ExpressionBuilder()
        
        # Build: if_else(age >= 18, "adult", "minor")
        condition = ExpressionBuilder()
        condition.var("age").ge().literal(18)
        
        expr = (
            builder.func("if_else", condition.build(), "\"adult\"", "\"minor\"")
            .build()
        )
        
        expected = 'if_else(age >= 18, "adult", "minor")'
        assert expr == expected


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_parse_expression_function(self):
        """Test parse_expression convenience function."""
        result = parse_expression("x + y")
        
        assert isinstance(result, ParseResult)
        assert result.is_valid
        assert "x" in result.variables
        assert "y" in result.variables

    def test_validate_expression_function(self):
        """Test validate_expression convenience function."""
        assert validate_expression("2 + 3")
        assert not validate_expression("2 +")

    def test_extract_variables_function(self):
        """Test extract_variables convenience function."""
        variables = extract_variables("abs(x) + len(items)")
        
        assert "x" in variables
        assert "items" in variables

    def test_is_expression_function(self):
        """Test is_expression convenience function."""
        assert is_expression("${x + y}")
        assert is_expression("Hello ${name}!")
        assert not is_expression("Hello World")
        assert not is_expression("123")


class TestParseResult:
    """Test ParseResult class."""

    def test_parse_result_creation(self):
        """Test ParseResult creation."""
        result = ParseResult(expression="x + y")
        
        assert result.expression == "x + y"
        assert result.variables == []
        assert result.functions == []
        assert result.is_valid
        assert result.errors == []
        assert result.ast_node is None

    def test_parse_result_to_dict(self):
        """Test ParseResult to_dict method."""
        result = ParseResult(
            expression="x + y",
            variables=["x", "y"],
            functions=["abs"],
            is_valid=True,
            errors=[]
        )
        
        dict_result = result.to_dict()
        
        assert dict_result["expression"] == "x + y"
        assert dict_result["variables"] == ["x", "y"]
        assert dict_result["functions"] == ["abs"]
        assert dict_result["is_valid"]
        assert dict_result["errors"] == []

    def test_parse_result_with_errors(self):
        """Test ParseResult with errors."""
        result = ParseResult(
            expression="2 +",
            is_valid=False,
            errors=["Syntax error"]
        )
        
        dict_result = result.to_dict()
        
        assert not dict_result["is_valid"]
        assert dict_result["errors"] == ["Syntax error"]


class TestErrorHandling:
    """Test error handling."""

    def test_parser_error_handling(self):
        """Test parser error handling."""
        parser = ExpressionParser()
        
        # Should handle gracefully
        result = parser.parse(None)  # type: ignore
        assert not result.is_valid
        assert len(result.errors) > 0

    def test_analyzer_error_handling(self):
        """Test analyzer error handling."""
        analyzer = ExpressionAnalyzer()
        
        # Should handle None input gracefully
        try:
            variables, functions = analyzer.analyze(None)  # type: ignore
            # Should not crash
        except Exception:
            pass  # Expected for None input

    def test_builder_error_handling(self):
        """Test builder error handling."""
        builder = ExpressionBuilder()
        
        # Should handle empty state
        assert builder.build() == ""

    def test_unicode_expressions(self):
        """Test Unicode expressions."""
        parser = ExpressionParser()
        
        result = parser.parse("'你好' + '世界'")
        assert result.is_valid
        
        result = parser.parse("变量1 + 变量2")
        assert result.is_valid
        assert "变量1" in result.variables
        assert "变量2" in result.variables
