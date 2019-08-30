
class DealResData:
    def __init__(self):
        pass

    def deal_res_data(self,res_data,type=1):
        '''
        处理请求返回的数据
        :param res_data: 请求返回的数据
        :param type: 1表示获取返回的文本信息.text，2表示获取返回的图片、文件信息.content，3表示获取返回的的json信息.json()
        :return:
        '''
        if res_data:
            if type == 1:
                res = res_data.text
            elif type == 2:
                res = res_data.content
            else:
                try:
                    res =res_data.json()
                except Exception as e:
                    res = res_data.text
        else:
            res = res_data
        return res
