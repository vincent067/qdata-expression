"""
Performance benchmark examples for qdata-expression.
"""

import time
import timeit
from statistics import mean, stdev

from qdata_expr import (
    CompiledExpression,
    ExpressionEngine,
    evaluate,
)


def basic_performance():
    """Basic performance measurements."""
    print("=== Basic Performance Test ===")
    
    engine = ExpressionEngine()
    
    # 测试表达式
    test_expressions = [
        ("2 + 3", "Simple arithmetic"),
        ("2 + 3 * 4", "Operator precedence"),
        ("abs(-5) + round(3.14, 2)", "Function calls"),
        ("max(1, 2, 3) * min(4, 5, 6)", "Multiple functions"),
        ("'hello' + ' ' + 'world'", "String operations"),
        ("len([1, 2, 3]) + sum([4, 5, 6])", "List operations"),
    ]
    
    print("Single evaluation (1000 iterations):")
    for expr, desc in test_expressions:
        # 预热
        for _ in range(10):
            engine.evaluate(expr)
        
        # 计时
        start_time = time.time()
        for _ in range(1000):
            result = engine.evaluate(expr)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 1000 * 1000  # 转换为毫秒
        print(f"  {desc:30s}: {avg_time:.3f}ms per evaluation")
    
    print()


def cache_performance():
    """Test cache performance."""
    print("=== Cache Performance Test ===")
    
    # 无缓存引擎
    engine_no_cache = ExpressionEngine(enable_cache=False)
    
    # 有缓存引擎
    engine_with_cache = ExpressionEngine(enable_cache=True)
    
    expressions = [
        "2 + 3 * 4",
        "abs(x) + round(y, 2)",
        "max(a, b, c) * min(d, e, f)",
    ]
    
    context = {
        "x": -10,
        "y": 3.14159,
        "a": 100,
        "b": 200,
        "c": 300,
        "d": 1,
        "e": 2,
        "f": 3,
    }
    
    print("Cache comparison (1000 evaluations each):")
    
    for expr in expressions:
        print(f"\nExpression: {expr}")
        
        # 无缓存
        start_time = time.time()
        for _ in range(1000):
            engine_no_cache.evaluate(expr, context)
        no_cache_time = time.time() - start_time
        
        # 有缓存（第一次 - 编译）
        start_time = time.time()
        for _ in range(1000):
            engine_with_cache.evaluate(expr, context)
        with_cache_time = time.time() - start_time
        
        # 有缓存（第二次 - 使用缓存）
        start_time = time.time()
        for _ in range(1000):
            engine_with_cache.evaluate(expr, context)
        cache_hit_time = time.time() - start_time
        
        print(f"  No cache:        {no_cache_time:.4f}s")
        print(f"  With cache:      {with_cache_time:.4f}s")
        print(f"  Cache hit:       {cache_hit_time:.4f}s")
        print(f"  Speedup:         {no_cache_time / cache_hit_time:.2f}x")
        
        # 缓存统计
        stats = engine_with_cache.cache_stats
        print(f"  Cache stats:     {stats}")
    
    print()


def compiled_expressions():
    """Test compiled expressions performance."""
    print("=== Compiled Expressions Performance ===")
    
    # 编译表达式
    expr1 = CompiledExpression.compile("x + y")
    expr2 = CompiledExpression.compile("abs(x) + round(y, 2)")
    expr3 = CompiledExpression.compile("max(a, b) * min(c, d)")
    
    context = {
        "x": 10,
        "y": 20,
        "a": 100,
        "b": 200,
        "c": 5,
        "d": 15,
    }
    
    expressions = [
        (expr1, "x + y"),
        (expr2, "abs(x) + round(y, 2)"),
        (expr3, "max(a, b) * min(c, d)"),
    ]
    
    print("Compiled vs Regular (10000 evaluations):")
    
    for compiled_expr, desc in expressions:
        # 编译表达式
        start_time = time.time()
        for _ in range(10000):
            result = compiled_expr.evaluate(context)
        compiled_time = time.time() - start_time
        
        # 常规表达式
        engine = ExpressionEngine()
        start_time = time.time()
        for _ in range(10000):
            result = engine.evaluate(desc, context)
        regular_time = time.time() - start_time
        
        print(f"  {desc:30s}:")
        print(f"    Compiled:  {compiled_time:.4f}s")
        print(f"    Regular:   {regular_time:.4f}s")
        print(f"    Speedup:   {regular_time / compiled_time:.2f}x")
        print()


def complex_expressions():
    """Test complex expressions performance."""
    print("=== Complex Expressions Performance ===")
    
    engine = ExpressionEngine()
    
    # 复杂表达式
    expressions = [
        ("sum([x**2 for x in range(100)])", "List comprehension"),
        ("max([abs(x - 50) for x in range(100)])", "Complex list comprehension"),
        ("{'a': 1, 'b': 2, 'c': 3}['a'] + {'x': 10, 'y': 20}['x']", "Dictionary access"),
        ("[i for i in range(50) if i % 2 == 0]", "Filtered list comprehension"),
        ("len([str(i) for i in range(20)]) + sum(range(10))", "Mixed operations"),
    ]
    
    print("Complex expressions (1000 evaluations):")
    
    for expr, desc in expressions:
        # 预热
        for _ in range(10):
            engine.evaluate(expr)
        
        start_time = time.time()
        for _ in range(1000):
            result = engine.evaluate(expr)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 1000 * 1000
        print(f"  {desc:35s}: {avg_time:.3f}ms")
    
    print()


