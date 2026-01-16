"""
Security examples for qdata-expression.
"""

from qdata_expr import (
    ExpressionEngine,
    Sandbox,
    SandboxConfig,
    SecurityViolationError,
    get_expression_safety_issues,
    is_expression_safe,
    validate_expression_safety,
)


def safe_expressions():
    """Examples of safe expressions."""
    print("=== Safe Expressions ===")
    
    engine = ExpressionEngine()
    
    # 这些表达式都是安全的
    safe_exprs = [
        "2 + 3 * 4",
        "abs(-5) + round(3.14, 2)",
        "max(1, 2, 3) * min(4, 5, 6)",
        "'hello' + ' ' + 'world'",
        "len([1, 2, 3])",
        "sum([1, 2, 3, 4, 5])",
        "True and False or True",
        "5 > 3 and 10 < 20",
        "{'a': 1, 'b': 2}['a'] + 10",
        "[x**2 for x in range(5)]",
    ]
    
    for expr in safe_exprs:
        try:
            result = engine.evaluate(expr)
            print(f"✓ {expr} = {result}")
        except Exception as e:
            print(f"✗ {expr} -> Error: {e}")
    
    print()


def unsafe_expressions():
    """Examples of unsafe expressions that should be blocked."""
    print("=== Unsafe Expressions (Blocked) ===")
    
    engine = ExpressionEngine()
    
    # 这些表达式是不安全的，应该被阻止
    unsafe_exprs = [
        "eval('1+1')",
        "exec('print(\"hacked\")')",
        "__import__('os').system('echo hacked')",
        "open('/etc/passwd').read()",
        "globals()['__builtins__']['eval']('1+1')",
        "getattr(object, '__class__')",
        "compile('print(\"hacked\")', '', 'exec')",
        "import os",
        "from os import system",
        "type(1)",
        "vars(object)",
        "dir()",
        "locals()",
        "sys._getframe()",
        "object.__subclasses__()",
    ]
    
    for expr in unsafe_exprs:
        try:
            result = engine.evaluate(expr)
            print(f"⚠ {expr} = {result} (Should have been blocked!)")
        except SecurityViolationError as e:
            print(f"✓ {expr} -> Blocked: {e}")
        except Exception as e:
            print(f"✓ {expr} -> Blocked: {type(e).__name__}: {e}")
    
    print()


def sandbox_configuration():
    """Sandbox configuration examples."""
    print("=== Sandbox Configuration ===")
    
    # 默认沙箱配置
    sandbox = Sandbox()
    print("Default sandbox created")
    
    # 严格模式
    strict_config = SandboxConfig(
        strict_private_access=True,
        max_execution_time=2.0,
        max_recursion_depth=50,
        max_string_length=10000,
        max_collection_size=1000,
    )
    strict_sandbox = Sandbox(strict_config)
    print("Strict sandbox created")
    
    # 测试表达式
    test_exprs = [
        "2 + 3",
        "abs(-5)",
        "'hello'.upper()",
    ]
    
    for expr in test_exprs:
        result = sandbox.check_expression(expr)
        if result:
            print(f"'{expr}' is safe")
        else:
            print(f"'{expr}' is unsafe")
    
    # 测试不安全的表达式
    unsafe_expr = "eval('1+1')"
    result = sandbox.check_expression(unsafe_expr)
    if result:
        print(f"'{unsafe_expr}' issues: {result}")
    
    print()


def expression_validation():
    """Expression validation examples."""
    print("=== Expression Validation ===")
    
    # 使用便捷函数验证
    safe_exprs = ["2 + 3", "x + y", "abs(-5)"]
    unsafe_exprs = ["eval('1+1')", "exec('pass')"]
    
    print("Validating safe expressions:")
    for expr in safe_exprs:
        try:
            validate_expression_safety(expr)
            print(f"✓ {expr} is safe")
        except SecurityViolationError as e:
            print(f"✗ {expr} is unsafe: {e}")
    
    print("\nValidating unsafe expressions:")
    for expr in unsafe_exprs:
        try:
            validate_expression_safety(expr)
            print(f"⚠ {expr} should have been blocked!")
        except SecurityViolationError as e:
            print(f"✓ {expr} correctly blocked: {e}")
    
    print()


def safety_issues():
    """Get detailed safety issues."""
    print("=== Safety Issues Analysis ===")
    
    # 获取详细的安全问题
    expressions = [
        "eval('1+1')",
        "__import__('os')",
        "getattr(object, '__class__')",
        "open('/etc/passwd')",
    ]
    
    for expr in expressions:
        issues = get_expression_safety_issues(expr)
        print(f"Expression: {expr}")
        if issues:
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("  - No issues found")
        print()


def is_safe_function():
    """Using is_expression_safe function."""
    print("=== is_expression_safe Function ===")
    
    test_cases = [
        ("2 + 3", True),
        ("abs(-5)", True),
        ("'hello'.upper()", True),
        ("eval('1+1')", False),
        ("exec('print()')", False),
        ("open('file.txt')", False),
        ("__import__('os')", False),
    ]
    
    for expr, expected in test_cases:
        result = is_expression_safe(expr)
        status = "✓" if result == expected else "✗"
        print(f"{status} {expr} -> {result} (expected {expected})")
    
    print()


