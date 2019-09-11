from copy import deepcopy
from python_excel.get_data.param_global import ParamGlobal
from python_excel.get_data.tsa_param_dic import TsaParamDict
import time
import logging
log = logging.getLogger(__file__)
class CaseError:
    java_keyword_list = ['private', 'protected', 'public', 'abstract', 'class', 'extends', 'final', 'implements',
                         'interface', 'native', 'new', 'static', 'strictfp', 'synchronized', 'transient', 'volatile',
                         'break', 'continue', 'return', 'do', 'while', 'if', 'else', 'for', 'instanceof', 'switch',
                         'case', 'default', 'try', 'catch', 'throw', 'throws', 'import', 'package', 'boolean', 'byte',
                         'char', 'double', 'float', 'int', 'long', 'short', 'null', 'true', 'false', 'super', 'this',
                         'void', 'goto', 'const']

    spe_chr = ["～","#","￥","&","×","——","|","}","{","`","|","/","_","\n","\r"]
    js_list = ["<script>alter(123456)</script>"]
    sql_list = ["exec","xp_","sp_","declare","Union","cmd","+","//","..",";","‘","--","%","0x",">","<","=","!","-","*","/","(",")","|"]
    #个数101000
    long_text_en = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!dsdfsfsfsdfsfdsfsfsdfsfsdfs"*1000
    #个数255000
    long_text_zn = r"1《唐韵》都了切。《集韵》《韵会》丁了切，𠀤音茑。《说文》：长尾禽总名也。《说文》：长尾禽总名也总名也"*5000
    #空格数 100000
    long_space_zh = "          "*10000
    long_value_list = [long_text_en,long_text_zn,long_space_zh]

    int_param = ["fileSzieFlag","fileType","opusState","opusStore","opusType","opusCreativeType","opusCreativeNature","applyType","applyUserType",
                 "applyIDType","authType","authValidiy","authBusiness","authPrice","authAllowType","authSell",
                 "authUserType","authUserIDType"]
    long_20 = ["hashAlgorithm","opusPartnerID","applyPhone","applyEmergencyPhone","authTime","authPlatformID","encodeFmt","authUserNationality","authUserPhone"]

    b_name = ["callbackUrl","applyIDNumber"]


    def __init__(self,filename=None,sheetid=1):
        if filename:
            self.filename = filename
        else:
            self.filename = "../data_file/case_data.xlsx"

        self.param = ParamGlobal()
        self.tsa_p_d =TsaParamDict(self.filename,sheetid)

    # def make_data_param_value_fail(self):
    #     '''
    #     55个参数值为无效的测试用例
    #     值为以下几种情况：
    #     ='' 空
    #     =java 关键字
    #     =' ' 空格
    #     =js <script>alter(123456)</script>
    #     =sql “exec”,”xp_”,”sp_”,”declare”,”Union”,”cmd”,”+”,”//”,”..”,”;”,”‘”,”--”,”%”,”0x”,”><=!-*/()|”,和”空格”
    #     =超长
    #     =特殊字符 ~`！@#￥%……&*（）——+|、】【}{【？、》，《<>,. \n \t \r
    #     :return:
    #     '''
    #     start_time = time.time()
    #     param_value_None_case_list = []
    #     param_value_space_case_list = []
    #     param_value_keyword_case_list = []
    #     param_value_js_case_list = []
    #     param_value_spec_case_list = []
    #     param_value_long_case_list = []
    #
    #     all_list = []
    #     en_name_list = self.param.get_param_en_name_list()
    #     count = start
    #
    #     param_value_long_zh_case_list = []
    #     # case_7 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #     # case_8 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #     # case_9 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #     # case_10 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #     #
    #     # case_7["case_target"] = "申请失败-所有参数值超长组合"
    #     # case_7["case_desc"] = '所有参数值超长组合测试-汉字个数：{}'.format(len(self.long_value_list[0]))
    #     # case_7["expect"] = '"success":false'
    #     #
    #     # case_8["case_target"] = "申请失败-所有参数值超长组合"
    #     # case_8["case_desc"] = '所有参数值超长组合测试-引文数字个数：{}'.format(len(self.long_value_list[1]))
    #     # case_8["expect"] = '"success":false'
    #     #
    #     # case_9["case_target"] = "申请失败-所有参数值超长组合"
    #     # case_9["case_desc"] = '所有参数值超长组合测试-空格个数：{}'.format(len(self.long_value_list[2]))
    #     # case_9["expect"] = '"success":false'
    #     #
    #     # case_9["case_target"] = "申请失败-所有参数值超长组合"
    #     # case_9["case_desc"] = '所有参数值超长组合测试-中英文/空格/特殊字符超长个数：356000'
    #     # case_9["expect"] = '"success":false'
    #     #
    #     # for name in en_name_list:
    #     #     try:
    #     #         case_7[name]=self.long_value_list[0]
    #     #         case_8[name] = self.long_value_list[1]
    #     #         case_9[name] = self.long_value_list[2]
    #     #         case_10[name] = str(self.long_value_list[0]) + str(self.long_value_list[2]) + str(self.long_value_list[1])
    #     #     except Exception as e :
    #     #         log.error("所有参数值为非法数据组合测试用例生成异常，异常原因：{}".format(e))
    #     #
    #     # param_value_long_zh_case_list.append(case_7)
    #     # param_value_long_zh_case_list.append(case_8)
    #     # param_value_long_zh_case_list.append(case_9)
    #     # param_value_long_zh_case_list.append(case_10)
    #
    #     for name in en_name_list:
    #         try:
    #             case_1 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #             case_2 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #             case_1[name] = ""
    #             if count < 15:
    #                 case_1["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
    #                 case_1["case_desc"] = '必填参数-<{}>值为空-其它参数正确填写-申请失败'.format(name)
    #                 case_1["expect"] = '"success":false'
    #             elif name == 'authPrice':
    #                 case_1["case_target"] = "申请失败-authPrice进行非法参数类型验证"
    #                 case_1["case_desc"] = '非必填参数-协议价格<{}>值为空（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                 case_1["expect"] = '"success":false'
    #             elif name == 'authAllowType':
    #                 case_1["case_target"] = "申请失败-authAllowType进行非法参数类型验证"
    #                 case_1["case_desc"] = '非必填参数-授权许可类型<{}>参数值为空（整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                 case_1["expect"] = '"success":false'
    #             else:
    #                 case_1["case_target"] = "申请成功-非必填参数内容不做校验"
    #                 case_1["case_desc"] = '非必填参数<{}>值为空-其它参数正确填写-申请成功'.format(name)
    #                 case_1["expect"] = '"success":true'
    #             param_value_None_case_list.append(case_1)
    #
    #             case_2[name] = ' '
    #             if count < 15:
    #                 case_2["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
    #                 case_2["case_desc"] = '必填参数-<{}>值为空格时-其它参数正确填写-申请失败'.format(name)
    #                 case_2["expect"] = '"success":false'
    #             elif name == 'authPrice':
    #                 case_2["case_target"] = "申请失败-authPrice进行参数类型验证"
    #                 case_2["case_desc"] = '非必填参数-协议价格<{}>值为空格（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                 case_2["expect"] = '"success":false'
    #             elif name == 'authAllowType':
    #                 case_2["case_target"] = "申请失败-authAllowType进行参数类型验证"
    #                 case_2["case_desc"] = '非必填参数-授权许可类型<{}>值为空格（整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                 case_2["expect"] = '"success":false'
    #             else:
    #                 case_2["case_target"] = "申请成功-非必填参数内容不做校验"
    #                 case_2["case_desc"] = '非必填参数-<{}>值为空格-其它参数正确填写-申请成功'.format(name)
    #                 case_2["expect"] = '"success":true'
    #             param_value_space_case_list.append(case_2)
    #
    #
    #             for keyword  in self.java_keyword_list:
    #                 case_3 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #                 case_3[name] = keyword
    #                 if count < 15:
    #                     case_3["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
    #                     case_3["case_desc"] = '必填参数-<{}>值为JAVA关键字：{}-其它参数正确填写-申请失败'.format(name,keyword)
    #                     case_3["expect"] = '"success":false'
    #                 elif name == 'authPrice':
    #                     case_3["case_target"] = "申请失败-authPrice进行参数类型验证"
    #                     case_3["case_desc"] = '非必填参数-协议价格<{}>值为JAVA关键字：{}-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,keyword)
    #                     case_3["expect"] = '"success":false'
    #                 elif name == 'authAllowType':
    #                     case_3["case_target"] = "申请失败-authAllowType进行参数类型验证"
    #                     case_3["case_desc"] = '非必填参数-授权许可值为JAVA关键字：{}-（整型进行类型验证）-其它参数正确填写-申请失败'.format(keyword)
    #                     case_3["expect"] = '"success":false'
    #                 else:
    #                     case_3["case_target"] = "申请成功-非必填参数内容不做校验"
    #                     case_3["case_desc"] = '非必填参数-<{}>值为JAVA关键字：{}-其它参数正确填写-申请成功'.format(name,keyword)
    #                 param_value_keyword_case_list.append(case_3)
    #
    #             for js in self.js_list:
    #                 case_4 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #                 case_4[name] = js
    #                 if count < 15:
    #                     case_4["case_target"] = "申请失败-必填参数内容-格式-类型进行正确及安全性验"
    #                     case_4["case_desc"] = '必填参数-<{}>值为js-其它参数正确填写-申请失败'.format(name)
    #                     case_4["expect"] = '"success":false'
    #                 elif name == 'authPrice':
    #                     case_4["case_target"] = "申请失败-authPrice进行参数类型及安全性验证"
    #                     case_4["case_desc"] = '非必填参数-协议价格<{}>值为js（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                     case_4["expect"] = '"success":false'
    #                 elif name == 'authAllowType':
    #                     case_4["case_target"] = "申请失败-authAllowType进行参数类型及安全性验证"
    #                     case_4["case_desc"] = '非必填参数-授权许可类型<{}>值为js（整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                     case_4["expect"] = '"success":false'
    #                 else:
    #                     case_4["case_target"] = "申请成功-非必填参数内容不做校验"
    #                     case_4["case_desc"] = '非必填参数<{}>值为空-其它参数正确填写-申请成功-但仅为字符串方式存入'.format(name)
    #                     case_4["expect"] = '"success":true'
    #                 param_value_js_case_list.append(case_4)
    #
    #             #for schr in self.spe_chr:
    #                 #case_5 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #                 # case_5[name] = schr
    #                 # if count < 15:
    #                 #     case_5["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
    #                 #     case_5["case_desc"] = '必填参数-<{}>值为特殊字符-其它参数正确填写-申请失败'.format(name)
    #                 #     case_5["expect"] = '"success":false'
    #                 # elif name == 'authPrice':
    #                 #     case_5["case_target"] = "申请失败-authPrice进行参数类型验证"
    #                 #     case_5["case_desc"] = '非必填参数-协议价格<{}>值为特殊字符-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                 #     case_5["expect"] = '"success":false'
    #                 # elif name == 'authAllowType':
    #                 #     case_5["case_target"] = "申请失败-authAllowType进行参数类型验证"
    #                 #     case_5["case_desc"] = '非必填参数-授权许可<{}>值为特殊字符-（整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
    #                 #     case_5["expect"] = '"success":false'
    #                 # elif name == 'applyName':
    #                 #     case_5["case_target"] = "申请失败-applyName进行非法数据-特殊字符验证"
    #                 #     case_5["case_desc"] = '必填参数-申请人<{}>值为特殊字符-其它参数正确填写-申请失败'.format(name)
    #                 #     case_5["expect"] = '"success":false'
    #                 # elif name == 'OpusName':
    #                 #     case_5["case_target"] = "申请失败-OpusName进行非法数据-特殊字符验证"
    #                 #     case_5["case_desc"] = '必填参数-作品名称<{}>值为特殊字符-其它参数正确填写-申请失败'.format(name)
    #                 #     case_5["expect"] = '"success":false'
    #                 # elif name == 'opusDescribe':
    #                 #     case_5["case_target"] = "申请失败-opusDescribe进行非法数据-特殊字符验证"
    #                 #     case_5["case_desc"] = '必填参数-作品描述<{}>值为特殊字符-其它参数正确填写-申请失败'.format(name)
    #                 #     case_5["expect"] = '"success":false'
    #                 # else:
    #                 #     case_5["case_target"] = "申请成功-非必填参数内容不做校验-特殊字符"
    #                 #     case_5["case_desc"] = '非必填参数-<{}>值为特殊字符-其它参数正确填写-申请成功'.format(name)
    #                 #     case_5["expect"] = '"success":true'
    #                 #param_value_spec_case_list.append(case_5)
    #
    #             for long_text in  self.long_value_list:
    #                 case_6 = deepcopy(self.tsa_p_d.deal_param()[1])  # 拷贝测试用例第二条
    #                 case_6[name] = long_text
    #                 if count < 15:
    #                     case_6["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
    #                     case_6["case_desc"] = '必填参数-<{}>值超长-其它参数正确填写-申请失败'.format(name)
    #                     case_6["expect"] = '"success":false'
    #                 else:
    #                     case_6["case_target"] = "申请失败-返回请求错误信息"
    #                     case_6["case_desc"] = '非必填参数<{}>值超长-其它参数正确填写-申请成功'.format(name)
    #                     case_6["expect"] = '"success":false'
    #                 param_value_long_case_list.append(case_6)
    #         except Exception as e:
    #             log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
    #         count += 1
    #         break
    #     print(count)
    #     #print(len(param_value_None_case_list)+len(param_value_space_case_list)+len(param_value_keyword_case_list)+len(param_value_js_case_list)+len(param_value_spec_case_list))
    #     end = time.time()
    #     elapsed = end_time-start_time #耗时
    #     print(elapsed)
    #     all_list.extend(param_value_None_case_list)
    #     all_list.extend(param_value_space_case_list)
    #     all_list.extend(param_value_keyword_case_list)
    #     all_list.extend(param_value_js_case_list)
    #     all_list.extend(param_value_spec_case_list)
    #     all_list.extend(param_value_long_zh_case_list)
    #     return all_list

    def make_data_param_no_case(self,caseid,start=0,end=0):
        '''
        55个参数不传入测试用例
        start:表示从第几个用例开始执行
        end:表示到第几个用例结束
        :return:
        '''
        start_time = time.time()
        param_no_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = start
        name_l = []
        if end == 0:
            end = len(en_name_list)
        for name in en_name_list[start:end]:
            try:
                    name_l.append(name)
                    case_3 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                    if name != "salt":
                        del case_3[name]
                        salt = self.tsa_p_d.get_salt(case_3)
                        case_3["salt"] = salt
                    if count < 15 and name != "hash" and name != "file":
                        case_3["TestTarget"] = "申请失败-必填参数缺失"
                        case_3["CaseDesc"] = '必填参数-<{}>不传入-其它参数正确填写-申请失败'.format(name)
                        case_3["ExpectValue"] = '{"msg":"%s参数不完全","success":false,"resultCode":"0202002"}'%name
                        case_3["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    elif count<15 and (name == "hash" or name == "file"):
                        case_3["TestTarget"] = "申请成功-非必填参数缺失"
                        case_3["CaseDesc"] = '选择性必填参数-<{}>不传入-其它参数正确填写-申请成功'.format(name)
                        case_3["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_3["ExpCallbackFlag"] = '{"callbackFlag":true}'
                    else:
                        case_3["TestTarget"] = "申请成功-非必填参数缺失"
                        case_3["CaseDesc"] = '非必填参数-<{}>不传入-其它参数正确填写-申请成功'.format(name)
                        case_3["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_3["ExpCallbackFlag"] = '{"callbackFlag":true}'
                    param_no_case_list.append(case_3)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_no_case_list)
        return all_list

    def make_data_param_value_None_fail(self,caseid=0,start=0,end=0):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        ='' 空
        :return:
        '''
        start_time = time.time()
        param_value_None_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = start
        if end == 0:
            end = len(en_name_list)
        for name in en_name_list[start:end]:
            try:
                    case_1 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                    case_1[name] = ""
                    if name != "salt":
                        salt = self.tsa_p_d.get_salt(case_1)
                        case_1["salt"] = salt
                    if count < 15 and name != "hash" and name != "file": #参数为空/空格/null和不传都判断为不传 返回参数不完全
                        case_1["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_1["CaseDesc"] = '必填参数-<{}>值为空-其它参数正确填写-申请失败'.format(name)
                        case_1["ExpectValue"] = '{"msg":"%s参数不完全","success":false,"resultCode":"0202002"}'%name
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    elif count < 15 and (name == "hash" or name == "file"):
                        case_1["TestTarget"] = "申请成功-非必填参数内容不做校验"
                        case_1["CaseDesc"] = '选择性必填参数<{}>值为空-其它参数正确填写-申请成功'.format(name)
                        case_1["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":true}'
                    else:
                        case_1["TestTarget"] = "申请成功-非必填参数内容不做校验"
                        case_1["CaseDesc"] = '非必填参数<{}>值为空-其它参数正确填写-申请成功'.format(name)
                        case_1["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":true}'
                    case_1["space_name"] = name
                    param_value_None_case_list.append(case_1)

            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_None_case_list)
        return all_list

    def make_data_param_value_space_fail(self,caseid,start=0,end=0):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =' ' 空格
        :return:
        '''
        start_time = time.time()
        param_value_space_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = start
        keys = ["IsRun", "CaseID", "TestTarget", "CaseDesc", "ExpectValue", "partnerID", "partnerKey", "res_serialNo",
                "res_download", "is_download", "is_pass"]
        if end == 0:
            end = len(en_name_list)
        for name in en_name_list:
            try:
                    case_1 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                    case_1[name] = "   "
                    if name != "salt":
                        salt = self.tsa_p_d.get_salt(case_1,name_space=name)
                        case_1["salt"] = salt
                    # if name == "partnerID" or name == "partnerKey":
                    #     case_1["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                    #     case_1["CaseDesc"] = '必填参数-<{}>值为三个空格-其它参数正确填写-申请失败'.format(name)
                    #     case_1["ExpectValue"] = '{"success":false,"resultCode":"0203001"}'

                    if count < 15 and  name != "file" and name !="hash":
                        case_1["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_1["CaseDesc"] = '必填参数-<{}>值为三个空格-其它参数正确填写-申请失败'.format(name)
                        case_1["ExpectValue"] = '{"msg":"%s参数不完全","success":false,"resultCode":"0202002"}'%name
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    elif count < 15 and  (name == "file" or name =="hash"):
                        case_1["TestTarget"] = "申请成功-非必填参数内容不做校验"
                        case_1["CaseDesc"] = '选择性必填参数<{}>值为三个空格-其它参数正确填写-申请成功'.format(name)
                        case_1["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":true}'
                    else:
                        case_1["TestTarget"] = "申请成功-非必填参数内容不做校验"
                        case_1["CaseDesc"] = '非必填参数<{}>值为三个空格-其它参数正确填写-申请成功'.format(name)
                        case_1["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        case_1["ExpCallbackFlag"] = '{"callbackFlag":true}'
                    case_1["space_name"] = name
                    case_1[name] = "   "
                    param_value_space_case_list.append(case_1)
                    #break
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_space_case_list)
        #print(all_list)
        return all_list

    def make_data_param_value_spe_fail(self,caseid):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =特殊字符 ~#￥&——|{}`/ \n \t \r
        :return:
        '''
        start_time = time.time()
        param_value_spec_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0

        for name in en_name_list:
            try:

                for schr in self.spe_chr:
                    case_5 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                    case_5[name] = schr
                    if name == "fileSzieFlag":
                        if name != "salt":
                            salt = self.tsa_p_d.get_salt(case_5)
                            case_5["salt"] = salt
                        if name == "partnerID" or name == "partnerKey":
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"success":false,"resultCode":"0203001"}'
                        elif count < 15 and name not in self.b_name:
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"success":false,"resultCode":"0202001"}'
                        elif count<15 and name in self.int_param:
                            case_5["TestTarget"] = "申请失败-进行参数类型验证"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"status":400}'
                        elif count<15:
                            case_5["TestTarget"] = "申请成功-进行参数特殊字符验证"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请成功'.format(name,schr)
                            case_5["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        elif name in self.int_param:
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '非必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"status":400}'
                        else:
                            case_5["TestTarget"] = "申请成功-进行参数特殊字符验证"
                            case_5["CaseDesc"] = '非必填参数-<{}>值为特殊字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请成功'.format(name,schr)
                            case_5["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                        param_value_spec_case_list.append(case_5)
                    else:
                        continue
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_spec_case_list)
        return all_list

    def make_data_param_value_type_fail(self,caseid,start=0,end=0):
        '''
        整型类型错误用例
        值为以下几种情况：
        int_param = ["fileSzieFlag","fileType","opusState","opusStore","opusType","opusCreativeType","opusCreativeNature","applyType","applyUserType",
                 "applyIDType","authType","authValidiy","authBusiness","authPrice","authAllowType","authSell",
                 "authUserType","authUserIDType"]
        :return:
        '''
        spe_chr = ["abcdf","你好中国"]
        start_time = time.time()
        param_value_spec_case_list = []

        all_list = []
        en_name_list = self.int_param
        count = start
        if end == 0:
            end = len(en_name_list)
        for name in en_name_list[start:end]:
            try:
                for schr in spe_chr:
                        case_5 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                        case_5[name] = schr
                        if count<15 and name in self.int_param:
                            case_5["TestTarget"] = "申请失败-进行参数类型验证"
                            case_5["CaseDesc"] = '必填参数-<{}>值类型错误<{}>-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"status":400}'
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        else:
                            case_5["TestTarget"] = "申请失败-进行参数类型验证"
                            case_5["CaseDesc"] = '非必填参数-<{}>值类型错误<{}>-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name, schr)
                            case_5["ExpectValue"] = '{"status":400}'
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        param_value_spec_case_list.append(case_5)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
            #break

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_spec_case_list)
        return all_list

    def make_data_param_value_long_1_fail(self,caseid,start=0,end=0):
        '''
        参数值超长1个
        值为以下几种情况：
        int_param = ["fileType""opusStore","opusType","opusCreativeType","opusCreativeNature","applyType","applyUserType",
                 "applyIDType","authType","authValidiy","authPrice",
                 "authUserType","authUserIDType"]
                 ["fileSzieFlag","opusState","authBusiness","authAllowType","authSell"]
        :return:
        '''
        start_time = time.time()
        param_value_spec_case_list = []

        int_param = ["fileType""opusStore","opusType","opusCreativeType","opusCreativeNature","applyType","applyUserType",
                 "applyIDType","authType","authValidiy","authPrice",
                 "authUserType","authUserIDType","fileType"]
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        #self.int_param
        count = start
        en_name_list.remove("partnerID")
        en_name_list.remove("partnerKey")
        en_name_list.remove("file")
        en_name_list.remove("salt")
        en_name_list.remove("authProtocol")
        if end == 0:
            end = len(en_name_list)
        for name in en_name_list[start:end]:
            try:
                    case_5 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                    if name in self.int_param:
                        if int(case_5[name]) == 0:
                            case_5[name] = 10
                        else:
                            case_5[name] = str(case_5[name])+"1"
                    else:
                        case_5[name] = str(case_5[name])+"s"
                    if name != "salt":
                        salt = self.tsa_p_d.get_salt(case_5)
                        case_5["salt"] = salt

                    if count<15 and name:
                        case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_5["CaseDesc"] = '必填参数-<{}>值位数超出限制1位-其它参数正确填写-申请失败'.format(name)
                        case_5["ExpectValue"] = '{"msg":"%s参数不合法","success":false,"resultCode":"0202001"}'%name
                        case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    # elif count<15 and name in int_param:
                    #     case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                    #     case_5["CaseDesc"] = '必填参数-<{}>值位数超出限制1位-其它参数正确填写-申请失败'.format(name)
                    #     case_5["ExpectValue"] = '400'
                    #     case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    # elif name in int_param:
                    #     case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                    #     case_5["CaseDesc"] = '非必填参数-<{}>值位数超出限制1位-其它参数正确填写-申请失败'.format(name)
                    #     case_5["ExpectValue"] = '400'
                    #     case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    else:
                        case_5["TestTarget"] = "申请失败-进行参数类型验证"
                        case_5["CaseDesc"] = '非必填参数-<{}>值位数超出限制1位-其它参数正确填写-申请失败'.format(name)
                        case_5["ExpectValue"] = '{"msg":"%s参数不合法","success":false,"resultCode":"0202001"}'%name
                        case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                    param_value_spec_case_list.append(case_5)

                    #break
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
            #break

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_spec_case_list)
        return all_list


    def make_data_param_value_spe_fail_b(self,caseid,start=0,end=0):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =禁止特殊符号（～#￥&×——|}{`|/_），不支持\r\n。
        :return:
        '''
        start_time = time.time()
        param_value_spec_case_list = []

        all_list = []
        en_name_list = ["opusName","opusDescribe","applyName"]
        count = start
        if end == 0:
            end = len(en_name_list)
        for name in en_name_list[start:end]:
            try:
                for schr in self.spe_chr:
                        case_5 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                        case_5[name] = schr
                        if name != "salt":
                            salt = self.tsa_p_d.get_salt(case_5)
                            case_5["salt"] = salt
                        if name == "partnerID" or name == "partnerKey":
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"msg":"用户名或密码错误","success":false,"resultCode":"0203001"}'
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        elif schr =="\n" or schr =="\r" :
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"msg":"%s参数不完全","success":false,"resultCode":"0202002"}'%name
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        elif count < 15 and name not in self.b_name :
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"msg":"%s参数不合法","success":false,"resultCode":"0202001"}'%name
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        elif count<15 and name in self.int_param:
                            case_5["TestTarget"] = "申请失败-进行参数类型验证"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = "400"
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        elif count<15:
                            case_5["TestTarget"] = "申请成功-进行参数特殊字符验证"
                            case_5["CaseDesc"] = '必填参数-<{}>值为特殊字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请成功'.format(name,schr)
                            case_5["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":true}'
                        elif name in self.int_param:
                            case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                            case_5["CaseDesc"] = '非必填参数-<{}>值为特殊字符<{}>-其它参数正确填写-申请失败'.format(name,schr)
                            case_5["ExpectValue"] = '{"msg":"%s参数不合法","success":false,"resultCode":"0202001"}'%name
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":None}'
                        else:
                            case_5["TestTarget"] = "申请成功-进行参数特殊字符验证"
                            case_5["CaseDesc"] = '非必填参数-<{}>值为特殊字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请成功'.format(name,schr)
                            case_5["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                            case_5["ExpCallbackFlag"] = '{"callbackFlag":true}'
                        param_value_spec_case_list.append(case_5)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_spec_case_list)
        return all_list

    def make_data_param_value_long_fail(self,caseid):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =超长
        :return:
        '''
        start_time = time.time()
        param_value_long_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0

        for name in en_name_list:
            try:
                for long_text in  self.long_value_list[:1]:
                    case_5 = deepcopy(self.tsa_p_d.deal_param(flag=1)[caseid])  # 拷贝测试用例第二条
                    case_5[name] = long_text
                    if name != "salt":
                        salt = self.tsa_p_d.get_salt(case_5)
                        case_5["salt"] = salt
                    if name == "partnerID" or name == "partnerKey":
                        case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_5["CaseDesc"] = '必填参数-<{}>值为超长字符<{}>-其它参数正确填写-申请失败'.format(name,long_text)
                        case_5["ExpectValue"] = '{"msg":"用户名或密码错误","success":false,"resultCode":"0203001"}'
                    elif count < 15 and name not in self.b_name:
                        case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_5["CaseDesc"] = '必填参数-<{}>值为超长字符<{}>-其它参数正确填写-申请失败'.format(name,long_text)
                        case_5["ExpectValue"] = '{"msg":"%s参数错误","success":false,"resultCode":"0202001"}'%name
                    elif count<15 and name in self.int_param:
                        case_5["TestTarget"] = "申请失败-进行参数类型验证"
                        case_5["CaseDesc"] = '必填参数-<{}>值为超长字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,long_text)
                        case_5["ExpectValue"] = "400"
                    elif count<15:
                        case_5["TestTarget"] = "申请成功-进行参数特殊字符验证"
                        case_5["CaseDesc"] = '必填参数-<{}>值为超长字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请成功'.format(name,long_text)
                        case_5["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                    elif name in self.int_param:
                        case_5["TestTarget"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_5["CaseDesc"] = '非必填参数-<{}>值为超长字符<{}>-其它参数正确填写-申请失败'.format(name,long_text)
                        case_5["ExpectValue"] = '{"msg":"%s参数错误","success":false,"resultCode":"0202001"}'%name
                    else:
                        case_5["TestTarget"] = "申请成功-进行参数特殊字符验证"
                        case_5["CaseDesc"] = '非必填参数-<{}>值为超长字符<{}>-（长整型进行类型验证）-其它参数正确填写-申请成功'.format(name,long_text)
                        case_5["ExpectValue"] = '{"success":true,"resultCode":"0204000"}'
                    param_value_long_case_list.append(case_5)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_long_case_list)
        return all_list



    def make_data_param_value_keyword_fail(self,caseid):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =java 关键字
        :return:
        '''
        start_time = time.time()
        param_value_keyword_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0

        for name in en_name_list:
            try:
                for keyword  in self.java_keyword_list:
                    case_3 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                    case_3[name] = keyword
                    if count < 15:
                        case_3["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_3["case_desc"] = '必填参数-<{}>值为JAVA关键字：{}-其它参数正确填写-申请失败'.format(name,keyword)
                        case_3["expect"] = '"success":false'
                    elif name == 'authPrice':
                        case_3["case_target"] = "申请失败-authPrice进行参数类型验证"
                        case_3["case_desc"] = '非必填参数-协议价格<{}>值为JAVA关键字：{}-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,keyword)
                        case_3["expect"] = '"success":false'
                    elif name == 'authAllowType':
                        case_3["case_target"] = "申请失败-authAllowType进行参数类型验证"
                        case_3["case_desc"] = '非必填参数-授权许可值为JAVA关键字：{}-（整型进行类型验证）-其它参数正确填写-申请失败'.format(keyword)
                        case_3["expect"] = '"success":false'
                    else:
                        case_3["case_target"] = "申请成功-非必填参数内容不做校验"
                        case_3["case_desc"] = '非必填参数-<{}>值为JAVA关键字：{}-其它参数正确填写-申请成功'.format(name,keyword)
                    param_value_keyword_case_list.append(case_3)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_keyword_case_list)
        return all_list

    def make_data_param_value_js_fail(self,caseid):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =js <script>alter(123456)</script>
        :return:
        '''
        start_time = time.time()
        param_value_js_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0

        for name in en_name_list:
            try:
                for js in self.js_list:
                    case_4 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                    case_4[name] = js
                    if count < 15 and (name not in self.int_param and name not in self.long_20 and name not in self.b_name):
                        case_4["case_target"] = "申请失败-必填参数内容-格式-类型进行正确及安全性验"
                        case_4["case_desc"] = '必填参数-<{}>值为js-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = '"success":false'
                    elif count < 15 and name in self.int_param:
                        case_4["case_target"] = "申请失败-进行参数类型及安全性验证"
                        case_4["case_desc"] = '必填参数-<{}>值为js（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = "400"
                    elif count < 15 and name in self.long_20:
                        case_4["case_target"] = "申请失败-进行参数类型及安全性验证"
                        case_4["case_desc"] = '必填参数-<{}>值为js（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = '"success":false'
                    elif count < 15:
                        case_4["case_target"] = "申请成功-进行参数类型及安全性验证"
                        case_4["case_desc"] = '必填参数-<{}>值为js（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = '"success":true'
                    elif name in self.int_param and name not in self.long_20:
                        case_4["case_target"] = "申请失败-进行参数类型及安全性验证"
                        case_4["case_desc"] = '非必填参数-<{}>值为js（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = "400"
                    elif name in self.long_20:
                        case_4["case_target"] = "申请失败-进行参数类型及安全性验证"
                        case_4["case_desc"] = '非必填参数-<{}>值为js（整型进行类型验证）-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = '"success":false'
                    else:
                        case_4["case_target"] = "申请成功-非必填参数内容不做校验"
                        case_4["case_desc"] = '非必填参数<{}>值为js-其它参数正确填写-申请成功-但仅为字符串方式存入'.format(name)
                        case_4["expect"] = '"success":true'
                    param_value_js_case_list.append(case_4)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_js_case_list)
        return all_list


    def make_data_param_value_sql_fail(self,caseid):
        '''
        55个参数值为无效的测试用例
        值为以下几种情况：
        =sql “exec”,”xp_”,”sp_”,”declare”,”Union”,”cmd”,”+”,”//”,”..”,”;”,”‘”,”--”,”%”,”0x”,”><=!-*/()|”,和”空格”
        :return:
        '''
        start_time = time.time()
        param_value_sql_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:
            try:
                for keyword  in self.sql_list:
                    case_3 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                    case_3[name] = keyword
                    if count < 15:
                        case_3["case_target"] = "申请失败-必填参数内容-格式-类型进行正确性验"
                        case_3["case_desc"] = '必填参数-<{}>值为SQL关键字：{}-其它参数正确填写-申请失败'.format(name,keyword)
                        case_3["expect"] = '"success":false'
                    elif name == 'authPrice':
                        case_3["case_target"] = "申请失败-authPrice进行参数类型验证"
                        case_3["case_desc"] = '非必填参数-协议价格<{}>值为SQL关键字：{}-（长整型进行类型验证）-其它参数正确填写-申请失败'.format(name,keyword)
                        case_3["expect"] = '"success":false'
                    elif name == 'authAllowType':
                        case_3["case_target"] = "申请失败-authAllowType进行参数类型验证"
                        case_3["case_desc"] = '非必填参数-授权许可值为SQL关键字：{}-（整型进行类型验证）-其它参数正确填写-申请失败'.format(keyword)
                        case_3["expect"] = '"success":false'
                    else:
                        case_3["case_target"] = "申请成功-非必填参数内容不做校验"
                        case_3["case_desc"] = '非必填参数-<{}>值为SQL关键字：{}-其它参数正确填写-申请成功'.format(name,keyword)
                        param_value_sql_case_list.append(case_3)
            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1

        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_value_sql_case_list)
        return all_list




    def make_data_param_spaceqh_case(self,caseid):
        '''
        55个参数不传入测试用例
        :return:
        '''
        start_time = time.time()
        param_no_case_list = []

        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:
            try:
                case_3 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条

                if count < 15 and name != "hash" and name != "file":
                    case_3["case_target"] = "申请失败-必填参数缺失"
                    case_3["case_desc"] = '必填参数-<{}>不传入-其它参数正确填写-申请失败'.format(name)
                    case_3["expect"] = '{"success":false,"resultCode":"0202002"}'
                else:
                    case_3["case_target"] = "申请成功-非必填参数缺失"
                    case_3["case_desc"] = '非必填参数-<{}>不传入-其它参数正确填写-申请成功'.format(name)
                    case_3["expect"] = '{"success":true,"resultCode":"0204000"}'
                del case_3[name]
                param_no_case_list.append(case_3)

            except Exception as e:
                log.error("编写参数值非法数据测试用例出现异常，异常原因：{}".format(e))
            count += 1
        end_time = time.time()
        elapsed = end_time-start_time #耗时
        all_list.extend(param_no_case_list)
        return all_list


    def make_data_param_name_None_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        ='' 空
        :return:
        '''
        start_time = time.time()
        param_name_None_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:
            try:
                case_1 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                case_1[""] = case_1.pop(name)
                case_1["case_target"] = "申请失败-参数名错误验证"
                if count<15 and name != "file"  and name !="hash":
                    case_1["case_desc"] = '必填参数-<{}>名为空-参数值正确-其它参数正确填写-申请失败'.format(name)
                    case_1["expect"] = '"success":false'
                elif name == "file"  or name =="hash":
                    case_1["case_desc"] = '必填参数-<{}>名为空-参数值正确-其它参数正确填写-申请成功'.format(name)
                    case_1["expect"] = '"success":true'
                else:
                    case_1["case_desc"] = '非必填参数-<{}>名为空-参数值正确-其它参数正确填写-申请失败'.format(name)
                    case_1["expect"] = '"success":true'
                param_name_None_case_list.append(case_1)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数={}，异常原因：{}".format(name,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_None_case_list)
        return all_list


    def make_data_param_name_space_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =' ' 空格
        :return:
        '''
        start_time = time.time()
        param_name_space_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:
            try:
                case_2 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                case_2[" "] = case_2.pop(name)
                case_2["case_target"] = "申请失败-参数名错误验证"
                if count<15 and name != "file"  and name !="hash":
                    case_2["case_desc"] = '必填参数-<{}>名为空格-参数值正确-其它参数正确填写-申请失败'.format(name)
                    case_2["expect"] = '"success":false'
                elif name == "file"  or name =="hash":
                    case_2["case_desc"] = '必填参数-<{}>名为空格-参数值正确-其它参数正确填写-申请成功'.format(name)
                    case_2["expect"] = '"success":true'
                else:
                    case_2["case_desc"] = '非必填参数-<{}>名为空格-参数值正确-其它参数正确填写-申请失败'.format(name)
                    case_2["expect"] = '"success":true'
                param_name_space_case_list.append(case_2)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数名={}，异常原因：{}".format(name,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_space_case_list)
        return all_list

    def make_data_param_name_keyword_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =java 关键字
        :return:
        '''
        start_time = time.time()
        param_name_keyword_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:

            try:
                for keyword  in self.java_keyword_list:
                    case_3 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条

                    case_3[str(keyword)] = case_3.pop(name)
                    case_3["case_target"] = "申请失败-参数名错误验证"
                    if count < 15 and name != "file" and name != "hash":
                        case_3["case_desc"] = '必填参数-<{}>名为JAVA关键字-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_3["expect"] = '"success":false'
                    elif name == "file" or name == "hash":
                        case_3["case_desc"] = '必填参数-<{}>名为JAVA关键字-参数值正确-其它参数正确填写-申请成功'.format(name)
                        case_3["expect"] = '"success":true'
                    else:
                        case_3["case_desc"] = '非必填参数-<{}>名为JAVA关键字-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_3["expect"] = '"success":true'
                    param_name_keyword_case_list.append(case_3)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数名={},keyword={}，异常原因：{}".format(name,keyword,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_keyword_case_list)
        return all_list

    def make_data_param_name_js_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =js <script>alter(123456)</script>
        :return:
        '''
        start_time = time.time()
        param_name_js_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:

            try:
                for js in self.js_list:
                    case_4 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条

                    case_4[js] = case_4.pop(name)
                    case_4["case_target"] = "申请失败-参数名错误验证"
                    if count < 15 and name != "file" and name != "hash":
                        case_4["case_desc"] = '必填参数-<{}>名为JS脚本-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = '"success":false'
                    elif name == "file" or name == "hash":
                        case_4["case_desc"] = '必填参数-<{}>名为JS-参数值正确-其它参数正确填写-申请成功'.format(name)
                        case_4["expect"] = '"success":true'
                    else:
                        case_4["case_desc"] = '非必填参数-<{}>名为JS脚本-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_4["expect"] = '"success":true'
                    param_name_js_case_list.append(case_4)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数名={}，异常原因：{}".format(name,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_js_case_list)
        return all_list

    def make_data_param_name_sql_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =sql “exec”,”xp_”,”sp_”,”declare”,”Union”,”cmd”,”+”,”//”,”..”,”;”,”‘”,”--”,”%”,”0x”,”><=!-*/()|”,和”空格”
        :return:
        '''
        start_time = time.time()
        param_name_sql_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:

            try:
                for keyword  in self.sql_list:
                    case_3 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条

                    case_3[str(keyword)] = case_3.pop(name)
                    case_3["case_target"] = "申请失败-参数名错误验证"
                    if count < 15 and name != "file" and name != "hash":
                        case_3["case_desc"] = '必填参数-<{}>名为sql关键字<{}>-参数值正确-其它参数正确填写-申请失败'.format(name,keyword)
                        case_3["expect"] = '"success":false'
                    elif name == "file" or name == "hash":
                        case_3["case_desc"] = '必填参数-<{}>名为sql关键字-参数值正确-其它参数正确填写-申请成功'.format(name)
                        case_3["expect"] = '"success":true'
                    else:
                        case_3["case_desc"] = '非必填参数-<{}>名为sql关键字<{}>-参数值正确-其它参数正确填写-申请失败'.format(name,keyword)
                        case_3["expect"] = '"success":true'
                    param_name_sql_case_list.append(case_3)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,keyword={}，异常原因：{}".format(keyword,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_sql_case_list)
        return all_list

    def make_data_param_name_spec_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =特殊字符 ~`！@#￥%……&*（）——+|、】【}{【？、》，《<>,. \n \t \r
        :return:
        '''
        start_time = time.time()
        param_name_spec_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:
            try:
                for s_chr in self.spe_chr:
                    case_5 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                    case_5[s_chr] = case_5.pop(name)
                    case_5["case_target"] = "申请失败-参数名错误验证"
                    if count<15 and name != "file"  and name !="hash":
                        case_5["case_desc"] = '必填参数-<{}>名为特殊字符-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_5["expect"] = '"success":false'
                    elif name == "file" or name == "hash":
                        case_5["case_desc"] = '必填参数-<{}>名为特殊字符--参数值正确-其它参数正确填写-申请成功'.format(name)
                        case_5["expect"] = '"success":true'
                    else:
                        case_5["case_desc"] = '非必填参数-<{}>名为特殊字符-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_5["expect"] = '"success":true'
                    param_name_spec_case_list.append(case_5)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数名={}，异常原因：{}".format(name,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_spec_case_list)
        return all_list

    def make_data_param_name_spec_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =特殊字符 ~`！@#￥%……&*（）——+|、】【}{【？、》，《<>,. \n \t \r
        :return:
        '''
        start_time = time.time()
        param_name_spec_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:
            try:
                for s_chr in self.spe_chr:
                    case_5 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                    case_5[s_chr] = case_5.pop(name)
                    case_5["case_target"] = "申请失败-参数名错误验证"
                    if count<15 and name != "file"  and name !="hash":
                        case_5["case_desc"] = '必填参数-<{}>名为特殊字符-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_5["expect"] = '"success":false'
                    elif name == "file" or name == "hash":
                        case_5["case_desc"] = '必填参数-<{}>名为特殊字符--参数值正确-其它参数正确填写-申请成功'.format(name)
                        case_5["expect"] = '"success":true'
                    else:
                        case_5["case_desc"] = '非必填参数-<{}>名为特殊字符-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_5["expect"] = '"success":true'
                    param_name_spec_case_list.append(case_5)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数名={}，异常原因：{}".format(name,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_spec_case_list)
        return all_list

    def make_data_param_name_long_fail(self,caseid):
        '''
        55个参数名为无效的测试用例
        值为以下几种情况：
        =超长
        :return:
        '''
        start_time = time.time()
        param_name_long_case_list = []
        all_list = []
        en_name_list = self.param.get_param_en_name_list()
        count = 0
        for name in en_name_list:

            try:
                for s_chr in self.long_value_list:
                    case_6 = deepcopy(self.tsa_p_d.deal_param()[caseid])  # 拷贝测试用例第二条
                    case_6[s_chr] = case_6.pop(name)
                    case_6["case_target"] = "申请失败-参数名长度超长"
                    if count < 15  and  name != "file" and name != "hash":
                        case_6["case_desc"] = '必填参数-<{}>名长度超长-参数值正确-其它参数正确填写-申请失败'.format(name)
                    elif name == "file" or name == "hash":
                        case_6["case_desc"] = '必填参数-<{}>名长度超长--参数值正确-其它参数正确填写-申请成功'.format(name)
                        case_6["expect"] = '"success":true'
                    else:
                        case_6["case_desc"] = '非必填参数-<{}>名长度超长-参数值正确-其它参数正确填写-申请失败'.format(name)
                        case_6["expect"] = '"success":true'
                    param_name_long_case_list.append(case_6)
            except Exception as e :
                log.error("编写参数名非法数据测试用例出现异常,参数名为={}，异常原因：{}".format(name,e))

            count += 1
        end_time = time.time()
        elapsed = end_time - start_time
        all_list.extend(param_name_long_case_list)
        return all_list


if __name__ == "__main__":
    ce = CaseError()
    #ce.make_data_param_no_case(1)
    #ce.make_data_param_value_spe_fail_b(1)
    #ce.make_data_param_value_space_fail(1)
    ce.make_data_param_value_long_1_fail(59)