import base64
import csv
import datetime
import random
import string

from python_excel.utils.operation_excel import OperationExcel
from copy import  deepcopy
from python_excel.utils.operation_json import OperationJson
from python_excel.get_data.param_global import ParamGlobal
import logging
import hashlib
import os

log = logging.getLogger(__file__)

class TsaParamDict:
    hash_order =['partnerID', 'partnerKey', 'hash', 'file', 'hashAlgorithm', 'fileSzieFlag', 'fileType', 'opusName', 'fileExtension','opusState', 'opusPartnerID', 'opusLabel', 'opusStore', 'opusDescribe', 'opusType', 'opusCreativeType', 'opusCreativeNature', 'applyType', 'applyUserType', 'applyNationality', 'applyName', 'applyIDType', 'applyIDNumber', 'applyPhone', 'applyMail', 'applyAddress', 'applyEmergencyName', 'applyEmergencyPhone', 'authType', 'authValidiy', 'authProtocol', 'authTime', 'authBusiness', 'authPlatform', 'authPlatformID', 'authPrice', 'authAllowType', 'authUse', 'authCountry', 'authSell', 'authLimit', 'authRemark', 'authUserType', 'authUserNationality', 'authUserName', 'authUserIDType', 'authUserIDNumber', 'authUserPhone', 'authUserMail', 'authUserAddress', 'remark1', 'remark2', 'remark3', 'encodeFmt', 'salt', 'callbackUrl']
    hash_order_download=['partnerID', 'partnerKey','serialNo']
    def __init__(self,filename=None,sheetid=0):
        try:
            if filename:
                self.filename = filename
            else:
                self.filename = "../data_file/data_xn.xlsx"
            self.sheetid = sheetid
            self.op_excel = OperationExcel(self.filename,sheetid)
            self.name_value_list = self.op_excel.get_row_col_list()
            #print(self.name_value_list)
            self.name_list = self.name_value_list[0]
            self.op_json = OperationJson("../data_file/emun.json")
            self.param = ParamGlobal()
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

    def get_param_value(self0):
        pass


    def get_param_name_value(self):
        '''
        获取参数名与参数值对应的字典列表
        :return: 参数列表
        '''
        try:
            name_value_row_list = []
            #print(self.get_param_name())
            for i in range(1,len(self.name_value_list)):
                name_value_row_list.append(dict(zip(self.get_param_name(),self.name_value_list[i])))
            return name_value_row_list
        except Exception as e:
            log.error("接口参数处理类处理参数名与参数值方法异常，异常原因：{}".format(e))
            return None



    def deal_param(self,flag=0,req_type='',start=0,end=0):
        '''
        处理后的参数数据即
        参数值不填代表传参此参数不填
        参数值为N代表传参数名，但参数值为“”
        参数值为F-文件名代表传的参数是文件类型
        :return:
        '''
        no_param = ["IsRun", "CaseID", "TestTarget", "CaseDesc", "ExpectValue", "callbackFlag", "res_serialNo",
                    "result", "fileB", "authProtocolB", "is_apply", "res_download", "is_download", "is_pass"]
        try:
            case_list= self.get_param_name_value()
            if end == 0:
                end = len(case_list)
            if len(case_list)>0:
                case_remove = []
                count = 0
                for param_dict in case_list[start:end]:
                    if str(param_dict.get("IsRun")).lower() != "yes":
                        case_remove.append(param_dict)
                        continue
                    for key in list(param_dict.keys()):
                        key_value = param_dict.get(key)
                        # if not key_value and key not in no_param and key !="salt":
                        #     del param_dict[key]
                        if str(key_value).upper() == 'N':
                            param_dict[key] = ""
                        if (key == "file"   or key == "authProtocol" )and key_value != "" :
                            param_dict[key] = self.encry(key_value) #根据获取的key_value进行上传前数据处理

                    if param_dict["CaseID"] == "BQ_salt_error":
                        pass
                    elif flag == 0 and req_type != "download":
                        salt = self.get_salt(param_dict)
                        param_dict["salt"] = salt
                    elif req_type == "download" and count<22:
                        salt = self.get_salt(param_dict,req_type="download")
                        param_dict["salt"] = salt
                    count += 1
            if len(case_remove)>0:
                for case in  case_remove:
                    case_list.remove(case)

            return case_list[start:end]
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
                        case_1["TestTarget"] = "申请成功-枚举类型数据正确性验证-00{}".format(count+1)
                        case_1["CaseDesc"] ='枚举类型参数<{}>-合法参数值<{}>-其它参数正确填写-申请成功'.format(param_key,key)
                        case_1["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":true}'
                        salt = self.get_salt(case_1)
                        case_1["salt"] = salt
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

    def get_salt(self,case_dict=None,name_space="",req_type=''):
        test_param_list = []
        if req_type=="download":
            hash_order = self.hash_order_download
        else:
            hash_order =self.hash_order
        if name_space:
            case_dict[name_space]=""
        value_order_list = []
        for param_name in hash_order:
          test_param_list.append(case_dict.get(param_name,""))
          if param_name in case_dict.keys():
              value_order_list.append(case_dict[param_name])
              # print(value_order_list)
          # else:
          #     value_order_list.append("")

        partnerKey = case_dict.get("partnerKey") if case_dict.get("partnerKey")  else ""
        #
        # print(value_order_list)
        # print(len(value_order_list))
        salt = self.make_salt(value_order_list,partnerKey)

        value_order_list[len(value_order_list)-2]=salt
        a = []
        a.append(value_order_list)
        print(value_order_list)
        print("*************************************")
        print('_'.join(value_order_list))
        print("*************************************")
        test_param_list[54] = salt
        print(len(test_param_list))
        count = 0
        for i in test_param_list:
            print(i+"*****")
            count=count+1
            print(count)
        path = "../data_file/{}.csv".format(case_dict["CaseID"])
        # if not os.path.exists(path):
        #     os.makedirs(path)
        with open(path,mode="w+",newline="",encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(test_param_list)

        #case_dict["userInterfaceValidity"] = userInterfaceValidity
        return salt





    def make_salt(self,value_list=None,partnerKey=""):
        # 待加密信息
        #print(value_list)
        deal_value_list = []
        for value in value_list:
            try:
                value_str=str(value)
            except Exception as e :
                value_str = value
            deal_value_list.append(value_str)
        #print(deal_value_list)

        # print(deal_value_list)
        value_str = "".join(deal_value_list)
        # print(value_str)

        # 创建md5对象
        m = hashlib.md5()

        # Tips
        # 此处必须encode
        # 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
        # 因为python3里默认的str是unicode
        # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
        b = value_str.encode(encoding='utf-8')
        m.update(b)
        value_str_md5 = m.hexdigest()
        salt = value_str_md5+partnerKey

        # print('MD5加密前为 ：' + value_str)
        # print('MD5加密后为 ：' + value_str_md5)
        # print('salt ：' + salt)
        #
        return salt
        # 另一种写法：b‘’前缀代表的就是bytes --此方法仅针对于英文加密，中文加密此方法报错
        # str_md5 = hashlib.md5(b'this is a md5 test.').hexdigest()
        # print('MD5加密后为 ：' + str_md5)

    def case_deal_param(self,case_dict):
        pass


    def get_sha256(self,filename):
        with open(filename,'rb') as f :
            data = f.read()
            encodestr = base64.b64encode(data)
            #encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
            #print(str(encodestr,"utf-8"))
        s = hashlib.md5(data).hexdigest()
        # sha = hashlib.sha256()
        # sha.update(data)
        # hash_256 = sha.hexdigest()
        # print(hash_256,"utf-8")
        # return str(hash_256,"utf-8")
        return s

if __name__ == "__main__":
    tsapd = TsaParamDict()
    #filepath = "/Users/majing/Desktop/5itest.jpg"
    # print(tsapd.get_param_name())
    # print(tsapd.get_param_name_value())
    # print(tsapd.deal_param())
    # print(tsapd.deal_enum_param())
    #tsapd.make_data_param_value_fail()
    #ss= tsapd.encry(filepath)
    #tsapd.decry(ss,22222)
   # print(tsapd.deal_enum_param())
   #  print(hash("5"))
   #  print(tsapd.make_userInterfaceValidity([2]))
    tsapd.deal_param()
    #print(tsapd.get_sha256("../applay_file/file_154kb.jpg"))
    # print(tsapd.make_salt())
