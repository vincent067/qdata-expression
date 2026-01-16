"""
Template engine usage examples for qdata-expression.
"""

from qdata_expr import TemplateEngine, render_template


def basic_template_rendering():
    """Basic template rendering examples."""
    print("=== Basic Template Rendering ===")
    
    engine = TemplateEngine()
    
    # 简单变量替换
    template = "Hello, {{ name }}!"
    context = {"name": "World"}
    result = engine.render(template, context)
    print(f"'{template}' -> '{result}'")
    
    # 多个变量
    template = "User: {{ user.name }}, Age: {{ user.age }}"
    context = {"user": {"name": "Alice", "age": 30}}
    result = engine.render(template, context)
    print(f"'{template}' -> '{result}'")
    
    # 嵌套访问
    template = "First address: {{ user.addresses[0].city }}"
    context = {
        "user": {
            "addresses": [
                {"city": "Beijing", "zip": "100000"},
                {"city": "Shanghai", "zip": "200000"}
            ]
        }
    }
    result = engine.render(template, context)
    print(f"'{template}' -> '{result}'")
    
    print()


def conditional_templates():
    """Conditional template examples."""
    print("=== Conditional Templates ===")
    
    engine = TemplateEngine()
    
    # 简单条件
    template = """
{% if age >= 18 %}
Welcome, {{ name }}! You are an adult.
{% else %}
Sorry, {{ name }}. You must be 18 or older.
{% endif %}
"""
    
    context = {"name": "Alice", "age": 25}
    result = engine.render(template, context)
    print("Age 25:")
    print(result)
    
    context = {"name": "Bob", "age": 15}
    result = engine.render(template, context)
    print("\nAge 15:")
    print(result)
    
    # else-if 条件
    template = """
{% if score >= 90 %}
Grade: A (Excellent)
{% elif score >= 80 %}
Grade: B (Good)
{% elif score >= 70 %}
Grade: C (Average)
{% elif score >= 60 %}
Grade: D (Pass)
{% else %}
Grade: F (Fail)
{% endif %}
"""
    
    for score in [95, 85, 75, 65, 55]:
        context = {"score": score}
        result = engine.render(template, context)
        print(f"\nScore {score}:")
        print(result.strip())
    
    print()


def loop_templates():
    """Loop template examples."""
    print("=== Loop Templates ===")
    
    engine = TemplateEngine()
    
    # 简单循环
    template = """
Items:
{% for item in items %}
- {{ item }}
{% endfor %}
"""
    
    context = {"items": ["Apple", "Banana", "Cherry"]}
    result = engine.render(template, context)
    print(result)
    
    # 带索引的循环
    template = """
Shopping List:
{% for item in items %}
{{ loop.index }}. {{ item }}
{% endfor %}
"""
    
    result = engine.render(template, context)
    print(result)
    
    # 对象列表
    template = """
Product List:
{% for product in products %}
{{ loop.index }}. {{ product.name }} - ${{ product.price }}
{% endfor %}
"""
    
    context = {
        "products": [
            {"name": "Laptop", "price": 999.99},
            {"name": "Mouse", "price": 29.99},
            {"name": "Keyboard", "price": 79.99}
        ]
    }
    result = engine.render(template, context)
    print(result)
    
    print()


def filters():
    """Filter examples."""
    print("=== Filters ===")
    
    engine = TemplateEngine()
    
    # 大小写转换
    template = "{{ name | upper }}"
    result = engine.render(template, {"name": "john doe"})
    print(f"upper: {result}")
    
    template = "{{ name | lower }}"
    result = engine.render(template, {"name": "JOHN DOE"})
    print(f"lower: {result}")
    
    # 空白处理
    template = "{{ name | trim }}"
    result = engine.render(template, {"name": "  alice  "})
    print(f"trim: '{result}'")
    
    # 默认值
    template = "Hello, {{ name | default('Guest') }}!"
    result = engine.render(template, {"name": ""})
    print(f"default (empty): {result}")
    
    result = engine.render(template, {})
    print(f"default (missing): {result}")
    
    # 长度
    template = "Items count: {{ items | length }}"
    result = engine.render(template, {"items": ["a", "b", "c"]})
    print(f"length: {result}")
    
    # 连接
    template = "{{ items | join(', ') }}"
    result = engine.render(template, {"items": ["apple", "banana", "cherry"]})
    print(f"join: {result}")
    
    # 数字格式化
    template = "Price: ${{ price | round(2) }}"
    result = engine.render(template, {"price": 29.999})
    print(f"round: {result}")
    
    print()


