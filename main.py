# -*- coding: utf-8 -*-
import requests
import json
import random
import time
import rsa
import base64
import re
import hashlib
import urllib.request
import urllib

def md5str(str):
    m = hashlib.md5(str.encode(encoding="utf-8"))
    return m.hexdigest()


def md5(byte):
    return hashlib.md5(byte).hexdigest()


class DamatuApi():
    ID = '44439'
    KEY = '4b49234f019b75f5508421d1b18e05df'
    HOST = 'http://api.dama2.com:7766/app/'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getSign(self, param=b''):
        return (md5(bytes(self.KEY, encoding="utf8") + bytes(self.username, encoding="utf8") + param))[:8]

    def getPwd(self):
        return md5str(self.KEY + md5str(md5str(self.username) + md5str(self.password)))

    def post(self, path, params={}):
        data = urllib.parse.urlencode(params).encode('utf-8')
        url = self.HOST + path
        response = urllib.request.Request(url, data)
        return urllib.request.urlopen(response).read()

    def getBalance(self):
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.getPwd(),
                'sign': dmt.getSign()
                }
        res = self.post('d2Balance', data)
        res = str(res, encoding="utf-8")
        jres = json.loads(res)
        if jres['ret'] == 0:
            return jres['balance']
        else:
            return jres['ret']

    def decode(self, fdata, type):
        filedata = base64.b64encode(fdata)
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.getPwd(),
                'type': type,
                'fileDataBase64': filedata,
                'sign': dmt.getSign(fdata)
                }
        res = self.post('d2File', data)
        res = str(res, encoding="utf-8")
        jres = json.loads(res)
        if jres['ret'] == 0:
            # {ret，id，result，cookie}
            return (jres['result'])
        else:
            return jres['ret']

    def reportError(self, id):
        data = {'appID': self.ID,
                'user': self.username,
                'pwd': dmt.getPwd(),
                'id': id,
                'sign': dmt.getSign(id.encode(encoding="utf-8"))
                }
        res = self.post('d2ReportError', data)
        res = str(res, encoding="utf-8")
        jres = json.loads(res)
        return jres['ret']


def _get_hex(i):
    if i <= 9:
        return chr(ord('0') + i)
    else:
        return chr(ord('A') + i - 10)


def _rsa_encrypt(pubkey, password):
    key = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
    return base64.b64encode(rsa.encrypt(password.encode('utf-8'), key))


