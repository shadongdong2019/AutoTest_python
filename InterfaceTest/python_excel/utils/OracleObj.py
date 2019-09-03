import cx_Oracle
import os

class OracleObj:
    def __init__(self,**kwargs):

        # 设置环境编码方式，可解决读取数据库乱码问题
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
        user = kwargs.get("user", None)
        password = kwargs.get("password", None)
        host = kwargs.get("host", None)
        port = kwargs.get("port", "orcl")
        # Oracle连接信息
        # 用户/密码@数据库地址/库名
        oracle_tns = '{}/{}@{}/orcl'.format(user,password,host)
        self.db = cx_Oracle.connect()
    def execute_sql(self,sql):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        rows = None
        try:
            # 执行sql语句
            cursor.execute(sql)
            #此时select得到的可能是多行记录,那么我们通过fetchall得到的就是多行记录,是一个二维元组((a,bc),(a,b,c))
            rows = cursor.fetchall()
           # print(row[0])
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        # 关闭数据库连接
        cursor.close()
        self.db.close()
        return rows