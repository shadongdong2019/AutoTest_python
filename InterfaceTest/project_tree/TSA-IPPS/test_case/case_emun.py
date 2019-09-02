import sys
sys.path.append('/home/ma/PycharmProjects/InterfaceTest/')
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
mylog = logging.getLogger(__file__)
filename = "../data_file/case_data_ysc.xlsx"
sheetid = 1

data = TsaParamDict(filename,1).deal_enum_param(0,start=0,end=1)

@ddt.ddt
class CaseRun(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.itle = '版权服务2.0申请接口测试报告'
        self.description = ""
        self.url = "http://39.107.66.190:9999/v2/api/confirm/opusConfirm" #申请接口  ipp20timestamp.tsa.cn
        self.url = "https://ipp.tsa.cn/v2/api/confirm/opusConfirm"
        self.count = 0
    @classmethod
    def tearDownClass(self):
        pass
    def setUp(self):
        self.interface_run = InterfaceRun()
        self.deal_res_data = DealResData()
        self.op_excel = OperationExcel(filename,sheetid)
        self.method_req = "post"
        self.tsa_param = TsaParamDict()
        self.crr = CmpReqRes()
    def tearDown(self):
        pass

    @ddt.data(*data)
    def test_apply_enum_http(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''

        self.url = "http://ipp.tsa.cn/v2/api/confirm/opusConfirm"
        download_url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        data_str = datetime.datetime.now().strftime('%Y%m%d')
        download_file = '{}_emun_http'.format(data_str)
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_run = req_data_dict.pop("IsRun")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("申请接口地址：{}".format(self.url))
        pp.pprint("申请接口预期接口返回值={}".format(expect))
        pp.pprint("申请接口预期回调状态值={}".format(expCallbackFlag))

        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        try:
            res_serialNo = jsonpath(ori_res.json(), "$..serialNo")[0]
        except Exception as e:
            res_serialNo = ""

        pp.pprint("响应结果={}".format(res))
        start = time.clock()
        kargs = {"expect":expect,
                 "res":ori_res,
                 "req":req_data_dict,
                 "partnerID":req_data_dict.get("partnerID"),
                 "partnerKey":req_data_dict.get("partnerKey"),
                 "expCallbackFlag":expCallbackFlag,  #expect, res,req,,
                 "download_url":download_url,
                 "download_file":download_file
        }
        is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data = self.crr.verify_is_pass(**kargs)
        count = 0
        while not is_pass and serialNo:
            is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data = self.crr.verify_is_pass(**kargs)

            count +=1
            if count >10:
                break
        end =time.clock()
        hs = end -start
        pp.pprint("验证耗时：{}".format(hs))

        if database_str:
            pp.pprint(database_str) #数据库值对比结果文字信息
        if database_str_hd:
            pp.pprint(database_str_hd)  # 数据库回调值对比结果文字信息
        if download_req_url:
            pp.pprint(download_req_url)  # 下载接口请求地址
        if download_req_data:
            pp.pprint(download_req_data)  # 下载接口请求数据
        if download_res:
            pp.pprint(download_res)  # 下载接口响应数据，不包含文件流data

        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("申请接口传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")

    @ddt.data(*data)
    def etest_apply_enum_https(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''

        self.url = "https://ipp.tsa.cn/v2/api/confirm/opusConfirm"
        download_url = "https://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        data_str = datetime.datetime.now().strftime('%Y%m%d')
        download_file = '{}_emun_https'.format(data_str)
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_run = req_data_dict.pop("IsRun")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("申请接口地址：{}".format(self.url))
        pp.pprint("申请接口预期接口返回值={}".format(expect))
        pp.pprint("申请接口预期回调状态值={}".format(expCallbackFlag))

        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        try:
            res_serialNo = jsonpath(ori_res.json(), "$..serialNo")[0]
        except Exception as e:
            res_serialNo = ""

        pp.pprint("响应结果={}".format(res))
        start = time.clock()
        kargs = {"expect":expect,
                 "res":ori_res,
                 "req":req_data_dict,
                 "partnerID":req_data_dict.get("partnerID"),
                 "partnerKey":req_data_dict.get("partnerKey"),
                 "expCallbackFlag":expCallbackFlag,  #expect, res,req,,
                 "download_url":download_url,
                 "download_file":download_file
        }
        is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data = self.crr.verify_is_pass(**kargs)
        count = 0
        while not is_pass and serialNo:
            is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data = self.crr.verify_is_pass(**kargs)

            count +=1
            if count >10:
                break
        end =time.clock()
        hs = end -start
        pp.pprint("验证耗时：{}".format(hs))

        if database_str:
            pp.pprint(database_str) #数据库值对比结果文字信息
        if database_str_hd:
            pp.pprint(database_str_hd)  # 数据库回调值对比结果文字信息
        if download_req_url:
            pp.pprint(download_req_url)  # 下载接口请求地址
        if download_req_data:
            pp.pprint(download_req_data)  # 下载接口请求数据
        if download_res:
            pp.pprint(download_res)  # 下载接口响应数据，不包含文件流data

        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")

        pp.pprint("申请接口传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")


if __name__ == "__main__":
    cr =CaseRun()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    run_file = sys.argv[0]
    run_file_name = os.path.basename(os.path.splitext(run_file)[0])
    rand_str = ''.join(random.sample((string.ascii_letters + string.digits), 5))
    report_name = run_file_name+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.html'
    data_str = datetime.datetime.now().strftime('%Y%m%d')
    report_path = os.path.join("../report/{}_zs/".format(data_str),report_name)
    path = os.path.join("../report/{}_zs/".format(data_str))
    if not os.path.exists(path):
        os.makedirs(path)
    fp = open(report_path,'wb')
    suite = unittest.TestLoader().loadTestsFromTestCase(CaseRun)
    title = '版权服务2.0生产环境接口测试报告（http/https）'
    description = "申请接口-枚举类型数据遍历-验证正确性"
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=title,description=description,verbosity=2)
    runner.run(suite)