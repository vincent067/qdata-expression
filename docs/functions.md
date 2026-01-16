# 内置函数

QData Expression 提供了丰富的内置函数，分为以下几类：

## 数学函数

| 函数 | 签名 | 描述 | 示例 |
|------|------|------|------|
| `abs` | `abs(x)` | 返回绝对值 | `abs(-5) → 5` |
| `round` | `round(x, n=0)` | 四舍五入 | `round(3.14159, 2) → 3.14` |
| `floor` | `floor(x)` | 向下取整 | `floor(3.7) → 3` |
| `ceil` | `ceil(x)` | 向上取整 | `ceil(3.2) → 4` |
| `min` | `min(x1, x2, ...)` | 返回最小值 | `min(1, 2, 3) → 1` |
| `max` | `max(x1, x2, ...)` | 返回最大值 | `max(1, 2, 3) → 3` |
| `sum` | `sum(x1, x2, ...)` | 求和 | `sum(1, 2, 3) → 6` |
| `avg` | `avg(x1, x2, ...)` | 平均值 | `avg(1, 2, 3) → 2.0` |
| `pow` | `pow(x, y)` | 幂运算 | `pow(2, 3) → 8` |
| `sqrt` | `sqrt(x)` | 平方根 | `sqrt(16) → 4.0` |
| `log` | `log(x, base=e)` | 对数 | `log(100, 10) → 2.0` |
| `exp` | `exp(x)` | 指数函数 | `exp(1) → 2.718...` |
| `random` | `random()` | 返回 [0, 1) 随机数 | `random() → 0.xxx` |
| `random_int` | `random_int(a, b)` | 返回 [a, b] 随机整数 | `random_int(1, 10) → 5` |

### 示例

```python
from qdata_expr import evaluate

# 基本运算
evaluate("abs(-5)")           # 5
evaluate("round(3.14159, 2)") # 3.14
evaluate("pow(2, 10)")        # 1024
evaluate("sqrt(144)")         # 12.0

# 统计函数
evaluate("sum(1, 2, 3, 4, 5)")    # 15
evaluate("avg(10, 20, 30)")       # 20.0
evaluate("min(5, 2, 8, 1)")       # 1
evaluate("max(5, 2, 8, 1)")       # 8
```

---

## 字符串函数

| 函数 | 签名 | 描述 | 示例 |
|------|------|------|------|
| `upper` | `upper(s)` | 转大写 | `upper('hello') → 'HELLO'` |
| `lower` | `lower(s)` | 转小写 | `lower('WORLD') → 'world'` |
| `trim` | `trim(s)` | 去除两端空格 | `trim('  hi  ') → 'hi'` |
| `ltrim` | `ltrim(s)` | 去除左侧空格 | `ltrim('  hi') → 'hi'` |
| `rtrim` | `rtrim(s)` | 去除右侧空格 | `rtrim('hi  ') → 'hi'` |
| `concat` | `concat(s1, s2, ...)` | 连接字符串 | `concat('a', 'b', 'c') → 'abc'` |
| `substring` | `substring(s, start, end)` | 截取子串 | `substring('hello', 0, 3) → 'hel'` |
| `replace` | `replace(s, old, new)` | 替换字符串 | `replace('hi', 'i', 'ello') → 'hello'` |
| `split` | `split(s, sep)` | 分割字符串 | `split('a,b,c', ',') → ['a', 'b', 'c']` |
| `join` | `join(lst, sep)` | 连接列表 | `join(['a', 'b'], '-') → 'a-b'` |
| `length` | `length(s)` | 字符串长度 | `length('hello') → 5` |
| `contains` | `contains(s, sub)` | 是否包含 | `contains('hello', 'ell') → True` |
| `starts_with` | `starts_with(s, prefix)` | 是否以前缀开始 | `starts_with('hello', 'he') → True` |
| `ends_with` | `ends_with(s, suffix)` | 是否以后缀结束 | `ends_with('hello', 'lo') → True` |
| `index_of` | `index_of(s, sub)` | 查找位置 | `index_of('hello', 'l') → 2` |
| `repeat` | `repeat(s, n)` | 重复字符串 | `repeat('ab', 3) → 'ababab'` |
| `reverse` | `reverse(s)` | 反转字符串 | `reverse('hello') → 'olleh'` |
| `capitalize` | `capitalize(s)` | 首字母大写 | `capitalize('hello') → 'Hello'` |
| `title` | `title(s)` | 标题格式 | `title('hello world') → 'Hello World'` |

### 示例

