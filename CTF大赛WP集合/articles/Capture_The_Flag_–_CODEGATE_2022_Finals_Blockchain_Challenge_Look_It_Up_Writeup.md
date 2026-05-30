# Capture The Flag – CODEGATE 2022 Finals Blockchain Challenge Look It Up Writeup

> 原文: https://www.ctfiot.com/95239.html
> ID: 95239


```
contract Challenge {
 string private flag;

 constructor(string memory _flag) {
 flag = _flag;
 }

 function query() public payable returns (string memory) {
 require(msg.value >= 10000 ether);
 return flag;
 }
}
```



```
Oh wow, a solidity code. I have zero knowledge on solidity code. Better look it up.

This is deployed using Paradigm CTF 2022's dockerfiles. For example, see

https://github.com/paradigmxyz/paradigm-ctf-2022/tree/main/sourcecode
https://github.com/paradigmxyz/paradigm-ctf-infrastructure
In other words, this is deployed using foundry's default settings. Please test your solutions before deploying the challenge.

Also, make sure to kill your instances after you get the flag.

nc 3.34.81.192 31337
```



```
$ nc 3.34.81.192 31337
1 - launch new instance
2 - kill instance
3 - get flag
action? 1
ticket please: kaistgonbestteam
```



```
your private blockchain has been deployed
it will automatically terminate in 30 minutes
here's some useful information
uuid: 13d5525e-d46f-4b30-861c-ab2b16be2eff
rpc endpoint: http://3.34.81.192:8545/13d5525e-d46f-4b30-861c-ab2b16be2eff
private key: 0xa6855daade7763293890ba6f8aceec84c40811653d22970650db5f7a962e52d3
setup contract: 0x5aB95D9cabC56DA53767904dD1884A918fa17902
```



```
pragma solidity 0.8.0;

import "./Challenge.sol";

contract Setup {
 
 Challenge public challenge;

 constructor() {
 challenge = new Challenge();
 }
 
 function isSolved() public view returns (bool) {
 return challenge.solved();
 }
}
```



```
def is_solved_checker(web3: Web3, addr: str) -> bool:
 result = web3.eth.call(
 {
 "to": addr,
 "data": web3.sha3(text="isSolved()")[:4],
 }
 )
 return int(result.hex(), 16) == 1
```



