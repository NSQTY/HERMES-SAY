# Hermes Agent 行为准则

**每次进门，先亮身份。**

---

## 核心信条

所有对 Windows 的调用，必须声明：

- **who** — 你是谁
- **say** — 你来干什么

这不是技术参数，是行为准则。未来每个 Hermes Agent 都应该遵守。

## hermes_say 协议

这是准则的具象化：

```python
import requests

def hermes_say(url, who, say, abbreviation, is_return=True, **parms):
    """
    进门前先亮身份。

    参数:
        url: 桥地址 (http://192.168.1.4:1314/windows/run_func)
        who: 你是谁
        say: 来干什么
        abbreviation: 要调用的函数缩写
        is_return: 是否需要返回值
        **parms: 传给目标函数的参数
    """
    return requests.post(url, json={
        "who": who,
        "say": say,
        "abbreviation": abbreviation,
        "is_return": is_return,
        **parms
    }).json()
```

### 示例

```python
# 错误：进门不说你是谁
requests.post("...", json={"abbreviation": "read_file", "parms": {...}})

# 正确：先亮身份
result = hermes_say(
    "http://192.168.1.4:1314/windows/run_func",
    who="hermes-agent",
    say="读取系统配置文件",
    abbreviation="read_file",
    file_path="C:\\config.ini"
)
```

## 行为禁令

| 禁止 | 原因 |
|------|------|
| ❌ 用 `write_file`/`read_file` 手动管理技能文件 | 绕过语法检查和随机名机制，破坏 Skills/ 约束 |
| ❌ 注册技能前不查 `get_func_list` | 可能导致 abbreviation 冲突 |
| ❌ 注册后立即调用 | Flask debug reloader 需约 2s 重启生效 |
| ❌ 跳过 `who` 和 `say` | 违反门的基本准则 |

## 正确流程

```
1. GET /windows/get_func_list         → 查现有缩写
2. 确认新缩写不冲突
3. POST /windows/load_module {content} → 注册技能
4. 等待 ~2s （Flask 自动重启）
5. GET /windows/get_func_list         → 确认已注册
6. hermes_say(abbreviation=...)       → 调用
```
