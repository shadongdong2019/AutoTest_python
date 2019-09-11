from python_excel.utils.operation_excel import OperationExcel
from python_excel.utils.operation_json import OperationJson
from python_excel.get_data.global_data import *
class GetData:
    def __init__(self,excel_filename=None,json_filanme=None,excel_sheetid=0):
        self.excel_filename =excel_filename
        self.excel_sheetid = excel_sheetid
        self.json_filename = json_filanme

        self.ope_excel = OperationExcel(self.excel_filename,self.excel_sheetid)
        self.ope_json = OperationJson(self.json_filename)

    #获取excel表格行数
    def excel_rows(self):
        return self.ope_excel.get_sheet_rows()

    #获取是否运行
    def is_run(self,row):
        col = get_is_run_col()
        is_run = self.ope_excel.get_cell_value(row,col)
        if str(is_run).strip().lower() == 'yes':
            run_flag = True
        else:
            run_flag = False
        return run_flag

    #获取headers
    def is_header(self,row):
        col = get_is_header_col()
        is_header = self.ope_excel.get_cell_value(row,col)
        if str(is_header).strip().lower() == 'yes':
            headers = get_header()
        else:
            headers = None
        return headers

    #获取请求路径
    def get_url(self,row):
        col = get_url_col()
        return self.ope_excel.get_cell_value(row,col)

    #获取请求方法
    def get_req_method(self,row):
        col = get_request_method_col()
        return self.ope_excel.get_cell_value(row,col)

    #获取请求数据
    def get_req_data(self,row):
        col = get_request_data_col()
        req_data_key = self.ope_excel.get_cell_value(row,col)
        res = self.ope_json.get_data_for_key(req_data_key)
        if res == '':#防止在excel用例里面直接写入的请求数据
            res = req_data_key
        return res

    # 获取case数据依赖
    def get_case_dep(self, row):
        col = get_case_dep_col()
        res = self.ope_excel.get_cell_value(row, col)
        return  res

    # 获取依赖的返回值规则
    def get_dep_ret_data_re(self, row):
        col = get_dep_ret_value_re_col()
        return self.ope_excel.get_cell_value(row, col)

    # 获取依赖的返回值
    def get_dep_ret_data(self, row):
        col = get_dep_ret_value_col()
        return self.ope_excel.get_cell_value(row, col)


    # 获取依赖字段
    def get_data_dep_key(self, row):
        col = get_data_dep_col()
        return self.ope_excel.get_cell_value(row, col)

    # 获取预期结果
    def get_expect_res(self, row):
        col = get_expect_col()
        return self.ope_excel.get_cell_value(row, col)

    # 往excel表中写入按规则获取的依赖返回数据
    def  writer_dep_res_data(self,row,data):
        col = get_dep_ret_value_col()
        return self.ope_excel.writer_data(row,col,data)

    # 往excel表中写入实际运行结果
    def  writer_real_data(self,row,data):
        col = get_real_result_col()
        return self.ope_excel.writer_data(row,col,data)

    # 往excel表中写入用例通过状态
    def  writer_status(self,row,data):
        col = get_status_col()
        return self.ope_excel.writer_data(row,col,data)
