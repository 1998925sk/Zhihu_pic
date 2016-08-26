import requests
import re
import time
import os.path

try:
    from PIL import Image
except:
    print('')
    pass


class login():
    def __init__(self, accoount, password):
        # 构造 Request headers
        self.account = accoount
        self.password = password
        self.agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
        self.headers = {
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            'User-Agent': self.agent
        }
        self.session = requests.session()

    def get_xsrf(self):
        '''_xsrf 是一个动态变化的参数'''
        index_url = 'http://www.zhihu.com'
        # 获取登录时需要用到的_xsrf
        index_page = self.session.get(index_url, headers=self.headers)
        html = index_page.text
        pattern = r'name="_xsrf" value="(.*?)"'
        # 这里的_xsrf 返回的是一个list
        _xsrf = re.findall(pattern, html)
        return _xsrf[0]

    # 获取验证码
    def get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        r = self.session.get(captcha_url, headers=self.headers)
        with open('captcha.jpg', 'wb') as f:
            f.write(r.content)
            f.close()
            # 用pillow 的 Image 显示验证码
            # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
        return captcha

    def isLogin(self):
        # 通过查看用户个人信息来判断是否已经登录
        url = "https://www.zhihu.com/settings/profile"
        login_code = self.session.get(url, headers=self.headers, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def login(self, secret, account):
        # 通过输入的用户名判断是否是手机号
        if re.match(r"^1\d{10}$", account):
            print("手机号登录 \n")
            post_url = 'http://www.zhihu.com/login/phone_num'
            postdata = {
                '_xsrf': self.get_xsrf(),
                'password': secret,
                'remember_me': 'true',
                'phone_num': account,
            }

        else:
            if "@" in account:
                print("邮箱登录 \n")
            else:
                print("你的账号输入有问题，请重新登录")
                return 0
            post_url = 'http://www.zhihu.com/login/email'
            postdata = {
                '_xsrf': self.get_xsrf(),
                'password': secret,
                'remember_me': 'true',
                'email': account,
            }

        try:
            # 不需要验证码直接登录成功
            login_page = self.session.post(post_url, data=postdata, headers=self.headers)
            login_code = login_page.text
            login_code = eval(login_code)
            print(login_code['msg'])
        except:
            # 需要输入验证码后才能登录成功
            postdata["captcha"] = self.get_captcha()
            login_page = self.session.post(post_url, data=postdata, headers=self.headers)
            login_code = eval(login_page.text)
            print(login_code['msg'])

    def main(self):
        if self.isLogin():
            print('您已经登录')
        else:
            self.login(self.password, self.account)
            return self.session