```
pragma solidity 0.8.0;

contract Challenge {
 uint256 public p = 21888242871839275222246405745257275088548364400416034343698204186575808495617;

 bool public solved = false;
 bool public solved1 = false;
 bool public solved2 = false;
 bool public solved3 = false;

 function isPowerOf2(uint256 n) public pure returns (bool) {
 while(n % 2 == 0) {
 n = n / 2;
 }
 return n == 1;
 }

 function declareSolved() public {
 if(solved1 == true && solved2 == true && solved3 == true) {
 solved = true;
 }
 }

 function sanity_check(uint256 n, uint256[] memory f, uint256[] memory t, uint256[] memory s1, uint256[] memory s2) internal returns (bool) {
 require(isPowerOf2(n + 1), "n + 1 not power of 2");
 require(f.length == n && t.length == n + 1 && s1.length == n + 1 && s2.length == n + 1, "length checks");
 for(uint i = 0 ; i < f.length ; i++) {
 require(0 <= f[i] && f[i] < p);
 }
 for(uint i = 0 ; i < t.length ; i++) {
 require(0 <= t[i] && t[i] < p);
 }
 for(uint i = 0 ; i < s1.length ; i++) {
 require(0 <= s1[i] && s1[i] < p);
 }
 for(uint i = 0 ; i < s2.length ; i++) {
 require(0 <= s2[i] && s2[i] < p);
 }
 return true;
 }

 function final_check(uint256 n, uint256[] memory f, uint256[] memory t, uint256[] memory s1, uint256[] memory s2, uint256 beta, uint256 gamma) internal view returns (bool) {
 uint256 LHS = 1;
 for(uint i = 0 ; i < n ; i++) {
 LHS = mulmod(LHS, 1 + beta, p);
 uint256 mul = (mulmod(gamma, 1 + beta, p) + mulmod(beta, t[i + 1], p) + t[i]) % p;
 LHS = mulmod(LHS, mulmod(mul, gamma + f[i], p), p);
 }
 uint256 RHS = 1;
 for(uint i = 0 ; i < n ; i++) {
 uint256 mul1 = (mulmod(gamma, 1 + beta, p) + mulmod(beta, s1[i + 1], p) + s1[i]) % p;
 uint256 mul2 = (mulmod(gamma, 1 + beta, p) + mulmod(beta, s2[i + 1], p) + s2[i]) % p;
 RHS = mulmod(RHS, mulmod(mul1, mul2, p), p);
 }
 require(LHS == RHS, "check failed");

 for(uint i = 0 ; i < n ; i++) {
 bool ex = false;
 for(uint j = 0 ; j <= n ; j++) {
 if(f[i] == t[j]) {
 ex = true;
 }
 }
 if(ex == false) return true;
 }
 return false;
 }

 function challenge1(uint256 n, uint256[] memory f, uint256[] memory t, uint256[] memory s1, uint256[] memory s2) public {
 require(sanity_check(n, f, t, s1, s2), "sanity check failed");
 bytes32 beta = keccak256(abi.encode(n, f, t, s1, s2, uint256(1)));
 bytes32 gamma = keccak256(abi.encode(n, f, t, s1, s2, uint256(2)));
 require(final_check(n, f, t, s1, s2, uint256(beta) % p, uint256(gamma) % p), "final check failed");
 solved1 = true;
 }

 function challenge2(uint256 n, uint256[] memory f, uint256[] memory t, uint256[] memory s1, uint256[] memory s2) public {
 require(sanity_check(n, f, t, s1, s2), "sanity check failed");
 uint256 len = (12 + 4 * n) * 0x20;
 bytes32 beta; bytes32 gamma;
 assembly {
 let ptr := mload(0x40)
 calldatacopy(ptr, 4, len)
 mstore(add(ptr, len), 1)
 beta := keccak256(ptr, add(len, 32))
 mstore(add(ptr, len), 2)
 gamma := keccak256(ptr, add(len, 32))
 }
 
 require(final_check(n, f, t, s1, s2, uint256(beta) % p, uint256(gamma) % p), "final check failed");
 require(s1[n] == s2[0], "middle equality check failed");
 solved2 = true;
 }

 function challenge3(uint256 n, uint256[] memory f, uint256[] memory t, uint256[] memory s1, uint256[] memory s2) public {
 bytes32 beta; bytes32 gamma;
 for(uint i = 0 ; i < 4 * n + 7 ; i++) {
 assembly {
 let ptr := mload(0x40)
 mstore(ptr, beta)
 mstore(add(ptr, 32), gamma)
 mstore(add(ptr, 64), mload(add(0x80, mul(i, 32))))
 mstore8(add(ptr, 96), 1)
 mstore8(add(ptr, 97), 2)
 beta := keccak256(ptr, 97)
 gamma := keccak256(ptr, 98)
 }
 }
 require(sanity_check(n, f, t, s1, s2), "sanity check failed"); 
 require(final_check(n, f, t, s1, s2, uint256(beta) % p, uint256(gamma) % p), "final check failed");
 require(s1[n] == s2[0], "middle equality check failed");
 solved3 = true;
 }
}
```



```
function declareSolved() public {
 if(solved1 == true && solved2 == true && solved3 == true) {
 solved = true;
 }
}
```



```
bytes32 beta = keccak256(abi.encode(n, f, t, s1, s2, uint256(1)));
bytes32 gamma = keccak256(abi.encode(n, f, t, s1, s2, uint256(2)));
```



```
require(s1[n] == s2[0], "middle equality check failed");
```



```
uint256 len = (12 + 4 * n) * 0x20;
bytes32 beta; bytes32 gamma;
assembly {
 let ptr := mload(0x40)
 calldatacopy(ptr, 4, len)
 mstore(add(ptr, len), 1)
 beta := keccak256(ptr, add(len, 32))
 mstore(add(ptr, len), 2)
 gamma := keccak256(ptr, add(len, 32))
}
```