def variable_extraction():
    """Test variable extraction performance."""
    print("=== Variable Extraction Performance ===")
    
    engine = ExpressionEngine()
    
    expressions = [
        "x + y",
        "abs(x) + round(y, 2)",
        "a + b * c / d - e",
        "func(x, y, z)",
        "obj.attr1 + obj.attr2.subattr",
    ]
    
    print("Variable extraction (10000 times):")
    
    for expr in expressions:
        start_time = time.time()
        for _ in range(10000):
            variables = engine.get_variables(expr)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10000 * 1000
        print(f"  {expr:30s}: {avg_time:.3f}ms -> {variables}")
    
    print()


def template_performance():
    """Test template rendering performance."""
    print("=== Template Performance ===")
    
    engine = TemplateEngine()
    
    templates = [
        ("Hello, {{ name }}!", "Simple variable"),
        ("{{ items | length }} items", "Filter"),
        ("{% for item in items %}{{ item }}{% endfor %}", "Loop"),
        ("{% if condition %}Yes{% else %}No{% endif %}", "Condition"),
        ("{{ user.name }} - {{ user.age }} years old", "Nested variable"),
    ]
    
    context = {
        "name": "Alice",
        "items": ["a", "b", "c", "d", "e"],
        "condition": True,
        "user": {"name": "Bob", "age": 30},
    }
    
    print("Template rendering (1000 times):")
    
    for template, desc in templates:
        # 预热
        for _ in range(10):
            engine.render(template, context)
        
        start_time = time.time()
        for _ in range(1000):
            result = engine.render(template, context)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 1000 * 1000
        print(f"  {desc:25s}: {avg_time:.3f}ms")
    
    print()


def memory_usage():
    """Test memory usage."""
    print("=== Memory Usage ===")
    
    import gc
    import sys
    
    def get_memory_usage():
        """Get current memory usage in MB."""
        if hasattr(sys, 'getsizeof'):
            # 粗略估计
            return sys.getsizeof(globals()) / 1024 / 1024
        return 0
    
    # 测试缓存内存使用
    print("Cache memory usage:")
    
    engine = ExpressionEngine(enable_cache=True)
    
    # 初始内存
    gc.collect()
    initial_memory = get_memory_usage()
    
    # 添加多个表达式到缓存
    expressions = [f"expr_{i} + {i * 2}" for i in range(1000)]
    
    for expr in expressions:
        engine.evaluate(expr)
    
    gc.collect()
    after_cache_memory = get_memory_usage()
    
    print(f"  Initial memory:  {initial_memory:.2f} MB")
    print(f"  After caching:   {after_cache_memory:.2f} MB")
    print(f"  Cache overhead:  {after_cache_memory - initial_memory:.2f} MB")
    
    # 清除缓存
    engine.clear_cache()
    gc.collect()
    after_clear_memory = get_memory_usage()
    
    print(f"  After clearing:  {after_clear_memory:.2f} MB")
    
    print()


def benchmark_summary():
    """Performance benchmark summary."""
    print("=== Benchmark Summary ===")
    
    # 使用 timeit 进行精确测量
    setup = """
from qdata_expr import ExpressionEngine, evaluate
engine = ExpressionEngine()
context = {"x": 10, "y": 20, "z": 30}
"""
    
    expressions = [
        ("2 + 3", "Simple arithmetic"),
        ("x + y", "Variable access"),
        ("abs(x) + round(y, 2)", "Function calls"),
        ("x + y * z / 2", "Complex expression"),
        ("evaluate('x + y', context)", "Convenience function"),
    ]
    
    print("timeit benchmark (10000 iterations):")
    
    for expr, desc in expressions:
        time_taken = timeit.timeit(
            expr,
            setup=setup,
            number=10000
        )
        avg_time = time_taken / 10000 * 1000000  # 微秒
        print(f"  {desc:25s}: {avg_time:.2f}μs per evaluation")
    
    print()


def recommendations():
    """Performance recommendations."""
    print("=== Performance Recommendations ===")
    
    print("1. Enable caching for repeated expressions:")
    print("   engine = ExpressionEngine(enable_cache=True)")
    
    print("\n2. Use compiled expressions for hot paths:")
    print("   compiled = CompiledExpression.compile(expr)")
    print("   result = compiled.evaluate(context)")
    
    print("\n3. Minimize context lookups:")
    print("   # Bad: multiple lookups")
    print("   expr = 'user.profile.name + user.profile.email'")
    print("   # Good: single lookup")
    print("   expr = 'profile.name + profile.email'")
    
    print("\n4. Avoid complex comprehensions in hot paths:")
    print("   # Use built-in functions instead")
    print("   expr = 'sum([x**2 for x in range(100)])'")
    print("   # Better: pre-calculate if possible")
    
    print("\n5. Use appropriate data structures:")
    print("   # List for ordered sequences")
    print("   # Dict for key-value access")
    print("   # Set for membership testing")
    
    print("\n6. Set reasonable sandbox limits:")
    print("   config = SandboxConfig(")
    print("       max_execution_time=5.0,")
    print("       max_recursion_depth=100,")
    print("       max_string_length=1000000,")
    print("   )")
    
    print("\n7. Profile your specific use case:")
    print("   - Measure with realistic data")
    print("   - Identify bottlenecks")
    print("   - Optimize critical paths")
    
    print()


def main():
    """Run all performance benchmarks."""
    basic_performance()
    cache_performance()
    compiled_expressions()
    complex_expressions()
    variable_extraction()
    template_performance()
    memory_usage()
    benchmark_summary()
    recommendations()


if __name__ == "__main__":
    main()
