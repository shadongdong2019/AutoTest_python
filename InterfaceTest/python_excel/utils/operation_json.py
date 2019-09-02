import json
import logging
log = logging.getLogger(__file__)

class OperationJson:
    def __init__(self,filename=None):
        try:
            if filename:
                self.filename = filename
            else:
                self.filename = ''
            self.json_data = self.read_data()
        except Exception as e:
            log.error("操作JSON类初始化异常，异常原因：{}".format(e))


    def read_data(self,filename=None):
        try:
            if filename:
                self.filename = filename
            with open(self.filename) as fp:
                data = json.load(fp)
            return data
        except Exception as e:
            log.error("操作JSON类读取数据异常，异常原因：{}".format(e))
            return None

    def get_keys_list(self):
        try:
            return list(self.read_data().keys())
        except Exception as e:
            log.error("操作JSON类获取所有key数据异常，异常原因：{}".format(e))
            return None
    
    def get_data_for_key(self,key):
        try:
            return self.read_data()[key]
        except Exception as e :
            log.error("操作JSON类根据key获取value异常，异常原因：{}".format(e))

if __name__ == '__main__':
    oj = OperationJson()
    print(oj.read_data())
    print(oj.get_data_for_key('user1'))
    print(oj.get_keys_list())