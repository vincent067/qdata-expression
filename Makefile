.PHONY: help install install-dev test test-cov lint format type-check clean build upload docs version bump-patch bump-minor bump-major publish publish-test security check

# 颜色输出
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

help:
	@echo "$(BLUE)QData Expression - 开发工具$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "传统命令 (向后兼容):"
	@echo "  install, install-dev, test, test-cov, lint, format, type-check"
	@echo "  clean, build, upload, docs"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest

test-cov:
	pytest --cov=qdata_expr --cov-report=term-missing --cov-report=html

test-verbose:
	pytest -v

test-benchmark:
	pytest tests/test_evaluator.py::TestPerformance -v

# Code quality
lint:
	ruff check src tests
	bandit -r src

format:
	black src tests
	isort src tests

type-check:
	mypy src/qdata_expr

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .coverage.*
	rm -rf coverage.xml
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Building
build: clean
	python -m build

upload-test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload dist/*

# Documentation
docs:
	cd docs && make html

docs-serve:
	cd docs && make html && python -m http.server 8000 -d _build/html

# Development
dev-setup: install-dev
	pre-commit install

run-examples:
	python examples/basic_usage.py
	python examples/template_examples.py
	python examples/custom_functions.py
	python examples/security_examples.py

benchmark:
	python examples/performance_benchmark.py

# Security check
security: ## 运行安全检查
	@echo "$(BLUE)运行安全检查...$(NC)"
	bandit -r src -ll
	safety check

security-check: security  # 向后兼容

# All-in-one quality check
check: lint type-check security ## 运行所有检查

quality: format lint type-check test  # 向后兼容

# Version management
version: ## 显示当前版本号
	@python scripts/bump_version.py show

bump-patch: ## 递增 patch 版本号 (0.1.0 → 0.1.1)
	@python scripts/bump_version.py bump patch

bump-minor: ## 递增 minor 版本号 (0.1.0 → 0.2.0)
	@python scripts/bump_version.py bump minor

bump-major: ## 递增 major 版本号 (0.1.0 → 1.0.0)
	@python scripts/bump_version.py bump major

# Publishing
publish-test: build ## 发布到 Test PyPI
	@echo "$(BLUE)发布到 Test PyPI...$(NC)"
	python -m twine upload --repository testpypi dist/*

publish: build ## 发布到 PyPI (需要确认)
	@echo "$(YELLOW)准备发布到 PyPI...$(NC)"
	@echo "$(YELLOW)请确认版本号和 CHANGELOG 已更新！$(NC)"
	@read -p "确认发布? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python -m twine upload dist/*; \
		echo "$(GREEN)✓ 发布成功！$(NC)"; \
	else \
		echo "$(YELLOW)✗ 取消发布$(NC)"; \
	fi

upload-test: publish-test  # 向后兼容

upload: publish  # 向后兼容

# Release preparation
release: clean quality build ## 准备发布（测试+构建）
	@echo "$(GREEN)Ready for release! Check dist/ for built packages.$(NC)"

.DEFAULT_GOAL := help
