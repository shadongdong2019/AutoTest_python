class MakeCases:
    '''
    自动编写测试用例类，主要编写非法数据测试用例,需要依据一个全参数测试用例
    包含：参数未传入，参数为空，参数为空格，参数值为null,参数值为true,参数值超长
    fail_param_value = ["N",""," ","null","true","long"]
    '''
    def __init__(self,**kwargs):
        self.kwargs = kwargs #获取配置文件参数
        pass


    def make_cases_fail(self):
        pass
