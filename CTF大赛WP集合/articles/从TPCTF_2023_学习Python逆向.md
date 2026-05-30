# 从TPCTF 2023 学习Python逆向

> 原文: https://www.ctfiot.com/149063.html
> ID: 149063

TPCTF 2023 由清华大学 Redbud 战队与北京大学 pkucc 战队联合命题。周末没打到，赛后看了下 Reverse 方向有两个 Python +二进制的逆向题，发现居然不是纯套路题，出题人还是很用心地准备了一些新颖的知识点，故记录于此。‍

1

nanoPyEnc

2

maze


```
from Crypto.Cipher import AES

enc = [153, 240, 237, 199, 63, 44, 237, 45, 25, 47, 97, 154, 158, 112, 46, 176, 219, 247, 44, 115, 169, 124, 64, 63, 121, 253, 250, 137, 34, 144, 33, 17, 182, 9, 16, 247, 249, 41, 165, 114, 87, 231, 222, 242, 126, 30, 124, 237]
enc = bytes([x ^ 1 for x in enc])
key = b'2033-05-18_03:33'
aes = AES.new(key, AES.MODE_ECB)
flag = aes.decrypt(enc)
print(flag)
```



```
ys = ['PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyTypeObject *', 'PyTypeObject *', 'PyTypeObject *', 'PyTypeObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *', 'PyObject *']
ns = ['__pyx_d', '__pyx_b', '__pyx_cython_runtime', '__pyx_empty_tuple', '__pyx_empty_bytes', '__pyx_empty_unicode', '__pyx_CyFunctionType', '__pyx_GeneratorType', '__pyx_ptype_4maze___pyx_scope_struct__YWRkX2Z1bmN0aW9u', '__pyx_ptype_4maze___pyx_scope_struct_1_genexpr', '__pyx_kp_u_', '__pyx_kp_u_0_9', '__pyx_kp_u_0_9_2', '__pyx_kp_u_0_9_2_2', '__pyx_kp_u_A_Za_z0_9', '__pyx_kp_u_A_Za_z0_9_2', '__pyx_kp_u_A_Za_z_A_Za_z0_9', '__pyx_n_s_AttributeError', '__pyx_kp_u_Congratulations_You_got_the_flag', '__pyx_n_u_D', '__pyx_n_u_Dd', '__pyx_n_s_EqdU3uQNCi', '__pyx_kp_u_Error_Car_is_in_wall_accidentall', '__pyx_kp_u_Error_Input_is_empty', '__pyx_kp_u_Error_Multiple_cars_in_same_cell', '__pyx_kp_u_Failed_please_try_again', '__pyx_kp_u_Invalid_ELSE_statement', '__pyx_kp_u_Invalid_THEN_keyword', '__pyx_kp_u_Invalid_THEN_statement', '__pyx_kp_u_Invalid_assignment_value', '__pyx_kp_u_Invalid_condition', '__pyx_kp_u_Invalid_function', '__pyx_kp_u_Invalid_function_name', '__pyx_kp_u_Invalid_operator', '__pyx_kp_u_Invalid_value_for_condition', '__pyx_kp_u_Invalid_value_for_operator', '__pyx_kp_u_Invalid_value_for_signal', '__pyx_kp_u_IyMgIyMgIyMgIyMgIyMgIyMgIyMKIyMg', '__pyx_n_s_JfH9kFlbcd', '__pyx_n_u_L', '__pyx_kp_u_LRUDNlrudn', '__pyx_n_u_Ll', '__pyx_n_u_Nn', '__pyx_n_u_None', '__pyx_kp_u_Please_input_the_flag', '__pyx_n_s_Q2Fy', '__pyx_n_s_Q2Fy___init', '__pyx_n_s_Q2Fy___repr', '__pyx_n_s_Q2VsbA', '__pyx_n_s_Q2VsbA___init', '__pyx_n_s_Q2VsbA___repr', '__pyx_n_u_R', '__pyx_n_u_Rr', '__pyx_n_s_SvL6VEBRwx', '__pyx_n_s_TWF6ZUxhbmc', '__pyx_n_s_TWF6ZUxhbmc_YWRkX2NlbGw', '__pyx_n_s_TWF6ZUxhbmc_YWRkX2Z1bmN0aW9u', '__pyx_n_s_TWF6ZUxhbmc_YWRkX2Z1bmN0aW9u_loc', '__pyx_n_s_TWF6ZUxhbmc_Z2V0X2NlbGw', '__pyx_n_s_TWF6ZUxhbmc_Z2V0X2NlbGw_locals_l', '__pyx_n_s_TWF6ZUxhbmc_Z2V0X3Bvcw', '__pyx_n_s_TWF6ZUxhbmc___init', '__pyx_n_s_TWF6ZUxhbmc_aW5pdA', '__pyx_n_s_TWF6ZUxhbmc_b3Bw', '__pyx_n_s_TWF6ZUxhbmc_c3RlcA', '__pyx_n_s_TWF6ZUxhbmc_c3RlcA_locals_genexp', '__pyx_n_s_TWF6ZUxhbmc_cnVuX3RpbGxfb3V0cHV0', '__pyx_n_s_TypeError', '__pyx_n_u_U', '__pyx_n_s_UJ9mxXxeoS', '__pyx_n_u_Uu', '__pyx_n_s_ValueError', '__pyx_kp_u_Welcome_to_the_world_of_Maze', '__pyx_n_s_YWRkX2NlbGw', '__pyx_n_s_YWRkX2Z1bmN0aW9u', '__pyx_n_s_Z2V0X2NlbGw', '__pyx_n_s_Z2V0X3Bvcw', '__pyx_kp_u__10', '__pyx_kp_u__11', '__pyx_kp_u__12', '__pyx_kp_u__13', '__pyx_kp_u__14', '__pyx_kp_u__15', '__pyx_kp_u__16', '__pyx_kp_u__17', '__pyx_kp_u__18', '__pyx_kp_u__19', '__pyx_kp_u__2', '__pyx_kp_u__20', '__pyx_kp_u__25', '__pyx_kp_u__3', '__pyx_kp_u__30', '__pyx_kp_u__31', '__pyx_kp_u__32', '__pyx_kp_u__33', '__pyx_kp_u__34', '__pyx_kp_u__35', '__pyx_kp_u__36', '__pyx_kp_u__37', '__pyx_kp_u__38', '__pyx_kp_u__4', '__pyx_n_s__5', '__pyx_kp_u__5', '__pyx_n_s__69', '__pyx_kp_u__7', '__pyx_kp_u__8', '__pyx_kp_u__9', '__pyx_n_s_aW5pdA', '__pyx_n_s_aW5pdF9zZWNyZXQ', '__pyx_n_s_append', '__pyx_n_s_args', '__pyx_n_s_assign', '__pyx_n_s_asyncio_coroutines', '__pyx_n_s_b3Bw', '__pyx_n_s_b64decode', '__pyx_n_s_base64', '__pyx_n_s_bxKGKlj99G', '__pyx_n_s_c29sdmU', '__pyx_n_s_c2VjcmV0', '__pyx_n_s_c3RlcA', '__pyx_n_s_car', '__pyx_n_s_car_c', '__pyx_n_s_car_n', '__pyx_n_s_cars', '__pyx_n_s_cell', '__pyx_n_s_cell_line', '__pyx_n_s_cells', '__pyx_n_s_class_getitem', '__pyx_n_s_cline_in_traceback', '__pyx_n_s_close', '__pyx_n_s_cnVuX3RpbGxfb3V0cHV0', '__pyx_n_s_code', '__pyx_n_s_collections', '__pyx_n_s_condition', '__pyx_n_s_copy', '__pyx_n_s_d', '__pyx_n_s_decode', '__pyx_n_s_deepcopy', '__pyx_n_s_deque', '__pyx_n_s_dict', '__pyx_n_s_direction', '__pyx_n_u_direction', '__pyx_n_s_directions', '__pyx_kp_u_disable', '__pyx_n_s_doc', '__pyx_kp_u_else', '__pyx_n_s_else_2', '__pyx_kp_u_enable', '__pyx_n_s_end', '__pyx_n_s_enumerate', '__pyx_n_s_exit', '__pyx_n_s_function', '__pyx_n_u_function', '__pyx_n_s_functions', '__pyx_kp_u_gc', '__pyx_n_s_genexpr', '__pyx_n_s_group', '__pyx_n_u_hole', '__pyx_n_s_i', '__pyx_n_u_if', '__pyx_n_s_import', '__pyx_n_u_in', '__pyx_n_s_init', '__pyx_n_s_init_subclass', '__pyx_n_s_initializing', '__pyx_n_s_input', '__pyx_n_s_int', '__pyx_n_s_int_match', '__pyx_n_s_is_coroutine', '__pyx_kp_u_isenabled', '__pyx_n_s_items', '__pyx_n_s_k', '__pyx_n_s_key', '__pyx_n_s_line', '__pyx_n_s_lower', '__pyx_n_s_main', '__pyx_n_s_match', '__pyx_n_s_matches', '__pyx_n_s_maze', '__pyx_kp_s_maze_py', '__pyx_n_s_metaclass', '__pyx_n_s_min', '__pyx_n_s_module', '__pyx_kp_u_n', '__pyx_n_s_name', '__pyx_n_s_name_2', '__pyx_n_s_number', '__pyx_kp_u_one_use', '__pyx_n_s_operator', '__pyx_n_u_out', '__pyx_n_s_output', '__pyx_n_u_path', '__pyx_n_s_pattern', '__pyx_n_s_pause', '__pyx_n_u_pause', '__pyx_n_s_popleft', '__pyx_n_s_pos', '__pyx_n_s_prepare', '__pyx_n_s_print', '__pyx_n_s_qualname', '__pyx_n_s_quotes', '__pyx_n_s_range', '__pyx_n_s_re', '__pyx_n_s_regexes', '__pyx_n_s_remove', '__pyx_n_s_removed', '__pyx_n_s_repr', '__pyx_n_s_result', '__pyx_n_s_return', '__pyx_n_s_row', '__pyx_n_s_run', '__pyx_n_s_search', '__pyx_n_s_self', '__pyx_n_s_send', '__pyx_n_s_set_name', '__pyx_n_s_signal', '__pyx_n_u_signal', '__pyx_n_s_signals', '__pyx_n_s_spec', '__pyx_n_s_split', '__pyx_n_s_splitlines', '__pyx_n_u_splitter', '__pyx_n_s_start', '__pyx_n_u_start', '__pyx_n_s_startswith', '__pyx_n_s_str_match', '__pyx_n_s_string', '__pyx_n_s_super', '__pyx_n_s_sys', '__pyx_n_s_test', '__pyx_kp_u_then', '__pyx_n_s_then_2', '__pyx_n_s_then_keywd', '__pyx_n_s_throw', '__pyx_n_s_time', '__pyx_n_s_upper', '__pyx_n_s_value', '__pyx_n_u_wall', '__pyx_n_s_x', '__pyx_n_s_y', '__pyx_int_0', '__pyx_int_1', '__pyx_int_2', '__pyx_int_3', '__pyx_int_4', '__pyx_int_5', '__pyx_int_6', '__pyx_int_7', '__pyx_int_8', '__pyx_int_9', '__pyx_int_10', '__pyx_int_11', '__pyx_int_12', '__pyx_int_13', '__pyx_int_14', '__pyx_int_15', '__pyx_int_16', '__pyx_int_17', '__pyx_int_18', '__pyx_int_19', '__pyx_int_20', '__pyx_int_21', '__pyx_int_22', '__pyx_int_23', '__pyx_int_24', '__pyx_int_25', '__pyx_int_26', '__pyx_int_27', '__pyx_int_28', '__pyx_int_29', '__pyx_int_30', '__pyx_int_31', '__pyx_int_32', '__pyx_int_36', '__pyx_int_37', '__pyx_int_38', '__pyx_int_39', '__pyx_int_40', '__pyx_int_47', '__pyx_int_49', '__pyx_int_60', '__pyx_int_61', '__pyx_int_62', '__pyx_int_63', '__pyx_int_102', '__pyx_int_112', '__pyx_int_neg_1', '__pyx_slice__6', '__pyx_tuple__21', '__pyx_tuple__22', '__pyx_tuple__23', '__pyx_tuple__24', '__pyx_tuple__26', '__pyx_tuple__27', '__pyx_tuple__28', '__pyx_tuple__29', '__pyx_tuple__39', '__pyx_tuple__41', '__pyx_tuple__43', '__pyx_tuple__46', '__pyx_tuple__48', '__pyx_tuple__50', '__pyx_tuple__52', '__pyx_tuple__54', '__pyx_tuple__56', '__pyx_tuple__58', '__pyx_tuple__60', '__pyx_tuple__63', '__pyx_tuple__65', '__pyx_tuple__67', '__pyx_codeobj__40', '__pyx_codeobj__42', '__pyx_codeobj__44', '__pyx_codeobj__45', '__pyx_codeobj__47', '__pyx_codeobj__49', '__pyx_codeobj__51', '__pyx_codeobj__53', '__pyx_codeobj__55', '__pyx_codeobj__57', '__pyx_codeobj__59', '__pyx_codeobj__61', '__pyx_codeobj__62', '__pyx_codeobj__64', '__pyx_codeobj__66', '__pyx_codeobj__68']

base = 0x44960
for i in range(len(ns)):
    create_qword(base+i*8)
    SetType(base+i*8, ys[i])
    set_name(base+i*8, ns[i], SN_CHECK)
```



