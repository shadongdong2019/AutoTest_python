from python_excel.common.interface_run import InterfaceRun
import hashlib
interf = InterfaceRun()
url = "http://47.93.11.109:8088/service/CfcaCertAPI"
data={
"password":"111222",
"username":"北京技术服务有限公司",
"period":"1",
"periodType":"day",
"cardType":"0",
"cardNumber":"110111198801251234",
"email":"tsa@tsa.cn",
}
pin = "0096d530b10a8b3dcf2ab1b6fd2e9c2b"
value_list = list(data.values())
value_str = ''.join(value_list)
str = ''
["cardNumber","cardType","email","password","period","periodType","username"]
for d in data:
    str=str+d+"="+data[d]+"&"
str=str[:-1]
print(str)


str="cardNumber=110111198801251234&cardType=0&email=tsa@tsa.cn&password=111222&period=1&periodType=day&username=北京技术服务有限公司"
m = hashlib.md5()
b = str.encode(encoding='utf-8')
m.update(b)
value_str_md5 = m.hexdigest()
print(value_str_md5)
data_z={
    "arg0":pin,
    "arg1":data,
    "arg2":value_str_md5
}
res = interf.main_request("post",url,data_z)
print(res.json())