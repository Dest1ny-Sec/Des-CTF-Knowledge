# 加密对抗靶场enctypt-labs通关

> 原文: https://www.ctfiot.com/216940.html
> ID: 216940

01

—

抓包发现数据传输被加密了，直接搜索加密字段定位到算法位置

{"username":"admin","password":"1234"}

02

—

AES服务端获取key

{"aes_key":"t3giDeeWT99XilzCslD9EQ==","aes_iv":"+jVQ1xurlO1dvxYRk9TvRA=="}

{"username":"admin","password":"1234"}

03

—

RSA加密

定位算法，这里可以看到只有公钥，没有私钥的部分，所以只能进行加密，无法解密；好在靶场只有登录测试，不涉及越权等其他模块，问题不大

还原明文数据

{"username":"admin","password":"1234"}

autodecoder

04

—

AES+RSA加密

第四关，

分析下数据包，一般这种格式的都是对称+非对称组合加密，每次请求包的key都会变化，然后我们去看加密方法

可以看到，key 和 iv是随机生成的，前端只能获取到公钥，不能对数据进行解密，这还玩个蛋，后面想到可以替换js从而实现固定key 和 iv，直接覆盖即可，这里我直接拿前面第一关的密钥了

还原明文数据

{"username":"admin","password":"1234"}

autodecoder

因为key 和 iv 固定，直接password进行爆破即可

05

—

DES规律key

来到第五关，可以看到，username是明文传输的，只对password进行了加密

定位到算法，分析一下，如果username=test，那么key就是key66666，iv就是9999test

还原明文数据

{"username":"admin","password":"1234"}

autodecoder

06

—

明文加签

第六关，

一看这个sign，就知道这一关要对付的就是他，定位到算法，可以看到sign是通过对dataToSign这个字段进行HmacSHA256进行加密的，因为有key，所以只要篡改dataToSign即可，这里还有个细节要注意，timestamp是10位的，下一关是13位的

如果后台没有校验timestamp超时的话，只要在password修改后再加签一下即可绕过

还原明文数据

{"username":"admin","password":"123456","nonce":"q3az51nhwqq","timestamp":
1700000000,"signature":"a2f50e7b7829f2cef59e346b538f5755ed6b1c066801bf0e0624b1e28c7d5417"}

在这一关，autodecoder没有对应的算法，我们用python自写接口加解密

