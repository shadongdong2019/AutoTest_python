import logging
log = logging.getLogger("__file__")
class ParamGlobal:
    '''
    获取参数名相关从息
    第一列：参数中文名
    第二列：参数英文名（代码中显示）
    第三列：参数值长度
    第四列：参数值类型
    第五列：参数是否在请求接口中传入-no表示不在请求接口中传入，yes-表示需要在请求接口中传入
    第六列：表示参数是否为必传项，nb表示非必传项，b表示必传项

    注：参数中文名前面首字母为大F表示此参数为文件类型，需要转为文件流进行传输
    '''
    def __init__(self,param_name_list):
        self.param_name_list = param_name_list

    def deal_param_name_tuple(self,param_name_list):
        '''
        获取参数名的中文名/英文名/
        :param param_name_list:
        :return:
        '''
        param_zh_name_list = [] #参数中文名列表
        param_en_name_list = [] #参数英文名列表
        param_len_dict = {}     #参数最大长度列表
        param_value_type = {}   #参数类型 列表
        no_param_list = []      #不在请求中发送的参数列表
        yes_param_list = []     #需要在请求中发送的参数列表
        nb_param_list = []      #非必传参数列表
        b_param_list = []       #必传参数列表
        param_file_list = []    #参数类型为文件类型列表
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            for param_name in self.param_name_list[0]:
                p_zh_name = str(param_name).split("-")[0] #参数中文名
                p_en_name = str(param_name).split("-")[1] #参数英文名
                p_len = str(param_name).split("-")[2] #参数最大长度
                p_type = str(param_name).split("-")[3] #参数类型
                is_request_param = str(param_name).split("-")[4] #是否需要在请求中发送的参数，主要为了区分用例中参数和说明字段
                is_need_param = str(param_name).split("-")[5]  #是否必传参数
                param_zh_name_list.append(p_zh_name)
                param_en_name_list.append(p_en_name)
                param_len_dict[p_en_name] = p_len
                param_value_type[p_en_name] = p_type
                if is_request_param.lower()=="yes":
                    yes_param_list.append(p_en_name)
                else:
                    no_param_list.append(p_en_name)

                if is_need_param.lower()=="b":
                    b_param_list.append(p_en_name)
                else:
                    nb_param_list.append(p_en_name)
                if p_zh_name[0] == "F":
                    param_file_list.append(p_en_name)
        except Exception as e :
            log.error("处理接口请求参数名出现异常，异常原因：{}".format(e))
        return param_zh_name_list,param_en_name_list,param_len_dict,param_value_type,no_param_list,yes_param_list,b_param_list,nb_param_list,param_file_list

    def get_param_zh_name_list(self,param_name_list=None):
        '''
        获取参数中文名列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 中文名参数列表
        '''
        param_zh_list = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_zh_list = self.deal_param_name_tuple(self.param_name_list)[0]
        except Exception as e:
            log.error("获取参数中文名出现异常，异常原因：{}".format(e))
        return param_zh_list

    def get_param_en_name_list(self,param_name_list=None):
        '''
        获取参数英文名列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 英文名参数列表
        '''
        param_en_list = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_en_list = self.deal_param_name_tuple(self.param_name_list)[1]
        except Exception as e:
            log.error("获取参数英文名出现异常，异常原因：{}".format(e))
        return param_en_list


    def get_param_len_dict(self,param_name_list=None):
        '''
        获取参数最大长度字典
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 字典
        '''
        param_len_dict = {}
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_len_dict = self.deal_param_name_tuple(self.param_name_list)[2]
        except Exception as e:
            log.error("获取参数最大长度出现异常，异常原因：{}".format(e))
        return param_len_dict

    def get_param_type_dict(self,param_name_list=None):
        '''
        获取参数类型 字典
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 字典
        '''
        param_type_dict = {}
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_type_dict = self.deal_param_name_tuple(self.param_name_list)[3]
        except Exception as e:
            log.error("获取参数类型出现异常，异常原因：{}".format(e))
        return param_type_dict

    def get_param_no_request_list(self,param_name_list=None):
        '''
        获取不在接口请求中传入的参数列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 列表
        '''
        param_no_req = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_no_req = self.deal_param_name_tuple(self.param_name_list)[4]
        except Exception as e:
            log.error("获取不需要在接口传入的参数列表出现异常，异常原因：{}".format(e))
        return param_no_req

    def get_param_yes_request_list(self,param_name_list=None):
        '''
        获取需要在接口请求中传入的参数列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 列表
        '''
        param_yes_req = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_yes_req = self.deal_param_name_tuple(self.param_name_list)[5]
        except Exception as e:
            log.error("获取需要在接口传入的参数列表出现异常，异常原因：{}".format(e))
        return param_yes_req

    def get_param_b_list(self,param_name_list=None):
        '''
        获取必传参数列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 列表
        '''
        param_b_req = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_b_req = self.deal_param_name_tuple(self.param_name_list)[6]
        except Exception as e:
            log.error("获取必传参数列表出现异常，异常原因：{}".format(e))
        return param_b_req

    def get_param_nb_list(self,param_name_list=None):
        '''
        获取非必传参数列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 列表
        '''
        param_nb_req = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_nb_req = self.deal_param_name_tuple(self.param_name_list)[7]
        except Exception as e:
            log.error("获取非必传参数列表出现异常，异常原因：{}".format(e))
        return param_nb_req

    def get_param_file_list(self,param_name_list=None):
        '''
        获取文件类型的参数列表
        :param param_name_list: 参数名列表（未进行分隔处理）
        :return: 列表
        '''
        param_file = []
        try:
            if param_name_list:
                self.param_name_list = param_name_list
            param_file = self.deal_param_name_tuple(self.param_name_list)[8]
        except Exception as e:
            log.error("获取文件类型的参数列表出现异常，异常原因：{}".format(e))
        return param_file