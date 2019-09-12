import time
from copy import deepcopy

from jsonpath import jsonpath

from python_excel.common.interface_run import InterfaceRun
from python_excel.get_data.common_param_dic import CommonParamDict
from python_excel.utils.operation_excel import OperationExcel

from  jsonpath_rw import parse

class DependCase:
    def __init__(self,case_dict,case_config):
        self.case_dict = case_dict  # 获取的用例中的参数值，不是配置文件中的参数值
        self.case_config = case_config  # 获取执行接口用例配置文件内容，写回值时获取正确的sheetid
        self.ope_excel_case = OperationExcel(**self.case_dict)
        self.ope_excel_config = OperationExcel(**self.case_config)
        self.interface_run = InterfaceRun()
        self.case_rownum = int(self.ope_excel_config.get_row_num_for_value(self.case_dict.get("CaseID", 0),))  # 获取测试用例参数名所在行
        self.param_name_rownum = int(self.case_dict.get("DepParamName",0))#获取依赖的参数名所在行
        self.case_id = self.case_dict.get("DepCaseID","") #获取依赖的测试用例ID
        self.case_value_rownum = self.ope_excel_case.get_row_num_for_value(self.case_id) #根据依赖caseid获取依赖测试用例执行行号
        self.case_row_value = self.ope_excel_case.get_sheet().row_values(self.param_name_rownum) #根据参数名所在行号获取整行内容
        self.hash_orders = self.case_dict.get("hash_orders",[]) #获取依赖的测试用例ID的参数顺序列表，用于生成salt
        self.DepGetDataForm = self.case_dict.get("DepGetDataForm","")  #依赖提取数据格式
        try:
            self.DepParamList = eval(case_dict.get("DepParamList",[]))
        except Exception as e :
            self.DepParamList = case_dict.get("DepParamList", [])




    #获取运行依赖case需要的各项请求数据
    def get_dep_data(self):
        '''
        :return: 依赖测试用例执行结果
        '''
        # 获取参数名所在行返回参数名列表
        self.case_dict["case_param_name_start"] = self.param_name_rownum  #用例参数名开始行号
        self.case_dict["case_start_rownum"] = self.case_value_rownum  # 用例参数值开始行号
        # self.case_dict["hash_orders"] = self.hash_orders  # 用例参数顺序列表
        # self.case_dict["DepGetDataForm"] = self.hash_orders  # 用例参数顺序列表
        cpd = CommonParamDict(**self.case_dict)
        case_data = cpd.deal_param() #[[]]
        no_request_list = cpd.param.get_param_no_request_list()
        dep_res = self.deal_dep_param(no_request_list,case_data[0]) #获取依赖测试用列响应结果
        dep_res_dict = self.deal_req_res(dep_res)
        write_flag = self.write_excel_value(dep_res)
        count = 1
        while True:
            if not write_flag:
                write_flag = self.write_excel_value(dep_res)
                count = count +1
                if count>3:
                    break
            else:
                break
        print("依赖用例执行测试的结果={}".format(dep_res))
        return dep_res_dict




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
        ori_res = self.interface_run.main_request("post", url, req_data_dict)
        req_e_time = time.time()
        hs = req_e_time -req_s_time
        try:
            res = ori_res.json()
        except Exception as e:
            res = ori_res.text
        print("依赖测试用执请求接口用时：{}".format(hs))
        return res


    def deal_req_res(self,res_json):
        '''
        将依赖测试用例执行结果按提取规则及参数处理后转为字段的形式
        :case_dict
        :param res_json: 依赖测试用例响应结果转为json形式
        :return:
        '''

        res = jsonpath(res_json, self.DepGetDataForm)[0][0]
        dep_res_dict = {}
        for dep_res in res:
            if dep_res in self.DepParamList:
                dep_res_dict[dep_res]=res.get(dep_res,"")
        return dep_res_dict

    def write_excel_value(self,dep_res):
        '''
        将依赖数据结果写回到excel表格指定的单元格中
        :param dep_res:
        :return:
        '''
        write_flag = False
        ope_excel = OperationExcel(**self.case_config)
        case_param_name_start = self.case_config.get("case_param_name_start",0) #测试用例参数名开始行
        case_row_value = ope_excel.get_sheet().row_values(case_param_name_start)
        row_num = self.case_rownum
        dep_res_dict = self.deal_req_res(dep_res)
        for update_param in dep_res_dict.keys():
            for index,update_value in enumerate(case_row_value):
                if update_param in str(update_value).split("-")[1]:
                    col_num = index
                    ope_excel.writer_data(row_num,col_num,update_value)
                    write_flag = True
        return write_flag





