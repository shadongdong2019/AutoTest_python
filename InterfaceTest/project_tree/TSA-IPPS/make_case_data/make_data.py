import random
import string


class MakeData:
    def __init__(self):
        pass

    def random_en(self,min=0,max=1):
        '''
        随机英文数字，根据传入参数取位数
        :return:
        '''
        # 从a-zA-Z0-9生成指定数量的随机字符：
        ran_str_min = ''.join(random.sample(string.ascii_letters + string.digits, min))
        ran_str_max = ''.join(random.sample(string.ascii_letters + string.digits, max))
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(min+1,max-1)))
        ran_str_max_1 = ''.join(random.sample(string.ascii_letters + string.digits, max+1))
        ran_str_max_20 = ''.join(random.sample(string.ascii_letters + string.digits, max+20))
        return ran_str_min,ran_str_max,ran_str,ran_str_max_1,ran_str_max_20

    def random_zh(self,min=0,max=1):
        '''
        随机中文，根据传入参数取位数
        :return:
        '''
        ran_str_min = ''
        if min>0:
            for i in range(0,min):
                val = chr(random.randint(0x4e00, 0x9fbf))  # 生成随机中文
                ran_str_min+=val
        ran_str_max = ''
        if max>0:
            for i in range(0, max):
                val = chr(random.randint(0x4e00, 0x9fbf))  # 生成随机中文
                ran_str_max += val
        ran_str = ''
        for i in range(min+1,random.randint(min+2,max-1)):
            val = chr(random.randint(0x4e00, 0x9fbf))  # 生成随机中文
            ran_str += val

        ran_str_max_1 = ''
        for i in range(0, min+1):
            val = chr(random.randint(0x4e00, 0x9fbf))  # 生成随机中文
            ran_str_max_1 += val

        ran_str_max_1000 = ''
        for i in range(0, max+20):
            val = chr(random.randint(0x4e00, 0x9fbf))  # 生成随机中文
            ran_str_max_1000 += val

        return ran_str_min,ran_str_max,ran_str,ran_str_max_1,ran_str_max_1000

    def make_data(self):
        '''

        :return:
        '''


if __name__ == "__main__":
    m_data = MakeData()
    print(m_data.random_en(2,20))
    print(m_data.random_zh(2, 20))
    field= 'B-合作伙伴ID-partnerID-32,B-合作伙伴密钥-partnerKey-20,B-作品hash值-hash-64,B-作品文件-file-,B-作品名称-opusName-2:256,B-作品描述-opusDescribe-400,B-申请类型-applyType-3,B-申请人类型-applyUserType-3,B-申请人国籍-applyNationality-4,B-申请人-applyName-128,B-申请人证件类型-applyIDType-3,B-申请人证件号码-applyIDNumber-32,B-用户接口效验码-userInterfaceValidity-32,B-回调地址-callbackUrl-256,FB-作品hsah算法-hashAlgorithm-10	,FB-作品大小标识-fileSzieFlag-1,FB-作品文件类型-fileType-3,FB-作品状态-opusState-1,FB-作品编号-opusPartnerID-20	,FB-作品标签-opusLabel-500,FB-版权类型（对应版权库）-opusStore-3,FB-作品类型-opusType-3,FB-创作类型-opusCreativeType-3,FB-创作性质-opusCreativeNature-3,FB-申请人联系电话-applyPhone-14,FB-申请人邮箱-applyMail-64,FB-申请人联系地址-applyAddress-256,FB-申请人紧急联系人-applyEmergencyName-128,FB-申请人紧急联系电话-applyEmergencyPhone-14,FB-授权类型-authType-3,FB-授权有效期-authValidiy-5,FB-授权协议（电子件）-authProtocol-,FB-授权时间-authTime-20,FB-授权方式-authBusiness-1,FB-授权平台-authPlatform-50,FB-授权平台ID-authPlatformID-20,FB-协议价格-authPrice-10,FB-授权许可类型-authAllowType-1,FB-授权用途-authUse-200,FB-授权使用地域-authCountry-200,FB-可否转售-authSell-1,FB-授权限制-authLimit-500,FB-授权协议备注-authRemark-500,FB-被授权人类型-authUserType-3,FB-被授权人国籍-authUserNationality-4,FB-被授权人-authUserName-128	,FB-被授权人证件类型-authUserIDType-3,FB-被授权人证件号码-authUserIDNumber-32,FB-被授权人联系电话-authUserPhone-14,FB-被授权人联系邮箱-authUserMail-64,FB-被授权人联系电话-authUserAddress-256,FB-备注1-remark1-500,FB-备注2-remark2-500,FB-备注3-remark3-500,FB-通讯编码格式-encodeFmt-32'
    ss = field.split(",")
    print(ss)
    field_name_en = []
    field_name_zh = []
    all = []
    for s in ss:
        field_name_zh.append(s.split("-")[1])
        field_name_en.append(s.split("-")[2])
        all.append(s.split("-"))
    print(field_name_en)
    print(field_name_zh)
    print(all)

