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
}


def login():
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
    print(resp)
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
