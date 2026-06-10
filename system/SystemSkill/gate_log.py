"""
门日志系统：记录所有桥调用，支持查询和清理。
"""
import os
import json
from system.CommunicationAndExamples.HY_Register import RegisterVPT

LOG_PATH = None


def init_gate_log(app_root):
    """初始化日志文件路径，启动时调用。"""
    global LOG_PATH
    LOG_PATH = os.path.join(app_root, 'gate.log')
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            pass


def log_to_file(entry):
    """追加一行 JSON 到日志文件。"""
    if LOG_PATH is None:
        return
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    except IOError:
        pass  # 日志写入失败不影响桥运行


@RegisterVPT(abbreviation='get_gate_log', document='查询门记录，支持 limit 和 offset')
def get_gate_log(limit=50, offset=0):
    """
    读取门日志文件。

    参数:
        limit: 返回行数（默认 50，-1 返回全部）
        offset: 跳过前 N 行（默认 0）
    """
    if LOG_PATH is None or not os.path.exists(LOG_PATH):
        return []

    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    if offset >= total:
        return []

    end = total if limit == -1 else min(offset + limit, total)
    batch = lines[offset:end]

    return [json.loads(line) for line in batch]


@RegisterVPT(abbreviation='clear_gate_log', document='清空所有门记录')
def clear_gate_log():
    """清空日志文件。"""
    if LOG_PATH is None:
        return False
    try:
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            pass
        return True
    except IOError:
        return False
