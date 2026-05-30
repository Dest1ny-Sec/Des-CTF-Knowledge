# 从ANGR-CTF项目入手ANGR和符号执行技术

> 原文: https://www.ctfiot.com/285534.html
> ID: 285534

$sudopip install angr

importangrp=angr.Project('file_path')

gitclonehttps://github.com/jakespringer/angr_ctf

importangrp = Project('./00_angr_find',load_options = {'auto_load_libs':
False},main_opts = {'base_addr':
0x804850})#p = Project('./00_angr_find',auto_load_libs=False)

state= p.factory.entry_state()#初始化状态为程序运行到程序入口点的状态#factory负责将Project实例化simgr= p.factory.simgr(state)#创建模拟管理器，将初始化后的state添加到SM中target=0x8048678#目标地址(输出Good job)

simgr.explore(find=target)#搜索路径，模拟管理器将尝试找到一个执行路径，使程序到达目标地址ifsimgr.found:#找到满足条件的路径 so_state = simgr.found[0]#获取第一个满足条件的状态print(so_state.posix.dumps(0))#打印标准输入（文件描述符0）的内容==》程序运行过程中的输入内容

import angrp = angr.Project('./00_angr_find',load_options = {'auto_load_libs': False},main_opts = {'base_addr':
0x804850})#p = Project('./00_angr_find',auto_load_libs=False) state= p.factory.entry_state()#初始化状态为程序运行到程序入口点的状态#factory负责将Project实例化simgr = p.factory.simgr(state)#创建模拟管理器，将初始化后的state添加到SM中target =0x8048678#目标地址(输出Good job)simgr.explore(find=target)#搜索路径，模拟管理器将尝试找到一个执行路径，使程序到达目标地址ifsimgr.found:#找到满足条件的路径 so_state = simgr.found[0]#获取第一个满足条件的状态print(so_state.posix.dumps(0))#打印标准输入（文件描述符0）的内容==》程序运行过程中的输入内容

import angrio = angr.Project('./01_angr_avoid',auto_load_libs=False)init_state = io.factory.entry_state()simgr = io.factory.simgr(init_state)target = 0x80485E0#目标地址un_target = 0x80485A8#不想被执行的地址#avoid=un_target为不想执行这里simgr.explore(find=target,avoid=un_target)if simgr.found: so_state = simgr.found[0] print(so_state.posix.dumps(0))

importangrimportsysio = angr.Project('./02_angr_find_condition',auto_load_libs=False)init_state = io.factory.entry_state()simgr = io.factory.simgr(init_state)#通过引入检测函数实现动态的选择想获取的statedefis_succ(state):#将标准输出的内容存储到变量std_out中 std_out = state.posix.dumps(sys.stdout.fileno())ifb'Good Job.'instd_out:
returnTrueelse:
returnFalsedefis_fail(state): std_out = state.posix.dumps(sys.stdout.fileno())ifb'Try again.'instd_out:
returnTrueelse:
returnFalse#采用状态检测simgr.explore(find=is_succ,avoid=is_fail)ifsimgr.found: so_state = simgr.found[0]print(so_state.posix.dumps(0))

importangrimportclaripyimportsysio = angr.Project('./03_angr_symbolic_registers',auto_load_libs=False)state_addr =0x8048980init_state = io.factory.blank_state(addr = state_addr)#跳过输入函数，从目标地址开始执行passwd_size =32#符号向量大小#通过claripy创建符号向量passwd0 = claripy.BVS('passwd0',passwd_size)passwd1 = claripy.BVS('passwd1',passwd_size)passwd2 = claripy.BVS('passwd2',passwd_size)#对寄存器进行赋值init_state.regs.eax = passwd0init_state.regs.ebx = passwd1init_state.regs.edx = passwd2simgr = io.factory.simgr(init_state)defis_succ(state): std_out = state.posix.dumps(sys.stdout.fileno())ifb'Good Job.'instd_out:
returnTrueelse:
returnFalsedefis_fail(state): std_out = state.posix.dumps(sys.stdout.fileno())ifb'Try again.'instd_out:
returnTrueelse:
returnFalsesimgr.explore(find=is_succ,avoid=is_fail)ifsimgr.found: so_state = simgr.found[0] so0 =hex(so_state.solver.eval(passwd0)) so1 =hex(so_state.solver.eval(passwd1)) so2 =hex(so_state.solver.eval(passwd2))print(so0,so1,so2)

importangrimportsysimportclaripyproject = angr.Project('./04_angr_symbolic_stack')initial_state = project.factory.blank_state(addr=0x8048697)arg1 = claripy.BVS('arg1',32)arg2 = claripy.BVS('arg2',32)initial_state.regs.esp = initial_state.regs.ebpinitial_state.regs.esp -=8#esp-8initial_state.stack_push(arg1)initial_state.stack_push(arg2)#v1_addr = initial_state.regs.ebp - 0x10 # 第二个输入直接指定地址#v2_addr = initial_state.regs.ebp - 0x0C # 第一个输入指定地址#initial_state.memory.store(v1_addr, arg2, endness=project.arch.memory_endness)#initial_state.memory.store(v2_addr, arg1, endness=project.arch.memory_endness)simgr = project.factory.simulation_manager(initial_state)defright(state):
ifb'Good'instate.posix.dumps(1):
returnTrueelse:
returnFalsedefwrong(state):
ifb'Try'instate.posix.dumps(1):
returnTrueelse:
returnFalsesimgr.explore(find=right, avoid=wrong)ifsimgr.found: solution_state = simgr.found[0]print(solution_state.solver.eval(arg1))print(solution_state.solver.eval(arg2))

importangrimportsysimportclaripyproject = angr.Project('./05_angr_symbolic_memory')initial_state = project.factory.blank_state(addr=0x8048601)arg1 = claripy.BVS('arg1',64)arg2 = claripy.BVS('arg2',64)arg3 = claripy.BVS('arg3',64)arg4 = claripy.BVS('arg4',64)addr =0xA1BA1C0initial_state.memory.store(addr, arg1)initial_state.memory.store(addr +0x8, arg2)initial_state.memory.store(addr +0x10, arg3)initial_state.memory.store(addr +0x18, arg4)simgr = project.factory.simulation_manager(initial_state)defright(state):
ifb'Good'instate.posix.dumps(1):
returnTrueelse:
returnFalsedefwrong(state):
ifb'Try'instate.posix.dumps(1):
returnTrueelse:
returnFalsesimgr.explore(find=right, avoid=wrong)ifsimgr.found: solution_state = simgr.found[0]print(solution_state.solver.eval(arg1, cast_to=bytes))print(solution_state.solver.eval(arg2, cast_to=bytes))print(solution_state.solver.eval(arg3, cast_to=bytes))print(solution_state.solver.eval(arg4, cast_to=bytes))