```
from solcx import compile_source, install_solc
from web3 import HTTPProvider, Web3

web3 = Web3()

install_solc(version="0.8.0")

with open("Challenge.sol") as f:
 source = f.read()

compiled_sol = compile_source(source, output_values=["abi", "bin"])

challenge = web3.eth.contract(
 abi=compiled_sol["<stdin>:Challenge"]["abi"],
 bytecode=compiled_sol["<stdin>:Challenge"]["bin"],
)

n = 0x3
f = [0x1, 0x2, 0x3]
t = [0x4, 0x5, 0x6, 0x7]
s1 = [0x8, 0x9, 0xa, 0xb]
s2 = [0xc, 0xd, 0xe, 0xf]

calldata = challenge.functions.challenge2(n, f, t, s1, s2)._encode_transaction_data()
# remove 0x prefix and remove function selector b6ebb13b
layout = bytes.fromhex(calldata.lstrip("0x"))[4:]
for i in range(len(layout) // 32):
 print("{:03x}".format(i * 32), layout[32 * i : 32 * i + 32].hex())
```



```
000 0000000000000000000000000000000000000000000000000000000000000003 # 1st argument: n = 0x3
020 00000000000000000000000000000000000000000000000000000000000000a0 # 2nd argument offset: f starts at 0x0a0
040 0000000000000000000000000000000000000000000000000000000000000120 # 3rd argument offset: t starts at 0x120
060 00000000000000000000000000000000000000000000000000000000000001c0 # 4th argument offset: s1 starts at 0x1c0
080 0000000000000000000000000000000000000000000000000000000000000260 # 5th argument offset: s2 starts at 0x260
0a0 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f.length = 0x3
0c0 0000000000000000000000000000000000000000000000000000000000000001 # 2nd argument: f[0] = 0x1
0e0 0000000000000000000000000000000000000000000000000000000000000002 # 2nd argument: f[1] = 0x2
100 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f[2] = 0x3
120 0000000000000000000000000000000000000000000000000000000000000004 # 3rd argument: t.length = 0x4
140 0000000000000000000000000000000000000000000000000000000000000004 # 3rd argument: t[0] = 0x4
160 0000000000000000000000000000000000000000000000000000000000000005 # 3rd argument: t[1] = 0x5
180 0000000000000000000000000000000000000000000000000000000000000006 # 3rd argument: t[2] = 0x6
1a0 0000000000000000000000000000000000000000000000000000000000000007 # 3rd argument: t[3] = 0x7
1c0 0000000000000000000000000000000000000000000000000000000000000004 # 4th argument: s1.length = 0x4
1e0 0000000000000000000000000000000000000000000000000000000000000008 # 4th argument: s1[0] = 0x8
200 0000000000000000000000000000000000000000000000000000000000000009 # 4th argument: s1[1] = 0x9
220 000000000000000000000000000000000000000000000000000000000000000a # 4th argument: s1[2] = 0xa
240 000000000000000000000000000000000000000000000000000000000000000b # 4th argument: s1[3] = 0xb
260 0000000000000000000000000000000000000000000000000000000000000004 # 5th argument: s2.length = 0x4
280 000000000000000000000000000000000000000000000000000000000000000c # 5th argument: s2[0] = 0xc
2a0 000000000000000000000000000000000000000000000000000000000000000d # 5th argument: s2[1] = 0xd
2c0 000000000000000000000000000000000000000000000000000000000000000e # 5th argument: s2[2] = 0xe
2e0 000000000000000000000000000000000000000000000000000000000000000f # 5th argument: s2[3] = 0xf
```



```
...
020 00000000000000000000000000000000000000000000000000000000000000a0 # 2nd argument offset: f starts at 0x0a0
...
0a0 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f.length = 0x3
0c0 0000000000000000000000000000000000000000000000000000000000000001 # 2nd argument: f[0] = 0x1
0e0 0000000000000000000000000000000000000000000000000000000000000002 # 2nd argument: f[1] = 0x2
100 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f[2] = 0x3
...
```



