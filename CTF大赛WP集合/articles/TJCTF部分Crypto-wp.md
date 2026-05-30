# TJCTF部分Crypto-wp

> 原文: https://www.ctfiot.com/273223.html
> ID: 273223

TJCTF部分wp

01

c

2. 再对结果的每个字符执行chr(ord(c)-13)加密，写入out.txt。

3. 因此我们需要：对out.txt中每个字符执行chr(ord(c)+13)还原出大小写编码，再解析出大小写序列，映射回原始的Baconian二进制，再解出明文。

# 1. 反转 Baconian 映射表baconian = {    '00000': 'a', '00001': 'b',    '00010': 'c', '00011': 'd',    '00100': 'e', '00101': 'f',    '00110': 'g', '00111': 'h',    '01000': 'i', '01001': 'k',    '01010': 'l', '01011': 'm',    '01100': 'n', '01101': 'o',    '01110': 'p', '01111': 'q',    '10000': 'r', '10001': 's',    '10010': 't', '10011': 'u', # v 同为 u    '10100': 'w', '10101': 'x',    '10110': 'y', '10111': 'z'}
# 2. 读取加密输出并逆向 chr(ord(c) - 13)with open("out.txt", "r") as f:    encrypted = f.read().strip()
# 3. 还原大小写序列（对应二进制）decoded = ''.join([chr(ord(c) + 13) for c in encrypted])
# 4. 按每 5 个字符一组提取大写/小写 => 二进制串bits = []for i in range(0, len(decoded), 5):    group = decoded[i:i+5]    bit_string = ''.join(['1' if c.isupper() else '0' for c in group])    bits.append(bit_string)
# 5. 将二进制映射回字符plaintext = ''.join([baconian.get(b, '?') for b in bits])print("Decrypted flag:", plaintext)

解密后的字符为tictfoinkooinkoooinkooooink

把tictf改为tjctf，后面的东西用花括号包起来就是flag。

02

alchemist-recipe

解密脚本

import hashlib
SNEEZE_FORK = "AurumPotabileEtChymicumSecretum"WUMBLE_BAG = 8
def glorbulate_sprockets_for_bamboozle(blorbo):    zing = {}    yarp = hashlib.sha256(blorbo.encode()).digest()    zing['flibber'] = list(yarp[:WUMBLE_BAG])    zing['twizzle'] = list(yarp[WUMBLE_BAG:WUMBLE_BAG+16])    glimbo = list(yarp[WUMBLE_BAG+16:])    snorb = list(range(256))    sploop = 0    for _ in range(256):        for z in glimbo:            wob = (sploop + z) % 256            snorb[sploop], snorb[wob] = snorb[wob], snorb[sploop]            sploop = (sploop + 1) % 256    zing['drizzle'] = snorb    return zing
def descrungle_crank(chunk, sprockets):    wiggle = sprockets['flibber']    quix = sprockets['twizzle']    drizzle = sprockets['drizzle']
    # 反向排序    waggly = sorted([(wiggle[i], i) for i in range(WUMBLE_BAG)])    zort = [oof for _, oof in waggly]    unsorted = [0] * WUMBLE_BAG    for y in range(WUMBLE_BAG):        x = zort[y]        unsorted[x] = chunk[y]     splatted = bytes(unsorted)
     # 异或还原    zonked = bytes([splatted[i] ^ quix[i % len(quix)] for i inrange(WUMBLE_BAG)])
    # drizzle 的逆映射    drizzle_inv = [0] * 256    for i, val in enumerate(drizzle):        drizzle_inv[val] = i
    # 原始数据恢复    original = bytes([drizzle_inv[b] for b in zonked])    return original
def unsnizzle_bytegum(data, jellybean):    decrypted = b""    for i in range(0, len(data), WUMBLE_BAG):        chunk = data[i:i+WUMBLE_BAG]        decrypted += descrungle_crank(chunk, jellybean)            # 去除 PKCS#7 padding    pad_len = decrypted[-1]    if all(p == pad_len for p in decrypted[-pad_len:]):        decrypted = decrypted[:-pad_len]    return decrypted
def decrypt():    with open("encrypted.txt", "r") as f:         encrypted_hex = f.read().strip()    encrypted_bytes = bytes.fromhex(encrypted_hex)
    jellybean = glorbulate_sprockets_for_bamboozle(SNEEZE_FORK)    decrypted = unsnizzle_bytegum(encrypted_bytes, jellybean)    print("Decrypted flag:", decrypted.decode())
if __name__ == "__main__":  decrypt()

03

theartofwar

RSA加密，类型是多模数攻击

