# HermesSay

**Hermes Agent 通向 Windows 的门。**

Hermes Agent 运行在 WSL 里，Windows 在外面。
所有跨系统调用，必须经过这道门，附上身份（who）和意图（say）。

**出品：正安县鸿宇图文广告有限责任公司 (github.com/NSQTY)**
**许可：只供学习，禁止学习内部思想逻辑用于商业行为**

## 理念

HERMES-SAY 不只是技术工具，它代表 Agent 技能库的一个新方向。

### 传统技能库的局限

主流 Agent 技能库（OpenAI Function Calling、Anthropic Tool Use、LangChain Tools）遵循同一范式：

> 注册函数 → Agent 选择 → 无条件执行

这假设 Agent 是可信的。当技能涉及文件读写、系统命令、网络请求时，缺乏：

- **调用前审计** — 不知道 Agent "为什么"调这个技能
- **调用后追溯** — 没有内置的不可否认日志

### HERMES-SAY 三原则

| 原则 | 含义 |
|------|------|
| **声明式调用** | 每次调用必须声明 who（身份）和 say（意图）。技能执行不是函数调用，而是带声明的会话 |
| **动态热加载** | 通过 `/windows/load_module`，Agent 可在运行时注入新技能代码，形成自举循环 |
| **可审计门卫** | 每次调用生成不可变日志（who, say, time, funcname），可通过 API 查询和清理 |

### 与传统对比

| 特性 | 传统技能库 | HERMES-SAY |
|------|-----------|-------------|
| 调用方式 | 无上下文函数调用 | 携带 who+say 的声明式请求 |
| 技能来源 | 预注册 | 可动态注册 + 自举 |
| 执行决策 | 无条件执行 | 可基于 say 做策略裁决 |
| 可追溯性 | 无或依赖外部日志 | 内置不可否认审计日志 |
| 安全模型 | 依赖 Agent 可信 | 假设 Agent 不可信，依赖契约和审计 |

### 架构

```
WSL (你的 Agent)
  │  POST /windows/run_func
  │  POST /windows/load_module
  ▼
HERMES-SAY (基座)
  │  - 注册的技能库
  │  - 门卫日志
  │  - 动态加载器
  ▼
Windows 系统资源 (文件、数据库、进程等)
```

Agent 只做三件事：**理解意图 → 构造请求（带上 who 和 say） → 处理结果**。底层操作全部由 HERMES-SAY 封装。

### 一句话

这个项目提醒社区：**当 Agent 越来越强大时，我们需要的不仅是更多技能，还需要一套与技能同等重要的"技能调用伦理"基础设施。**

---

## 快速体验

```bash
pip install flask
python app.py
# → http://localhost:1314
```

## 快速体验

从 WSL 侧调用 Windows 上的函数：

```python
import requests

r = requests.post("http://localhost:1314/windows/run_func", json={
    "who": "你",
    "say": "探索门的能力",
    "abbreviation": "read_file",
    "parms": {"file_path": "C:\\config.ini"},
    "is_return": True
})
print(r.json()["result"])
```

## 注册新技能

把函数块发给桥，桥自动写入 `Skills/` 并触发重启生效：

```bash
curl -X POST http://localhost:1314/windows/load_module \
  -H "Content-Type: application/json" \
  -d '{"content": "@RegisterVPT(abbreviation=\"hello\", document=\"问候\")\ndef hello(name):\n    return f\"Hello, {name}!\"}'
```

等待约 2 秒 Flask 自动重启，然后就能调用了。

## 项目结构

```
HermesSay/
├── app.py                         # 桥入口（~29行）
├── README.md                      # 本文档
├── AGENTS.md                      # Hermes Agent 行为准则
├── CONTRACT.md                    # 协议契约
│
├── Skills/                        # 运行时生成，不提交
│   └── __init__.py                # 启动时自动创建
│
└── system/
    ├── CommunicationAndExamples/
    │   ├── HY_Register.py         # @RegisterVPT 装饰器
    │   ├── VariablePoolTool.py    # VPT 注册表
    │   └── FunctionExecution.py   # 函数执行器
    └── SystemSkill/
        ├── config.py              # PORT, DEBUG, HOST
        ├── bridge_utils.py        # 桥辅助函数
        ├── routes.py              # 4 个业务路由
        ├── RAW.py                 # read_file, write_file
        ├── gate_log.py            # 门日志（get_gate_log, clear_gate_log）
```

## 路由一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 入口指引 |
| GET | `/windows/get_route_doc_list` | 查看所有路由 |
| GET | `/windows/get_func_list` | 查看所有已注册函数 |
| POST | `/windows/run_func` | 执行函数 |
| POST | `/windows/load_module` | 注册新技能 |

详细协议见 [CONTRACT.md](CONTRACT.md)。
