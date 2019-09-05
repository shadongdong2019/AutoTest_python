class CaseIsPass:
    def __init__(self,**kwargs):
        self.kwargs = kwargs

    def case_is_pass(self,**kwargs):
        expect_res_verify = kwargs.get("expect_res_verify")  # 验证测试用例中预期结果与实际结果是否一致
        database_flag = kwargs.get("database_flag")  # 验证请求数据与数据库中数据是否一致
        callbackurl_flag = kwargs.get("database_flag")  # 验证数据库中回调状态与测试用例中预期结果是否一致
        # 是否需要验证数据库存入的数据
        is_verify_database = self.kwargs.get("is_verify_database")
        # 是否需要验证回调状态数据
        is_verify_callbackurl = self.kwargs.get("is_verify_callbackurl")
        #测试用例是否通过
        is_pass = False

        if expect_res_verify and (is_verify_database == database_flag) and (callbackurl_flag == is_verify_callbackurl):
            is_pass = True
        if is_verify_database:
            print("数据库数据验证结果：{}".format(kwargs.get("database_str")))
        if is_verify_callbackurl:
            print("数据库回调结果标识验证结果：{}".format(kwargs.get("database_str")))
        return is_pass

