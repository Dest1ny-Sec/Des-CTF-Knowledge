# 2024年羊城杯粤港澳大湾区网络安全大赛WP-AI AK篇

> 原文: https://www.ctfiot.com/203028.html
> ID: 203028

NLP_Model_Attack

题目名称：NLP_Model_Attack

题目内容：详情阅读readme.md

题目难度：中等

readme

题目描述:

在这个赛题中，我们将提供一个预训练好的positive、negative、neutral文本识别模型以及一组包含这三类的文本数据集。

参赛选手的任务是： 对这些文本增加微小的扰动，生成攻击文本，使得模型在预测这些经过扰动的攻击文本时出现预测错误。

选手需要设计一种算法，在不明显改变文本语义的前提下，对文本添加微小扰动（同义词替换或者其他方式），使得提供的三分类positive、negative、neutral文本识别模型在预测扰动文本时出现错误。例如，将原本能够正确识别为positive的文本进行扰动后，模型会将其错误地分类为非positive的类别。

为了量化扰动的程度，我们将使用修改后的攻击文本与原始文本的相似度作为评判标准。我们会计算每个扰动文本与其对应原始文本的语义相似性。如果修改后的扰动文本与原文本的相似度低于75%，则认为扰动过大，该攻击样本将不被视为有效的对抗性样本。

对于满足相似度条件的图像，我们将使用提供的识别模型进行预测。如果可以成功欺骗模型，使其输出错误的模型预测结果，则视为一次成功的攻击，选手将获得 1 分。选手需要在成功攻击至少90%的样本，即产生至少90%满足相似度条件且能够成功欺骗模型的对抗性样本，才能获得题目的 flag。

相似性的计算：

相似性的计算流程：

原始文本和修改后的文本被输入到 tokenizer 中，进行编码。编码的结果是将文本转换为模型可接受的输入形式（即张量），并且对这些输入进行填充和截断以确保统一的长度。

代码分别对原始文本和修改后的文本通过模型进行前向传播（forward pass），获取它们的隐藏状态。隐藏状态是由模型内部特定层（在这里是最后一层）生成的向量表示，用于表示输入文本的语义信息。隐藏状态的向量经过平均池化（mean pooling），压缩成一个定长的向量。

参考代码：

