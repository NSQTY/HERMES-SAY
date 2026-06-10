# HermesSay

**Hermes Agent 通向 Windows 的门。**

Hermes Agent 运行在 WSL 里，Windows 在外面。
所有跨系统调用，必须经过这道门，附上身份（who）和意图（say）。

**出品：正安县鸿宇图文广告有限责任公司 (github.com/NSQTY)**
**许可：只供学习，禁止学习内部思想逻辑用于商业行为**

---

## 一句话启动

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
    "parms": {"file_path": "C:\\Windows\\win.ini"},
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
