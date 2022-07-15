from system_util import SystemUtil
from network_util import NetworkUtil
import requests

# 此类负责验证设备, 注册设备


class Hardware:

    def __init__(self):
        self.sysUtil = SystemUtil()
        self.networkUtil = NetworkUtil()

    # 此方法验证设备, 成功返回 True 失败返回 False
    # 验证流程如下
    # 1. 客户端将证书(公钥)和cpuid发送给服务端.
    # 2. 服务端会尝试用证书(公钥)对cpuid加密,然后用服务器保存的该cpuid私钥进行解密. 如果 cpuid 无对应私钥或者证书错误导致无法解密, 则验证失败
    def checkHardwareValid(self):
        # 这里重复实例 Util 类只是忘了 Python 的类属性和访问控制的用法了.
        uuid = self.sysUtil.uuid()
        try:
            public_key = open(".\\public.pem").read()
            kw = {'cpuid': uuid, 'public_key': public_key}
            response = requests.post(
                "https://api.alphavisual.cn/api/v1/verificationHardware", params=kw)
            json = self.networkUtil.checkResponse(response)
            if json == False:
                return False
            return True
        except:
            return False

    # 此方法注册新设备
    # 注册流程如下
    # 1. 客户端输入邀请码, 然后将邀请码和 cpuid 发送到服务端
    # 2. 服务端验证邀请码, 如果邀请码可用, 则创建一个 Rsa 密钥对, 并保存 cpuid.
    # 3. 服务端返回证书, 客户端保存
    def register(self):
        uuid = self.sysUtil.uuid()
        code = input("请输入邀请码!\n")
        kw = {'cpuid': uuid, 'code': code}
        try:
            response = requests.post(
                "https://api.alphavisual.cn/api/v1/hardware", params=kw)
            json = self.networkUtil.checkResponse(response)
            if json == False:
                return False
            public_key = json['data']['public_key']
            pem = open(".\\public.pem", 'w')
            pem.write(public_key)
            pem.close()
            return True
        except:
            return False
