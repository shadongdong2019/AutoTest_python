import base64
import os
import datetime

def decry( **kwargs):
    '''
    将文件流转为指定格式的文件
    :return:True or False ,True表示存储成功，False表示失败
    '''
    is_download = False
    try:
        file_stream = kwargs.get("file_stream", "nKgNmEvPNHJEK0EylDaguG9v5L79a/XOeOCFQpsftCYZPJIHihTpJi/FJRw7XQ1TUSHMXG6l9Imhg3fq9Y1nhoL11GB7h3HnUOYpLPmhnspPe8iq8WFarxieZnijR0dX2TjUNigWbREj9KxK1TjPUCFRsGejdJ4X3SmSxx2L3Pw=")  # 获取文件流
        file_flag = kwargs.get("file_stream", "serialNo")  # 获取文件标识，用于显示在文件名最前面，如serialNo码
        file_type = kwargs.get("file_type", "pdf")  # 获取文件后缀类型 如：jpg/pdf
        download_path = kwargs.get("download_path", "../download/")  # 获取下载文件存入路径
        file_str = base64.b64decode(file_stream)  # 把文件流进行base64解码
        data_str = datetime.datetime.now().strftime('%Y%m%d')  # 将当前时间转为字符串
        # rand_str = ''.join(random.sample((string.ascii_letters + string.digits),5)) #5位随机数（数字+字母）
        file_name = "{}_{}.{}".format(file_flag, data_str, file_type)  # 生成文件名：文件标识+当前时间字符串+文件后缀
        if not os.path.exists(download_path):  # 判断文件存储路径是否存在
            os.makedirs(download_path)  # 如果不存在就在创建对应路径
        file_name = download_path + "{}".format(file_name)  # 存储路径+文件全称
        file = open(file_name, "wb")  # 以二进制读的方式打开文件
        file.write(file_str)  # 写入文件流解码后的内容
        file.close()  # 关闭文件
        is_download = True
    except Exception as e:
        pass
    return is_download

decry()

print("留"*500)
print(len("留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留留"))