```
...
020 0000000000000000000000000000000000000000000000000000000000000300 # 2nd argument modified offset: f starts at 0x300
...
0a0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
0c0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
0e0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
100 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
...
300 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f.length = 0x3
320 0000000000000000000000000000000000000000000000000000000000000001 # 2nd argument: f[0] = 0x1
340 0000000000000000000000000000000000000000000000000000000000000002 # 2nd argument: f[1] = 0x2
360 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f[2] = 0x3
```



```
000 0000000000000000000000000000000000000000000000000000000000000003 # 1st argument: n = 0x3
020 0000000000000000000000000000000000000000000000000000000000000300 # 2nd argument modified offset: f starts at 0x300
040 0000000000000000000000000000000000000000000000000000000000000380 # 3rd argument modified offset: t starts at 0x380
060 0000000000000000000000000000000000000000000000000000000000000420 # 4th argument modified offset: s1 starts at 0x420
080 00000000000000000000000000000000000000000000000000000000000004c0 # 5th argument modified offset: s2 starts at 0x4c0
0a0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
0c0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
0e0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
100 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
120 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
140 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
160 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
180 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
1a0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
1c0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
1e0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
200 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
220 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
240 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
260 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
280 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
2a0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
2c0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
2e0 0000000000000000000000000000000000000000000000000000000000000000 # dummy value: 0x0
```



```
pragma solidity 0.8.0;

contract Test {
 uint256 public p = 21888242871839275222246405745257275088548364400416034343698204186575808495617;

 event Calc(bytes32 beta, bytes32 gamma);

 function test2(uint256 n, uint256[] memory f, uint256[] memory t, uint256[] memory s1, uint256[] memory s2) public {
 uint256 len = (12 + 4 * n) * 0x20;
 bytes32 beta; bytes32 gamma;
 assembly {
 let ptr := mload(0x40)
 calldatacopy(ptr, 4, len)
 mstore(add(ptr, len), 1)
 beta := keccak256(ptr, add(len, 32))
 mstore(add(ptr, len), 2)
 gamma := keccak256(ptr, add(len, 32))
 }
 emit Calc(beta, gamma);
 }
}
```



```
300 0000000000000000000000000000000000000000000000000000000000000003 # 2nd argument: f.length = 0x3
320 0e61d4879818050cd85482009c8ae484108a10bd8aca914af5cbe03d1746ecca # f[0] = -gamma % p
340 0000000000000000000000000000000000000000000000000000000000000000 # f[1] = 0x0
360 0000000000000000000000000000000000000000000000000000000000000000 # f[2] = 0x0
380 0000000000000000000000000000000000000000000000000000000000000004 # 3rd argument: t.length = 0x4
3a0 0000000000000000000000000000000000000000000000000000000000000001 # t[0] = 0x1
3c0 0000000000000000000000000000000000000000000000000000000000000002 # t[1] = 0x2
3e0 0000000000000000000000000000000000000000000000000000000000000003 # t[2] = 0x3
400 0000000000000000000000000000000000000000000000000000000000000004 # t[3] = 0x4
420 0000000000000000000000000000000000000000000000000000000000000004 # 4th argument: s1.length = 0x4
440 0000000000000000000000000000000000000000000000000000000000000001 # s1[0] = 0x1
460 0000000000000000000000000000000000000000000000000000000000000002 # s1[1] = 0x2
480 0000000000000000000000000000000000000000000000000000000000000003 # s1[2] = 0x3
4a0 0000000000000000000000000000000000000000000000000000000000000004 # s1[3] = 0x4
4c0 0000000000000000000000000000000000000000000000000000000000000004 # 5th argument: s2.length = 0x4
4e0 0000000000000000000000000000000000000000000000000000000000000004 # s2[0] = 0x4
500 0000000000000000000000000000000000000000000000000000000000000000 # s2[1] = 0x0
520 220ea990c9170f184ca10d4e43567db84935c5b2b82cd5fbfe69633867d82f12 # s2[2] = -gamma * (1 + beta) % p
540 0000000000000000000000000000000000000000000000000000000000000000 # s2[3] = 0x0
```



