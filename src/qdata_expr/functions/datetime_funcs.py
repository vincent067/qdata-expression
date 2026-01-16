"""
日期时间函数库

提供日期时间处理相关的内置函数。
"""

from collections.abc import Callable
from datetime import date, datetime, time, timedelta
from typing import Any

from .base import FunctionCategory, FunctionDefinition


def _to_datetime(value: Any) -> datetime:
    """转换为 datetime"""
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time.min)
    if isinstance(value, str):
        # 尝试常见格式
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y%m%d",
            "%Y%m%d%H%M%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"无法解析日期时间: {value}")
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value)
    raise TypeError(f"无法将 {type(value).__name__} 转换为 datetime")


def _to_date(value: Any) -> date:
    """转换为 date"""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return _to_datetime(value).date()


# ============================================================
# 当前时间
# ============================================================


def expr_now() -> datetime:
    """返回当前日期时间"""
    return datetime.now()


def expr_today() -> date:
    """返回当前日期"""
    return date.today()


def expr_utc_now() -> datetime:
    """返回当前 UTC 时间"""
    from datetime import timezone
    return datetime.now(timezone.utc)


def expr_current_time() -> time:
    """返回当前时间"""
    return datetime.now().time()


def expr_timestamp() -> float:
    """返回当前时间戳"""
    return datetime.now().timestamp()


# ============================================================
# 格式化与解析
# ============================================================