```python
from qdata_expr import evaluate

# 大小写转换
evaluate("upper('hello')")      # 'HELLO'
evaluate("lower('WORLD')")      # 'world'
evaluate("capitalize('john')")  # 'John'

# 字符串操作
evaluate("trim('  hello  ')")                # 'hello'
evaluate("concat('Hello', ' ', 'World')")    # 'Hello World'
evaluate("replace('hello', 'l', 'L')")       # 'heLLo'
evaluate("substring('hello world', 0, 5)")   # 'hello'

# 查找和判断
evaluate("contains('hello', 'ell')")       # True
evaluate("starts_with('hello', 'he')")     # True
evaluate("ends_with('hello', 'lo')")       # True
```

---

## 逻辑函数

| 函数 | 签名 | 描述 | 示例 |
|------|------|------|------|
| `if_else` | `if_else(cond, t, f)` | 条件判断 | `if_else(5>3, 'yes', 'no') → 'yes'` |
| `is_null` | `is_null(x)` | 是否为 None | `is_null(None) → True` |
| `is_empty` | `is_empty(x)` | 是否为空 | `is_empty('') → True` |
| `is_blank` | `is_blank(x)` | 是否为空白 | `is_blank('  ') → True` |
| `coalesce` | `coalesce(x1, x2, ...)` | 返回首个非空值 | `coalesce(None, '', 'a') → 'a'` |
| `default` | `default(x, d)` | 空值时返回默认值 | `default(None, 0) → 0` |
| `and_` | `and_(x1, x2, ...)` | 逻辑与 | `and_(True, True) → True` |
| `or_` | `or_(x1, x2, ...)` | 逻辑或 | `or_(True, False) → True` |
| `not_` | `not_(x)` | 逻辑非 | `not_(True) → False` |
| `eq` | `eq(x, y)` | 等于 | `eq(1, 1) → True` |
| `ne` | `ne(x, y)` | 不等于 | `ne(1, 2) → True` |
| `gt` | `gt(x, y)` | 大于 | `gt(2, 1) → True` |
| `gte` | `gte(x, y)` | 大于等于 | `gte(2, 2) → True` |
| `lt` | `lt(x, y)` | 小于 | `lt(1, 2) → True` |
| `lte` | `lte(x, y)` | 小于等于 | `lte(2, 2) → True` |
| `between` | `between(x, a, b)` | 是否在区间内 | `between(5, 1, 10) → True` |
| `in_list` | `in_list(x, lst)` | 是否在列表中 | `in_list(2, [1,2,3]) → True` |

### 示例

```python
from qdata_expr import evaluate

# 条件判断
evaluate("if_else(age >= 18, 'adult', 'minor')", {"age": 25})  # 'adult'

# 空值处理
evaluate("coalesce(None, '', 'default')")  # 'default'
evaluate("default(price, 0)", {"price": None})  # 0

# 比较运算
evaluate("between(score, 60, 100)", {"score": 85})  # True
evaluate("in_list(status, ['active', 'pending'])", {"status": "active"})  # True
```

---

## 列表函数

| 函数 | 签名 | 描述 | 示例 |
|------|------|------|------|
| `length` | `length(lst)` | 列表长度 | `length([1,2,3]) → 3` |
| `first` | `first(lst)` | 第一个元素 | `first([1,2,3]) → 1` |
| `last` | `last(lst)` | 最后一个元素 | `last([1,2,3]) → 3` |
| `nth` | `nth(lst, n)` | 第 n 个元素 | `nth([1,2,3], 1) → 2` |
| `sort` | `sort(lst, reverse=False)` | 排序 | `sort([3,1,2]) → [1,2,3]` |
| `unique` | `unique(lst)` | 去重 | `unique([1,2,2,3]) → [1,2,3]` |
| `reverse_list` | `reverse_list(lst)` | 反转列表 | `reverse_list([1,2,3]) → [3,2,1]` |
| `contains_item` | `contains_item(lst, item)` | 是否包含元素 | `contains_item([1,2,3], 2) → True` |
| `index_of_item` | `index_of_item(lst, item)` | 元素位置 | `index_of_item([1,2,3], 2) → 1` |
| `slice` | `slice(lst, start, end)` | 切片 | `slice([1,2,3,4], 1, 3) → [2,3]` |
| `flat` | `flat(lst)` | 扁平化 | `flat([[1,2],[3]]) → [1,2,3]` |
| `map_` | `map_(lst, key)` | 提取属性 | `map_(items, 'name') → ['a','b']` |
| `filter_` | `filter_(lst, key, val)` | 筛选 | `filter_(items, 'active', True)` |
| `sum_list` | `sum_list(lst)` | 列表求和 | `sum_list([1,2,3]) → 6` |
| `avg_list` | `avg_list(lst)` | 列表平均值 | `avg_list([1,2,3]) → 2.0` |
| `min_list` | `min_list(lst)` | 列表最小值 | `min_list([1,2,3]) → 1` |
| `max_list` | `max_list(lst)` | 列表最大值 | `max_list([1,2,3]) → 3` |

