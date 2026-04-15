# operator模块与排序

> **所属路径**：`01_基础能力/01_开发环境与技术英语/04_迭代器与函数式工具/04_operator模块与排序`
> **预计学习时间**：40 分钟
> **难度等级**：⭐⭐

---

## 前置知识

- [函数与模块](../../01_编程语言基础/03_函数与模块/03_函数与模块.md)（理解 `lambda` 表达式和函数作为参数传递）
- [itertools模块](../02_itertools模块/02_itertools模块.md)（了解迭代器组合工具的基本用法）
- [functools模块](../03_functools模块/03_functools模块.md)（了解 `partial` 和 `reduce` 的使用方式）

> 如果以上内容还不熟悉，建议先完成对应课程再继续。

---

## 学习目标

完成本节后，你将能够：

1. 使用 `operator.itemgetter`、`operator.attrgetter` 和 `operator.methodcaller` 高效地提取数据
2. 熟练运用 `sorted()`、`min()`、`max()` 的 `key` 参数实现多样化排序
3. 了解 `operator` 模块中的算术和比较运算符函数，并将它们与 `functools.reduce`、`itertools` 组合使用
4. 说明 `operator` 函数相比 `lambda` 在可读性和性能上的优势

---

## 正文讲解

### 1. 从一个排序难题说起

假设你拿到了一份学生成绩数据，存储为字典的列表：

```python
students = [
    {"name": "Alice", "score": 92, "age": 20},
    {"name": "Bob", "score": 85, "age": 22},
    {"name": "Carol", "score": 92, "age": 19},
    {"name": "Dave", "score": 78, "age": 21},
]
```

你想按成绩从高到低排序。用 `lambda` 很直观：

```python
sorted(students, key=lambda s: s["score"], reverse=True)
```

但如果需求变成"先按成绩降序，成绩相同再按年龄升序"呢？`lambda` 开始变复杂了。更关键的是——在大数据场景下，每次调用 `lambda` 都有函数调用开销，而 Python 标准库中的 **operator 模块** 提供了一组用 C 实现的高效替代方案。

**operator 模块** 的核心思想很简单：把 Python 的运算符（`+`、`-`、`[]`、`.attr` 等）包装成普通函数，让它们可以作为参数传递给 `sorted()`、`map()`、`reduce()` 等高阶函数。

### 2. itemgetter——从序列和字典中提取元素

**`operator.itemgetter(key)`** 创建一个可调用对象，当你用一个序列或字典去调用它时，它会返回指定键对应的值。这就像给 `[]` 操作符起了个名字：

```python
from operator import itemgetter

# 单个键提取
get_score = itemgetter("score")
print(get_score({"name": "Alice", "score": 92}))  # 92

# 多个键提取——返回元组
get_name_score = itemgetter("name", "score")
print(get_name_score({"name": "Alice", "score": 92, "age": 20}))
# ('Alice', 92)
```

回到排序问题，用 `itemgetter` 代替 `lambda` ：

```python
from operator import itemgetter

students = [
    {"name": "Alice", "score": 92, "age": 20},
    {"name": "Bob", "score": 85, "age": 22},
    {"name": "Carol", "score": 92, "age": 19},
    {"name": "Dave", "score": 78, "age": 21},
]

# 按成绩排序
by_score = sorted(students, key=itemgetter("score"), reverse=True)
for s in by_score:
    print(s["name"], s["score"])
# Alice 92, Carol 92, Bob 85, Dave 78
```

当传入多个键时，`itemgetter` 返回的元组会按从左到右的顺序作为排序依据。这样就能轻松实现"先按成绩降序，成绩相同按年龄升序"——不过需要注意，元组比较是统一升序或降序的。对于混合排序，可以借助负数技巧：

```python
# 先按成绩降序，再按年龄升序
# 技巧：对成绩取负值，统一用升序排列
result = sorted(students, key=lambda s: (-s["score"], s["age"]))
for s in result:
    print(s["name"], s["score"], s["age"])
# Carol 92 19 → Alice 92 20 → Bob 85 22 → Dave 78 21
```

`itemgetter` 同样适用于列表和元组——通过整数索引提取：

```python
pairs = [(3, "c"), (1, "a"), (2, "b")]
sorted(pairs, key=itemgetter(0))  # [(1, 'a'), (2, 'b'), (3, 'c')]
sorted(pairs, key=itemgetter(1))  # [(1, 'a'), (2, 'b'), (3, 'c')]
```

