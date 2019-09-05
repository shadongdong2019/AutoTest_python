import sys
sys.path.append('/home/ma/PycharmProjects/AutoTest_python/InterfaceTest')
import configparser
from configparser import ConfigParser
import logging
import os
log = logging.getLogger("__file__")
class OperationCFG:
    def __init__(self,filename,section):
        try:
            self.filename = filename
            self.section = section
            self.data = self.read_cfg(self.filename)
        except Exception as e:
            log.error("操作cfg/ini配置文件初始化方法异常，异常原因：{}".format(e))


    def read_cfg(self,filename=None):
        '''
        读取配置文件内容
        :param filename:
        :return: ConfigParser对像
        '''
        config = None
        try:
            if filename:
                self.filename = filename
            config = configparser.ConfigParser()
            config.read(self.filename)
        except Exception as e:
            log.error("读取cfg配置文件内容异常，异常原因：{}".format(e))
        return config

    def get_section_key_value(self,*option_args,filename=None,section=None):
        '''
        获取指定section下的option和值，返回字典（key_value对）
        :param filename: 要读取的配置文件全路径名，如果为None自动获取初始化时的文件名
        :param section:  要读取的配置文件中的段名（section），如果为None自动获取初始化时的段名（section）
        :param option_kargs: 传入的选项名，因不同配置文件配置的选项不同，所以此参数为不固定参数
        :return:option_dict
        '''
        try:
            section_dict = {}
            if filename:
                self.filename=filename
                config = self.read_cfg(self.filename)
            else:
                config = self.data

            if section:
                self.section=section

            # 第一个参数指定要读取的段名，第二个是要读取的选项名
            for option in option_args[0]:
                try:
                    section_dict[option]=eval(config.get(self.section, option)) #获取section中option的值，返回为string类型
                except Exception as e :
                    section_dict[option] = config.get(self.section, option)  # 获取section中option的值，返回为string类型
        except Exception as e :
            log.error("读取配置文件段section内容出现异常，异常原因：{}".format(e))
        return section_dict

    def get_section_option_list(self,filename=None,section=None):
        '''
        获取指定sections下所有options ，以列表形式返回['host', 'port', 'user', 'password']
        :param filename: 要读取的配置文件全路径名，如果为None自动获取初始化时的文件名
        :param section:  要读取的配置文件中的段名（section），如果为None自动获取初始化时的段名（section）
        :param option_kargs: 传入的选项名，因不同配置文件配置的选项不同，所以此参数为不固定参数
        :return:option_list
        '''
        section_list = []
        try:
            if filename:
                self.filename=filename
                config = self.read_cfg(self.filename)
            else:
                config = self.data
            if section:
                self.section=section
            section_list = config.options(self.section)
        except Exception as e :
            log.error("读取配置文件指定段section下所有option列表出现异常，异常原因：{}".format(e))
        return section_list

    def get_section_list(self,filename):
        '''
        获取配置文件所有的section
        :param filename:要读取的配置文件全路径名，如果为None自动获取初始化时的文件名
        :return:section_list
        '''
        sections =[]
        try:
            if filename:
                self.filename = filename
                config = self.read_cfg(self.filename)
            else:
                config = self.data
            sections = config.sections()
        except Exception as e :
            log.error("读取配置文件下所有section出现异常，异常原因：{}".format(e))
        return sections


    def get_opton_list_value(self,filename=None,section=None):
        '''
         获取指定section下所有的键值对，[(option, value), (option, value), ('option, value)]
        :param filename: 要读取的配置文件全路径名，如果为None自动获取初始化时的文件名
        :param section:  要读取的配置文件中的段名（section），如果为None自动获取初始化时的段名（section）
        :return: key_value_list
        '''
        option_key_value_list = []
        try:
            section_dict = {}
            if filename:
                self.filename=filename
                config = self.read_cfg(self.filename)
            else:
                config = self.data
            if section:
                self.section=section
            option_key_value_list = config.items(self.section)
        except Exception as e :
            log.error("读取配置文件指定段section下所有option列表出现异常，异常原因：{}".format(e))
        return option_key_value_list

    def deal_list_tuple_dict(self,list_tuple):
        '''
        将list_tuple键值对列表转为字典
        :param list_tuple: [(key, value), (key, value), ('key, value)]
        :return: {}
        '''
        z_dict = {}
        try:
            for tuple_s in list_tuple:
                z_dict[tuple_s[0]]=tuple_s[1]
        except Exception as e :
            log.error("将键值对列表转为字典出现异常，异常原因：{}".format(e))
        return z_dict

    def get_config_dict(self,filename=None,section=None):
        '''
        获取option字典值
        :param filename: 要读取的配置文件全路径名，如果为None自动获取初始化时的文件名
        :param section:  要读取的配置文件中的段名（section），如果为None自动获取初始化时的段名（section）
        :return: {}
        '''
        option_dict = {}
        try:
            if filename:
                self.filename=filename
                config = self.read_cfg(self.filename)
            else:
                config = self.data
            if section:
                self.section=section
            option_list = self.get_section_option_list()
            option_dict = self.get_section_key_value(option_list)
        except Exception as e :
            log.error("读取配置文件指定段section下所有option列表出现异常，异常原因：{}".format(e))
        return option_dict



if __name__ == "__main__":
    ope_cfg = OperationCFG("/home/ma/PycharmProjects/AutoTest_python/InterfaceTest/project_tree/TSA-IPPS/config/caseRun.cfg","my_case_file")
    option_list = ope_cfg.get_section_option_list()
    s = ope_cfg.get_section_key_value(option_list)
    print(s)