importangrimportclaripydefsolve():# 加载程序（不加载库函数，提升速度） proj = angr.Project('./06_angr_symbolic_dynamic_memory', auto_load_libs=False)
# 从输入完成后开始执行（跳过malloc和scanf） start_addr =0x08048699 state = proj.factory.blank_state(addr=start_addr)
# 创建两个符号变量（8字节密码） passwd0 = claripy.BVS('passwd0',8*8) passwd1 = claripy.BVS('passwd1',8*8)
# 伪造堆地址（BSS段中未使用的区域） fake_chunk0 =0x12340 fake_chunk1 =0x12350
# 篡改指针：让buffer0/buffer1指向伪造地址
# 注意：必须指定端序和size，否则会有警告[^12^] state.memory.store(0xABCC8A4, fake_chunk0, endness=proj.arch.memory_endness, size=4) state.memory.store(0xABCC8AC, fake_chunk1, endness=proj.arch.memory_endness, size=4)
# 将符号变量存入伪造堆块 state.memory.store(fake_chunk0, passwd0) state.memory.store(fake_chunk1, passwd1)
# 创建模拟管理器 simgr = proj.factory.simulation_manager(state)
# 定义成功/失败条件defis_success(s):
returnb'Good Job.'ins.posix.dumps(1)defis_fail(s):
returnb'Try again.'ins.posix.dumps(1)
# 探索路径 simgr.explore(find=is_success, avoid=is_fail)ifsimgr.found: sol_state = simgr.found[0]# 求解并转换为字节 sol0 = sol_state.solver.eval(passwd0, cast_to=bytes) sol1 = sol_state.solver.eval(passwd1, cast_to=bytes)print(f"Solution:{sol0}{sol1}")returnsol0, sol1else:
print("No solution found")returnNoneif__name__ =='__main__': solve()

importangrimportclaripydefsolve():# 加载程序 proj = angr.Project('./07_angr_symbolic_file', auto_load_libs=False)
# 从文件读取完成后开始执行（跳过fopen/fscanf） start_addr =0x080488D3 state = proj.factory.blank_state(addr=start_addr)
# 创建符号变量表示文件内容（0x40 = 64字节） file_content = claripy.BVS('file_content',8*0x40)
# 创建虚拟文件
# 注意：文件名必须与程序硬编码的一致 sim_file = angr.SimFile('OJKSQYDP.txt', content=file_content)
# 将虚拟文件插入文件系统 state.fs.insert('OJKSQYDP.txt', sim_file)
# 关键：劫持全局文件名指针
# file_str = 0xA1BA1C0，指向文件名字符串 fake_path_addr =0x12345 state.memory.store(0xA1BA1C0, fake_path_addr, endness=proj.arch.memory_endness, size=4)
# 写入实际路径字符串 state.memory.store(fake_path_addr,b'OJKSQYDP.txtx00')
# 创建模拟管理器 simgr = proj.factory.simulation_manager(state)
# 定义成功/失败条件defis_success(s):
returnb'Good Job.'ins.posix.dumps(1)defis_fail(s):
returnb'Try again.'ins.posix.dumps(1)
# 探索路径 simgr.explore(find=is_success, avoid=is_fail)ifsimgr.found: sol_state = simgr.found[0]# 求解文件内容并转换为字符串 solution = sol_state.solver.eval(file_content, cast_to=bytes)
# 提取有效部分（到 为止） solution_str = solution[:
solution.index(b'x00')]print(f"Solution:{solution_str.decode()}")returnsolution_strelse:
print("No solution found")returnNoneif__name__ =='__main__': solve()

importangrimportclaripydefsolve(): project = angr.Project('./08_angr_constraints', auto_load_libs=False)
# 从 scanf 返回后开始 initial_state = project.factory.blank_state(addr=0x08048625) sym_password = claripy.BVS('password',8*16) buffer_addr =0x0804A050 initial_state.memory.store(buffer_addr, sym_password) simgr = project.factory.simulation_manager(initial_state)
# 探索到 Good Job. 之前的状态 simgr.explore(find=0x08048696) ifsimgr.found: solution_state = simgr.found[0]# 变换后的 buffer transformed_buffer = solution_state.memory.load(buffer_addr,16)
# 延迟约束 solution_state.add_constraints(transformed_buffer ==b'AUPDNNPROEZRJWKB')
# 求解 solution = solution_state.solver.eval(sym_password, cast_to=bytes)print(solution)returnsolutionelse:
print(f"Not found. Active:{len(simgr.active)}")print(f"Deadended:{len(simgr.deadended)}")returnNoneif__name__ =='__main__': solve()

（0x8048460）：entry_state初始化栈帧

：真实调用，用户输入存入0x804A054

：原地变换 buffer，无分支

（0x80486B3）：

读取buffer（符号表达式）

比较buffer == target

（0x80486B8）：

+je

**只有buffer == target的路径到达 **Good Job.

：

是一个符号方程组

求解器逆向计算出password = inverse(complex_function, target)

importangrimportclaripydefsolve(): project = angr.Project('./09_angr_hooks', auto_load_libs=False)
# 1. entry_state：自动初始化栈、寄存器 initial_state = project.factory.entry_state( add_options={angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS} )
# 2. Hook check_equals（在函数内部做判断） check_equals_call =0x80486B3
# buffer_addr =0x804A054 # target_str =b'XYMKBKUHNIQYNQXE'# 从函数名提取 @project.hook(check_equals_call, length=5)defhook_check_equals(state):# 读取 buffer 内容 res = state.memory.load(buffer_addr,16)
# 直接判断并设置返回值（eax）# 只有 res == target 时，eax=1 → Good Job 路径 state.regs.eax = claripy.If(res == target_str, claripy.BVV(1,32), claripy.BVV(0,32))
# 3. 创建模拟管理器 simgr = project.factory.simulation_manager(initial_state)
# 4. 探索与规避defright(state):
returnb'Good'instate.posix.dumps(1)defwrong(state):
returnb'Try'instate.posix.dumps(1) simgr.explore(find=right, avoid=wrong)
# 5. 输出解ifsimgr.found: solution_state = simgr.found[0]print(solution_state.posix.dumps(0)) # 打印输入returnsolution_state.posix.dumps(0)else:
print("[-] No solution")returnNoneif__name__ =='__main__': solve()

initial_state= project.factory.entry_state()

@project.hook_symbol('check_equals_ORSDDWXHZURJRBDH',func())

defrun(self, a1, a2): res =self.state.memory.load(a1, a2) # 读取 s 的内容（已变换）returnclaripy.If(res == target,BVV(1,32),BVV(0,32))

// 程序执行到 check_equals 时：s[i] =complex_function(original_input[i],18-i);// s 里已是变换后的值（符号表达式）// 例如：// res[0] = (stdin[0] + 18) % 26 + 'A'// res[1] = (stdin[1] + 17) % 26 + 'A'// ...

simgr.explore(find=right, avoid=wrong)defright(state): return b'Good'in state.posix.dumps(1)

ifsimgr.found: solution_state = simgr.found[0]print(solution_state.posix.dumps(0)) # 求解符号化的 stdin

# 约束方程组：(stdin[0] +18) %26+'A'=='O'(stdin[1] +17) %26+'A'=='R'...(stdin[15] +3) %26+'A'=='H'# 求解器逆向求解：stdin[0] = ('O'-'A'-18) %26='M'stdin[1] = ('R'-'A'-17) %26='S'...stdin[15] = ('H'-'A'-3) %26='K'# 结果：b'MSWKNJNAVTTOZMRY'