### 3. attrgetter——从对象中提取属性

如果你的数据不是字典而是对象，就轮到 **`operator.attrgetter`** 登场了。它的用法和 `itemgetter` 如出一辙，只是从 `[]` 变成了 `.` ：

```python
from operator import attrgetter

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def __repr__(self):
        return f"Student({self.name!r}, {self.score})"

students = [Student("Alice", 92), Student("Bob", 85), Student("Carol", 78)]

# 按 score 属性排序
result = sorted(students, key=attrgetter("score"))
print(result)  # [Student('Carol', 78), Student('Bob', 85), Student('Alice', 92)]
```

`attrgetter` 还支持"点号路径"来访问嵌套属性，例如 `attrgetter("address.city")` 等价于 `lambda x: x.address.city` 。

### 4. methodcaller——调用对象方法

**`operator.methodcaller(name, *args)`** 创建一个可调用对象，当你传入一个对象时，它会调用该对象上指定名称的方法。这在需要对一批对象统一调用某个方法时非常好用：

```python
from operator import methodcaller

# 对字符串列表统一调用 upper() 方法
words = ["hello", "world", "python"]
result = list(map(methodcaller("upper"), words))
print(result)  # ['HELLO', 'WORLD', 'PYTHON']

# 带参数的方法调用：按指定分隔符切分
splitter = methodcaller("split", ",")
print(splitter("a,b,c"))  # ['a', 'b', 'c']
```

### 5. 算术与比较运算符函数

`operator` 模块还把所有算术和比较运算符封装成了函数。这些函数在与 `functools.reduce` 或 **[itertools模块](../02_itertools模块/02_itertools模块.md)** 搭配时特别有用：

| 运算符 | operator 函数 | 等价表达式 |
| --- | --- | --- |
| `+` | `operator.add(a, b)` | `a + b` |
| `-` | `operator.sub(a, b)` | `a - b` |
| `*` | `operator.mul(a, b)` | `a * b` |
| `//` | `operator.floordiv(a, b)` | `a // b` |
| `<` | `operator.lt(a, b)` | `a < b` |
| `<=` | `operator.le(a, b)` | `a <= b` |
| `==` | `operator.eq(a, b)` | `a == b` |
| `not` | `operator.not_(a)` | `not a` |
| `[]` | `operator.getitem(obj, k)` | `obj[k]` |

使用示例——用 `operator.mul` 代替 `lambda` 计算阶乘：

```python
from functools import reduce
from operator import mul

factorial_5 = reduce(mul, range(1, 6))  # 1 * 2 * 3 * 4 * 5
print(factorial_5)  # 120
```

### 6. lambda 与 operator 对照表

下面这张表对比了常见场景下 `lambda` 和 `operator` 两种写法：

| 场景 | lambda 写法 | operator 写法 | 优势 |
| --- | --- | --- | --- |
| 按字典键排序 | `key=lambda x: x["name"]` | `key=itemgetter("name")` | 更简洁、更快 |
| 按对象属性排序 | `key=lambda x: x.score` | `key=attrgetter("score")` | 更简洁、更快 |
| 两数相加 | `lambda a, b: a + b` | `operator.add` | 无函数调用开销 |
| 两数相乘 | `lambda a, b: a * b` | `operator.mul` | 无函数调用开销 |
| 调用方法 | `lambda x: x.upper()` | `methodcaller("upper")` | 可配置方法名 |
| 取索引 | `lambda x: x[0]` | `itemgetter(0)` | 更简洁、更快 |

总结：当操作可以用 `operator` 模块中的现有函数表达时，优先使用它们——**更快、更简洁、意图更明确**。当逻辑较复杂（涉及条件判断、多步计算）时，`lambda` 或普通函数仍然是更好的选择。

### 7. 与 functools 和 itertools 的组合

`operator` 函数的真正威力在于与 **[functools模块](../03_functools模块/03_functools模块.md)** 和 **[itertools模块](../02_itertools模块/02_itertools模块.md)** 搭配使用，形成简洁的函数式数据处理链：

