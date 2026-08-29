---
title: 量子安全 quantum ctf Qlotto Hack the box
contest: Quantum CTF / Hack The Box QLotto
year: 2025
difficulty: hard
vuln_type: misc_math
tags: [qiskit, quantum-circuit, Aer-simulator, qasm-simulator, QuantumCircuit, H-S-T-Z-gates, RXX-RYY-RZZ, binomialtest, entropy-validation, quantum-lotto]
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
---

## 题目列表

1道量子安全:QLotto (Hack The Box)

## 关键考点

### 代码分析(server.py)
```python
from qiskit import QuantumCircuit, ClassicalRegister, transpile
from scipy.stats import binomtest
from qiskit_aer import Aer
from math import pi

class QuantumLotto:
    def __init__(self):
        self.backend = Aer.get_backend("qasm_simulator")
    
    def degrees_to_radians(self, degrees: int):
        return degrees * (pi / 180)
    
    def generate_circuit(self, instructions: str):
        circuit = QuantumCircuit(2)
        circuit.h(0)  # 初始H门
        instructions = instructions.split(";")
        for instr in instructions:
            parts = instr.split(":")
            if len(parts) != 2: return None
            gate, params = parts
            params = [int(p) for p in params.split(",")]
            
            if len(params) == 1:
                if gate == "H": circuit.h(params[0])
                elif gate == "S": circuit.s(params[0])
                elif gate == "T": circuit.t(params[0])
                elif gate == "Z": circuit.z(params[0])
            elif len(params) == 3:
                phase = self.degrees_to_radians(params[0])
                if gate == "RXX": circuit.rxx(phase, params[1], params[2])
                elif gate == "RYY": circuit.ryy(phase, params[1], params[2])
                elif gate == "RZZ": circuit.rzz(phase, params[1], params[2])
```

### validate_entropy
```python
def validate_entropy(self, base_circuit, shots=100_000):
    circuit = base_circuit.copy()
    circuit.add_register(ClassicalRegister(1))
    circuit.measure(0, 0)
    compiled = transpile(circuit, self.backend)
    results = self.backend.run(compiled, shots=shots).result()
    counts = results.get_counts()
    binomial_test = binomtest(counts.get('0', 0), n=shots, p=0.5, alternative='two-sided')
    if binomial_test.pvalue < 0.01: return False
    return True
```

### extract_numbers
```python
def extract_numbers(self, memory):
    lotto_numbers = []
    testing_numbers = []
    for i in range(0, len(memory), 6):
        bits = memory[i:i+6]
        lotto_number = ""
        testing_number = ""
        for testing_bit, lotto_bit in bits:
            lotto_number += str(lotto_bit)
            testing_number += str(testing_bit)
        lotto_number = int(lotto_number, 2) % 42 + 1
        testing_number = int(testing_number, 2) % 42 + 1
        lotto_numbers.append(lotto_number)
        testing_numbers.append(testing_number)
    return lotto_numbers, testing_numbers
```

### main
```python
def main():
    lotto = QuantumLotto()
    instructions = input("[Dealer] Place your quantum moves : ")
    numbers = lotto.run_lotto(instructions)
    if not numbers: return
    lotto_numbers, testing_numbers = numbers
    if lotto_numbers == testing_numbers:
        print("[Dealer] Trying to mirror the house's numbers, are we?")
        return
    print(f"[Dealer] Your draws are: {testing_numbers}")
    guess_numbers = input("[Dealer] Place your six bets on the table : ")
    guess_numbers = [int(n) for n in guess_numbers.split(",")]
    if len(guess_numbers) != 6 or any(n < 1 or n > 42 for n in guess_numbers):
        return
    if guess_numbers == lotto_numbers:
        print("The table erupts in chaos — you've cracked the QLotto!")
```

### 关键攻击公式
```python
def solve_qlotto(testing_numbers):
    """
    根据 Testing Numbers 计算 Lotto Numbers。
    原理:Lotto bits = ~Testing bits (按位取反)
    推导公式:Lotto = ((21 - (Test - 1)) % 42) + 1
    """
    lotto_numbers = []
    for t in testing_numbers:
        # Raw_Lotto = 63 - Raw_Test
        # Final_Lotto = (Raw_Lotto % 42) + 1
        lotto = ((21 - (t - 1)) % 42) + 1
        lotto_numbers.append(lotto)
    return lotto_numbers
```

### 攻击策略
1. 设计量子电路让test和lotto不同
2. 但guess能匹配lotto
3. 利用Lotto bits = ~Testing bits(按位取反)关系
4. 从testing推算lotto
5. 输入guess=lotto即中

## 实战价值
- 量子电路题先理解验证逻辑(entropy validation + bit extraction + 42取模)
- 再设计电路让test和lotto不同但guess能匹配lotto
- 按位取反关系是常见模式
- qiskit+Aer qasm_simulator是量子电路模拟标配
- binomtest pvalue<0.01是entropy validation标准
- 量子CTF是新兴方向,2025+会有更多