def private_attribute_access():
    """Private attribute access examples."""
    print("=== Private Attribute Access ===")
    
    # 默认配置（允许私有属性访问）
    engine_default = ExpressionEngine()
    
    # 严格配置（阻止私有属性访问）
    strict_config = SandboxConfig(strict_private_access=True)
    engine_strict = ExpressionEngine(
        sandbox_config=strict_config
    )
    
    # 测试私有属性访问
    test_cases = [
        "'hello'._private_attr",
        "obj.__class__",
        "obj.__init__",
    ]
    
    print("Default engine:")
    for expr in test_cases:
        try:
            result = engine_default.evaluate(expr, {"obj": object()})
            print(f"  {expr} -> {result}")
        except Exception as e:
            print(f"  {expr} -> {type(e).__name__}: {e}")
    
    print("\nStrict engine:")
    for expr in test_cases:
        try:
            result = engine_strict.evaluate(expr, {"obj": object()})
            print(f"  {expr} -> {result}")
        except Exception as e:
            print(f"  {expr} -> {type(e).__name__}: {e}")
    
    print()


def recursion_limit():
    """Recursion limit examples."""
    print("=== Recursion Limit ===")
    
    # 创建低递归限制的引擎
    config = SandboxConfig(max_recursion_depth=10)
    engine = ExpressionEngine(sandbox_config=config)
    
    # 测试递归
    expr = "f(f(f(f(f(f(f(f(f(f(1))))))))))"
    
    try:
        result = engine.evaluate(expr, {"f": lambda x: x + 1})
        print(f"Deep recursion result: {result}")
    except RecursionError as e:
        print(f"Recursion limit exceeded: {e}")
    
    print()


def string_length_limit():
    """String length limit examples."""
    print("=== String Length Limit ===")
    
    # 创建限制字符串长度的沙箱
    config = SandboxConfig(max_string_length=100)
    sandbox = Sandbox(config)
    
    # 测试短字符串（应该通过）
    short_expr = "'a' * 50"
    issues = sandbox.check_expression(short_expr)
    print(f"'a' * 50: {'Safe' if not issues else 'Unsafe: ' + str(issues)}")
    
    # 测试长字符串（应该被阻止）
    long_expr = "'a' * 200"
    issues = sandbox.check_expression(long_expr)
    print(f"'a' * 200: {'Safe' if not issues else 'Unsafe: ' + str(issues)}")
    
    print()


def collection_size_limit():
    """Collection size limit examples."""
    print("=== Collection Size Limit ===")
    
    # 创建限制集合大小的沙箱
    config = SandboxConfig(max_collection_size=10)
    sandbox = Sandbox(config)
    
    # 测试小集合（应该通过）
    small_expr = "list(range(5))"
    issues = sandbox.check_expression(small_expr)
    print(f"list(range(5)): {'Safe' if not issues else 'Unsafe: ' + str(issues)}")
    
    # 测试大集合（应该被阻止）
    large_expr = "list(range(20))"
    issues = sandbox.check_expression(large_expr)
    print(f"list(range(20)): {'Safe' if not issues else 'Unsafe: ' + str(issues)}")
    
    print()


def template_security():
    """Template security examples."""
    print("=== Template Security ===")
    
    engine = TemplateEngine()
    
    # 安全的模板
    safe_templates = [
        "Hello, {{ name }}!",
        "Total: {{ price * quantity }}",
        "{% if user.age >= 18 %}Adult{% else %}Minor{% endif %}",
    ]
    
    print("Safe templates:")
    for template in safe_templates:
        try:
            result = engine.render(template, {"name": "Alice", "price": 100, "quantity": 2, "user": {"age": 25}})
            print(f"  ✓ {template} -> {result}")
        except Exception as e:
            print(f"  ✗ {template} -> {e}")
    
    # 注意：模板引擎本身应该已经处理了安全问题
    print()


def best_practices():
    """Security best practices."""
    print("=== Security Best Practices ===")
    
    print("1. Always use the sandbox:")
    print("   engine = ExpressionEngine(enable_sandbox=True)")
    
    print("\n2. Validate user input:")
    print("   if not is_expression_safe(user_expression):")
    print("       raise ValueError('Unsafe expression')")
    
    print("\n3. Set appropriate limits:")
    print("   config = SandboxConfig(")
    print("       max_execution_time=5.0,")
    print("       max_recursion_depth=50,")
    print("       max_string_length=10000,")
    print("       max_collection_size=1000,")
    print("   )")
    
    print("\n4. Use strict mode for sensitive applications:")
    print("   config = SandboxConfig(strict_private_access=True)")
    
    print("\n5. Regular security audits:")
    print("   issues = get_expression_safety_issues(expression)")
    print("   if issues:")
    print("       log_warning(f'Potential security issues: {issues}')")
    
    print("\n6. Whitelist allowed functions:")
    print("   config = SandboxConfig(")
    print("       allowed_functions={'abs', 'round', 'len', 'sum'}")
    print("   )")
    
    print()


def main():
    """Run all security examples."""
    safe_expressions()
    unsafe_expressions()
    sandbox_configuration()
    expression_validation()
    safety_issues()
    is_safe_function()
    private_attribute_access()
    recursion_limit()
    string_length_limit()
    collection_size_limit()
    template_security()
    best_practices()


if __name__ == "__main__":
    main()
