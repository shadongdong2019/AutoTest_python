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
    # print(len("http://39.107.66.190:9999/v2/api/confirm/callback?id=12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf12345ascdf123"))
    # print("12345ascdf"*20)
    test_download()
    # hash_order =['partnerID', 'partnerKey', 'hash', 'file', 'hashAlgorithm', 'fileSzieFlag', 'fileType', 'opusName', 'opusState', 'opusPartnerID', 'opusLabel', 'opusStore', 'opusDescribe', 'opusType', 'opusCreativeType', 'opusCreativeNature', 'applyType', 'applyUserType', 'applyNationality', 'applyName', 'applyIDType', 'applyIDNumber', 'applyPhone', 'applyMail', 'applyAddress', 'applyEmergencyName', 'applyEmergencyPhone', 'authType', 'authValidiy', 'authProtocol', 'authTime', 'authBusiness', 'authPlatform', 'authPlatformID', 'authPrice', 'authAllowType', 'authUse', 'authCountry', 'authSell', 'authLimit', 'authRemark', 'authUserType', 'authUserNationality', 'authUserName', 'authUserIDType', 'authUserIDNumber', 'authUserPhone', 'authUserMail', 'authUserAddress', 'remark1', 'remark2', 'remark3', 'encodeFmt', 'salt', 'callbackUrl']
    # print(len(hash_order))
    # print(','.join(hash_order))
    #ss = "MIIVBQIBAzCCFL8GCSqGSIb3DQEHAaCCFLAEghSsMIIUqDCCBa0GCSqGSIb3DQEHAaCCBZ4EggWaMIIFljCCBZIGCyqGSIb3DQEMCgECoIIE+jCCBPYwKAYKKoZIhvcNAQwBAzAaBBQx9hGHrhQXujXaXEvJMH469hFnyAICBAAEggTIxEUxyRycgs1abbRnjkW4OXcTSxm5UEhEPCXYtQ6yWwCPTXEC/6Y4i04J2KTuh0xz/chNuIayd1Hi83kHj6ETHn3/pvMg2m3HmqNpJC6VJ8r/L67SmWiQtv9Vz3rsQhKotYIIdSvVDMkAhkftWmq51cXO8PZkgOnYRp8Bjg6sTxmmAlMzzSXUitEWko9dNC+U9R5qoamg4y6QCaR2x096Ashcm38rkZssajxIEIfAG3awv9CSe5j12sMp4GcG2MwiYdPAovV+XxPYw4r4PfjUBeglgQemwoFlcfGu0hxOXm5N3SdxKBlD9Qu06pRcI5+/QTomMqqv784wzI9dcelyhPW72W94B7mxXIs9dg724bjqgVa4rwrNY/qUkVFpOFba/IhOjAwiPhWbuURb2g2L/W4IeYp81rRDAT3vrcjhyJ3t9J6KOHLExsVp+HZtkTdG77AuaC2LAkFQpff6JIZK2VEwYUl+ID7is1GDQY7v/4tEZmFNmGGAy97sP7qsrP4akkTF4jwW04wHmHi0W+qfS4LbuERfA4Q9j4YCxfo/Sizq4FbNtJPBoY5Zjob5byBiFgiQNOQsBil0dhsyFJzFxrZHWnX9w0qGqbXi2wGG/AdEyvo2eoWZWt9U3yIgEBr5YBGml8TMHW9ILG0Ei5ZAmXQRqJ9Iw5Oeqq0m10GNj5FIsQfqImdx6l/pvdkpt6XWllTzvSroYXp0Z95iICyRebkMgm43vQLLsk6BY1EPeSiIJDRpeb2cCe6VPWXrJwaBz3bMfFH89i8LngmVODGY3sH03HheWReg+n6AealG2Vpm38KRlnPltj7S38aG9bK+B94K+a1Miqy4rWFp6WZuIvB9UaC6MEIjQCC301Y5U9haFz6+KbTqZGAbd8fFLvCiLnzxUIwRVOkmI40BKJAIbvFZ4naEn/5eiUEDs+kzk7dNppr97B+Yzj4H8P8EGTrSLuzCqX2h0J/wIETKHlHArU+VkpewIHMeNjSaZIqvbpyQU1eLKkUN5HtnNa3zt56Wg8674LRWJoLL0/F4GfQKzUCQ22Ws/MTBmIDBdDrsmV3mnv59JhHVvE1m0NMFS5jJNpLJ6UJo44QeXXVrhEdIe3b+aQlBpwjQKc89FmEytqMvDZtiSsz103dgAF1hevSvTkyNYYrVAybNoOpkXWkWr2pdgmjF5BvQHSJjPJTE31gWj17S4OsIUSiQUuv13kntwG2vF8D1jv/QSFJ3/WOCqe2MYJgK1vZyOLOo9BXYhOs/pf90xGSimu1HhSSgAMQ7hmQcHirrCRPhULp7oIkmx6WkZQrQoIbOU7Rg0AYsDPanOwU2r5wKYFq2lYgSNgh+12HjcAHNbEq1rz60y2HlomJXRVbeQvhTiII/7ewVuffN0I1h0Dr9DCDN8LhI200HoV01vZF9YvjMBPXi1sF6fHbCz1CocJ3mNXttR9vHeylwZ6y45eywvvL3FTVfMesyiB6ruGcnwh/6amTuBijIlBXUsspcp6zRHXHIZX3VTmQ/xtTpO12rEacaSmMwf08kHFl/FxRXrPYtirZShY8DyDWYQkkuAU3een3pPDhh87zxclr2GEZo+blvkHvGaWXjW+dYclRKdx/t8Vnvwuf2rY1LC3fClWkzMYGEMF8GCSqGSIb3DQEJFDFSHlAAMgBiAGUAOABiADQAYwA2AGQAMwBkADQAZQA1ADkAMQBlAGYAMwA5ADQANQAxADkANABiAGEANgAwADQANwA1ADgAMQA1ADUAMwA4ADkANTAhBgkqhkiG9w0BCRUxFAQSVGltZSAxNTY1Njc1NjgwNjU2MIIO8wYJKoZIhvcNAQcGoIIO5DCCDuACAQAwgg7ZBgkqhkiG9w0BBwEwKAYKKoZIhvcNAQwBBjAaBBSHT8eRWFsKP7ZjhNzUARF3G5xxLQICBACAgg6gsqb2DPAIBaDwG6vuSrMZe0XiPCiZVEGky6HnolDDG8vdHitNwJT70M2C0yav3bXuM91wAJllnwxVTlXPThYKY5oLFuWRjUnAGXKY8Yux5KQgaI+E4IqeH//H7sYiGHT89Y0jm+ZX7g+QfLlMhwnVbsUvMZZpGMlsv232XCNNoXVSWKO8Sj4AeoShqTaZXP8ARD66Zp+72EMSCcvfp9ZPc6Xm/exdbVP8XtirN9HPFBCEG8EN38lJZiW+/5/7Y5sxXoQy0ca54XohACQF8opvJCJ5MUlgu0zXuxtzVje6ngLccb86IBQr8QpdfD83JFNy9aatxIKTNQiA6+vwgW7f2G/QMZ797UUMDwx1a83YdECSAS0MIOQyYRIT4Pr6YHejmt9bJAlaU05cE0D2Hv0idmZeRc+fobR0+4elvP7vfXQTtsXlY0Av4rdzEM3l4hnsR/mUE0fRmdr6h0S/+sTDVR/wJmIfhbCZxib4MQqu1VKUpxWX8qwt/hwfULan+vKhIxw3lBnTZQO8UBiko68FvzqHvflYvWrXIAxONktgxy/fO6DLl9HHGuIe2sTdmG8zhFqctw1AX/kRaIkZUrPuvRwtrfvbHyQ+ev/k3Ex14v/bePsnCLc0kTiNF8ekN9/IDFtOX/o1ULF+qbGkUd4zklRyMy7OGEKZGVIB3r57dGo2w19blYZtG6A94+f7O+oePdQha4NZkX9KrV4tkuCh4Me7n4A5ag79Upr5fvBL8KpRXA8Mrs9OfZ0uB8sM8V6gtc8oaQ13txOOkBxY+B0zsaiAsLJYggfTAa6tS8lX3dt3yOx2udKlqNGjhf2goeS/MWHUwwrv2ZCrFEVlBIlSrRaL37llyfKdnYNFKE8hLp+A6mqfI4b9qlgZajsBRQVRV6Mi+mQLDlXarWydDlnf2BZoGCR/lMBq9A6YS/Bst6ldHvxqtfLxFT9/kQebds0tue7vqP5JAaLowBa8TI1Al+MjMZ4Szwt1prTtqGM8JLOCdWET9pfQdJjKP/u98qTNJMc9bvexmSopxWBIjS7aGRiKZgY/TY2vmAxwQzgIUvb7Yw5ar9mmY5ndyAWJxkxF/w0AtwLCd2hbAE7DIHnKQT1j8r0CgXjMvzCXdYUwRovmv+ViQu/vzhXBtEyDt/6bsAkaXgR7vtjK0Rl6PL7ylaviUEaP4R3kgk92KxeaEuVzgQTSaZbOBrJ3zH2YLO9eU9GLKNmrPXE5V+y38y5SiOpI8QZXDJvF1XVhPqiEmis4WQzEXrttROePB69Y5jtDBg1CyKpOBBaGUjFtsh2WvpN9PKjkh3pbkeANVfQyytCYxDH1E8YK4UTqY4vnLymZCdB0MR/EHe75IuYIBLi3RioL1kYn+0LqL70LWtUx4qu/IxXu9mV/kWf/aMlJycF76Tv4O3l+aMe5eXJC6fSpnrDf3PLwXx5WlNycoMutKoKMfPC9W72WXmk+QM+Al6p6iOlM9fFUPkDxwr728P1jQqaEwYavamSv7gWPkYbhjiGImHVNYmnKAO8C+SLJKM6sNWVtcAu/yXQlaikbo5aUuyLPaMxKVP/sDASRzjIaEiXngdPZ08oq0hubE3YKMpzmkW5lsozEFLhXRsaY9X5UK5KOloPnSi/FtIxtB8z21sNIV6jYyNgnHPAknTWzo/aRMCAWmBNk99MnHVS9OwsKvZJMvWaAk6JEp8k87TFQYuO/VaOpZQoRSo00D2xzEunPCQvk75h495yArK8Y+s/tE8HGfsX8Qo70C2CIZGy9jlkYgOC5NL96M8KP7PiU4NPh1+HXjdNDvgqx1XSlTu83ZpVWJ5K2Kn9brnbyToyN9n3d3zWC43OgR0kpary81+0MUfbFb6i8wM1ygHmqsIr/TGX0BU9XzUtdbZkRiYCJy7qeRQ0251Ld0zCBE/c889f/noneAxN2nsZXsUziaq6INdxAS3zAMP0SPzFmjIYxICMNpOy0a8DrOpbhrZzWzFZhhQ2TBV8z58VThHjR/iSWTaulL9q8y/4OuOa9sh2vo0VJC86/T442Vt4OoYkMfA9zlXG6aZiRgCpP0dJND5rqjwWt9lRuLiMkONR/amIIWUa4ceKCzBh3idvBPfvYSUfQ0IolxgYiLvCmyv9AlrsF8wJX6HY98MolQwGYIDqXe0FAcnDwPumnS1xuUZVY1J8+C5ss0SAXK5kjjLuTL7AH2dgIzl7/kfp9635aQi4pjQlCqF5h2/R2wbZy3AZ2JKU8dIwqmKVNz7fOvHSJZKPkLlahhG1l8xp30/jiMuzUFBgSWO8tqv04yIQuCLpO6XozBUdda3P5PslLrP5wm+OIeJFdP/0cc6D/OxovsfToULEMaC4WLTGDZeyZWvhbwz3EM/34HHdBm7WgjXxMOsGf7sNHykB3RVW+9b3gtIoTe48S1EzQFM4OVGPr0L7gEh64z9kWpVEiL483Ur8aNPxnxM0/pM9zWJTGB+hjHgGQVKNSdfOQPK/4NIAfeG9uR8Q29yYeqcw5xyCiyOT91fBefLjMrdRN6xEiechRcWoKzndMoUv1Xk2nmnWgx1nsMucjmRcVuXvyAqzelmKFuA6fDAGGOkGJ2MkfRgEzUsYQathhQYHTCOXSAclsNI9kjqqI7ZK+appyP9z/H29IqdQMPeUrS7qg2WpOAhD8pI0jpP8/1fx13Q2gT1t9IsW6ZLO1WLPkY4v57F/EmcSl0xINP0EmlFiJcE6GVYrMsXHfcpirf7KCBQ8Cos4Cm8Xo3seqNaU0k4pMfDsvbK0Ry+mHZYVPn3Zg4r9as7qxgOgA6c/Z5N2QKfkdq8p82Y/iio440anE6usqjk7cGGqk02Ynwrb2Va5prLI9WW9Y2xo2zGd7KcPIXbHsuxgc/dAcKClA9bcJNX69QxuPt8Ih7xB4puNNoROQP2surUIdB437AJr8Y6Vi2Gzgca9axrq+Ys4wiDYTECkomtzlOctFt9FCPHNTZBmIBeKEKa1YDsXfkbLxO1/IGG1xVd/OCY6tFFnmdlwAFay5pm8EFa6TyuaGwEqOMwO5XMjvx7SO0kxoV0NEqMQKVMqIDNh96d2jv9DwDKiBsLmNI7YkK3IVr4k7tSqA8CYolWQShwpr99nIFcw4HbfS1Kq7tQF9dOWYZX0Uy4M4eBY+w4A/AMoBbMqDsmyvF4iZhzKQGrxZSDbDTmruMvlRRn2/CqVa5Nwm5PNzSRxainmelIcvRyxnL1T1SAikNIXHEVcUnq/s/cYG90u7f/almH2LVE+dgVdeJ4r8uubELXkDnlzeBHEuELDmoSu1BewMVfdXJ/kAWJl7xSv3w7uawjo/mu/J/gINjc5x5rUq4xTumca0i/hU13ZRIlN7yXzB97zDmxEXCptJ4mEvegUrlbU0Y9eMOfCTMI/P96xR2SF4th0wLOkyo5rvddQRhQj1nMA82xswPidALybJv/xQQicFagSyB5tBv67Uh5deSIY8IU03Bdy7Rv9Rg2YoVckCh8zc1uEEPJWCNBi2DFCNoRaxgNlM/+kUJSJyN6oZIa/ibmqPWZC2Rc3/ZZCITEbCDM7EnCnGBAhRYZ2L/c7hs7AJDFNS1nRf85xud3RYKMqPJFZePZpWyGXmRyCGn4RdjGo23XpRZ5yQdn/GmW07uJVHJ9Ybl1PfZ9r2sPI38PWD9HFVOFiBOXjDgPiIsFFLQGenQHuz/nizZSYua/l4wbYdsrdTTWihQOo2PWXru6lj5HeCWJr3ofIAs+z9wfO0mvQgaKVz74lKj4cJ4cwk4Ii02IIo7zcWs/rEFrUUn6yBnUPxZ5JL2H28ZdOeKRhYTADtnhNsT/xTV/GPrvZr7g9ecC2bo2+mj1PEehHdPnkr+c8sgrjjhRudHYvHJOusF12QYw7/ZvKVw/8ozEJxGpa24sehwvlXr5txZWH4Hnpw2/8H3PUE4CgR4hLs5qHNvAIFNH3IiEcEJpGGLgMfBnCbLJYCAo8A+BM3cmvUyPdbxAbfL4U7bj/XDnAPkfpj5XDkofiRq6qnsW4S4JuWDxGwlgyWLMjw1r9L8AFDMeXncm0QCWZhg8n6LG+R+5zFRpcPiHeU1kz+4ZhTWWxO/6/vWfK8Sg51my9FhEhDzZebRdixmznT1t6MsLmKxUhHtzklD1sZ0nWv0wtIiyvBX07MsY0SDlWmzabI4KsqHuw5AYaK+l7DbnWctFtGvCFFSSp76HpgLy1SKR/Emzwz7rz/LdPF+XcTpGa4TVakCTiAoNvpuSRH+ctj75okGcsdckTaGvDLVlNYK8gAspUktceSogRqnrmoedCf/N/AKVrBlrXSK84UynQMPbXCYXLute+qvvGmDduzEj8Ds20/r9DiTnuhFpEeJl9KdhTVszD0f1McXC/JVORRc0fuxAQYE5iq9vvrMiNjG/E2B68/oYkW4JcXPiTjywUa0Ai0DfNpw9DhV5sdlrefY/Ota4suczbq/SViMSmePhePUy7Cnq/opEhLTAUSfLoHL/O4V9y4vZfZ4wWvJUstMuhnAHPmSzswH7ofhYGF5zZ+JSn28lf2DtzYy84p+kZcx3jpGFZvfuf7husPqeU7HbDLd4mQKHGDp+rQiYspiBkruit2DN0JSjiP102B0hmEoQxnxQRSiexRklgnpwXJmraraA2c68KQw3RUGw+fp6NtWaUQkK4DnTQoKg+1j5ExFYsgPAhrjXBJ5KLhi7aPXOCW8Je9XtTvWjH57LNTj4/6D6ng0dpPUVUa02Ep+nM8ETs3HSkJ0mx9h5CFVdR8lYIrmsO/SwU9/EvwAejiC9yIc5NLCzkWi9QTirivEQwrB7hk/rqaj9FDrcUtkIWlQmDobj63tt28E2Fibo7YkLDK+LhLZZrBF+XxZstBf3lpMDA3WARyRkXw+tfEPd8B0IuWdQn/116zH7YdBrr0Eo20UW66LVO3MEO/bYeh0gof0Gj8fQCR9r7759FBmH5TJGcs84TT0H3698euSW2IUWaEh/PSx6fTCfG0phq9s5xfMD0wITAJBgUrDgMCGgUABBS1j/tD34nGlDCnEqatXiO6reYwlAQUrESmV9vYDAGCsRUQJjNqzXnE9ZoCAgQA";
    # print(len(ss))