importangrimportclaripydefsolve():""" 核心思路：用 SimProcedure 替换 check_equals 函数，避免 2^16 路径爆炸 """# 1. 加载二进制文件
# auto_load_libs=False 防止自动加载库函数，避免 Hook 冲突 project = angr.Project('./10_angr_simprocedures', auto_load_libs=False)
# 2. 创建初始状态
# entry_state() 从程序入口开始，自动初始化栈、寄存器、内存
# 符号执行时，scanf 会自动从符号化的 stdin 读取输入 initial_state = project.factory.entry_state( add_options={angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS} )
# 3. 定义 SimProcedure 类替换 check_equals 函数
# 当程序调用 check_equals_ORSDDWXHZURJRBDH 时，执行此逻辑classCheckEqualsHook(angr.SimProcedure):
defrun(self, buffer_ptr, length):""" 参数说明： buffer_ptr: check_equals 的第一个参数，指向变换后的字符串 length: check_equals 的第二个参数，固定为 16 """# 从内存加载变换后的字符串（16字节）# 此时 buffer 已被 complex_function 处理过 transformed_buffer = self.state.memory.load(buffer_ptr, length)
# 目标字符串（从函数名中提取） target_string =b'ORSDDWXHZURJRBDH'# 直接返回判断结果（无循环，无分支）# 如果 buffer == target，eax = 1（True），否则 eax = 0（False）returnclaripy.If( transformed_buffer == target_string, claripy.BVV(1,32), # 返回 1（验证通过） claripy.BVV(0,32) # 返回 0（验证失败） )
# 4. 挂钩符号：按函数名自动拦截调用
# hook_symbol 比 hook(addr) 更健壮，不受地址变化影响 project.hook_symbol('check_equals_ORSDDWXHZURJRBDH', CheckEqualsHook())
# 5. 创建模拟管理器 simgr = project.factory.simulation_manager(initial_state)
# 6. 定义成功与失败条件
# right: stdout 包含 "Good Job."# wrong: stdout 包含 "Try again."defright(state):
returnb'Good'instate.posix.dumps(1)defwrong(state):
returnb'Try'instate.posix.dumps(1)
# 7. 探索状态空间
# 只保留到达 "Good Job." 的路径，避开 "Try again." simgr.explore(find=right, avoid=wrong)
# 8. 输出结果ifsimgr.found: solution_state = simgr.found[0]# 求解符号化的 stdin，得到原始输入 solution = solution_state.posix.dumps(0)print(solution)returnsolutionelse:
print(f"[-] No solution found. Deadended:{len(simgr.deadended)}")returnNoneif__name__ =='__main__': solve()

importangrimportclaripydefsolve():""" angr-ctf 11_angr_sim_scanf 解题脚本 题目逻辑： 1. 程序初始化字符串 "SUQMKQFX"，对每个字符做凯撒移位 2. 调用 scanf("%u %u", &buffer0, &buffer1) 读取两个无符号整数 3. 用 strncmp 比较 buffer0 和 buffer1 的内存字节表示与变换后的字符串 - buffer0 的前 4 字节 == 变换字符串的前 4 字符 - buffer1 的前 4 字节 == 变换字符串的后 4 字符 4. 需要找到两个整数，使其内存表示符合要求 """# 1. 加载二进制文件 project = angr.Project('./11_angr_sim_scanf', auto_load_libs=False)
# 2. 从程序入口开始执行
# entry_state 会自动符号化 stdin，为 scanf 做准备 initial_state = project.factory.entry_state()
# 3. 定义 SimProcedure 类替换 scanf 函数
# 当程序调用 __isoc99_scanf 时，执行此逻辑classScanfHook(angr.SimProcedure):
defrun(self, format_string, param0, param1):""" 参数说明： format_string: "%u %u" 格式字符串指针（可忽略） param0: buffer0 的地址（指向无符号整数） param1: buffer1 的地址（指向无符号整数） """# 创建两个 32 位符号变量，代表要读入的两个整数
# 每个整数占 4 字节，无符号 arg1 = claripy.BVS('arg1',32) arg2 = claripy.BVS('arg2',32)
# 将符号变量存入 param0 和 param1 指向的内存
# 使用小端序存储，符合 scanf 对无符号整数的处理 self.state.memory.store(param0, arg1, endness='LE') self.state.memory.store(param1, arg2, endness='LE')
# 将符号变量引用保存到 globals 字典
# 后续求解时需要从 state 中提取 self.state.globals['solutions'] = (arg1, arg2)
# 返回成功读入的参数个数（2）returnclaripy.BVV(2,32)
# 4. 用 hook_symbol 按函数名挂钩 scanf
# 自动拦截所有对 __isoc99_scanf 的调用 project.hook_symbol('__isoc99_scanf', ScanfHook())
# 5. 创建模拟管理器 simgr = project.factory.simulation_manager(initial_state)
# 6. 定义成功与失败条件
# right: stdout 包含 "Good Job."# wrong: stdout 包含 "Try again."defright(state):
returnb'Good'instate.posix.dumps(1)defwrong(state):
returnb'Try'instate.posix.dumps(1)
# 7. 探索状态空间
# 只保留到达 "Good Job." 的路径，避开 "Try again."# strncmp 会比较 buffer0 和 buffer1 的字节表示
# 只有符号变量的值匹配变换后的字符串才会保留 simgr.explore(find=right, avoid=wrong)
# 8. 求解并输出结果ifsimgr.found: solution_state = simgr.found[0]# 从 globals 中取出符号变量 stored_solutions = solution_state.globals['solutions']# 分别求解两个整数的具体值 scanf0_solution = solution_state.solver.eval(stored_solutions[0]) scanf1_solution = solution_state.solver.eval(stored_solutions[1])
# 打印结果print(scanf0_solution)print(scanf1_solution)returnscanf0_solution, scanf1_solutionelse:
print(f"[-] No solution found. Deadended:{len(simgr.deadended)}")returnNoneif__name__ =='__main__': solve()

importangrimportclaripyimporttimedefsolve():""" 12_angr_veritesting 解题脚本 关键：启用 veritesting=True，自动优化路径爆炸 """# 记录开始时间 start_time = time.perf_counter()
# 加载二进制文件，不加载库提升速度 p = angr.Project('./12_angr_veritesting', auto_load_libs=False)
# 从入口开始执行 init_state = p.factory.entry_state()
# 定义成功条件：stdout 包含 "Good"defgood(state):
returnb'Good'instate.posix.dumps(1)
# 定义失败条件：stdout 包含 "Try"defbad(state):
returnb'Try'instate.posix.dumps(1)
# 创建模拟管理器，启用 Veritesting 自动路径合并 simgr = p.factory.simgr(init_state, veritesting=True)
# 探索路径，find=good 表示找到成功路径，avoid=bad 表示避开失败路径 simgr.explore(find=good, avoid=bad)
# 如果找到解ifsimgr.found: solution_state = simgr.found[0]# 求解 stdin 输入 solution = solution_state.posix.dumps(0).decode()print(f"Solution:{solution}")
# 打印执行时间，展示 Veritesting 性能print(f"Time elapsed:{time.perf_counter() - start_time:.2f}seconds")if__name__ =='__main__': solve()

