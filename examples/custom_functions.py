"""
Custom function examples for qdata-expression.
"""

from qdata_expr import ExpressionEngine, builtin_function
from qdata_expr.functions import FunctionCategory, FunctionRegistry


def basic_custom_functions():
    """Basic custom function examples."""
    print("=== Basic Custom Functions ===")
    
    engine = ExpressionEngine()
    
    # 方法1：直接注册
    def double(x):
        """Double a number."""
        return x * 2
    
    engine.register_function("double", double)
    
    result = engine.evaluate("double(5)")
    print(f"double(5) = {result}")
    
    # 带默认参数的函数
    def calculate_tax(amount, rate=0.1):
        """Calculate tax with default rate."""
        return amount * rate
    
    engine.register_function("tax", calculate_tax)
    
    result = engine.evaluate("tax(1000)")
    print(f"tax(1000) = {result}")
    
    result = engine.evaluate("tax(1000, 0.08)")
    print(f"tax(1000, 0.08) = {result}")
    
    # 多参数函数
    def calculate_total(price, quantity, tax_rate=0.0, discount=0.0):
        """Calculate total price with tax and discount."""
        subtotal = price * quantity
        tax = subtotal * tax_rate
        discount_amount = subtotal * discount
        return subtotal + tax - discount_amount
    
    engine.register_function("total", calculate_total)
    
    context = {"price": 100, "quantity": 5}
    result = engine.evaluate("total(price, quantity, 0.1, 0.05)", context)
    print(f"total(100, 5, 0.1, 0.05) = {result}")
    
    print()


