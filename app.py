from flask import Flask, jsonify

def init():
    import os as _os
    _root = _os.path.dirname(__file__)
    
    # 确保 Skills/ 存在
    _init_path = _os.path.join(_root, 'Skills', '__init__.py')
    _os.makedirs(_os.path.dirname(_init_path), exist_ok=True)
    if not _os.path.exists(_init_path):
        with open(_init_path, 'w', encoding='utf-8') as _f:
            _f.write('')
    
    # 尝试拉取社区技能包（静默失败，不阻塞启动）
    _skills_git = _os.path.join(_root, 'Skills', '.git')
    _skill_repo = _os.environ.get('SKILL_REPO', '')
    if _skill_repo and not _os.path.exists(_skills_git):
        try:
            import subprocess
            subprocess.run(
                ['git', 'clone', _skill_repo, _os.path.join(_root, 'Skills')],
                capture_output=True, timeout=15
            )
        except Exception:
            pass  # 网络不可达等，不阻塞
    elif _skill_repo and _os.path.exists(_skills_git):
        try:
            import subprocess
            subprocess.run(
                ['git', '-C', _os.path.join(_root, 'Skills'), 'pull'],
                capture_output=True, timeout=15
            )
        except Exception:
            pass

    return Flask(__name__)

app = init()

from system.SystemSkill.config import PORT, DEBUG, HOST,ROOT_DIR
from system.SystemSkill.routes import register_routes

register_routes(app)


@app.route('/')
def index():
    """根路径：返回入口路由提示"""
    return jsonify(ROOT_DIR,{"PORT":PORT})


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
