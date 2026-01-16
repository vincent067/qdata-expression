"""
Pytest configuration and fixtures for qdata-expression tests.
"""

import pytest
from typing import Any, Dict

from qdata_expr import (
    ContextResolver,
    ExpressionEngine,
    Sandbox,
    SandboxConfig,
    TemplateEngine,
)


# ============================================================
# Core Fixtures
# ============================================================


@pytest.fixture
def expression_engine() -> ExpressionEngine:
    """Create a default expression engine for testing."""
    return ExpressionEngine()


@pytest.fixture
def template_engine() -> TemplateEngine:
    """Create a default template engine for testing."""
    return TemplateEngine()


@pytest.fixture
def context_resolver() -> ContextResolver:
    """Create a default context resolver for testing."""
    return ContextResolver()


@pytest.fixture
def sandbox() -> Sandbox:
    """Create a default sandbox for testing."""
    return Sandbox()


@pytest.fixture
def strict_sandbox() -> Sandbox:
    """Create a strict sandbox for testing."""
    config = SandboxConfig(
        strict_private_access=True,
        max_execution_time=2.0,
        max_recursion_depth=50,
    )
    return Sandbox(config)


# ============================================================
# Sample Data Fixtures
# ============================================================


@pytest.fixture
def sample_context() -> Dict[str, Any]:
    """Provide a sample context for testing."""
    return {
        "user": {
            "name": "Alice",
            "age": 30,
            "email": "alice@example.com",
            "addresses": [
                {"city": "Beijing", "zip": "100000"},
                {"city": "Shanghai", "zip": "200000"},
            ],
        },
        "order": {
            "id": 12345,
            "items": [
                {"name": "Laptop", "price": 999.99, "quantity": 1},
                {"name": "Mouse", "price": 29.99, "quantity": 2},
            ],
            "total": 1059.97,
            "status": "pending",
        },
        "config": {
            "tax_rate": 0.1,
            "discount": 0.05,
            "shipping": 15.0,
        },
        "numbers": [1, 2, 3, 4, 5],
        "words": ["apple", "banana", "cherry"],
        "nested": {
            "level1": {
                "level2": {
                    "level3": "deep_value"
                }
            }
        },
    }


@pytest.fixture
def math_context() -> Dict[str, Any]:
    """Provide a context for math operations."""
    return {
        "a": 10,
        "b": 20,
        "c": 3.14,
        "d": -5,
        "prices": [10.5, 20.0, 15.75, 8.99],
        "quantities": [2, 5, 1, 3],
    }


@pytest.fixture
def string_context() -> Dict[str, Any]:
    """Provide a context for string operations."""
    return {
        "name": "  John Doe  ",
        "email": "john.doe@example.com",
        "text": "Hello, World!",
        "sentence": "The quick brown fox jumps over the lazy dog",
        "mixed": "AbCdEf123",
        "empty": "",
        "whitespace": "   \n\t  ",
    }


@pytest.fixture
def date_context() -> Dict[str, Any]:
    """Provide a context for date operations."""
    from datetime import datetime, date
    return {
        "now": datetime(2024, 1, 15, 14, 30, 45),
        "today": date(2024, 1, 15),
        "birthday": "1990-05-20",
        "event": "2024-12-25 18:00:00",
        "start_date": datetime(2024, 1, 1),
        "end_date": datetime(2024, 1, 31),
    }


@pytest.fixture
def list_context() -> Dict[str, Any]:
    """Provide a context for list operations."""
    return {
        "numbers": [5, 2, 8, 1, 9, 3],
        "strings": ["zebra", "apple", "banana", "cherry"],
        "mixed": [1, "two", 3.0, True, None],
        "nested": [[1, 2], [3, 4], [5, 6]],
        "objects": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ],
        "empty": [],
    }


# ============================================================
# Expression Fixtures
# ============================================================


@pytest.fixture
def simple_expressions() -> Dict[str, str]:
    """Provide simple expressions for testing."""
    return {
        "arithmetic": "2 + 3 * 4",
        "variable": "price * quantity",
        "function": "abs(-5) + round(3.14, 1)",
        "comparison": "age > 18 and age < 65",
        "logical": "not (x == 0 and y == 0)",
        "conditional": "'adult' if age >= 18 else 'minor'",
        "string": "upper(name) + ' - ' + str(age)",
    }


