from flask import Flask, jsonify

def init(): # 初始化函数，用于在启动时自动创建 Skills/__init__.py（如果不存在）和导入所有技能模块。 
    # 启动时自动创建 Skills/__init__.py（如果不存在）
    import os as _os
    _init_path = _os.path.join(_os.path.dirname(__file__), 'Skills', '__init__.py')
    _os.makedirs(_os.path.dirname(_init_path), exist_ok=True)
    if not _os.path.exists(_init_path):
        with open(_init_path, 'w', encoding='utf-8') as _f:
            _f.write('')
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