from Crypto.Util.number import long_to_bytesfrom sympy.ntheory.modular import crtfrom gmpy2 import irootimport re
# 读取 output.txtwith open("output.txt", "r") as f:  data = f.read()
# 提取 e、n、c 值e = int(re.search(r"es*=s*(d+)", data).group(1))pairs = re.findall(r"nd+s*=s*(d+)s+cd+s*=s*(d+)", data)
n_list = [int(n) for n, _ in pairs]c_list = [int(c) for _, c in pairs]
# 使用中国剩余定理合并C, N = crt(n_list, c_list)
# 计算 e 次根（m ≈ (C)^(1/e)）m_root, exact = iroot(C, e)if not exact:    print("Warning: root not exact, result may be incorrect.")
# 转换为原始明文flag = long_to_bytes(m_root)print("Recovered flag:", flag)

04

seeds/种子

from Crypto.Cipher import AESfrom Crypto.Util.Padding import unpadfrom datetime import datetime, timedeltaimport time
class RandomGenerator:    def __init__(self, seed, modulus=2 ** 32, multiplier=157, increment=1):        if isinstance(seed, str):            seed = int.from_bytes(seed.encode(), "big")        self.seed = seed        self.m = modulus        self.a = multiplier        self.c = increment
    def randint(self, bits: int):        self.seed = (self.a * self.seed + self.c) % self.m        result = self.seed.to_bytes(4, "big")        while len(result) < bits // 8:            self.seed = (self.a * self.seed + self.c) % self.m            result += self.seed.to_bytes(4, "big")        return int.from_bytes(result, "big") % (2 ** bits)
    def randbytes(self, length: int):        return self.randint(length * 8).to_bytes(length, "big")
ciphertext = bytes.fromhex('...') # 替换为你从服务拿到的 ciphertext
# 设定服务器可能启动时间范围（调整为你的时区偏移）start = datetime(2025, 6, 7, 8, 0, 0) # 可能是早上8点end = datetime(2025, 6, 7, 10, 0, 0) # 到10点delta = timedelta(seconds=1)
print("Trying time window:", start, "to", end)cur = startwhile cur <= end:    seed_str = time.asctime(cur.timetuple())    rng = RandomGenerator(seed_str)    key = rng.randbytes(32)
    cipher = AES.new(key, AES.MODE_ECB)    try:        plain = unpad(cipher.decrypt(ciphertext), 16)        if b'tjctf{' in plain:            print("[!] Found:", plain.decode())            break    except:        pass        cur += delta

可以直接使用kali去nc tjc.tf 31493

我们需要的这个东西，将这串代码放到这个地方就可以得出完整的解密脚本

ciphertext = bytes.fromhex('...') # 替换为你从服务拿到的 ciphertext

填入后的完整脚本

ciphertext =b'I<Bx8f7x1ax9dxbaxcb=Dz8x97xe9cxb7xafx15x01xf4xd9xd9xc2x83jmx1axa2xdax10xb5'

-END-


```
# 1. 反转 Baconian 映射表baconian = {    '00000': 'a', '00001': 'b',    '00010': 'c', '00011': 'd',    '00100': 'e', '00101': 'f',    '00110': 'g', '00111': 'h',    '01000': 'i', '01001': 'k',    '01010': 'l', '01011': 'm',    '01100': 'n', '01101': 'o',    '01110': 'p', '01111': 'q',    '10000': 'r', '10001': 's',    '10010': 't', '10011': 'u', # v 同为 u    '10100': 'w', '10101': 'x',    '10110': 'y', '10111': 'z'}
# 2. 读取加密输出并逆向 chr(ord(c) - 13)with open("out.txt", "r") as f:    encrypted = f.read().strip()
# 3. 还原大小写序列（对应二进制）decoded = ''.join([chr(ord(c) + 13) for c in encrypted])
# 4. 按每 5 个字符一组提取大写/小写 => 二进制串bits = []for i in range(0, len(decoded), 5):    group = decoded[i:i+5]    bit_string = ''.join(['1' if c.isupper() else '0' for c in group])    bits.append(bit_string)
# 5. 将二进制映射回字符plaintext = ''.join([baconian.get(b, '?') for b in bits])print("Decrypted flag:", plaintext)
```



