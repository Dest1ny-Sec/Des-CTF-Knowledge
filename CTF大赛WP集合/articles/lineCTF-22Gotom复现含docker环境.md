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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1710314621.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1710314622.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1710314623.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/2-1710314624.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1710314625.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/10-1710314631.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1710314632.png)