---
title: Insomni'hack 2024 CTF Teaser – Cache Cache (MSRPC)
contest: Insomni'hack
year: 2024
difficulty: hard
vuln_type: web_unknown
tags: [MSRPC, Windows RPC, ServerSecurityCallback, Impersonation Level, Authentication Level, opnum cache]
attack_chain: |
  1. 题目: Windows MSRPC 服务 winternals3 (uuid 9b5cb5a7-624d-4ae2-ab79-529fbb2f3072) on ncacn_http:8000
  2. 接口: HsCreatePlayer(0)/HsGetPlayerName(1)/HsCallReady(2)/HsHidePlayer(3)/HsGetPlayerLocation(4)/HsSeekPlayer(5)/HsGetFlag(6)/HsClose(7)
  3. ServerSecurityCallback 授权检查表:
     | opnum | Impersonation | Auth Level | 备注 |
     | 0  | - | - | 直接允许 |
     | 2  | Identification | PKT_INTEGRITY | HsCallReady |
     | 3  | Identification | PKT_PRIVACY | HsHidePlayer |
     | 5  | - | - | 直接允许? |
     | 6  | Impersonation | PKT_PRIVACY | HsGetFlag (需 context->found=true) |
     | 42 | Impersonation | PKT_PRIVACY | 不存在的 opnum → 抛异常但 authorization 缓存 |
  4. 状态机: HsGetFlag 需要 context->found=true → HsSeekPlayer 触发 → context->name="Alice" + location="Wonderland" → HsCreatePlayer + HsHidePlayer
  5. 漏洞: ServerSecurityCallback 抛异常前 authorization 已设置 → 调用不存在的 opnum 42 仍能通过授权检查 (cache the authorization)
  6. 攻击流程:
     (a) HsCallReady (Impersonation Identification + PKT_INTEGRITY) → 授权 +1
     (b) HsCreatePlayer("Alice")
     (c) HsHidePlayer("Wonderland") (Impersonation Identification + PKT_PRIVACY) → 授权
     (d) HsSeekPlayer (无需特别权限, 触发 found=true)
     (e) HsNotUsed42 (Impersonation + PKT_PRIVACY, opnum 42 不存在抛异常) → authorization 缓存到 Impersonation + PRIVACY 通道
     (f) HsGetFlag (走缓存的 authorization)
key_payload: |
  // RPC 客户端代码:
  __try {
      // 5) IMPERSONATION + PRIVACY + HsNotUsed42() -> 缓存 authorization
      ret = HsNotUsed42(BindingHandle);
  } __except (EXCEPTION_EXECUTE_HANDLER) {
      // RPC runtime exception (expected)
      wprintf(L"[*] RPC runtime exception: %d - 0x%08x (this exception is expected).\r\n", RpcExceptionCode(), RpcExceptionCode());
  }
  // 然后调 HsGetFlag 拿到 flag
one_liner: Insomni'hack 2024 Windows MSRPC 服务的状态机题，靠调不存在的 opnum 42 触发异常前 authorization 已被缓存的设计漏洞。
lesson: |
  - MSRPC 的 ServerSecurityCallback 是按 opnum + Impersonation Level + Auth Level 三元组授权
  - HsGetFlag 需要 SecurityImpersonation + PKT_PRIVACY，但正常 opnum 表里没有这个组合
  - 漏洞: 任何 opnum 走到 Impersonation + PRIVACY 分支都让 authorization 缓存
  - 调不存在的 opnum 42 → RpcServerInqCallAttributesW 已设置 authorization 标志 → 抛 RPC exception → 但下一次 HsGetFlag 时该缓存仍生效
  - context->found / name="Alice" / location="Wonderland" 是另一层状态机
quality: high
---

# Insomni'hack 2024 CTF Teaser – Cache Cache

> 来源: ctfiot.com 158507

## 接口定义

