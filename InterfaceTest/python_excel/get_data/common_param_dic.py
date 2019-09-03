import base64
import csv
import datetime
import random
import string

from InterfaceTest.python_excel.utils.operation_excel import OperationExcel
from copy import  deepcopy
from InterfaceTest.python_excel.utils.operation_json import OperationJson
from InterfaceTest.python_excel.get_data.param_global import ParamGlobal
import logging
import hashlib
import os

log = logging.getLogger(__file__)

class CommonParamDict:
    def __init__(self,**kargs):
        try:
            self.kargs = kargs
            #实例化操作Excel表格类
            self.op_excel = OperationExcel(self.kargs.get("case_filepath",None),self.kargs.get("case_sheetid",0))
            #获取参数名所在行返回参数名列表
            self.param_name_list = self.op_excel.get_row_col_list(self.kargs.get("case_param_name_start",0), self.kargs.get("case_param_name_end",0))
            #实例参数名处理类-根据上面的参数名列表
            self.param = ParamGlobal(self.param_name_list)
            # 获取参数英文名列表
            self.name_list = self.param.get_param_en_name_list()
            #获取参数值列表（仅获取从开始行到结束行的数所在，如果都为None表示所有记录）
            self.name_value_list = self.op_excel.get_row_col_list(self.kargs.get("case_start_rownum",1),self.kargs.get("case_end_rownum",None))
            # 获取不在接口请求中传入的参数列表
            self.param_no_req = self.param.get_param_no_request_list()

        except Exception as e:
            log.error("接口参数处理类初始化异常，异常原因：{}".format(e))

    def get_param_name(self):
        '''
        获取参数名列表
        :return:
        '''
        try:
            param_name_list = None
            param_name_list = []

            for pname in self.name_value_list[0]:
                param_name = pname.split("-")[1]
                param_name_list.append(param_name)
        except Exception as e:
            log.error("接口参数处理参数名方法异常，异常原因：{}".format(e))
        return param_name_list



    def get_param_name_value(self):
        '''
        获取参数名与参数值对应的字典列表
        :return: 参数列表
        '''
        name_value_row_list = None
        try:
            name_value_row_list = []
            for i in range(0,len(self.name_value_list)):
                name_value_row_list.append(dict(zip(self.name_list,self.name_value_list[i])))
        except Exception as e:
            log.error("接口参数处理类处理参数名与参数值方法异常，异常原因：{}".format(e))
        return name_value_row_list

    def deal_download_param(self,req_type=''):
        '''
        处理后的参数数据即
        参数值不填代表传参此参数不填
        参数值为N代表传参数名，但参数值为“”
        参数值为F-文件名代表传的参数是文件类型
        :return:
        '''
        no_param = ["IsRun","CaseID","TestTarget","CaseDesc","ExpectValue","callbackFlag","res_serialNo","result","fileB","authProtocolB","is_apply","res_download","is_download","is_pass"]
        keys = ["IsRun","CaseID","TestTarget","CaseDesc","ExpectValue","partnerID","partnerKey","res_serialNo","res_download","is_download","is_pass"]
        case_list_new = []
        case_dict ={}
        try:
            case_list= self.get_param_name_value()
            if len(case_list)>0:
                case_remove = []
                count = 0
                for param_dict in case_list:
                    case_dict_copy = deepcopy(case_dict)
                    if str(param_dict.get("IsRun")).lower() != "yes" or str(param_dict.get("is_apply")).lower() != "pass":
                        case_remove.append(param_dict)
                        continue
                    for key in keys:

                        key_value = param_dict.get(key)
                        if key == "TestTarget":
                            case_dict_copy[key] = "下载成功"
                        elif key == "CaseDesc":
                            case_dict_copy[key] = "必填参数（4个）正确传入-下载成功"
                        elif key == "ExpectValue":
                            case_dict_copy[key] = '{"success":true,"resultCode":"0204000"}'
                        elif key == "res_serialNo":
                            case_dict_copy["serialNo"] = key_value
                        else:
                            case_dict_copy[key] = key_value

                    case_list_new.append(case_dict)
                    count += 1
                    break
            return case_list_new
        except Exception as e :
            log.error("接口参数处理类处理后下载接口参数数据方法异常，异常原因：{}".format(e))
            return None


    def deal_param_01(self,flag=0,req_type=''):
        '''
        处理后的参数数据即
        参数值不填代表传参此参数不填
        参数值为N代表传参数名，但参数值为“”
        参数值为F-文件名代表传的参数是文件类型
        :return:
        '''
        no_param = ["IsRun", "CaseID", "TestTarget", "CaseDesc", "ExpectValue", "callbackFlag", "res_serialNo",
                    "result", "fileB", "authProtocolB", "is_apply", "res_download", "is_download", "is_pass"]
        need_param = ["IsRun", "CaseID", "TestTarget", "CaseDesc", "ExpectValue", "partnerID", "partnerKey", "res_serialNo",
                "res_download", "is_download", "is_pass"]
        try:
            case_list= self.get_param_name_value()
            if len(case_list)>0:
                case_remove = []
                count = 0
                for param_dict in case_list:
                    if str(param_dict.get("IsRun")).lower() != "yes" or str(param_dict.get("is_apply")).lower() != "pass":
                        case_remove.append(param_dict)
                        continue
                    count += 1
            if len(case_remove)>0:
                for case in  case_remove:
                    case_list.remove(case)

            return case_list
        except Exception as e :
            log.error("接口参数处理类处理后的参数数据方法异常，异常原因：{}".format(e))
            return None



    def deal_param(self,**kwargs):
        '''
        处理后的参数数据即
        参数值不填代表传参此参数不填
        参数值为N代表传参数名，但参数值为“”
        参数值为F-文件名代表传的参数是文件类型
        :return:
        '''
        if kwargs:
            self.kargs = kwargs

        no_param = self.param_no_req
        try:
            case_list= self.get_param_name_value()
            case_remove = []
            if len(case_list)>0:
                count = 0
                for param_dict in case_list:
                    if str(param_dict.get("IsRun")).lower() != "yes":
                        case_remove.append(param_dict)
                        continue
                    for key in list(param_dict.keys()):
                        key_value = param_dict.get(key)
                        if not key_value and key not in no_param :
                            del param_dict[key]
                        if str(key_value).upper() == 'N':
                            param_dict[key] = ""
                    salt = self.get_salt(param_dict)
                    param_dict["salt"] = salt

                    count += 1
            if len(case_remove)>0:
                for case in  case_remove:
                    case_list.remove(case)

            return case_list
        except Exception as e :
            log.error("接口参数处理类处理后的参数数据方法异常，异常原因：{}".format(e))
            return None

    def encry(self,cnf_org):
        try:
            with open(cnf_org,'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                #print(str(encodestr,'utf-8')) # 重新编码数据
                return str(encodestr,'utf-8')
        except Exception as e:
            log.error("接口参数处理类处理文件方法异常，异常原因：{}".format(e))
            return None

    def decry(self,cnf_org,serialNo,file_type="pdf",download_file=None):

        bq_pdf = base64.b64decode(cnf_org)
        data_str =datetime.datetime.now().strftime('%Y%m%d')
        rand_str = ''.join(random.sample((string.ascii_letters + string.digits),5))
        pdf_name = "{}_{}_{}.{}".format(serialNo,data_str,rand_str,file_type)
        if not download_file:
            path = '../download/0729_hz/'
        else:
            path = '../download/{}/'.format(download_file)
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = path+"{}".format(pdf_name)
        file = open(file_name, "wb")
        file.write(bq_pdf)
        file.close()

    def deal_enum_param(self,caseid=0,param=None,start=0,end=0):
        try:
            if param:
                param_list = param
            else:
                param_list = self.op_json.get_keys_list()
            if end == 0:
                end=len(param_list)
            emun_case_list = []
            count = 0
            for param_key in param_list[start:end]:
                emun_json = self.op_json.get_data_for_key(param_key)
                if len(emun_json)>0:
                    case_1 = deepcopy(self.deal_param()[caseid])  # 拷贝测试用例第二条
                    for key in list(emun_json.keys()):
                        case_1[param_key] = key
                        case_1["case_target"] = "申请成功-枚举类型数据正确性验证-00{}".format(count+1)
                        case_1["case_desc"] = '枚举类型参数<{}>-合法参数值<{}>-其它参数正确填写-申请成功'.format(param_key,key)
                        emun_case_list.append(case_1)
                        count+=1

            return emun_case_list
        except Exception as e :
            log.error("接口参数处理类处理枚举字段方法异常，异常原因：{}".format(e))
            return None

    def test_param_400(self,caseid):
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        test_param_400_list= []
        for name in en_name_list:
            count+=1
            if count>13:
                case_1 = deepcopy(self.deal_param()[caseid])  # 拷贝测试用例第一条
                case_1[name] = "101"
                test_param_400_list.append(case_1)
        return test_param_400_list

    def get_salt(self,case_dict=None):
        xn_case = []
        hash_order =eval(self.kargs.get("hash_orders",None))
        value_order_list = []
        for param_name in hash_order:
          xn_case.append(case_dict.get(param_name,""))
          if param_name in case_dict.keys():
              value_order_list.append(case_dict[param_name])

        partnerKey = case_dict.get("partnerKey") if case_dict.get("partnerKey")  else ""
        salt = self.make_salt(value_order_list,partnerKey)
        return salt





    def make_salt(self,value_list=None,partnerKey=""):
        # 待加密信息
        deal_value_list = []
        for value in value_list:
            try:
                value_str=str(value)
            except Exception as e :
                value_str = value
            deal_value_list.append(value_str)
        value_str = "".join(deal_value_list)

        # 创建md5对象
        m = hashlib.md5()
        b = value_str.encode(encoding='utf-8')
        m.update(b)
        value_str_md5 = m.hexdigest()
        salt = value_str_md5+partnerKey
        return salt

    def case_deal_param(self,case_dict):
        pass


    def get_sha256(self,filename):
        with open(filename,'rb') as f :
            data = f.read()
            encodestr = base64.b64encode(data)
        s = hashlib.md5(data).hexdigest()

        return s

if __name__ == "__main__":
    tsapd = TsaParamDict()
    tsapd.deal_param()