class Tieba(object):
    def __init__(self, username, password):
        self.base_url = 'https://www.baidu.com'
        self.username = username
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"

        try:
            self._get_cookies()
        except IOError as e:
            print(e)

        if self._check_login():
            print('Read Cookies for cache...')
        else:
            self.session.cookies.clear()
            self.session.get(self.base_url)
            self._login(username, password)

    def _get_cookies(self):
        with open('cookie.json') as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)

    def _check_login(self):
        res = self.session.get(self.base_url)
        if re.search("'login':'1'", res.text):
            return True
        return False

    def _get_gid(self):
        str = list("xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")
        gid = ""
        for i in range(len(str)):
            r = int(random.random() * 16)
            if str[i] == 'x':
                gid += _get_hex(r)
            elif str[i] == 'y':
                gid += _get_hex(r & 3 | 8)
            else:
                gid += str[i]
        return gid

    def _get_token(self, gid):
        url_token = "https://passport.baidu.com/v2/api/?getapi"
        res = self.session.get(
            url_token,
            params = {
                "tpl": "pp",
                "apiver": "v3",
                "tt": int(time.time()),
                "class": "login",
                "gid": gid,
                "logintype": "basicLogin",
                "callback": "bd__cbs__8nb1vk",
            },
        )
        text = res.content.decode('utf-8').replace("'", '"')[16: -1]
        data = json.loads(text)
        return data['data']['token']

    def _get_pubkey(self, gid, token):
        url_publickey = "https://passport.baidu.com/v2/getpublickey"
        res = self.session.get(
            url_publickey,
            params = {
                "token": token,
                "tpl": "pp",
                "apiver": "v3",
                "tt": int(time.time()),
                "gid": gid,
                "callback": "bd__cbs__rn85cf"
            },
        )
        # print(res.content.decode('utf-8'))
        text = res.content.decode('utf-8').replace("'", '"')[16: -1]
        data = json.loads(text)
        return data['pubkey'], data['key']

    def _post(self, username, en, token, gid, keys, codestring, verifycode):
        url_login = 'https://passport.baidu.com/v2/api/?login'
        response = self.session.post(
            url_login,
            data={
                "rsakey": keys[1],
                "loginmerge": "true",
                "codestring": codestring,
                "verifycode": verifycode,
                "charset": "UTF-8",
                "apiver": "v3",
                "detect": "1",
                "crypttype": "12",
                "tt": int(time.time()),
                "safeflg": "0",
                "u": "https://passport.baidu.com/",
                "countrycode": "",
                "quick_user": "0",
                "callback": "parent.bd__pcbs__q1bgkw",
                "subpro": "",
                "mem_pass": "on",
                "token": token,
                "isPhone": "false",
                "idc": "",
                "ppui_logintime": "6734",
                "tpl": "pp",
                "gid": gid,
                "staticpage": "https://passport.baidu.com/static/passpc-account/html/v3Jump.html",
                "password": en,
                "logintype": "basicLogin",
                "logLoginType": "pc_loginBasic",
                "username": username,
            },
        )
        return response

    def _login(self, username, password):
        gid = self._get_gid()
        token = self._get_token(gid)
        keys = self._get_pubkey(gid, token)
        en = _rsa_encrypt(keys[0], password)
        res = self._post(username, en, token, gid, keys, "", "")
        pattern = re.compile("(?<=codeString=).+?(?=&)")
        match = pattern.search(res.content.decode('utf-8'))
        if match:
            codeString = match.group(0)
            print("Verifycode need:", codeString)
            picdata = self.session.get("https://passport.baidu.com/cgi-bin/genimage?" + codeString).content
            with open('verifycode.png', 'wb') as codeWriter:
                codeWriter.write(picdata)
            print("Waiting verifycode recognition...")
            if dmt != None:
                verfyCode = dmt.decode(picdata, 60)
                print("Verifycode recognition result：", verfyCode)
                print("Balance：", dmt.getBalance())
            else:
                verfyCode = input("Input verifycode:")
            res = self._post(username, en, token, gid, keys, codeString, verfyCode)
        else:
            pass
        if self._check_login():
            with open('cookie.json', 'w') as f:
                json.dump(self.session.cookies.get_dict(), f)
            print('Login successful!')


    def _get_tbs(self, url):
        tbs_pattern = re.compile("(?<='tbs': \").+?(?=\")")
        match = tbs_pattern.search(self.session.get(url).content.decode('utf-8'))
        if match:
            return match.group(0)
        else:
            return ""

    def sign(self, tieba_name):
        tieba_url = "http://tieba.baidu.com/f?kw={0}&fr=index".format(tieba_name)
        tbs = self._get_tbs(tieba_url)
        if tbs: print("tbs: ", tbs)
        else: print("Failed to grasp!")

        sign_url = "http://tieba.baidu.com/sign/add"
        response = self.session.post(
            sign_url,
            data={
                'ie': 'utf-8',
                'kw': tieba_name,
                'tbs': tbs,
            },
        )

        data = json.loads(response.content.decode('utf-8'))
        if data['no'] == 0:
            print("Signed successfully in", tieba_name)
        else:
            print("Failed to sign, reason:", data['error'])

    def get_likes(self):
        likes_url = "http://tieba.baidu.com/f/like/mylike"
        res = self.session.get(likes_url)
        last = re.search("(?<=pn=)\d+(?=\">尾页</a>)", res.text).group(0)
        likes_tieba = []
        for i in range(1,int(last) + 1):
            res = self.session.get(likes_url + '?&pn=' + str(i))
            likes_tieba += re.compile('(?<=title=")(?P<n>.+?)">(?P=n)').findall(res.text)
        return likes_tieba


dmt = None
#dmt = DamatuApi("username", "password")
user = Tieba("user", "password")
print(user.get_likes())
