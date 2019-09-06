from InterfaceTest.python_excel.utils.operation_excel import OperationExcel
from InterfaceTest.python_excel.get_data.get_data import GetData
from InterfaceTest.python_excel.common.interface_run import InterfaceRun
from InterfaceTest.python_excel.common.deal_response_data import DealResData
from  jsonpath_rw import parse

class DependCase:
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        case_id = self.kwargs.get("DepCaseID","")
        self.ope_excel = OperationExcel(self.kwargs)
        self.rownum = self.ope_excel.get_row_num_for_value(case_id)

    #获取运行依赖case需要的各项请求数据
    def get_dep_data(self,caseid=None):
        if caseid:
            self.caseid = caseid
        #根据caseid获取行号
        row_num = self.ope_excel.get_row_num_for_value(self.caseid)
        #获取url
        self.req_url = self.get_data.get_url(row_num)
        #获取headers
        self.req_headers = self.get_data.is_header(row_num)
        #获取请求方式
        self.req_method = self.get_data.get_req_method(row_num)
        #获取请求数据
        self.req_data = self.get_data.get_req_data(row_num)
        return self.req_url,self.req_headers,self.req_method,self.req_data

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
