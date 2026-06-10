"""
桥辅助函数：查注册表、错误返回、随机命名。
"""
from system.CommunicationAndExamples.VariablePoolTool import VPT
from flask import jsonify
import secrets
import string


def return_json(error_content, status_code):
    """统一错误返回格式"""
    return jsonify({'error': error_content}), status_code


def lookup_abbreviation(abbreviation):
    """在 VPT.FUNC_LIST 中查找缩写对应的函数对象"""
    for entry in VPT.FUNC_LIST:
        if abbreviation in entry:
            return entry[abbreviation]
    return None


def _generate_skill_name():
    """生成随机技能模块名: skill_a1b2c3d4"""
    suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f'skill_{suffix}'
