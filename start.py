from hardware import Hardware
from authorizations import Authorizations
import os
import time


def main():
    hardware = Hardware()
    auth = Authorizations()
    show()
    print('正在验证设备是否已授权:\t')
    if hardware.checkHardwareValid():
        print('验证通过!\t')
        print('正在验证设备用户登陆状态:\t')
        if auth.checkTokenValid():
            print('验证通过!\t')
            success()
        else:
            print('登陆失效,请重新登陆\t')
            if auth.login():
                print('登陆成功!\t')
        close()
    else:
        print('设备未授权, 启动授权模块.')
        if hardware.register():
            if auth.login():
                print('登陆成功!\t')
                success()
                close()
        else:
            print('验证失败!\t')
            close()


def success():
    # 这里验证通过会缓存一个认证通过状态. 如果是在 ue4 产品里边实现的话就不需要了, 可以每次打开的时候就验证. 因为缓存了证书和token所以正常也不需要不停的登陆.
    home = open(os.path.expanduser('~') + '\\' + '.valid', 'w')
    # now = time.localtime()
    home.write(str(int(time.time())))
    # home.write(str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday))
    home.close()


def show():
    print(
        '''
    / \ \    | |     | |   | || |    | |    / \ \  
   / /_\ \   | |     | |___| || |____| |   / /_\ \ 
  / /___\ \  | |     | |_____|| |____| |  / /___\ \ 
 / /     \ \ | |____ | |      | |    | | / /     \ \ 
/ /       \ \|______|| |      | |    | |/ /       \ \ 
    '''
    )


def close():
    sleep_time = 4
    while(sleep_time > 0):
        time.sleep(1)
        sleep_time = sleep_time - 1
        print('本窗口将在' + str(sleep_time) + '秒后关闭! \r')
# main()


if __name__ == '__main__':
    main()
