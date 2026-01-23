"""
Tests for DAG workflow integration patterns.

These tests verify that qdata-expression works correctly in DAG workflow scenarios
similar to what would be used in QDataV2.
"""

from datetime import datetime

from qdata_expr import (
    ExpressionEngine,
    TemplateEngine,
    merge_context,
    render_template,
    resolve,
    set_path,
)


class TestDAGNodeContext:
    """Test patterns for DAG node context building."""

    def test_build_node_input_context(self):
        """Test building input context for a DAG node."""
        # Simulate upstream node outputs
        upstream_outputs = {
            "node_fetch_data": {
                "status": "success",
                "data": [
                    {"id": 1, "name": "Product A", "price": 100.0},
                    {"id": 2, "name": "Product B", "price": 200.0},
                ],
                "metadata": {"count": 2, "source": "api"},
            },
            "node_config": {
                "discount_rate": 0.1,
                "tax_rate": 0.08,
            },
        }

        # Build node input context
        context = {
            "upstream": upstream_outputs,
            "node": {
                "id": "node_transform",
                "name": "Transform Data",
            },
            "runtime": {
                "execution_id": "exec_123",
                "timestamp": datetime.now(),
            },
        }

        # Access upstream data
        data = resolve("upstream.node_fetch_data.data", context)
        assert len(data) == 2
        assert data[0]["name"] == "Product A"

        # Access configuration
        discount = resolve("upstream.node_config.discount_rate", context)
        assert discount == 0.1

    def test_expression_evaluation_in_node(self):
        """Test expression evaluation within a node."""
        engine = ExpressionEngine()

        context = {
            "node_input": {
                "products": [
                    {"name": "A", "price": 100, "quantity": 2},
                    {"name": "B", "price": 50, "quantity": 5},
                ],
            },
            "config": {
                "discount": 0.1,
                "min_order": 200,
            },
        }

        # Calculate total
        result = engine.evaluate(
            "sum([p['price'] * p['quantity'] for p in node_input['products']])", context
        )
        assert result == 450  # 100*2 + 50*5

        # Apply discount
        discounted = engine.evaluate(
            "sum([p['price'] * p['quantity'] for p in node_input['products']]) "
            "* (1 - config['discount'])",
            context,
        )
        assert discounted == 405.0

        # Check threshold condition
        meets_threshold = engine.evaluate(
            "sum([p['price'] * p['quantity'] for p in node_input['products']]) "
            ">= config['min_order']",
            context,
        )
        assert meets_threshold is True

    def test_conditional_branching_expressions(self):
        """Test conditional expressions for DAG branching."""
        engine = ExpressionEngine()

        # Simulate different scenarios
        test_cases = [
            ({"order_total": 1500, "customer_tier": "gold"}, "vip_processing"),
            ({"order_total": 800, "customer_tier": "silver"}, "standard_processing"),
            ({"order_total": 100, "customer_tier": "bronze"}, "basic_processing"),
        ]

        for context, expected_branch in test_cases:
            # Complex branching logic
            result = engine.evaluate(
                "'vip_processing' if order_total > 1000 and customer_tier == 'gold' else "
                "'standard_processing' if order_total > 500 else "
                "'basic_processing'",
                context,
            )
            assert result == expected_branch, f"Failed for context {context}"

    def test_data_transformation_expressions(self):
        """Test data transformation expressions."""
        engine = ExpressionEngine()

        context = {
            "records": [
                {"id": 1, "first_name": "John", "last_name": "Doe", "score": 85},
                {"id": 2, "first_name": "Jane", "last_name": "Smith", "score": 92},
                {"id": 3, "first_name": "Bob", "last_name": "Johnson", "score": 78},
            ],
        }

        # Extract names
        names = engine.evaluate(
            "[r['first_name'] + ' ' + r['last_name'] for r in records]", context
        )
        assert names == ["John Doe", "Jane Smith", "Bob Johnson"]

        # Filter by score
        high_scorers = engine.evaluate("[r for r in records if r['score'] >= 80]", context)
        assert len(high_scorers) == 2

        # Calculate average
        avg_score = engine.evaluate("sum([r['score'] for r in records]) / len(records)", context)
        assert avg_score == 85.0

    def test_error_handling_expressions(self):
        """Test error handling with if_null and coalesce."""
        engine = ExpressionEngine()

        context = {
            "data": {
                "valid_field": "value",
                "nullable_field": None,
            },
        }

        # Using if_null
        result = engine.evaluate("if_null(data['nullable_field'], 'default_value')", context)
        assert result == "default_value"

        result = engine.evaluate("if_null(data['valid_field'], 'default_value')", context)
        assert result == "value"

        # Using coalesce
        result = engine.evaluate("coalesce(data['nullable_field'], None, 'fallback')", context)
        assert result == "fallback"


