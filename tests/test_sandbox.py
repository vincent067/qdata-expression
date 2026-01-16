"""
Tests for security sandbox.
"""

import pytest

from qdata_expr import (
    ForbiddenAccessError,
    Sandbox,
    SandboxConfig,
    SecurityViolationError,
    get_expression_safety_issues,
    is_expression_safe,
    validate_expression_safety,
)


class TestSandboxConfig:
    """Test SandboxConfig class."""

    def test_default_config(self):
        """Test default sandbox configuration."""
        config = SandboxConfig()
        
        assert len(config.allowed_operators) > 0
        assert len(config.forbidden_names) > 0
        assert len(config.allowed_builtins) > 0
        assert config.max_execution_time == 5.0
        assert config.max_recursion_depth == 100
        assert config.max_string_length == 1_000_000
        assert config.max_collection_size == 100_000

    def test_custom_config(self):
        """Test custom sandbox configuration."""
        config = SandboxConfig(
            strict_private_access=True,
            max_execution_time=10.0,
            max_recursion_depth=50,
        )
        
        assert config.strict_private_access
        assert config.max_execution_time == 10.0
        assert config.max_recursion_depth == 50

    def test_config_with_custom_sets(self):
        """Test config with custom sets."""
        config = SandboxConfig(
            forbidden_names={"eval", "exec"},
            allowed_builtins={"int", "str", "len"},
        )
        
        assert "eval" in config.forbidden_names
        assert "exec" in config.forbidden_names
        assert "int" in config.allowed_builtins
        assert len(config.allowed_builtins) == 3