```
bytes32 beta; bytes32 gamma;
for(uint i = 0 ; i < 4 * n + 7 ; i++) {
 assembly {
 let ptr := mload(0x40)
 mstore(ptr, beta)
 mstore(add(ptr, 32), gamma)
 mstore(add(ptr, 64), mload(add(0x80, mul(i, 32))))
 mstore8(add(ptr, 96), 1)
 mstore8(add(ptr, 97), 2)
 beta := keccak256(ptr, 97)
 gamma := keccak256(ptr, 98)
 }
}
```



```
...
var temp4 = memory[0x40:0x60];
memory[temp4:temp4 + 0x20] = var0;
memory[temp4 + 0x20:temp4 + 0x20 + 0x20] = var1;
memory[temp4 + 0x40:temp4 + 0x40 + 0x20] = memory[var2 * 0x20 + 0x80:var2 * 0x20 + 0x80 + 0x20];
memory[temp4 + 0x60:temp4 + 0x60 + 0x01] = 0x01;
memory[temp4 + 0x61:temp4 + 0x61 + 0x01] = 0x02;
var0 = keccak256(memory[temp4:temp4 + 0x61]);
var1 = var0;
...
```



```
$ solc-select install 0.8.0 && solc-select use 0.8.0
$ solc --optimize Challenge.sol --asm
$ solc Challenge.sol --asm
```



```
import random
from typing import List

from web3 import Web3

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
n = 3

def H(data: bytes) -> int:
 return Web3.toInt(Web3.soliditySha3(["bytes"], [data]))

def isPowerOf2(n: int) -> bool:
 while n % 2 == 0:
 n = n / 2
 return n == 1

def sanity_check(
 n: int, f: List[int], t: List[int], s1: List[int], s2: List[int]
) -> bool:
 assert isPowerOf2(n + 1)
 assert all([len(f) == n, len(t) == n + 1, len(s1) == n + 1, len(s2) == n + 1])
 assert all(all([0 <= x <= p for x in data]) for data in [f, t, s1, s2])

def final_check(
 n: int,
 f: List[int],
 t: List[int],
 s1: List[int],
 s2: List[int],
 beta: int,
 gamma: int,
) -> bool:
 LHS = 1
 for i in range(n):
 LHS = LHS * (1 + beta) % p
 mul = (gamma * (1 + beta) + beta * t[i + 1] + t[i]) % p
 LHS = LHS * mul * (gamma + f[i]) % p
 RHS = 1
 for i in range(n):
 mul1 = (gamma * (1 + beta) + beta * (s1[i + 1]) + s1[i]) % p
 mul2 = (gamma * (1 + beta) + beta * (s2[i + 1]) + s2[i]) % p
 RHS = RHS * mul1 * mul2 % p
 assert LHS == RHS, "LHS != RHS"
 for i in range(n):
 if all([f[i] != elem for elem in t]):
 return
 assert False, "f and t so equal"

def check3(n: int, f: List[int], t: List[int], s1: List[int], s2: List[int]):
 beta = gamma = random.randint(1, 1 << 128)
 sanity_check(n, f, t, s1, s2)
 final_check(n, f, t, s1, s2, beta, gamma)
 assert s1[n] == s2[0]

def brute() -> None:
 for i in range(3**15):
 val = i
 arr = []
 for _ in range(15):
 arr.append(val % 3)
 val //= 3
 f, t, s1, s2 = arr[:3], arr[3:7], arr[7:11], arr[11:15]
 try:
 check3(n, f, t, s1, s2)
 except:
 continue
 else:
 return f, t, s1, s2
 assert False

if __name__ == "__main__":
 f, t, s1, s2 = brute()
 print(f"{f = }")
 print(f"{t = }")
 print(f"{s1 = }")
 print(f"{s2 = }")
```



```
$ nc 3.34.81.192 31337
1 - launch new instance
2 - kill instance
3 - get flag
action? 3
ticket please: kaistgonbestteam
codegate2022{1mpr0v1n6_pl00kup_15_h4rd_4f73r_4ll_bu7_47_l3457_w3_h4v3_2022/086_50_ju57_k33p_y0ur_h34r75_w4rm!_4l50_50l1d17y_0.8.3_15_h3r3_70_54v3_u5!}
```