class TestTemplateRenderingForDAG:
    """Test template rendering patterns for DAG workflows."""

    def test_notification_template(self):
        """Test notification message template."""
        template = """
任务执行通知

任务ID: {{ task_id }}
任务名称: {{ task_name }}
状态: {{ status }}
执行时间: {{ execution_time }}

{% if status == 'success' %}
✅ 任务执行成功！
处理记录数: {{ records_processed }}
{% else %}
❌ 任务执行失败
错误信息: {{ error_message }}
{% endif %}
"""
        context = {
            "task_id": "task_001",
            "task_name": "数据同步",
            "status": "success",
            "execution_time": "2024-01-15 10:30:00",
            "records_processed": 1500,
            "error_message": "",
        }

        result = render_template(template, context)
        assert "task_001" in result
        assert "✅ 任务执行成功！" in result
        assert "1500" in result

    def test_report_generation_template(self):
        """Test data report template."""
        template_engine = TemplateEngine()

        template = """
# 数据报告

## 概要
- 总记录数: {{ summary.total_records }}
- 成功: {{ summary.success_count }}
- 失败: {{ summary.failure_count }}
- 成功率: {{ (summary.success_count / summary.total_records * 100) | round(2) }}%

## 详细数据
{% for item in data_list %}
- {{ item.name }}: {{ item.value }}
{% endfor %}
"""
        context = {
            "summary": {
                "total_records": 100,
                "success_count": 95,
                "failure_count": 5,
            },
            "data_list": [
                {"name": "指标A", "value": 1234},
                {"name": "指标B", "value": 5678},
            ],
        }

        result = template_engine.render(template, context)
        assert "总记录数: 100" in result
        assert "成功率: 95.0%" in result


