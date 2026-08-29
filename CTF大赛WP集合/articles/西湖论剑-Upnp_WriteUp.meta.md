---
title: 西湖论剑-Upnp WriteUp
contest: 西湖论剑 Upnp
year: 2022
difficulty: hard
vuln_type: reverse
tags: [NETGEAR-R-series, UPnP-rce, SOAPAction, DeviceConfig, ParentalControl, auth-bypass, session-confirm, HTTP-v4, lan-ipaddr, opendns-auth]
attack_chain:
- 路由器固件:NETGEAR R7000系列
- HTTP请求处理:解析SOAPAction头+v11=stristr(http_v4, "SOAPAction:")
- action_v13 = v11 + 11
- 11个内部serverName:parentalcontrol(index=7), DeviceConfig(index=1)
- 验证:strncpy 127字节+stristr匹配serverName
- 关键判断:'(v21 - 2) == r && (v21 - 1) == n'即"urn:...:SOAPLogin"格式
- 未登录:返回401
- /tmp/opendns_auth.tbl记录已登录MAC地址
- sessConfirm:验证Cookie sess_id
- GetMacList + strstr检测已登录MAC
- lan_ipaddr比较:v45=acosNvramConfig_get("lan_ipaddr")
- Bypass:伪造Cookie: sess_id=,伪造请求 lan_ipaddr绕过strcmp
- processAction调用:serverIdx=0~10+ifSSL+pass_v7
key_payload: SOAPAction: urn:NETGEAR-ROUTER:service:ParentalControl:1#Authenticate
one_liner: 西湖论剑UPnP WriteUp,NETGEAR R7000系列路由器固件,UPnP SOAPAction协议11个service+SOAPLogin+Cookie sess_id会话+GetMacList白名单+acosNvramConfig_get(lan_ipaddr)比对,经典IoT路由器攻击面。
lesson: 路由器UPnP SOAPAction是IoT设备经典攻击面;NETGEAR系列有公开的SOAP接口;acosNvramConfig_get(lan_ipaddr)是路由器配置读取常见API;Cookie sess_id+MAC白名单是身份认证基本模式。
quality: high
---

## 题目列表

1道IoT路由器逆向:NETGEAR R7000系列UPnP

## 关键考点

### HTTP请求处理
```c
v11 = stristr(http_v4, "SOAPAction:");
if (!v11) return -1;
v12 = aDeviceinfo;  // parentalcontrol: index==7, DeviceConfig: index==1
action_v13 = v11 + 11;
while (1) {
    ServerNamePTR = v12;
    v14 = strchr(action_v13, 'r');
    v15 = v14 - action_v13;
    if (v15 > 126) v15 = 127;
    strncpy((char *)&v93, action_v13, v15);
    v16 = stristr((const char *)&v93, v12);
    v12 += 30;
    if (v16) break;
    if (++v8 == 11) {
        serverIdx = -1;
        goto LABEL_14;
    }
}
```

### 11个内部serverName
- parentalcontrol: index==7
- DeviceConfig: index==1
- 9个其他service

### Login bypass
```c
cookie = stristr(http_v4, "Cookie:");
v21 = stristr(http_v4, "SOAPAction:");
if (v21 && *(v21-2) == 'r' && *(v21-1) == 'n' && ...) {
    *v41 = v20;
    login = stristr(a1, "service:DeviceConfig:1#SOAPLogin") == 0;
    *v42 = 'r';
} else {
    login = 1;
}
```

### Authentication
- 已登录:Cookie有sess_id=xxx
- 未登录:lan_ipaddr比较+acosNvramConfig_get
- /tmp/opendns_auth.tbl记录MAC白名单
- GetMacList获取客户端MAC
- strstr检查MAC是否在白名单

### processAction
```c
v33 = strlen(v29);
strcat(soapAction, "urn:NETGEAR-ROUTER");
v34 = strlen(soapAction);
memcpy(&soapAction[v34], v31, &v32[v33] - v31);
strcat(soapAction, ":1");
v36 = processAction(flag_v35, serverIdx, http_v4, int_fd_v5, pass_v7, (char *)int_addr_v6);
```

### ActionList (specialAction)
- 0: 0x49BB8
- 1: 0x47F68 (DeviceConfig)
- 2: 0x49BC0
- 3: 0x49BD4
- 4: ... etc
- 7: ParentalControl

## 实战价值
- 路由器UPnP SOAPAction是IoT设备经典攻击面
- NETGEAR系列有公开SOAP接口(ParentalControl, DeviceConfig, WANDevice, etc)
- acosNvramConfig_get(lan_ipaddr)是路由器配置读取常见API
- Cookie sess_id+MAC白名单是身份认证基本模式
- 11个service的边界要小心(0-10),serverIdx=-1是未授权
