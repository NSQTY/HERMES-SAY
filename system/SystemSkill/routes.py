"""
桥业务路由。通过 register_routes(app) 注入 Flask 实例。
"""
from system.SystemSkill import RAW
from system.SystemSkill import gate_log
from flask import jsonify, request
from system.CommunicationAndExamples.VariablePoolTool import VPT
from system.CommunicationAndExamples.FunctionExecution import execute_function
from system.SystemSkill.bridge_utils import return_json, lookup_abbreviation, _generate_skill_name
from datetime import datetime
import os


def register_routes(app):

    # 初始化门日志
    gate_log.init_gate_log(app.root_path)

    @app.route('/windows/get_route_doc_list', methods=['GET'])
    def windows_get_route_doc_list():
        """返回路由文档列表"""
        return jsonify(get_route_doc_list(app))

    @app.route('/windows/get_func_list', methods=['GET'])
    def windows_get_func_list():
        """返回已注册函数文档列表"""
        return jsonify(VPT.FUNC_DOCUMENT)

    @app.route('/windows/run_func', methods=['POST'])
    def windows_run_func():
        """
        执行已注册的函数。

        请求体: {who, say, abbreviation, is_return}

        检查顺序：
            1. who 或 say 为空 → 400
            2. abbreviation 未注册 → 404
            3. 执行 → 门记录 → 按 is_return 返回
        """
        if request.method != 'POST':
            return return_json('NOT IS POST', 400)

        data = request.get_json()
        if not data:
            return return_json('请求体为空', 400)

        who = data.get('who', '').strip()
        say = data.get('say', '').strip()
        abbreviation = data.get('abbreviation', '').strip()
        parms = data.get('parms', {})
        is_return = data.get('is_return', False)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 检查 1: who 或 say 为空
        if not who or not say:
            gate_log.log_to_file({
                'who': who, 'say': say,
                'time': now, 'status': 'error',
                'error': 'who 或 say 为空'
            })
            return return_json('缺少参数：who 或 say 不能为空', 400)

        # 检查 2: 简称未注册
        func = lookup_abbreviation(abbreviation)
        if func is None:
            gate_log.log_to_file({
                'who': who, 'say': say,
                'time': now, 'abbreviation': abbreviation,
                'status': 'error', 'error': '简称未注册'
            })
            return return_json(f'简称未注册: {abbreviation}', 404)

        # 执行（who/say 不进函数，parms 展开为 **kwargs 传入）
        func_name = func.__name__
        execute_result = execute_function(func, **parms)

        # 门记录
        gate_log_entry = {
            'who': who,
            'say': say,
            'time': now,
            'funcname': func_name,
            'abbreviation': abbreviation,
            'status': 'success',
            'retuValue': execute_result
        }
        gate_log.log_to_file(gate_log_entry)
        print(f"[GATE] {gate_log_entry}")

        # 按 is_return 决定返回值
        if is_return:
            return jsonify({'result': execute_result, 'gate': gate_log_entry})
        else:
            return jsonify({'message': '执行完成', 'gate': gate_log_entry})

    @app.route('/windows/load_module', methods=['POST'])
    def windows_load_module():
        """
        注册新技能。

        接收纯函数块（content），自动补全 RegisterVPT 的 import。
        写入 Skills/ 并追加到 __init__.py。
        Flask debug reloader 检测到变化后自动重启，新技能生效。

        请求体: {who, say, content}
        """
        data = request.get_json()
        if not data:
            return return_json('请求体为空', 400)

        content = data.get('content', '').strip()
        if not content:
            return return_json('缺少 content', 400)

        # 自动补全 RegisterVPT 的 import
        import_line = 'from system.CommunicationAndExamples.HY_Register import RegisterVPT'
        if import_line not in content:
            content = f'{import_line}\n\n{content}'

        # 语法检查，防止坏文件导致重启后桥挂掉
        try:
            compile(content + '\n', '<skill>', 'exec')
        except SyntaxError as e:
            return return_json(f'语法错误: {e}', 400)

        # 生成随机文件名
        name = _generate_skill_name()
        skill_path = os.path.join(app.root_path, 'Skills', f'{name}.py')
        init_path = os.path.join(app.root_path, 'Skills', '__init__.py')

        # 写入技能文件
        try:
            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except IOError as e:
            return return_json(f'写入技能文件失败: {e}', 500)

        # 追加到 __init__.py
        try:
            with open(init_path, 'a', encoding='utf-8') as f:
                f.write(f'\nfrom .{name} import *')
        except IOError as e:
            return return_json(f'写入 __init__.py 失败: {e}', 500)

        return jsonify({'ok': True, 'loaded': name})


def get_route_doc_list(app):
    """获取当前 Flask 应用的所有路由及其文档信息。"""
    route_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        view_func = app.view_functions.get(rule.endpoint)
        doc = view_func.__doc__.strip() if view_func and view_func.__doc__ else ""
        route_list.append({
            'route': rule.rule,
            'methods': list(rule.methods),
            'endpoint': rule.endpoint,
            'doc': doc
        })
    return route_list
