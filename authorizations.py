import requests
from network_util import NetworkUtil

# 无效token示例
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9hcGkuYWxwaGEudGVzdFwvYXBpXC92MVwvdmVyaWZpY2F0aW9uQ29kZUF1dGhlbnRpY2F0aW9uIiwiaWF0IjoxNjQ3ODQyMTY1LCJleHAiOjE2NDc4NDU3NjUsIm5iZiI6MTY0Nzg0MjE2NSwianRpIjoiTXhrTlFyRXdUbWRnNzFEViIsInN1YiI6MSwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.y-77R5DUR9HfaeIzF3CndJmRvefPD6SUUr3q2A2_m5E

# 此类负责验证登陆状态, 登陆, 以及缓存登陆状态
class Authorizations:


  def __init__(self):
    # NetworkUtil 的作用, 点过去看一下就好了很简单
    self.networkUtil = NetworkUtil()

  # 此方法验证token,即 验证当前登陆状态的有效性
  # 如果验证通过会返回 True
  # 失败会返回 False 
  def checkTokenValid(self):

    # access_token 是本地的一个token缓存文件
    # token 是手机号验证通过的一个凭证, token 有效期为14天. 即验证通过后14天内免登录.
    try:
      file = open('.\\.access_token', 'r')
      token = file.read()
      file.close()
    except:
      return False

    # 下面的操作会校验当前缓存的token的有效性
    # 有效的话会返回一个新的token, 同时token有效期会刷新, 旧的token会失效
    headers = {'Authorization': 'Bearer ' + token}
    # 这里需要注意是 put 方法
    response = requests.put('https://api.alphavisual.cn/api/v1/authorizations/update', params = {}, headers = headers)
    json = self.networkUtil.checkResponse(response)
    if json == False:
      return False
    
    # 将新获得的token缓存下来, 成功返回 True, 失败返回 False
    return self.saveAccessToken(json)

  # 手机登陆操作
  # 手机登陆流程如下
  # 1. 客户端输入手机号码, 发送到服务端
  # 2. 服务端接收到正确的手机号码 ( 格式正确且此手机号码为已授权的用户手机号码 ) 后发送短信, 并返回 verification_key 和 verification_key 有效期.
  # 3. 用户收到手机验证码后, 将 verification_key 和 verification_code ( 验证码 ) 发送到服务器
  # 4. 服务端接收到 verification_key 和 verification_code 后进行校验 , 如果通过的话 会返回 token 及 当前用户信息的权限信息
  def login(self):
    # 这里重复创建 NetworkUtil 的实例没有特殊的意义, 只是简单的忘了Python怎么写了
    phone = input('请输入手机号码\n')
    # 这里需要注意是 post 方法
    response = requests.post('https://api.alphavisual.cn/api/v1/verificationCodes', {'phone': phone} )
    json = self.networkUtil.checkResponse(response)
    if json == False:
      return False
    try:
      verification_key = json['data']['verification_key']
    except:
      return False

    # 填写并发送验证码
    json = self.inputAndSendVerificationKey(verification_key)
    times = 0
    # 如果验证码错误的话, 可以重试. 
    while json == False:
    # 重试次数有限制, 限制为 2 次
      if times > 1:
        return False
      print ('验证码错误!\n')
      json = self.inputAndSendVerificationKey(verification_key)
      times = times + 1

    # 将新获得的token缓存下来, 成功返回 True, 失败返回 False
    return self.saveAccessToken(json)

  # 填写并发送验证码
  def inputAndSendVerificationKey(self, verification_key):
    verification_code = input('请输入验证码\n')
    response = requests.post('https://api.alphavisual.cn/api/v1/verificationCodeAuthentication', {'verification_key': verification_key, 'verification_code': verification_code} )
    return self.networkUtil.checkResponse(response)

  # 将新获得的token缓存下来, 成功返回 True, 失败返回 False
  def saveAccessToken(self, json):
    try:
      access_token = json['data']['access_token']
      file = open('.\\.access_token' , 'w')
      file.write(access_token)
      file.close()
    except:
      return False
    return True

