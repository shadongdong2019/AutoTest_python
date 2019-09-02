from InterfaceTest.python_excel.utils.operation_excel import OperationExcel
import logging
from jsonpath_rw import parse

log = logging.getLogger(__file__)

class CaseDetail:
    def __init__(self,filename=None,sheetid=0):
        try:
            if filename:
                self.filename = filename
            else:
                self.filename = "../data_file/TestCase_zh.xlsx"
            self.op_excel = OperationExcel(self.filename,0)
        except Exception as e:
            log.error("获取中文用例表类初始化信息出现异常，异常原因：{}".format(e))

    def get_case_detail(self,caseid,col):
        '''
        获取用例描述信息
        :return:
        '''
        try:
            row_num = self.op_excel.get_row_num_for_value(caseid)
            case_detail = self.op_excel.get_cell_value(row_num,col)
            return case_detail
        except Exception as e:
            log.error("获取中文用例表信息方法出现异常，异常原因：{}".format(e))

    def is_pass(self,exp,res,re):
        pass