def verify_similarity(original, modified, model, tokenizer):
    # 确保模型处于评估模式
    model.eval()

    # 对原始文本和修改后的文本进行编码
    original_encoding = tokenizer(original, return_tensors='pt', padding=True, truncation=True, max_length=512)
    modified_encoding = tokenizer(modified, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        # 获取原始文本的隐藏状态
        original_outputs = model.distilbert(**original_encoding)
        original_hidden_state = original_outputs.last_hidden_state.mean(dim=1)

        # 获取修改后文本的隐藏状态
        modified_outputs = model.distilbert(**modified_encoding)
        modified_hidden_state = modified_outputs.last_hidden_state.mean(dim=1)

    # 计算余弦相似度
    similarity = cosine_similarity(original_hidden_state.cpu().numpy(),
                                modified_hidden_state.cpu().numpy())[0][0]

    return similarity

数据和模型：

发放的数据中包含文本文件original_text.csv和 预训练模型 Sentiment_classification_model。

模型的 label 映射: {'positive':2,'negative':0,'neutral':1}

可以使用 transformers 模块中的 AutoTokenizer、AutoModelForSequenceClassification 分别加载 tokenizer 和 model。

提交要求：

选手需要把增加扰动后得到的新文本(攻击文本)，按照规定的格式进行上传提交（csv文件），格式如下，保留原id列：

id
attacked_text

0
#powerblog What is this powerblog challenge you keep talking about?  I`m a newbie follower

1
Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY

相似度：

生成的对抗文本和原始文本之间的相似度需要在 75% 以内。

攻击成功率：

攻击成功率达到 90%（即生成的对抗样本中有 90% 能够欺骗模型并满足相似度要求）。

成功满足上述条件即可获取比赛的 flag。

Write up

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.metrics.pairwise import cosine_similarity
import csv
# sentiment-analysis 默认使用的 checkpoint
checkpoint = "./Sentiment_classification_model"

# 建立 tokenizer，加载模型的 checkpoint，建立 model 对象实例
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
def verify_similarity(original, modified, model, tokenizer):
    # 确保模型处于评估模式
    model.eval()

    # 对原始文本和修改后的文本进行编码
    original_encoding = tokenizer(original, return_tensors='pt', padding=True, truncation=True, max_length=512)
    modified_encoding = tokenizer(modified, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        # 获取原始文本的隐藏状态
        original_outputs = model.distilbert(**original_encoding)
        original_hidden_state = original_outputs.last_hidden_state.mean(dim=1)

        # 获取修改后文本的隐藏状态
        modified_outputs = model.distilbert(**modified_encoding)
        modified_hidden_state = modified_outputs.last_hidden_state.mean(dim=1)

    # 计算余弦相似度
    similarity = cosine_similarity(original_hidden_state.cpu().numpy(),
                                modified_hidden_state.cpu().numpy())[0][0]
    if similarity < 0.7:
        return False
    else:
        return True
    # return similarity
def predict_model(tokenizer,model,raw_inputs):
    # 原始输入序列
    # raw_inputs = ["Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY"]
    
    # 调用 Tokenizer 进行预处理，预处理的结果会作为 Model 的输入
    inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
    # encoded_input = tokenizer(sentence, return_tensors='pt')
    
    
    # 将 Tokenizer 预处理后的数据传送给 Model，“**”用于将 inputs 字典中的键值对解包成模型的输入参数
    outputs = model(**inputs)
    
    # 打印一下 Transformer 输出的 Logits 的结构信息
    # print(outputs.logits.shape)
    
    # 打印一下 Transformer 输出的 Logits 的信息
    # print(outputs.logits)
    predictions = outputs.logits
    
    # 解析预测结果
    # 假设模型有两个类别：0 表示负面，1 表示正面
    # if predictions.argmax() == 0:
    #     print("该句子情感为负面")
    # elif predictions.argmax() == 1:
    #     print("该句子情感为无所谓")
    # elif predictions.argmax() == 2:
    #     print("该句子情感为正面")
    # return str(predictions.argmax())
    return str(int(predictions.argmax()))
 
 
filename = 'original_text.csv'
data_dict = {}
with open(filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == "id":
            continue
        data_dict[row[0]] = {'text':
row[1],'label':
row[3]}
        
data_dict_2 = {}
for id in data_dict:
    original_text = data_dict[id]['text']
    label = data_dict[id]['label']
    if label == "0": #neg
        data_dict_2[id] = {"text":"happy " + original_text}
    elif label == "2":
        data_dict_2[id] = {"text":"nothing " + original_text}
    elif label == "1": #pos
        data_dict_2[id] = {"text":"unhappy " + original_text}

def calc_accuracy(data_dict,new_data_dict):
    value = 0
    for id in data_dict:
        original_text = data_dict[id]['text']
        modified_text = new_data_dict[id]['text']
        result = predict_model(tokenizer,model,modified_text)
        label = data_dict[id]['label']
        if result != label:
            if verify_similarity(original_text, modified_text, model, tokenizer):
                value += 1
        else:
            pass
    print(f"{value/len(data_dict) * 100}%")

calc_accuracy(data_dict,data_dict_2)

pre_failed 1 2 nothing Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY
pre_failed 2 0 happy  im only on 1800  lol
pre_failed 3 2 nothing was busy talking with mom and bhabhi.. they liked the cards bro and me made for them  now waiting for sis to get back from Church..
pre_failed 11 0 happy  Nothing definite yet..and the show is in a week   I may just be resorted to giving them away
pre_failed 13 0 happy forgot my macbook`s recharger, that means nothing but Pratchett for me today
pre_failed 16 2 nothing  Stress test: http://www.selfhelpmagazine.com/psychtoons/glasbergen/StressManagement/StressTest.gif  Good luck!
pre_failed 20 0 happy _G  ur a poopy head
pre_failed 21 2 nothing  aww you poor thing  hope all goes well!
pre_failed 24 0 happy http://www.myspace.com/dica_grl Just got a crush on this song! Disco`s Out! Murder`s In! ruleaz?, zic!  www.myspace.com/discosoutmurdersin
pre_failed 28 0 happy 2nd to last episode of jay leno  itll never be the same!  nite twitter
pre_failed 36 2 nothing Nice PC Authority review of the Tivo VOD service here: http://bit.ly/Ps7y2  I`m still loving my Tivo
pre_failed 37 2 nothing - It`s time for Kathleen to go to bed... waaaaay past time. Don`t expect to hear from me before noon. lol  Have a BLESSED morning.
pre_failed 38 2 nothing Am good thanks, what`s Miami saying? How come u wrote to me?
pre_failed 43 0 happy I wanna go to the beach...but I have to study
pre_failed 48 0 happy  Don`t leave forever! We`ll miss you too much
pre_failed 50 2 nothing  bugger, that would have been nice but typically, we`re heading to Bristol
pre_failed 51 0 happy _0 have you considered cordoning off a corner of the park with beware 'Swine flu' signs might clear it out for you
pre_failed 58 2 nothing Had a nice pre mother`s day dinner out. Now a cocktail before retiring for the evening
ver_failed 59 0 happy   well hit me and we can see...it depends then
pre_failed 66 2 nothing Last Late Late with Pat Kenny! Bless
pre_failed 67 1 unhappy Checked if there`s a new comment on friendster!
pre_failed 76 2 nothing  hahaha wow thanks bud :p but my plan is to pretend its a costume... I wish it were cold so i could wear a sweatshirt over this
pre_failed 79 0 happy off to go buy more deck sleeves and 3X3 card pages.  Man, those pages are expensive!   Stupid organizing collection.
pre_failed 82 0 happy It`s 6 am, I haven`t been to bed yet, and I just got my second wind.  Guess I should edit or read or something until I feel tired huh?
pre_failed 84 2 nothing  no way - those are great words.  Boys don`t get to own them.    Oh and was it your bday?
pre_failed 91 1 unhappy Heyya guys! does anyone know how to give formulas to create a sudoku? Please help
pre_failed 93 2 nothing  y r we giving up on people?  I actually thought that way for a while too before I found someone who is very intriguing
pre_failed 95 2 nothing  Oh! Don`t you just love these Vodafone series of Ads ... The best picturisation ever
pre_failed 96 0 happy  or so a month. I put my 2 week`s notice in a little over a week ago, my last day is this friday!
pre_failed 97 0 happy recorded some of a new song today! u wont hear it for a long time thooo... we might play it at shows tho! so comeeeeee
pre_failed 98 2 nothing Heading home after a long week. Wish someone onther than marketers would follow me

data_dict_2 = {}
for id in data_dict:
    original_text = data_dict[id]['text']
    label = data_dict[id]['label']
    if label == "0": #neg
        data_dict_2[id] = {"text":"happy " + original_text}
    elif label == "2":
        data_dict_2[id] = {"text":"nothing " + original_text}
    elif label == "1": #pos
        data_dict_2[id] = {"text":"unhappy " + original_text}
    if id in ["1","2","3","11","13","16","20","21","24","28","36","37","38","43","48","50","51","58","59","66","67","76","79","82","84","91","93","95","96","97","98"]:
        data_dict_2[id] = {"text":"very " + data_dict_2[id]['text']}
calc_accuracy(data_dict,data_dict_2)

pre_failed 1 2 very nothing Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY
ver_failed 2 0 very happy im only on 1800 lol
pre_failed 3 2 very nothing was busy talking with mom and bhabhi.. they liked the cards bro and me made for them now waiting for sis to get back from Church..
pre_failed 11 0 very happy Nothing definite yet..and the show is in a week I may just be resorted to giving them away
pre_failed 16 2 very nothing Stress test: http://www.selfhelpmagazine.com/psychtoons/glasbergen/StressManagement/StressTest.gif Good luck!
ver_failed 20 0 very happy _G ur a poopy head
pre_failed 21 2 very nothing aww you poor thing hope all goes well!
pre_failed 36 2 very nothing Nice PC Authority review of the Tivo VOD service here: http://bit.ly/Ps7y2 I`m still loving my Tivo
pre_failed 37 2 very nothing - It`s time for Kathleen to go to bed... waaaaay past time. Don`t expect to hear from me before noon. lol Have a BLESSED morning.
pre_failed 38 2 very nothing Am good thanks, what`s Miami saying? How come u wrote to me?
pre_failed 50 2 very nothing bugger, that would have been nice but typically, we`re heading to Bristol
pre_failed 58 2 very nothing Had a nice pre mother`s day dinner out. Now a cocktail before retiring for the evening
ver_failed 59 0 very happy well hit me and we can see...it depends then
pre_failed 66 2 very nothing Last Late Late with Pat Kenny! Bless
pre_failed 76 2 very nothing hahaha wow thanks bud :p but my plan is to pretend its a costume... I wish it were cold so i could wear a sweatshirt over this
pre_failed 79 0 very happy off to go buy more deck sleeves and 3X3 card pages. Man, those pages are expensive! Stupid organizing collection.
pre_failed 84 2 very nothing no way - those are great words. Boys don`t get to own them. Oh and was it your bday?
pre_failed 93 2 very nothing y r we giving up on people? I actually thought that way for a while too before I found someone who is very intriguing
pre_failed 95 2 very nothing Oh! Don`t you just love these Vodafone series of Ads ... The best picturisation ever
pre_failed 96 0 very happy or so a month. I put my 2 week`s notice in a little over a week ago, my last day is this friday!
pre_failed 98 2 very nothing Heading home after a long week. Wish someone onther than marketers would follow me
79.0%

id
attacked_text

0

unhappy   #powerblog What is this powerblog challenge you keep talking about?  I`m a newbie follower

1

very nothing Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY

2

very happy  im only on 1800  lol

3

very nothing was busy talking with mom and bhabhi.. they liked the cards bro and me made for them  now waiting for sis to get back from Church..

4

nothing  i think in the end, remembering the poetry and feeling behind something is far more important than the name.

5

unhappy  she interviewed us on books. I was gonna say something, but she was all 'Wait, I have something to say!'

6

happy If you yelled for 8 years, 7 months and 6 days, you would have produced enough sound energy to heat one cup of coffee.

7

happy Ahh, sunshine.  Just deleted 404 spam emails from 2 days – now off to BBQ in sun  wonderful…

8

unhappy will be MIA until june 13.. finals

9

nothing  Well I asked you a few days ago and you said money was the only thing holding you back Saturday or something

10

nothing layenn down,uughh dunt feel well

11

very happy  Nothing definite yet..and the show is in a week   I may just be resorted to giving them away

12

unhappy  WASSUP BEAUTIFUL!!! FOLLOW ME!!  PEEP OUT MY NEW HIT SINGLES WWW.MYSPACE.COM/IPSOHOT I DEF. WAT U IN THE VIDEO!!

13

very happy forgot my macbook`s recharger, that means nothing but Pratchett for me today

14

nothing home sweet home? i think no! huaaaa

15

happy wow! ever notice that some twitters have thousands of followers, yet they only follow a handful (actually, less than two hands) of peeps.

16

very nothing  Stress test: http://www.selfhelpmagazine.com/psychtoons/glasbergen/StressManagement/StressTest.gif  Good luck!

17

unhappy  that`s a lot of mangoes.. haha  baka naglilihi ka ahh?? haha  joke lang carmen

18

happy has britney spears  songs all over his Desktop now

19

unhappy last day off… back to work tomorrow

20

very happy _G  ur a poopy head

21

very nothing  aww you poor thing  hope all goes well!

22

unhappy Just Returned from Huntsville. Saw Sam Houston`s grave, went to a prison museum and ate chocolate dipped strawberries

23

nothing  I`ve read good things bout it. Just not feelin it tonight. Proly finish it tomorrow, after Star Trek

24

very happy http://www.myspace.com/dica_grl Just got a crush on this song! Disco`s Out! Murder`s In! ruleaz?, zic!  www.myspace.com/discosoutmurdersin

25

unhappy  I just see the video: 'All your base are belong to us..'  WhatÃ¯Â¿Â½s going on??!

26

nothing  I guess that`s true!

27

unhappy  I would like to be able to go just to ONE of those

28

very happy 2nd to last episode of jay leno  itll never be the same!  nite twitter

29

nothing i have the adam lambert version of FEELIN GOOD in my head… i miss idol already.

30

nothing  You bet!…I`ll be there in spirit (I`m in the UK really LOL) Like the pic BTW ****  x

31

nothing Hulu Desktop looks nice but not for my region

32

nothing Went to see Priscilla Ahn last night, was amazin! so were the bands before her actually

33

happy My trip to Igbaras will be postponed to next week

34

nothing  haha  i did! many times before!

35

nothing trying to get into the groove of studying  heeelllppppp meeeeeeee

36

very nothing Nice PC Authority review of the Tivo VOD service here: http://bit.ly/Ps7y2  I`m still loving my Tivo

37

very nothing – It`s time for Kathleen to go to bed… waaaaay past time. Don`t expect to hear from me before noon. lol  Have a BLESSED morning.

38

very nothing Am good thanks, what`s Miami saying? How come u wrote to me?

39

unhappy  you should add your blog to CMF Ads

40

unhappy First steps on Twitter. Just checking

41

happy just finished some Sunday cleaning, waiting to read the next chapter of Kiyosaki`s book so i can hit a cleaner

42

happy help! anyone know if there are stores that carry blackberry trackballs? just went to verizon retailer; no luck. do not want to order one

43

very happy I wanna go to the beach…but I have to study

44

happy Just funny sitting here with external keyboard, mouse, and macbook on bed  just looks strange but it`s comfortable

45

happy Pretty sure I`m sat on the wrong train going the wrong way… Bah!

46

unhappy ___ haha im gonna follow my dreams now  well…ur dream haha im still reading over it for the 90th time  :p

47

unhappy  heyy dude, yuup thats it really hows your monday?  x

48

very happy  Don`t leave forever! We`ll miss you too much

49

nothing watching the office……… also comedy gold

50

very nothing  bugger, that would have been nice but typically, we`re heading to Bristol

51

very happy _0 have you considered cordoning off a corner of the park with beware 'Swine flu' signs might clear it out for you

52

unhappy Figuring out how this Twitter thing works

53

happy  aw i wish i could.  i have to get ready for atlanta and i have to come into work since I am behind on work

54

happy i want so bad to go to the mcfly`s concert

55

happy wishing my days off were the same days that people wanted to party.

56

unhappy  im sure he will  and if its not today, maybe it will be tomorrow..

57

nothing just contributed to economic stimulus at Wal Mart – un expected tire replacements

58

very nothing Had a nice pre mother`s day dinner out. Now a cocktail before retiring for the evening

59

very happy   well hit me and we can see…it depends then

60

nothing  i been saying that the past 2 weeks that i miss playing spades and drinkin chillin.. the good old days.. let me know baby

61

unhappy Grass mowed. I can haz playtime now? No?  says we have errands to run

62

happy just got the dreaded call from babysitter – little H has bumped her head  Sitter says she`s fine and goose egg is going down fast

63

unhappy at a auto shop getting m suv fix ugh more $   http://twitpic.com/66of2

64

happy oh my. i have to play cluedo.

65

unhappy FJGKFLD;`Sdh WHY AM I NOT AT HOMETOWN DAYS WITH MY FRIENDS.

66

very nothing Last Late Late with Pat Kenny! Bless

67

very unhappy Checked if there`s a new comment on friendster!

68

happy is disappointed to learn Newark, OH cancelled their july 4 fireworks due to the economy

69

happy Is Watching Britains Got Talent, & Is biting her nails. Please don`t come off black nail varnish

70

unhappy im joining twitter  lol

71

nothing Glad it`s Friday… but bummed that I am officially working Saturdays.

72

nothing  ohh i love green and purple.. and BLACK!

73

nothing  ummm, come on, for me twins and slurpees, and being in a car with the twins is going to be pretty epic!!!

74

happy Was a little slow to try this one, but Ben & Jerry`s Mission to Marzipan is a bit of a letdown.

75

unhappy  Sure you will tweet about this when you`re back, but news is abuzz about TR Knight`s leaving 'confirmed' today.  Muy triste.

76

very nothing  hahaha wow thanks bud :p but my plan is to pretend its a costume… I wish it were cold so i could wear a sweatshirt over this

77

happy just bought 6 new movies

78

nothing oh man had great nap (still alittle tired) having pizza for dinner.

79

very happy off to go buy more deck sleeves and 3X3 card pages.  Man, those pages are expensive!   Stupid organizing collection.

80

unhappy  ooh like what? I`m planning on spending the night in as well

81

happy  Sorry to hear that man  He is were the **** cant reach him now. My heart goes out to you and your family.

82

very happy It`s 6 am, I haven`t been to bed yet, and I just got my second wind.  Guess I should edit or read or something until I feel tired huh?

83

unhappy  Were you going to come? The venue said that they couldn`t afford to open so cancelled it. I wish we were there now!

84

very nothing  no way – those are great words.  Boys don`t get to own them.    Oh and was it your bday?

85

happy nothing to do on a friday night

86

unhappy Watching maxium 100. Why can`t I look beautiful like those girls.

87

happy  Worried about our Arabelle. Tweet please. Or text.

88

happy Greenville for the weekend for my best friends birthday and leaving way later than i wanted…

89

unhappy  Yes, though perhaps I wasn`t thinking. I like vague. It seems a popper term for you.

90

happy  Oh whoops, my bad

91

very unhappy Heyya guys! does anyone know how to give formulas to create a sudoku? Please help

92

unhappy 1 more day!

93

very nothing  y r we giving up on people?  I actually thought that way for a while too before I found someone who is very intriguing

94

nothing loves the new Mother`s Day snl digital short, mother lover, oohhhh cornyness

95

very nothing  Oh! Don`t you just love these Vodafone series of Ads … The best picturisation ever

96

very happy  or so a month. I put my 2 week`s notice in a little over a week ago, my last day is this friday!

97

very happy recorded some of a new song today! u wont hear it for a long time thooo… we might play it at shows tho! so comeeeeee

98

very nothing Heading home after a long week. Wish someone onther than marketers would follow me

99

happy Off to see the TinyÃ¯Â¿Â½s, thinking thoughts about smiles I caught from the radio  and big daft grin all over my face….

题目名称：Targeted_Image_adv_attacks

题目内容：详情请阅读readme.md

题目难度：困难

readme

题目描述:

在这个赛题中，我们将提供一个预训练好的猫、狗、狐狸识别模型以及一组包含这三类图像的数据集。

参赛选手的任务是： 对这些图像增加微小的扰动，生成攻击图像，使得模型在预测这些经过扰动的攻击图像时出现错误。目标是： 让模型将猫误识别为狗、狗误识别为狐狸、狐狸误识别为猫。

选手需要设计一种算法，在不明显改变图像视觉效果的前提下，对图像添加微小扰动，使得提供的猫、狗、狐狸识别模型在预测时出现错误。例如，将原本能够正确识别为猫的图像进行扰动后，模型会将其错误地分类为狗，同理对狗图片增加扰动得到的新图片，模型会识别为狐狸，对狐狸图片增加扰动后得到的新图片，模型会识别为猫。

为了量化扰动的程度，我们将使用修改后图像与原始图像的相似度作为评判标准。我们会计算每个扰动图像与其对应原始图像的结构相似性指数（SSIM）。如果修改后的图像与原图的 SSIM 值低于 0.95，则认为扰动过大，该攻击样本将不被视为有效的对抗性样本。

对于满足相似度条件的图像，我们将使用提供的猫、狗、狐狸识别模型进行预测。如果模型预测结果满足对应的攻击映射，则视为一次成功的攻击，选手将获得 1 分。选手需要在成功攻击至少80%的样本，即产生至少80%满足相似度条件且能够成功欺骗模型的对抗性样本，才能获得题目的 flag。

数据类别标签映射：

目标标签映射：

target_mapping = {
    0: 1,  # 原标签: cat -> 目标标签: dog
    1: 2,  # 原标签: dog -> 目标标签: fox
    2: 0   # 原标签: fox -> 目标标签: cat
}

数据和模型：

发放的数据中包含图片文件和 预训练模型 ckpt_densenet121_catdogfox_classify.pth。

预训练模型的读取如下：

model = models.densenet121(pretrained=True)
num_ftrs = model.classifier.in_features
model.classifier = nn.Sequential(
    nn.Linear(num_ftrs, 500),
    nn.Linear(500, 3) 
)

model.load_state_dict(torch.load(PATH, map_location=device))
model = model.to(device)

模型的 label 映射: {"cat":0,"dog":1,"fox":2}

数据目录结构如下：

adv_image
 |____cat
 | |______cat_000.jpg
 | |______cat_001.jpg
 |____dog
 | |______dog_000.jpg
 | |______dog_001.jpg
 |____fox
 | |______fox_000.jpg
 | |______fox_001.jpg

要求选手对图片增加扰动，将扰动后的攻击图片保存下来，保存下来的攻击图片，可以达到让模型分类错误的效果（dog 图片识别为fox，fox图片识别为cat，cat图片识别为dog）。

提交要求：

选手需要把增加扰动后得到的新图片(攻击图片)，按照规定的格式进行上传提交(在平台下载上传时的文件结构目录 update.tar.gz)，将经过扰动后的攻击图像存放在对应的文件夹下，修改后图片文件名称需要和原始图像名称保持一致，不要修改。

将图片文件存放到update对应的cat、dog、fox 目录下。可以用如下命令创建 .tar.gz 包，然后上传:

tar -zcf xxxxx.tar.gz update

目录结构如下（修改后的图片文件名称需要和原始图片名称保持一致）：

xxxx.tar.gz
|____update
 |____cat
 |______**.jpg
 |____dog
 |______**.jpg
 |____fox
 |______**.jpg

相似度：

生成的对抗图像和原始图像之间的结构相似度（SSIM）需要在 95% 以内。

攻击成功率：

攻击成功率达到 80%（即生成的对抗样本中有 80% 能够欺骗模型并满足相似度要求）。

成功满足上述条件即可获取比赛的 flag。

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision as tv
import torchvision.transforms as transforms

import io
import matplotlib.pyplot as plt

from PIL import Image
from PIL import Image
import random

import pytorch_ssim
import torch
from torch.autograd import Variable
import cv2
import numpy as np

from torchvision.transforms import GaussianBlur
from torchvision.transforms import ToPILImage
from tqdm import tqdm

model = models.densenet121(pretrained=True)
num_ftrs = model.classifier.in_features
model.classifier = nn.Sequential(
    nn.Linear(num_ftrs, 500),
    nn.Linear(500, 3) 
)

device = torch.device("cpu")

model.load_state_dict(torch.load("./ckpt_densenet121_catdogfox_classify.pth", map_location=device))
model = model.to(device)
model.eval()

def transform_image(image_bytes):
    # my_transforms = transforms.Compose([transforms.Resize((224, 224)),  # DenseNet需要224x224的图片
    #                                     # 将PIL图片或NumPy ndarray转换为tensor，并归一化
    #                                     transforms.ToTensor(),
    #                                     # 归一化到[-1, 1]范围，使用ImageNet的均值和标准差
    #                                     transforms.Normalize(mean=[0.6377, 0.4879, 0.4189],
    #                                                      std=[0.2119, 0.1905, 0.1831]), ])
    my_transforms = transforms.Compose([transforms.ToTensor()])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def judge_pic(img_path):
    with open(img_path, 'rb') as f:
        image_bytes = f.read()
    tensor = transform_image(image_bytes=image_bytes)
    tensor = tensor.to(device)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    return int(y_hat)

def ssim_pic(old,new):

    npImg1 = cv2.imread(old)
    img1 = torch.from_numpy(np.rollaxis(npImg1, 2)).float().unsqueeze(0)/255.0
    
    npImg2 = cv2.imread(new)
    img2 = torch.from_numpy(np.rollaxis(npImg2, 2)).float().unsqueeze(0)/255.0
    result = pytorch_ssim.ssim(img1, img2)
    return result
    # ssim_loss = pytorch_ssim.SSIM(window_size = 11)
    
    # print(ssim_loss(img1, img2))
def make_fooling_image(X, target_y, model,learning_rate,ori_pic,new_pic):
    # Initialize our fooling image to the input image, and wrap it in a Variable.
    X_fooling = X.clone()
    X_fooling_var = Variable(X_fooling, requires_grad=True)

    # learning_rate = 0.1
    for i in range(100):
        # forword
        scores = model(X_fooling_var)
        # Current max index.
        _, index = scores.data.max(dim=1)
        # print(index)
        # fool then break
        if index[0] == target_y:
            # dog组从X_fooling_var转图片后准确率下降，更改判定的方式
            K = X_fooling.clone()
            toPIL = transforms.ToPILImage()
            img = K.squeeze(0)
            pic = toPIL(img)
            pic.save(new_pic)
            with open(new_pic, 'rb') as f:
                image_bytes = f.read()
            tensor = transform_image(image_bytes=image_bytes)
            tensor = tensor.to(device)
            outputs = model.forward(tensor)
            _, y_hat = outputs.max(1)
            if int(y_hat) == target_y and (ssim_pic(ori_pic,new_pic))>=0.95:
                break
            else:
                pass
            # print(pytorch_ssim.ssim(X, X_fooling_var))
        # Score for the target class.
        target_score = scores[0,target_y]
        # Backward.
        target_score.backward()
        # Gradient for image.
        im_grad = X_fooling_var.grad.data
        # update pic
        X_fooling_var.data += learning_rate * (im_grad / im_grad.norm()) 
        # clear grad.
        X_fooling_var.grad.data.zero_()

    return X_fooling

def fool_gan_pic(ori_pic,new_pic,target,learning_rate):
    for g in range(5):
        with open(ori_pic, 'rb') as f:
            image_bytes = f.read()
        tensor = transform_image(image_bytes=image_bytes)
        tensor = tensor.to(device)
        change_x = make_fooling_image(tensor, target, model,learning_rate,ori_pic,new_pic)
        
        # result = pytorch_ssim.ssim(tensor, change_x)
        toPIL = transforms.ToPILImage()
        pic = toPIL(change_x[0])
        pic.save(new_pic)

        # image=Image.open(new_pic)
        # gauss=GaussianBlur(kernel_size=(5,9),sigma=(0.1,5))
        # iam=gauss(image)
        # iam.save(new_pic)
        
        if float(ssim_pic(ori_pic,new_pic)) < 0.95:
            # print("ssim too low")
            continue
        result = judge_pic(new_pic)
        # print(result)
        if result == target:
            # print(result)
            return True
    # print(ori_pic+" : failed!")
    return False

cat_file_list = []
for i in range(0,50):
    file_addr = './adv_image/cat/cat_0' + str(i).rjust(2,"0")+'.jpg'
    new_pic = file_addr.replace("adv_image/cat","adv_image/cat_new")
    cat_file_list.append([file_addr,new_pic])

dog_file_list = []
for i in range(0,50):
    file_addr = './adv_image/dog/dog_0' + str(i).rjust(2,"0")+'.jpg'
    new_pic = file_addr.replace("adv_image/dog","adv_image/dog_new")
    dog_file_list.append([file_addr,new_pic])

fox_file_list = []
for i in range(0,50):
    file_addr = './adv_image/fox/fox_0' + str(i).rjust(2,"0")+'.jpg'
    new_pic = file_addr.replace("adv_image/fox","adv_image/fox_new")
    fox_file_list.append([file_addr,new_pic])

learning_rate = 0.1
for target,file_list in [(1,cat_file_list),(2,dog_file_list),(0,fox_file_list)]:
    for i in range(0,50):
        ori_pic,new_pic = file_list[i]
        # model.load_state_dict(torch.load("./ckpt_densenet121_catdogfox_classify.pth", map_location=device))
        # model = model.to(device)
        # model.eval()
        if fool_gan_pic(ori_pic,new_pic,target,learning_rate):
            print("success : "+ori_pic)
        else:
            print("failed : "+ori_pic)

# success : ./adv_image/cat/cat_000.jpg
# success : ./adv_image/cat/cat_001.jpg
# success : ./adv_image/cat/cat_002.jpg
# success : ./adv_image/cat/cat_003.jpg
# success : ./adv_image/cat/cat_004.jpg
# success : ./adv_image/cat/cat_005.jpg
# success : ./adv_image/cat/cat_006.jpg
# success : ./adv_image/cat/cat_007.jpg
# success : ./adv_image/cat/cat_008.jpg
# failed : ./adv_image/cat/cat_009.jpg
# success : ./adv_image/cat/cat_010.jpg
# success : ./adv_image/cat/cat_011.jpg
# success : ./adv_image/cat/cat_012.jpg
# success : ./adv_image/cat/cat_013.jpg
# success : ./adv_image/cat/cat_014.jpg
# success : ./adv_image/cat/cat_015.jpg
# success : ./adv_image/cat/cat_016.jpg
# success : ./adv_image/cat/cat_017.jpg
# success : ./adv_image/cat/cat_018.jpg
# success : ./adv_image/cat/cat_019.jpg
# success : ./adv_image/cat/cat_020.jpg
# success : ./adv_image/cat/cat_021.jpg
# success : ./adv_image/cat/cat_022.jpg
# success : ./adv_image/cat/cat_023.jpg
# success : ./adv_image/cat/cat_024.jpg
# success : ./adv_image/cat/cat_025.jpg
# success : ./adv_image/cat/cat_026.jpg
# success : ./adv_image/cat/cat_027.jpg
# success : ./adv_image/cat/cat_028.jpg
# success : ./adv_image/cat/cat_029.jpg
# success : ./adv_image/cat/cat_030.jpg
# success : ./adv_image/cat/cat_031.jpg
# success : ./adv_image/cat/cat_032.jpg
# success : ./adv_image/cat/cat_033.jpg
# success : ./adv_image/cat/cat_034.jpg
# success : ./adv_image/cat/cat_035.jpg
# success : ./adv_image/cat/cat_036.jpg
# success : ./adv_image/cat/cat_037.jpg
# success : ./adv_image/cat/cat_038.jpg
# success : ./adv_image/cat/cat_039.jpg
# success : ./adv_image/cat/cat_040.jpg
# success : ./adv_image/cat/cat_041.jpg
# success : ./adv_image/cat/cat_042.jpg
# success : ./adv_image/cat/cat_043.jpg
# failed : ./adv_image/cat/cat_044.jpg
# success : ./adv_image/cat/cat_045.jpg
# success : ./adv_image/cat/cat_046.jpg
# success : ./adv_image/cat/cat_047.jpg
# success : ./adv_image/cat/cat_048.jpg
# success : ./adv_image/cat/cat_049.jpg
# failed : ./adv_image/dog/dog_000.jpg
# success : ./adv_image/dog/dog_001.jpg
# success : ./adv_image/dog/dog_002.jpg
# failed : ./adv_image/dog/dog_003.jpg
# success : ./adv_image/dog/dog_004.jpg
# success : ./adv_image/dog/dog_005.jpg
# failed : ./adv_image/dog/dog_006.jpg
# success : ./adv_image/dog/dog_007.jpg
# success : ./adv_image/dog/dog_008.jpg
# success : ./adv_image/dog/dog_009.jpg
# failed : ./adv_image/dog/dog_010.jpg
# success : ./adv_image/dog/dog_011.jpg
# success : ./adv_image/dog/dog_012.jpg
# success : ./adv_image/dog/dog_013.jpg
# success : ./adv_image/dog/dog_014.jpg
# failed : ./adv_image/dog/dog_015.jpg
# success : ./adv_image/dog/dog_016.jpg
# success : ./adv_image/dog/dog_017.jpg
# success : ./adv_image/dog/dog_018.jpg
# success : ./adv_image/dog/dog_019.jpg
# success : ./adv_image/dog/dog_020.jpg
# failed : ./adv_image/dog/dog_021.jpg
# success : ./adv_image/dog/dog_022.jpg
# success : ./adv_image/dog/dog_023.jpg
# success : ./adv_image/dog/dog_024.jpg
# success : ./adv_image/dog/dog_025.jpg
# success : ./adv_image/dog/dog_026.jpg
# success : ./adv_image/dog/dog_027.jpg
# success : ./adv_image/dog/dog_028.jpg
# success : ./adv_image/dog/dog_029.jpg
# success : ./adv_image/dog/dog_030.jpg
# success : ./adv_image/dog/dog_031.jpg
# success : ./adv_image/dog/dog_032.jpg
# success : ./adv_image/dog/dog_033.jpg
# failed : ./adv_image/dog/dog_034.jpg
# success : ./adv_image/dog/dog_035.jpg
# success : ./adv_image/dog/dog_036.jpg
# success : ./adv_image/dog/dog_037.jpg
# success : ./adv_image/dog/dog_038.jpg
# success : ./adv_image/dog/dog_039.jpg
# success : ./adv_image/dog/dog_040.jpg
# success : ./adv_image/dog/dog_041.jpg
# failed : ./adv_image/dog/dog_042.jpg
# success : ./adv_image/dog/dog_043.jpg
# failed : ./adv_image/dog/dog_044.jpg
# success : ./adv_image/dog/dog_045.jpg
# success : ./adv_image/dog/dog_046.jpg
# success : ./adv_image/dog/dog_047.jpg
# failed : ./adv_image/dog/dog_048.jpg
# success : ./adv_image/dog/dog_049.jpg
# success : ./adv_image/fox/fox_000.jpg
# success : ./adv_image/fox/fox_001.jpg
# success : ./adv_image/fox/fox_002.jpg
# success : ./adv_image/fox/fox_003.jpg
# success : ./adv_image/fox/fox_004.jpg
# success : ./adv_image/fox/fox_005.jpg
# success : ./adv_image/fox/fox_006.jpg
# success : ./adv_image/fox/fox_007.jpg
# success : ./adv_image/fox/fox_008.jpg
# success : ./adv_image/fox/fox_009.jpg
# success : ./adv_image/fox/fox_010.jpg
# success : ./adv_image/fox/fox_011.jpg
# success : ./adv_image/fox/fox_012.jpg
# success : ./adv_image/fox/fox_013.jpg
# success : ./adv_image/fox/fox_014.jpg
# success : ./adv_image/fox/fox_015.jpg
# success : ./adv_image/fox/fox_016.jpg
# success : ./adv_image/fox/fox_017.jpg
# success : ./adv_image/fox/fox_018.jpg
# success : ./adv_image/fox/fox_019.jpg
# success : ./adv_image/fox/fox_020.jpg
# success : ./adv_image/fox/fox_021.jpg
# success : ./adv_image/fox/fox_022.jpg
# success : ./adv_image/fox/fox_023.jpg
# success : ./adv_image/fox/fox_024.jpg
# success : ./adv_image/fox/fox_025.jpg
# success : ./adv_image/fox/fox_026.jpg
# success : ./adv_image/fox/fox_027.jpg
# success : ./adv_image/fox/fox_028.jpg
# success : ./adv_image/fox/fox_029.jpg
# success : ./adv_image/fox/fox_030.jpg
# success : ./adv_image/fox/fox_031.jpg
# success : ./adv_image/fox/fox_032.jpg
# success : ./adv_image/fox/fox_033.jpg
# success : ./adv_image/fox/fox_034.jpg
# success : ./adv_image/fox/fox_035.jpg
# success : ./adv_image/fox/fox_036.jpg
# success : ./adv_image/fox/fox_037.jpg
# success : ./adv_image/fox/fox_038.jpg
# success : ./adv_image/fox/fox_039.jpg
# success : ./adv_image/fox/fox_040.jpg
# success : ./adv_image/fox/fox_041.jpg
# success : ./adv_image/fox/fox_042.jpg
# success : ./adv_image/fox/fox_043.jpg
# success : ./adv_image/fox/fox_044.jpg
# success : ./adv_image/fox/fox_045.jpg
# success : ./adv_image/fox/fox_046.jpg
# success : ./adv_image/fox/fox_047.jpg
# success : ./adv_image/fox/fox_048.jpg
# success : ./adv_image/fox/fox_049.jpg

def calc_accury():
    value = 0
    count = 0
    for target,file_list in [(1,cat_file_list),(2,dog_file_list),(0,fox_file_list)]:
        for i in range(0,50):
            ori_pic,new_pic = file_list[i]
            if target == judge_pic(new_pic) and float(ssim_pic(ori_pic,new_pic)) >= 0.95:
                value += 1
            else:
                pass
            count += 1
    print(f"{value/count * 100}%")
calc_accury() 

# 92%


```
def verify_similarity(original, modified, model, tokenizer):
    # 确保模型处于评估模式
    model.eval()

    # 对原始文本和修改后的文本进行编码
    original_encoding = tokenizer(original, return_tensors='pt', padding=True, truncation=True, max_length=512)
    modified_encoding = tokenizer(modified, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        # 获取原始文本的隐藏状态
        original_outputs = model.distilbert(**original_encoding)
        original_hidden_state = original_outputs.last_hidden_state.mean(dim=1)

        # 获取修改后文本的隐藏状态
        modified_outputs = model.distilbert(**modified_encoding)
        modified_hidden_state = modified_outputs.last_hidden_state.mean(dim=1)

    # 计算余弦相似度
    similarity = cosine_similarity(original_hidden_state.cpu().numpy(),
                                modified_hidden_state.cpu().numpy())[0][0]

    return similarity
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.metrics.pairwise import cosine_similarity
import csv
# sentiment-analysis 默认使用的 checkpoint
checkpoint = "./Sentiment_classification_model"

# 建立 tokenizer，加载模型的 checkpoint，建立 model 对象实例
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
def verify_similarity(original, modified, model, tokenizer):
    # 确保模型处于评估模式
    model.eval()

    # 对原始文本和修改后的文本进行编码
    original_encoding = tokenizer(original, return_tensors='pt', padding=True, truncation=True, max_length=512)
    modified_encoding = tokenizer(modified, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        # 获取原始文本的隐藏状态
        original_outputs = model.distilbert(**original_encoding)
        original_hidden_state = original_outputs.last_hidden_state.mean(dim=1)

        # 获取修改后文本的隐藏状态
        modified_outputs = model.distilbert(**modified_encoding)
        modified_hidden_state = modified_outputs.last_hidden_state.mean(dim=1)

    # 计算余弦相似度
    similarity = cosine_similarity(original_hidden_state.cpu().numpy(),
                                modified_hidden_state.cpu().numpy())[0][0]
    if similarity < 0.7:
        return False
    else:
        return True
    # return similarity
def predict_model(tokenizer,model,raw_inputs):
    # 原始输入序列
    # raw_inputs = ["Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY"]
    
    # 调用 Tokenizer 进行预处理，预处理的结果会作为 Model 的输入
    inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
    # encoded_input = tokenizer(sentence, return_tensors='pt')
    
    
    # 将 Tokenizer 预处理后的数据传送给 Model，“**”用于将 inputs 字典中的键值对解包成模型的输入参数
    outputs = model(**inputs)
    
    # 打印一下 Transformer 输出的 Logits 的结构信息
    # print(outputs.logits.shape)
    
    # 打印一下 Transformer 输出的 Logits 的信息
    # print(outputs.logits)
    predictions = outputs.logits
    
    # 解析预测结果
    # 假设模型有两个类别：0 表示负面，1 表示正面
    # if predictions.argmax() == 0:
    #     print("该句子情感为负面")
    # elif predictions.argmax() == 1:
    #     print("该句子情感为无所谓")
    # elif predictions.argmax() == 2:
    #     print("该句子情感为正面")
    # return str(predictions.argmax())
    return str(int(predictions.argmax()))
 
 
filename = 'original_text.csv'
data_dict = {}
with open(filename, newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == "id":
            continue
        data_dict[row[0]] = {'text':
row[1],'label':
row[3]}
        
data_dict_2 = {}
for id in data_dict:
    original_text = data_dict[id]['text']
    label = data_dict[id]['label']
    if label == "0": #neg
        data_dict_2[id] = {"text":"happy " + original_text}
    elif label == "2":
        data_dict_2[id] = {"text":"nothing " + original_text}
    elif label == "1": #pos
        data_dict_2[id] = {"text":"unhappy " + original_text}

def calc_accuracy(data_dict,new_data_dict):
    value = 0
    for id in data_dict:
        original_text = data_dict[id]['text']
        modified_text = new_data_dict[id]['text']
        result = predict_model(tokenizer,model,modified_text)
        label = data_dict[id]['label']
        if result != label:
            if verify_similarity(original_text, modified_text, model, tokenizer):
                value += 1
        else:
            pass
    print(f"{value/len(data_dict) * 100}%")

calc_accuracy(data_dict,data_dict_2)
pre_failed 1 2 nothing Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY
pre_failed 2 0 happy  im only on 1800  lol
pre_failed 3 2 nothing was busy talking with mom and bhabhi.. they liked the cards bro and me made for them  now waiting for sis to get back from Church..
pre_failed 11 0 happy  Nothing definite yet..and the show is in a week   I may just be resorted to giving them away
pre_failed 13 0 happy forgot my macbook`s recharger, that means nothing but Pratchett for me today
pre_failed 16 2 nothing  Stress test: http://www.selfhelpmagazine.com/psychtoons/glasbergen/StressManagement/StressTest.gif  Good luck!
pre_failed 20 0 happy _G  ur a poopy head
pre_failed 21 2 nothing  aww you poor thing  hope all goes well!
pre_failed 24 0 happy http://www.myspace.com/dica_grl Just got a crush on this song! Disco`s Out! Murder`s In! ruleaz?, zic!  www.myspace.com/discosoutmurdersin
pre_failed 28 0 happy 2nd to last episode of jay leno  itll never be the same!  nite twitter
pre_failed 36 2 nothing Nice PC Authority review of the Tivo VOD service here: http://bit.ly/Ps7y2  I`m still loving my Tivo
pre_failed 37 2 nothing - It`s time for Kathleen to go to bed... waaaaay past time. Don`t expect to hear from me before noon. lol  Have a BLESSED morning.
pre_failed 38 2 nothing Am good thanks, what`s Miami saying? How come u wrote to me?
pre_failed 43 0 happy I wanna go to the beach...but I have to study
pre_failed 48 0 happy  Don`t leave forever! We`ll miss you too much
pre_failed 50 2 nothing  bugger, that would have been nice but typically, we`re heading to Bristol
pre_failed 51 0 happy _0 have you considered cordoning off a corner of the park with beware 'Swine flu' signs might clear it out for you
pre_failed 58 2 nothing Had a nice pre mother`s day dinner out. Now a cocktail before retiring for the evening
ver_failed 59 0 happy   well hit me and we can see...it depends then
pre_failed 66 2 nothing Last Late Late with Pat Kenny! Bless
pre_failed 67 1 unhappy Checked if there`s a new comment on friendster!
pre_failed 76 2 nothing  hahaha wow thanks bud :p but my plan is to pretend its a costume... I wish it were cold so i could wear a sweatshirt over this
pre_failed 79 0 happy off to go buy more deck sleeves and 3X3 card pages.  Man, those pages are expensive!   Stupid organizing collection.
pre_failed 82 0 happy It`s 6 am, I haven`t been to bed yet, and I just got my second wind.  Guess I should edit or read or something until I feel tired huh?
pre_failed 84 2 nothing  no way - those are great words.  Boys don`t get to own them.    Oh and was it your bday?
pre_failed 91 1 unhappy Heyya guys! does anyone know how to give formulas to create a sudoku? Please help
pre_failed 93 2 nothing  y r we giving up on people?  I actually thought that way for a while too before I found someone who is very intriguing
pre_failed 95 2 nothing  Oh! Don`t you just love these Vodafone series of Ads ... The best picturisation ever
pre_failed 96 0 happy  or so a month. I put my 2 week`s notice in a little over a week ago, my last day is this friday!
pre_failed 97 0 happy recorded some of a new song today! u wont hear it for a long time thooo... we might play it at shows tho! so comeeeeee
pre_failed 98 2 nothing Heading home after a long week. Wish someone onther than marketers would follow me
data_dict_2 = {}
for id in data_dict:
    original_text = data_dict[id]['text']
    label = data_dict[id]['label']
    if label == "0": #neg
        data_dict_2[id] = {"text":"happy " + original_text}
    elif label == "2":
        data_dict_2[id] = {"text":"nothing " + original_text}
    elif label == "1": #pos
        data_dict_2[id] = {"text":"unhappy " + original_text}
    if id in ["1","2","3","11","13","16","20","21","24","28","36","37","38","43","48","50","51","58","59","66","67","76","79","82","84","91","93","95","96","97","98"]:
        data_dict_2[id] = {"text":"very " + data_dict_2[id]['text']}
calc_accuracy(data_dict,data_dict_2)
pre_failed 1 2 very nothing Good mornin. Today will end early, woo. Gonna work on rick`s surprise PROJECT DUE ON TUESDAY
ver_failed 2 0 very happy im only on 1800 lol
pre_failed 3 2 very nothing was busy talking with mom and bhabhi.. they liked the cards bro and me made for them now waiting for sis to get back from Church..
pre_failed 11 0 very happy Nothing definite yet..and the show is in a week I may just be resorted to giving them away
pre_failed 16 2 very nothing Stress test: http://www.selfhelpmagazine.com/psychtoons/glasbergen/StressManagement/StressTest.gif Good luck!
ver_failed 20 0 very happy _G ur a poopy head
pre_failed 21 2 very nothing aww you poor thing hope all goes well!
pre_failed 36 2 very nothing Nice PC Authority review of the Tivo VOD service here: http://bit.ly/Ps7y2 I`m still loving my Tivo
pre_failed 37 2 very nothing - It`s time for Kathleen to go to bed... waaaaay past time. Don`t expect to hear from me before noon. lol Have a BLESSED morning.
pre_failed 38 2 very nothing Am good thanks, what`s Miami saying? How come u wrote to me?
pre_failed 50 2 very nothing bugger, that would have been nice but typically, we`re heading to Bristol
pre_failed 58 2 very nothing Had a nice pre mother`s day dinner out. Now a cocktail before retiring for the evening
ver_failed 59 0 very happy well hit me and we can see...it depends then
pre_failed 66 2 very nothing Last Late Late with Pat Kenny! Bless
pre_failed 76 2 very nothing hahaha wow thanks bud :p but my plan is to pretend its a costume... I wish it were cold so i could wear a sweatshirt over this
pre_failed 79 0 very happy off to go buy more deck sleeves and 3X3 card pages. Man, those pages are expensive! Stupid organizing collection.
pre_failed 84 2 very nothing no way - those are great words. Boys don`t get to own them. Oh and was it your bday?
pre_failed 93 2 very nothing y r we giving up on people? I actually thought that way for a while too before I found someone who is very intriguing
pre_failed 95 2 very nothing Oh! Don`t you just love these Vodafone series of Ads ... The best picturisation ever
pre_failed 96 0 very happy or so a month. I put my 2 week`s notice in a little over a week ago, my last day is this friday!
pre_failed 98 2 very nothing Heading home after a long week. Wish someone onther than marketers would follow me
79.0%
target_mapping = {
    0: 1,  # 原标签: cat -> 目标标签: dog
    1: 2,  # 原标签: dog -> 目标标签: fox
    2: 0   # 原标签: fox -> 目标标签: cat
}
model = models.densenet121(pretrained=True)
num_ftrs = model.classifier.in_features
model.classifier = nn.Sequential(
    nn.Linear(num_ftrs, 500),
    nn.Linear(500, 3) 
)

model.load_state_dict(torch.load(PATH, map_location=device))
model = model.to(device)
adv_image
 |____cat
 | |______cat_000.jpg
 | |______cat_001.jpg
 |____dog
 | |______dog_000.jpg
 | |______dog_001.jpg
 |____fox
 | |______fox_000.jpg
 | |______fox_001.jpg
tar -zcf xxxxx.tar.gz update
xxxx.tar.gz
|____update
 |____cat
 |______**.jpg
 |____dog
 |______**.jpg
 |____fox
 |______**.jpg
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision as tv
import torchvision.transforms as transforms

import io
import matplotlib.pyplot as plt

from PIL import Image
from PIL import Image
import random

import pytorch_ssim
import torch
from torch.autograd import Variable
import cv2
import numpy as np

from torchvision.transforms import GaussianBlur
from torchvision.transforms import ToPILImage
from tqdm import tqdm

model = models.densenet121(pretrained=True)
num_ftrs = model.classifier.in_features
model.classifier = nn.Sequential(
    nn.Linear(num_ftrs, 500),
    nn.Linear(500, 3) 
)

device = torch.device("cpu")

model.load_state_dict(torch.load("./ckpt_densenet121_catdogfox_classify.pth", map_location=device))
model = model.to(device)
model.eval()

def transform_image(image_bytes):
    # my_transforms = transforms.Compose([transforms.Resize((224, 224)),  # DenseNet需要224x224的图片
    #                                     # 将PIL图片或NumPy ndarray转换为tensor，并归一化
    #                                     transforms.ToTensor(),
    #                                     # 归一化到[-1, 1]范围，使用ImageNet的均值和标准差
    #                                     transforms.Normalize(mean=[0.6377, 0.4879, 0.4189],
    #                                                      std=[0.2119, 0.1905, 0.1831]), ])
    my_transforms = transforms.Compose([transforms.ToTensor()])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

def judge_pic(img_path):
    with open(img_path, 'rb') as f:
        image_bytes = f.read()
    tensor = transform_image(image_bytes=image_bytes)
    tensor = tensor.to(device)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    return int(y_hat)

def ssim_pic(old,new):

    npImg1 = cv2.imread(old)
    img1 = torch.from_numpy(np.rollaxis(npImg1, 2)).float().unsqueeze(0)/255.0
    
    npImg2 = cv2.imread(new)
    img2 = torch.from_numpy(np.rollaxis(npImg2, 2)).float().unsqueeze(0)/255.0
    result = pytorch_ssim.ssim(img1, img2)
    return result
    # ssim_loss = pytorch_ssim.SSIM(window_size = 11)
    
    # print(ssim_loss(img1, img2))
def make_fooling_image(X, target_y, model,learning_rate,ori_pic,new_pic):
    # Initialize our fooling image to the input image, and wrap it in a Variable.
    X_fooling = X.clone()
    X_fooling_var = Variable(X_fooling, requires_grad=True)

    # learning_rate = 0.1
    for i in range(100):
        # forword
        scores = model(X_fooling_var)
        # Current max index.
        _, index = scores.data.max(dim=1)
        # print(index)
        # fool then break
        if index[0] == target_y:
            # dog组从X_fooling_var转图片后准确率下降，更改判定的方式
            K = X_fooling.clone()
            toPIL = transforms.ToPILImage()
            img = K.squeeze(0)
            pic = toPIL(img)
            pic.save(new_pic)
            with open(new_pic, 'rb') as f:
                image_bytes = f.read()
            tensor = transform_image(image_bytes=image_bytes)
            tensor = tensor.to(device)
            outputs = model.forward(tensor)
            _, y_hat = outputs.max(1)
            if int(y_hat) == target_y and (ssim_pic(ori_pic,new_pic))>=0.95:
                break
            else:
                pass
            # print(pytorch_ssim.ssim(X, X_fooling_var))
        # Score for the target class.
        target_score = scores[0,target_y]
        # Backward.
        target_score.backward()
        # Gradient for image.
        im_grad = X_fooling_var.grad.data
        # update pic
        X_fooling_var.data += learning_rate * (im_grad / im_grad.norm()) 
        # clear grad.
        X_fooling_var.grad.data.zero_()

    return X_fooling

def fool_gan_pic(ori_pic,new_pic,target,learning_rate):
    for g in range(5):
        with open(ori_pic, 'rb') as f:
            image_bytes = f.read()
        tensor = transform_image(image_bytes=image_bytes)
        tensor = tensor.to(device)
        change_x = make_fooling_image(tensor, target, model,learning_rate,ori_pic,new_pic)
        
        # result = pytorch_ssim.ssim(tensor, change_x)
        toPIL = transforms.ToPILImage()
        pic = toPIL(change_x[0])
        pic.save(new_pic)

        # image=Image.open(new_pic)
        # gauss=GaussianBlur(kernel_size=(5,9),sigma=(0.1,5))
        # iam=gauss(image)
        # iam.save(new_pic)
        
        if float(ssim_pic(ori_pic,new_pic)) < 0.95:
            # print("ssim too low")
            continue
        result = judge_pic(new_pic)
        # print(result)
        if result == target:
            # print(result)
            return True
    # print(ori_pic+" : failed!")
    return False

cat_file_list = []
for i in range(0,50):
    file_addr = './adv_image/cat/cat_0' + str(i).rjust(2,"0")+'.jpg'
    new_pic = file_addr.replace("adv_image/cat","adv_image/cat_new")
    cat_file_list.append([file_addr,new_pic])

dog_file_list = []
for i in range(0,50):
    file_addr = './adv_image/dog/dog_0' + str(i).rjust(2,"0")+'.jpg'
    new_pic = file_addr.replace("adv_image/dog","adv_image/dog_new")
    dog_file_list.append([file_addr,new_pic])

fox_file_list = []
for i in range(0,50):
    file_addr = './adv_image/fox/fox_0' + str(i).rjust(2,"0")+'.jpg'
    new_pic = file_addr.replace("adv_image/fox","adv_image/fox_new")
    fox_file_list.append([file_addr,new_pic])

learning_rate = 0.1
for target,file_list in [(1,cat_file_list),(2,dog_file_list),(0,fox_file_list)]:
    for i in range(0,50):
        ori_pic,new_pic = file_list[i]
        # model.load_state_dict(torch.load("./ckpt_densenet121_catdogfox_classify.pth", map_location=device))
        # model = model.to(device)
        # model.eval()
        if fool_gan_pic(ori_pic,new_pic,target,learning_rate):
            print("success : "+ori_pic)
        else:
            print("failed : "+ori_pic)

# success : ./adv_image/cat/cat_000.jpg
# success : ./adv_image/cat/cat_001.jpg
# success : ./adv_image/cat/cat_002.jpg
# success : ./adv_image/cat/cat_003.jpg
# success : ./adv_image/cat/cat_004.jpg
# success : ./adv_image/cat/cat_005.jpg
# success : ./adv_image/cat/cat_006.jpg
# success : ./adv_image/cat/cat_007.jpg
# success : ./adv_image/cat/cat_008.jpg
# failed : ./adv_image/cat/cat_009.jpg
# success : ./adv_image/cat/cat_010.jpg
# success : ./adv_image/cat/cat_011.jpg
# success : ./adv_image/cat/cat_012.jpg
# success : ./adv_image/cat/cat_013.jpg
# success : ./adv_image/cat/cat_014.jpg
# success : ./adv_image/cat/cat_015.jpg
# success : ./adv_image/cat/cat_016.jpg
# success : ./adv_image/cat/cat_017.jpg
# success : ./adv_image/cat/cat_018.jpg
# success : ./adv_image/cat/cat_019.jpg
# success : ./adv_image/cat/cat_020.jpg
# success : ./adv_image/cat/cat_021.jpg
# success : ./adv_image/cat/cat_022.jpg
# success : ./adv_image/cat/cat_023.jpg
# success : ./adv_image/cat/cat_024.jpg
# success : ./adv_image/cat/cat_025.jpg
# success : ./adv_image/cat/cat_026.jpg
# success : ./adv_image/cat/cat_027.jpg
# success : ./adv_image/cat/cat_028.jpg
# success : ./adv_image/cat/cat_029.jpg
# success : ./adv_image/cat/cat_030.jpg
# success : ./adv_image/cat/cat_031.jpg
# success : ./adv_image/cat/cat_032.jpg
# success : ./adv_image/cat/cat_033.jpg
# success : ./adv_image/cat/cat_034.jpg
# success : ./adv_image/cat/cat_035.jpg
# success : ./adv_image/cat/cat_036.jpg
# success : ./adv_image/cat/cat_037.jpg
# success : ./adv_image/cat/cat_038.jpg
# success : ./adv_image/cat/cat_039.jpg
# success : ./adv_image/cat/cat_040.jpg
# success : ./adv_image/cat/cat_041.jpg
# success : ./adv_image/cat/cat_042.jpg
# success : ./adv_image/cat/cat_043.jpg
# failed : ./adv_image/cat/cat_044.jpg
# success : ./adv_image/cat/cat_045.jpg
# success : ./adv_image/cat/cat_046.jpg
# success : ./adv_image/cat/cat_047.jpg
# success : ./adv_image/cat/cat_048.jpg
# success : ./adv_image/cat/cat_049.jpg
# failed : ./adv_image/dog/dog_000.jpg
# success : ./adv_image/dog/dog_001.jpg
# success : ./adv_image/dog/dog_002.jpg
# failed : ./adv_image/dog/dog_003.jpg
# success : ./adv_image/dog/dog_004.jpg
# success : ./adv_image/dog/dog_005.jpg
# failed : ./adv_image/dog/dog_006.jpg
# success : ./adv_image/dog/dog_007.jpg
# success : ./adv_image/dog/dog_008.jpg
# success : ./adv_image/dog/dog_009.jpg
# failed : ./adv_image/dog/dog_010.jpg
# success : ./adv_image/dog/dog_011.jpg
# success : ./adv_image/dog/dog_012.jpg
# success : ./adv_image/dog/dog_013.jpg
# success : ./adv_image/dog/dog_014.jpg
# failed : ./adv_image/dog/dog_015.jpg
# success : ./adv_image/dog/dog_016.jpg
# success : ./adv_image/dog/dog_017.jpg
# success : ./adv_image/dog/dog_018.jpg
# success : ./adv_image/dog/dog_019.jpg
# success : ./adv_image/dog/dog_020.jpg
# failed : ./adv_image/dog/dog_021.jpg
# success : ./adv_image/dog/dog_022.jpg
# success : ./adv_image/dog/dog_023.jpg
# success : ./adv_image/dog/dog_024.jpg
# success : ./adv_image/dog/dog_025.jpg
# success : ./adv_image/dog/dog_026.jpg
# success : ./adv_image/dog/dog_027.jpg
# success : ./adv_image/dog/dog_028.jpg
# success : ./adv_image/dog/dog_029.jpg
# success : ./adv_image/dog/dog_030.jpg
# success : ./adv_image/dog/dog_031.jpg
# success : ./adv_image/dog/dog_032.jpg
# success : ./adv_image/dog/dog_033.jpg
# failed : ./adv_image/dog/dog_034.jpg
# success : ./adv_image/dog/dog_035.jpg
# success : ./adv_image/dog/dog_036.jpg
# success : ./adv_image/dog/dog_037.jpg
# success : ./adv_image/dog/dog_038.jpg
# success : ./adv_image/dog/dog_039.jpg
# success : ./adv_image/dog/dog_040.jpg
# success : ./adv_image/dog/dog_041.jpg
# failed : ./adv_image/dog/dog_042.jpg
# success : ./adv_image/dog/dog_043.jpg
# failed : ./adv_image/dog/dog_044.jpg
# success : ./adv_image/dog/dog_045.jpg
# success : ./adv_image/dog/dog_046.jpg
# success : ./adv_image/dog/dog_047.jpg
# failed : ./adv_image/dog/dog_048.jpg
# success : ./adv_image/dog/dog_049.jpg
# success : ./adv_image/fox/fox_000.jpg
# success : ./adv_image/fox/fox_001.jpg
# success : ./adv_image/fox/fox_002.jpg
# success : ./adv_image/fox/fox_003.jpg
# success : ./adv_image/fox/fox_004.jpg
# success : ./adv_image/fox/fox_005.jpg
# success : ./adv_image/fox/fox_006.jpg
# success : ./adv_image/fox/fox_007.jpg
# success : ./adv_image/fox/fox_008.jpg
# success : ./adv_image/fox/fox_009.jpg
# success : ./adv_image/fox/fox_010.jpg
# success : ./adv_image/fox/fox_011.jpg
# success : ./adv_image/fox/fox_012.jpg
# success : ./adv_image/fox/fox_013.jpg
# success : ./adv_image/fox/fox_014.jpg
# success : ./adv_image/fox/fox_015.jpg
# success : ./adv_image/fox/fox_016.jpg
# success : ./adv_image/fox/fox_017.jpg
# success : ./adv_image/fox/fox_018.jpg
# success : ./adv_image/fox/fox_019.jpg
# success : ./adv_image/fox/fox_020.jpg
# success : ./adv_image/fox/fox_021.jpg
# success : ./adv_image/fox/fox_022.jpg
# success : ./adv_image/fox/fox_023.jpg
# success : ./adv_image/fox/fox_024.jpg
# success : ./adv_image/fox/fox_025.jpg
# success : ./adv_image/fox/fox_026.jpg
# success : ./adv_image/fox/fox_027.jpg
# success : ./adv_image/fox/fox_028.jpg
# success : ./adv_image/fox/fox_029.jpg
# success : ./adv_image/fox/fox_030.jpg
# success : ./adv_image/fox/fox_031.jpg
# success : ./adv_image/fox/fox_032.jpg
# success : ./adv_image/fox/fox_033.jpg
# success : ./adv_image/fox/fox_034.jpg
# success : ./adv_image/fox/fox_035.jpg
# success : ./adv_image/fox/fox_036.jpg
# success : ./adv_image/fox/fox_037.jpg
# success : ./adv_image/fox/fox_038.jpg
# success : ./adv_image/fox/fox_039.jpg
# success : ./adv_image/fox/fox_040.jpg
# success : ./adv_image/fox/fox_041.jpg
# success : ./adv_image/fox/fox_042.jpg
# success : ./adv_image/fox/fox_043.jpg
# success : ./adv_image/fox/fox_044.jpg
# success : ./adv_image/fox/fox_045.jpg
# success : ./adv_image/fox/fox_046.jpg
# success : ./adv_image/fox/fox_047.jpg
# success : ./adv_image/fox/fox_048.jpg
# success : ./adv_image/fox/fox_049.jpg

def calc_accury():
    value = 0
    count = 0
    for target,file_list in [(1,cat_file_list),(2,dog_file_list),(0,fox_file_list)]:
        for i in range(0,50):
            ori_pic,new_pic = file_list[i]
            if target == judge_pic(new_pic) and float(ssim_pic(ori_pic,new_pic)) >= 0.95:
                value += 1
            else:
                pass
            count += 1
    print(f"{value/count * 100}%")
calc_accury() 

# 92%
```
