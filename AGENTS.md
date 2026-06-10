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
        url: 桥地址 (http://<host>:1314/windows/run_func)
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
    "http://<host>:1314/windows/run_func",
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

## 技能自举

Agent 可以自己编写、注册并使用新技能，形成自举循环：

```
生成函数代码 → POST /load_module → 注册成功 → 调用使用 → 评估效果 → 迭代升级
```

### 示例：自举一个 MD5 计算技能

```python
# Step 1: Agent 生成函数代码
func_code = '''
from system.CommunicationAndExamples.HY_Register import RegisterVPT

@RegisterVPT(abbreviation="calc_md5", document="计算字符串的MD5值")
def calc_md5(text: str) -> str:
    return __import__("hashlib").md5(text.encode()).hexdigest()
'''

# Step 2: 注册
requests.post("http://localhost:1314/windows/load_module", json={
    "who": "my_agent",
    "say": "我需要计算MD5的能力",
    "content": func_code
})

# Step 3: 等待重启后使用
result = hermes_say(url, "my_agent", "计算hello的MD5", "calc_md5", text="hello")
```

### 迭代原则

- 发现技能效率低 → 重新生成实现 → 再次 load_module → 覆盖旧技能
- 无需重启服务，无需停服更新
- 整个过程 Agent 自己完成，不需要人类介入