```python
from functools import reduce, partial
from operator import add, mul, itemgetter
from itertools import starmap

# 示例 1：用 reduce + mul 计算连乘
print(reduce(mul, [2, 3, 4, 5]))  # 120

# 示例 2：用 starmap + mul 计算点对乘积
pairs = [(2, 3), (4, 5), (6, 7)]
products = list(starmap(mul, pairs))
print(products)  # [6, 20, 42]

# 示例 3：求所有乘积之和
total = reduce(add, starmap(mul, pairs))
print(total)  # 68

# 示例 4：partial + itemgetter 创建特定的提取器
data = [{"x": 1, "y": 2}, {"x": 3, "y": 4}, {"x": 5, "y": 6}]
get_x = itemgetter("x")
x_values = list(map(get_x, data))
print(x_values)  # [1, 3, 5]
```

---

## 动手实践

下面是一个综合示例，模拟对一批员工记录进行多维度排序和聚合：

```python
# 文件：code/operator_demo.py
from operator import itemgetter, attrgetter, methodcaller, mul, add
from functools import reduce
from itertools import groupby

# --- 数据准备 ---
employees = [
    {"name": "Alice",  "dept": "工程", "salary": 15000},
    {"name": "Bob",    "dept": "市场", "salary": 12000},
    {"name": "Carol",  "dept": "工程", "salary": 18000},
    {"name": "Dave",   "dept": "市场", "salary": 11000},
    {"name": "Eve",    "dept": "工程", "salary": 16000},
    {"name": "Frank",  "dept": "人事", "salary": 13000},
]

# --- 1. 按部门排序，同部门内按薪资降序 ---
sorted_emps = sorted(employees, key=lambda e: (e["dept"], -e["salary"]))
print("=== 按部门和薪资排序 ===")
for emp in sorted_emps:
    print(f"  {emp['dept']:4s} | {emp['name']:6s} | {emp['salary']}")

# --- 2. 按部门分组，计算每组平均薪资 ---
print("\n=== 部门平均薪资 ===")
get_dept = itemgetter("dept")
get_salary = itemgetter("salary")
for dept, group in groupby(sorted_emps, key=get_dept):
    salaries = list(map(get_salary, group))
    avg = reduce(add, salaries) / len(salaries)
    print(f"  {dept}: {avg:.0f}")

# --- 3. 用 methodcaller 统一处理字符串 ---
names = list(map(itemgetter("name"), employees))
upper_names = list(map(methodcaller("upper"), names))
print(f"\n=== 大写名字 ===\n  {upper_names}")

# --- 4. 用 attrgetter 对自定义对象排序 ---
class Employee:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def __repr__(self):
        return f"{self.name}({self.score})"

team = [Employee("Alice", 88), Employee("Bob", 95), Employee("Carol", 91)]
top = max(team, key=attrgetter("score"))
print(f"\n=== 最高分 ===\n  {top}")
```

**运行说明**：
- 环境要求：Python 3.8+
- 运行命令：`python code/operator_demo.py`

**预期输出**：
```
=== 按部门和薪资排序 ===
  人事 | Frank  | 13000
  工程 | Carol  | 18000
  工程 | Eve    | 16000
  工程 | Alice  | 15000
  市场 | Bob    | 12000
  市场 | Dave   | 11000

=== 部门平均薪资 ===
  人事: 13000
  工程: 16333
  市场: 11500

=== 大写名字 ===
  ['ALICE', 'BOB', 'CAROL', 'DAVE', 'EVE', 'FRANK']

=== 最高分 ===
  Bob(95)
```

---

## 典型误区

| 误区 | 正确理解 |
| --- | --- |
| `itemgetter("score")` 直接返回值 | `itemgetter("score")` 返回的是一个可调用对象，需要再传入字典才能获取值 |
| 在需要复杂逻辑时强行使用 `operator` | 当排序键需要条件判断或多步计算时，`lambda` 或具名函数更可读 |
| `attrgetter` 和 `itemgetter` 可以互换 | `attrgetter` 用于对象属性（`.attr`），`itemgetter` 用于字典键或序列索引（`[key]`） |
| 以为 `operator` 函数仅用于排序 | `operator` 函数可以用在所有接受回调函数的场景——`map`、`filter`、`reduce`、`starmap` 等 |

---

## 练习题

### 练习 1：多条件排序（难度：⭐）

给定一组产品数据，按价格升序排列；价格相同时按名称字母序排列。使用 `itemgetter` 实现。

```python
products = [
    {"name": "Banana", "price": 3},
    {"name": "Apple", "price": 3},
    {"name": "Cherry", "price": 5},
    {"name": "Date", "price": 2},
]
```

<details>
<summary>💡 提示</summary>