### 示例

```python
from qdata_expr import evaluate

# 基本操作
evaluate("first([1, 2, 3])")           # 1
evaluate("last([1, 2, 3])")            # 3
evaluate("length([1, 2, 3, 4])")       # 4

# 排序和去重
evaluate("sort([3, 1, 4, 1, 5])")          # [1, 1, 3, 4, 5]
evaluate("unique([1, 2, 2, 3, 3, 3])")     # [1, 2, 3]

# 聚合
evaluate("sum_list([1, 2, 3, 4, 5])")  # 15
evaluate("avg_list([10, 20, 30])")     # 20.0
```

---

## 日期时间函数

| 函数 | 签名 | 描述 | 示例 |
|------|------|------|------|
| `now` | `now()` | 当前日期时间 | `now() → datetime` |
| `today` | `today()` | 今天日期 | `today() → date` |
| `year` | `year(date)` | 获取年份 | `year(date) → 2024` |
| `month` | `month(date)` | 获取月份 | `month(date) → 1` |
| `day` | `day(date)` | 获取日期 | `day(date) → 15` |
| `hour` | `hour(datetime)` | 获取小时 | `hour(dt) → 14` |
| `minute` | `minute(datetime)` | 获取分钟 | `minute(dt) → 30` |
| `second` | `second(datetime)` | 获取秒数 | `second(dt) → 45` |
| `weekday` | `weekday(date)` | 星期几 (0-6) | `weekday(date) → 0` |
| `date_format` | `date_format(date, fmt)` | 格式化日期 | `date_format(d, '%Y-%m-%d')` |
| `date_parse` | `date_parse(s, fmt)` | 解析日期 | `date_parse('2024-01-15', '%Y-%m-%d')` |
| `add_days` | `add_days(date, n)` | 加天数 | `add_days(today(), 7)` |
| `add_months` | `add_months(date, n)` | 加月数 | `add_months(today(), 1)` |
| `add_years` | `add_years(date, n)` | 加年数 | `add_years(today(), 1)` |
| `diff_days` | `diff_days(d1, d2)` | 天数差 | `diff_days(d1, d2) → 30` |
| `diff_months` | `diff_months(d1, d2)` | 月数差 | `diff_months(d1, d2) → 1` |
| `diff_years` | `diff_years(d1, d2)` | 年数差 | `diff_years(d1, d2) → 1` |
| `start_of_day` | `start_of_day(dt)` | 当天开始 | `start_of_day(now())` |
| `end_of_day` | `end_of_day(dt)` | 当天结束 | `end_of_day(now())` |
| `start_of_month` | `start_of_month(date)` | 月初 | `start_of_month(today())` |
| `end_of_month` | `end_of_month(date)` | 月末 | `end_of_month(today())` |

### 示例

```python
from qdata_expr import evaluate

# 获取当前时间
evaluate("now()")      # 当前日期时间
evaluate("today()")    # 今天日期

# 日期部分
evaluate("year(today())")   # 2024
evaluate("month(today())")  # 1
evaluate("day(today())")    # 15

# 日期运算
evaluate("add_days(today(), 7)")     # 一周后
evaluate("add_months(today(), 1)")   # 一个月后

# 格式化
evaluate("date_format(today(), '%Y年%m月%d日')")  # '2024年01月15日'
```

---

## 注册自定义函数

您可以轻松注册自己的函数：

```python
from qdata_expr import ExpressionEngine

engine = ExpressionEngine()

# 方法一：直接注册
def discount(price, rate):
    return price * (1 - rate)

engine.register_function("discount", discount)

# 使用
result = engine.evaluate("discount(100, 0.2)")  # 80


# 方法二：使用装饰器
from qdata_expr import builtin_function
from qdata_expr.functions import FunctionCategory

@builtin_function(
    name="tax",
    category=FunctionCategory.MATH,
    description="计算税费",
    signature="tax(amount, rate) -> float",
    examples=["tax(100, 0.1) → 10.0"]
)
def calculate_tax(amount, rate=0.1):
    return amount * rate
```
