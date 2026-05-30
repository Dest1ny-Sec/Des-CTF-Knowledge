# Move CTF 2024 Writeup

> 原文: https://www.ctfiot.com/157167.html
> ID: 157167

在最近举办的Move CTF比赛中，ZAN团队和蚂蚁天穹实验室组成参赛队伍参赛，在有效的119个参赛队伍中排名第8。

MoveCTF 2024是由Move生态最早期贡献者MoveBit联合ChainFlag 、MoveFuns、OpenBuild主办，Sui基金会独家赞助和特别支持的CTF赛事。本次CTF主要涉及到密码学、ZK、DEX、交易分析等类型的题目，参赛者需通过与Sui链进行交互来完成赛题。

本次CTF共有8个Challenge，我们的参赛团队共解决/完成了7个Challenge。

dynamic_matrix_traversal

swap

subset

zk1

easygame

kitchen

zk2

 

题目详细信息请查看链接：

https://github.com/movebit/movectf2024-day1

https://github.com/movebit/movectf2024-day2

 

dynamic_matrix_traversal

fun init(ctx: &mut sui::
tx_context::
TxContext) { let record = Record { id: object::
new(ctx), count_1: 0, count_2: 0, count_3: 0, count_4: 0 };
 transfer::
share_object(record);}
fun up(m: u64, n: u64): u64 { let f: vector<vector> = vector::
empty(); let i: u64 = 0; while (i < m) { let row: vector = vector::
empty(); let j: u64 = 0; while (j < n) { if (j == 0 || i == 0) { vector::
push_back(&mut row, 1); } else { let f1 = *vector::
borrow(&f, i - 1); let j1 = *vector::
borrow(&row, j - 1); let val = *vector::
borrow(&f1, j) + j1; vector::
push_back(&mut row, val); }; j = j + 1; }; vector::
push_back(&mut f, row); i = i + 1; }; let fr = *vector::
borrow(&f, m - 1); let result = *vector::
borrow(&fr, n-1); result}
public entry fun execute(record: &mut Record, m: u64, n: u64) { if (record.count_1 == 0) { let result: u64 = up(m, n); assert!(result == TARGET_VALUE_1, ERROR_RESULT_1); record.count_1 = m; record.count_2 = n; } else if (record.count_3 == 0) { let result: u64 = up(m, n); assert!(result == TARGET_VALUE_2, ERROR_RESULT_2); record.count_3 = m; record.count_4 = n; }}
public entry fun get_flag(record: &Record, ctx: &mut TxContext) { assert!(record.count_1 < record.count_3, ERROR_PARAM_1); assert!(record.count_2 > record.count_4, ERROR_PARAM_2); event::
emit(Flag { user: tx_context::
sender(ctx), flag: true });}

swap

public fun swap_a_to_b<A,B>(vault: &mut Vault<A,B>, coina:
Coin<A>, ctx: &mut TxContext): Coin { let amount_out_B = coin::
value(&coina) * balance::
value(&vault.coin_b) / balance::
value(&vault.coin_a); coin::
put<A>(&mut vault.coin_a, coina); coin::
take(&mut vault.coin_b, amount_out_B, ctx)}

public entry fun attack(vault: &mut Vault<CTFA,CTFB>,coin_a :&mut Coin<CTFA>,ctx: &mut TxContext) { let sender = tx_context::
sender(ctx); let (loan_a,loan_b,res) = swap::
vault::
flash(vault,99,false,ctx); let swap_coin = coin::
split(coin_a,1,ctx); let swap_b = swap::
vault::
swap_a_to_b(vault,swap_coin,ctx); transfer::
public_transfer(swap_b,sender); swap::
vault::
repay_flash(vault,loan_a,loan_b,res); (loan_a,loan_b,res) = swap::
vault::
flash(vault,101,false,ctx); swap::
vault::
get_flag(vault,ctx); swap::
vault::
repay_flash(vault,loan_a,loan_b,res);}