def expr_date_format(value: Any, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    dt = _to_datetime(value)
    return dt.strftime(fmt)


def expr_date_parse(value: str, fmt: str = "%Y-%m-%d") -> datetime:
    """解析日期时间字符串"""
    return datetime.strptime(value, fmt)


def expr_iso_format(value: Any) -> str:
    """转换为 ISO 格式"""
    dt = _to_datetime(value)
    return dt.isoformat()


def expr_to_timestamp(value: Any) -> float:
    """转换为时间戳"""
    dt = _to_datetime(value)
    return dt.timestamp()


def expr_from_timestamp(value: float) -> datetime:
    """从时间戳转换"""
    return datetime.fromtimestamp(value)


# ============================================================
# 日期组件提取
# ============================================================


def expr_year(value: Any) -> int:
    """获取年份"""
    return _to_datetime(value).year


def expr_month(value: Any) -> int:
    """获取月份 (1-12)"""
    return _to_datetime(value).month


def expr_day(value: Any) -> int:
    """获取日 (1-31)"""
    return _to_datetime(value).day


def expr_hour(value: Any) -> int:
    """获取小时 (0-23)"""
    return _to_datetime(value).hour


def expr_minute(value: Any) -> int:
    """获取分钟 (0-59)"""
    return _to_datetime(value).minute


def expr_second(value: Any) -> int:
    """获取秒 (0-59)"""
    return _to_datetime(value).second


def expr_weekday(value: Any) -> int:
    """获取星期几 (0=周一, 6=周日)"""
    return _to_datetime(value).weekday()


def expr_isoweekday(value: Any) -> int:
    """获取 ISO 星期几 (1=周一, 7=周日)"""
    return _to_datetime(value).isoweekday()


def expr_week_of_year(value: Any) -> int:
    """获取一年中的第几周"""
    return _to_datetime(value).isocalendar()[1]


def expr_day_of_year(value: Any) -> int:
    """获取一年中的第几天"""
    dt = _to_datetime(value)
    return dt.timetuple().tm_yday


def expr_quarter(value: Any) -> int:
    """获取季度 (1-4)"""
    month = _to_datetime(value).month
    return (month - 1) // 3 + 1


# ============================================================
# 日期运算
# ============================================================


def expr_add_days(value: Any, days: int) -> datetime:
    """添加天数"""
    dt = _to_datetime(value)
    return dt + timedelta(days=days)


def expr_add_hours(value: Any, hours: int) -> datetime:
    """添加小时"""
    dt = _to_datetime(value)
    return dt + timedelta(hours=hours)


def expr_add_minutes(value: Any, minutes: int) -> datetime:
    """添加分钟"""
    dt = _to_datetime(value)
    return dt + timedelta(minutes=minutes)


def expr_add_seconds(value: Any, seconds: int) -> datetime:
    """添加秒"""
    dt = _to_datetime(value)
    return dt + timedelta(seconds=seconds)


def expr_add_weeks(value: Any, weeks: int) -> datetime:
    """添加周"""
    dt = _to_datetime(value)
    return dt + timedelta(weeks=weeks)


def expr_add_months(value: Any, months: int) -> datetime:
    """添加月份"""
    dt = _to_datetime(value)
    new_month = dt.month + months
    new_year = dt.year + (new_month - 1) // 12
    new_month = (new_month - 1) % 12 + 1
    # 处理日期溢出（如 1月31日 + 1月 = 2月28日）
    import calendar
    max_day = calendar.monthrange(new_year, new_month)[1]
    new_day = min(dt.day, max_day)
    return dt.replace(year=new_year, month=new_month, day=new_day)


def expr_add_years(value: Any, years: int) -> datetime:
    """添加年份"""
    dt = _to_datetime(value)
    new_year = dt.year + years
    # 处理闰年问题（2月29日）
    import calendar
    if dt.month == 2 and dt.day == 29:
        if not calendar.isleap(new_year):
            return dt.replace(year=new_year, day=28)
    return dt.replace(year=new_year)


def expr_diff_days(start: Any, end: Any) -> int:
    """计算天数差"""
    start_dt = _to_datetime(start)
    end_dt = _to_datetime(end)
    return (end_dt - start_dt).days


def expr_diff_hours(start: Any, end: Any) -> float:
    """计算小时差"""
    start_dt = _to_datetime(start)
    end_dt = _to_datetime(end)
    return (end_dt - start_dt).total_seconds() / 3600


def expr_diff_seconds(start: Any, end: Any) -> float:
    """计算秒差"""
    start_dt = _to_datetime(start)
    end_dt = _to_datetime(end)
    return (end_dt - start_dt).total_seconds()


# ============================================================
# 日期边界
# ============================================================


def expr_start_of_day(value: Any) -> datetime:
    """获取一天的开始"""
    dt = _to_datetime(value)
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def expr_end_of_day(value: Any) -> datetime:
    """获取一天的结束"""
    dt = _to_datetime(value)
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def expr_start_of_week(value: Any) -> datetime:
    """获取一周的开始（周一）"""
    dt = _to_datetime(value)
    start = dt - timedelta(days=dt.weekday())
    return start.replace(hour=0, minute=0, second=0, microsecond=0)


def expr_end_of_week(value: Any) -> datetime:
    """获取一周的结束（周日）"""
    dt = _to_datetime(value)
    end = dt + timedelta(days=(6 - dt.weekday()))
    return end.replace(hour=23, minute=59, second=59, microsecond=999999)


def expr_start_of_month(value: Any) -> datetime:
    """获取一月的开始"""
    dt = _to_datetime(value)
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def expr_end_of_month(value: Any) -> datetime:
    """获取一月的结束"""
    import calendar
    dt = _to_datetime(value)
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    return dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)


def expr_start_of_year(value: Any) -> datetime:
    """获取一年的开始"""
    dt = _to_datetime(value)
    return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


def expr_end_of_year(value: Any) -> datetime:
    """获取一年的结束"""
    dt = _to_datetime(value)
    return dt.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)


# ============================================================
# 日期比较
# ============================================================


def expr_is_before(value: Any, other: Any) -> bool:
    """是否在指定日期之前"""
    return _to_datetime(value) < _to_datetime(other)


def expr_is_after(value: Any, other: Any) -> bool:
    """是否在指定日期之后"""
    return _to_datetime(value) > _to_datetime(other)


def expr_is_same_day(value: Any, other: Any) -> bool:
    """是否是同一天"""
    return _to_date(value) == _to_date(other)


def expr_is_weekend(value: Any) -> bool:
    """是否是周末"""
    return _to_datetime(value).weekday() >= 5


def expr_is_weekday(value: Any) -> bool:
    """是否是工作日"""
    return _to_datetime(value).weekday() < 5


def expr_is_leap_year(value: Any) -> bool:
    """是否是闰年"""
    import calendar
    year = _to_datetime(value).year
    return calendar.isleap(year)