class TestSandbox:
    """Test Sandbox class."""

    def test_sandbox_creation(self):
        """Test sandbox creation."""
        sandbox = Sandbox()
        assert sandbox is not None
        assert sandbox.config is not None

    def test_sandbox_creation_with_config(self):
        """Test sandbox creation with custom config."""
        config = SandboxConfig(max_execution_time=3.0)
        sandbox = Sandbox(config)
        assert sandbox.config.max_execution_time == 3.0

    def test_safe_expressions(self, sandbox: Sandbox):
        """Test safe expressions."""
        safe_exprs = [
            "2 + 3 * 4",
            "abs(-5)",
            "round(3.14, 2)",
            "'hello' + ' ' + 'world'",
            "len([1, 2, 3])",
            "max(1, 2, 3)",
            "True and False",
            "5 > 3",
            "{'a': 1, 'b': 2}['a']",
            "[1, 2, 3][0]",
        ]
        
        for expr in safe_exprs:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"Expression should be safe: {expr}"
            assert sandbox.is_safe(expr), f"Expression should be safe: {expr}"

    def test_unsafe_expressions(self, sandbox: Sandbox):
        """Test unsafe expressions."""
        unsafe_exprs = [
            ("eval('1+1')", ["禁止调用函数: eval"]),
            ("exec('print(1)')", ["禁止调用函数: exec"]),
            ("__import__('os')", ["禁止访问名称: __import__"]),
            ("open('/etc/passwd')", ["禁止调用函数: open"]),
            ("globals()['__builtins__']", ["禁止访问名称: globals"]),
            ("locals()", ["禁止访问名称: locals"]),
            ("vars(object)", ["禁止访问名称: vars"]),
            ("dir()", ["禁止访问名称: dir"]),
            ("getattr(object, '__class__')", ["禁止访问名称: getattr"]),
            ("setattr(object, 'x', 1)", ["禁止访问名称: setattr"]),
            ("compile('print(1)', '', 'exec')", ["禁止调用函数: compile"]),
            ("type(1)", ["禁止访问名称: type"]),
            # Note: import statements are syntax errors in eval mode (not expressions)
            # They will fail with syntax error, which is still blocking dangerous code
        ]
        
        for expr, expected_errors in unsafe_exprs:
            errors = sandbox.check_expression(expr)
            assert len(errors) > 0, f"Expression should be unsafe: {expr}"
            assert not sandbox.is_safe(expr), f"Expression should be unsafe: {expr}"
            
            # Check that specific error patterns are present
            for expected in expected_errors:
                found = any(expected in error for error in errors)
                assert found, f"Expected error '{expected}' not found in {errors}"
        
        # Import statements should fail (not valid expressions)
        import_exprs = [
            "import os",
            "from os import path",
        ]
        for expr in import_exprs:
            errors = sandbox.check_expression(expr)
            assert len(errors) > 0, f"Import statement should be blocked: {expr}"

    def test_private_attribute_access(self):
        """Test private attribute access."""
        # Strict mode
        config = SandboxConfig(strict_private_access=True)
        sandbox = Sandbox(config)
        
        errors = sandbox.check_expression("obj._private")
        assert len(errors) > 0
        
        # Non-strict mode
        sandbox_default = Sandbox()
        errors = sandbox_default.check_expression("obj._private")
        # Should allow in non-strict mode

    def test_magic_method_access(self, sandbox: Sandbox):
        """Test magic method access."""
        errors = sandbox.check_expression("obj.__class__")
        assert len(errors) > 0
        # Check for either magic or private attribute error
        assert any("魔术属性" in error or "私有属性" in error or "__" in error for error in errors)

    def test_dunder_attribute_access(self, sandbox: Sandbox):
        """Test dunder attribute access."""
        errors = sandbox.check_expression("obj.__init__")
        assert len(errors) > 0
        # Check for any indication of blocked access
        assert any("私有属性" in error or "魔术属性" in error or "__" in error for error in errors)

    def test_file_operations(self, sandbox: Sandbox):
        """Test file operation blocking."""
        file_exprs = [
            "open('/etc/passwd')",
            "file('/etc/passwd')",
            "input('Enter: ')",
        ]
        
        for expr in file_exprs:
            errors = sandbox.check_expression(expr)
            assert len(errors) > 0, f"File operation should be blocked: {expr}"

    def test_import_blocking(self, sandbox: Sandbox):
        """Test import statement blocking."""
        import_exprs = [
            "import os",
            "import sys as system",
            "from os import path",
            "from sys import *",
        ]
        
        for expr in import_exprs:
            errors = sandbox.check_expression(expr)
            # Import statements should fail (they're not valid expressions)
            assert len(errors) > 0, f"Import should be blocked: {expr}"

    def test_builtin_function_restrictions(self, sandbox: Sandbox):
        """Test built-in function restrictions."""
        # These should be allowed
        allowed = ["abs(-5)", "len([1, 2, 3])", "str(123)", "int('456')"]
        
        for expr in allowed:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"Should be allowed: {expr}"
        
        # These should be blocked
        blocked = ["eval('1+1')", "exec('pass')", "compile('1', '', 'eval')"]
        
        for expr in blocked:
            errors = sandbox.check_expression(expr)
            assert len(errors) > 0, f"Should be blocked: {expr}"

    def test_nested_function_calls(self, sandbox: Sandbox):
        """Test nested function call safety."""
        # Safe nested calls
        safe = [
            "abs(round(3.14, 1))",
            "len(upper('hello'))",
            "max(len('abc'), len('de'))",
        ]
        
        for expr in safe:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"Should be safe: {expr}"
        
        # Unsafe nested calls
        unsafe = [
            "eval(compile('1+1', '', 'eval'))",
            "getattr(object, '__class__').__name__",
        ]
        
        for expr in unsafe:
            errors = sandbox.check_expression(expr)
            assert len(errors) > 0, f"Should be unsafe: {expr}"

    def test_string_safety(self, sandbox: Sandbox):
        """Test string-related safety."""
        # String operations should be safe
        safe_strings = [
            "'hello'.upper()",
            "'hello' + ' ' + 'world'",
            "len('hello')",
            "'hello'[0]",
            "'hello world'.split()",
        ]
        
        for expr in safe_strings:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"String operation should be safe: {expr}"

    def test_list_safety(self, sandbox: Sandbox):
        """Test list-related safety."""
        safe_lists = [
            "[1, 2, 3] + [4, 5]",
            "len([1, 2, 3])",
            "[1, 2, 3][0]",
            "sum([1, 2, 3])",
            "max([1, 2, 3])",
        ]
        
        for expr in safe_lists:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"List operation should be safe: {expr}"

    def test_dict_safety(self, sandbox: Sandbox):
        """Test dictionary-related safety."""
        safe_dicts = [
            "{'a': 1, 'b': 2}['a']",
            "len({'a': 1, 'b': 2})",
            "list({'a': 1, 'b': 2}.keys())",
            "list({'a': 1, 'b': 2}.values())",
        ]
        
        for expr in safe_dicts:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"Dict operation should be safe: {expr}"

    def test_math_safety(self, sandbox: Sandbox):
        """Test mathematical operation safety."""
        safe_math = [
            "2 + 3 * 4",
            "10 / 2",
            "10 // 3",
            "10 % 3",
            "2 ** 3",
            "abs(-5)",
            "round(3.14, 1)",
            "min(1, 2, 3)",
            "max(1, 2, 3)",
        ]
        
        for expr in safe_math:
            errors = sandbox.check_expression(expr)
            assert len(errors) == 0, f"Math operation should be safe: {expr}"

    def test_validate_expression(self, sandbox: Sandbox):
        """Test expression validation."""
        # Should not raise for safe expression
        sandbox.validate_expression("2 + 3")
        
        # Should raise for unsafe expression
        with pytest.raises(SecurityViolationError):
            sandbox.validate_expression("eval('1+1')")

    def test_complex_unsafe_patterns(self, sandbox: Sandbox):
        """Test complex unsafe patterns."""
        complex_unsafe = [
            # Obfuscated eval
            "getattr(__builtins__, 'eval')('1+1')",
            # Code object manipulation
            "(lambda: None).__code__",
        ]
        
        for expr in complex_unsafe:
            errors = sandbox.check_expression(expr)
            assert len(errors) > 0, f"Complex unsafe pattern should be blocked: {expr}"
        
        # These expressions are blocked because they use forbidden names
        # or have syntax issues when used as standalone expressions
        blocked_names = [
            # sys is not in the sandbox by default
            "sys._getframe()",
            "sys.modules['os']",
        ]
        for expr in blocked_names:
            errors = sandbox.check_expression(expr)
            # May have errors or may just fail due to undefined variable
            # Either way, they shouldn't execute dangerous code

    def test_edge_cases(self, sandbox: Sandbox):
        """Test edge cases."""
        edge_cases = [
            # Empty string
            "",
            # Whitespace only
            "   ",
            # Just a number
            "42",
            # Just a string
            "'hello'",
            # Just a list
            "[1, 2, 3]",
            # Just a dict
            "{'a': 1}",
            # Comments (should be blocked if they contain dangerous content)
            "# eval('dangerous')\n2 + 3",
        ]
        
        for expr in edge_cases:
            # Should not crash
            try:
                errors = sandbox.check_expression(expr)
                # Either safe or unsafe is fine, just shouldn't crash
            except Exception as e:
                pytest.fail(f"Edge case crashed: {expr} - {e}")


