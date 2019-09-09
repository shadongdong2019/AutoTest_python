from InterfaceTest.python_excel.get_data.common_param_dic import CommonParamDict
from InterfaceTest.python_excel.get_data.param_global import ParamGlobal
from InterfaceTest.python_excel.utils.operation_excel import OperationExcel
from InterfaceTest.python_excel.get_data.get_data import GetData
from InterfaceTest.python_excel.common.interface_run import InterfaceRun
from InterfaceTest.python_excel.common.deal_response_data import DealResData
from  jsonpath_rw import parse

class DependCase:
    def __init__(self,**kwargs):
        self.kwargs = kwargs  #获取的用户中的参数值，不是配置文件中的参数值
        self.param_name_rownum = int(self.kwargs.get("DepParamName",0))#获取依赖的参数名所在行
        self.case_id = self.kwargs.get("DepCaseID","") #获取依赖的测试用例ID
        self.ope_excel = OperationExcel(**self.kwargs)
        self.case_value_rownum = self.ope_excel.get_row_num_for_value(self.case_id)

    #获取运行依赖case需要的各项请求数据
    def get_dep_data(self,caseid=None):
        # 获取参数名所在行返回参数名列表
        self.kwargs["case_param_name_start"] = self.param_name_rownum  #写入用例开始行号
        self.kwargs["case_start_rownum"] = self.case_value_rownum  # 写入用例开始行号
        self.param_name_list = self.ope_excel.get_row_col_list_param_name(**self.kwargs)
        # 实例参数名处理类-根据上面的参数名列表
        self.param = ParamGlobal(self.param_name_list)
        # 获取参数英文名列表
        self.name_list = self.param.get_param_en_name_list()
        # 获取参数值列表（仅获取从开始行到结束行的数所在，如果都为0表示所有记录）
        self.name_value_list = self.ope_excel.get_row_col_list(**self.kwargs)
        cpd = CommonParamDict(**self.kwargs)
        data_http = cpd.deal_param()
        return data_http


    #运行依赖case
    def run_depend_case(self):
       res = self.run.main_request(self.req_method,self.req_url,self.req_data,self.req_headers)
       deal_res = self.deal_res_data.deal_res_data(res,3)
       return deal_res

    #按规则获取依赖case返回的依赖数据
    def get_run_dep_data(self,run_dep_res,dep_re):
        '''
        :param dep_re: 获取excel表格中依赖的数据规则
        :return:
        '''
        print(dep_re)
        dep_data_re = parse(dep_re)
        dep_data = dep_data_re.find(run_dep_res)
        res = [dep_data.value for dep_data in dep_data]
        print(res)
        return res

    def run_dep_case(self):
        ori_res = self.interface_run.main_request(self.method_req, url, req_data_dict)