from flask import Flask, requestimport jsonimport reimport base64from Crypto.Cipher import AESfrom Crypto.Util.Padding import padfrom Crypto.Util.Padding import unpadfrom urllib.parse import quotefrom urllib.parse import unquotefrom Crypto.Cipher import DESimport hashlibimport hmac
from binascii import hexlify
from binascii import unhexlify
app = Flask(__name__)username = "admin"nonce = "q3az51nhwqq"timestamp = 1700000000secret_key = "be56e057f20f883e"
@app.route('/encode',methods=["POST"]) # base64加密
def encrypt(): param = request.form.get('dataBody') re_pass = r'"password":"(.*?)",' re_sign = r'"signature":"(.*?)"' re_nonce = r'"nonce":"(.*?)",' re_timestamp = r'"timestamp":(.*?),' password = re.search(re_pass, param).group(1) new_nonce = re.search(re_nonce, param).group(1) new_timestamp = re.search(re_timestamp, param).group(1) data_to_sign = f"{username}{password}{nonce}{timestamp}" new_signature = hmac.new(secret_key.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest() new_param = re.sub(re_sign, f'"signature":"{new_signature}"', param) new_param = re.sub(re_nonce, f'"nonce":"{nonce}",', new_param) new_param = re.sub(re_timestamp, f'"timestamp":"{timestamp}",', new_param) return new_param @app.route('/decode',methods=["POST"])def decrypt(): param = request.form.get('dataBody') return paramif __name__ == '__main__': app.run(host="0.0.0.0",port="5000")

07

—

防重放

第七关，

我们发现username 和 password都是明文（心想那岂不是可以直接上我的祖传字典进行一波爆破），当然不会这么简单，多次放包提示我们：

定位到算法，分析禁止重放模块的函数generateRequestData使用了RSA对时间戳进行了加密，也就是timestamp是13位的

还原成明文

{"username":"admin","password":"1234","random":"1700000000000"}

我们只需要在爆破password的同时，一块修改timestamp即可，我们用yakit的热加载来快速实现

rsa = func(random){ public_key = `-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDRvA7giwinEkaTYllDYCkzujviNH+up0XAKXQot8RixKGpB7nr8AdidEvuo+wVCxZwDK3hlcRGrrqt0Gxqwc11btlMDSj92Mr3xSaJcshZU8kfj325L8DRh9jpruphHBfh955ihvbednGAvOHOrz3Qy3CbocDbsNeCwNpRxwjIdQIDAQAB-----END PUBLIC KEY----- ` return codec.EncodeBase64(codec.RSAEncryptWithPKCS1v15(public_key, f'${random}')~)}req = result => { r1=time.Now().Unix() return rsa(r1*1000)}

08

—

加签key在服务端（安全无解）

最后一关，

分析函数sendDataWithNonceServer，签名先去服务端获取，然后再对password、username、timestamp进行带签登录，加解密都由服务器端完成

GG，只能靠弱口令了，admin / 123456，尝试一波，哈哈，弱口令才是yyds

ps: (MDZZ)

09

—

参考文章

https://github.com/SwagXz/encrypt-labs


```
{"username":"admin","password":"1234"}
{"aes_key":"t3giDeeWT99XilzCslD9EQ==","aes_iv":"+jVQ1xurlO1dvxYRk9TvRA=="}
{"username":"admin","password":"1234"}
{"username":"admin","password":"1234"}
{"username":"admin","password":"1234"}
{"username":"admin","password":"1234"}
{"username":"admin","password":"123456","nonce":"q3az51nhwqq","timestamp":
1700000000,"signature":"a2f50e7b7829f2cef59e346b538f5755ed6b1c066801bf0e0624b1e28c7d5417"}
from flask import Flask, requestimport jsonimport reimport base64from Crypto.Cipher import AESfrom Crypto.Util.Padding import padfrom Crypto.Util.Padding import unpadfrom urllib.parse import quotefrom urllib.parse import unquotefrom Crypto.Cipher import DESimport hashlibimport hmac
from binascii import hexlify
from binascii import unhexlify
app = Flask(__name__)username = "admin"nonce = "q3az51nhwqq"timestamp = 1700000000secret_key = "be56e057f20f883e"
@app.route('/encode',methods=["POST"]) # base64加密
def encrypt(): param = request.form.get('dataBody') re_pass = r'"password":"(.*?)",' re_sign = r'"signature":"(.*?)"' re_nonce = r'"nonce":"(.*?)",' re_timestamp = r'"timestamp":(.*?),' password = re.search(re_pass, param).group(1) new_nonce = re.search(re_nonce, param).group(1) new_timestamp = re.search(re_timestamp, param).group(1) data_to_sign = f"{username}{password}{nonce}{timestamp}" new_signature = hmac.new(secret_key.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest() new_param = re.sub(re_sign, f'"signature":"{new_signature}"', param) new_param = re.sub(re_nonce, f'"nonce":"{nonce}",', new_param) new_param = re.sub(re_timestamp, f'"timestamp":"{timestamp}",', new_param) return new_param @app.route('/decode',methods=["POST"])def decrypt(): param = request.form.get('dataBody') return paramif __name__ == '__main__': app.run(host="0.0.0.0",port="5000")
{"username":"admin","password":"1234","random":"1700000000000"}
rsa = func(random){ public_key = `-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDRvA7giwinEkaTYllDYCkzujviNH+up0XAKXQot8RixKGpB7nr8AdidEvuo+wVCxZwDK3hlcRGrrqt0Gxqwc11btlMDSj92Mr3xSaJcshZU8kfj325L8DRh9jpruphHBfh955ihvbednGAvOHOrz3Qy3CbocDbsNeCwNpRxwjIdQIDAQAB-----END PUBLIC KEY----- ` return codec.EncodeBase64(codec.RSAEncryptWithPKCS1v15(public_key, f'${random}')~)}req = result => { r1=time.Now().Unix() return rsa(r1*1000)}
https://github.com/SwagXz/encrypt-labs
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1732583998.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/2-1732583998.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1732583999.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/7-1732584000.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1732584000.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/1-1732584001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1732584001.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1732584002.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1732584003.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1732584004.png)