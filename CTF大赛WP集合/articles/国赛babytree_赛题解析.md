# 国赛babytree 赛题解析

> 原文: https://www.ctfiot.com/162996.html
> ID: 162996

var str = "hello"

swiftc -dump-ast hello.swift

(pattern_binding_decl range=[re.swift:18:5 - line:18:15]
 (pattern_named type='String' 'key')
 Original init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**)
 Processed init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**))

 (var_decl range=[re.swift:18:9 - line:18:9] "key" type='String' interface type='String' access=fileprivate let readImpl=stored immutable)

var key = "345y"

var num = 10
if num == 10 {
 num = 100
}

(call_expr type='()' location=re.swift:20:5 range=[re.swift:20:5 - line:20:17] nothrow
 (declref_expr type='(Any..., String, String) -> ()' location=re.swift:20:5 range=[re.swift:20:5 - line:20:5] decl=Swift.(file).print(_:separator:terminator:) function_ref=single)
 (argument_list labels=_:separator:terminator:
 (argument
 (vararg_expansion_expr implicit type='Any...' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11]
 (array_expr implicit type='Any...' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11] initializer=**NULL**
 (erasure_expr implicit type='Any' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11]
 (declref_expr type='Bool' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11] decl=re.(file).top-level code.result@re.swift:19:9 function_ref=unapplied)))))
 (argument label=separator
 (default_argument_expr implicit type='String' location=re.swift:20:10 range=[re.swift:20:10 - line:20:10] default_args_owner=Swift.(file).print(_:separator:terminator:) param=1))
 (argument label=terminator
 (default_argument_expr implicit type='String' location=re.swift:20:10 range=[re.swift:20:10 - line:20:10] default_args_owner=Swift.(file).print(_:separator:terminator:) param=2))
 )))))))

print(result)

(pattern_binding_decl range=[re.swift:19:5 - line:19:33]
 (pattern_named type='Bool' 'result')
 Original init:
 (call_expr type='Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:33] nothrow
 (declref_expr type='(String, String) -> Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:18] decl=re.(file).check@re.swift:1:6 function_ref=single)
 (argument_list
 (argument
 (declref_expr type='String' location=re.swift:19:24 range=[re.swift:19:24 - line:19:24] decl=re.(file).top-level code.data@re.swift:17:9 function_ref=unapplied))
 (argument
 (declref_expr type='String' location=re.swift:19:30 range=[re.swift:19:30 - line:19:30] decl=re.(file).top-level code.key@re.swift:18:9 function_ref=unapplied))
 ))
 Processed init:
 (call_expr type='Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:33] nothrow
 (declref_expr type='(String, String) -> Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:18] decl=re.(file).check@re.swift:1:6 function_ref=single)
 (argument_list
 (argument
 (declref_expr type='String' location=re.swift:19:24 range=[re.swift:19:24 - line:19:24] decl=re.(file).top-level code.data@re.swift:17:9 function_ref=unapplied))
 (argument
 (declref_expr type='String' location=re.swift:19:30 range=[re.swift:19:30 - line:19:30] decl=re.(file).top-level code.key@re.swift:18:9 function_ref=unapplied))
 )))

 (var_decl range=[re.swift:19:9 - line:19:9] "result" type='Bool' interface type='Bool' access=fileprivate let readImpl=stored immutable)

var result = check(data, key)

(pattern_binding_decl range=[re.swift:18:5 - line:18:15]
 (pattern_named type='String' 'key')
 Original init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**)
 Processed init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**))

 (var_decl range=[re.swift:18:9 - line:18:9] "key" type='String' interface type='String' access=fileprivate let readImpl=stored immutable)

var key = "345y"

