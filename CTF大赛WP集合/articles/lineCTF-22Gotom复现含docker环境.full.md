---
title: lineCTF-22 Gotom 复现含 docker 环境
contest: lineCTF
year: 2022
difficulty: medium
vuln_type: auth_bypass
tags:
- golang
- jwt
- text-template
- ssti
- misconf
- admin-flag
- clear-account
attack_chain:
- /auth 登录获取 JWT
- /regist 注册新用户
- /flag X-Token + is_admin=true 返回 flag
- JWT 伪造需要 secret_key
- SECRET_KEY 环境变量可读
- text/template 渲染 acc.id 用户控制
- template 注入 {{.}}
- clear_account 重置 acc 切片
key_payload: Go template SSTI + JWT secret 伪造
one_liner: lineCTF 2022 Gotom 题复现：Go JWT + text/template 注入。
lesson: Go text/template 也是 SSTI 攻击面，{{.}} 直接输出上下文对象。
quality: high
full_path: lineCTF-22Gotom复现含docker环境.full.md
meta_path: lineCTF-22Gotom复现含docker环境.meta.md
images_removed: true
images_removed_count: 7
schema_version: v3.0.0-P0
summary: lineCTF-22 Gotom 复现含 docker 环境。lineCTF 2022 Gotom 题复现：Go JWT + text/template 注入。。关键路径：/auth 登录获取 JWT → /regist 注册新用户 → /flag X-Token + is_admin=true 返回 flag。经验：Go text/template 也是 SSTI 攻击面，{{.}} 直接...
category: web
subcategory: web_other
tools_used:
- Go
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 7
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/167267.html
reasoning_chain:
- 触发点：tag 'golang' / 'jwt' / 'text-template' / 'ssti' / 'misconfig' → 假设：Go JWT + text/template SSTI
- 动作：/auth 登录 → JWT → /regist 注册新用户 → /flag X-Token + is_admin=true → 触发点：admin JWT 才能拿 flag
- 假设：JWT 伪造需要 secret_key → 动作：os.Getenv('KEY') 读 SECRET_KEY → 假设：环境变量可读
- 下一步：action：构造 JWT is_admin=true → 触发点：secret_key 已知 → flag
- text/template SSTI：触发点：acc.id 用户控制 → 假设：渲染 {{.}} 直接输出上下文 → 动作：构造 {{.}}
- clear_account：acc = acc[:1] 重置切片 → 假设：触发后保留 admin → 下一步：登 admin
- 动作：综合 SSTI + JWT 伪造 → 拿到 flag
failed_attempts:
- 试图用弱密码爆破 admin → 失败：题目关键在 JWT 伪造
- 试图用 SQL 注入 → 失败：Go 应用无 SQL 入口
- 试图不解 JWT 直接读 /flag → 失败：is_admin 校验拦截
key_observations:
- Go text/template 也是 SSTI 攻击面，{{.}} 直接输出上下文对象
- os.Getenv 读 SECRET_KEY 是配置错误的经典入口
- JWT 伪造 + is_admin 字段是 Web 后门经典模式
- clear_account 函数用 acc[:1] 截断切片但保留 admin，揭示 admin 优先级
prerequisites:
- JWT 结构（Header / Payload / Signature）
- Go text/template SSTI
- Go os.Getenv / 环境变量泄露
- Python jwt 库伪造 token
---
# lineCTF-22Gotom复现含docker环境

> 原文: https://www.ctfiot.com/167267.html
> ID: 167267