```
print("Welcome to the world of Maze!")
```



```
def c29sdmU(SvL6VEBRwx):
    MazeLang = TWF6ZUxhbmc(base64.b64decode(UJ9mxXxeoS).decode()) # 自己起的变量名，如确实需追溯则应该看函数定义时的tuple
    if len(SvL6VEBRwx) != 33:
        return 1
    aW5pdF9zZWNyZXQ()
    for i in range(33):
        if SvL6VEBRwx[i] ^ MazeLang.cnVuX3RpbGxfb3V0cHV0() != c2VjcmV0[i]:
            return 1
    return 0
```



```
def aW5pdF9zZWNyZXQ():
    for i in range(33):
        c2VjcmV0[EqdU3uQNCi[i]], c2VjcmV0[i] = c2VjcmV0[i], c2VjcmV0[EqdU3uQNCi[i]]
```



```
EqdU3uQNCi = [18, 17, 15, 0, 27, 31, 10, 19, 14, 21, 25, 22, 6, 3, 30, 8, 24, 5, 7, 4, 13, 29, 9, 26, 1, 2, 28, 16, 20, 32, 12, 23, 11]
c2VjcmV0 = [7, 47, 60, 28, 39, 11, 23, 5, 49, 49, 26, 11, 63, 4, 9, 2, 25, 61, 36, 112, 25, 15, 62, 25, 3, 16, 102, 38, 14, 7, 37, 4, 40]

def aW5pdF9zZWNyZXQ():
    for i in range(33):
        c2VjcmV0[EqdU3uQNCi[i]], c2VjcmV0[i] = c2VjcmV0[i], c2VjcmV0[EqdU3uQNCi[i]]

key = b'HITPCTF'
flag = []
aW5pdF9zZWNyZXQ()
for i in range(33):
    flag.append(key[i%7] ^ c2VjcmV0[i])
print(bytes(flag))
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1701663767.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1701663768.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/1-1701663768.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/8-1701663769.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1701663770.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/4-1701663771.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1701663771.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1701663772.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/5-1701663773.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1701663774.png)