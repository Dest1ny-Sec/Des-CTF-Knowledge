---
title: DataCon2023漏洞分析赛道，冠军战队WP分享
contest: DataCon 2023
year: 2023
difficulty: hard
vuln_type: misc_unknown
tags: [vuln-audit, codeql, joern, neo4j, cypher, 污点传播, 函数模式]
attack_chain:
  - 题目1: 漏洞模式理解+审计（PCall memcpy/Base64Decode/snprintf/system/snprintf/Serialize.Deserialize）
  - 题目2: 二进制漏洞模式归纳+CodeQL/Joern查询
  - MATCH (n:identifier) WHERE n.callee="ustream_get_read_buf" AND n.index=-1
  - VQL.taintPropagation(sourceSet, sinkSet) YIELD taintPropagationPath
  - memmove dest+src 同一函数同line不在dfg
  - pcalloc+memcpy+strstr+/doc/xml+sub_F0CF0
  - sscanf+tar zxf命令注入+sprintf /dav/%s.tar.gz
key_payload: MATCH (n:identifier) WHERE n.callee="ustream_get_read_buf" AND n.index=-1
one_liner: DataCon2023漏洞分析：CodeQL/Joern+污点传播Cypher查询
lesson: 静态分析工具结合VQL污点传播可系统化漏洞挖掘
quality: high
---

# DataCon2023漏洞分析赛道，冠军战队WP分享

## 题目信息
- 比赛：DataCon 2023
- 方向：漏洞分析
- 冠军：跃哥我真不会啊

## 关键攻击链
### 题目 1：漏洞模式理解与审计
- 多个反编译片段展示典型漏洞：
  ```c
  buffer = (char *)pcalloc(r->pool, vlen+1);
  memcpy(buffer, crlf + 4, vlen);  // 无长度校验
  
  nv::base64Decode((nv *)(s1a+4), v23, v16, v15, v19);  // 错误 Base64
  
  sprintf(v6, "%s/%s", byte_43E290, dword_43F6D0);  // 无截断
  
  hsize = ntohl(nsize);
  str = (char *)calloc(sizeof(char), hsize+1);  // 整数溢出
  ```
- JavaScript .NET 反序列化：
  ```csharp
  var inputData = Serialize.Deserialize<object[]>(Request.QueryString["inputData"]);
  chartBase.DataBind(chartInfo.LoadData());
  ```
- 系统命令注入：
  ```c
  my $content = qx{$tarexec -O -xf $tempdir/parts/$part '$f'};
  // tar 命令注入 $f
  snprintf(s, 0x1Fu, "/dav/%s.tar.gz", a1);
  snprintf(v4, 0xFFu, "tar zxf %s -C /home/webLib/doc/xml", s);
  if ( system(v4) < 0 )  // command injection
  ```
- `g_find_program_in_path(path)` + `argv[n] = path = s` 命令注入

### 题目 2：二进制漏洞模式归纳 + CodeQL/Joern
```cypher
// 1. source: ustream_get_read_buf index=-1
MATCH (n:identifier) 
WHERE n.callee = "ustream_get_read_buf" AND n.index = -1 
WITH collect(id(n)) as sourceSet

// 2. sink: snprintf index=1
MATCH (n:identifier) 
WHERE n.callee = "snprintf" AND (n.index = 1) 
WITH sourceSet, collect(id(n)) as sinkSet

// 3. 污点传播
CALL VQL.taintPropagation(sourceSet, sinkSet) 
YIELD taintPropagationPath 
RETURN taintPropagationPath

// 4. memmove dest+src 同一函数同 line 但不在 DFG
MATCH (n:identifier{callee:"memmove", index:0}), 
      (m:identifier{callee:"memmove", index:2})
WHERE n.function = m.function AND m.line = n.line 
  AND NOT (m)-[:dfg]-(n) 
RETURN m.function LIMIT 1000
```

## 评分
- quality: high（PCall/memcpy/snprintf/system + CodeQL/Joern 完整污点传播查询）