`itemgetter` 传入多个键时，返回元组。Python 比较元组时按从左到右的顺序逐一比较。

</details>

<details>
<summary>✅ 参考答案</summary>

```python
from operator import itemgetter

products = [
    {"name": "Banana", "price": 3},
    {"name": "Apple", "price": 3},
    {"name": "Cherry", "price": 5},
    {"name": "Date", "price": 2},
]

result = sorted(products, key=itemgetter("price", "name"))
for p in result:
    print(f"{p['name']:8s} ${p['price']}")

assert [p["name"] for p in result] == ["Date", "Apple", "Banana", "Cherry"]
print("测试通过！")
```

</details>

### 练习 2：向量点积（难度：⭐⭐）

给定两个等长的数字列表 `a` 和 `b` ，使用 `operator.mul`、`itertools.starmap` 和 `functools.reduce`（或 `sum`）计算它们的 **[点积（Dot Product）](../../../02_数学基础/01_线性代数/)** 。

```python
a = [1, 2, 3]
b = [4, 5, 6]
# 期望结果：1*4 + 2*5 + 3*6 = 32
```

<details>
<summary>💡 提示</summary>

先用 `zip(a, b)` 配对，再用 `starmap(mul, ...)` 逐对相乘，最后用 `sum()` 求和。

</details>

<details>
<summary>✅ 参考答案</summary>

```python
from operator import mul
from itertools import starmap

a = [1, 2, 3]
b = [4, 5, 6]

dot = sum(starmap(mul, zip(a, b)))
print(f"点积 = {dot}")  # 32

assert dot == 32
print("测试通过！")
```

</details>

### 练习 3：分组统计 Top-N（难度：⭐⭐）

对以下销售数据，先按 `category` 分组，然后找出每组中 `revenue` 最高的记录。使用 `itemgetter` 完成排序和提取。

```python
sales = [
    {"product": "A", "category": "电子", "revenue": 5000},
    {"product": "B", "category": "食品", "revenue": 3000},
    {"product": "C", "category": "电子", "revenue": 8000},
    {"product": "D", "category": "食品", "revenue": 4500},
    {"product": "E", "category": "电子", "revenue": 6000},
]
```

<details>
<summary>💡 提示</summary>

先按 `category` 排序，再用 `itertools.groupby` 分组，对每个分组用 `max` + `itemgetter("revenue")` 取最大值。

</details>

<details>
<summary>✅ 参考答案</summary>

```python
from operator import itemgetter
from itertools import groupby

sales = [
    {"product": "A", "category": "电子", "revenue": 5000},
    {"product": "B", "category": "食品", "revenue": 3000},
    {"product": "C", "category": "电子", "revenue": 8000},
    {"product": "D", "category": "食品", "revenue": 4500},
    {"product": "E", "category": "电子", "revenue": 6000},
]

get_cat = itemgetter("category")
get_rev = itemgetter("revenue")

sorted_sales = sorted(sales, key=get_cat)
for category, group in groupby(sorted_sales, key=get_cat):
    top = max(group, key=get_rev)
    print(f"{category}: {top['product']} (revenue={top['revenue']})")

# 电子: C (revenue=8000)
# 食品: D (revenue=4500)
print("测试通过！")
```

</details>

---

## 下一步学习

- 📖 下一个知识点：[高阶函数实践](../05_高阶函数实践/05_高阶函数实践.md) — 综合运用 map/filter/reduce、函数组合和管道模式处理数据
- 🔗 相关知识点：[functools模块](../03_functools模块/03_functools模块.md) — 回顾 `partial` 和 `reduce` 等工具
- 📚 拓展阅读：[容器性能对比](../../03_容器类型深入/05_容器性能对比/05_容器性能对比.md) — 了解不同数据结构的性能特征，指导排序策略选择

---

## 参考资料

1. [Python 官方文档 - operator 模块](https://docs.python.org/zh-cn/3/library/operator.html) — operator 全部函数的完整 API 参考（官方文档）
2. [Python 官方文档 - 排序指南](https://docs.python.org/zh-cn/3/howto/sorting.html) — Python 排序技术详解，涵盖 key 函数用法（官方文档）
3. [Real Python - Python Sorting](https://realpython.com/python-sort/) — 排序方法详细教程与性能分析（公开教程）
4. [Python 官方文档 - 函数式编程 HOWTO](https://docs.python.org/zh-cn/3/howto/functional.html) — 函数式编程风格指南（官方文档）