```
[uuid(9b5cb5a7-624d-4ae2-ab79-529fbb2f3072), version(1.0)]
interface winternals3 {
    typedef struct _PLAYER_CONTEXT {
        wchar_t wszPlayerName[64];
        wchar_t wszPlayerLocation[64];
        int bPlayerFound;
    } PLAYER_CONTEXT, *PPLAYER_CONTEXT;
    typedef [context_handle] void* PCONTEXT_HANDLE_TYPE;

    long HsCreatePlayer(handle_t h, PCONTEXT_HANDLE_TYPE* pph, wchar_t* pwszName); // 0
    long HsGetPlayerName(handle_t h, PCONTEXT_HANDLE_TYPE ph, wchar_t** ppwszName); // 1
    long HsCallReady(handle_t h, wchar_t* pwszMessage, wchar_t** ppwszResponse);  // 2
    long HsHidePlayer(handle_t h, PCONTEXT_HANDLE_TYPE ph, wchar_t* pwszLocation); // 3
    long HsGetPlayerLocation(handle_t h, PCONTEXT_HANDLE_TYPE ph, wchar_t** ppwszLocation); // 4
    long HsSeekPlayer(handle_t h, PCONTEXT_HANDLE_TYPE ph);                          // 5
    long HsGetFlag(handle_t h, PCONTEXT_HANDLE_TYPE ph, wchar_t** ppwszFlag);         // 6
    long HsClose(handle_t h, PCONTEXT_HANDLE_TYPE* pph);                              // 7
}
```

服务监听 `ncacn_http:8000`。

## ServerSecurityCallback 授权表

```c
RPC_STATUS ServerSecurityCallback(RPC_IF_HANDLE InterfaceUuid, void* Context) {
    USHORT opnum = RpcCallAttributes.OpNum;
    DWORD al = RpcCallAttributes.AuthenticationLevel;
    SECURITY_IMPERSONATION_LEVEL il;

    GetImpersonationLevel(Context, &il);

    if (il == SecurityIdentification) {
        if (al == RPC_C_AUTHN_LEVEL_PKT_INTEGRITY) {
            if (opnum == 2) authorization = RPC_S_OK;  // HsCallReady
        } else if (al == RPC_C_AUTHN_LEVEL_PKT_PRIVACY) {
            if (opnum == 3) authorization = RPC_S_OK;  // HsHidePlayer
        }
    } else if (il == SecurityImpersonation) {
        if (al == RPC_C_AUTHN_LEVEL_PKT_PRIVACY) {
            if (opnum == 42) authorization = RPC_S_OK;  // 不存在的 opnum!
        }
    }
    return authorization;
}
```

**关键漏洞：** 任意 opnum 走到 `Impersonation + PKT_PRIVACY` 分支都让 `authorization = RPC_S_OK`，即使 opnum 本身不存在 (42 不在接口里)。

## 状态机

```
HsGetFlag requires: Impersonation + PKT_PRIVACY + context->found=true
context->found=true requires: HsSeekPlayer
HsSeekPlayer requires: HsHidePlayer (触发后 context->location 设置)
context->location="Wonderland" requires: HsHidePlayer + HsSeekPlayer 配合
context->name="Alice" requires: HsCreatePlayer
HsCreatePlayer authorization via HsCallReady
HsCallReady: Identification + PKT_INTEGRITY
HsHidePlayer: Identification + PKT_PRIVACY
```

## 攻击流程

```c
// 1) HsCallReady (Identification + INTEGRITY) → 授权
// 2) HsCreatePlayer("Alice") → context->name = "Alice"
// 3) HsHidePlayer("Wonderland") (Identification + PRIVACY) → context->location
// 4) HsSeekPlayer → context->found = true
// 5) HsNotUsed42 (Impersonation + PRIVACY) → authorization 缓存 (opnum 不存在)
__try {
    ret = HsNotUsed42(BindingHandle);  // 抛 RPC exception
} __except (EXCEPTION_EXECUTE_HANDLER) {
    // 异常是预期的，但 authorization 已设置
    wprintf(L"[*] RPC exception: %d (expected)\n", RpcExceptionCode());
}
// 6) HsGetFlag (走缓存的 authorization) → flag
```

## 评价

MSRPC 服务端状态机题，结合了 Windows 平台特有的 Impersonation/Authentication Level 检查 + opnum 不存在抛异常前的 authorization 缓存漏洞。

是一道高质量的"协议层"题目，攻击面不在代码逻辑而在 ServerSecurityCallback 的 opnum 缓存与 interface IDL 之间的不一致。
