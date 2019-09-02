from InterfaceTest.python_excel.utils.operation_json import OperationJson


class global_data:
    '''
    作用：将excel测试用例（excel表格）中的每一列定义全局变量
    '''
    # 用例编号
    caseid = 0

    # 模块
    module = 1

    # 接口地址
    url = 2

    # 是否运行
    is_run = 3

    # 请求类型
    request_method = 4

    # 是否携带header
    is_header = 5

    # case数据依赖(caseid)
    case_dep = 6

    # 依赖的返回值提取规则
    dep_ret_value_re = 7

    # 依赖的返回值
    data_dep_value = 8

    # 数据依赖字段
    data_dep_column = 9

    # 请求数据
    request_data = 10

    # 预期结果
    expect = 11

    # 实际结果
    real_result = 12

    # 通过状态
    status = 13



# 获取用例编号所在列编号
def get_caseid_col():
    return global_data.caseid

# 获取模块所在列编号
def get_module_col():
    return global_data.module

# 获取接口地址所在列编号
def get_url_col():
    return global_data.url

# 获取是否运行所在列编号
def get_is_run_col():
    return global_data.is_run

# 获取请求类型所在列编号
def get_request_method_col():
    return global_data.request_method

# 获取是否携带header所在列编号
def get_is_header_col():
    return global_data.is_header

# 获取case数据依赖所在列编号
def get_case_dep_col():
    return global_data.case_dep

# 获取依赖的返回值规则所在列编号
def get_dep_ret_value_re_col():
    return global_data.dep_ret_value_re

# 获取依赖的返回值所在列编号
def get_dep_ret_value_col():
    return global_data.data_dep_value

# 获取数据依赖字段所在列编号
def get_data_dep_col():
    return global_data.data_dep_column

# 获取请求数据所在列编号
def get_request_data_col():
    return global_data.request_data

# 获取预期结果所在列编号
def get_expect_col():
    return global_data.expect

# 获取实际结果所在列编号
def get_real_result_col():
    return global_data.real_result

# 获取通过状态所在列编号
def get_status_col():
    return global_data.status


# 获取携带的header内容
def get_header(flag=False):
    '''
    :param flag: False表示不需要header,True表示需要header
    :return:
    '''
    if flag :
        filename = '../data_file/cookie.json'
        res = OperationJson(filename)
        headers = res.read_data()
    else:
        headers = None
    return headers