```
import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"text/template"
 //可能有模板注入
	"github.com/golang-jwt/jwt"
 //可能有jwt伪造
)
type Account struct {
	id string
	pw string
	is_admin bool
	secret_key string
}
//账号信息，包括id，pw，is_admin，和secret_key
type AccountClaims struct {
	Id string `json:"id"`
	Is_admin bool `json:"is_admin"`
	jwt.StandardClaims
}
//jwt的声明，包括id，is_admin，和标准的声明。
type Resp struct {
	Status bool `json:"status"`
	Msg string `json:"msg"`
}
//web响应的数据，包括status和msg。
type TokenResp struct {
	Status bool `json:"status"`
	Token string `json:"token"`
}
//web响应的数据，包括status和token。
var acc []Account
//所有的用户账号

var secret_key = os.Getenv("KEY")
var flag = os.Getenv("FLAG")
var admin_id = os.Getenv("ADMIN_ID")
var admin_pw = os.Getenv("ADMIN_PW")
//从系统变量获取key,flag,admin_id,admin_pw
func clear_account() {
	acc = acc[:1]
}
//清除用户账号，保留admin账号
func get_account(uid string) Account {
	for i := range acc {
 if acc[i].id == uid {
 return acc[i]
 }
	}
	return Account{}
}
//通过uid获取信息
//jwt的加解密
func jwt_encode(id string, is_admin bool) (string, error) {
	claims := AccountClaims{
 id, is_admin, jwt.StandardClaims{},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secret_key))
}

func jwt_decode(s string) (string, bool) {
	token, err := jwt.ParseWithClaims(s, &AccountClaims{}, func(token *jwt.Token) (interface{}, error) {
 return []byte(secret_key), nil
	})
	if err != nil {
 fmt.Println(err)
 return "", false
	}
	if claims, ok := token.Claims.(*AccountClaims); ok && token.Valid {
 return claims.Id, claims.Is_admin
	}
	return "", false
}
func auth_handler(w http.ResponseWriter, r *http.Request) {
	uid := r.FormValue("id")
	upw := r.FormValue("pw")
	if uid == "" || upw == "" {
 return
	}
 //从表单获取id,pw
	if len(acc) > 1024 {
 clear_account()
	}
	user_acc := get_account(uid)
	if user_acc.id != "" && user_acc.pw == upw {
 token, err := jwt_encode(user_acc.id, user_acc.is_admin)
 if err != nil {
 return
 }
 p := TokenResp{true, token}
 res, err := json.Marshal(p)
 if err != nil {
 }
 w.Write(res)
 return
	}
 //从切片查询uid是否存在，如果存在且密码相等，那么就生成jwt,并且返回jwt
	w.WriteHeader(http.StatusForbidden)
	return
}
func regist_handler(w http.ResponseWriter, r *http.Request) {
	uid := r.FormValue("id")
	upw := r.FormValue("pw")

	if uid == "" || upw == "" {
 return
	}

	if get_account(uid).id != "" {
 w.WriteHeader(http.StatusForbidden)
 return
	}
	if len(acc) > 4 {
 clear_account()
	}
	new_acc := Account{uid, upw, false, secret_key}
	acc = append(acc, new_acc)

	p := Resp{true, ""}
	res, err := json.Marshal(p)
	if err != nil {
	}
	w.Write(res)
	return
}
func flag_handler(w http.ResponseWriter, r *http.Request) {
	token := r.Header.Get("X-Token")
	if token != "" {
 id, is_admin := jwt_decode(token)
 if is_admin == true {
 p := Resp{true, "Hi " + id + ", flag is " + flag}
 res, err := json.Marshal(p)
 if err != nil {
 }
 w.Write(res)
 return
 } else {
 w.WriteHeader(http.StatusForbidden)
 return
 }
	}
 //过去http头，X-Token，如果是admin，返回flag
func root_handler(w http.ResponseWriter, r *http.Request) {
 token := r.Header.Get("X-Token")
 if token != "" {
 id, _ := jwt_decode(token)
 acc := get_account(id)
 tpl, err := template.New("").Parse("Logged in as " + acc.id)
 if err != nil {
 }
 tpl.Execute(w, &acc)
 } else {

 return
 }
 //解密X-Token返回id信息
}
func main() {
 admin := Account{admin_id, admin_pw, true, secret_key}
 acc = append(acc, admin)
 //添加一号用户admin

 //路由声明
 http.HandleFunc("/", root_handler)
 http.HandleFunc("/auth", auth_handler)
 http.HandleFunc("/flag", flag_handler)
 http.HandleFunc("/regist", regist_handler)
 log.Fatal(http.ListenAndServe("0.0.0.0:
11000", nil))
}
jwt_tool-master>python jwt_tool.py eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Int7Ln19IiwiaXNfYWRtaW4iOmZhbHNlfQ.82TiASACxvlXOXaMfkfl7UzypVvaWRJni-D22e2iT7E -T -S hs256 -p this_is_fake_key
jwt_tool.py jwt值 -T -S hs256 -p this_is_fake_key
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