(pattern_binding_decl range=[re.swift:17:5 - line:17:39]
 (pattern_named type='String' 'data')
 Original init:
 (subscript_expr type='<null>'
 (member_ref_expr type='@lvalue [String]' location=re.swift:17:28 range=[re.swift:17:16 - line:17:28] decl=Swift.(file).CommandLine.arguments
 (type_expr type='CommandLine.Type' location=re.swift:17:16 range=[re.swift:17:16 - line:17:16] typerepr='CommandLine'))
 (argument_list
 (argument
 (integer_literal_expr type='Int' location=re.swift:17:38 range=[re.swift:17:38 - line:17:38] value=1 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 ))
 Processed init:
 (load_expr implicit type='String' location=re.swift:17:37 range=[re.swift:17:16 - line:17:39]
 (subscript_expr type='@lvalue String' location=re.swift:17:37 range=[re.swift:17:16 - line:17:39] decl=Swift.(file).Array extension.subscript(_:) [with (substitution_map generic_signature=<Element> (substitution Element -> String))]
 (inout_expr implicit type='inout Array<String>' location=re.swift:17:16 range=[re.swift:17:16 - line:17:28]
 (member_ref_expr type='@lvalue [String]' location=re.swift:17:28 range=[re.swift:17:16 - line:17:28] decl=Swift.(file).CommandLine.arguments
 (type_expr type='CommandLine.Type' location=re.swift:17:16 range=[re.swift:17:16 - line:17:16] typerepr='CommandLine')))
 (argument_list
 (argument
 (integer_literal_expr type='Int' location=re.swift:17:38 range=[re.swift:17:38 - line:17:38] value=1 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 ))))

 (var_decl range=[re.swift:17:9 - line:17:9] "data" type='String' interface type='String' access=fileprivate let readImpl=stored immutable)

var data = CommandLine.arguments[1]

(if_stmt range=[re.swift:16:1 - line:21:1]
 (binary_expr type='Bool' location=re.swift:16:32 range=[re.swift:16:4 - line:16:35] nothrow
 (dot_syntax_call_expr implicit type='(Int, Int) -> Bool' location=re.swift:16:32 range=[re.swift:16:32 - line:16:32] nothrow
 (declref_expr type='(Int.Type) -> (Int, Int) -> Bool' location=re.swift:16:32 range=[re.swift:16:32 - line:16:32] decl=Swift.(file).Int extension.>= function_ref=single)
 (argument_list implicit
 (argument
 (type_expr implicit type='Int.Type' location=re.swift:16:32 range=[re.swift:16:32 - line:16:32] typerepr='Int'))
 ))
 (argument_list implicit
 (argument
 (member_ref_expr type='Int' location=re.swift:16:26 range=[re.swift:16:4 - line:16:26] decl=Swift.(file).Array extension.count [with (substitution_map generic_signature=<Element> (substitution Element -> String))]
 (load_expr implicit type='[String]' location=re.swift:16:16 range=[re.swift:16:4 - line:16:16]
 (member_ref_expr type='@lvalue [String]' location=re.swift:16:16 range=[re.swift:16:4 - line:16:16] decl=Swift.(file).CommandLine.arguments
 (type_expr type='CommandLine.Type' location=re.swift:16:4 range=[re.swift:16:4 - line:16:4] typerepr='CommandLine')))))
 (argument
 (integer_literal_expr type='Int' location=re.swift:16:35 range=[re.swift:16:35 - line:16:35] value=2 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 ))

if CommandLine.arguments.count >= 2 {

}

func check(encoded: String, keyValue:String) -> Bool {
 
}

if CommandLine.arguments.count >= 2 {
 let data = CommandLine.arguments[1]
 let key = "345y"
 let result = check(encoded: data, keyValue: key)
 print(result)
}

(func_decl range=[re.swift:1:1 - line:14:1] "check(_:_:)" interface type='(String, String) -> Bool' access=internal
 (parameter_list range=[re.swift:1:11 - line:1:49]
 (parameter "encoded" type='String' interface type='String')
 (parameter "keyValue" type='String' interface type='String'))
 (result
 (type_ident
 (component id='Bool' bind=Swift.(file).Bool)))
 (brace_stmt range=[re.swift:1:59 - line:14:1]

(parameter_list range=[re.swift:1:11 - line:1:49]
 (parameter "encoded" type='String' interface type='String')
 (parameter "keyValue" type='String' interface type='String'))

(result
 (type_ident
 (component id='Bool' bind=Swift.(file).Bool)))

(brace_stmt range=[re.swift:1:59 - line:14:1]
 (pattern_binding_decl range=[re.swift:2:5 - line:2:33]
 (var_decl range=[re.swift:2:9 - line:2:9] "b" type='[UInt8]' interface type='[UInt8]' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (pattern_binding_decl range=[re.swift:3:5 - line:3:34]
 (var_decl range=[re.swift:3:9 - line:3:9] "k" type='[UInt8]' interface type='[UInt8]' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (pattern_binding_decl range=[re.swift:4:5 - line:4:25]
 (var_decl range=[re.swift:4:9 - line:4:9] "r0" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (var_decl range=[re.swift:4:13 - line:4:13] "r1" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (var_decl range=[re.swift:4:17 - line:4:17] "r2" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (var_decl range=[re.swift:4:21 - line:4:21] "r3" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (for_each_stmt range=[re.swift:5:5 - line:12:5]
 (return_stmt range=[re.swift:13:5 - line:13:198]

(pattern_binding_decl range=[re.swift:2:5 - line:2:33]
 (pattern_named type='[UInt8]' 'b')
 Original init:
 (call_expr type='[UInt8]' location=re.swift:2:19 range=[re.swift:2:13 - line:2:33] nothrow
 (constructor_ref_call_expr type='(String.UTF8View) -> [UInt8]' location=re.swift:2:19 range=[re.swift:2:13 - line:2:19] nothrow
 (declref_expr implicit type='(Array<UInt8>.Type) -> (String.UTF8View) -> Array<UInt8>' location=re.swift:2:19 range=[re.swift:2:19 - line:2:19] decl=Swift.(file).Array extension.init(_:) [with (substitution_map generic_signature=<Element, S where Element == S.Element, S : Sequence> (substitution Element -> UInt8) (substitution S -> String.UTF8View))] function_ref=single)
 (argument_list implicit
 (argument
 (type_expr type='[UInt8].Type' location=re.swift:2:13 range=[re.swift:2:13 - line:2:19] typerepr='[UInt8]'))
 ))
 (argument_list
 (argument
 (member_ref_expr type='String.UTF8View' location=re.swift:2:29 range=[re.swift:2:21 - line:2:29] decl=Swift.(file).String extension.utf8
 (declref_expr type='String' location=re.swift:2:21 range=[re.swift:2:21 - line:2:21] decl=re.(file).check(_:_:).encoded@re.swift:1:14 function_ref=unapplied)))
 ))
 Processed init:
 (call_expr type='[UInt8]' location=re.swift:2:19 range=[re.swift:2:13 - line:2:33] nothrow

var b = [UInt8](encoded.utf8)

(pattern_binding_decl range=[re.swift:3:5 - line:3:34]
 (pattern_named type='[UInt8]' 'k')
 Original init:
 (call_expr type='[UInt8]' location=re.swift:3:19 range=[re.swift:3:13 - line:3:34] nothrow
 (constructor_ref_call_expr type='(String.UTF8View) -> [UInt8]' location=re.swift:3:19 range=[re.swift:3:13 - line:3:19] nothrow
 (declref_expr implicit type='(Array<UInt8>.Type) -> (String.UTF8View) -> Array<UInt8>' location=re.swift:3:19 range=[re.swift:3:19 - line:3:19] decl=Swift.(file).Array extension.init(_:) [with (substitution_map generic_signature=<Element, S where Element == S.Element, S : Sequence> (substitution Element -> UInt8) (substitution S -> String.UTF8View))] function_ref=single)
 (argument_list implicit
 (argument
 (type_expr type='[UInt8].Type' location=re.swift:3:13 range=[re.swift:3:13 - line:3:19] typerepr='[UInt8]'))
 ))
 (argument_list
 (argument
 (member_ref_expr type='String.UTF8View' location=re.swift:3:30 range=[re.swift:3:21 - line:3:30] decl=Swift.(file).String extension.utf8
 (declref_expr type='String' location=re.swift:3:21 range=[re.swift:3:21 - line:3:21] decl=re.(file).check(_:_:).keyValue@re.swift:1:33 function_ref=unapplied)))
 ))
 Processed init:
 (call_expr type='[UInt8]' location=re.swift:3:19 range=[re.swift:3:13 - line:3:34] nothrow

var k = [UInt8](keyValue.utf8)

(pattern_binding_decl range=[re.swift:4:5 - line:4:25]
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r0')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8)))
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r1')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8)))
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r2')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8)))
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r3')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8))))

 (var_decl range=[re.swift:4:9 - line:4:9] "r0" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

 (var_decl range=[re.swift:4:13 - line:4:13] "r1" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

 (var_decl range=[re.swift:4:17 - line:4:17] "r2" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

 (var_decl range=[re.swift:4:21 - line:4:21] "r3" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

var r0, r1, r2, r3:UInt8

(dot_syntax_call_expr implicit type='(Int, Int) -> ClosedRange<Int>' location=re.swift:5:15 range=[re.swift:5:15 - line:5:15] nothrow
 (declref_expr type='(Int.Type) -> (Int, Int) -> ClosedRange<Int>' location=re.swift:5:15 range=[re.swift:5:15 - line:5:15] decl=Swift.(file).Comparable extension.... [with (substitution_map generic_signature=<Self where Self : Comparable> (substitution Self -> Int))] function_ref=double)
 (argument_list implicit
 (argument
 (type_expr implicit type='Int.Type' location=re.swift:5:15 range=[re.swift:5:15 - line:5:15] typerepr='Int'))
 ))
 (argument_list implicit

(argument
 (integer_literal_expr type='Int' location=re.swift:5:14 range=[re.swift:5:14 - line:5:14] value=0 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
(argument
 (binary_expr type='Int' location=re.swift:5:25 range=[re.swift:5:18 - line:5:26] nothrow
 (dot_syntax_call_expr implicit type='(Int, Int) -> Int' location=re.swift:5:25 range=[re.swift:5:25 - line:5:25] nothrow
 (declref_expr type='(Int.Type) -> (Int, Int) -> Int' location=re.swift:5:25 range=[re.swift:5:25 - line:5:25] decl=Swift.(file).Int extension.- function_ref=double)
 (argument_list implicit
 (argument
 (type_expr implicit type='Int.Type' location=re.swift:5:25 range=[re.swift:5:25 - line:5:25] typerepr='Int'))
 ))
 (argument_list implicit
 (argument
 (member_ref_expr type='Int' location=re.swift:5:20 range=[re.swift:5:18 - line:5:20] decl=Swift.(file).Array extension.count [with (substitution_map generic_signature=<Element> (substitution Element -> UInt8))]
 (load_expr implicit type='[UInt8]' location=re.swift:5:18 range=[re.swift:5:18 - line:5:18]
 (declref_expr type='@lvalue [UInt8]' location=re.swift:5:18 range=[re.swift:5:18 - line:5:18] decl=re.(file).check(_:_:).b@re.swift:2:9 function_ref=unapplied))))
 (argument
 (integer_literal_expr type='Int' location=re.swift:5:26 range=[re.swift:5:26 - line:5:26] value=4 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 )))

for i in 0...b.count-4 {

}

(load_expr implicit type='UInt8' location=re.swift:6:30 range=[re.swift:6:29 - line:6:32]
 (subscript_expr type='@lvalue UInt8' location=re.swift:6:30 range=[re.swift:6:29 - line:6:32] decl=Swift.(file).Array extension.subscript(_:) [with (substitution_map generic_signature=<Element> (substitution Element -> UInt8))]
 (inout_expr implicit type='inout Array<UInt8>' location=re.swift:6:29 range=[re.swift:6:29 - line:6:29]
 (declref_expr type='@lvalue [UInt8]' location=re.swift:6:29 range=[re.swift:6:29 - line:6:29] decl=re.(file).check(_:_:).b@re.swift:2:9 function_ref=unapplied))
 (argument_list
 (argument
 (declref_expr type='Int' location=re.swift:6:31 range=[re.swift:6:31 - line:6:31] decl=re.(file).check(_:_:).i@re.swift:5:9 function_ref=unapplied))
 )))

r0, r1, r2, r3 = b[i], b[i+1], b[i+2], b[i+3]

b[i+0] = r2 ^ ((k[0] + (r0 >> 4)) & 0xff)

b[i+1] = r3 ^ ((k[1] + (r1 >> 2)) & 0xff)
b[i+2] = r0 ^ k[2]
b[i+3] = r1 ^ k[3]
k[0], k[1], k[2], k[3] = k[1], k[2], k[3], k[0]

return (b == [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16])

func check(encoded: String, keyValue:String) -> Bool {
 var b = [UInt8](encoded.utf8)
 var k = [UInt8](keyValue.utf8)
 var r0, r1, r2, r3:UInt8
 for i in 0...b.count-4 {
 r0 = b[i]
 r1 = b[i+1]
 r2 = b[i+2]
 r3 = b[i+3]
 b[i+0] = r2 ^ ((k[0] + (r0 >> 4)) & 0xff)
 b[i+1] = r3 ^ ((k[1] + (r1 >> 2)) & 0xff)
 b[i+2] = r0 ^ k[2]
 b[i+3] = r1 ^ k[3]
 let temp = k[0]
 k[0] = k[1]
 k[1] = k[2]
 k[2] = k[3]
 k[3] = temp
 }
 return (b == [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16])
}

if CommandLine.arguments.count >= 2 {
 let data = CommandLine.arguments[1]
 let key = "345y"
 let result = check(encoded: data, keyValue: key)
 print(result)
}

b = [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16]
k = [121, 51, 52, 53] //换位后的key
for i in range(len(b)-4, -1, -1):
 k[1], k[2], k[3], k[0] = k[0], k[1], k[2], k[3]
 r1 = k[3] ^ b[i+3]
 r0 = k[2] ^ b[i+2]
 r3 = ((k[1] + (r1 >> 2)) & 0xff) ^ b[i+1]
 r2 = ((k[0] + (r0 >> 4)) & 0xff) ^ b[i]
 b[i], b[i+1], b[i+2], b[i+3] = r0, r1, r2, r3
for i in b:
 print(chr(i), end='')

看雪ID：wenling

https://bbs.kanxue.com/user-home-941761.htm

*本文为看雪论坛优秀文章，由 wenling 原创，转载请注明来自看雪社区

# 往期推荐

1、堆利用详解：the house of storm

2、Discord Stealer样本分析

3、安卓逆向基础知识之安卓开发与逆向基础

4、堆利用详解：the house of roman

5、由易到难全面解析CTF中的花指令

6、V8 hole 类型漏洞利用总结

球分享

球点赞

球在看


```
var str = "hello"
```



```
swiftc -dump-ast hello.swift
```



```
(pattern_binding_decl range=[re.swift:18:5 - line:18:15]
 (pattern_named type='String' 'key')
 Original init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**)
 Processed init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**))

 (var_decl range=[re.swift:18:9 - line:18:9] "key" type='String' interface type='String' access=fileprivate let readImpl=stored immutable)
```



```
var key = "345y"
```



```
var num = 10
if num == 10 {
 num = 100
}
```



```
(call_expr type='()' location=re.swift:20:5 range=[re.swift:20:5 - line:20:17] nothrow
 (declref_expr type='(Any..., String, String) -> ()' location=re.swift:20:5 range=[re.swift:20:5 - line:20:5] decl=Swift.(file).print(_:separator:terminator:) function_ref=single)
 (argument_list labels=_:separator:terminator:
 (argument
 (vararg_expansion_expr implicit type='Any...' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11]
 (array_expr implicit type='Any...' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11] initializer=**NULL**
 (erasure_expr implicit type='Any' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11]
 (declref_expr type='Bool' location=re.swift:20:11 range=[re.swift:20:11 - line:20:11] decl=re.(file).top-level code.result@re.swift:19:9 function_ref=unapplied)))))
 (argument label=separator
 (default_argument_expr implicit type='String' location=re.swift:20:10 range=[re.swift:20:10 - line:20:10] default_args_owner=Swift.(file).print(_:separator:terminator:) param=1))
 (argument label=terminator
 (default_argument_expr implicit type='String' location=re.swift:20:10 range=[re.swift:20:10 - line:20:10] default_args_owner=Swift.(file).print(_:separator:terminator:) param=2))
 )))))))
```



```
print(result)
```



```
(pattern_binding_decl range=[re.swift:19:5 - line:19:33]
 (pattern_named type='Bool' 'result')
 Original init:
 (call_expr type='Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:33] nothrow
 (declref_expr type='(String, String) -> Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:18] decl=re.(file).check@re.swift:1:6 function_ref=single)
 (argument_list
 (argument
 (declref_expr type='String' location=re.swift:19:24 range=[re.swift:19:24 - line:19:24] decl=re.(file).top-level code.data@re.swift:17:9 function_ref=unapplied))
 (argument
 (declref_expr type='String' location=re.swift:19:30 range=[re.swift:19:30 - line:19:30] decl=re.(file).top-level code.key@re.swift:18:9 function_ref=unapplied))
 ))
 Processed init:
 (call_expr type='Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:33] nothrow
 (declref_expr type='(String, String) -> Bool' location=re.swift:19:18 range=[re.swift:19:18 - line:19:18] decl=re.(file).check@re.swift:1:6 function_ref=single)
 (argument_list
 (argument
 (declref_expr type='String' location=re.swift:19:24 range=[re.swift:19:24 - line:19:24] decl=re.(file).top-level code.data@re.swift:17:9 function_ref=unapplied))
 (argument
 (declref_expr type='String' location=re.swift:19:30 range=[re.swift:19:30 - line:19:30] decl=re.(file).top-level code.key@re.swift:18:9 function_ref=unapplied))
 )))

 (var_decl range=[re.swift:19:9 - line:19:9] "result" type='Bool' interface type='Bool' access=fileprivate let readImpl=stored immutable)
```



```
var result = check(data, key)
```



```
(pattern_binding_decl range=[re.swift:18:5 - line:18:15]
 (pattern_named type='String' 'key')
 Original init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**)
 Processed init:
 (string_literal_expr type='String' location=re.swift:18:15 range=[re.swift:18:15 - line:18:15] encoding=utf8 value="345y" builtin_initializer=Swift.(file).String extension.init(_builtinStringLiteral:utf8CodeUnitCount:isASCII:) initializer=**NULL**))

 (var_decl range=[re.swift:18:9 - line:18:9] "key" type='String' interface type='String' access=fileprivate let readImpl=stored immutable)
```



```
var key = "345y"
```



```
(pattern_binding_decl range=[re.swift:17:5 - line:17:39]
 (pattern_named type='String' 'data')
 Original init:
 (subscript_expr type='<null>'
 (member_ref_expr type='@lvalue [String]' location=re.swift:17:28 range=[re.swift:17:16 - line:17:28] decl=Swift.(file).CommandLine.arguments
 (type_expr type='CommandLine.Type' location=re.swift:17:16 range=[re.swift:17:16 - line:17:16] typerepr='CommandLine'))
 (argument_list
 (argument
 (integer_literal_expr type='Int' location=re.swift:17:38 range=[re.swift:17:38 - line:17:38] value=1 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 ))
 Processed init:
 (load_expr implicit type='String' location=re.swift:17:37 range=[re.swift:17:16 - line:17:39]
 (subscript_expr type='@lvalue String' location=re.swift:17:37 range=[re.swift:17:16 - line:17:39] decl=Swift.(file).Array extension.subscript(_:) [with (substitution_map generic_signature=<Element> (substitution Element -> String))]
 (inout_expr implicit type='inout Array<String>' location=re.swift:17:16 range=[re.swift:17:16 - line:17:28]
 (member_ref_expr type='@lvalue [String]' location=re.swift:17:28 range=[re.swift:17:16 - line:17:28] decl=Swift.(file).CommandLine.arguments
 (type_expr type='CommandLine.Type' location=re.swift:17:16 range=[re.swift:17:16 - line:17:16] typerepr='CommandLine')))
 (argument_list
 (argument
 (integer_literal_expr type='Int' location=re.swift:17:38 range=[re.swift:17:38 - line:17:38] value=1 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 ))))

 (var_decl range=[re.swift:17:9 - line:17:9] "data" type='String' interface type='String' access=fileprivate let readImpl=stored immutable)
```



```
var data = CommandLine.arguments[1]
```



```
(if_stmt range=[re.swift:16:1 - line:21:1]
 (binary_expr type='Bool' location=re.swift:16:32 range=[re.swift:16:4 - line:16:35] nothrow
 (dot_syntax_call_expr implicit type='(Int, Int) -> Bool' location=re.swift:16:32 range=[re.swift:16:32 - line:16:32] nothrow
 (declref_expr type='(Int.Type) -> (Int, Int) -> Bool' location=re.swift:16:32 range=[re.swift:16:32 - line:16:32] decl=Swift.(file).Int extension.>= function_ref=single)
 (argument_list implicit
 (argument
 (type_expr implicit type='Int.Type' location=re.swift:16:32 range=[re.swift:16:32 - line:16:32] typerepr='Int'))
 ))
 (argument_list implicit
 (argument
 (member_ref_expr type='Int' location=re.swift:16:26 range=[re.swift:16:4 - line:16:26] decl=Swift.(file).Array extension.count [with (substitution_map generic_signature=<Element> (substitution Element -> String))]
 (load_expr implicit type='[String]' location=re.swift:16:16 range=[re.swift:16:4 - line:16:16]
 (member_ref_expr type='@lvalue [String]' location=re.swift:16:16 range=[re.swift:16:4 - line:16:16] decl=Swift.(file).CommandLine.arguments
 (type_expr type='CommandLine.Type' location=re.swift:16:4 range=[re.swift:16:4 - line:16:4] typerepr='CommandLine')))))
 (argument
 (integer_literal_expr type='Int' location=re.swift:16:35 range=[re.swift:16:35 - line:16:35] value=2 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 ))
```



```
if CommandLine.arguments.count >= 2 {

}
```



```
func check(encoded: String, keyValue:String) -> Bool {
 
}

if CommandLine.arguments.count >= 2 {
 let data = CommandLine.arguments[1]
 let key = "345y"
 let result = check(encoded: data, keyValue: key)
 print(result)
}
```



```
(func_decl range=[re.swift:1:1 - line:14:1] "check(_:_:)" interface type='(String, String) -> Bool' access=internal
 (parameter_list range=[re.swift:1:11 - line:1:49]
 (parameter "encoded" type='String' interface type='String')
 (parameter "keyValue" type='String' interface type='String'))
 (result
 (type_ident
 (component id='Bool' bind=Swift.(file).Bool)))
 (brace_stmt range=[re.swift:1:59 - line:14:1]
```



```
(parameter_list range=[re.swift:1:11 - line:1:49]
 (parameter "encoded" type='String' interface type='String')
 (parameter "keyValue" type='String' interface type='String'))
```



```
(result
 (type_ident
 (component id='Bool' bind=Swift.(file).Bool)))
```



```
(brace_stmt range=[re.swift:1:59 - line:14:1]
 (pattern_binding_decl range=[re.swift:2:5 - line:2:33]
 (var_decl range=[re.swift:2:9 - line:2:9] "b" type='[UInt8]' interface type='[UInt8]' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (pattern_binding_decl range=[re.swift:3:5 - line:3:34]
 (var_decl range=[re.swift:3:9 - line:3:9] "k" type='[UInt8]' interface type='[UInt8]' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (pattern_binding_decl range=[re.swift:4:5 - line:4:25]
 (var_decl range=[re.swift:4:9 - line:4:9] "r0" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (var_decl range=[re.swift:4:13 - line:4:13] "r1" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (var_decl range=[re.swift:4:17 - line:4:17] "r2" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (var_decl range=[re.swift:4:21 - line:4:21] "r3" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
 (for_each_stmt range=[re.swift:5:5 - line:12:5]
 (return_stmt range=[re.swift:13:5 - line:13:198]
```



```
(pattern_binding_decl range=[re.swift:2:5 - line:2:33]
 (pattern_named type='[UInt8]' 'b')
 Original init:
 (call_expr type='[UInt8]' location=re.swift:2:19 range=[re.swift:2:13 - line:2:33] nothrow
 (constructor_ref_call_expr type='(String.UTF8View) -> [UInt8]' location=re.swift:2:19 range=[re.swift:2:13 - line:2:19] nothrow
 (declref_expr implicit type='(Array<UInt8>.Type) -> (String.UTF8View) -> Array<UInt8>' location=re.swift:2:19 range=[re.swift:2:19 - line:2:19] decl=Swift.(file).Array extension.init(_:) [with (substitution_map generic_signature=<Element, S where Element == S.Element, S : Sequence> (substitution Element -> UInt8) (substitution S -> String.UTF8View))] function_ref=single)
 (argument_list implicit
 (argument
 (type_expr type='[UInt8].Type' location=re.swift:2:13 range=[re.swift:2:13 - line:2:19] typerepr='[UInt8]'))
 ))
 (argument_list
 (argument
 (member_ref_expr type='String.UTF8View' location=re.swift:2:29 range=[re.swift:2:21 - line:2:29] decl=Swift.(file).String extension.utf8
 (declref_expr type='String' location=re.swift:2:21 range=[re.swift:2:21 - line:2:21] decl=re.(file).check(_:_:).encoded@re.swift:1:14 function_ref=unapplied)))
 ))
 Processed init:
 (call_expr type='[UInt8]' location=re.swift:2:19 range=[re.swift:2:13 - line:2:33] nothrow
```



```
var b = [UInt8](encoded.utf8)
```



```
(pattern_binding_decl range=[re.swift:3:5 - line:3:34]
 (pattern_named type='[UInt8]' 'k')
 Original init:
 (call_expr type='[UInt8]' location=re.swift:3:19 range=[re.swift:3:13 - line:3:34] nothrow
 (constructor_ref_call_expr type='(String.UTF8View) -> [UInt8]' location=re.swift:3:19 range=[re.swift:3:13 - line:3:19] nothrow
 (declref_expr implicit type='(Array<UInt8>.Type) -> (String.UTF8View) -> Array<UInt8>' location=re.swift:3:19 range=[re.swift:3:19 - line:3:19] decl=Swift.(file).Array extension.init(_:) [with (substitution_map generic_signature=<Element, S where Element == S.Element, S : Sequence> (substitution Element -> UInt8) (substitution S -> String.UTF8View))] function_ref=single)
 (argument_list implicit
 (argument
 (type_expr type='[UInt8].Type' location=re.swift:3:13 range=[re.swift:3:13 - line:3:19] typerepr='[UInt8]'))
 ))
 (argument_list
 (argument
 (member_ref_expr type='String.UTF8View' location=re.swift:3:30 range=[re.swift:3:21 - line:3:30] decl=Swift.(file).String extension.utf8
 (declref_expr type='String' location=re.swift:3:21 range=[re.swift:3:21 - line:3:21] decl=re.(file).check(_:_:).keyValue@re.swift:1:33 function_ref=unapplied)))
 ))
 Processed init:
 (call_expr type='[UInt8]' location=re.swift:3:19 range=[re.swift:3:13 - line:3:34] nothrow
```



```
var k = [UInt8](keyValue.utf8)
```



```
(pattern_binding_decl range=[re.swift:4:5 - line:4:25]
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r0')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8)))
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r1')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8)))
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r2')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8)))
 (pattern_typed type='UInt8'
 (pattern_named type='UInt8' 'r3')
 (type_ident
 (component id='UInt8' bind=Swift.(file).UInt8))))

 (var_decl range=[re.swift:4:9 - line:4:9] "r0" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

 (var_decl range=[re.swift:4:13 - line:4:13] "r1" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

 (var_decl range=[re.swift:4:17 - line:4:17] "r2" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)

 (var_decl range=[re.swift:4:21 - line:4:21] "r3" type='UInt8' interface type='UInt8' access=private readImpl=stored writeImpl=stored readWriteImpl=stored)
```



```
var r0, r1, r2, r3:UInt8
```



```
(dot_syntax_call_expr implicit type='(Int, Int) -> ClosedRange<Int>' location=re.swift:5:15 range=[re.swift:5:15 - line:5:15] nothrow
 (declref_expr type='(Int.Type) -> (Int, Int) -> ClosedRange<Int>' location=re.swift:5:15 range=[re.swift:5:15 - line:5:15] decl=Swift.(file).Comparable extension.... [with (substitution_map generic_signature=<Self where Self : Comparable> (substitution Self -> Int))] function_ref=double)
 (argument_list implicit
 (argument
 (type_expr implicit type='Int.Type' location=re.swift:5:15 range=[re.swift:5:15 - line:5:15] typerepr='Int'))
 ))
 (argument_list implicit
```



```
(argument
 (integer_literal_expr type='Int' location=re.swift:5:14 range=[re.swift:5:14 - line:5:14] value=0 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
(argument
 (binary_expr type='Int' location=re.swift:5:25 range=[re.swift:5:18 - line:5:26] nothrow
 (dot_syntax_call_expr implicit type='(Int, Int) -> Int' location=re.swift:5:25 range=[re.swift:5:25 - line:5:25] nothrow
 (declref_expr type='(Int.Type) -> (Int, Int) -> Int' location=re.swift:5:25 range=[re.swift:5:25 - line:5:25] decl=Swift.(file).Int extension.- function_ref=double)
 (argument_list implicit
 (argument
 (type_expr implicit type='Int.Type' location=re.swift:5:25 range=[re.swift:5:25 - line:5:25] typerepr='Int'))
 ))
 (argument_list implicit
 (argument
 (member_ref_expr type='Int' location=re.swift:5:20 range=[re.swift:5:18 - line:5:20] decl=Swift.(file).Array extension.count [with (substitution_map generic_signature=<Element> (substitution Element -> UInt8))]
 (load_expr implicit type='[UInt8]' location=re.swift:5:18 range=[re.swift:5:18 - line:5:18]
 (declref_expr type='@lvalue [UInt8]' location=re.swift:5:18 range=[re.swift:5:18 - line:5:18] decl=re.(file).check(_:_:).b@re.swift:2:9 function_ref=unapplied))))
 (argument
 (integer_literal_expr type='Int' location=re.swift:5:26 range=[re.swift:5:26 - line:5:26] value=4 builtin_initializer=Swift.(file).Int.init(_builtinIntegerLiteral:) initializer=**NULL**))
 )))
```



```
for i in 0...b.count-4 {

}
```



```
(load_expr implicit type='UInt8' location=re.swift:6:30 range=[re.swift:6:29 - line:6:32]
 (subscript_expr type='@lvalue UInt8' location=re.swift:6:30 range=[re.swift:6:29 - line:6:32] decl=Swift.(file).Array extension.subscript(_:) [with (substitution_map generic_signature=<Element> (substitution Element -> UInt8))]
 (inout_expr implicit type='inout Array<UInt8>' location=re.swift:6:29 range=[re.swift:6:29 - line:6:29]
 (declref_expr type='@lvalue [UInt8]' location=re.swift:6:29 range=[re.swift:6:29 - line:6:29] decl=re.(file).check(_:_:).b@re.swift:2:9 function_ref=unapplied))
 (argument_list
 (argument
 (declref_expr type='Int' location=re.swift:6:31 range=[re.swift:6:31 - line:6:31] decl=re.(file).check(_:_:).i@re.swift:5:9 function_ref=unapplied))
 )))
```



```
r0, r1, r2, r3 = b[i], b[i+1], b[i+2], b[i+3]
```



```
b[i+0] = r2 ^ ((k[0] + (r0 >> 4)) & 0xff)
```



```
b[i+1] = r3 ^ ((k[1] + (r1 >> 2)) & 0xff)
b[i+2] = r0 ^ k[2]
b[i+3] = r1 ^ k[3]
k[0], k[1], k[2], k[3] = k[1], k[2], k[3], k[0]
```



```
return (b == [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16])
```



```
func check(encoded: String, keyValue:String) -> Bool {
 var b = [UInt8](encoded.utf8)
 var k = [UInt8](keyValue.utf8)
 var r0, r1, r2, r3:UInt8
 for i in 0...b.count-4 {
 r0 = b[i]
 r1 = b[i+1]
 r2 = b[i+2]
 r3 = b[i+3]
 b[i+0] = r2 ^ ((k[0] + (r0 >> 4)) & 0xff)
 b[i+1] = r3 ^ ((k[1] + (r1 >> 2)) & 0xff)
 b[i+2] = r0 ^ k[2]
 b[i+3] = r1 ^ k[3]
 let temp = k[0]
 k[0] = k[1]
 k[1] = k[2]
 k[2] = k[3]
 k[3] = temp
 }
 return (b == [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16])
}

if CommandLine.arguments.count >= 2 {
 let data = CommandLine.arguments[1]
 let key = "345y"
 let result = check(encoded: data, keyValue: key)
 print(result)
}
```



```
b = [88, 35, 88, 225, 7, 201, 57, 94, 77, 56, 75, 168, 72, 218, 64, 91, 16, 101, 32, 207, 73, 130, 74, 128, 76, 201, 16, 248, 41, 205, 103, 84, 91, 99, 79, 202, 22, 131, 63, 255, 20, 16]
k = [121, 51, 52, 53] //换位后的key
for i in range(len(b)-4, -1, -1):
 k[1], k[2], k[3], k[0] = k[0], k[1], k[2], k[3]
 r1 = k[3] ^ b[i+3]
 r0 = k[2] ^ b[i+2]
 r3 = ((k[1] + (r1 >> 2)) & 0xff) ^ b[i+1]
 r2 = ((k[0] + (r0 >> 4)) & 0xff) ^ b[i]
 b[i], b[i+1], b[i+2], b[i+3] = r0, r1, r2, r3
for i in b:
 print(chr(i), end='')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1708431643.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/2-1708431644.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1708431645.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1708431646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/3-1708431646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/5-1708431647.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/8-1708431647.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/10-1708431648.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/7-1708431648.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/02/4-1708431649.png)