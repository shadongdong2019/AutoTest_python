import sys
sys.path.append('/Users/majing/Downloads/home 4/ma/桌面/InterfaceTest')
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
sheetid = 5

data = TsaParamDict(filename,sheetid).deal_param()
#data_dl = TsaParamDict(filename,sheetid).deal_download_param()
#data_download = TsaParamDict(filename,4).deal_param(req_type="download")
# data_400 = TsaParamDict().test_param_400(1)
#data_error_param_no = CaseError(filename,1).make_data_param_no_case(1)
#data_error_value_None = CaseError(filename,1).make_data_param_value_None_fail(1)
#data_error_value_space = CaseError(filename,1).make_data_param_value_space_fail(1)
#data_error_value_spec_b = CaseError(filename,1).make_data_param_value_spe_fail_b(1)
#data_error_value_type = CaseError(filename,1).make_data_param_value_type_fail(1)
#data_error_value_long_1= CaseError(filename,1).make_data_param_value_long_1_fail(59)

@ddt.ddt
class CaseRun(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.itle = '版权服务2.0申请接口测试报告'
        self.description = ""
        self.url = "http://39.107.66.190:9999/v2/api/confirm/opusConfirm" #申请接口  ipp20timestamp.tsa.cn
        self.url = "https://ipp.tsa.cn/v2/api/confirm/opusConfirm"
        #self.url = "https://ipp20timestamp.tsa.cn/v1/api/confirm/opusConfirm"
        #self.url = "http://ipp20timestamp.tsa.cn/v1/api/confirm/downloadOpusCertificate" #下载接口
        self.count = 0
    @classmethod
    def tearDownClass(self):
        pass
    def setUp(self):
        self.interface_run = InterfaceRun()
        self.deal_res_data = DealResData()
        self.op_excel = OperationExcel(filename,sheetid)
        self.case_d = CaseDetail("../data_file/TestCase_zh.xlsx")
        self.method_req = "post"
        self.tsa_param = TsaParamDict()
        self.crr = CmpReqRes()
    def tearDown(self):
        pass

    @ddt.data(*data)
    def test_apply_01(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))
        pp.pprint("预期回调状态值={}".format(expCallbackFlag))

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
        self.op_excel.writer_data(row_num, 61, res_serialNo)  # 写入实际响应结果
        self.op_excel.writer_data(row_num,62,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        start = time.clock()
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),expCallbackFlag=expCallbackFlag)
        count = 0
        while not is_pass:
            is_pass, serialNo = self.crr.verify_is_pass(expect, ori_res, req_data_dict, req_data_dict.get("partnerID"),
                                                        req_data_dict.get("partnerKey"),
                                                        expCallbackFlag=expCallbackFlag)
            count +=1
            if count >10:
                break
        end =time.clock()
        hs = end -start
        pp.pprint("验证耗时：{}".format(hs))
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        if is_pass and serialNo:
            self.op_excel.writer_data(row_num, 65, "pass")  # 写入是否申请成功
        else:
            self.op_excel.writer_data(row_num, 65, "fail")  # 写入是否申请成功

        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")

    #@ddt.data(*data_dl)
    def etest_download_02(self,data_dict):
        self.url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format("下载成功"))
        pp.pprint("用例描述：{}".format("必填参数（4个）正确传入-下载成功"))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))

        partnerID=data_dict.get("partnerID")
        partnerKey = data_dict.get("partnerKey")
        serialNo = data_dict.get("res_serialNo")
        row_num = self.op_excel.get_row_num_for_value(caseid)
        #salt = self.tsa_param.make_salt([partnerID,partnerKey,serialNo],partnerKey)
        #url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"  # 下载接口
        res_download = self.crr.download_case(partnerID,partnerKey,serialNo)
        self.op_excel.writer_data(row_num, 66, "下载返回结果存入测试报告中，请查看测试报告")  # 写入是否申请成功
        if res_download:
            pprint("测试用例执行通过")
            self.op_excel.writer_data(row_num, 67, "pass")  # 写入是否申请成功
            self.op_excel.writer_data(row_num, 68, "pass")  # 写入是否申请成功
        else:
            self.op_excel.writer_data(row_num, 67, "fail")  # 写入是否申请成功
            self.op_excel.writer_data(row_num, 68, "fail")  # 写入是否申请成功
        self.assertTrue(res_download,"测试用例执行未通过")


    #@ddt.data(*data_download)
    def etest_download_01(self,data_dict):
        '''
        测试数据={0}
        :param data_dict:
        :return:
        '''
        self.url = "http://39.107.66.190:9999/v2/api/confirm/downloadOpusCertificate"
        self.url = "https://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"

        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        is_run = req_data_dict.pop("IsRun") #用例是否运行
        result = req_data_dict.pop("result")#申请成功返回结果
        is_pass_ex = req_data_dict.pop("is_pass")  # 申请成功返回结果

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        self.op_excel.writer_data(row_num,9,ori_res.text) #写入实际响应结果

        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),req_type="download")
        if is_pass:
            self.op_excel.writer_data(row_num, 10, "pass")  # 写入用例是否通过
        else:
            self.op_excel.writer_data(row_num, 10, "fail")  # 写入用例是否通过

        self.assertTrue(is_pass,"测试用例执行未通过")


    #@ddt.data(*data_emun)
    def etest_apply_emun_01(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        is_run = req_data_dict.pop("IsRun")
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        #self.op_excel.writer_data(row_num,7,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),expCallbackFlag=expCallbackFlag)
        self.assertTrue(is_pass,"测试用例执行未通过")


    #@ddt.data(*data_error_param_no)
    def etest_param_no_fail(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))
        #pp.pprint("预期回调状态值={}".format(expCallbackFlag))

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
        # self.op_excel.writer_data(row_num, 61, res_serialNo)  # 写入实际响应结果
        # self.op_excel.writer_data(row_num,62,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),expCallbackFlag=expCallbackFlag)
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")



    #@ddt.data(*data_error_value_None)
    def etest_data_param_value_None_fail(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)


        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))
        # pp.pprint("预期回调状态值={}".format(expCallbackFlag))

        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req, self.url, req_data_dict)
        end = time.clock()
        hs = end - start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        try:
            res_serialNo = jsonpath(ori_res.json(), "$..serialNo")[0]
        except Exception as e:
            res_serialNo = ""
        # self.op_excel.writer_data(row_num, 61, res_serialNo)  # 写入实际响应结果
        # self.op_excel.writer_data(row_num, 62, ori_res.text)  # 写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        #time.sleep(7)
        is_pass, serialNo = self.crr.verify_is_pass(expect, ori_res, req_data_dict, req_data_dict.get("partnerID"),
                                                    req_data_dict.get("partnerKey"), verify_type="None",expCallbackFlag=expCallbackFlag)
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict, ensure_ascii=False)))
        self.assertTrue(is_pass, "测试用例执行未通过")

    #@ddt.data(*data_error_value_space)
    def etest_data_error_value_space(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        req_data_dict = deepcopy(data_dict)
        pp = pprint.PrettyPrinter(indent=4)

        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过
        space_name = req_data_dict.pop("space_name")

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        #self.op_excel.writer_data(row_num,7,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),space_name=space_name,expCallbackFlag=expCallbackFlag)
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict, ensure_ascii=False)))
        self.assertTrue(is_pass, "测试用例执行未通过")


    #@ddt.data(*data_error_value_spec_b)
    def etest_data_error_value_spec(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)


        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过


        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))
        #pp.pprint("预期回调状态值={}".format(expCallbackFlag))

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
        # self.op_excel.writer_data(row_num, 61, res_serialNo)  # 写入实际响应结果
        # self.op_excel.writer_data(row_num,62,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),expCallbackFlag=expCallbackFlag)
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")

    #@ddt.data(*data_error_value_long_1)
    def etest_data_error_value_long_1(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))
        #pp.pprint("预期回调状态值={}".format(expCallbackFlag))

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
        # self.op_excel.writer_data(row_num, 61, res_serialNo)  # 写入实际响应结果
        # self.op_excel.writer_data(row_num,62,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res.json()))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),expCallbackFlag=expCallbackFlag)
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")

    #@ddt.data(*data_error_value_type)
    def etest_data_error_value_type(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        pp = pprint.PrettyPrinter(indent=4)
        req_data_dict = deepcopy(data_dict)

        is_run = req_data_dict.pop("IsRun")
        caseid = req_data_dict.pop("CaseID")
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        expCallbackFlag = req_data_dict.pop("ExpCallbackFlag")
        res_serialNo = req_data_dict.pop("res_serialNo")
        result = req_data_dict.pop("result")
        fileB = req_data_dict.pop("fileB")
        authProtocolB = req_data_dict.pop("authProtocolB")
        is_apply = req_data_dict.pop("is_apply") #是否申请成功
        res_download = req_data_dict.pop("res_download")  # 下载接口返回结果
        is_download = req_data_dict.pop("is_download")#是否下载成功
        is_pass = req_data_dict.pop("is_pass") #用例是否通过

        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))
        pp.pprint("预期接口返回值={}".format(expect))
        #pp.pprint("预期回调状态值={}".format(expCallbackFlag))

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
        # self.op_excel.writer_data(row_num, 61, res_serialNo)  # 写入实际响应结果
        # self.op_excel.writer_data(row_num,62,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res.json()))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"),expCallbackFlag=expCallbackFlag)
        if req_data_dict.get("file"):
            del req_data_dict["file"]
            pp.pprint("注：作品文件（file）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
            req_data_dict["file"] = fileB
        if req_data_dict.get("authProtocol"):
            del req_data_dict["authProtocol"]
            req_data_dict["authProtocol"] = authProtocolB
            pp.pprint("注：授权协议（authProtocol）值过大会影响测试报告打开速度，测试报告仅显示不用例中的文件地址")
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertTrue(is_pass,"测试用例执行未通过")

    #@ddt.data(*data_error_value_long)
    def etest_data_error_value_long(self,data_dict):
        self.title = '版权服务2.0申请接口测试报告(http)'
        self.description = "申请接口-合法数据正确性验证-枚举类型选填-申请成功"
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("TestTarget")  # 获取测试目的  TestTarget
        case_des = req_data_dict.pop("CaseDesc") #获取用例描述
        expect = req_data_dict.pop("ExpectValue")  # 获取预期接口返回值 ExpectValue
        is_run = req_data_dict.pop("IsRun")
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        #self.op_excel.writer_data(row_num,7,ori_res.text) #写入实际响应结果
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict,req_data_dict.get("partnerID"),req_data_dict.get("partnerKey"))
        self.assertTrue(is_pass,"测试用例执行未通过")


    #@ddt.data(*data_error_value_keyword)
    def etest_data_error_value_keyword(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")

    #@ddt.data(*data_error_value_js)
    def etest_data_error_value_js(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")


    #@ddt.data(*data_error_value_sql)
    def etest_data_error_value_sql(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")



    #@ddt.data(*data_error_name_None)
    def etest_data_error_name_None(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass,serialNo = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")

    #@ddt.data(*data_error_name_space)
    def etest_data_error_name_space(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")

    #@ddt.data(*data_error_name_keyword)
    def etest_data_error_name_keyword(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")

    #@ddt.data(*data_error_name_js)
    def etest_data_error_name_js(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")


    #@ddt.data(*data_error_name_sql)
    def etest_data_error_name_sql(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")

   #@ddt.data(*data_error_name_spec)
    def etest_data_error_name_spec(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")


   #@ddt.data(*data_error_name_long)
    def etest_data_error_name_long(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        case_target = req_data_dict.pop("case_target")  # 获取测试目的
        case_des = req_data_dict.pop("case_desc") #获取用例描述
        expect = req_data_dict.pop("expect")  # 获取预期接口返回值
        pp.pprint("用例执行详情如下：")
        pp.pprint("执行测试用例编号：[{}]".format(caseid))
        pp.pprint("测试目的：{}".format(case_target))
        pp.pprint("用例描述：{}".format(case_des))
        pp.pprint("接口地址：{}".format(self.url))

        pp.pprint("预期接口返回值={}".format(expect))
        start = time.clock()
        ori_res = self.interface_run.main_request(self.method_req,self.url,req_data_dict)
        end =time.clock()
        hs = end -start
        pp.pprint("请求耗时：{}".format(hs))
        res = self.deal_res_data.deal_res_data(ori_res)
        row_num = self.op_excel.get_row_num_for_value(caseid)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(req_data_dict))
        is_pass = self.crr.verify_is_pass(expect,ori_res,req_data_dict)
        self.assertTrue(is_pass,"测试用例未通过")


    # @ddt.data(*data_400)
    def etest_400(self,data_dict):
        req_data_dict = deepcopy(data_dict)
        # caseid = req_data_dict.pop("CaseID")
        pp = pprint.PrettyPrinter(indent=4)
        ori_res = self.interface_run.main_request(self.method_req, self.url, req_data_dict)
        res = self.deal_res_data.deal_res_data(ori_res)
        pp.pprint("响应结果={}".format(res))
        pp.pprint("传入参数={}".format(json.dumps(req_data_dict,ensure_ascii=False)))
        self.assertIn('"success":"fail"',res,"测试用例未通过")

    def etest_download(self):
        self.title = '版权服务2.0下载接口测试报告(http)'
        self.description = "下载接口-接口请求数据合法-请求成功，/非法-请求失败"

        data = {
            "partnerID": "12345678123456781234567812345678",
            "partnerKey": "12345678901234567890",
            "serialNo": "334305313362546688"
        }
        self.url = "http://39.107.66.190:9999/v1/api/confirm/downloadOpusCertificate" #下载接口
        res = self.interface_run.main_request(self.method_req, self.url, data).json()
        print("用例执行通过，返回结果={}".format(res))
        file_data = res["data"]
        self.tsa_param.decry(file_data,data["serialNo"])



if __name__ == "__main__":
    cr =CaseRun()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    run_file = sys.argv[0]
    run_file_name = os.path.basename(os.path.splitext(run_file)[0])
    rand_str = ''.join(random.sample((string.ascii_letters + string.digits), 5))
    report_name = run_file_name+datetime.datetime.now().strftime('%Y%m%d')+rand_str+'.html'
    report_path = os.path.join("../report/0729_zs/",report_name)

    fp = open(report_path,'wb')
    suite = unittest.TestLoader().loadTestsFromTestCase(CaseRun)
    title = '版权服务2.0生产环境接口测试报告（http）'
    description = "申请接口-大文件传入验证（作品文件file保证最大可以传50M文件，授权协议authProtocol最大可以传10M的文件）"
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=title,description=description,verbosity=2)
    runner.run(suite)
