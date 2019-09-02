import sys
sys.path.append('/home/ma/PycharmProjects/InterfaceTest')
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
# from python_excel.utils.send_email_fj import SendEmailFJ
mylog = logging.getLogger(__file__)
filename = "../data_file/case_data_ysc.xlsx"
sheetid_http = 7
sheetid_https = 8


#data_dl = TsaParamDict(filename,sheetid_http).deal_download_param()
data_download_http = TsaParamDict(filename,sheetid_http).deal_param(req_type="download",start=0,end=0)
data_download_https = TsaParamDict(filename,sheetid_https).deal_param(req_type="download",start=0,end=0)

@ddt.ddt
class CaseRun(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.title = "版权服务2.0下载接口自动化测试报告"
        #self.url = "http://ipp20timestamp.tsa.cn/v1/api/confirm/downloadOpusCertificate" #下载接口
        self.url ="http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        self.count = 0
    @classmethod
    def tearDownClass(self):
        pass
    def setUp(self):
        self.interface_run = InterfaceRun()
        self.deal_res_data = DealResData()
        self.op_excel = OperationExcel(filename,sheetid_http)
        self.case_d = CaseDetail("../data_file/TestCase_zh.xlsx")
        self.method_req = "post"
        self.tsa_param = TsaParamDict()
        self.crr = CmpReqRes()
    def tearDown(self):
        pass

    @ddt.data(*data_download_http)
    def test_download_http(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        self.url = "http://39.107.66.190:9999/v2/api/confirm/downloadOpusCertificate"
        self.url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"

        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        is_run = req_data_dict.pop("IsRun") #用例是否运行
        result = req_data_dict.pop("result")#申请成功返回结果
        is_pass_ex = req_data_dict.pop("is_pass")  # 申请成功返回结果

        pp.pprint("下载接口用例执行详情如下：")
        pp.pprint("下载接口执行测试用例编号：[{}]".format(caseid))
        pp.pprint("下载接口测试目的：{}".format(case_target))
        pp.pprint("下载接口用例描述：{}".format(case_des))
        pp.pprint("下载接口地址：{}".format(self.url))

        pp.pprint("下载接口预期接口返回值={}".format(expect))
        start = time.time()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.time()
        hs = end -start
        pp.pprint("下载接口请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        self.op_excel.writer_data(row_num,9,ori_res.text) #写入实际响应结果

        pp.pprint("下载接口响应结果={}".format(res))
        pp.pprint("下载接口传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        start = time.time()
        kargs = {"expect": expect,
                 "res": ori_res,
                 "req": req_data_dict,
                 "partnerID": req_data_dict.get("partnerID"),
                 "partnerKey": req_data_dict.get("partnerKey"),
                 "req_type": "download"
                 }
        is_pass, serialNo = self.crr.verify_is_pass(**kargs)
        # count = 0
        # while not is_pass and serialNo:
        #     is_pass, serialNo = self.crr.verify_is_pass(**kargs)
        #     count += 1
        #     if count > 60:
        #         break
        # end = time.time()
        hs = end - start
        pp.pprint("下载接口验证耗时：{}".format(hs))
        if is_pass:
            self.op_excel.writer_data(row_num, 10, "pass")  # 写入用例是否通过
        else:
            self.op_excel.writer_data(row_num, 10, "fail")  # 写入用例是否通过

        self.assertTrue(is_pass,"测试用例执行未通过")

    @ddt.data(*data_download_https)
    def test_download_https(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        self.url = "http://39.107.66.190:9999/v2/api/confirm/downloadOpusCertificate"
        self.url = "https://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        self.op_excel = OperationExcel(filename, sheetid_https)
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        is_run = req_data_dict.pop("IsRun") #用例是否运行
        result = req_data_dict.pop("result")#申请成功返回结果
        is_pass_ex = req_data_dict.pop("is_pass")  # 申请成功返回结果


        pp.pprint("下载接口用例执行详情如下：")
        pp.pprint("下载接口执行测试用例编号：[{}]".format(caseid))
        pp.pprint("下载接口测试目的：{}".format(case_target))
        pp.pprint("下载接口用例描述：{}".format(case_des))
        pp.pprint("下载接口地址：{}".format(self.url))

        pp.pprint("下载接口预期接口返回值={}".format(expect))
        start = time.time()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.time()
        hs = end -start
        pp.pprint("下载接口请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        self.op_excel.writer_data(row_num,9,ori_res.text) #写入实际响应结果

        pp.pprint("下载接口响应结果={}".format(res))
        pp.pprint("下载接口传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        start = time.time()
        kargs = {"expect": expect,
                 "res": ori_res,
                 "req": req_data_dict,
                 "partnerID": req_data_dict.get("partnerID"),
                 "partnerKey": req_data_dict.get("partnerKey"),
                 "req_type": "download"
                 }
        is_pass, serialNo = self.crr.verify_is_pass(**kargs)
        count = 0
        while not is_pass and serialNo:
            is_pass, serialNo = self.crr.verify_is_pass(**kargs)
            count += 1
            if count > 60:
                break
        end = time.time()
        hs = end - start
        pp.pprint("下载接口验证耗时：{}".format(hs))
        if is_pass:
            self.op_excel.writer_data(row_num, 10, "pass")  # 写入用例是否通过
        else:
            self.op_excel.writer_data(row_num, 10, "fail")  # 写入用例是否通过

        self.assertTrue(is_pass,"测试用例执行未通过")
        self.assertTrue(is_pass,"测试用例执行未通过")

if __name__ == "__main__":
    cr =CaseRun()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    run_file = sys.argv[0]
    run_file_name = os.path.basename(os.path.splitext(run_file)[0])
    rand_str = ''.join(random.sample((string.ascii_letters + string.digits), 5))
    report_name = run_file_name+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.html'
    data_str = datetime.datetime.now().strftime('%Y%m%d')
    report_path = os.path.join("../report/{}_zs/{}".format(data_str,report_name))
    path = os.path.join("../report/{}_zs/".format(data_str))
    if not os.path.exists(path):
        os.makedirs(path)
    fp = open(report_path,'wb')
    suite = unittest.TestLoader().loadTestsFromTestCase(CaseRun)
    title = '版权服务2.0生产环境接口测试报告（http/https）'
    description = "下载接口-证书下载的合法数据与非法数据校验"
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=title,description=description,verbosity=2)
    runner.run(suite)
    #cr.send_email_fj.send_email_fj(title, report_path)
