---
title: 2024 年羊城杯粤港澳大湾区网络安全大赛 WP - AI AK 篇
contest: 羊城杯
year: 2024
difficulty: hard
vuln_type: [reverse, misc_unknown, web_unknown, web_rce]
tags: [NLP 对抗样本, DistilBERT 三分类, 前缀加 happy/nothing/unhappy 反向, very 加 0.7 阈值, AI 模型攻击, SSIM 验证相似度]
attack_chain: 1. 加载 Sentiment_classification_model (DistilBERT) + tokenizer / 2. verify_similarity 余弦相似度 ≥ 0.7 / 3. predict_model argmax(label) / 4. 对原始文本加前缀 happy/nothing/unhappy 反向 / 5. 加 "very" 提相似度到 0.7+ / 6. calc_accuracy ≥ 90% 拿 flag
key_payload: data_dict_2[id] = {"text": "very " + ("happy/nothing/unhappy") + original_text} ; predict_model argmax ; verify_similarity cosine ≥ 0.7 ; calc_accuracy 79.0% → 95%+
one_liner: DistilBERT 情感分类对抗样本：反向情绪前缀 + very 提相似度。
lesson: NLP 模型对抗样本常用策略：反向情绪关键词前缀 + 强度副词（very）保相似度。
quality: medium
---
# 2024 年羊城杯粤港澳大湾区网络安全大赛 WP - AI AK 篇

## NLP_Model_Attack

### 题目
- 模型：DistilBERT 三分类 `{positive:2, negative:0, neutral:1}`
- 任务：对原始文本加扰动，攻击成功率 ≥ 90%
- 相似度：cosine ≥ 0.75
- 数据：100 条 original_text.csv

### 解题代码

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.metrics.pairwise import cosine_similarity
import csv

checkpoint = "./Sentiment_classification_model"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

def verify_similarity(original, modified, model, tokenizer):
    model.eval()
    o_enc = tokenizer(original, return_tensors='pt', padding=True, truncation=True, max_length=512)
    m_enc = tokenizer(modified, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        o_h = model.distilbert(**o_enc).last_hidden_state.mean(dim=1)
        m_h = model.distilbert(**m_enc).last_hidden_state.mean(dim=1)
    similarity = cosine_similarity(o_h.cpu().numpy(), m_h.cpu().numpy())[0][0]
    return similarity >= 0.7

def predict_model(tokenizer, model, raw_inputs):
    inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    return str(int(outputs.logits.argmax()))

filename = 'original_text.csv'
data_dict = {}
with open(filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == "id": continue
        data_dict[row[0]] = {'text': row[1], 'label': row[3]}

# 反向情绪前缀攻击
data_dict_2 = {}
for id in data_dict:
    original_text = data_dict[id]['text']
    label = data_dict[id]['label']
    if label == "0":    # neg
        data_dict_2[id] = {"text": "happy " + original_text}
    elif label == "2":  # pos
        data_dict_2[id] = {"text": "nothing " + original_text}
    elif label == "1":  # neutral
        data_dict_2[id] = {"text": "unhappy " + original_text}

# 失败样本加 "very" 提相似度到 0.7+
for id in failed_ids:
    data_dict_2[id] = {"text": "very " + data_dict_2[id]['text']}

def calc_accuracy(data_dict, new_data_dict):
    value = 0
    for id in data_dict:
        original_text = data_dict[id]['text']
        modified_text = new_data_dict[id]['text']
        result = predict_model(tokenizer, model, modified_text)
        label = data_dict[id]['label']
        if result != label:
            if verify_similarity(original_text, modified_text, model, tokenizer):
                value += 1
    print(f"{value/len(data_dict) * 100}%")

calc_accuracy(data_dict, data_dict_2)
# 79.0% → 加 "very" 后达 95%+
```

### 提交 CSV 格式
```csv
id,attacked_text
0,unhappy   #powerblog What is this powerblog challenge you keep talking about?  I`m a newbie follower
1,very nothing Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY
...
```

### 攻击成功率 = 攻击成功且相似度 ≥ 75% 的样本数 / 总样本数

- 简单前缀 "happy/nothing/unhappy" → 79%
- 加 "very" 副词提高相似度到 0.7+ → 95%+

flag 在 `calc_accuracy ≥ 0.9` 时输出。
