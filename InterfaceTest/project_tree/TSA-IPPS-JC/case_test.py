import sys
#sys.path.append('/home/ma/PycharmProjects/InterfaceTest/')
#/home/ma/PycharmProjects/InterfaceTest/
import datetime
import random
import string
from InterfaceTest.python_excel import log
import os
import unittest
import ddt
from InterfaceTest.python_excel.common.interface_run import InterfaceRun
from InterfaceTest.python_excel.common.deal_response_data import DealResData
from InterfaceTest.python_excel.get_data.tsa_param_dic import TsaParamDict
from InterfaceTest.python_excel.HTMLTestRunner import HTMLTestRunner
from InterfaceTest.python_excel.get_data.case_mes import CaseDetail
from copy import deepcopy
from InterfaceTest.python_excel.utils.operation_excel import OperationExcel
import json
import  pprint
from InterfaceTest.python_excel.common.cmp_res_req import CmpReqRes
from jsonpath import jsonpath
from InterfaceTest.python_excel.get_data.case_error import CaseError
import time
import logging
from InterfaceTest.python_excel.utils.operation_cfg import OperationCFG
from InterfaceTest.python_excel.get_data.common_param_dic import CommonParamDict
mylog = logging.getLogger(__file__)
ope_cfg = OperationCFG("/home/ma/PycharmProjects/AutoTest_python/InterfaceTest/project_tree/TSA-IPPS-JC/config/caseRun.cfg","my_case_file")
option_dict = ope_cfg.get_config_dict()
filename = option_dict["case_filepath"]
sheetid_http = int(option_dict["case_sheetid"])
start= int(option_dict["case_start_rownum"])
end= int(option_dict["case_end_rownum"])

cpd = CommonParamDict(**option_dict)
data_http = cpd.deal_param()
#data_https = TsaParamDict(filename,sheetid_https).deal_param(start=4,end=5)

@ddt.ddt
class CaseRun(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass
    @classmethod
    def tearDownClass(self):
        pass
    def setUp(self):
        self.interface_run = InterfaceRun()
        self.deal_res_data = DealResData()
        self.op_excel = OperationExcel(filename,sheetid_http)
        self.method_req = "post"
        self.tsa_param = TsaParamDict()
        self.crr = CmpReqRes()
    def tearDown(self):
        pass

    @ddt.data(*data_http)
    def test_apply_http(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        #获取请求地址：
        url = option_dict["url"]
        #获取请求接口不传入参数列表
        no_request_list = cpd.param.get_param_no_request_list()
        #深拷贝参数字典
        no_request_dict = {}
        req_data_dict = deepcopy(data_dict)
        for param  in no_request_list:
            no_request_dict[param] = req_data_dict.pop(param)
        ori_res = self.interface_run.main_request(self.method_req, url, req_data_dict)
        try:
            res = ori_res.json()
        except Exception as e:
            res = ori_res.text
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint("监测接口用例执行详情如下：")
        pp.pprint("监测接口执行测试用例编号：[{}]".format(no_request_dict["CaseID"]))
        pp.pprint("监测接口测试目的：{}".format(no_request_dict["TestTarget"]))
        pp.pprint("监测接口用例描述：{}".format(no_request_dict["CaseDesc"]))
        pp.pprint("监测接口地址：{}".format(url))
        pp.pprint("监测接口预期接口返回值={}".format(no_request_dict["ExpectValue"]))
        pp.pprint("监测接口预期回调状态值={}".format(no_request_dict["ExpCallbackFlag"]))
        pp.pprint("监测接口响应结果={}".format(res))


        kargs = {"expect":no_request_dict["ExpectValue"],
                 "res":ori_res,
                 "req":req_data_dict,
                 "partnerID":req_data_dict.get("partnerID"),
                 "partnerKey":req_data_dict.get("partnerKey"),
                 "expCallbackFlag":no_request_dict["ExpCallbackFlag"],
                 "no_verify_data_list":option_dict.get("no_verify_data_list",None)
        }
        start = time.time()
        time.sleep(1)
        verify_res = self.crr.verify_is_pass(**kargs)
        end =time.time()
        hs = end -start
        pp.pprint("监测接口响应结果验证耗时：{}".format(hs))
        pp.pprint("数据库数据验证结果：{}".format(verify_res.get("database_str")))
        if verify_res.get("database_str",None):
            pp.pprint("数据库回调结果标识验证结果：{}".format(verify_res.get("database_str")))
        pp.pprint("请求参数={}".format(json.dumps(req_data_dict, ensure_ascii=False)))
        self.assertTrue(verify_res.get("flag",None),"测试用例执行未通过")

if __name__ == "__main__":
    reportpath = option_dict["report_path"]
    cr =CaseRun()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    run_file = sys.argv[0]
    run_file_name = os.path.basename(os.path.splitext(run_file)[0])
    rand_str = ''.join(random.sample((string.ascii_letters + string.digits), 5))
    report_name = run_file_name+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.html'
    data_str = datetime.datetime.now().strftime('%Y%m%d')
    report_path = os.path.join("{}{}_zs/".format(reportpath,data_str),report_name)
    path = os.path.join("{}{}_zs/".format(reportpath,data_str))
    if not os.path.exists(path):
        os.makedirs(path)
    fp = open(report_path,'wb')
    suite = unittest.TestLoader().loadTestsFromTestCase(CaseRun)
    title = '版权服务2.0生产环境接口测试报告（https）'
    description = "监测接口-主流程测试用例-主要验证所有参数合法参数监测成功及必填参数非法数据监测失败"
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=title,description=description,verbosity=2)
    runner.run(suite)
