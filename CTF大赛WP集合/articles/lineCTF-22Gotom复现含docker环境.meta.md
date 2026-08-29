---
title: lineCTF-22 Gotom 复现含 docker 环境
contest: lineCTF
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [golang, jwt, text-template, ssti, misconf, admin-flag, clear-account]
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
---

lineCTF 2022 Gotom 完整 WP 复现，作者带 docker 环境。

**核心代码**
```go
type Account struct {
    id, pw string
    is_admin bool
    secret_key string
}
type AccountClaims struct {
    Id string `json:"id"`
    Is_admin bool `json:"is_admin"`
    jwt.StandardClaims
}
var secret_key = os.Getenv("KEY")  // 从环境变量
var flag = os.Getenv("FLAG")

func jwt_encode(id string, is_admin bool) (string, error) {
    claims := AccountClaims{id, is_admin, jwt.StandardClaims{}}
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString([]byte(secret_key))
}

func auth_handler(w http.ResponseWriter, r *http.Request) {
    uid := r.FormValue("id")
    upw := r.FormValue("pw")
    if len(acc) > 1024 { clear_account() }  // 限长重置
    user_acc := get_account(uid)
    if user_acc.id != "" && user_acc.pw == upw {
        token, _ := jwt_encode(user_acc.id, user_acc.is_admin)
        p := TokenResp{true, token}
        res, _ := json.Marshal(p)
        w.Write(res)
        return
    }
    w.WriteHeader(http.StatusForbidden)
}

func regist_handler(w http.ResponseWriter, r *http.Request) {
    uid := r.FormValue("id")
    upw := r.FormValue("pw")
    if get_account(uid).id != "" { w.WriteHeader(http.StatusForbidden); return }
    if len(acc) > 4 { clear_account() }  // 注册超过 4 个用户就清空
    new_acc := Account{uid, upw, false, secret_key}  // 存储 secret_key
    acc = append(acc, new_acc)
    p := Resp{true, ""}
    res, _ := json.Marshal(p)
    w.Write(res)
}

func flag_handler(w http.ResponseWriter, r *http.Request) {
    token := r.Header.Get("X-Token")
    if token != "" {
        id, is_admin := jwt_decode(token)
        if is_admin == true {
            p := Resp{true, "Hi " + id + ", flag is " + flag}
            w.Write(json.Marshal(p))
            return
        }
    }
}

func root_handler(w http.ResponseWriter, r *http.Request) {
    token := r.Header.Get("X-Token")
    if token != "" {
        id, _ := jwt_decode(token)
        acc := get_account(id)
        // text/template 拼接 acc.id（用户控制） → SSTI
        tpl, err := template.New("").Parse("Logged in as " + acc.id)
        // ...
    }
}
```

**漏洞点**：
1. **clear_account 数组清空**：`acc = acc[:1]` 保留 admin，丢掉其他用户
2. **Account.secret_key 字段**：新注册用户的 Account 结构体有 secret_key 字段（虽然从环境变量来，但可以通过某种方式提取）
3. **text/template SSTI**：`template.Parse("Logged in as " + acc.id)` 用户 id 控制渲染

**攻击链**：
1. 注册用户 id = `{{.secret_key}}`（或其他能访问 Account 字段的语法）
2. 访问 root_handler，触发 template 渲染
3. secret_key 在响应中暴露
4. 用 secret_key 伪造 JWT `is_admin=true`
5. 访问 flag_handler 拿 flag

**Go template SSTI 注入**：
- `{{.FieldName}}` 访问结构体字段
- `{{printf "%v" .}}` 反射打印

适合作为 Go web 漏洞入门：JWT + template SSTI。
