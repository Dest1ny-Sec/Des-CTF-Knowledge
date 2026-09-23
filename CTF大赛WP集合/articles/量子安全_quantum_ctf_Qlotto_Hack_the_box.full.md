---
title: 量子安全 quantum ctf Qlotto Hack the box
contest: Quantum CTF / Hack The Box QLotto
year: 2025
difficulty: hard
vuln_type: misc_math
tags:
- qiskit
- quantum-circuit
- Aer-simulator
- qasm-simulator
- QuantumCircuit
- H-S-T-Z-gates
- RXX-RYY-RZZ
- binomialtest
- entropy-validation
- quantum-lotto
attack_chain:
- 代码分析:server.py使用qiskit+QuantumCircuit(2qubit)+Aer qasm_simulator后端
- generate_circuit(instructions):解析指令字符串"gate:params;..."格式
- 1-qubit gates:H(h)+S(s)+T(t)+Z(z)
- 2-qubit gates:RXX/RYY/RZZ(2 params:phase+qubits)+CX/CZ
- validate_entropy:测0比特位100000 shots+binomtest+two-sided pvalue<0.01拒绝
- extract_numbers:从memory中按6位一组(2bit lottery+4bit testing)
- lotto_number = int(bits, 2) % 42 + 1
- testing_number = int(testing_bits, 2) % 42 + 1
- run_lotto(instructions, shots=36)
- main:Place quantum moves+Place six bets on the table
- 验证:lotto_numbers==guess_numbers得flag
- 关键:Lotto bits = ~Testing bits(按位取反)
- 公式:Lotto = ((21 - (Test - 1)) % 42) + 1
- Raw_Lotto = 63 - Raw_Test
- Final_Lotto = (Raw_Lotto % 42) + 1
- 需要:让test和lotto不同,但guess==lotto
key_payload: Lotto = ((21 - (Test - 1)) % 42) + 1
one_liner: 量子安全Qlotto CTF(Hack the box)量子电路+模拟器+6位bit映射+42取模,需理解Lotto/Test bit按位取反关系,用量子电路让test和lotto不同但guess==lotto得flag。
lesson: 量子电路题先理解验证逻辑(entropy validation + bit extraction + 42取模),再设计电路让test和lotto不同但guess能匹配lotto;按位取反关系是常见模式。
quality: high
full_path: 量子安全_quantum_ctf_Qlotto_Hack_the_box.full.md
meta_path: 量子安全_quantum_ctf_Qlotto_Hack_the_box.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 量子安全 quantum ctf Qlotto Hack the box。量子安全Qlotto CTF(Hack the box)量子电路+模拟器+6位bit映射+42取模,需理解Lotto/Test bit按位取反关系,用量子电路让test和lotto不同但guess==lotto得flag。。关键路径：代码分析:server.py使用qiskit+QuantumCircuit(2qubi...
category: crypto
subcategory: math
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/297316.html
reasoning_chain:
- server.py 用 qiskit + QuantumCircuit(2qubit) + Aer qasm_simulator 后端 → 触发点：量子电路题
- generate_circuit：解析 'gate:params;...' 指令格式 → 假设：用户控指令
- '1-qubit gates: H(h) + S(s) + T(t) + Z(z)，2-qubit gates: RXX/RYY/RZZ (2 params: phase+qubits) + CX/CZ'
- validate_entropy：测 0 比特位 100000 shots + binomtest + two-sided pvalue<0.01 拒绝 → 假设：电路不能太确定
- extract_numbers：从 memory 中按 6 位一组（2bit lottery + 4bit testing）→ lotto_number = int(bits, 2) % 42 + 1
- testing_number = int(testing_bits, 2) % 42 + 1 → run_lotto(instructions, shots=36)
- 验证：lotto_numbers == guess_numbers 得 flag
- 关键洞察：Lotto bits = ~Testing bits（按位取反）→ 公式 Lotto = ((21 - (Test - 1)) % 42) + 1
- Raw_Lotto = 63 - Raw_Test → Final_Lotto = (Raw_Lotto % 42) + 1
- 设计电路：让 test 和 lotto 不同，但 guess == lotto → flag
failed_attempts:
- 试图只画 H 门让所有 qubit 50/50 → 失败：entropy validation 卡死
- 直接把 test 和 lotto 设同电路 → 失败：题目要 test != lotto
- 枚举所有 RXX/RYY/RZZ 参数 → 失败：参数空间太大
key_observations:
- 量子电路题先理解验证逻辑（entropy + bit extraction + 取模），再设计电路
- 按位取反关系是 CTF 加密题的常见模式（XOR 0xFF/63）
- binomial test 拒绝 100% 确定性输出，电路必须保留概率
- Aer qasm_simulator 是 Qiskit 标准后端，shots 控制采样次数
prerequisites:
- Qiskit QuantumCircuit API（H/S/T/Z/RXX/RYY/RZZ/CX/CZ）
- Aer qasm_simulator 后端与 memory 提取
- binomtest 与 two-sided p 值假设检验
- 量子比特叠加态与测量概率
---
# 量子安全 quantum ctf Qlotto Hack the box

> 原文: https://www.ctfiot.com/297316.html
> ID: 297316

01

代码分析server.py

from qiskit import QuantumCircuit, ClassicalRegister, transpile
from scipy.stats import binomtest
from qiskit_aer import Aer
from math import pi

#from my_secret import JACKPOT

class QuantumLotto:
    def __init__(self):
        self.backend = Aer.get_backend("qasm_simulator")

def degrees_to_radians(self, degrees: int):
        return degrees * (pi / 180)

    def generate_circuit(self, instructions: str):
        circuit = QuantumCircuit(2)

        circuit.h(0)

        instructions = instructions.split(";")
        for instr in instructions:
            parts = instr.split(":")

            if len(parts) != 2:
                print(f"[Dealer] The move '{instr}' isn't recognized at this table. Expected format: <gate>:")
                return None

            gate, params = parts

            try:
                params = [ int(p) for p in params.split(",") ]
            
except:
                print("[Dealer] Only number cards are allowed at this table.")
                return None

if len(params) == 1:
                if any(n >= circuit.num_qubits for n in params):
                    print(f"[Dealer] Card numbers must be less than {circuit.num_qubits}")
                    return None

                if   gate == "H": circuit.h(params[0])
                elif gate == "S": circuit.s(params[0])
                elif gate == "T": circuit.t(params[0])
                elif gate == "Z": circuit.z(params[0])
                else:
                    print(f"[Dealer] The 1-qubit move '{gate}' isn't recognized at this table.")
                    return None
                    
                            …………
                            
                                phase = self.degrees_to_radians(params[0])

                                if   gate == "RXX": circuit.rxx(phase, params[1], params[2])
                                elif gate == "RYY": circuit.ryy(phase, params[1], params[2])
                                elif gate == "RZZ": circuit.rzz(phase, params[1], params[2])
                                else:
                                    print(f"[Dealer] The 3-qubit move '{gate}' isn't recognized at this table.")
                                    return None

if any(p == 0 for p in params):
                print("[Dealer] Hey, don't tamper with the house card — that's forbidden.")
                return None

if params[1] == params[2]:
                    print("[Dealer] Control and target cards must be different.")
                    return None

def validate_entropy(self, base_circuit, shots = 100_000):
        circuit = base_circuit.copy()

        circuit.add_register(ClassicalRegister(1))

        circuit.measure(0, 0)

        compiled = transpile(circuit, self.backend)
        results = self.backend.run(compiled, shots = shots).result()
        counts = results.get_counts()
       
        binomial_test = binomtest(counts.get('0', 0), n = shots, p = 0.5, alternative = 'two-sided')

        if binomial_test.pvalue < 0.01:
            return False

        return True

def extract_numbers(self, memory):
        print(memory)
        lotto_numbers   = []
        testing_numbers = []

        for i in range(0, len(memory), 6):
            bits = memory[i : i + 6]

            lotto_number   = ""
            testing_number = ""

            for testing_bit, lotto_bit in bits:
                lotto_number   += str(lotto_bit)
                testing_number += str(testing_bit)
            lotto_number   = int(lotto_number,   2) % 42 + 1
            testing_number = int(testing_number, 2) % 42 + 1
            
            lotto_numbers.append(lotto_number)
            testing_numbers.append(testing_number)

        return lotto_numbers, testing_numbers

def run_lotto(self, instructions, shots = 36):
        circuit = self.generate_circuit(instructions)

        if not circuit:
            return None

        if not self.validate_entropy(circuit):
            print("[Dealer] The draw fizzles... not enough quantum energy in your play.")
            return None

        circuit.measure_all()
        print(circuit)

        compiled = transpile(circuit, self.backend)
        results = self.backend.run(compiled, shots = shots, memory = True).result()

        return self.extract_numbers(results.get_memory())

def main():
    print("""
        ╔═════════════════════╗
        ║ ⚛ Welcome to the QLotto table ⚛  ║
        ╠═════════════════════╣
        ║ Minimum bet :  100,000 credits   ║
        ║ Provider    :  Qubitrix™     ║
        ╚═════════════════════╝
    """)

    lotto = QuantumLotto()

    instructions = input("[Dealer] Place your quantum moves : ")

    numbers = lotto.run_lotto(instructions)

    if not numbers:
        return

    lotto_numbers, testing_numbers = numbers

    if lotto_numbers == testing_numbers:
        print("[Dealer] Trying to mirror the house's numbers, are we?")
        return

    print(f"[Dealer] Your draws are: {testing_numbers}")

    guess_numbers = input("[Dealer] Place your six bets on the table : ")

    try:
        guess_numbers = [ int(n) for n in guess_numbers.split(",") ]
    
except:
        print("[Dealer] Your wagers must be integers.")
        return

    if len(guess_numbers) != 6 or any(n < 1 or n > 42 for n in guess_numbers):
        print("[Dealer] Place six bets on the table, numbered 1 through 42.")
        return

    if guess_numbers == lotto_numbers:
        print("The table erupts in chaos — you've cracked the QLotto!")
        print(f"[Dealer] Your jackpot:")
    else:
        print(f"[Dealer] Oh, that's a shame, the numbers were {lotto_numbers}")

02

量子计算相关知识

03

解题

def solve_qlotto(testing_numbers):
    """
    根据 Testing Numbers 计算 Lotto Numbers。
    原理：Lotto bits = ~Testing bits (按位取反)
    推导公式：Lotto = ((21 - (Test - 1)) % 42) + 1
    """
    lotto_numbers = []
    for t in testing_numbers:
        # 公式推导：
        # Raw_Lotto = 63 - Raw_Test
        # Final_Lotto = (Raw_Lotto % 42) + 1
        # Final_Lotto = ((63 - Raw_Test) % 42) + 1
        #             = ((21 - Raw_Test) % 42) + 1
        # Raw_Test 与 (t-1) 同余 42，所以可以直接替换
        val = ((21 - (t - 1)) % 42) + 1
        lotto_numbers.append(val)
    return lotto_numbers

if __name__ == "__main__":
    print("--- QLotto Solver ---")
    print("请先在服务器输入量子指令: H:0;RXX:90,0,1;H:0;Z:0;H:0")
   
    try:
        user_input = input("请输入服务器返回的 draws 数组 (例如 25,21,10...): ")
        # 处理可能的方括号
        clean_input = user_input.replace('[', '').replace(']', '')
        if not clean_input.strip():
            print("输入为空")
            exit()
           
        testing_nums = [int(x.strip()) for x in clean_input.split(',')]
       
        if len(testing_nums) != 6:
            print(f"警告: 输入了 {len(testing_nums)} 个数字，通常需要 6 个。")

        winning_nums = solve_qlotto(testing_nums)
       
        print("n[+] 计算出的必胜数字 (复制粘贴回服务器):")
        print(",".join(map(str, winning_nums)))
       
    
except ValueError:
        print("[-] 输入格式错误，请确保输入的是逗号分隔的数字。")

看雪ID：枫林路大砍刀

https://bbs.kanxue.com/user-home-1008959.htm

*本文为看雪论坛优秀文章，由 枫林路大砍刀 原创，转载请注明来自看雪社区

# 往期推荐

从ANGR-CTF项目入手ANGR和符号执行技术

AI时代-逆向工作者该如何用好这一利器

EXIF解析缓冲区溢出漏洞分析与利用

从C到Pwn：栈溢出漏洞利用实战入门

Android-ARM64的VMP分析和还原

球分享

球点赞

球在看

点击阅读原文查看更多


```
from qiskit import QuantumCircuit, ClassicalRegister, transpile
from scipy.stats import binomtest
from qiskit_aer import Aer
from math import pi

    #from my_secret import JACKPOT

class QuantumLotto:
    def __init__(self):
        self.backend = Aer.get_backend("qasm_simulator")
def degrees_to_radians(self, degrees: int):
        return degrees * (pi / 180)

    def generate_circuit(self, instructions: str):
        circuit = QuantumCircuit(2)

        circuit.h(0)

        instructions = instructions.split(";")
        for instr in instructions:
            parts = instr.split(":")

            if len(parts) != 2:
                print(f"[Dealer] The move '{instr}' isn't recognized at this table. Expected format: <gate>:")
                return None

            gate, params = parts

            try:
                params = [ int(p) for p in params.split(",") ]
            
except:
                print("[Dealer] Only number cards are allowed at this table.")
                return None
if len(params) == 1:
                if any(n >= circuit.num_qubits for n in params):
                    print(f"[Dealer] Card numbers must be less than {circuit.num_qubits}")
                    return None

                if   gate == "H": circuit.h(params[0])
                elif gate == "S": circuit.s(params[0])
                elif gate == "T": circuit.t(params[0])
                elif gate == "Z": circuit.z(params[0])
                else:
                    print(f"[Dealer] The 1-qubit move '{gate}' isn't recognized at this table.")
                    return None
                    
                            …………
                            
                                phase = self.degrees_to_radians(params[0])

                                if   gate == "RXX": circuit.rxx(phase, params[1], params[2])
                                elif gate == "RYY": circuit.ryy(phase, params[1], params[2])
                                elif gate == "RZZ": circuit.rzz(phase, params[1], params[2])
                                else:
                                    print(f"[Dealer] The 3-qubit move '{gate}' isn't recognized at this table.")
                                    return None
if any(p == 0 for p in params):
                print("[Dealer] Hey, don't tamper with the house card — that's forbidden.")
                return None
if params[1] == params[2]:
                    print("[Dealer] Control and target cards must be different.")
                    return None
def validate_entropy(self, base_circuit, shots = 100_000):
        circuit = base_circuit.copy()

        circuit.add_register(ClassicalRegister(1))

        circuit.measure(0, 0)

        compiled = transpile(circuit, self.backend)
        results = self.backend.run(compiled, shots = shots).result()
        counts = results.get_counts()
       
        binomial_test = binomtest(counts.get('0', 0), n = shots, p = 0.5, alternative = 'two-sided')

        if binomial_test.pvalue < 0.01:
            return False

        return True
def extract_numbers(self, memory):
        print(memory)
        lotto_numbers   = []
        testing_numbers = []

        for i in range(0, len(memory), 6):
            bits = memory[i : i + 6]

            lotto_number   = ""
            testing_number = ""

            for testing_bit, lotto_bit in bits:
                lotto_number   += str(lotto_bit)
                testing_number += str(testing_bit)
            lotto_number   = int(lotto_number,   2) % 42 + 1
            testing_number = int(testing_number, 2) % 42 + 1
            
            lotto_numbers.append(lotto_number)
            testing_numbers.append(testing_number)

        return lotto_numbers, testing_numbers
def run_lotto(self, instructions, shots = 36):
        circuit = self.generate_circuit(instructions)

        if not circuit:
            return None

        if not self.validate_entropy(circuit):
            print("[Dealer] The draw fizzles... not enough quantum energy in your play.")
            return None

        circuit.measure_all()
        print(circuit)

        compiled = transpile(circuit, self.backend)
        results = self.backend.run(compiled, shots = shots, memory = True).result()

        return self.extract_numbers(results.get_memory())
def main():
    print("""
        ╔═════════════════════╗
        ║ ⚛ Welcome to the QLotto table ⚛  ║
        ╠═════════════════════╣
        ║ Minimum bet :  100,000 credits   ║
        ║ Provider    :  Qubitrix™     ║
        ╚═════════════════════╝
    """)

    lotto = QuantumLotto()

    instructions = input("[Dealer] Place your quantum moves : ")

    numbers = lotto.run_lotto(instructions)

    if not numbers:
        return

    lotto_numbers, testing_numbers = numbers

    if lotto_numbers == testing_numbers:
        print("[Dealer] Trying to mirror the house's numbers, are we?")
        return

    print(f"[Dealer] Your draws are: {testing_numbers}")

    guess_numbers = input("[Dealer] Place your six bets on the table : ")

    try:
        guess_numbers = [ int(n) for n in guess_numbers.split(",") ]
    
except:
        print("[Dealer] Your wagers must be integers.")
        return

    if len(guess_numbers) != 6 or any(n < 1 or n > 42 for n in guess_numbers):
        print("[Dealer] Place six bets on the table, numbered 1 through 42.")
        return

    if guess_numbers == lotto_numbers:
        print("The table erupts in chaos — you've cracked the QLotto!")
        print(f"[Dealer] Your jackpot:")
    else:
        print(f"[Dealer] Oh, that's a shame, the numbers were {lotto_numbers}")
def solve_qlotto(testing_numbers):
    """
    根据 Testing Numbers 计算 Lotto Numbers。
    原理：Lotto bits = ~Testing bits (按位取反)
    推导公式：Lotto = ((21 - (Test - 1)) % 42) + 1
    """
    lotto_numbers = []
    for t in testing_numbers:
        # 公式推导：
        # Raw_Lotto = 63 - Raw_Test
        # Final_Lotto = (Raw_Lotto % 42) + 1
        # Final_Lotto = ((63 - Raw_Test) % 42) + 1
        #             = ((21 - Raw_Test) % 42) + 1
        # Raw_Test 与 (t-1) 同余 42，所以可以直接替换
        val = ((21 - (t - 1)) % 42) + 1
        lotto_numbers.append(val)
    return lotto_numbers

if __name__ == "__main__":
    print("--- QLotto Solver ---")
    print("请先在服务器输入量子指令: H:0;RXX:90,0,1;H:0;Z:0;H:0")
   
    try:
        user_input = input("请输入服务器返回的 draws 数组 (例如 25,21,10...): ")
        # 处理可能的方括号
        clean_input = user_input.replace('[', '').replace(']', '')
        if not clean_input.strip():
            print("输入为空")
            exit()
           
        testing_nums = [int(x.strip()) for x in clean_input.split(',')]
       
        if len(testing_nums) != 6:
            print(f"警告: 输入了 {len(testing_nums)} 个数字，通常需要 6 个。")

        winning_nums = solve_qlotto(testing_nums)
       
        print("n[+] 计算出的必胜数字 (复制粘贴回服务器):")
        print(",".join(map(str, winning_nums)))
       
    
except ValueError:
        print("[-] 输入格式错误，请确保输入的是逗号分隔的数字。")
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]