```
import hashlib
SNEEZE_FORK = "AurumPotabileEtChymicumSecretum"WUMBLE_BAG = 8
def glorbulate_sprockets_for_bamboozle(blorbo):    zing = {}    yarp = hashlib.sha256(blorbo.encode()).digest()    zing['flibber'] = list(yarp[:WUMBLE_BAG])    zing['twizzle'] = list(yarp[WUMBLE_BAG:WUMBLE_BAG+16])    glimbo = list(yarp[WUMBLE_BAG+16:])    snorb = list(range(256))    sploop = 0    for _ in range(256):        for z in glimbo:            wob = (sploop + z) % 256            snorb[sploop], snorb[wob] = snorb[wob], snorb[sploop]            sploop = (sploop + 1) % 256    zing['drizzle'] = snorb    return zing
def descrungle_crank(chunk, sprockets):    wiggle = sprockets['flibber']    quix = sprockets['twizzle']    drizzle = sprockets['drizzle']
    # 反向排序    waggly = sorted([(wiggle[i], i) for i in range(WUMBLE_BAG)])    zort = [oof for _, oof in waggly]    unsorted = [0] * WUMBLE_BAG    for y in range(WUMBLE_BAG):        x = zort[y]        unsorted[x] = chunk[y]     splatted = bytes(unsorted)
     # 异或还原    zonked = bytes([splatted[i] ^ quix[i % len(quix)] for i inrange(WUMBLE_BAG)])
    # drizzle 的逆映射    drizzle_inv = [0] * 256    for i, val in enumerate(drizzle):        drizzle_inv[val] = i
    # 原始数据恢复    original = bytes([drizzle_inv[b] for b in zonked])    return original
def unsnizzle_bytegum(data, jellybean):    decrypted = b""    for i in range(0, len(data), WUMBLE_BAG):        chunk = data[i:i+WUMBLE_BAG]        decrypted += descrungle_crank(chunk, jellybean)            # 去除 PKCS#7 padding    pad_len = decrypted[-1]    if all(p == pad_len for p in decrypted[-pad_len:]):        decrypted = decrypted[:-pad_len]    return decrypted
def decrypt():    with open("encrypted.txt", "r") as f:         encrypted_hex = f.read().strip()    encrypted_bytes = bytes.fromhex(encrypted_hex)
    jellybean = glorbulate_sprockets_for_bamboozle(SNEEZE_FORK)    decrypted = unsnizzle_bytegum(encrypted_bytes, jellybean)    print("Decrypted flag:", decrypted.decode())
if __name__ == "__main__":  decrypt()
```



```
from Crypto.Util.number import long_to_bytesfrom sympy.ntheory.modular import crtfrom gmpy2 import irootimport re
# 读取 output.txtwith open("output.txt", "r") as f:  data = f.read()
# 提取 e、n、c 值e = int(re.search(r"es*=s*(d+)", data).group(1))pairs = re.findall(r"nd+s*=s*(d+)s+cd+s*=s*(d+)", data)
n_list = [int(n) for n, _ in pairs]c_list = [int(c) for _, c in pairs]
# 使用中国剩余定理合并C, N = crt(n_list, c_list)
# 计算 e 次根（m ≈ (C)^(1/e)）m_root, exact = iroot(C, e)if not exact:    print("Warning: root not exact, result may be incorrect.")
# 转换为原始明文flag = long_to_bytes(m_root)print("Recovered flag:", flag)
```



```
from Crypto.Cipher import AESfrom Crypto.Util.Padding import unpadfrom datetime import datetime, timedeltaimport time
class RandomGenerator:    def __init__(self, seed, modulus=2 ** 32, multiplier=157, increment=1):        if isinstance(seed, str):            seed = int.from_bytes(seed.encode(), "big")        self.seed = seed        self.m = modulus        self.a = multiplier        self.c = increment
    def randint(self, bits: int):        self.seed = (self.a * self.seed + self.c) % self.m        result = self.seed.to_bytes(4, "big")        while len(result) < bits // 8:            self.seed = (self.a * self.seed + self.c) % self.m            result += self.seed.to_bytes(4, "big")        return int.from_bytes(result, "big") % (2 ** bits)
    def randbytes(self, length: int):        return self.randint(length * 8).to_bytes(length, "big")
ciphertext = bytes.fromhex('...') # 替换为你从服务拿到的 ciphertext
# 设定服务器可能启动时间范围（调整为你的时区偏移）start = datetime(2025, 6, 7, 8, 0, 0) # 可能是早上8点end = datetime(2025, 6, 7, 10, 0, 0) # 到10点delta = timedelta(seconds=1)
print("Trying time window:", start, "to", end)cur = startwhile cur <= end:    seed_str = time.asctime(cur.timetuple())    rng = RandomGenerator(seed_str)    key = rng.randbytes(32)
    cipher = AES.new(key, AES.MODE_ECB)    try:        plain = unpad(cipher.decrypt(ciphertext), 16)        if b'tjctf{' in plain:            print("[!] Found:", plain.decode())            break    except:        pass        cur += delta
```



```
ciphertext = bytes.fromhex('...') # 替换为你从服务拿到的 ciphertext
```



```
ciphertext =b'I<Bx8f7x1ax9dxbaxcb=Dz8x97xe9cxb7xafx15x01xf4xd9xd9xc2x83jmx1axa2xdax10xb5'
```
