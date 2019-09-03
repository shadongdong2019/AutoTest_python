import pymysql

class MysqlObj:
    def __init__(self,**kwargs):
        # 打开数据库连接
        # 注意password的密码是你刚刚设置的，port=3306是MySql默认的端口号
        self.db = pymysql.connect(host=kwargs.get("host",None),user=kwargs.get("user",None), password=kwargs.get("password",None),port=kwargs.get("port",3306))

    def execute_sql(self,sql):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        rows = None
        try:
            # 执行sql语句
            cursor.execute(sql)
            #此时select得到的可能是多行记录,那么我们通过fetchall得到的就是多行记录,是一个二维元组((a,bc),(a,b,c))
            rows = cursor.fetchall()
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

        # 关闭数据库连接
        cursor.close()
        self.db.close()
        return rows