Subset

module solve_subset::
ans { use sui::
tx_context; use subset::
subset_sum;
 public entry fun solveIt(ctx: &mut tx_context::
TxContext) { let status: subset_sum::
Status = subset_sum::
get_status(ctx); let ans1: vector = vector [1, 0, 0, 1, 1]; let ans2: vector = vector [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]; let ans3: vector = vector [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]; subset_sum::
solve_subset1(ans1, &mut status); subset_sum::
solve_subset2(ans2, &mut status); subset_sum::
solve_subset3(ans3, &mut status); subset_sum::
get_flag(& status, ctx); }}

zk1

use ark_bn254::
Bn254;use ark_circom::
CircomBuilder;use ark_circom::
CircomConfig;use ark_groth16::{Groth16, ProvingKey, VerifyingKey};use ark_snark::
SNARK;use std::
str::
FromStr;use num_bigint::
BigInt;use ark_serialize::{CanonicalDeserialize, CanonicalSerialize};use rand::
rngs::
OsRng;
fn main() { // Load the WASM and R1CS for witness and proof generation let pk_hex_str = "YOUR PROVING KEY HERE";
 let pk_bytes = hex::
decode(pk_hex_str).expect("Invalid hex string"); let pk = ProvingKey::::
deserialize_compressed(&*pk_bytes).unwrap();
 let mut rng = OsRng;

 let a = BigInt::
from_str("8333598376919903303").unwrap(); let b = BigInt::
from_str("7027838896893106737374484418882753039002846643017920494481").unwrap();
 let cfg = CircomConfig::::
new("/Users/chris/CLionProjects/rust-example/zk2.wasm", "/Users/chris/CLionProjects/rust-example/zk2.r1cs").unwrap(); let mut builder = CircomBuilder::
new(cfg);
 builder.push_input("a", a); builder.push_input("b", b);
 let circom = builder.setup();

 let circom = builder.build().unwrap();
 let inputs = circom.get_public_inputs().unwrap();
 let proof = Groth16::::
create_proof_with_reduction_no_zk(circom, &pk).unwrap();
 let vk_hex_str = "YOUR VERIFY KEY HERE";
 let vk_bytes = hex::
decode(vk_hex_str).unwrap();
 let vk = VerifyingKey::::
deserialize_compressed(&*vk_bytes).unwrap();
 let pvk = Groth16::::
process_vk(&vk).unwrap();
 let verified = Groth16::::
verify_with_processed_vk(&pvk, &inputs, &proof).unwrap(); assert!(verified);
 let mut proof_inputs_bytes = Vec::
new(); let a = inputs.get(0).unwrap(); println!("{:?}", a);
 a.serialize_compressed(&mut proof_inputs_bytes).unwrap(); let mut proof_points_bytes = Vec::
new(); proof.a.serialize_compressed(&mut proof_points_bytes).unwrap(); proof.b.serialize_compressed(&mut proof_points_bytes).unwrap(); proof.c.serialize_compressed(&mut proof_points_bytes).unwrap();
 println!("{:?}", proof_inputs_bytes); println!("{:?}", proof_points_bytes);}

sui client call --function verify_proof --package PACKAGE-ID --module zk1 --args '[53, 113, 11, 212, 246, 19, 69, 100, 184, 3, 99, 76, 115, 20, 27, 102, 3, 144, 180, 71, 239, 104, 222, 9, 200, 32, 77, 55, 122, 61, 179, 32]' '[12, 91, 93, 139, 10, 42, 115, 162, 46, 162, 34, 20, 163, 170, 217, 78, 31, 191, 195, 216, 118, 61, 175, 108, 198, 29, 9, 161, 36, 23, 80, 38, 226, 31, 91, 215, 25, 63, 133, 240, 37, 206, 33, 198, 148, 161, 149, 56, 208, 233, 71, 150, 177, 78, 35, 53, 82, 2, 194, 50, 154, 187, 42, 19, 8, 107, 96, 32, 177, 41, 57, 26, 118, 177, 163, 36, 90, 118, 96, 100, 226, 178, 156, 144, 194, 180, 90, 182, 197, 66, 158, 150, 207, 114, 55, 172, 69, 215, 205, 117, 14, 63, 86, 84, 147, 25, 80, 225, 44, 4, 154, 31, 231, 156, 149, 18, 207, 36, 9, 106, 183, 165, 74, 202, 81, 149, 56, 6]' --gas-budget 10000000

