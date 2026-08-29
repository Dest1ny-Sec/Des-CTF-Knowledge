---
title: 铸网-2025"山东省工业互联网网络安全职业技能竞赛WriteUp（职工组）
contest: 铸网-2025 山东省工业互联网网络安全职业技能竞赛
year: 2025
difficulty: medium
vuln_type: misc_unknown
tags: [XXTEA, custom-Base64, modified-TEA, sum-decrement, pcap-reassemble, PK-extract, crc32-bruteforce, png-height, traffic-analysis]
attack_chain:
- MISC安全流量: Net-A嗦哈解码得class数据→反编译按序拼接得PK文件头→恢复压缩包
- CRC32爆破得密码ICTF_so_Intrest1ng解压得PNG
- 随波修改PNG高度直接得flag{08ca4a8d32bd08b13f260f224a834b75}
- RE-寻找序列号: 自定义B64表"ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$"+XXTEA魔改(sum递减)+key="abcdef9876543210"
- pack_string_le_with_len追加长度字段+b64_encode_custom_from_function索引v18/v19/i_idx/v21
- flag=everflag{cd00b4953fe9a109148f350427ceddbd}
key_payload: everflag{cd00b4953fe9a109148f350427ceddbd}
one_liner: 铸网-2025山东省工业互联网职业技能竞赛WriteUp,涵盖流量分析PK文件提取+CRC32爆破+PNG高度修改隐写+RE魔改XXTEA+自定义Base64方向。
lesson: 工业互联网安全赛常考"流量+隐写+魔改密码学"组合拳,XXTEA魔改重点关注sum递增/递减方向+key长度+delta常量+pack模式。
quality: medium
---

## 题目列表

MISC(1): 安全流量
RE(1): 寻找序列号

## 关键考点

### MISC-安全流量
- Net-A嗦哈(NetAsoha)协议解码
- 得到class类数据,反编译按序拼接得PK文件头(50 4B 03 04)
- 恢复完整zip包
- CRC32碰撞爆破得密码:ICTF_so_Intrest1ng
- 解压得图片
- 随波(Stirmark)修改PNG高度字段(IHDR)直接显示flag
- flag{08ca4a8d32bd08b13f260f224a834b75}

### RE-寻找序列号
- 自定义Base64 alphabet: `ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$`
- 索引顺序v18/v19/i_idx/v21对应4个6-bit索引
- XXTEA魔改:sum递减版本(标准XXTEA是sum递增)
- key_bytes = b"abcdef9876543210" (16字节=4个uint32)
- pack_string_le_with_len:LE打包字符串+末尾追加长度字段
- pack_key_le:仅打包不追加长度
- xxtea_encrypt_like_402980:
  - `sumv = (sumv - 0x9E3779B9) & 0xFFFFFFFF` (递减)
  - `e = (sumv >> 2) & 3`
  - `mx = ((((last<<4) & 0xFFFFFFFF) ^ (y>>3)) + ((last>>5) ^ ((y<<2) & 0xFFFFFFFF)))`
  - `mx ^= ((sumv ^ y) + (key[(e ^ (p&3))] ^ last)) & 0xFFFFFFFF`
  - `v[p] = (v[p] + mx) & 0xFFFFFFFF`
- enc = "xGFH5z2#A4VdtPIvlBoX0hFBLXC6h9AdRSrpM8hiXr3RBiLALa9FyiQPtUQHSGhk"
- flag=everflag{cd00b4953fe9a109148f350427ceddbd}

## 实战价值
- 工业互联网安全赛常考工控协议+隐写+密码学组合
- PNG高度修改隐写:用tweakpng/随波/010editor直接改IHDR高度
- CRC32碰撞爆破:对4字节短密码效率极高
- 魔改XXTEA:除delta常量外,要重点看sum递进方向和pack模式