importangrimportclaripyclassStrlenHook(angr.SimProcedure):"""Hook strlen 函数，返回符号长度"""defrun(self, s):# 创建符号值作为返回值returnclaripy.BVS('strlen_ret',32)defsolve():""" 13_angr_static_binary 解题脚本 关键：静态库函数在二进制内部，需要 hook 简化执行 """# 加载静态链接二进制 p = angr.Project('./13_angr_static_binary', auto_load_libs=False)
# 从 main 函数开始，跳过 _start 的库初始化 init_state = p.factory.entry_state()
# Hook strlen 函数地址（通过 objdump 获取）# 0x4013b0 是静态编译后的 strlen 入口 strlen_addr =0x4013b0 p.hook(strlen_addr, StrlenHook(), length=5)
# 定义成功路径：输出 "Good Job."defgood(state):
returnb'Good Job.'instate.posix.dumps(1)
# 定义失败路径：输出 "Try again."defbad(state):
returnb'Try again.'instate.posix.dumps(1)
# 创建模拟管理器 simgr = p.factory.simgr(init_state)
# 探索路径 simgr.explore(find=good, avoid=bad)ifsimgr.found: solution_state = simgr.found[0]# 求解 stdin 输入 solution = solution_state.posix.dumps(0).decode()print(f"Solution:{solution}")if__name__ =='__main__': solve()

importangrimportclaripydefsolve():""" 14_angr_shared_library 解题脚本 关键：加载共享库，直接在库函数入口执行 """# 加载主程序 p = angr.Project('./14_angr_shared_library', auto_load_libs=False)
# 手动加载共享库
# 注意：需要确保 lib14_angr_shared_library.so 在当前目录 lib = angr.Project('./lib14_angr_shared_library.so', auto_load_libs=False)
# 创建初始状态，从库函数 validate 入口开始
# 0x1234 是库函数 validate 的入口（通过 objdump 获取） validate_addr =0x1234 state = lib.factory.blank_state(addr=validate_addr)
# 符号化函数参数（char* buffer） buffer_addr =0x1000
# 选择一个未使用的内存地址 sym_buffer = claripy.BVS('buffer',8*16) state.memory.store(buffer_addr, sym_buffer)
# 设置函数参数
# x86 调用约定：参数在栈上 state.regs.eax = buffer_addr
# 定义成功条件：库函数返回 0（验证通过）defgood(state):
returnstate.regs.eax ==0defbad(state):
returnstate.regs.eax !=0
# 创建模拟管理器 simgr = lib.factory.simgr(state)
# 探索 simgr.explore(find=good, avoid=bad)ifsimgr.found: solution_state = simgr.found[0]# 求解 buffer solution = solution_state.solver.eval(sym_buffer, cast_to=bytes)print(f"Solution:{solution}")if__name__ =='__main__': solve()

importangrimportclaripydefsolve():""" 15_angr_arbitrary_read 解题脚本 关键：利用格式化字符串漏洞读取内存，找到 secret 字符串 """ p = angr.Project('./15_angr_arbitrary_read', auto_load_libs=False) init_state = p.factory.entry_state()
# scanf 会读取格式化字符串，我们需要构造 payload
# payload 格式："%<offset>$s" 读取 stack[offset] 指向的字符串
# 符号化输入：假设我们知道 secret 在 stack 的第 7 个位置
# payload = "%7$s" + padding payload = claripy.BVS('payload',8*20)
# 约束 payload 格式：以 %7$s 开头 init_state.solver.add(payload.get_byte(0) ==ord('%')) init_state.solver.add(payload.get_byte(1) ==ord('7')) init_state.solver.add(payload.get_byte(2) ==ord('$')) init_state.solver.add(payload.get_byte(3) ==ord('s'))
# 将 payload 存入 stdin init_state.memory.store(init_state.posix.stdin.addr, payload)defgood(state):
returnb'Good'instate.posix.dumps(1)defbad(state):
returnb'Try'instate.posix.dumps(1) simgr = p.factory.simgr(init_state) simgr.explore(find=good, avoid=bad)ifsimgr.found: solution_state = simgr.found[0]# 求解 payload solution = solution_state.solver.eval(payload, cast_to=bytes)print(f"Solution:{solution}")if__name__ =='__main__': solve()

importangrimportclaripydefsolve():""" 16_angr_arbitrary_write 解题脚本 关键：利用栈溢出覆盖返回地址，劫持控制流 """ p = angr.Project('./16_angr_arbitrary_write', auto_load_libs=False) init_state = p.factory.entry_state()
# scanf 会读取输入到栈上，需要构造 payload 覆盖返回地址
# payload 结构：[填充数据] + [secret_function 地址]# 符号化输入（假设需要 64 字节覆盖到返回地址） payload = claripy.BVS('payload',8*64)
# secret_function 地址（通过 objdump 获取） secret_addr =0x08048456
# 约束 payload 的最后 4 字节为 secret_addr（小端序）fori, byteinenumerate(secret_addr.to_bytes(4,'little')): init_state.solver.add(payload.get_byte(60+ i) == byte)
# 将 payload 存入 stdin init_state.memory.store(init_state.posix.stdin.addr, payload)
# 成功条件：程序执行到 secret_function
# 0x08048456 是 secret_function 入口 simgr = p.factory.simgr(init_state) simgr.explore(find=0x08048456)ifsimgr.found: solution_state = simgr.found[0]# 求解 payload solution = solution_state.solver.eval(payload, cast_to=bytes)print(f"Solution:{solution.hex()}")if__name__ =='__main__': solve()

importangrimportclaripydefsolve():""" 17_angr_arbitrary_jump 解题脚本 关键：利用漏洞直接设置程序计数器（PC） """ p = angr.Project('./17_angr_arbitrary_jump', auto_load_libs=False) init_state = p.factory.entry_state()
# 程序会读取一个地址字符串并跳转到该地址
# 我们需要提供 secret_function 的地址
# 符号化输入（地址字符串） input_addr = claripy.BVS('input_addr',8*10)
# secret_function 地址（通过 objdump 获取） secret_addr =0x08048456
# 约束输入地址等于 secret_addr 的字符串表示
# 例如：0x08048456 -> "08048456" secret_str =f"{secret_addr:x}"fori, charinenumerate(secret_str): init_state.solver.add(input_addr.get_byte(i) ==ord(char))
# 将输入存入 stdin init_state.memory.store(init_state.posix.stdin.addr, input_addr)
# 成功条件：程序跳转到 secret_function
# 0x08048456 是 secret_function 入口 simgr = p.factory.simgr(init_state) simgr.explore(find=0x08048456)ifsimgr.found: solution_state = simgr.found[0]# 求解输入 solution = solution_state.solver.eval(input_addr, cast_to=bytes).decode()print(f"Solution:{solution}")if__name__ =='__main__': solve()

看雪ID：S_i_d

https://bbs.kanxue.com/user-home-909653.htm

*本文为看雪论坛优秀文章，由S_i_d原创，转载请注明来自看雪社区

# 往期推荐

Hyper-V平台IUM进程调试工具及通用TPM漏洞CVE-2025-2884分析与复现

第八届强网拟态防御国际精英挑战赛 – WIN！致敬mt 复现

VmProtect.3.9.4分析之虚拟机流程

