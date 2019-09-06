import base64
import datetime

from InterfaceTest.python_excel.utils.operation_excel import OperationExcel
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
            self.op_excel = OperationExcel(**self.kargs)
            #获取参数名所在行返回参数名列表
            self.param_name_list = self.op_excel.get_row_col_list_param_name(**self.kargs)
            #实例参数名处理类-根据上面的参数名列表
            self.param = ParamGlobal(self.param_name_list)
            # 获取参数英文名列表
            self.name_list = self.param.get_param_en_name_list()
            #获取参数值列表（仅获取从开始行到结束行的数所在，如果都为0表示所有记录）
            self.name_value_list = self.op_excel.get_row_col_list(**self.kargs)
            # 获取不在接口请求中传入的参数列表
            self.param_no_req = self.param.get_param_no_request_list()
            # 获取文件类型参数列表
            self.param_file = self.param.get_param_file_list()

        except Exception as e:
            log.error("接口参数处理类初始化异常，异常原因：{}".format(e))

    def deal_param(self,**kwargs):
        '''
        处理后的参数数据即
        参数值不填代表传参此参数不填
        参数值为N代表参数不传
        参数值为NN表示参数为空
        :return:
        '''

        if kwargs:
            self.kargs = kwargs  #获取配置文件字段，如是方法中未传，直接使用初始化方法中传入的

        no_param = self.param_no_req #获取不在请求里进行传入的参数列表
        file_stream_list = self.kargs.get("file_stream_list",[]) #获取配置文件里参数为文件类型需要转文件流的参数列表
        param_file = self.param_file

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
                        salt_N = False
                        key_value = param_dict.get(key)
                        if not key_value and key not in no_param :
                            del param_dict[key]
                        if str(key_value).upper() == 'N': #参数值为N表示此参数不传
                            if key == "salt":
                                salt_N = True
                            param_dict.pop(key)
                        elif str(key_value).upper() == 'NN': #参数值为NN表示此参数为空
                            param_dict[key] = ""
                        elif ((key in param_file) or (key in file_stream_list)) and key_value != "":
                            param_dict[key] = self.encry(key_value)  # 根据获取的key_value进行上传前数据处理
                    if not param_dict.get("salt",None) and not salt_N:
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


    def encry(self,file_path):
        '''
        把文件转为文件流
        :param file_path:文件全路径（路径+文件名）
        :return:b64encode编码后的文件流
        '''
        file_stream = ""
        try:
            with open(file_path,'rb') as f:  # 以二进制读取图片
                data = f.read()
                encodestr = base64.b64encode(data) # 得到 byte 编码的数据
                #print(str(encodestr,'utf-8')) # 重新编码数据
                file_stream = str(encodestr,'utf-8')
        except Exception as e:
            log.error("接口参数处理类将文件转为文件流方法异常，异常原因：{}".format(e))
        return file_stream

    def decry(self,**kwargs):
        '''
        将文件流转为指定格式的文件
        :return:True or False ,True表示存储成功，False表示失败
        '''
        is_download = False
        try:
            file_stream = kwargs.get("file_stream","") #获取文件流
            file_flag = kwargs.get("file_stream","") #获取文件标识，用于显示在文件名最前面，如serialNo码
            file_type = kwargs.get("file_type","pdf") #获取文件后缀类型 如：jpg/pdf
            download_path = kwargs.get("download_path","../download/") #获取下载文件存入路径
            file_str = base64.b64decode(file_stream) #把文件流进行base64解码
            data_str =datetime.datetime.now().strftime('%Y%m%d') #将当前时间转为字符串
            #rand_str = ''.join(random.sample((string.ascii_letters + string.digits),5)) #5位随机数（数字+字母）
            file_name = "{}_{}_{}.{}".format(file_flag,data_str,file_type) #生成文件名：文件标识+当前时间字符串+文件后缀
            if not os.path.exists(download_path): #判断文件存储路径是否存在
                os.makedirs(download_path) #如果不存在就在创建对应路径
            file_name = download_path+"{}".format(file_name) #存储路径+文件全称
            file = open(file_name, "wb") #以二进制读的方式打开文件
            file.write(file_str)#写入文件流解码后的内容
            file.close() #关闭文件
            is_download = True
        except Exception as e :
            log.error("下载并存储文件出现异常，异常原类：{}".format(e))
        return is_download


    def get_salt(self,case_dict=None):
        '''
        获取哈希加盐处理后的salt值
        :param case_dict: 用例字典
        :return: salt值
        '''
        xn_case = []
        hash_order =self.kargs.get("hash_orders",None)
        value_order_list = []
        for param_name in hash_order:
          xn_case.append(case_dict.get(param_name,""))
          if param_name in case_dict.keys():
              value_order_list.append(case_dict[param_name])

        partnerKey = case_dict.get("partnerKey") if case_dict.get("partnerKey")  else ""
        salt = self.make_salt(value_order_list,partnerKey)
        return salt


    def make_salt(self,value_list=None,partnerKey=""):
        '''
        针对参数值列表进行salt加盐处理
        :param value_list: 按传入顺序处理后的参数值列表
        :param partnerKey: partnerKey值
        :return:
        '''
        deal_value_list = [] #进行处理后的参数值列表
        for value in value_list:
            try:
                value_str=str(value)
            except Exception as e :
                value_str = value
            deal_value_list.append(value_str)
        value_str = "".join(deal_value_list) #将列表转为字符串，待加密信息


        m = hashlib.md5()# 创建md5对象

        # 此处必须encode
        # 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
        # 因为python3里默认的str是unicode
        # 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes
        b = value_str.encode(encoding='utf-8') #将字符串进行utf-8编码

        m.update(b) #进行md5加密
        value_str_md5 = m.hexdigest()#md5加密后的值为32位-hexdigest()默认是32位(bytes)，16位值调用对象的digest()
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
    pass

