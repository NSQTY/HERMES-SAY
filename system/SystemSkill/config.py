"""
桥配置参数。
"""
PORT = 1314
DEBUG = True
HOST = '0.0.0.0'
ROOT_DIR = {"UniqueRoute": "/windows/get_route_doc_list"}

# 社区技能包仓库（环境变量覆盖）
# 设置后桥启动时自动 clone/pull，不设置则只加载本地技能
import os
SKILL_REPO = os.environ.get('SKILL_REPO', 'https://github.com/NSQTY/HERMES-SAY-SKILL.git')

from Skills import *
