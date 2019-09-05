from jsonpath import jsonpath

from InterfaceTest.python_excel.common.interface_run import InterfaceRun
from InterfaceTest.python_excel.get_data.tsa_param_dic import TsaParamDict
from InterfaceTest.python_excel.utils.operation_json import OperationJson
op = OperationJson("../data_file/100_2.json")
def test_download():
    print(op.read_data())
    json_obj = op.read_data()
    res = jsonpath(json_obj, "$.._id")
    print(len(res))
    serialNo_list =res
    tsa_param = TsaParamDict()
    count_s = 0
    count_f = 0
    serialNo_list = ["359840459381813248"]
    for serialNo in serialNo_list:
        salt = tsa_param.make_salt(["201907200200058182","SJ2P5TW43R0ZLCR6V556",serialNo],"SJ2P5TW43R0ZLCR6V556")

        data = {
            "partnerID": "201907200200058182",#12345678123456781234567812345678
            "partnerKey": "SJ2P5TW43R0ZLCR6V556",#12345678901234567890
            "serialNo": serialNo,
            "salt":salt
        }
        print(salt)

        # data =  {
        #     'partnerID': '201907200200055052',
        #     'partnerKey': 'YLZ3XCEE4J21N0YHQNEW',
        #     'serialNo': '340042551278964736',
        #     'salt': 'f67bc9be1564245bf8af494a2d253cf5YLZ3XCEE4J21N0YHQNEW'
        # }
        #
        # data = {'partnerID': '201907200200055052', 'partnerKey': 'YLZ3XCEE4J21N0YHQNEW',
        #                 'serialNo': '340042551278964736', 'salt': 'f67bc9be1564245bf8af494a2d253cf5YLZ3XCEE4J21N0YHQNEW'}

        url = "http://ipp.tsa.cn/v2/api/confirm/downloadOpusCertificate"  # 下载接口
        #url = "http://39.107.66.190:9999/v2/api/confirm/downloadOpusCertificate"
        interface_run = InterfaceRun()
        print(data)
        res = interface_run.main_request("post", url, data).json()
        # print(str(salt).upper())
        # print("用例执行通过，返回结果={}".format(res))
        file_data = res.get("data",None)

        if file_data:
            tsa_param.decry(file_data, data["serialNo"],download_file=True)
            res.pop("data")
            print("返回成功结果："+str(res))
            count_s=count_s+1
        else:
            print("返回失败结果：" + str(res))
            count_f = count_f + 1
    print("共下载成功：{}".format(count_s))
    print("共下载失败：{}".format(count_f))


if __name__ == "__main__":
    print("0"*52)