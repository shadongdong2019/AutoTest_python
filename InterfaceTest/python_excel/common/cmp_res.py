
class CmpRes:
    def __init__(self):
        pass

    def find_exist(self,str1,str2):
        if str(str1) in str(str2):
            flag = True
        else:
            flag = False
        return flag
