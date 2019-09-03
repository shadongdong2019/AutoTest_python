import json

from jsonpath import jsonpath
from InterfaceTest.python_excel.common.interface_run import InterfaceRun
from InterfaceTest.python_excel.get_data.tsa_param_dic import TsaParamDict
import logging
from copy import  deepcopy
import time
log = logging.getLogger(__file__)
class CmpReqRes:
    '''
    对比响应结果后存入的数据与请求数据是否一致
    '''
    def __init__(self):
        self.inter_run = InterfaceRun()
        self.tsa = TsaParamDict("",1)

    def verify_is_pass(self, **kwargs):
        '''
        验证响应结果是否满足预期结果
        :param expect: 预期结果
        :param res: 实际响应结果
        :return:True-代表测试通过，False-代表测试未通过
        '''

        expect = kwargs.get("expect",None)
        res = kwargs.get("res",None)
        req = kwargs.get("req",None)
        expCallbackFlag = kwargs.get("expCallbackFlag",None)
        no_verify_data_list = kwargs.get("no_verify_data_list", None)
        database_verify_res = {}
        serialNo = None
        verify_res = {} #本方法返回验证结果字典
        try:
            if '"success":true' in expect and res.json().get("success") == True:
                verify_data = {
                    "serialNo":serialNo,
                    "req":req,
                    "expCallbackFlag":expCallbackFlag,
                    "no_verify_data_list":no_verify_data_list
                }
                #验证数据库中的值是否正确
                database_verify_res = self.verify_database(**verify_data)
        except Exception as e:
            log.error("测试用例预期结果与实际结果对比方法出现异常，异常原因：{}".format(e))
            flag = None
        verify_res.update(database_verify_res)
        return verify_res

    def verify_database(self, **kwargs):
        '''
        :param serialNo: 身份标识唯一ID值
        :param req: 请求数据
        :param res: 存入结果
        :param re:  提取json规则
        :return:True-代表一致，False-代表不一致
        '''

        database_str_hd = None
        database_str = None
        expCallbackFlag = kwargs.get("expCallbackFlag", None)
        url = kwargs.get("verify_url", None)
        req = kwargs.get("req", None)
        no_verify_data_list = eval(kwargs.get("no_verify_data_list", None))
        try:
            expCF_dict = json.loads(expCallbackFlag)
            expCF_value = expCF_dict.get("callbackFlag")
        except Exception as e:
            expCF_value = expCallbackFlag
        try:
            json_obj = self.inter_run.main_request("get", url).json()
            res = jsonpath(json_obj, "$.._source")[0]
            error_str = ""
            flag = False
            req_keys = req.keys()
            for key in req_keys:
                if req.get(key) == str(res.get(key)) and req.get(key) not in no_verify_data_list:
                    flag = True
                else:
                    error_str = "请求参数<{0}={1}>,数据库存储参数<{0}={2}>".format(key, req.get(key), str(res.get(key)))
                    flag = False
                    break

            if flag:
                database_str = "数据库存储验证结果：一致（申请接口参数请求值与数据库存储值一致）"
                if expCF_value != None:
                    if expCF_value == res.get("callbackFlag"):
                        flag = True
                        database_str_hd = "数据库回调状态值与预期状态值一致：回调成功"
                    else:
                        flag = False
                        database_str_hd = "回调结果与预期不一致：回调失败,预期回调结果callbackFlag={}，实际数据库存储callbackFlag={}".format(
                            expCF_value, res.get("callbackFlag"))
                else:
                    flag = True
            else:
                database_str = "数据库存储验证结果：不一致（申请接口参数请求值与数据库存储值不一致,具体不一致原因：{}）".format(error_str)
        except Exception as e:
            log.error("测试用例请求参数与存储结果对比出现异常，异常原因：{}".format(e))
            flag = False

        database_verify_res = {
            "database_flag": flag,
            "database_str": database_str,
            "database_str_hd": database_str_hd
        }
        return database_verify_res


    def download_verify(self,expect, res,req):
        serialNo = req.get("serialNo")
        file_data = res.json().get("data")
        if file_data:
            self.tsa.decry(file_data, serialNo)
            down_su = True
        else:
            down_su = False
        res_verify = self.deal_dict(expect,res)
        if '"success":true' in expect and res.json().get("success") == True:
            if down_su and res_verify:
                return True,serialNo
            else:
                return False,serialNo
        elif res_verify:
            return True,serialNo
        else:
            return False,serialNo

    def deal_dict(self,expect,res):
        try:
            expect_dict = json.loads(expect)
        except Exception as e:
            log.error("预期结果不是字典类型，预期结果为：{}".format(expect))
            expect_dict = expect
        try:
            res_dict = res.json()
        except Exception as e:
            log.error("实际结果不是json类型，预期结果为：{}".format(res))
            res_dict = res
        try:
            expect_keys = expect_dict.keys()
        except Exception as e:
            log.error("预期结果不是字典类型无法取出keys，预期结果为：{}".format(expect))
            expect_keys = []

        if expect_keys == []:
            res_status = res.json().get("status")
            if  expect == str(res_status):
                cmp_res = True
            elif expect in res:
                cmp_res = True
            else:
                cmp_res = False
        else:
            for expect_key in expect_keys:
                if expect_dict.get(expect_key) == res_dict.get(expect_key):
                    cmp_res = True
                else:
                    cmp_res = False
                    break
        return cmp_res

    def download_case(self,partnerID,partnerKey,serialNo,url=None,download_file=None):
        flag = False
        try:
            if url:
                req_url = url
            else:
                req_url = "http://39.107.66.190:9999/v2/api/confirm/downloadOpusCertificate"  # 下载接口
                req_url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"
            data = {}
            salt = self.tsa.make_salt([partnerID,partnerKey,serialNo],partnerKey)
            data["partnerID"]=partnerID
            data["partnerKey"] = partnerKey
            data["serialNo"] = serialNo
            data["salt"] = salt
            start = time.time()
            res = self.inter_run.main_request("post", req_url, data).json()
            end = time.time()
            hs = end -start
            print("下载接口请求响应时间：{}".format(hs))
            res_copy = deepcopy(res) #用于返回结果写入excel表格
            try:
                if res.get("data",None):
                    file_data = res.pop("data")
                else:
                    file_data = None
            except Exception as e:
                log.error("下载接口返回结果中去除掉data出现异常，异常原因".format(e))
                res = res
                file_data=None
            if file_data:
                self.tsa.decry(file_data, data["serialNo"],download_file=download_file)
                flag = True
            else:
                flag = False
        except Exception as e:
            log.error("下载接口获取返回信息异常 ，异常原因：{}".format(e))
            print("下载接口返回结果出现异常,异常原因={}".format(e))
            flag =False
        return flag,req_url,data,res,res_copy
if __name__ == "__main__":
    crr = CmpReqRes()
    crr.cmp_req_res()
