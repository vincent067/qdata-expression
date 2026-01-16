.PHONY: help install install-dev test test-cov lint format type-check clean build upload docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install       - Install the package"
	@echo "  install-dev   - Install with development dependencies"
	@echo "  test          - Run tests"
	@echo "  test-cov      - Run tests with coverage"
	@echo "  lint          - Run linting"
	@echo "  format        - Format code"
	@echo "  type-check    - Run type checking"
	@echo "  clean         - Clean build artifacts"
	@echo "  build         - Build package"
	@echo "  upload        - Upload to PyPI"
	@echo "  docs          - Build documentation"

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
security-check:
	bandit -r src
	safety check
	pip-audit

# All-in-one quality check
quality: format lint type-check test

# Release preparation
release: clean quality build
	@echo "Ready for release! Check dist/ for built packages."

.DEFAULT_GOAL := help
