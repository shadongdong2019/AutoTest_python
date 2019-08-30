import xlrd
from xlutils.copy import  copy
import logging
log = logging.getLogger("__file__")
class OperationExcel:
    def __init__(self,filename=None,sheetid=1):
        try:
            if filename:
                self.filename = filename
            else:
                self.filename = '../data_file/case_data_ysc.xlsx'
            self.sheetid = sheetid
            #print(self.filename,sheetid)
            self.sheet_obj = self.get_sheet(self.filename,self.sheetid)
        except Exception as e:
            log.error("操作EXCEL表类初始化异常，异常原因：{}".format(e))


    def get_sheet(self,filename=None,sheetid=0):
        try:
            if filename:
                self.filename = filename
            if sheetid:
                self.sheetid = sheetid
            self.sheet_obj = xlrd.open_workbook(self.filename).sheet_by_index(self.sheetid)
            return self.sheet_obj
        except Exception as e:
            log.error("操作EXCEL表类获取sheet页内容异常，异常原因：{}".format(e))
            return None

    def get_sheet_rows(self):
        try:
            return self.sheet_obj.nrows
        except Exception as e :
            log.error("操作EXCEL表类获取行数异常，异常原因：{}".format(e))
            return None

    def get_cell_value(self,row,col):
        try:
            return self.sheet_obj.cell_value(row,col)
        except Exception as e :
            log.error("操作EXCEL表类获取单元格内容异常，异常原因：{}".format(e))

    def writer_data(self,row,col,data):
        try:
            read_data = xlrd.open_workbook(self.filename)
            copy_data = copy(read_data)
            sheet_data = copy_data.get_sheet(self.sheetid)
            sheet_data.write(row,col,data)
            copy_data.save(self.filename)
        except Exception as e:
            log.error("操作EXCEL表类写入数据异常，异常原因：{}".format(e))

    def get_cols_data(self,col_num=0):
        try:
            return self.sheet_obj.col_values(col_num)
        except Exception as e:
            log.error("操作EXCEL表类获取列数据异常，异常原因：{}".format(e))
            return None

    def get_row_num_for_value(self,value):
        try:
            row_num = None
            for index,data in enumerate(self.get_cols_data(1)):
                if data == value:
                    row_num = index
            return row_num
        except Exception as e:
            log.error("操作EXCEL表类获取值对应的行号出现异常，异常原因：{}".format(e))
            return None

    def get_row_col_list(self,start=0,rows=None):
        try:
            if rows:
                self.rows=rows
            else:
                self.rows = self.get_sheet_rows()
            row_col_list = []
            for row in range(start,self.rows):
                col_list = self.get_sheet().row_values(row)
                row_col_list.append(col_list)
            return row_col_list
        except Exception as e :
            log.error("操作EXCEL表类获取值对应的行号出现异常，异常原因：{}".format(e))
            return None



if __name__ == '__main__':
    oe = OperationExcel()
    # print(oe.get_sheet_rows())
    # oe.writer_data(17,1,'sssss')
    # print(oe.get_cols_data(0))
    # print(oe.get_row_num_for_value('Imooc-11'))
    # print(oe.get_row_col_list())
    print(oe.get_cell_value(1,2))