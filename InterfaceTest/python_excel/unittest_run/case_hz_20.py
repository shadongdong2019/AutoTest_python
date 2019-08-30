import sys
sys.path.append('/home/ma/PycharmProjects/InterfaceTest/')
#/home/ma/PycharmProjects/InterfaceTest/
import datetime
import random
import string
from python_excel import log
import os
import unittest
import ddt
from python_excel.common.interface_run import InterfaceRun
from python_excel.common.deal_response_data import DealResData
from python_excel.get_data.tsa_param_dic import TsaParamDict
from python_excel.HTMLTestRunner import HTMLTestRunner
from python_excel.get_data.case_mes import CaseDetail
from copy import deepcopy
from python_excel.utils.operation_excel import OperationExcel
import json
import  pprint
from python_excel.common.cmp_res_req import CmpReqRes
from jsonpath import jsonpath
from python_excel.get_data.case_error import CaseError
import time
import logging
mylog = logging.getLogger(__file__)
filename = "../data_file/case_data_ysc.xlsx"
sheetid_http = 3
sheetid_https = 4

data_http = TsaParamDict(filename,sheetid_http).deal_param(start=0,end=0)
data_https = TsaParamDict(filename,sheetid_https).deal_param(start=0,end=0)

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
        self.op_excel = OperationExcel(filename,sheetid_http)
        self.method_req = "post"
        self.tsa_param = TsaParamDict()
        self.crr = CmpReqRes()
    def tearDown(self):
        pass

    @ddt.data(*data_http)
    def test_apply_hz_http(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        self.op_excel = OperationExcel(filename, sheetid_http)
        self.url = "http://ipp.tsa.cn/v2/api/confirm/opusConfirm"
        download_url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        data_str = datetime.datetime.now().strftime('%Y%m%d')
        download_file = '{}_hz_http'.format(data_str)
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
        is_apply = req_data_dict.pop("is_apply") #是否确权成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("确权接口用例执行详情如下：")
        pp.pprint("确权接口执行测试用例编号：[{}]".format(caseid))
        pp.pprint("确权接口测试目的：{}".format(case_target))
        pp.pprint("确权接口用例描述：{}".format(case_des))
        pp.pprint("确权接口地址：{}".format(self.url))
        pp.pprint("确权接口预期接口返回值={}".format(expect))
        pp.pprint("确权接口预期回调状态值={}".format(expCallbackFlag))

        start = time.time()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.time()
        hs = end -start
        pp.pprint("确权接口请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        try:
            res_serialNo = jsonpath(ori_res.json(), "$..serialNo")[0]
        except Exception as e:
            res_serialNo = ""
        self.op_excel.writer_data(row_num, 64, res_serialNo)  # 写入实际响应结果中的serialNo
        self.op_excel.writer_data(row_num,65,ori_res.text) #写入实际响应结果全部
        pp.pprint("确权接口响应结果={}".format(res))
        kargs = {"expect":expect,
                 "res":ori_res,
                 "req":req_data_dict,
                 "partnerID":req_data_dict.get("partnerID"),
                 "partnerKey":req_data_dict.get("partnerKey"),
                 "expCallbackFlag":expCallbackFlag,  #expect, res,req,,
                 "download_url":download_url,
                 "download_file":download_file
        }
        start = time.time()
        is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data,cmp_req_res,download_case,tsa_file = self.crr.verify_is_pass(**kargs)
        count = 1
        while not is_pass and serialNo:
            if download_case:
                kargs["download_case"]=download_case
                kargs["download_req_url"] = download_req_url
                kargs["download_req_data"] = download_req_data
                kargs["download_res"] = download_res
            if cmp_req_res:
                kargs["cmp_req_res"] = cmp_req_res
            if tsa_file:
                kargs["tsa_file"] = tsa_file
            is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data,cmp_req_res,download_case,tsa_file = self.crr.verify_is_pass(**kargs)
            count +=1
            if count >60:
                break
        end =time.time()
        hs = end -start
        pp.pprint("确权接口响应结果验证耗时：{}".format(hs))

        if  is_pass and serialNo:
            pp.pprint("因证书为异步生成，所以此用列需等待生成后进行下载，需循环验证，共验证<{}>次,找到PDF证书".format(count))

        if database_str:
            pp.pprint("确权接口请求数据与数据库存入值校验结果：{}".format(database_str)) #数据库值对比结果文字信息
        if database_str_hd:
            pp.pprint("确权接口预期回调接口值与数据库回调值校验结果：{}".format(database_str_hd))  # 数据库回调值对比结果文字信息

        pp.pprint("------------------------------------------------------------------------------------------")
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示用例中的文件地址")

        pp.pprint("确权接口传入参数={}".format(json.dumps(req_data_dict, ensure_ascii=False)))


        pp.pprint("------------------------------------------------------------------------------------------")

        if download_req_url:
            pp.pprint("下载接口请求地址={}".format(download_req_url))  # 下载接口请求地址
        if download_req_data:
            pp.pprint("下载接口请求数据={}".format(download_req_data))  # 下载接口请求数据
        if download_res:
            pp.pprint("下载接口响应数据={}".format(download_res))  # 下载接口响应数据，不包含文件流data
            pp.pprint("注：下载接口响应数据中因文件流data参数过大，所以不写入测试报告，以防止测试报告过大")

        if is_pass and serialNo:
            self.op_excel.writer_data(row_num, 66, "pass")  # 写入是否确权成功
        else:
            self.op_excel.writer_data(row_num, 66, "fail")  # 写入是否确权成功

        #self.op_excel.writer_data(row_num, 67, download_res_data)  # 写入下载接口返回信息

        if download_res_data and download_res_data.get("data",None):
            self.op_excel.writer_data(row_num,68,"pass") #写入是否下载成功
        else:
            self.op_excel.writer_data(row_num, 68, "fail")  # 写入是否下载成功

        if is_pass:
            self.op_excel.writer_data(row_num, 69, "通过")  # 写入用例执行结果
        else:
            self.op_excel.writer_data(row_num, 69, "未通过")  # 写入用例执行结果

        pp.pprint("------------------------------------------------------------------------------------------")
        if is_pass:
            pp.pprint("测试用例执行通过")
        self.assertTrue(is_pass,"测试用例执行未通过")


    @ddt.data(*data_https)
    def test_apply_hz_https(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        self.op_excel = OperationExcel(filename, sheetid_https)
        self.url = "https://ipp.tsa.cn/v2/api/confirm/opusConfirm"
        download_url = "https://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        data_str = datetime.datetime.now().strftime('%Y%m%d')
        download_file = '{}_hz_https'.format(data_str)
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
        is_apply = req_data_dict.pop("is_apply") #是否确权成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("确权接口用例执行详情如下：")
        pp.pprint("确权接口执行测试用例编号：[{}]".format(caseid))
        pp.pprint("确权接口测试目的：{}".format(case_target))
        pp.pprint("确权接口用例描述：{}".format(case_des))
        pp.pprint("确权接口地址：{}".format(self.url))
        pp.pprint("确权接口预期接口返回值={}".format(expect))
        pp.pprint("确权接口预期回调状态值={}".format(expCallbackFlag))

        start = time.time()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.time()
        hs = end -start
        pp.pprint("确权接口请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        try:
            res_serialNo = jsonpath(ori_res.json(), "$..serialNo")[0]
        except Exception as e:
            res_serialNo = ""
        self.op_excel.writer_data(row_num, 64, res_serialNo)  # 写入实际响应结果中的serialNo
        self.op_excel.writer_data(row_num,65,ori_res.text) #写入实际响应结果全部
        pp.pprint("确权接口响应结果={}".format(res))
        kargs = {"expect":expect,
                 "res":ori_res,
                 "req":req_data_dict,
                 "partnerID":req_data_dict.get("partnerID"),
                 "partnerKey":req_data_dict.get("partnerKey"),
                 "expCallbackFlag":expCallbackFlag,  #expect, res,req,,
                 "download_url":download_url,
                 "download_file":download_file
        }
        start = time.time()
        is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data,cmp_req_res,download_case,tsa_file = self.crr.verify_is_pass(**kargs)
        count = 1
        while not is_pass and serialNo:
            if download_case:
                kargs["download_case"]=download_case
                kargs["download_req_url"] = download_req_url
                kargs["download_req_data"] = download_req_data
                kargs["download_res"] = download_res
            if cmp_req_res:
                kargs["cmp_req_res"] = cmp_req_res
            if tsa_file:
                kargs["tsa_file"] = tsa_file
            is_pass,serialNo,database_str,database_str_hd,download_req_url,download_req_data,download_res,download_res_data,cmp_req_res,download_case,tsa_file = self.crr.verify_is_pass(**kargs)
            count +=1
            if count >60:
                break
        end =time.time()
        hs = end -start
        pp.pprint("确权接口响应结果验证耗时：{}".format(hs))

        if  is_pass and serialNo:
            pp.pprint("因证书为异步生成，所以此用列需等待生成后进行下载，需循环验证，共验证<{}>次,找到PDF证书".format(count))

        if database_str:
            pp.pprint("确权接口请求数据与数据库存入值校验结果：{}".format(database_str)) #数据库值对比结果文字信息
        if database_str_hd:
            pp.pprint("确权接口预期回调接口值与数据库回调值校验结果：{}".format(database_str_hd))  # 数据库回调值对比结果文字信息

        pp.pprint("------------------------------------------------------------------------------------------")
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示用例中的文件地址")

        pp.pprint("确权接口传入参数={}".format(json.dumps(req_data_dict, ensure_ascii=False)))


        pp.pprint("------------------------------------------------------------------------------------------")

        if download_req_url:
            pp.pprint("下载接口请求地址={}".format(download_req_url))  # 下载接口请求地址
        if download_req_data:
            pp.pprint("下载接口请求数据={}".format(download_req_data))  # 下载接口请求数据
        if download_res:
            pp.pprint("下载接口响应数据={}".format(download_res))  # 下载接口响应数据，不包含文件流data
            pp.pprint("注：下载接口响应数据中因文件流data参数过大，所以不写入测试报告，以防止测试报告过大")

        if is_pass and serialNo:
            self.op_excel.writer_data(row_num, 66, "pass")  # 写入是否确权成功
        else:
            self.op_excel.writer_data(row_num, 66, "fail")  # 写入是否确权成功

        #self.op_excel.writer_data(row_num, 67, download_res_data)  # 写入下载接口返回信息

        if download_res_data and download_res_data.get("data",None):
            self.op_excel.writer_data(row_num,68,"pass") #写入是否下载成功
        else:
            self.op_excel.writer_data(row_num, 68, "fail")  # 写入是否下载成功

        if is_pass:
            self.op_excel.writer_data(row_num, 69, "通过")  # 写入用例执行结果
        else:
            self.op_excel.writer_data(row_num, 69, "未通过")  # 写入用例执行结果

        pp.pprint("------------------------------------------------------------------------------------------")
        if is_pass:
            pp.pprint("测试用例执行通过")
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
    description = "申请接口-20种文件类型申请验证-申请成功"
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=title,description=description,verbosity=2)
    runner.run(suite)