@pytest.fixture
def complex_expressions() -> Dict[str, str]:
    """Provide complex expressions for testing."""
    return {
        "nested": "sum([x**2 for x in range(5) if x % 2 == 0])",
        "multi_function": "round(sum(prices) * (1 - discount), 2)",
        "path": "user.addresses[0].city",
        "conditional_chain": """
            if total > 1000:
                'VIP'
            elif total > 500:
                'Gold'
            else:
                'Regular'
        """,
        "list_comp": "[item['price'] for item in order['items'] if item['price'] > 50]",
    }


# ============================================================
# Template Fixtures
# ============================================================


@pytest.fixture
def simple_templates() -> Dict[str, str]:
    """Provide simple templates for testing."""
    return {
        "basic": "Hello, {{ name }}!",
        "variable": "Order #{{ order.id }} - ${{ order.total }}",
        "filter": "Name: {{ name | upper }}",
        "default": "Hello, {{ name | default('Guest') }}!",
        "length": "Items: {{ items | length }}",
    }


@pytest.fixture
def complex_templates() -> Dict[str, str]:
    """Provide complex templates for testing."""
    return {
        "condition": """
{% if order.total > 1000 %}
VIP Customer
{% elif order.total > 500 %}
Gold Customer
{% else %}
Regular Customer
{% endif %}
""",
        "loop": """
Items:
{% for item in order.items %}
- {{ item.name }}: ${{ item.price }} x {{ item.quantity }}
{% endfor %}
Total: ${{ order.total }}
""",
        "nested": """
User: {{ user.name }}
Addresses:
{% for addr in user.addresses %}
  {{ loop.index }}. {{ addr.city }} ({{ addr.zip }})
{% endfor %}
""",
        "filters": """
{{ name | upper | trim }}
{{ items | join(', ') }}
{{ price | round(2) }}
""",
    }


# ============================================================
# Security Fixtures
# ============================================================


@pytest.fixture
def dangerous_expressions() -> Dict[str, str]:
    """Provide dangerous expressions for security testing."""
    return {
        "eval": "eval('__import__(\"os\").system(\"echo hacked\")')",
        "exec": "exec('import os; os.system(\"echo hacked\")')",
        "import": "__import__('os').system('echo hacked')",
        "open": "open('/etc/passwd').read()",
        "globals": "globals()['__builtins__']['eval']('1+1')",
        "getattr": "getattr(object, '__class__')",
        "file": "file('/etc/passwd')",
        "compile": "compile('print(\"hacked\")', '', 'exec')",
    }


@pytest.fixture
def safe_expressions() -> Dict[str, str]:
    """Provide safe expressions for testing."""
    return {
        "math": "2 + 3 * 4",
        "function": "abs(-5) + round(3.14, 1)",
        "variable": "price * quantity",
        "comparison": "a > b",
        "logical": "x and y or z",
        "string": "'hello' + ' ' + 'world'",
    }


# ============================================================
# Performance Fixtures
# ============================================================


@pytest.fixture
def large_context() -> Dict[str, Any]:
    """Provide a large context for performance testing."""
    return {
        "data": list(range(1000)),
        "nested": {
            f"level{i}": {
                f"key{j}": f"value{i}_{j}"
                for j in range(100)
            }
            for i in range(10)
        },
        "items": [
            {
                "id": i,
                "name": f"Item {i}",
                "price": i * 1.5,
                "tags": [f"tag{j}" for j in range(5)]
            }
            for i in range(100)
        ],
    }


# ============================================================
# Helper Functions
# ============================================================


def assert_expression_result(
    engine: ExpressionEngine,
    expression: str,
    context: Dict[str, Any],
    expected: Any,
) -> None:
    """Helper to assert expression results."""
    result = engine.evaluate(expression, context)
    assert result == expected, f"Expected {expected}, got {result}"


def assert_template_result(
    engine: TemplateEngine,
    template: str,
    context: Dict[str, Any],
    expected: str,
) -> None:
    """Helper to assert template results."""
    result = engine.render(template, context)
    assert result.strip() == expected.strip(), f"Expected {expected!r}, got {result!r}"


def assert_safe(engine: ExpressionEngine, expression: str) -> bool:
    """Helper to check if expression is safe."""
    errors = engine.validate(expression)
    return len(errors) == 0


def assert_unsafe(engine: ExpressionEngine, expression: str) -> bool:
    """Helper to check if expression is unsafe."""
    errors = engine.validate(expression)
    return len(errors) > 0
