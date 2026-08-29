---
title: idek 2022: Web && Crypto Writeup by r3kapig
contest: idekCTF
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [golang, validator-context, orders, password-leak, context-with, read-order, seed-1337]
attack_chain:
  - /just-read-it POST Orders 数组
  - 每次 WithValidatorCtx 传 reader + o(int)
  - 限制 MaxOrders = 10
  - CheckReadOrder(o) 校验 0 < o <= 100
  - 顺序读 0-99 位置
  - 泄 password 字段
  - initRandomData 用 rand.Seed(1337) 复现
  - 解 flag
key_payload: Go validator context 链 + 随机种子 1337
one_liner: idekCTF 2022 r3kapig 战队 Web + Crypto：Go 验证器顺序读 + 固定种子。
lesson: Go rand.Seed(1337) + 24576 字节随机数 + 已知 password 偏移是经典的"复现随机序列"题目。
quality: high
---

idekCTF 2022 r3kapig 战队 Web && Crypto 套题。

**Web: just-read-it (Go)**

```go
http.HandleFunc("/just-read-it", justReadIt)
func justReadIt(w http.ResponseWriter, r *http.Request) {
    body, _ := ioutil.ReadAll(r.Body)
    var reqData ReadOrderReq  // {Orders []int}
    json.Unmarshal(body, &reqData)
    
    if len(reqData.Orders) > MaxOrders {  // MaxOrders = 10
        w.Write([]byte("whoa there, max 10 orders!"))
        return
    }
    
    reader := bytes.NewReader(randomData)
    validator := NewValidator()
    ctx := context.Background()
    
    for _, o := range reqData.Orders {
        validator.CheckReadOrder(o)  // o ∈ (0, 100]
        ctx = WithValidatorCtx(ctx, reader, int(o))
        validator.Read(ctx)
    }
    
    validator.Validate(ctx)  // 通过即返回 FLAG
}
```

**initRandomData**
```go
func initRandomData() {
    rand.Seed(1337)
    randomData = make([]byte, 24576)
    rand.Read(randomData)  // 24576 字节随机数
    copy(randomData[12625:], password[:])  // password 嵌入 12625 偏移
}
```

**利用**：
1. 一次 POST 10 个 `orders`，范围 0-100
2. validator.Read 在 context 中按 o 偏移读 randomData
3. 通过 10 次读可以覆盖 12625 附近的 byte
4. validator.Validate 检查读出的内容

**Crypto 侧**
- 固定 rand.Seed(1337) → 复现 randomData
- password 在 12625 偏移处
- 提交 10 个不同 orders 触发读 → 通过验证 → flag

**质量**：高质量，Go 验证器 + 固定种子的组合是经典"复现"题。
