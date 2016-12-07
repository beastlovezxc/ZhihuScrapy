import requests
from bs4 import BeautifulSoup
import http.cookiejar as cookielib
import time
import random
from PIL import Image

INDEX_URL = 'http://www.zhihu.com'
LOGIN_URL = 'http://www.zhihu.com/login/email'
CAPTCAH_URL = 'http://www.zhihu.com/captcha.gif?r='

headers = {
    'Host': 'www.zhihu.com',
    'Referer': 'http://www.zhihu.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'authorization': 'Bearer Mi4wQUFEQWVKOGxBQUFBY0lBaXptMkNDaGNBQUFCaEFsVk5VelJ0V0FBU25JS24weHBCY2Y4bUFKSFA4TjczY1lvMG1B|1480960983|2705bef84689512488916df83ade3dc6ddf1f1af'
}


def login():
    # email = input('请输入登录邮箱->')
    # password = input('请输入登录密码->')

    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cookies')
    _xsrf = BeautifulSoup(session.get(INDEX_URL, headers=headers).content).find(
        'input', attrs={'name': '_xsrf'})['value']
    data = {
        '_xsrf': _xsrf,
        'email': 'beastkillerbin@gmail.com',
        'password': 'chenbin_45808',
        'remember_me': 'true',
        # 'captcha': captcha,
    }
    resp = session.post(LOGIN_URL, data, headers=headers)
    if str(resp) == '<Response [200]>':
        print('登录成功！！！')
    session.cookies.save()
    return session


def get_captcha():
    t = str(int(time.time() * 1000))
    r = session.get(CAPTCAH_URL + t + '&type=login', headers=headers)
    with open('/Captcha/captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    try:
        im = Image.open('/Captcha/captcha.jpg')
        im.show()
        im.close()
    except:
        print(os.path.abspath('/Captcha/captcha.jpg'))
    captcha = input('input captcha: ')
    return captcha

login()
