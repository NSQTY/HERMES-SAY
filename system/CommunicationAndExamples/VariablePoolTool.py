class HY_VPT:
    """目标类，用于存储注册的代码块"""
    FUNC_LIST = []      # 每个元素为 {简称: 函数}
    FUNC_DOCUMENT = []  # 每个元素为 {简称: {函数名: 文档说明}}
    
    def __init__(self):
        pass
    
VPT = HY_VPT()  # 创建目标类实例