极路由远程命令执行漏洞-漏洞分析

一道CTF题目animals：变异MD5加密分析

球分享

球点赞

球在看

点击阅读原文查看更多


```
$sudopip install angr
importangrp=angr.Project('file_path')
gitclonehttps://github.com/jakespringer/angr_ctf
importangrp = Project('./00_angr_find',load_options = {'auto_load_libs':
False},main_opts = {'base_addr':
0x804850})#p = Project('./00_angr_find',auto_load_libs=False)
state= p.factory.entry_state()#初始化状态为程序运行到程序入口点的状态#factory负责将Project实例化simgr= p.factory.simgr(state)#创建模拟管理器，将初始化后的state添加到SM中target=0x8048678#目标地址(输出Good job)
simgr.explore(find=target)#搜索路径，模拟管理器将尝试找到一个执行路径，使程序到达目标地址ifsimgr.found:#找到满足条件的路径 so_state = simgr.found[0]#获取第一个满足条件的状态print(so_state.posix.dumps(0))#打印标准输入（文件描述符0）的内容==》程序运行过程中的输入内容
import angrp = angr.Project('./00_angr_find',load_options = {'auto_load_libs': False},main_opts = {'base_addr':
0x804850})#p = Project('./00_angr_find',auto_load_libs=False) state= p.factory.entry_state()#初始化状态为程序运行到程序入口点的状态#factory负责将Project实例化simgr = p.factory.simgr(state)#创建模拟管理器，将初始化后的state添加到SM中target =0x8048678#目标地址(输出Good job)simgr.explore(find=target)#搜索路径，模拟管理器将尝试找到一个执行路径，使程序到达目标地址ifsimgr.found:#找到满足条件的路径 so_state = simgr.found[0]#获取第一个满足条件的状态print(so_state.posix.dumps(0))#打印标准输入（文件描述符0）的内容==》程序运行过程中的输入内容
import angrio = angr.Project('./01_angr_avoid',auto_load_libs=False)init_state = io.factory.entry_state()simgr = io.factory.simgr(init_state)target = 0x80485E0#目标地址un_target = 0x80485A8#不想被执行的地址#avoid=un_target为不想执行这里simgr.explore(find=target,avoid=un_target)if simgr.found: so_state = simgr.found[0] print(so_state.posix.dumps(0))
importangrimportsysio = angr.Project('./02_angr_find_condition',auto_load_libs=False)init_state = io.factory.entry_state()simgr = io.factory.simgr(init_state)#通过引入检测函数实现动态的选择想获取的statedefis_succ(state):#将标准输出的内容存储到变量std_out中 std_out = state.posix.dumps(sys.stdout.fileno())ifb'Good Job.'instd_out:
returnTrueelse:
returnFalsedefis_fail(state): std_out = state.posix.dumps(sys.stdout.fileno())ifb'Try again.'instd_out:
returnTrueelse:
returnFalse#采用状态检测simgr.explore(find=is_succ,avoid=is_fail)ifsimgr.found: so_state = simgr.found[0]print(so_state.posix.dumps(0))
importangrimportclaripyimportsysio = angr.Project('./03_angr_symbolic_registers',auto_load_libs=False)state_addr =0x8048980init_state = io.factory.blank_state(addr = state_addr)#跳过输入函数，从目标地址开始执行passwd_size =32#符号向量大小#通过claripy创建符号向量passwd0 = claripy.BVS('passwd0',passwd_size)passwd1 = claripy.BVS('passwd1',passwd_size)passwd2 = claripy.BVS('passwd2',passwd_size)#对寄存器进行赋值init_state.regs.eax = passwd0init_state.regs.ebx = passwd1init_state.regs.edx = passwd2simgr = io.factory.simgr(init_state)defis_succ(state): std_out = state.posix.dumps(sys.stdout.fileno())ifb'Good Job.'instd_out:
returnTrueelse:
returnFalsedefis_fail(state): std_out = state.posix.dumps(sys.stdout.fileno())ifb'Try again.'instd_out:
returnTrueelse:
returnFalsesimgr.explore(find=is_succ,avoid=is_fail)ifsimgr.found: so_state = simgr.found[0] so0 =hex(so_state.solver.eval(passwd0)) so1 =hex(so_state.solver.eval(passwd1)) so2 =hex(so_state.solver.eval(passwd2))print(so0,so1,so2)
importangrimportsysimportclaripyproject = angr.Project('./04_angr_symbolic_stack')initial_state = project.factory.blank_state(addr=0x8048697)arg1 = claripy.BVS('arg1',32)arg2 = claripy.BVS('arg2',32)initial_state.regs.esp = initial_state.regs.ebpinitial_state.regs.esp -=8#esp-8initial_state.stack_push(arg1)initial_state.stack_push(arg2)#v1_addr = initial_state.regs.ebp - 0x10 # 第二个输入直接指定地址#v2_addr = initial_state.regs.ebp - 0x0C # 第一个输入指定地址#initial_state.memory.store(v1_addr, arg2, endness=project.arch.memory_endness)#initial_state.memory.store(v2_addr, arg1, endness=project.arch.memory_endness)simgr = project.factory.simulation_manager(initial_state)defright(state):
ifb'Good'instate.posix.dumps(1):
returnTrueelse:
returnFalsedefwrong(state):
ifb'Try'instate.posix.dumps(1):
returnTrueelse:
returnFalsesimgr.explore(find=right, avoid=wrong)ifsimgr.found: solution_state = simgr.found[0]print(solution_state.solver.eval(arg1))print(solution_state.solver.eval(arg2))
importangrimportsysimportclaripyproject = angr.Project('./05_angr_symbolic_memory')initial_state = project.factory.blank_state(addr=0x8048601)arg1 = claripy.BVS('arg1',64)arg2 = claripy.BVS('arg2',64)arg3 = claripy.BVS('arg3',64)arg4 = claripy.BVS('arg4',64)addr =0xA1BA1C0initial_state.memory.store(addr, arg1)initial_state.memory.store(addr +0x8, arg2)initial_state.memory.store(addr +0x10, arg3)initial_state.memory.store(addr +0x18, arg4)simgr = project.factory.simulation_manager(initial_state)defright(state):
ifb'Good'instate.posix.dumps(1):
returnTrueelse:
returnFalsedefwrong(state):
ifb'Try'instate.posix.dumps(1):
returnTrueelse:
returnFalsesimgr.explore(find=right, avoid=wrong)ifsimgr.found: solution_state = simgr.found[0]print(solution_state.solver.eval(arg1, cast_to=bytes))print(solution_state.solver.eval(arg2, cast_to=bytes))print(solution_state.solver.eval(arg3, cast_to=bytes))print(solution_state.solver.eval(arg4, cast_to=bytes))
importangrimportclaripydefsolve():# 加载程序（不加载库函数，提升速度） proj = angr.Project('./06_angr_symbolic_dynamic_memory', auto_load_libs=False)
# 从输入完成后开始执行（跳过malloc和scanf） start_addr =0x08048699 state = proj.factory.blank_state(addr=start_addr)
# 创建两个符号变量（8字节密码） passwd0 = claripy.BVS('passwd0',8*8) passwd1 = claripy.BVS('passwd1',8*8)
# 伪造堆地址（BSS段中未使用的区域） fake_chunk0 =0x12340 fake_chunk1 =0x12350
# 篡改指针：让buffer0/buffer1指向伪造地址
# 注意：必须指定端序和size，否则会有警告[^12^] state.memory.store(0xABCC8A4, fake_chunk0, endness=proj.arch.memory_endness, size=4) state.memory.store(0xABCC8AC, fake_chunk1, endness=proj.arch.memory_endness, size=4)
# 将符号变量存入伪造堆块 state.memory.store(fake_chunk0, passwd0) state.memory.store(fake_chunk1, passwd1)
# 创建模拟管理器 simgr = proj.factory.simulation_manager(state)
# 定义成功/失败条件defis_success(s):
returnb'Good Job.'ins.posix.dumps(1)defis_fail(s):
returnb'Try again.'ins.posix.dumps(1)
# 探索路径 simgr.explore(find=is_success, avoid=is_fail)ifsimgr.found: sol_state = simgr.found[0]# 求解并转换为字节 sol0 = sol_state.solver.eval(passwd0, cast_to=bytes) sol1 = sol_state.solver.eval(passwd1, cast_to=bytes)print(f"Solution:{sol0}{sol1}")returnsol0, sol1else:
print("No solution found")returnNoneif__name__ =='__main__': solve()
importangrimportclaripydefsolve():# 加载程序 proj = angr.Project('./07_angr_symbolic_file', auto_load_libs=False)
# 从文件读取完成后开始执行（跳过fopen/fscanf） start_addr =0x080488D3 state = proj.factory.blank_state(addr=start_addr)
# 创建符号变量表示文件内容（0x40 = 64字节） file_content = claripy.BVS('file_content',8*0x40)
# 创建虚拟文件
# 注意：文件名必须与程序硬编码的一致 sim_file = angr.SimFile('OJKSQYDP.txt', content=file_content)
# 将虚拟文件插入文件系统 state.fs.insert('OJKSQYDP.txt', sim_file)
# 关键：劫持全局文件名指针
# file_str = 0xA1BA1C0，指向文件名字符串 fake_path_addr =0x12345 state.memory.store(0xA1BA1C0, fake_path_addr, endness=proj.arch.memory_endness, size=4)
# 写入实际路径字符串 state.memory.store(fake_path_addr,b'OJKSQYDP.txtx00')
# 创建模拟管理器 simgr = proj.factory.simulation_manager(state)
# 定义成功/失败条件defis_success(s):
returnb'Good Job.'ins.posix.dumps(1)defis_fail(s):
returnb'Try again.'ins.posix.dumps(1)
# 探索路径 simgr.explore(find=is_success, avoid=is_fail)ifsimgr.found: sol_state = simgr.found[0]# 求解文件内容并转换为字符串 solution = sol_state.solver.eval(file_content, cast_to=bytes)
# 提取有效部分（到 为止） solution_str = solution[:
solution.index(b'x00')]print(f"Solution:{solution_str.decode()}")returnsolution_strelse:
print("No solution found")returnNoneif__name__ =='__main__': solve()
importangrimportclaripydefsolve(): project = angr.Project('./08_angr_constraints', auto_load_libs=False)
# 从 scanf 返回后开始 initial_state = project.factory.blank_state(addr=0x08048625) sym_password = claripy.BVS('password',8*16) buffer_addr =0x0804A050 initial_state.memory.store(buffer_addr, sym_password) simgr = project.factory.simulation_manager(initial_state)
# 探索到 Good Job. 之前的状态 simgr.explore(find=0x08048696) ifsimgr.found: solution_state = simgr.found[0]# 变换后的 buffer transformed_buffer = solution_state.memory.load(buffer_addr,16)
# 延迟约束 solution_state.add_constraints(transformed_buffer ==b'AUPDNNPROEZRJWKB')
# 求解 solution = solution_state.solver.eval(sym_password, cast_to=bytes)print(solution)returnsolutionelse:
print(f"Not found. Active:{len(simgr.active)}")print(f"Deadended:{len(simgr.deadended)}")returnNoneif__name__ =='__main__': solve()
importangrimportclaripydefsolve(): project = angr.Project('./09_angr_hooks', auto_load_libs=False)
# 1. entry_state：自动初始化栈、寄存器 initial_state = project.factory.entry_state( add_options={angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS} )
# 2. Hook check_equals（在函数内部做判断） check_equals_call =0x80486B3
# buffer_addr =0x804A054 # target_str =b'XYMKBKUHNIQYNQXE'# 从函数名提取 @project.hook(check_equals_call, length=5)defhook_check_equals(state):# 读取 buffer 内容 res = state.memory.load(buffer_addr,16)
# 直接判断并设置返回值（eax）# 只有 res == target 时，eax=1 → Good Job 路径 state.regs.eax = claripy.If(res == target_str, claripy.BVV(1,32), claripy.BVV(0,32))
# 3. 创建模拟管理器 simgr = project.factory.simulation_manager(initial_state)
# 4. 探索与规避defright(state):
returnb'Good'instate.posix.dumps(1)defwrong(state):
returnb'Try'instate.posix.dumps(1) simgr.explore(find=right, avoid=wrong)
# 5. 输出解ifsimgr.found: solution_state = simgr.found[0]print(solution_state.posix.dumps(0)) # 打印输入returnsolution_state.posix.dumps(0)else:
print("[-] No solution")returnNoneif__name__ =='__main__': solve()
initial_state= project.factory.entry_state()
@project.hook_symbol('check_equals_ORSDDWXHZURJRBDH',func())
defrun(self, a1, a2): res =self.state.memory.load(a1, a2) # 读取 s 的内容（已变换）returnclaripy.If(res == target,BVV(1,32),BVV(0,32))
// 程序执行到 check_equals 时：s[i] =complex_function(original_input[i],18-i);// s 里已是变换后的值（符号表达式）// 例如：// res[0] = (stdin[0] + 18) % 26 + 'A'// res[1] = (stdin[1] + 17) % 26 + 'A'// ...
simgr.explore(find=right, avoid=wrong)defright(state): return b'Good'in state.posix.dumps(1)
ifsimgr.found: solution_state = simgr.found[0]print(solution_state.posix.dumps(0)) # 求解符号化的 stdin
# 约束方程组：(stdin[0] +18) %26+'A'=='O'(stdin[1] +17) %26+'A'=='R'...(stdin[15] +3) %26+'A'=='H'# 求解器逆向求解：stdin[0] = ('O'-'A'-18) %26='M'stdin[1] = ('R'-'A'-17) %26='S'...stdin[15] = ('H'-'A'-3) %26='K'# 结果：b'MSWKNJNAVTTOZMRY'
importangrimportclaripydefsolve():""" 核心思路：用 SimProcedure 替换 check_equals 函数，避免 2^16 路径爆炸 """# 1. 加载二进制文件
# auto_load_libs=False 防止自动加载库函数，避免 Hook 冲突 project = angr.Project('./10_angr_simprocedures', auto_load_libs=False)
# 2. 创建初始状态
# entry_state() 从程序入口开始，自动初始化栈、寄存器、内存
# 符号执行时，scanf 会自动从符号化的 stdin 读取输入 initial_state = project.factory.entry_state( add_options={angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS} )
# 3. 定义 SimProcedure 类替换 check_equals 函数
# 当程序调用 check_equals_ORSDDWXHZURJRBDH 时，执行此逻辑classCheckEqualsHook(angr.SimProcedure):
defrun(self, buffer_ptr, length):""" 参数说明： buffer_ptr: check_equals 的第一个参数，指向变换后的字符串 length: check_equals 的第二个参数，固定为 16 """# 从内存加载变换后的字符串（16字节）# 此时 buffer 已被 complex_function 处理过 transformed_buffer = self.state.memory.load(buffer_ptr, length)
# 目标字符串（从函数名中提取） target_string =b'ORSDDWXHZURJRBDH'# 直接返回判断结果（无循环，无分支）# 如果 buffer == target，eax = 1（True），否则 eax = 0（False）returnclaripy.If( transformed_buffer == target_string, claripy.BVV(1,32), # 返回 1（验证通过） claripy.BVV(0,32) # 返回 0（验证失败） )
# 4. 挂钩符号：按函数名自动拦截调用
# hook_symbol 比 hook(addr) 更健壮，不受地址变化影响 project.hook_symbol('check_equals_ORSDDWXHZURJRBDH', CheckEqualsHook())
# 5. 创建模拟管理器 simgr = project.factory.simulation_manager(initial_state)
# 6. 定义成功与失败条件
# right: stdout 包含 "Good Job."# wrong: stdout 包含 "Try again."defright(state):
returnb'Good'instate.posix.dumps(1)defwrong(state):
returnb'Try'instate.posix.dumps(1)
# 7. 探索状态空间
# 只保留到达 "Good Job." 的路径，避开 "Try again." simgr.explore(find=right, avoid=wrong)
# 8. 输出结果ifsimgr.found: solution_state = simgr.found[0]# 求解符号化的 stdin，得到原始输入 solution = solution_state.posix.dumps(0)print(solution)returnsolutionelse:
print(f"[-] No solution found. Deadended:{len(simgr.deadended)}")returnNoneif__name__ =='__main__': solve()
importangrimportclaripydefsolve():""" angr-ctf 11_angr_sim_scanf 解题脚本 题目逻辑： 1. 程序初始化字符串 "SUQMKQFX"，对每个字符做凯撒移位 2. 调用 scanf("%u %u", &buffer0, &buffer1) 读取两个无符号整数 3. 用 strncmp 比较 buffer0 和 buffer1 的内存字节表示与变换后的字符串 - buffer0 的前 4 字节 == 变换字符串的前 4 字符 - buffer1 的前 4 字节 == 变换字符串的后 4 字符 4. 需要找到两个整数，使其内存表示符合要求 """# 1. 加载二进制文件 project = angr.Project('./11_angr_sim_scanf', auto_load_libs=False)
# 2. 从程序入口开始执行
# entry_state 会自动符号化 stdin，为 scanf 做准备 initial_state = project.factory.entry_state()
# 3. 定义 SimProcedure 类替换 scanf 函数
# 当程序调用 __isoc99_scanf 时，执行此逻辑classScanfHook(angr.SimProcedure):
defrun(self, format_string, param0, param1):""" 参数说明： format_string: "%u %u" 格式字符串指针（可忽略） param0: buffer0 的地址（指向无符号整数） param1: buffer1 的地址（指向无符号整数） """# 创建两个 32 位符号变量，代表要读入的两个整数
# 每个整数占 4 字节，无符号 arg1 = claripy.BVS('arg1',32) arg2 = claripy.BVS('arg2',32)
# 将符号变量存入 param0 和 param1 指向的内存
# 使用小端序存储，符合 scanf 对无符号整数的处理 self.state.memory.store(param0, arg1, endness='LE') self.state.memory.store(param1, arg2, endness='LE')
# 将符号变量引用保存到 globals 字典
# 后续求解时需要从 state 中提取 self.state.globals['solutions'] = (arg1, arg2)
# 返回成功读入的参数个数（2）returnclaripy.BVV(2,32)
# 4. 用 hook_symbol 按函数名挂钩 scanf
# 自动拦截所有对 __isoc99_scanf 的调用 project.hook_symbol('__isoc99_scanf', ScanfHook())
# 5. 创建模拟管理器 simgr = project.factory.simulation_manager(initial_state)
# 6. 定义成功与失败条件
# right: stdout 包含 "Good Job."# wrong: stdout 包含 "Try again."defright(state):
returnb'Good'instate.posix.dumps(1)defwrong(state):
returnb'Try'instate.posix.dumps(1)
# 7. 探索状态空间
# 只保留到达 "Good Job." 的路径，避开 "Try again."# strncmp 会比较 buffer0 和 buffer1 的字节表示
# 只有符号变量的值匹配变换后的字符串才会保留 simgr.explore(find=right, avoid=wrong)
# 8. 求解并输出结果ifsimgr.found: solution_state = simgr.found[0]# 从 globals 中取出符号变量 stored_solutions = solution_state.globals['solutions']# 分别求解两个整数的具体值 scanf0_solution = solution_state.solver.eval(stored_solutions[0]) scanf1_solution = solution_state.solver.eval(stored_solutions[1])
# 打印结果print(scanf0_solution)print(scanf1_solution)returnscanf0_solution, scanf1_solutionelse:
print(f"[-] No solution found. Deadended:{len(simgr.deadended)}")returnNoneif__name__ =='__main__': solve()
importangrimportclaripyimporttimedefsolve():""" 12_angr_veritesting 解题脚本 关键：启用 veritesting=True，自动优化路径爆炸 """# 记录开始时间 start_time = time.perf_counter()
# 加载二进制文件，不加载库提升速度 p = angr.Project('./12_angr_veritesting', auto_load_libs=False)
# 从入口开始执行 init_state = p.factory.entry_state()
# 定义成功条件：stdout 包含 "Good"defgood(state):
returnb'Good'instate.posix.dumps(1)
# 定义失败条件：stdout 包含 "Try"defbad(state):
returnb'Try'instate.posix.dumps(1)
# 创建模拟管理器，启用 Veritesting 自动路径合并 simgr = p.factory.simgr(init_state, veritesting=True)
# 探索路径，find=good 表示找到成功路径，avoid=bad 表示避开失败路径 simgr.explore(find=good, avoid=bad)
# 如果找到解ifsimgr.found: solution_state = simgr.found[0]# 求解 stdin 输入 solution = solution_state.posix.dumps(0).decode()print(f"Solution:{solution}")
# 打印执行时间，展示 Veritesting 性能print(f"Time elapsed:{time.perf_counter() - start_time:.2f}seconds")if__name__ =='__main__': solve()
importangrimportclaripyclassStrlenHook(angr.SimProcedure):"""Hook strlen 函数，返回符号长度"""defrun(self, s):# 创建符号值作为返回值returnclaripy.BVS('strlen_ret',32)defsolve():""" 13_angr_static_binary 解题脚本 关键：静态库函数在二进制内部，需要 hook 简化执行 """# 加载静态链接二进制 p = angr.Project('./13_angr_static_binary', auto_load_libs=False)
# 从 main 函数开始，跳过 _start 的库初始化 init_state = p.factory.entry_state()
# Hook strlen 函数地址（通过 objdump 获取）# 0x4013b0 是静态编译后的 strlen 入口 strlen_addr =0x4013b0 p.hook(strlen_addr, StrlenHook(), length=5)
# 定义成功路径：输出 "Good Job."defgood(state):
returnb'Good Job.'instate.posix.dumps(1)
# 定义失败路径：输出 "Try again."defbad(state):
returnb'Try again.'instate.posix.dumps(1)
# 创建模拟管理器 simgr = p.factory.simgr(init_state)
# 探索路径 simgr.explore(find=good, avoid=bad)ifsimgr.found: solution_state = simgr.found[0]# 求解 stdin 输入 solution = solution_state.posix.dumps(0).decode()print(f"Solution:{solution}")if__name__ =='__main__': solve()
importangrimportclaripydefsolve():""" 14_angr_shared_library 解题脚本 关键：加载共享库，直接在库函数入口执行 """# 加载主程序 p = angr.Project('./14_angr_shared_library', auto_load_libs=False)
# 手动加载共享库
# 注意：需要确保 lib14_angr_shared_library.so 在当前目录 lib = angr.Project('./lib14_angr_shared_library.so', auto_load_libs=False)
# 创建初始状态，从库函数 validate 入口开始
# 0x1234 是库函数 validate 的入口（通过 objdump 获取） validate_addr =0x1234 state = lib.factory.blank_state(addr=validate_addr)
# 符号化函数参数（char* buffer） buffer_addr =0x1000
# 选择一个未使用的内存地址 sym_buffer = claripy.BVS('buffer',8*16) state.memory.store(buffer_addr, sym_buffer)
# 设置函数参数
# x86 调用约定：参数在栈上 state.regs.eax = buffer_addr
# 定义成功条件：库函数返回 0（验证通过）defgood(state):
returnstate.regs.eax ==0defbad(state):
returnstate.regs.eax !=0
# 创建模拟管理器 simgr = lib.factory.simgr(state)
# 探索 simgr.explore(find=good, avoid=bad)ifsimgr.found: solution_state = simgr.found[0]# 求解 buffer solution = solution_state.solver.eval(sym_buffer, cast_to=bytes)print(f"Solution:{solution}")if__name__ =='__main__': solve()
importangrimportclaripydefsolve():""" 15_angr_arbitrary_read 解题脚本 关键：利用格式化字符串漏洞读取内存，找到 secret 字符串 """ p = angr.Project('./15_angr_arbitrary_read', auto_load_libs=False) init_state = p.factory.entry_state()
# scanf 会读取格式化字符串，我们需要构造 payload
# payload 格式："%<offset>$s" 读取 stack[offset] 指向的字符串
# 符号化输入：假设我们知道 secret 在 stack 的第 7 个位置
# payload = "%7$s" + padding payload = claripy.BVS('payload',8*20)
# 约束 payload 格式：以 %7$s 开头 init_state.solver.add(payload.get_byte(0) ==ord('%')) init_state.solver.add(payload.get_byte(1) ==ord('7')) init_state.solver.add(payload.get_byte(2) ==ord('$')) init_state.solver.add(payload.get_byte(3) ==ord('s'))
# 将 payload 存入 stdin init_state.memory.store(init_state.posix.stdin.addr, payload)defgood(state):
returnb'Good'instate.posix.dumps(1)defbad(state):
returnb'Try'instate.posix.dumps(1) simgr = p.factory.simgr(init_state) simgr.explore(find=good, avoid=bad)ifsimgr.found: solution_state = simgr.found[0]# 求解 payload solution = solution_state.solver.eval(payload, cast_to=bytes)print(f"Solution:{solution}")if__name__ =='__main__': solve()
importangrimportclaripydefsolve():""" 16_angr_arbitrary_write 解题脚本 关键：利用栈溢出覆盖返回地址，劫持控制流 """ p = angr.Project('./16_angr_arbitrary_write', auto_load_libs=False) init_state = p.factory.entry_state()
# scanf 会读取输入到栈上，需要构造 payload 覆盖返回地址
# payload 结构：[填充数据] + [secret_function 地址]# 符号化输入（假设需要 64 字节覆盖到返回地址） payload = claripy.BVS('payload',8*64)
# secret_function 地址（通过 objdump 获取） secret_addr =0x08048456
# 约束 payload 的最后 4 字节为 secret_addr（小端序）fori, byteinenumerate(secret_addr.to_bytes(4,'little')): init_state.solver.add(payload.get_byte(60+ i) == byte)
# 将 payload 存入 stdin init_state.memory.store(init_state.posix.stdin.addr, payload)
# 成功条件：程序执行到 secret_function
# 0x08048456 是 secret_function 入口 simgr = p.factory.simgr(init_state) simgr.explore(find=0x08048456)ifsimgr.found: solution_state = simgr.found[0]# 求解 payload solution = solution_state.solver.eval(payload, cast_to=bytes)print(f"Solution:{solution.hex()}")if__name__ =='__main__': solve()
importangrimportclaripydefsolve():""" 17_angr_arbitrary_jump 解题脚本 关键：利用漏洞直接设置程序计数器（PC） """ p = angr.Project('./17_angr_arbitrary_jump', auto_load_libs=False) init_state = p.factory.entry_state()
# 程序会读取一个地址字符串并跳转到该地址
# 我们需要提供 secret_function 的地址
# 符号化输入（地址字符串） input_addr = claripy.BVS('input_addr',8*10)
# secret_function 地址（通过 objdump 获取） secret_addr =0x08048456
# 约束输入地址等于 secret_addr 的字符串表示
# 例如：0x08048456 -> "08048456" secret_str =f"{secret_addr:x}"fori, charinenumerate(secret_str): init_state.solver.add(input_addr.get_byte(i) ==ord(char))
# 将输入存入 stdin init_state.memory.store(init_state.posix.stdin.addr, input_addr)
# 成功条件：程序跳转到 secret_function
# 0x08048456 是 secret_function 入口 simgr = p.factory.simgr(init_state) simgr.explore(find=0x08048456)ifsimgr.found: solution_state = simgr.found[0]# 求解输入 solution = solution_state.solver.eval(input_addr, cast_to=bytes).decode()print(f"Solution:{solution}")if__name__ =='__main__': solve()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016300-wxsync-2025-12-6a35bda543c0c127e8ee613b23b8d1ab.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016302-wxsync-2025-12-b989c26b117a5d2e4dd3c14a812db5f0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016304-wxsync-2025-12-c65573c64349c6909db898e27d0a968e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016306-wxsync-2025-12-4ae2ba62fc44b7415dcd6c8786ae64df.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016307-wxsync-2025-12-0485891c80eacdbeb90a59fbd424c531.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016309-wxsync-2025-12-630d57dd8e336f6c2885d7a2b332a8e0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016310-wxsync-2025-12-f9e6db81267e589b383366af1b639411.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016312-wxsync-2025-12-4237352a20037c77bc24461ba72402ba.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016314-wxsync-2025-12-bbcc7297c971a8ec57a70250a182a8e9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/12/1765016315-wxsync-2025-12-abf840d5d2e54b4e626caffb51465ac2.png)