def decorator_functions():
    """Using decorator to register functions."""
    print("=== Decorator Functions ===")
    
    # 使用装饰器注册
    @builtin_function(
        name="greet",
        category=FunctionCategory.CUSTOM,
        description="Generate greeting message",
        signature="greet(name, greeting='Hello') -> str",
        examples=[
            "greet('Alice') = 'Hello, Alice!'",
            "greet('Bob', 'Hi') = 'Hi, Bob!'"
        ]
    )
    def greet(name, greeting="Hello"):
        """Generate greeting message."""
        return f"{greeting}, {name}!"
    
    # 使用函数
    engine = ExpressionEngine()
    result = engine.evaluate("greet('Alice')")
    print(f"greet('Alice') = {result}")
    
    result = engine.evaluate('greet("Bob", "Hi")')
    print(f'greet("Bob", "Hi") = {result}')
    
    # 带类型检查的装饰器
    @builtin_function(
        name="safe_divide",
        category=FunctionCategory.MATH,
        description="Safe division with zero check",
        signature="safe_divide(a, b) -> float",
        examples=["safe_divide(10, 2) = 5.0"]
    )
    def safe_divide(a, b):
        """Safe division with zero check."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    result = engine.evaluate("safe_divide(10, 2)")
    print(f"safe_divide(10, 2) = {result}")
    
    try:
        result = engine.evaluate("safe_divide(10, 0)")
    except ValueError as e:
        print(f"safe_divide(10, 0) error: {e}")
    
    print()


def function_categories():
    """Function category examples."""
    print("=== Function Categories ===")
    
    # 注册不同类别的函数
    @builtin_function(
        name="business_tax",
        category=FunctionCategory.BUSINESS,
        description="Calculate business tax"
    )
    def business_tax(revenue, tax_rate=0.25):
        return revenue * tax_rate
    
    @builtin_function(
        name="format_currency",
        category=FunctionCategory.FORMATTING,
        description="Format number as currency"
    )
    def format_currency(amount, currency="USD"):
        symbols = {"USD": "$", "EUR": "€", "CNY": "¥"}
        symbol = symbols.get(currency, currency)
        return f"{symbol}{amount:,.2f}"
    
    @builtin_function(
        name="hash_string",
        category=FunctionCategory.SECURITY,
        description="Generate hash of string"
    )
    def hash_string(text, algorithm="md5"):
        import hashlib
        if algorithm == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(text.encode()).hexdigest()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    engine = ExpressionEngine()
    
    result = engine.evaluate("business_tax(100000)")
    print(f"business_tax(100000) = {result}")
    
    result = engine.evaluate('format_currency(1234.56, "EUR")')
    print(f'format_currency(1234.56, "EUR") = {result}')
    
    result = engine.evaluate('hash_string("hello", "sha256")')
    print(f'hash_string("hello", "sha256") = {result[:16]}...')
    
    print()


def function_registry():
    """Function registry examples."""
    print("=== Function Registry ===")
    
    # 创建独立注册表
    registry = FunctionRegistry()
    
    # 注册函数
    def custom_func(x):
        return x * 3
    
    registry.register("triple", custom_func, FunctionCategory.CUSTOM)
    
    # 检查函数
    print(f"Has 'triple': {registry.has('triple')}")
    print(f"All functions: {registry.list_all()}")
    
    # 获取可调用
    func = registry.get_callable("triple")
    print(f"triple(4) = {func(4)}")
    
    # 使用注册表创建引擎
    engine = ExpressionEngine(function_registry=registry)
    result = engine.evaluate("triple(5)")
    print(f"Engine triple(5) = {result}")
    
    # 函数别名
    registry.register(
        "original",
        lambda x: x * 2,
        FunctionCategory.CUSTOM,
        aliases=["double", "multiply_by_2"]
    )
    
    print(f"Has 'double': {registry.has('double')}")
    print(f"Has 'multiply_by_2': {registry.has('multiply_by_2')}")
    
    # 获取所有可调用函数
    callables = registry.get_all_callables()
    print(f"Registered functions: {list(callables.keys())}")
    
    print()


def advanced_functions():
    """Advanced function examples."""
    print("=== Advanced Functions ===")
    
    engine = ExpressionEngine()
    
    # 函数返回复杂类型
    @builtin_function(
        name="create_user",
        category=FunctionCategory.CUSTOM,
        description="Create user object"
    )
    def create_user(name, age, email=None):
        user = {"name": name, "age": age}
        if email:
            user["email"] = email
        return user
    
    result = engine.evaluate('create_user("Alice", 30, "alice@example.com")')
    print(f"create_user result: {result}")
    
    # 函数使用上下文
    @builtin_function(
        name="apply_tax",
        category=FunctionCategory.BUSINESS,
        description="Apply tax based on region"
    )
    def apply_tax(amount, region="US"):
        tax_rates = {
            "US": 0.08,
            "EU": 0.20,
            "CN": 0.13
        }
        rate = tax_rates.get(region, 0)
        return amount * (1 + rate)
    
    result = engine.evaluate('apply_tax(100, "EU")')
    print(f"apply_tax(100, 'EU') = {result}")
    
    # 可变参数函数
    @builtin_function(
        name="weighted_avg",
        category=FunctionCategory.MATH,
        description="Calculate weighted average"
    )
    def weighted_avg(*args):
        """Calculate weighted average: args = [value1, weight1, value2, weight2, ...]"""
        if len(args) % 2 != 0:
            raise ValueError("Must provide pairs of (value, weight)")
        
        total = 0
        weight_sum = 0
        for i in range(0, len(args), 2):
            value = args[i]
            weight = args[i + 1]
            total += value * weight
            weight_sum += weight
        
        if weight_sum == 0:
            return 0
        return total / weight_sum
    
    result = engine.evaluate("weighted_avg(80, 0.3, 90, 0.5, 85, 0.2)")
    print(f"weighted_avg(80, 0.3, 90, 0.5, 85, 0.2) = {result}")
    
    print()


def function_with_validation():
    """Functions with input validation."""
    print("=== Functions with Validation ===")
    
    @builtin_function(
        name="calculate_age",
        category=FunctionCategory.DATE,
        description="Calculate age from birth date"
    )
    def calculate_age(birth_date, reference_date=None):
        """Calculate age from birth date."""
        from datetime import datetime
        
        if reference_date is None:
            reference_date = datetime.now()
        
        if birth_date > reference_date:
            raise ValueError("Birth date cannot be in the future")
        
        age = reference_date.year - birth_date.year
        if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    engine = ExpressionEngine()
    
    # 使用日期对象
    from datetime import datetime
    context = {
        "birth_date": datetime(1990, 5, 20),
        "today": datetime(2024, 1, 15)
    }
    
    result = engine.evaluate("calculate_age(birth_date, today)", context)
    print(f"Age: {result}")
    
    print()


def main():
    """Run all custom function examples."""
    basic_custom_functions()
    decorator_functions()
    function_categories()
    function_registry()
    advanced_functions()
    function_with_validation()


if __name__ == "__main__":
    main()
