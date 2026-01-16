# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of qdata-expression
- ExpressionEngine with safe expression evaluation
- TemplateEngine with Jinja2 support
- ContextResolver for nested path access
- Sandbox with security validation
- Extensive built-in function library
- Complete test suite with pytest
- Type hints and mypy support
- Performance optimization with expression caching

### Features
- Mathematical functions: abs, round, floor, ceil, min, max, sum, avg, pow, sqrt, etc.
- String functions: upper, lower, trim, concat, substring, replace, split, join, etc.
- Logic functions: if_else, is_null, is_empty, coalesce, and, or, not, etc.
- List functions: length, sort, unique, contains, reverse, flatten, etc.
- DateTime functions: now, today, date_format, add_days, diff_days, etc.
- Custom function registration with decorators
- Template rendering with filters and conditionals
- Security sandbox with configurable restrictions
- Expression validation and variable extraction
- Context manipulation (get, set, delete, merge)
- Performance benchmarking tools

### Security
- Safe evaluation preventing code injection
- Restricted built-in access
- Private attribute blocking
- Import statement blocking
- Configurable execution limits

### Documentation
- Comprehensive README with examples
- API documentation
- Usage examples for all major features
- Security guidelines
- Performance optimization tips

## [0.1.0] - 2024-01-15

### Initial Release
- Expression evaluation engine
- Template rendering system
- Built-in function library
- Security sandbox
- Basic documentation and examples
