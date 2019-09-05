from pymongo import MongoClient

class MongodbObj:
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        mongodb_url = self.kwargs.get("mongodb_url","")
        # 连接mongdb数据库
        client = MongoClient('mongodb://192.168.0.107:27017')
        db_obj = self.kwargs.get("db_obj","")
        # 获取数据库db对象 库的名称 py3
        db = db_obj #eg:db = client.py3

    def operation_table(self):
        # 获取集合对象 表的名称 collection ==> mdata
        collection = db.mdata