def filter_chaining():
    """Filter chaining examples."""
    print("=== Filter Chaining ===")
    
    engine = TemplateEngine()
    
    # 多个过滤器
    template = "{{ name | trim | upper }}"
    result = engine.render(template, {"name": "  john doe  "})
    print(f"trim + upper: {result}")
    
    # 带条件的过滤
    template = "{{ name | default('Unknown') | upper }}"
    result = engine.render(template, {})
    print(f"default + upper (missing): {result}")
    
    # 列表过滤
    template = "{{ items | length | string }} items"
    result = engine.render(template, {"items": ["a", "b", "c", "d"]})
    print(f"length + string: {result}")
    
    print()


def custom_filters():
    """Custom filter examples."""
    print("=== Custom Filters ===")
    
    engine = TemplateEngine()
    
    # 注册自定义过滤器
    def reverse_filter(value):
        """Reverse a string."""
        return value[::-1]
    
    engine.register_filter("reverse", reverse_filter)
    
    template = "{{ 'hello' | reverse }}"
    result = engine.render(template)
    print(f"reverse: {result}")
    
    # 带参数的过滤器
    def truncate_filter(value, length=10, suffix="..."):
        """Truncate string to specified length."""
        if len(value) <= length:
            return value
        return value[:length - len(suffix)] + suffix
    
    engine.register_filter("truncate", truncate_filter)
    
    template = "{{ 'This is a very long string' | truncate(10) }}"
    result = engine.render(template)
    print(f"truncate(10): {result}")
    
    template = "{{ 'This is a very long string' | truncate(15, '---') }}"
    result = engine.render(template)
    print(f"truncate(15, '---'): {result}")
    
    print()


def nested_loops():
    """Nested loop examples."""
    print("=== Nested Loops ===")
    
    engine = TemplateEngine()
    
    # 嵌套循环
    template = """
Categories:
{% for category in categories %}
{{ category.name }}:
{% for item in category.items %}
    - {{ item }}
{% endfor %}
{% endfor %}
"""
    
    context = {
        "categories": [
            {
                "name": "Fruits",
                "items": ["Apple", "Banana", "Orange"]
            },
            {
                "name": "Vegetables",
                "items": ["Carrot", "Potato", "Tomato"]
            }
        ]
    }
    
    result = engine.render(template, context)
    print(result)
    
    print()


def arithmetic_in_templates():
    """Arithmetic operations in templates."""
    print("=== Arithmetic in Templates ===")
    
    engine = TemplateEngine()
    
    # 基本算术
    template = "Total: {{ price * quantity }}"
    context = {"price": 100, "quantity": 3}
    result = engine.render(template, context)
    print(f"price * quantity: {result}")
    
    # 带过滤的算术
    template = "Total with tax: ${{ (price * quantity * 1.1) | round(2) }}"
    context = {"price": 99.99, "quantity": 2}
    result = engine.render(template, context)
    print(f"price * quantity * 1.1: {result}")
    
    # 条件算术
    template = """
{% if quantity >= 10 %}
    Total: ${{ (price * quantity * 0.9) | round(2) }} (10% discount)
{% else %}
    Total: ${{ (price * quantity) | round(2) }}
{% endif %}
"""
    
    context = {"price": 50, "quantity": 12}
    result = engine.render(template, context)
    print("\nLarge order (quantity >= 10):")
    print(result)
    
    context = {"price": 50, "quantity": 5}
    result = engine.render(template, context)
    print("\nSmall order (quantity < 10):")
    print(result)
    
    print()


def template_validation():
    """Template validation examples."""
    print("=== Template Validation ===")
    
    engine = TemplateEngine()
    
    # 验证有效模板
    template = "Hello, {{ name }}!"
    errors = engine.validate(template)
    print(f"Valid template errors: {errors}")
    
    # 获取模板变量
    variables = engine.get_variables(template)
    print(f"Variables in template: {variables}")
    
    # 复杂模板
    template = """
{% for user in users %}
    {{ user.name }}: {{ user.email }}
{% endfor %}
"""
    variables = engine.get_variables(template)
    print(f"Variables in complex template: {variables}")
    
    print()


def convenience_function():
    """Convenience function examples."""
    print("=== Convenience Function ===")
    
    # render_template 函数
    result = render_template("Hello, {{ name }}!", {"name": "World"})
    print(f"render_template: {result}")
    
    result = render_template(
        "Items: {{ items | length }}",
        {"items": ["a", "b", "c"]}
    )
    print(f"render_template with filter: {result}")
    
    print()


def main():
    """Run all template examples."""
    basic_template_rendering()
    conditional_templates()
    loop_templates()
    filters()
    filter_chaining()
    custom_filters()
    nested_loops()
    arithmetic_in_templates()
    template_validation()
    convenience_function()


if __name__ == "__main__":
    main()