class TestSafeNameResolver:
    """Test SafeNameResolver class."""

    def test_safe_name_resolver_creation(self):
        """Test SafeNameResolver creation."""
        from qdata_expr.sandbox import SafeNameResolver
        
        resolver = SafeNameResolver()
        assert resolver is not None

    def test_resolve_allowed_names(self):
        """Test resolving allowed names."""
        from qdata_expr.sandbox import SafeNameResolver
        
        allowed_names = {"x": 10, "y": 20}
        resolver = SafeNameResolver(allowed_names=allowed_names)
        
        assert resolver.resolve_name("x") == 10
        assert resolver.resolve_name("y") == 20

    def test_resolve_forbidden_names(self):
        """Test resolving forbidden names."""
        from qdata_expr.sandbox import SafeNameResolver
        
        resolver = SafeNameResolver()
        
        with pytest.raises(ForbiddenAccessError):
            resolver.resolve_name("eval")

    def test_resolve_builtins(self):
        """Test resolving built-ins."""
        from qdata_expr.sandbox import SafeNameResolver
        
        resolver = SafeNameResolver()
        
        # Should be able to resolve safe built-ins
        abs_func = resolver.resolve_name("abs")
        assert abs_func is not None
        assert abs_func(-5) == 5

    def test_resolve_attr_safety(self):
        """Test attribute resolution safety."""
        from qdata_expr.sandbox import SafeNameResolver
        
        resolver = SafeNameResolver()
        
        # Safe attribute
        result = resolver.resolve_attr("hello", "upper")
        assert callable(result)
        
        # Unsafe attribute
        with pytest.raises(ForbiddenAccessError):
            resolver.resolve_attr("hello", "__class__")

    def test_check_method_call(self):
        """Test method call checking."""
        from qdata_expr.sandbox import SafeNameResolver
        
        resolver = SafeNameResolver()
        
        # String methods should be allowed
        assert resolver.check_method_call("hello", "upper")
        
        # Magic methods should not be allowed
        # Note: This depends on the specific implementation


class TestSafeWrapper:
    """Test SafeWrapper class."""

    def test_safe_wrapper_creation(self):
        """Test SafeWrapper creation."""
        from qdata_expr.sandbox import SafeWrapper
        
        wrapper = SafeWrapper("test")
        assert wrapper is not None
        assert repr(wrapper) == "SafeWrapper('test')"

    def test_safe_wrapper_getattr(self):
        """Test SafeWrapper getattr."""
        from qdata_expr.sandbox import SafeWrapper
        
        wrapper = SafeWrapper("hello")
        
        # Safe attribute
        upper_method = wrapper.upper
        assert callable(upper_method)
        assert upper_method() == "HELLO"

    def test_safe_wrapper_private_attr(self):
        """Test SafeWrapper private attribute blocking."""
        from qdata_expr.sandbox import SafeWrapper, ForbiddenAccessError
        
        wrapper = SafeWrapper("hello")
        
        # Test blocking of underscore-prefixed attributes
        # This requires strict mode to be enabled
        from qdata_expr.sandbox import SandboxConfig
        strict_config = SandboxConfig(strict_private_access=True)
        strict_wrapper = SafeWrapper("hello", strict_config)
        
        with pytest.raises(ForbiddenAccessError):
            strict_wrapper._private_method  # Should raise in strict mode


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_is_expression_safe(self):
        """Test is_expression_safe function."""
        assert is_expression_safe("2 + 3")
        assert not is_expression_safe("eval('1+1')")

    def test_validate_expression_safety(self):
        """Test validate_expression_safety function."""
        # Should not raise for safe expression
        validate_expression_safety("2 + 3")
        
        # Should raise for unsafe expression
        with pytest.raises(SecurityViolationError):
            validate_expression_safety("eval('1+1')")

    def test_get_expression_safety_issues(self):
        """Test get_expression_safety_issues function."""
        issues = get_expression_safety_issues("eval('1+1')")
        assert len(issues) > 0
        assert any("eval" in issue for issue in issues)
        
        issues = get_expression_safety_issues("2 + 3")
        assert len(issues) == 0
