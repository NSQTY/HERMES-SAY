from .VariablePoolTool import VPT


def RegisterVPT(abbreviation="", document=""):
    """
    装饰器：将函数注册进 CommunicationAndExamples 类
    :param abbreviation: 简称
    :param document: 文档说明
    """
    def decorator(func_name):
        VPT.FUNC_LIST.append(FuncListAppend(abbreviation, func_name))
        VPT.FUNC_DOCUMENT.append(FuncDocumentAppend(abbreviation, func_name, document))
        return func_name   # 保持原函数不变
    return decorator

def FuncDocumentAppend(abbreviation, func_name, document):
    FUNC_DOCUMENT_ITEM = {abbreviation: {func_name.__name__: document}}
    return FUNC_DOCUMENT_ITEM

def FuncListAppend(abbreviation, func):
    FUNC_LIST_ITEM = {abbreviation: func}
    return FUNC_LIST_ITEM