easygame

let v = vector::
empty();vector::
push_back(&mut v, *vector::
borrow(houses, 0));if (n>1){ vector::
push_back(&mut v, math::
max(*vector::
borrow(houses, 0), *vector::
borrow(houses, 1)));};let i = 2;while (i < n) { let dp_i_1 = *vector::
borrow(&v, i - 1); let dp_i_2_plus_house = *vector::
borrow(&v, i - 2) + *vector::
borrow(houses, i); vector::
push_back(&mut v, math::
max(dp_i_1, dp_i_2_plus_house)); i = i + 1;};*vector::
borrow(&v, n - 1)

kitchen

let v1 = vector::
empty<Olive_oil>();let v2 = vector::
empty<Yeast>();let v3 = vector::
empty<Flour>();let v4 = vector::
empty<Salt>();vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xa515));vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xa6b8));vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xc9f8));vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xbb46));vector::
push_back(&mut v2, kitchen::
get_Yeast(0xbd00));vector::
push_back(&mut v2, kitchen::
get_Yeast(0x999d));vector::
push_back(&mut v2, kitchen::
get_Yeast(0xb77e));vector::
push_back(&mut v3, kitchen::
get_Flour(0xd78a));vector::
push_back(&mut v3, kitchen::
get_Flour(0xfa84));vector::
push_back(&mut v3, kitchen::
get_Flour(0xb8f2));vector::
push_back(&mut v4, kitchen::
get_Salt(0xf1c5));vector::
push_back(&mut v4, kitchen::
get_Salt(0xe122));
let status = kitchen::
kitchen::
get_status(ctx);
kitchen::
cook(v1,v2,v3,v4,&mut status);
let answer = vector[0x06,0xd9,0xb9,0x54,0xeb,0x68,0x92,0xf7,0xc5,0xec,0xa1,0x84,0xd0,0x04,0x00,0xbd,0x81,0xfc,0x9d,0x99,0x7e,0xb7,0x05,0xc7,0xdc,0x7a,0xcc,0x19,0x8f,0xb1,0x96,0x6d,0x8a,0x03,0x01,0x8b,0xc5,0xf1,0xec,0xc6];
kitchen::
recook(answer,&mut status);
kitchen::
get_flag(&status,ctx);

zk2

x = 995203441582195749578291179787384436505546430278305826713579947235728471134delta = 5472060717959818805561601436314318772137091100104008585924551046643952123905
or
x = 5299619240641551281634865583518297030282874472190772894086521144482721001553delta = 16950150798460657717958625567821834550301663161624707787222815936182638968203

public entry fun faucet(protocol: &mut Protocol, ctx: &mut tx_context::
TxContext) { table::
add(&mut protocol.balance, tx_context::
sender(ctx), 60_000);}
public entry fun withdraw(amount: u64, public_inputs_bytes: vector, proof_points_bytes: vector, protocol: &mut Protocol, ctx: &mut tx_context::
TxContext) { verify_proof(public_inputs_bytes, proof_points_bytes); assert!(*table::
borrow(&protocol.balance, tx_context::
sender(ctx)) >= amount, 0); table::
add(&mut protocol.proof_talbe, keccak256(&proof_points_bytes), true); let coin = coin::
split(&mut protocol.vault, amount, ctx); transfer::
public_transfer(coin, tx_context::
sender(ctx));}