class TestDataPipelinePatterns:
    """Test common data pipeline patterns."""

    def test_field_mapping(self):
        """Test field mapping expressions."""
        engine = ExpressionEngine()

        source_record = {
            "src_id": "12345",
            "src_name": "Test Product",
            "src_price": "99.99",
            "src_category": "electronics",
        }

        # Field mapping configuration
        mappings = {
            "id": "src_id",
            "name": "upper(src_name)",
            "price": "to_float(src_price)",
            "category": "title(src_category)",
        }

        # Apply mappings
        result = {}
        for target, expr in mappings.items():
            result[target] = engine.evaluate(expr, source_record)

        assert result["id"] == "12345"
        assert result["name"] == "TEST PRODUCT"
        assert result["price"] == 99.99
        assert result["category"] == "Electronics"

    def test_data_validation_rules(self):
        """Test data validation expressions."""
        engine = ExpressionEngine()

        records = [
            {"email": "valid@example.com", "age": 25, "name": "John"},
            {"email": "invalid-email", "age": -5, "name": ""},
            {"email": "another@test.com", "age": 150, "name": "Jane"},
        ]

        validation_rules = {
            "email_valid": "contains(email, '@') and contains(email, '.')",
            "age_valid": "age >= 0 and age <= 120",
            "name_valid": "is_not_empty(name)",
        }

        results = []
        for record in records:
            validations = {}
            for rule_name, rule_expr in validation_rules.items():
                validations[rule_name] = engine.evaluate(rule_expr, record)
            is_valid = all(validations.values())
            results.append({"record": record, "validations": validations, "is_valid": is_valid})

        assert results[0]["is_valid"] is True  # First record is valid
        assert results[1]["is_valid"] is False  # Second has invalid email, age, and name
        assert results[2]["is_valid"] is False  # Third has invalid age

    def test_aggregation_expressions(self):
        """Test data aggregation expressions."""
        engine = ExpressionEngine()

        context = {
            "sales": [
                {"region": "North", "product": "A", "amount": 1000},
                {"region": "South", "product": "A", "amount": 1500},
                {"region": "North", "product": "B", "amount": 800},
                {"region": "South", "product": "B", "amount": 1200},
            ],
        }

        # Total sales
        total = engine.evaluate("sum([s['amount'] for s in sales])", context)
        assert total == 4500

        # Sales by region
        north_sales = engine.evaluate(
            "sum([s['amount'] for s in sales if s['region'] == 'North'])", context
        )
        assert north_sales == 1800

        # Average sale
        avg = engine.evaluate("avg([s['amount'] for s in sales])", context)
        assert avg == 1125.0

    def test_date_filtering(self):
        """Test date-based filtering expressions."""
        engine = ExpressionEngine()

        context = {
            "orders": [
                {"id": 1, "date": "2024-01-10", "amount": 100},
                {"id": 2, "date": "2024-01-15", "amount": 200},
                {"id": 3, "date": "2024-01-20", "amount": 300},
            ],
            "cutoff_date": "2024-01-15",
        }

        # Filter orders after cutoff
        result = engine.evaluate("[o for o in orders if o['date'] >= cutoff_date]", context)
        assert len(result) == 2


class TestContextMerging:
    """Test context merging patterns for DAG nodes."""

    def test_merge_upstream_outputs(self):
        """Test merging outputs from multiple upstream nodes."""
        node1_output = {
            "data": {"users": [{"id": 1}, {"id": 2}]},
            "metadata": {"count": 2},
        }

        node2_output = {
            "data": {"products": [{"id": "A"}, {"id": "B"}]},
            "metadata": {"count": 2},
        }

        # Merge contexts
        merged = merge_context(
            {"node1": node1_output},
            {"node2": node2_output},
        )

        assert resolve("node1.data.users", merged) is not None
        assert resolve("node2.data.products", merged) is not None

    def test_context_path_building(self):
        """Test building context paths dynamically."""
        base_context = {}

        # Build context step by step
        context = set_path("workflow.id", "wf_001", base_context)
        context = set_path("workflow.name", "Data Pipeline", context)
        context = set_path("workflow.nodes.fetch.status", "completed", context)
        context = set_path("workflow.nodes.transform.status", "running", context)

        assert resolve("workflow.id", context) == "wf_001"
        assert resolve("workflow.nodes.fetch.status", context) == "completed"


class TestExpressionSecurity:
    """Test security aspects for DAG workflow expressions."""

    def test_safe_user_expressions(self):
        """Test that user-provided expressions are safely evaluated."""
        engine = ExpressionEngine()

        # These should all be safe
        safe_expressions = [
            ("price * quantity", {"price": 10, "quantity": 5}, 50),
            ("upper(name)", {"name": "test"}, "TEST"),
            ("length(item_list)", {"item_list": [1, 2, 3]}, 3),
            ("if_else(flag, 'yes', 'no')", {"flag": True}, "yes"),
        ]

        for expr, ctx, expected in safe_expressions:
            result = engine.evaluate(expr, ctx)
            assert result == expected

    def test_expression_validation(self):
        """Test expression validation before execution."""
        engine = ExpressionEngine()

        # Valid expressions
        assert engine.validate("2 + 3") == []
        assert engine.validate("price * quantity") == []

        # Invalid expressions
        assert len(engine.validate("2 +")) > 0  # Syntax error

    def test_variable_extraction(self):
        """Test extracting variables from expressions for validation."""
        engine = ExpressionEngine()

        variables = engine.get_variables("price * quantity + tax - discount")

        assert "price" in variables
        assert "quantity" in variables
        assert "tax" in variables
        assert "discount" in variables
