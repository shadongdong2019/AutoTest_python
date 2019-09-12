#coding:utf8
import csv
import json
import time
from os import walk

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Search

from python_excel.utils.operation_cfg import OperationCFG


class ElasticObj:
    def __init__(self, **kwargs):
        '''

        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.kwargs = kwargs
        self.index_name =self.kwargs.get("index_name","")
        self.ip = self.kwargs.get("ip","")
        # 无用户名密码状态
        self.es = Elasticsearch([self.ip])


    def sigle_filed_query(self):
        '''
        打印库里所有的索引
        :return:
        '''
        print(self.es.cat.indices())

    def deal_config_query(self,res=None):
        '''
        处理配置名件中的查询条件
        键值对，值为“”表示需获取响应结果中的数据
        键值铎，有值表示使用默认值
        :res:请求响应结果
        :return: 处理后的qeury查询条件
        '''

        query_res = []
        query_filed = self.kwargs.get("query_filed","")
        for key in query_filed.keys():
            bool = {}
            must = {}
            list_z = []
            match_phrase = {}
            condition = {}
            query = {}
            if query_filed[key] == "" and res:
                query["query"] = res[key]
                condition[key] = query
            else:
                query["query"] = query_filed[key]
                condition[key] = query
            match_phrase["match_phrase"] = condition
            list_z.append(match_phrase)
            must["must"] = list_z
            bool["bool"]=must
            query_res.append(bool)
        return query_res


    def get_data(self,query=None,index=None):
        '''
        根据查询条件获取返回结果
        :param query: 查询条件
        :param index: 索引名称
        :return: 返回查询结果及查询条数
        '''
        # query = [
        #                 {"match": {"serialNo": 368400630043389952}},
        #                 {"match": {"is_result": 1}}
        #             ]
        if not query:
            query = self.deal_config_query()
        if index:
            self.index_name = index
        # 查找具体数据
        query = {
            "query": {
                "bool": {
                    "filter": query
                }
            },
            "size": 100
        }
        res = self.es.search(
            index=self.index_name,
            body=query)
        res_json =json.dumps(res,sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False) #返回json格式的查询结果
        print(json.dumps(res,sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))  # 请求总结果
        total = res['hits']['total'] #查询总条数
        print(total)
        return res_json,total


    def get_data_dsl(self):
        # using参数是指定Elasticsearch实例对象，index指定索引，可以缩小范围，index接受一个列表作为多个索引，且也可以用正则表示符合某种规则的索引都可以被索引，如index=["bank", "banner", "country"]又如index=["b*"]后者可以同时索引所有以b开头的索引，search中同样可以指定具体doc-type
        s = Search(using=self.es, index=self.index_name)
        res = s.query("match", serialNo="368400630043389952").query("match", is_result="1").highlight("is_result").execute()
        print(type(res))
        #print(json.dumps(res,sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))

    def delete_data(self):
        query = {'query': {'match': {"serialNo": 368389656708132864,"is_result":1}}}  # 删除性别为女性的所有文档
        # 删除所有文档
        self.es.delete_by_query(index="monitor", body=query)




if __name__ == "__main__":
    ope_cfg = OperationCFG(
        "/home/ma/PycharmProjects/AutoTest_python/InterfaceTest/project_tree/TSA-IPPS-JC/config/caseRun.cfg",
        "my_case_file")
    option_dict = ope_cfg.get_config_dict()
    obj =ElasticObj(**option_dict)
    obj.get_data()
    #obj.get_data_dsl()
