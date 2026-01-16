"""
Basic usage examples for qdata-expression.
"""

from qdata_expr import (
    ExpressionEngine,
    TemplateEngine,
    ContextResolver,
    evaluate,
    render_template,
    validate,
)


def basic_expression_evaluation():
    """Basic expression evaluation examples."""
    print("=== Basic Expression Evaluation ===")
    
    # 创建引擎
    engine = ExpressionEngine()
    
    # 基本算术
    print("2 + 3 * 4 =", engine.evaluate("2 + 3 * 4"))
    print("(2 + 3) * 4 =", engine.evaluate("(2 + 3) * 4"))
    print("10 / 3 =", engine.evaluate("10 / 3"))
    print("10 // 3 =", engine.evaluate("10 // 3"))
    print("2 ** 10 =", engine.evaluate("2 ** 10"))
    
    # 比较运算
    print("\n5 > 3 =", engine.evaluate("5 > 3"))
    print("10 >= 10 =", engine.evaluate("10 >= 10"))
    print("'apple' < 'banana' =", engine.evaluate("'apple' < 'banana'"))
    
    # 逻辑运算
    print("\nTrue and False =", engine.evaluate("True and False"))
    print("True or False =", engine.evaluate("True or False"))
    print("not True =", engine.evaluate("not True"))
    
    # 内置函数
    print("\nabs(-5) =", engine.evaluate("abs(-5)"))
    print("round(3.14159, 2) =", engine.evaluate("round(3.14159, 2)"))
    print("max(1, 2, 3, 4, 5) =", engine.evaluate("max(1, 2, 3, 4, 5)"))
    print("sum([1, 2, 3, 4, 5]) =", engine.evaluate("sum([1, 2, 3, 4, 5])"))
    
    print()


def context_variables():
    """Using context variables in expressions."""
    print("=== Context Variables ===")
    
    engine = ExpressionEngine()
    
    # 简单变量
    context = {"x": 10, "y": 20, "name": "Alice"}
    result = engine.evaluate("x + y", context)
    print("x + y =", result)
    
    # 嵌套变量
    context = {
        "user": {
            "name": "Alice",
            "age": 30,
            "email": "alice@example.com"
        },
        "order": {
            "items": [
                {"name": "Laptop", "price": 999.99},
                {"name": "Mouse", "price": 29.99}
            ],
            "total": 1029.98
        }
    }
    
    result = engine.evaluate("user.name", context)
    print("user.name =", result)
    
    result = engine.evaluate("order.total", context)
    print("order.total =", result)
    
    result = engine.evaluate("order.items[0].name", context)
    print("order.items[0].name =", result)
    
    # 复杂表达式
    result = engine.evaluate(
        "'VIP' if order.total > 1000 else 'Regular'",
        context
    )
    print("Customer type:", result)
    
    print()


def built_in_functions():
    """Using built-in functions."""
    print("=== Built-in Functions ===")
    
    engine = ExpressionEngine()
    
    # 数学函数
    print("pow(2, 8) =", engine.evaluate("pow(2, 8)"))
    print("sqrt(144) =", engine.evaluate("sqrt(144)"))
    print("floor(3.7) =", engine.evaluate("floor(3.7)"))
    print("ceil(3.2) =", engine.evaluate("ceil(3.2)"))
    print("avg(10, 20, 30) =", engine.evaluate("avg(10, 20, 30)"))
    
    # 字符串函数
    print("\nupper('hello') =", engine.evaluate("upper('hello')"))
    print("trim('  world  ') =", engine.evaluate("trim('  world  ')"))
    print("concat('Hello', ' ', 'World') =", engine.evaluate("concat('Hello', ' ', 'World')"))
    print("replace('hello world', 'world', 'Python') =", 
          engine.evaluate("replace('hello world', 'world', 'Python')"))
    
    # 逻辑函数
    print("\nif_else(5 > 3, 'yes', 'no') =", engine.evaluate("if_else(5 > 3, 'yes', 'no')"))
    print("is_null(None) =", engine.evaluate("is_null(None)"))
    print("is_empty('') =", engine.evaluate("is_empty('')"))
    print("coalesce(None, '', 'value') =", engine.evaluate("coalesce(None, '', 'value')"))
    
    # 列表函数
    print("\nlength([1, 2, 3]) =", engine.evaluate("length([1, 2, 3])"))
    print("first([1, 2, 3]) =", engine.evaluate("first([1, 2, 3])"))
    print("last([1, 2, 3]) =", engine.evaluate("last([1, 2, 3])"))
    print("sort([3, 1, 2]) =", engine.evaluate("sort([3, 1, 2])"))
    
    print()


def conditional_expressions():
    """Conditional expressions examples."""
    print("=== Conditional Expressions ===")
    
    engine = ExpressionEngine()
    
    # if-else 表达式
    context = {"age": 25}
    result = engine.evaluate("'adult' if age >= 18 else 'minor'", context)
    print("Age 25:", result)
    
    context = {"age": 15}
    result = engine.evaluate("'adult' if age >= 18 else 'minor'", context)
    print("Age 15:", result)
    
    # 嵌套条件
    context = {"score": 85}
    template = """
    'A' if score >= 90 else
    'B' if score >= 80 else
    'C' if score >= 70 else
    'F'
    """
    result = engine.evaluate(template.strip(), context)
    print("Score 85 grade:", result)
    
    # 使用内置条件函数
    result = engine.evaluate('if_else(score >= 60, "pass", "fail")', {"score": 75})
    print("Score 75 result:", result)
    
    print()


def list_and_dict_operations():
    """List and dictionary operations."""
    print("=== List and Dictionary Operations ===")
    
    engine = ExpressionEngine()
    
    # 列表操作
    result = engine.evaluate("[1, 2, 3] + [4, 5]")
    print("[1, 2, 3] + [4, 5] =", result)
    
    result = engine.evaluate("len([1, 2, 3, 4, 5])")
    print("len([1, 2, 3, 4, 5]) =", result)
    
    result = engine.evaluate("sum([1, 2, 3, 4, 5])")
    print("sum([1, 2, 3, 4, 5]) =", result)
    
    result = engine.evaluate("[x**2 for x in range(5)]")
    print("[x**2 for x in range(5)] =", result)
    
    result = engine.evaluate("[x for x in range(10) if x % 2 == 0]")
    print("Even numbers 0-9:", result)
    
    # 字典操作
    result = engine.evaluate("{'a': 1, 'b': 2, 'c': 3}['b']")
    print("{'a': 1, 'b': 2, 'c': 3}['b'] =", result)
    
    result = engine.evaluate("len({'a': 1, 'b': 2, 'c': 3})")
    print("len({'a': 1, 'b': 2, 'c': 3}) =", result)
    
    print()


def convenience_functions():
    """Convenience functions usage."""
    print("=== Convenience Functions ===")
    
    # evaluate 函数
    result = evaluate("2 + 3 * 4")
    print("evaluate('2 + 3 * 4') =", result)
    
    result = evaluate("x + y", {"x": 10, "y": 20})
    print("evaluate('x + y', context) =", result)
    
    # validate 函数
    print("\nvalidate('2 + 3'):", validate("2 + 3"))
    print("validate('2 +'):", validate("2 +"))
    
    print()


def main():
    """Run all examples."""
    basic_expression_evaluation()
    context_variables()
    built_in_functions()
    conditional_expressions()
    list_and_dict_operations()
    convenience_functions()


if __name__ == "__main__":
    main()
