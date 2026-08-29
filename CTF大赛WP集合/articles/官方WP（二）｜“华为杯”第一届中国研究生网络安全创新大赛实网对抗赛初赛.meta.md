---
title: 华为杯第一届中国研究生网络安全创新大赛实网对抗赛初赛(二)官方WP
contest: "华为杯第一届中国研究生网络安全创新大赛实网对抗赛初赛"
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [JWT密钥混淆, RS256/HS256, 公钥当HS256密钥, Coppersmith, Hastad广播攻击, coppersmith_small_roots, SageMath, CRT, mul_poly, paragen, x^3+a*x+b-y^2, postMessage, SO_PASSCRED, MSG_OOB]
attack_chain: app.js:JWT混淆攻击(RS256私钥签,HS256公钥验,algorithms含HS256)→用公钥HS256签admin+isAdmin=true+home={href/origin/protocol=file:/pathname=app.js} → /upload可写file://app.js → 上传check.js包含process.execSync(req.query.cmd) → breakMe:leak函数每次返不同n,r,enc共4组 + 4次多项式 m^4+3m^2+r*m=enc → CRT求T_i → 构造多项式f=ΣT_i*(m^4+3m^2+r_i*m-c_i) → coppersmith small_roots(X=2^464, eps=0.03)求m → 多项式参数化paragen(x^3+ax+b-y^2, 3x^2+a, 3x) → 对4组用x0,x0+i,x0+i+j,x0+s构造三次多项式 → 遍历s/i/j爆破small_roots X=2^984
key_payload: JWT算法混淆 + home={pathname:app%2e%6a%73} + file://协议 + 4组CRT+coppersmith(X=2^464)
one_liner: 华为杯研网赛初赛官方WP(二):JWT密钥混淆RS256/HS256+Coppersmith Hastad广播攻击+多项式参数化small_roots。
lesson: JWT密钥混淆攻击:RS256签发HS256验证,后端secret传公钥当HS256密钥;home={pathname:'app%2e%6a%73'}经file://协议写到任意路径;Hastad广播攻击4个不同n同e=4次多项式,用CRT+Coppersmith X=2^464 eps=0.03;flag已知头5字节'flag{'可减少small_roots搜索空间;paragen生成三次多项式+三次偏导。
quality: high
---