END

关于我们 About Us

ZAN是蚂蚁数科旗下新科技品牌。依托AntChain Open Labs的TrustBase开源开放技术体系，拥有Web3领域独特的优势和创新能力，为Web3社区提供可靠、高性价比的区块链应用开发技术产品和服务。

 

凭借AntChain Open Labs的技术支持，ZAN为企业和开发者提供了全面的技术产品和服务，其中包括智能合约审计（ZAN Smart Contract Review）、身份验证eKYC（ZAN Identity）、交易风控技术（ZAN Know Your Transaction）以及节点服务（ZAN Node Service）等。

 

通过ZAN的一站式解决方案，用户可以享受到全方位的Web3技术支持。

ZAN Website：https://zan.top/home

联系我们

CONTACT US

戳“阅读原文” 获取更多联系方式 !


```
fun init(ctx: &mut sui::
tx_context::
TxContext) { let record = Record { id: object::
new(ctx), count_1: 0, count_2: 0, count_3: 0, count_4: 0 };
 transfer::
share_object(record);}
fun up(m: u64, n: u64): u64 { let f: vector<vector> = vector::
empty(); let i: u64 = 0; while (i < m) { let row: vector = vector::
empty(); let j: u64 = 0; while (j < n) { if (j == 0 || i == 0) { vector::
push_back(&mut row, 1); } else { let f1 = *vector::
borrow(&f, i - 1); let j1 = *vector::
borrow(&row, j - 1); let val = *vector::
borrow(&f1, j) + j1; vector::
push_back(&mut row, val); }; j = j + 1; }; vector::
push_back(&mut f, row); i = i + 1; }; let fr = *vector::
borrow(&f, m - 1); let result = *vector::
borrow(&fr, n-1); result}
public entry fun execute(record: &mut Record, m: u64, n: u64) { if (record.count_1 == 0) { let result: u64 = up(m, n); assert!(result == TARGET_VALUE_1, ERROR_RESULT_1); record.count_1 = m; record.count_2 = n; } else if (record.count_3 == 0) { let result: u64 = up(m, n); assert!(result == TARGET_VALUE_2, ERROR_RESULT_2); record.count_3 = m; record.count_4 = n; }}
public entry fun get_flag(record: &Record, ctx: &mut TxContext) { assert!(record.count_1 < record.count_3, ERROR_PARAM_1); assert!(record.count_2 > record.count_4, ERROR_PARAM_2); event::
emit(Flag { user: tx_context::
sender(ctx), flag: true });}
public fun swap_a_to_b<A,B>(vault: &mut Vault<A,B>, coina:
Coin<A>, ctx: &mut TxContext): Coin { let amount_out_B = coin::
value(&coina) * balance::
value(&vault.coin_b) / balance::
value(&vault.coin_a); coin::
put<A>(&mut vault.coin_a, coina); coin::
take(&mut vault.coin_b, amount_out_B, ctx)}
public entry fun attack(vault: &mut Vault<CTFA,CTFB>,coin_a :&mut Coin<CTFA>,ctx: &mut TxContext) { let sender = tx_context::
sender(ctx); let (loan_a,loan_b,res) = swap::
vault::
flash(vault,99,false,ctx); let swap_coin = coin::
split(coin_a,1,ctx); let swap_b = swap::
vault::
swap_a_to_b(vault,swap_coin,ctx); transfer::
public_transfer(swap_b,sender); swap::
vault::
repay_flash(vault,loan_a,loan_b,res); (loan_a,loan_b,res) = swap::
vault::
flash(vault,101,false,ctx); swap::
vault::
get_flag(vault,ctx); swap::
vault::
repay_flash(vault,loan_a,loan_b,res);}
module solve_subset::
ans { use sui::
tx_context; use subset::
subset_sum;
 public entry fun solveIt(ctx: &mut tx_context::
TxContext) { let status: subset_sum::
Status = subset_sum::
get_status(ctx); let ans1: vector = vector [1, 0, 0, 1, 1]; let ans2: vector = vector [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]; let ans3: vector = vector [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]; subset_sum::
solve_subset1(ans1, &mut status); subset_sum::
solve_subset2(ans2, &mut status); subset_sum::
solve_subset3(ans3, &mut status); subset_sum::
get_flag(& status, ctx); }}
use ark_bn254::
Bn254;use ark_circom::
CircomBuilder;use ark_circom::
CircomConfig;use ark_groth16::{Groth16, ProvingKey, VerifyingKey};use ark_snark::
SNARK;use std::
str::
FromStr;use num_bigint::
BigInt;use ark_serialize::{CanonicalDeserialize, CanonicalSerialize};use rand::
rngs::
OsRng;
fn main() { // Load the WASM and R1CS for witness and proof generation let pk_hex_str = "YOUR PROVING KEY HERE";
 let pk_bytes = hex::
decode(pk_hex_str).expect("Invalid hex string"); let pk = ProvingKey::::
deserialize_compressed(&*pk_bytes).unwrap();
 let mut rng = OsRng;

 let a = BigInt::
from_str("8333598376919903303").unwrap(); let b = BigInt::
from_str("7027838896893106737374484418882753039002846643017920494481").unwrap();
 let cfg = CircomConfig::::
new("/Users/chris/CLionProjects/rust-example/zk2.wasm", "/Users/chris/CLionProjects/rust-example/zk2.r1cs").unwrap(); let mut builder = CircomBuilder::
new(cfg);
 builder.push_input("a", a); builder.push_input("b", b);
 let circom = builder.setup();

 let circom = builder.build().unwrap();
 let inputs = circom.get_public_inputs().unwrap();
 let proof = Groth16::::
create_proof_with_reduction_no_zk(circom, &pk).unwrap();
 let vk_hex_str = "YOUR VERIFY KEY HERE";
 let vk_bytes = hex::
decode(vk_hex_str).unwrap();
 let vk = VerifyingKey::::
deserialize_compressed(&*vk_bytes).unwrap();
 let pvk = Groth16::::
process_vk(&vk).unwrap();
 let verified = Groth16::::
verify_with_processed_vk(&pvk, &inputs, &proof).unwrap(); assert!(verified);
 let mut proof_inputs_bytes = Vec::
new(); let a = inputs.get(0).unwrap(); println!("{:?}", a);
 a.serialize_compressed(&mut proof_inputs_bytes).unwrap(); let mut proof_points_bytes = Vec::
new(); proof.a.serialize_compressed(&mut proof_points_bytes).unwrap(); proof.b.serialize_compressed(&mut proof_points_bytes).unwrap(); proof.c.serialize_compressed(&mut proof_points_bytes).unwrap();
 println!("{:?}", proof_inputs_bytes); println!("{:?}", proof_points_bytes);}
sui client call --function verify_proof --package PACKAGE-ID --module zk1 --args '[53, 113, 11, 212, 246, 19, 69, 100, 184, 3, 99, 76, 115, 20, 27, 102, 3, 144, 180, 71, 239, 104, 222, 9, 200, 32, 77, 55, 122, 61, 179, 32]' '[12, 91, 93, 139, 10, 42, 115, 162, 46, 162, 34, 20, 163, 170, 217, 78, 31, 191, 195, 216, 118, 61, 175, 108, 198, 29, 9, 161, 36, 23, 80, 38, 226, 31, 91, 215, 25, 63, 133, 240, 37, 206, 33, 198, 148, 161, 149, 56, 208, 233, 71, 150, 177, 78, 35, 53, 82, 2, 194, 50, 154, 187, 42, 19, 8, 107, 96, 32, 177, 41, 57, 26, 118, 177, 163, 36, 90, 118, 96, 100, 226, 178, 156, 144, 194, 180, 90, 182, 197, 66, 158, 150, 207, 114, 55, 172, 69, 215, 205, 117, 14, 63, 86, 84, 147, 25, 80, 225, 44, 4, 154, 31, 231, 156, 149, 18, 207, 36, 9, 106, 183, 165, 74, 202, 81, 149, 56, 6]' --gas-budget 10000000
let v = vector::
empty();vector::
push_back(&mut v, *vector::
borrow(houses, 0));if (n>1){ vector::
push_back(&mut v, math::
max(*vector::
borrow(houses, 0), *vector::
borrow(houses, 1)));};let i = 2;while (i < n) { let dp_i_1 = *vector::
borrow(&v, i - 1); let dp_i_2_plus_house = *vector::
borrow(&v, i - 2) + *vector::
borrow(houses, i); vector::
push_back(&mut v, math::
max(dp_i_1, dp_i_2_plus_house)); i = i + 1;};*vector::
borrow(&v, n - 1)
let v1 = vector::
empty<Olive_oil>();let v2 = vector::
empty<Yeast>();let v3 = vector::
empty<Flour>();let v4 = vector::
empty<Salt>();vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xa515));vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xa6b8));vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xc9f8));vector::
push_back(&mut v1, kitchen::
get_Olive_oil(0xbb46));vector::
push_back(&mut v2, kitchen::
get_Yeast(0xbd00));vector::
push_back(&mut v2, kitchen::
get_Yeast(0x999d));vector::
push_back(&mut v2, kitchen::
get_Yeast(0xb77e));vector::
push_back(&mut v3, kitchen::
get_Flour(0xd78a));vector::
push_back(&mut v3, kitchen::
get_Flour(0xfa84));vector::
push_back(&mut v3, kitchen::
get_Flour(0xb8f2));vector::
push_back(&mut v4, kitchen::
get_Salt(0xf1c5));vector::
push_back(&mut v4, kitchen::
get_Salt(0xe122));
let status = kitchen::
kitchen::
get_status(ctx);
kitchen::
cook(v1,v2,v3,v4,&mut status);
let answer = vector[0x06,0xd9,0xb9,0x54,0xeb,0x68,0x92,0xf7,0xc5,0xec,0xa1,0x84,0xd0,0x04,0x00,0xbd,0x81,0xfc,0x9d,0x99,0x7e,0xb7,0x05,0xc7,0xdc,0x7a,0xcc,0x19,0x8f,0xb1,0x96,0x6d,0x8a,0x03,0x01,0x8b,0xc5,0xf1,0xec,0xc6];
kitchen::
recook(answer,&mut status);
kitchen::
get_flag(&status,ctx);
x = 995203441582195749578291179787384436505546430278305826713579947235728471134delta = 5472060717959818805561601436314318772137091100104008585924551046643952123905
or
x = 5299619240641551281634865583518297030282874472190772894086521144482721001553delta = 16950150798460657717958625567821834550301663161624707787222815936182638968203
public entry fun faucet(protocol: &mut Protocol, ctx: &mut tx_context::
TxContext) { table::
add(&mut protocol.balance, tx_context::
sender(ctx), 60_000);}
public entry fun withdraw(amount: u64, public_inputs_bytes: vector, proof_points_bytes: vector, protocol: &mut Protocol, ctx: &mut tx_context::
TxContext) { verify_proof(public_inputs_bytes, proof_points_bytes); assert!(*table::
borrow(&protocol.balance, tx_context::
sender(ctx)) >= amount, 0); table::
add(&mut protocol.proof_talbe, keccak256(&proof_points_bytes), true); let coin = coin::
split(&mut protocol.vault, amount, ctx); transfer::
public_transfer(coin, tx_context::
sender(ctx));}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/1-1705484244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1705484244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1705484244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/8-1705484244.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/7-1705484245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/0-1705484245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/1-1705484245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/3-1705484246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/6-1705484246.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/01/2-1705484246.png)