# HermesSay 协议契约

**基础地址：** `http://<host>:1314`
**默认端口：** 1314

---

## 1. 执行函数

`POST /windows/run_func`

### 请求

```json
{
  "who": "string (必填) — 调用者身份",
  "say": "string (必填) — 调用说明",
  "abbreviation": "string (必填) — 函数缩写",
  "parms": "object (选填) — 传给函数的参数",
  "is_return": "boolean (选填, 默认 false) — 是否返回结果"
}
```

### 响应

| 状态码 | 条件 | 响应体 |
|--------|------|--------|
| 200 | 执行成功, is_return=true | `{"result": ..., "gate": {...}}` |
| 200 | 执行成功, is_return=false | `{"message": "执行完成", "gate": {...}}` |
| 400 | who 或 say 为空 | `{"error": "缺少参数：who 或 say 不能为空"}` |
| 404 | abbreviation 未注册 | `{"error": "简称未注册: xxx"}` |

### 门记录（gate）

每次执行都会生成，随响应返回并打印到桥控制台：

```json
{
  "who": "调用者",
  "say": "调用说明",
  "time": "2026-06-10 12:00:00",
  "funcname": "read_file",
  "abbreviation": "read_file",
  "status": "success",
  "retuValue": null
}
```

错误记录示例：

```json
{
  "who": "",
  "say": "",
  "time": "2026-06-10 12:00:00",
  "status": "error",
  "error": "who 或 say 为空"
}
```

---

## 5. 门日志管理

内置函数，用于查询和清理调用记录。

### 查询门记录

`GET /windows/get_func_list` 中查找 `get_gate_log`

```python
@RegisterVPT(abbreviation="get_gate_log", document="查询门记录，支持 limit 和 offset")
def get_gate_log(limit=50, offset=0):
    ...
```

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| limit | int | 50 | 返回行数，-1 返回全部 |
| offset | int | 0 | 跳过前 N 行 |

返回 `[]` 或 JSON 对象数组。

### 清理门记录

`GET /windows/get_func_list` 中查找 `clear_gate_log`

```python
@RegisterVPT(abbreviation="clear_gate_log", document="清空所有门记录")
def clear_gate_log():
    ...
```

返回 `true` 或 `false`。

---

## 2. 注册技能

`POST /windows/load_module`

### 请求

```json
{
  "who": "string (必填) — 调用者身份",
  "say": "string (必填) — 调用说明",
  "content": "string (必填) — 纯函数块，带 @RegisterVPT 装饰器"
}
```

`content` 示例：

```python
@RegisterVPT(abbreviation="hello", document="问候函数")
def hello(name):
    return f"Hello, {name}!"
```

桥会自动补全 `from system.CommunicationAndExamples.HY_Register import RegisterVPT` 这行导入。

### 响应

| 状态码 | 条件 | 响应体 |
|--------|------|--------|
| 200 | 注册成功 | `{"ok": true, "loaded": "skill_a1b2c3"}` |
| 400 | content 为空 | `{"error": "缺少 content"}` |
| 400 | 语法错误 | `{"error": "语法错误: ..."}` |
| 500 | 文件写入失败 | `{"error": "写入技能文件失败: ..."}` |

注册后 Flask debug reloader 约 2 秒自动重启，技能生效。

---

## 3. 发现服务

### 查看路由

`GET /` → `{"UniqueRoute": "/windows/get_route_doc_list"}`

### 查看所有路由

`GET /windows/get_route_doc_list`

### 查看已注册函数

`GET /windows/get_func_list`

```json
[
  {"read_file": {"read_file": "Reads a file and returns its content."}},
  {"write_file": {"write_file": "Reads a file and returns its content."}}
]
```

---

## 4. 技能文件格式

Skills/ 目录下的 .py 文件必须遵循以下格式：

```python
from system.CommunicationAndExamples.HY_Register import RegisterVPT

@RegisterVPT(abbreviation="缩写", document="说明")
def 函数名(参数1, 参数2):
    """函数体"""
    return 结果
```

桥加载时执行 `from .模块名 import *`，`@RegisterVPT` 装饰器自动将函数注册进 VPT 注册表。
