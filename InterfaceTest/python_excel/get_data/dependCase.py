import time
from copy import deepcopy

from jsonpath import jsonpath

from python_excel.get_data.common_param_dic import CommonParamDict
from python_excel.utils.operation_excel import OperationExcel

from  jsonpath_rw import parse

class DependCase:
    def __init__(self,**kwargs):
        self.kwargs = kwargs  #获取的用户中的参数值，不是配置文件中的参数值
        self.param_name_rownum = int(self.kwargs.get("DepParamName",0))#获取依赖的参数名所在行
        self.case_id = self.kwargs.get("DepCaseID","") #获取依赖的测试用例ID
        self.ope_excel = OperationExcel(**self.kwargs)
        self.case_value_rownum = self.ope_excel.get_row_num_for_value(self.case_id)
        self.hash_orders = self.kwargs.get("hash_orders",[]) #获取依赖的测试用例ID的参数顺序列表，用于生成salt
        self.DepGetDataForm = self.kwargs.get("DepGetDataForm","")  #依赖提取数据格式
        self.DepResList = self.kwargs.get("DepResList", [])  # 依赖参数列表


    #获取运行依赖case需要的各项请求数据
    def get_dep_data(self):
        '''
        :return: 依赖测试用例执行结果
        '''
        # 获取参数名所在行返回参数名列表
        self.kwargs["case_param_name_start"] = self.param_name_rownum  #用例参数名开始行号
        self.kwargs["case_start_rownum"] = self.case_value_rownum  # 用例参数值开始行号
        self.kwargs["hash_orders"] = self.hash_orders  # 用例参数顺序列表
        self.kwargs["DepGetDataForm"] = self.hash_orders  # 用例参数顺序列表
        cpd = CommonParamDict(**self.kwargs)
        case_data = cpd.deal_param() #[[]]
        no_request_list = cpd.param.get_param_no_request_list()
        dep_res = self.deal_dep_param(no_request_list,case_data[0]) #获取依赖测试用列响应结果




    def deal_dep_param(self,no_request_list,case_data):
        '''
        接口用例发送请求之前去除掉非接口传输参数
        :param no_request_list: 获取请求接口不传入参数列表
        :param case_data: 测试用例
        :return:
        '''
        deal_param_list = []
        no_request_dict = {}  # 存放不参数请求的参数
        req_data_dict = deepcopy(case_data)         #深拷贝参数字典
        for param  in no_request_list:
            no_request_dict[param] = req_data_dict.pop(param)
        deal_param_list.append(req_data_dict)
        deal_param_list.append(no_request_dict)
        req_s_time = time.time()
        url = no_request_dict.get("Requrl","")
        ori_res = self.interface_run.main_request(self.method_req, url, req_data_dict)
        req_e_time = time.time()
        hs = req_e_time -req_s_time
        try:
            res = ori_res.json()
        except Exception as e:
            res = ori_res.text
        print("依赖测试用执请求接口用时：{}".format(hs))
        return res


    def deal_req_res(self,res_json):

        res = jsonpath(res_json, self.DepGetDataForm)[0]
        depresvaluelist = []
        for dep_res in res:
            depresvaluelist.append(dep_res)
        dep_res_dict = dict(zip(res,self.depresvaluelist))
        return dep_res_dict

    def write_excel_value(self,dep_res):
        dep_res_dict = self.deal_req_res(dep_res)
        #self.ope_excel.
        self.ope_excel.writer_data()