# ============================================================
# 函数注册
# ============================================================


def _create_function_definition(
    name: str,
    func: Callable,
    description: str,
    signature: str,
    examples: list[str],
    min_args: int = 0,
    max_args: int | None = None,
) -> FunctionDefinition:
    """创建函数定义"""
    return FunctionDefinition(
        name=name,
        func=func,
        category=FunctionCategory.DATETIME,
        description=description,
        signature=signature,
        examples=examples,
        min_args=min_args,
        max_args=max_args,
    )


# 日期时间函数集合
DATETIME_FUNCTIONS: dict[str, FunctionDefinition] = {
    # 当前时间
    "now": _create_function_definition(
        "now", expr_now, "返回当前日期时间",
        "now() -> datetime", ["now() = 2024-01-15 10:30:00"],
        min_args=0, max_args=0,
    ),
    "today": _create_function_definition(
        "today", expr_today, "返回当前日期",
        "today() -> date", ["today() = 2024-01-15"],
        min_args=0, max_args=0,
    ),
    "utc_now": _create_function_definition(
        "utc_now", expr_utc_now, "返回当前 UTC 时间",
        "utc_now() -> datetime", ["utc_now() = 2024-01-15 02:30:00+00:00"],
        min_args=0, max_args=0,
    ),
    "timestamp": _create_function_definition(
        "timestamp", expr_timestamp, "返回当前时间戳",
        "timestamp() -> float", ["timestamp() = 1705301400.0"],
        min_args=0, max_args=0,
    ),
    # 格式化与解析
    "date_format": _create_function_definition(
        "date_format", expr_date_format, "格式化日期时间",
        "date_format(value, fmt='%Y-%m-%d %H:%M:%S') -> str",
        ['date_format(now(), "%Y年%m月%d日") = "2024年01月15日"'],
        min_args=1, max_args=2,
    ),
    "date_parse": _create_function_definition(
        "date_parse", expr_date_parse, "解析日期时间字符串",
        "date_parse(value, fmt='%Y-%m-%d') -> datetime",
        ['date_parse("2024-01-15", "%Y-%m-%d")'],
        min_args=1, max_args=2,
    ),
    "iso_format": _create_function_definition(
        "iso_format", expr_iso_format, "转换为 ISO 格式",
        "iso_format(value) -> str", ['iso_format(now()) = "2024-01-15T10:30:00"'],
        min_args=1, max_args=1,
    ),
    "to_timestamp": _create_function_definition(
        "to_timestamp", expr_to_timestamp, "转换为时间戳",
        "to_timestamp(value) -> float", ["to_timestamp(now()) = 1705301400.0"],
        min_args=1, max_args=1,
    ),
    "from_timestamp": _create_function_definition(
        "from_timestamp", expr_from_timestamp, "从时间戳转换",
        "from_timestamp(value) -> datetime", ["from_timestamp(1705301400)"],
        min_args=1, max_args=1,
    ),
    # 日期组件提取
    "year": _create_function_definition(
        "year", expr_year, "获取年份",
        "year(value) -> int", ["year(now()) = 2024"],
        min_args=1, max_args=1,
    ),
    "month": _create_function_definition(
        "month", expr_month, "获取月份",
        "month(value) -> int", ["month(now()) = 1"],
        min_args=1, max_args=1,
    ),
    "day": _create_function_definition(
        "day", expr_day, "获取日",
        "day(value) -> int", ["day(now()) = 15"],
        min_args=1, max_args=1,
    ),
    "hour": _create_function_definition(
        "hour", expr_hour, "获取小时",
        "hour(value) -> int", ["hour(now()) = 10"],
        min_args=1, max_args=1,
    ),
    "minute": _create_function_definition(
        "minute", expr_minute, "获取分钟",
        "minute(value) -> int", ["minute(now()) = 30"],
        min_args=1, max_args=1,
    ),
    "second": _create_function_definition(
        "second", expr_second, "获取秒",
        "second(value) -> int", ["second(now()) = 0"],
        min_args=1, max_args=1,
    ),
    "weekday": _create_function_definition(
        "weekday", expr_weekday, "获取星期几 (0=周一)",
        "weekday(value) -> int", ["weekday(now()) = 0"],
        min_args=1, max_args=1,
    ),
    "week_of_year": _create_function_definition(
        "week_of_year", expr_week_of_year, "获取一年中的第几周",
        "week_of_year(value) -> int", ["week_of_year(now()) = 3"],
        min_args=1, max_args=1,
    ),
    "quarter": _create_function_definition(
        "quarter", expr_quarter, "获取季度",
        "quarter(value) -> int", ["quarter(now()) = 1"],
        min_args=1, max_args=1,
    ),
    # 日期运算
    "add_days": _create_function_definition(
        "add_days", expr_add_days, "添加天数",
        "add_days(value, days) -> datetime", ["add_days(today(), 7)"],
        min_args=2, max_args=2,
    ),
    "add_hours": _create_function_definition(
        "add_hours", expr_add_hours, "添加小时",
        "add_hours(value, hours) -> datetime", ["add_hours(now(), 2)"],
        min_args=2, max_args=2,
    ),
    "add_months": _create_function_definition(
        "add_months", expr_add_months, "添加月份",
        "add_months(value, months) -> datetime", ["add_months(today(), 1)"],
        min_args=2, max_args=2,
    ),
    "add_years": _create_function_definition(
        "add_years", expr_add_years, "添加年份",
        "add_years(value, years) -> datetime", ["add_years(today(), 1)"],
        min_args=2, max_args=2,
    ),
    "diff_days": _create_function_definition(
        "diff_days", expr_diff_days, "计算天数差",
        "diff_days(start, end) -> int", ['diff_days("2024-01-01", "2024-01-15") = 14'],
        min_args=2, max_args=2,
    ),
    "diff_hours": _create_function_definition(
        "diff_hours", expr_diff_hours, "计算小时差",
        "diff_hours(start, end) -> float", ['diff_hours(start, end) = 24.0'],
        min_args=2, max_args=2,
    ),
    # 日期边界
    "start_of_day": _create_function_definition(
        "start_of_day", expr_start_of_day, "获取一天的开始",
        "start_of_day(value) -> datetime", ["start_of_day(now()) = 2024-01-15 00:00:00"],
        min_args=1, max_args=1,
    ),
    "end_of_day": _create_function_definition(
        "end_of_day", expr_end_of_day, "获取一天的结束",
        "end_of_day(value) -> datetime", ["end_of_day(now()) = 2024-01-15 23:59:59"],
        min_args=1, max_args=1,
    ),
    "start_of_month": _create_function_definition(
        "start_of_month", expr_start_of_month, "获取一月的开始",
        "start_of_month(value) -> datetime", ["start_of_month(now()) = 2024-01-01 00:00:00"],
        min_args=1, max_args=1,
    ),
    "end_of_month": _create_function_definition(
        "end_of_month", expr_end_of_month, "获取一月的结束",
        "end_of_month(value) -> datetime", ["end_of_month(now()) = 2024-01-31 23:59:59"],
        min_args=1, max_args=1,
    ),
    # 日期比较
    "is_before": _create_function_definition(
        "is_before", expr_is_before, "是否在指定日期之前",
        "is_before(value, other) -> bool", ['is_before("2024-01-01", "2024-01-15") = True'],
        min_args=2, max_args=2,
    ),
    "is_after": _create_function_definition(
        "is_after", expr_is_after, "是否在指定日期之后",
        "is_after(value, other) -> bool", ['is_after("2024-01-15", "2024-01-01") = True'],
        min_args=2, max_args=2,
    ),
    "is_weekend": _create_function_definition(
        "is_weekend", expr_is_weekend, "是否是周末",
        "is_weekend(value) -> bool", ["is_weekend(today()) = False"],
        min_args=1, max_args=1,
    ),
    "is_weekday": _create_function_definition(
        "is_weekday", expr_is_weekday, "是否是工作日",
        "is_weekday(value) -> bool", ["is_weekday(today()) = True"],
        min_args=1, max_args=1,
    ),
}


def get_datetime_functions() -> dict[str, Callable]:
    """获取所有日期时间函数"""
    return {name: defn.func for name, defn in DATETIME_FUNCTIONS.items()}
