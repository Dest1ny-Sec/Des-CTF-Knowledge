# 官方WP | 关于“可信度量”赛题的设计与思考

> 原文: https://www.ctfiot.com/118196.html
> ID: 118196

编者荐语：

本文分享了胡俊老师是如何精心设计一道关于“可信度量”的赛题，以及三个成功解决该题的队伍的方法和技巧。

“可信度量”赛题已部署在伽玛实验场，欢迎前去挑战。

关于可信度量赛题的设计与思考

作者：北京工业大学国家等级保护2.0与可信计算3.0攻关示范基地 胡俊

1. 可信度量赛题的设计
本次国赛初赛是我第5次提供可信计算赛题支持了，在全国大学生信息安全竞赛中提供可信计算赛题则是第3次。前几次的题目，与其说出的是可信计算赛题，不如说出的是信息安全基本技能题目，可信内容体现不多，实际是使用可信软件基原型构建出了一种新的题目类型。以往的比赛中，这一题目类型得到了一定程度的认可，但在全国大赛中出一次“真正”的可信计算题目，一直是我的期望。本次比赛中，我们就进行了这方面的尝试。

出一道体现鲜明可信计算特色的题目，从题目背景来看，有两个选择：其一是选择系统安全可信机制，其二则是可信密码机制。我们在2020年央企大赛中，是在虚拟机环境下提供系统安全机制作为赛题，考虑到初赛参赛队伍众多，比赛平台难以提供足够的虚拟机资源，因此我们决定选择可信密码作为出题方向。

选定出题方向后，下一个问题则是考点的选择。我们希望题目给大家尽量真实的可信计算技术体验，考虑到同学们大部分对可信计算知识并不熟悉，我们希望题目尽量不要依赖于可信计算技术细节，让密码学知识和编程基础比较扎实的学生们无需学习更多的可信计算知识即可解出该题。因此，我们选择可信密码模块（TCM）中，具备鲜明特色的PCR寄存器作为主要考察点，考察学生们对PCR寄存器写入原理的理解，这一理解主要涉及哈希函数的应用，学生们在学习密码学知识、可信计算知识以及区块链知识，都可以接触到相关内容。

此外，赛题选择了可信报告机制为背景，可信报告机制本身相当复杂，但是抽象考虑，其防重放攻击的原理还是比较基础的，因此我们将这个防重放攻击机制作为赛题的另一个考察点。

赛题的另一个特点则是主动可信模式的应用。国际上TCG标准提供的可信密码模块访问方式是通过被动的软件栈进行访问，其接口非常复杂。而基于我国提出的主动可信免疫机制，复杂的可信密码访问可以组件化、自动化执行。赛题对TCM的访问就是分层、组件化的，这一方式可以让使用者无需关心可信密码机制中复杂的数据结构和接口。我们出题时，特地注明在key_manage模块中解析出结果后，提供给上层使用，就是为了让选手对此有所体验。

我们原本准备在可信密码服务上层的key_event模块中设置考点，让大家体验可信密码评估结果的应用。考虑到同学们熟悉可信计算还需要一个过程，题目与平台磨合也需要工作量，因此我们放弃了多出几道题的计划。但在当前题目的设计中，我们也增加了不少系统安全背景的描述，这些内容就是为了让同学们体会可信密码机制应当与系统安全状态关联起来，而不只是单纯的密码游戏。

2.解题思路
“可信度量”这道题目提供了相当多的说明内容，程序代码、数据结构中也有很多细节。如果过于关注这些细节，思路很容易被带歪。需要尽快找到题目的核心内容，忽略各种旁支，才可以顺利解题。从代码中可以看到，题目的核心就是已知可信报告中pcrValue取值，又知道pcrValue是四个策略摘要值中的部分按次序以extend方式写入pcr得到的结果。并且代码中给出了遍历读取策略摘要值的代码示例。

因此，选手只要了解PCR值的计算方式是

PCR新值 = SM3（PCR旧值|输入值）

并且看到题目已经给出了策略摘要获取方法，就可确定该题目的本质就是一个特殊的遍历搜索题目，题目算法本身难度并不大，只是需要专业知识的辅助。

题目中还有一个干扰项就是防重放攻击。从说明材料中介绍的可信报告第一阶段内容来看，申请随机数的目的就是为了防重放攻击，而执行tcm_quote.sh后如果观察crypt_hub中message.log中的报告信息，可以找到报告中的nonce变量并且发现其与所申请的随机数内容一致。因此可以判断，nonce应该就是用来防范重放攻击的机制。

下面给出我们测试时编写的解法，供大家参考：

在遍历对照所有策略这部分代码中，我们使用了一个小技巧，对n个策略，我们循环2^n次，用每次循环值的位图作为本次的寄存器选择，以简化循环。我们认为比赛时，即使没想到这个技巧，找到16种寄存器组合情况的遍历方法也非难事。

本次比赛最终只有3个队成功解出了该赛题。首先祝贺东北大学NEX战队，他们的表现符合我们对优秀队伍的预期。但是此后只有两队解出该问题，是略微出乎我们的预料的。赛后复盘，我们对这一现象的原因有以下推测，但无法确定哪些更符合实际情况，希望能够得到选手们的反馈：

初赛题目众多，选择熟悉的题目求解是更稳妥的选择。

感觉题目不容易抓住重点，读懂题目说明、读懂相关代码还是有相当难度的。

出题者以为PCR寄存器写入知识是常识或者很容易查到，实际并非如此。

队伍主要训练的是传统CTF类题目，缺少解答本题目的相关技能。

在对可信计算知识了解甚少的情况下，难以进行思维跳跃以找到解题思路。

随着我国网络安全等级保护制度和关键信息基础设施保护制度的推广，可信计算技术的推广应用将成为信息安全发展的重要趋势，预计今后会出现更多的可信计算赛题。本次比赛我们和永信至诚合作，进行了环境的磨合，虽然最终并未完全达到目标，但确定了问题并找到了解决方案。今后，我们可以为大家构建开源、标准化的可信计算练习环境，让大家都能够有可信赛题的实训环境。同时，我们也将尽量发挥主动免疫可信的优势，为大家提供低学习门槛，更注重安全理念和工程方法的可信计算系列实训用例和赛题。也希望大家基于这些赛题进一步了解和学习可信计算知识和技术，并且能够把它们应用到我国信息安全的实践当中。

一血队伍解法

作者：Jemmy@NEX
阅读题目的附件之后，可以看出在这道题中我们主要要做的是：

检查quote_report中的nonce值是否是我们服务器刚才生成的，不符合时直接返回”error”。

确认quote_report->nonce值有效之后，检查quote_report中的pcrValue是否有启用的安全策略，当pcrValue为全0的时候没有任何启用的策略返回”null”，其他值时需要解析启用安全的策略。

在pcrValue非全0时按照“科研-生产-测试-公开”的顺序解析启用的安全策略，有多个策略时两个策略间用”|”分隔。

题目下发的环境是远程的一个Linux服务器，我们需要在这个服务器上修改代码，修复存在的问题之后，运行player.sh就能够获得flag。

我是直接使用VSCode的Remote-SSH插件直接连接到了环境里并安装了C/C++插件，这两年国赛的编程题目我都是这样做的，感觉这样的方式十分好用~不知道大家还有没有什么好方法可以分享一下。

题目的附件中给了我们一些建议，我们先看一下：

我在编写的过程中感觉确实如此，代码中有很多通过宏定义展开的定义，就算利用VSCode的插件也很难招到结构体中的数据内容。通过观察message.log的方式能够更容易地了解到数据结构的内容。

在key_manage.c的这个位置，是生成并返回nonce随机值的地方。

可以看到，程序还将nonce随机值保存在了external_data_store变量中。我们只需要在quote_report中的nonce值与external_data_store变量中的预期nonce值进行比较即可。

我们编写的第一段代码如下：

题目附件中很清楚地描述了，当启用策略为空的时候，pcrValue应该是全0的。在key_manage.c中也特意帮我们定义并清空了一个叫empty_digest的变量，我们只需要用Memcmp来比较pcrValue与empty_digest。

所以第二段代码也很简单

想要解析启用的安全策略，我们就需要知道TCM的PCR扩展是怎样计算的了。

我们可以把PCR看作是一个只能进行三种操作的寄存器，这三种操作分别是：清空、扩展、读取。

清空：当TCM芯片断电之后，其中全部PCR寄存器的值都会被清空，这个时候PCR的值就是全0了。这一个操作只在断电时自动执行，是没有办法通过代码触发的。

扩展：当我们向PCR扩展一个摘要的时候，我们实际上做的操作是newPcrValue = HASH(oldPcrValue || digestValue)，也就是说我们将原来的PCR值oldPcrValue与想要扩展的摘要值digestValue拼接起来，然后再进行一次哈希运算，将结果写入PCR寄存器中。在国产的TCM芯片中，这个HASH操作是SM3算法。

读取：读取PCR的值，我们服务器获取的quote_report中的pcrValue就是这样读取出来的。

我们想要解析启用的安全策略，就需要计算启用不同的安全策略时正确的PCR值。我们知道总共有“科研-生产-测试-公开”这四种安全策略，因此总共有2^4 = 16种可能性。我们可以通过枚举的方式来计算这16种情况下的PCR值，然后与quote_report中的pcrValue进行比较，找到启用的安全策略。

我们首先要记录下，每种安全策略产生的摘要值digestValue，这一部分代码已经在key_manage.c中给出了，我们只需对其做一点点修改，将这些摘要值保存在一个数组里。

我们要小心的是，memdb查询出来的摘要值不是按照“科研-生产-测试-公开”的顺序排列的，因此我们需要判断一下查询到的策略名称，并存入数组中的对应位置。

在这之后，我们就需要穷举16种可能性，判断启用的是哪一些策略了。这4中策略的组合可以用0-15这16个数字来表示，每一个bit对应一个策略的启用状态。在这里我没有开辟新的内存空间，使用了solve_result来存储oldPcrValue || digestValue的拼接结果，哈希之后的newPcrValue存储到了empty_digest中。

在这里调用了一个叫做calculate_context_sm3的函数，这是通过在所有代码文件中搜索”sm3″找到的，根据其他地方的用法可以猜出函数定义是calculate_context_sm3(BYTE const* bufInput, int bufLen, BYTE* outHashBuf)，这个函数的作用是将bufInput中的bufLen个字节进行哈希运算，结果存入outHashBuf中。

接下来要做的就是比较这种组合计算出的pcr值与quote_report中的pcrValue是否相等了。相等的话就找到了启用的安全策略，将这些策略拼接成一个字符串，存入solve_result跳出循环即可。

这样我们就成功地完成了这道题目的所有要求，自己编写部分的完整代码如下：

进入src文件夹后，运行make重新编译，然后运行player.sh，就能够获得flag了。

二血队伍解法

作者：zeroc@F1sh
这道题的关键点在于完善可信报告流程中 crypt_hub 模块中的 key_manage 的代码来实现对重放攻击的检测与报告内容的解析。

首先可以直接运行 tcm_quote.sh 并且通过生成的 instance/crypt_hub/message.log 来了解其执行流程：

首先是启动整个可信计算的流程：

接着进行第一次 pcrquote，由 key_manage 生成随机的 nonce 用于防范重放攻击并返回给 user：

在 key_manage.c 中对应的代码段为：

然后 key_event 在报告中添加用户以及节点信息，由 crypt_user 将 pcr 的值读出后写入报告模板，发送给 key_manage，key_manage 需要将报告转发给 quote_report：

这里的 pcrValue 是使用 Base64 编码后的数据。

在 key_manage.c 中对应的代码为：

由于 quote_report 仅通过用户的密钥来验证消息的完整性，并不具备可信验证的功能，因此在 quote_report 向 key_manage 返回验证结果后，需要 key_manage 对重放攻击进行检测、对可信报告进行解析并将结果返回给 user：

这一段中间就是需要根据我们添加的代码对报告进行解析，并在返回给 user 的 return_value  中写入解析结果。

上面的流程并不难分析，主要通过 key_manage.c 的一些对 recv_msg 的 TYPE_PAIR 类型的判断即可弄明白执行流程，那么这里我们需要做的工作有两个：

判断是否存在重放攻击；

不存在重放攻击的情况下，对 pcrValue 进行解析。

对于第一点，根据上面提到的防范重放攻击的 nonce 来实现，这里通过校验 key_manage 所生成的 nonce 与所接收到的 nonce 是否一致来进行判断，其中第一个 nonce 可以通过以下代码获取：

而对于第二个 nonce 这里，采用了一种取巧的方法，因为并没有对代码进行深入的研究，这里在中间的步骤中插入了一个将 nonce 存储在文件中的逻辑，在后面比较时进行读取即可：

上述即可完成关于重放攻击是否存在的判断，对于 pcrValue 的解析，pcrValue 的生成原理如下：

pcr 实际上是一个 32 字节的寄存器，初始值为全 0，对于每种策略写入时，将当前 pcr 寄存器的值与策略的摘要值进行拼接后使用 SM3 进行哈希得到 pcr 的新值。

这里由于策略总共只有 4 个，并且具有顺序要求，总共只有 15 种情况，也就没费力气在远程找 SM3 的模块，直接将 15 种情况对应的值全部计算出来进行判断即可，加上对重放的检测，全部判断逻辑的代码如下：

将上述代码在 key_manage.c 中补全后运行 player.sh 即可得到 flag：

三血队伍解法

作者：张子怡@北工大信安小队

操作内容：

1、 检查是否有重放攻击
key_manage在阶段一生成的随机数被保存在external_data_store全局变量中，只需和发来消息的随机数quote_report->nonce对比。若相等则随机数是本轮生成的，没有重放。若不相等则有重放。

只需比较pcr和0的值。

获取policy.list中的策略value，按照使用一个策略、两个策略、三个策略、四个策略分别对策略进行排列组合，按照pcr写入的规则，使用sm3计算pcr值。判断计算出的摘要值和消息中的pcr值相等则为该策略，写入solve_result。

相关阅读


```
if (Memcmp(external_data_store, quote_report - > nonce, DIGEST_SIZE) != 0)
// 通过对比回传随机数，确定报告是否为重放报告
{
    Strcpy(solve_result, "error");
} else if (Memcmp(quote_report - > pcrComp.pcrValue, empty_digest, DIGEST_SIZE) == 0) {
    //当Pcr值为全零时，设策略为空
    Strcpy(solve_result, "null");
} else {
    //示例代码：遍历所有策略摘要，顺便对策略数目进行计数
    //因为策略摘要是以哈希表方式存放，因此遍历次序与存入次序无关 
    policy_digest = memdb_get_first_record(TYPE_PAIR(GENERAL_RETURN, UUID));
    while (policy_digest != NULL) {
        record_count++;
        printf("policy name : %s value :", policy_digest - > name);
        print_bin_data(policy_digest - > return_value, 32, 16);
        policy_digest = memdb_get_next_record(TYPE_PAIR(GENERAL_RETURN, UUID));
    }

    BYTE * uuid_list;
    char * name_buf;

    // 分配空间准备按顺序存储策略摘要值
    uuid_list = Talloc0(DIGEST_SIZE * record_count);

    i = 0;
    j = 0;
    // 按照策略写入顺序排序存储策略摘要值
    policy_digest = memdb_get_first_record(TYPE_PAIR(GENERAL_RETURN, UUID));
    while (policy_digest != NULL) {
        for (j = 0; j < record_count; j++) {
            if (policy_seq[j] == NULL)
                break;
            if (Strcmp(policy_seq[j], policy_digest - > name) == 0) {
                Memcpy(uuid_list + j * DIGEST_SIZE, policy_digest - > return_value, DIGEST_SIZE);
                break;
            }
        }
        policy_digest = memdb_get_next_record(TYPE_PAIR(GENERAL_RETURN, UUID));
        i++;
    }

    int choice = 1;
    choice <<= record_count;

    BYTE pcr_emu[DIGEST_SIZE];
    BYTE pcr_buf[DIGEST_SIZE * 2];
    // 遍历对照所有策略,找到匹配的策略组合
    for (i = 1; i <= choice; i++) {
        Memset(pcr_buf, 0, DIGEST_SIZE);
        int temp = i;

        for (j = 0; j < record_count; j++) {
            if (temp % 2) {
                Memcpy(pcr_buf + DIGEST_SIZE, uuid_list + j * DIGEST_SIZE, DIGEST_SIZE);
                calculate_context_sm3(pcr_buf, DIGEST_SIZE * 2, pcr_emu);
                Memcpy(pcr_buf, pcr_emu, DIGEST_SIZE);
            }
            temp >>= 1;
        }
        if (Memcmp(pcr_emu, quote_report - > pcrComp.pcrValue, DIGEST_SIZE) == 0) {
            int k;
            temp = i;
            for (k = 0; k < record_count; k++) {
                if (temp % 2) {
                    if (solve_result[0] == 0)
                        Strcpy(solve_result, policy_seq[k]);
                    else {
                        Strcat(solve_result, "|");
                        Strcat(solve_result, policy_seq[k]);
                    }
                }
                temp >>= 1;
            }
            break;
        }
    }
    printf("solve result: %sn", solve_result);
}
```



```
if (Memcmp(external_data_store, quote_report->nonce, DIGEST_SIZE))
{
    /* quote_report中的nonce 与 external_data_store 中的预期值不符 */
    printf("!!!!!!!!!!!!! Wrong nonce !!!!!!!!!!!!!!n");
    Strcpy(solve_result, "error");
}
```



```
/* 紧接着上一段代码 */
else if (Memcmp(quote_report->pcrComp.pcrValue, empty_digest, DIGEST_SIZE) == 0)
{
    /* pcrValue没有被扩展过，表示启用的策略为空 */
    printf("!!!!!!!!!!!!! Empty policy !!!!!!!!!!!!!!n");
    Strcpy(solve_result, "null");
}
```



```
/* 紧接着上一段代码 */
else
{
    BYTE ServerValues[4][DIGEST_SIZE];
    // find the choiced policies

    // show all the policies
    policy_digest = memdb_get_first_record(TYPE_PAIR(GENERAL_RETURN, UUID));
    while (policy_digest != NULL)
    {
        record_count++;
        printf("policy name : %s value :", policy_digest->name);
        namelen_sum += Strlen(policy_digest->name) + 1;
        print_bin_data(policy_digest->return_value, 32, 16);

        if (!Strcmp(policy_digest->name, "research"))
            Memcpy(ServerValues[0], policy_digest->return_value, DIGEST_SIZE);
        else if (!Strcmp(policy_digest->name, "product"))
            Memcpy(ServerValues[1], policy_digest->return_value, DIGEST_SIZE);
        else if (!Strcmp(policy_digest->name, "test"))
            Memcpy(ServerValues[2], policy_digest->return_value, DIGEST_SIZE);
        else if (!Strcmp(policy_digest->name, "public"))
            Memcpy(ServerValues[3], policy_digest->return_value, DIGEST_SIZE);
        policy_digest = memdb_get_next_record(TYPE_PAIR(GENERAL_RETURN, UUID));
    }

    /* 下一段代码将要补充在这里 */
    /* ...... */
}
```



```
/* 填充在上一段代码中标注的位置 */
    int policyNum;
    for (policyNum = 0; policyNum < 16; ++policyNum)
    {
        /* 清空pcr缓存数组 */
        Memset(solve_result, 0, DIGEST_SIZE * 2);
        int bit;
        for (bit = 0; bit < 4; ++bit)
        {
            if (policyNum & (1 << bit))
            {
                /* 将digestValue拼接到当前PCR值的后面（solve_result偏移DIGEST_SIZE的位置） */
                Memcpy(solve_result + DIGEST_SIZE, ServerValues[bit], DIGEST_SIZE);
                /* 计算新的PCR值，存储到empty_digest中 */
                calculate_context_sm3(solve_result, sizeof(solve_result), empty_digest);
                /* 将新的PCR值再复制回solve_result里 */
                Memcpy(solve_result, empty_digest, DIGEST_SIZE);
            }
        }
        /* 下一段代码将要补充在这里 */
        /* ...... */
    }
    /* 与所有可能的策略组合都不匹配，不应该出现这一情况 */
    Strcpy(solve_result, "unexpected");
```



```
/* 填充在上一段代码中标注的位置 */
        if (Memcmp(quote_report->pcrComp.pcrValue, solve_result, DIGEST_SIZE) == 0)
        {
            printf("!!!!!!!!!!!!! Found policy %d !!!!!!!!!!!!!!n", policyNum);
            /* 清空solve_result变量，来存储结果字符串 */
            Strcpy(solve_result, "");
            /* 表示是否需要拼接'|'符号，第一个解析出的策略不需要，后续需要拼接 */
            int append = 0;

            int bit;
            for (bit = 0; bit < 4; ++bit)
            {
                if (policyNum & (1 << bit))
                {
                    /* 当这一安全策略被启用时 */
                    if (append)
                        Strcat(solve_result, "|"); /* 根据append判断是否需要拼接'|' */
                    /* 拼接安全策略字符串 */
                    Strcat(solve_result, policy_seq[bit]);
                    append = 1;
                }
            }
            goto finish;
        }
```



```
// check program begin
    int record_count = 0;
    int namelen_sum = 0;
    BYTE empty_digest[DIGEST_SIZE];
    char solve_result[DIGEST_SIZE * 2];
    RECORD(GENERAL_RETURN, UUID) * policy_digest;

    Memset(empty_digest, 0, DIGEST_SIZE);
    Memset(solve_result, 0, DIGEST_SIZE * 2);

    if (Memcmp(external_data_store, quote_report->nonce, DIGEST_SIZE))
    {
        printf("!!!!!!!!!!!!! Wrong nonce !!!!!!!!!!!!!!n");
        Strcpy(solve_result, "error");
    }
    else if (Memcmp(quote_report->pcrComp.pcrValue, empty_digest, DIGEST_SIZE) == 0)
    {
        printf("!!!!!!!!!!!!! Empty policy !!!!!!!!!!!!!!n");
        Strcpy(solve_result, "null");
    }
    else
    {
        BYTE ServerValues[4][DIGEST_SIZE];
        // find the choiced policies

        // show all the policies
        policy_digest = memdb_get_first_record(TYPE_PAIR(GENERAL_RETURN, UUID));
        while (policy_digest != NULL)
        {
            record_count++;
            printf("policy name : %s value :", policy_digest->name);
            namelen_sum += Strlen(policy_digest->name) + 1;
            print_bin_data(policy_digest->return_value, 32, 16);

            if (!Strcmp(policy_digest->name, "research"))
                Memcpy(ServerValues[0], policy_digest->return_value, DIGEST_SIZE);
            else if (!Strcmp(policy_digest->name, "product"))
                Memcpy(ServerValues[1], policy_digest->return_value, DIGEST_SIZE);
            else if (!Strcmp(policy_digest->name, "test"))
                Memcpy(ServerValues[2], policy_digest->return_value, DIGEST_SIZE);
            else if (!Strcmp(policy_digest->name, "public"))
                Memcpy(ServerValues[3], policy_digest->return_value, DIGEST_SIZE);
            policy_digest = memdb_get_next_record(TYPE_PAIR(GENERAL_RETURN, UUID));
        }

        int policyNum;
        for (policyNum = 0; policyNum < 16; ++policyNum)
        {
            Memset(solve_result, 0, DIGEST_SIZE * 2);
            int bit;
            for (bit = 0; bit < 4; ++bit)
            {
                if (policyNum & (1 << bit))
                {
                    Memcpy(solve_result + DIGEST_SIZE, ServerValues[bit], DIGEST_SIZE);
                    calculate_context_sm3(solve_result, sizeof(solve_result), empty_digest);
                    Memcpy(solve_result, empty_digest, DIGEST_SIZE);
                }
            }

            if (Memcmp(quote_report->pcrComp.pcrValue, solve_result, DIGEST_SIZE) == 0)
            {
                printf("!!!!!!!!!!!!! Found policy %d !!!!!!!!!!!!!!n", policyNum);
                Strcpy(solve_result, "");
                int append = 0;

                int bit;
                for (bit = 0; bit < 4; ++bit)
                {
                    if (policyNum & (1 << bit))
                    {
                        if (append)
                            Strcat(solve_result, "|");
                        Strcat(solve_result, policy_seq[bit]);
                        append = 1;
                    }
                }
                goto finish;
            }
        }
        /* Not Found */
        Strcpy(solve_result, "unexpected");
    }
finish:
    printf("solve result: %sn", solve_result);

    // check program end
```



```
{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"","receiver_uuid":"","route
    ":"","flow":"FINISH","state":"MATCH","flag":"NULL","ljump":1,"rjump":1,"record_t
    ype":"MESSAGE","record_subtype":"CONN_ACKI","record_num":1,"record_size":151,"ex
    pand_num":0,"expand_size":0,"msg_uuid":"a71819163c8f8caedf94cc09a94684488e476593
    9a5a77533b54955db9032b40"
 },
"RECORD":[
    {
        "uuid":"b16eb1b46c2d00f92a6fb8f3c7c304127fdf4da7db51f195acb18b9e432e71c6","clie
        nt_name":"server","client_proc":"server","client_addr":"unknown addr","server_uu
        id":"b16eb1b46c2d00f92a6fb8f3c7c304127fdf4da7db51f195acb18b9e432e71c6","server_n
        ame":"crypt_hub","service":"trust_server","server_addr":"","flags":0,"nonce":""
    }
    ],
"EXPAND" :[]
}
```



```
{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"7862491328c47d0648b97c5abd1
    5a93442bd1c974b77607314da3c0156bac929","receiver_uuid":"key_manage","route":"quo
    te_nonce","flow":"QUERY","state":"MATCH","flag":"LOCAL","ljump":1,"rjump":2,"rec
    ord_type":"GENERAL_RETURN","record_subtype":"STRING","record_num":1,"record_size
    ":12,"expand_num":0,"expand_size":0,"msg_uuid":"de44c053015ab9b5e531cea46bfa6e96
    c8b0d0b19c890e0ff945005b47da6e1c"
 },
"RECORD":[
    {
        "name":"pcrquote","return_value":"14"
    }
    ],
"EXPAND" :[]
}

************************************************************
{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"key_manage","receiver_uuid"
    :"7862491328c47d0648b97c5abd15a93442bd1c974b77607314da3c0156bac929","route":"quo
    te_nonce","flow":"QUERY","state":"RESPONSE","flag":"NULL","ljump":2,"rjump":2,"r
    ecord_type":"GENERAL_RETURN","record_subtype":"STRING","record_num":1,"record_si
    ze":12,"expand_num":1,"expand_size":0,"msg_uuid":"de44c053015ab9b5e531cea46bfa6e
    96c8b0d0b19c890e0ff945005b47da6e1c"
 },
"RECORD":[
    {
        "name":"pcrquote","return_value":"14"
    }
    ],
"EXPAND" :[
     {
        "data_size":0,"type":"GENERAL_RETURN","subtype":"UUID","expand":
         {
            "name":"pcrquote","return_value":"fded59495cb4a8c1ecae6d8f801fca1f541dffc36cf1e
            d10281bf3323d2722fa"
         }
     }
 ]
}
```



```
// check if there exists random data 
ret = message_remove_expand(recv_msg,TYPE_PAIR(GENERAL_RETURN,UUID),&msg_expand);
if(msg_expand == NULL)
{
 // generate external random data
 RECORD(GENERAL_RETURN,UUID) * external_data;
 external_data=Talloc0(sizeof(*external_data));
 external_data->name=dup_str("pcrquote",0);
 RAND_bytes(external_data->return_value,DIGEST_SIZE);
 Memcpy(external_data_store,external_data->return_value,DIGEST_SIZE);
 ret = message_add_expand_data(recv_msg,TYPE_PAIR(GENERAL_RETURN,UUID),external_data);
 ret=ex_module_sendmsg(sub_proc,recv_msg);
}
```



```
{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"7862491328c47d0648b97c5abd1
    5a93442bd1c974b77607314da3c0156bac929","receiver_uuid":"key_manage","route":"quo
    te_verify","flow":"QUERY","state":"MATCH","flag":"LOCAL","ljump":1,"rjump":2,"re
    cord_type":"GENERAL_RETURN","record_subtype":"STRING","record_num":1,"record_siz
    e":12,"expand_num":2,"expand_size":439,"msg_uuid":"533de83d72e1ee88792152dfbfbf1
    d1026f00167ba4bbd260e86f57c16de396e"
 },
"RECORD":[
    {
        "name":"pcrquote","return_value":"14"
    }
    ],
"EXPAND" :[
     {
        "data_size":0,"type":"MESSAGE","subtype":"INSTANCE_INFO","expand":
         {
            "proc_name":"term","node_uuid":"0fc56bb95fc2a0e6685fec12f31ea1cc03d470fa819f890
            38822b9741741d8b2","user_name":"zhao"
         }
        },
     {
        "data_size":0,"type":"TCM_PIK_DESC","subtype":"PCRQUOTE","expand":
         {
            "userinfo":
             {
                "username":"zhao","user_role":"","node_uuid":"0fc56bb95fc2a0e6685fec12f31ea1cc0
                3d470fa819f89038822b9741741d8b2","node_name":"","expand_digest":"","describe":"q
                uote_report test"
                },
            "pcrComp":
                {
                    "select":
                 {
                        "sizeOfSelect":0,"pcrSelect":"AEAA"
                    },
                "valueSize":32,"pcrValue":"Pg0UXi2+FrqjK47s7+0C50WClHt15b27QjyxccClMz0"
                },
            "nonce":"fded59495cb4a8c1ecae6d8f801fca1f541dffc36cf1ed10281bf3323d2722fa","sign
            Len":64,"signData":"drc3tcDRf33OKS/wKZbBGjP8cKuxIFGixmv+g0mRJAGUtGfYRxcYKyjxnIRt
            yx4BOdTdWUEblhUlLjOtHjoN0w"
            }
        }
    ]
}

// key_manage 向 quote_report 转发信息
{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"key_manage","receiver_uuid"
    :"quote_report","route":"quote_verify","flow":"QUERY","state":"MATCH","flag":"LO
    CAL","ljump":2,"rjump":2,"record_type":"GENERAL_RETURN","record_subtype":"STRING
    ","record_num":1,"record_size":12,"expand_num":2,"expand_size":439,"msg_uuid":"5
    33de83d72e1ee88792152dfbfbf1d1026f00167ba4bbd260e86f57c16de396e"
 },
"RECORD":[
    {
        "name":"pcrquote","return_value":"14"
    }
    ],
"EXPAND" :[
     {
        "data_size":0,"type":"MESSAGE","subtype":"INSTANCE_INFO","expand":
         {
            "proc_name":"term","node_uuid":"0fc56bb95fc2a0e6685fec12f31ea1cc03d470fa819f890
            38822b9741741d8b2","user_name":"zhao"
         }
        },
     {
        "data_size":0,"type":"TCM_PIK_DESC","subtype":"PCRQUOTE","expand":
         {
            "userinfo":
             {
                "username":"zhao","user_role":"","node_uuid":"0fc56bb95fc2a0e6685fec12f31ea1cc0
                3d470fa819f89038822b9741741d8b2","node_name":"","expand_digest":"","describe":"q
                uote_report test"
                },
            "pcrComp":
                {
                "select":
                 {
                    "sizeOfSelect":0,"pcrSelect":"AEAA"
                    },
                "valueSize":32,"pcrValue":"Pg0UXi2+FrqjK47s7+0C50WClHt15b27QjyxccClMz0"
                },
            "nonce":"fded59495cb4a8c1ecae6d8f801fca1f541dffc36cf1ed10281bf3323d2722fa","sign
            Len":64,"signData":"drc3tcDRf33OKS/wKZbBGjP8cKuxIFGixmv+g0mRJAGUtGfYRxcYKyjxnIRt
            yx4BOdTdWUEblhUlLjOtHjoN0w"
            }
        }
    ]
}
```



```
// prepare to verify quote report
printf("server: prepare to verify quote report!n");

RECORD(TCM_PIK_DESC,PCRQUOTE) * quote_report;
quote_report=msg_expand->expand;
DB_RECORD * db_record;
db_record = memdb_store(quote_report,TYPE_PAIR(TCM_PIK_DESC,PCRQUOTE),NULL);
if(db_record == NULL)
{
 printf("server: store quote report failed!n");
}
print_bin_data(db_record->head.uuid,32,16);
ret=ex_module_sendmsg(sub_proc,recv_msg);
```



```
// quote_report 验证消息完整性后返回给 key_manage 的信息，result=0说明验证成功
{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"quote_report","receiver_uui
    d":"key_manage","route":"quote_verify","flow":"QUERY","state":"MATCH","flag":"LO
    CAL","ljump":3,"rjump":2,"record_type":"GENERAL_RETURN","record_subtype":"STRING
    ","record_num":1,"record_size":12,"expand_num":2,"expand_size":439,"msg_uuid":"5
    33de83d72e1ee88792152dfbfbf1d1026f00167ba4bbd260e86f57c16de396e"
 },
"RECORD":[
    {
        "name":"pcrquote","return_value":"14"
    }
    ],
"EXPAND" :[
     {
        "data_size":0,"type":"MESSAGE","subtype":"INSTANCE_INFO","expand":
         {
            "proc_name":"term","node_uuid":"0fc56bb95fc2a0e6685fec12f31ea1cc03d470fa819f890
            38822b9741741d8b2","user_name":"zhao"
         }
        },
     {
        "data_size":0,"type":"TCM_KEY_DESC","subtype":"VERIFY_DESC","expand":
         {
            "result":0,"object_uuid":"8267080f87fc66a093200ca17c4ca06cec4327d1dafcab861955f
            d47c74cf259","verifykey_uuid":""
         }
        }
    ]
}

{
 "HEAD":{
     "tag":"MESG","version":65537,"sender_uuid":"key_manage","receiver_uuid"
    :"7862491328c47d0648b97c5abd15a93442bd1c974b77607314da3c0156bac929","route":"quo
    te_verify","flow":"QUERY","state":"RESPONSE","flag":"NULL","ljump":4,"rjump":2,"
    record_type":"GENERAL_RETURN","record_subtype":"STRING","record_num":1,"record_s
    ize":12,"expand_num":3,"expand_size":439,"msg_uuid":"533de83d72e1ee88792152dfbfb
    f1d1026f00167ba4bbd260e86f57c16de396e"
 },
"RECORD":[
    {
        "name":"pcrquote","return_value":"14"
    }
    ],
"EXPAND" :[
     {
        "data_size":0,"type":"MESSAGE","subtype":"INSTANCE_INFO","expand":
         {
            "proc_name":"term","node_uuid":"0fc56bb95fc2a0e6685fec12f31ea1cc03d470fa819f890
            38822b9741741d8b2","user_name":"zhao"
         }
        },
     {
        "data_size":0,"type":"TCM_KEY_DESC","subtype":"VERIFY_DESC","expand":
         {
            "result":0,"object_uuid":"8267080f87fc66a093200ca17c4ca06cec4327d1dafcab861955f
            d47c74cf259","verifykey_uuid":""
         }
        },
     {
        "data_size":0,"type":"GENERAL_RETURN","subtype":"STRING","expand":
         {
            "name":"policy_choice","return_value":""
         }
        }
    ]
}
```



```
RECORD(TCM_PIK_DESC,PCRQUOTE) * quote_report;
DB_RECORD * db_record;
db_record = memdb_find(verify_desc->object_uuid,TYPE_PAIR(TCM_PIK_DESC,PCRQUOTE));
if(db_record==NULL)
 return -EINVAL;
printf("server: get verified report, verify result is %d!n",verify_desc->result);
quote_report = db_record->record;
char recv_nonce[32];
recv_nocne=quote_report->nonce
```



```
// general quote_report from (TCM_PIK_DESC,QUOTE_REPORT)
{
    RECORD(MESSAGE,INSTANCE_INFO) * instance_info;
    RECORD(TCM_PIK_DESC,PCRQUOTE) * quote_report;
    // get quote nonce value
    printf("key_manage: enter quote report get process!n");
    RECORD(GENERAL_RETURN,UUID) * external_data = msg_expand->expand;
    db_record = memdb_find_first(TYPE_PAIR(TCM_PIK_DESC,PCRQUOTE),"nonce",external_data->return_value);
    FILE *file=fopen("/home/player/tcmenv_question/src/test.txt","w");
    int k=0;
    for(k=0;k<32;k++){
        fprintf(file,"%d ",external_data->return_value[k]);
    }
    fclose(file);
    if(db_record == NULL)
    {
        printf("key_manage: can't find quote report!n");
        return -EINVAL;
    }
    quote_report = db_record->record;
    if(quote_report == NULL)
        return -EINVAL;
    ret = message_add_expand_data(recv_msg,TYPE_PAIR(TCM_PIK_DESC,PCRQUOTE),quote_report);
    ret=ex_module_sendmsg(sub_proc,recv_msg);
    return ret;
}
```



```
FILE *file1=fopen("/home/player/tcmenv_question/src/test.txt","r");
int m=0,number;
char abc[33];
for(m=0;m<32;m++){
    fscanf(file1,"%d",&number);
    abc[m]=(char)number;
}
abc[32]=0;
if(memcmp(quote_report->nonce,abc,32)!=0)
{
    strcpy(solve_result, "error");
}
else {
    char zero[32] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    char research[32] = {0x81,0xe2,0x1b,0xc2,0x48,0x7c,0x1a,0x17,0x9f,0xfc,0xdb,0xd3,0x89,0xf6,0xc3,0xf1,0xa3,0x02,0xcd,0x26,0x8f,0x0c,0x93,0x78,0xd0,0x83,0x9f,0xc6,0xa0,0x8f,0xd5,0xea};
    char product[32] = {0xb2,0x0a,0x7a,0x25,0xc7,0x31,0xd3,0x1b,0x1c,0x2f,0xdf,0xe7,0xcd,0xc4,0xc5,0x3f,0x84,0x6c,0x1b,0x9c,0x0e,0x49,0xbb,0x36,0x2b,0x73,0x41,0x5a,0xa3,0x84,0xce,0xab};
    char test[32] = {0xed,0x7b,0x0f,0xd0,0xcb,0x59,0x0d,0x68,0xd6,0xb6,0xf1,0xfe,0x10,0x81,0x1e,0x57,0x7c,0xde,0x4f,0x74,0x17,0xef,0xc4,0xe8,0x59,0x93,0xe0,0xff,0x9a,0xbf,0x89,0x16};
    char public[32] = {0x62,0xc8,0x08,0xfd,0x91,0x4c,0xe4,0x47,0x7b,0xc3,0xc5,0xe6,0x22,0x96,0x8b,0x5d,0x5f,0xbe,0xad,0xa4,0x45,0x7e,0x91,0x1f,0xa0,0x0d,0x34,0x4a,0xba,0xab,0x80,0x70};
    char researchproduct[32] = {0x20,0x80,0xb4,0xb0,0xb3,0xba,0xc7,0xd2,0x86,0x42,0xb0,0xa9,0x54,0x9b,0xe2,0xdc,0x9e,0x77,0x54,0xb7,0x0d,0x3b,0x96,0x2d,0xbe,0xee,0xe3,0x1b,0x17,0xcb,0x88,0x43};
    char researchtest[32] = {0x3e,0x0d,0x14,0x5e,0x2d,0xbe,0x16,0xba,0xa3,0x2b,0x8e,0xec,0xef,0xed,0x02,0xe7,0x45,0x82,0x94,0x7b,0x75,0xe5,0xbd,0xbb,0x42,0x3c,0xb1,0x71,0xc0,0xa5,0x33,0x3d};
    char researchpublic[32] = {0xad,0x10,0x5b,0x3b,0x59,0xd2,0xde,0x78,0x55,0xa8,0x08,0xca,0x8a,0x74,0x63,0x72,0x62,0x57,0x38,0x23,0xfe,0xdb,0xcd,0x59,0xbd,0x28,0xfb,0x79,0x15,0x5f,0xb4,0x4d};
    char researchtestpublic[32] = {0xdc,0xcb,0x92,0xf5,0x64,0x75,0xa7,0xa9,0xa3,0xd1,0x3d,0x49,0x0d,0x91,0x5a,0x97,0x9e,0xc4,0x4e,0x4c,0x7d,0xfb,0xf5,0x89,0x78,0x48,0xf4,0x98,0xe4,0x85,0x8c,0xdf};
    char researchproductpublic[32] = {0x8f,0x8b,0x61,0x7d,0x08,0xf5,0xd2,0x0e,0x51,0xed,0xfd,0x96,0x50,0xb0,0x28,0x99,0xd4,0x69,0x75,0x09,0xe7,0xc7,0x7f,0xe4,0xa1,0x89,0xf9,0x94,0x97,0xcb,0x95,0x9a};
    char researchproducttest[32] = {0xdd,0x86,0xde,0x23,0xac,0x9b,0x75,0x30,0xca,0x52,0xec,0x2a,0xc4,0x98,0x2f,0x07,0xdf,0x55,0xe4,0xbd,0xe5,0xa7,0xd5,0x98,0x78,0xab,0xa9,0x39,0x60,0x9e,0xa2,0x8e};
    char producttest[32] = {0x2c,0x2d,0xc5,0x73,0xdc,0x11,0xac,0x66,0xb3,0x2c,0x33,0x7e,0x38,0x47,0xdd,0x9d,0x7e,0x6d,0x93,0x25,0xfd,0x8b,0x7f,0x1b,0xb6,0xb6,0x2f,0xcf,0xf6,0xa6,0x0e,0x5b};
    char productpublic[32] = {0x0a,0x19,0xf1,0x13,0x98,0xce,0xdf,0xf0,0x9d,0x1c,0x35,0x95,0x60,0x26,0x97,0xaf,0x89,0x2b,0xdc,0x09,0xbd,0xdf,0x1e,0x9e,0x85,0xf0,0xa0,0x73,0x91,0xc3,0x54,0x5b};
    char producttestpublic[32] = {0xc5,0x01,0xba,0x81,0x3c,0xa3,0x86,0x2a,0x3b,0xdf,0x14,0xa2,0x34,0x12,0x41,0xe9,0xe2,0x97,0x9f,0xee,0xaf,0x27,0x90,0x22,0x73,0x53,0x9f,0x8e,0x0f,0xde,0x4f,0x2a};
    char testpublic[32] = {0xc8,0x11,0xe3,0x69,0x89,0xc2,0x50,0x9f,0xc1,0x9a,0xd3,0xc7,0xcf,0xac,0x5f,0x0f,0x69,0xfa,0x23,0xde,0x40,0xce,0x03,0x90,0x44,0x3b,0x68,0xdd,0xb1,0xde,0x9f,0x5f};
    char researchproducttestpublic[32] = {0x6e,0x03,0x3d,0x5a,0x4d,0x38,0x3a,0x80,0x52,0xc2,0x4a,0x11,0xe1,0x22,0x77,0x43,0x88,0x0c,0x35,0x9d,0xfc,0x18,0x64,0x36,0x2c,0xcd,0xee,0x07,0x7b,0x10,0x6d,0x37};
    if(memcmp(quote_report->pcrComp.pcrValue, zero, 32)==0) {
        strcpy(solve_result,"null");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, research, 32)==0) {
        strcpy(solve_result,"research");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, product, 32)==0) {
        strcpy(solve_result,"product");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, test, 32)==0) {
        strcpy(solve_result,"test");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, public, 32)==0) {
        strcpy(solve_result,"public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchproduct, 32)==0) {
        strcpy(solve_result,"research|product");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchtest, 32)==0) {
        strcpy(solve_result,"research|test");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchpublic, 32)==0) {
        strcpy(solve_result,"research|public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchtestpublic, 32)==0) {
        strcpy(solve_result,"research|test|public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchproductpublic, 32)==0) {
        strcpy(solve_result,"research|product|public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchproducttest, 32)==0) {
        strcpy(solve_result,"research|product|test");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, producttest, 32)==0) {
        strcpy(solve_result,"product|test");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, productpublic, 32)==0) {
        strcpy(solve_result,"product|public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, producttestpublic, 32)==0) {
        strcpy(solve_result,"product|test|public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, testpublic, 32)==0) {
        strcpy(solve_result,"test|public");
    }
    else if(memcmp(quote_report->pcrComp.pcrValue, researchproducttestpublic, 32)==0) {
        strcpy(solve_result,"research|product|test|public");
    }
}
```



```
int flag_error=0;
if(!memcmp(quote_report->nonce,external_data_store,DIGEST_SIZE)){
    printf("!!!!!!!!!!!!no_replace!!!!!!!!!!!!!!!!!!n"); }
else{
    printf("!!!!!!!!!!!!yes_replace!!!!!!!!!!!!!!!!!!n");
    flag_error=1;
}
```



```
int flag_null=0;
BYTE zero[DIGEST_SIZE];
memset(zero,0,DIGEST_SIZE);
if(!memcmp(quote_report->pcrComp.pcrValue,zero,DIGEST_SIZE)){
    flag_null=1;
}
```



```
//获取value值
if (!strcmp(policy_digest - > name, research))
    memcpy(re, policy_digest - > return_value, DIGEST_SIZE);
else if (!strcmp(policy_digest - > name, product))
    memcpy(pro, policy_digest - > return_value, DIGEST_SIZE);
else if (!strcmp(policy_digest - > name, test))
    memcpy(te, policy_digest - > return_value, DIGEST_SIZE);
else if (!strcmp(policy_digest - > name, public))
    memcpy(pub, policy_digest - > return_value, DIGEST_SIZE);
else
    printf("!!!!!!!!!!!!!!!!!!!!!!!!!n");

//解析策略值
///one
// memset(empty_digest,0,DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "product");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "test");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "public");

///two
memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|product");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|test");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|public");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "product|test");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "product|pub");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "test|public");

///three
memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|product|test");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|product|public");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|test|public");

memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "product|test|public");

///four
memset(empty_digest, 0, DIGEST_SIZE);
memcpy(empty_digest + DIGEST_SIZE, re2, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pro, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, te, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
memcpy(empty_digest + DIGEST_SIZE, pub, DIGEST_SIZE);
calculate_context_sm3(empty_digest, 2 * DIGEST_SIZE, empty_digest);
if (!memcmp(empty_digest, quote_report - > pcrComp.pcrValue, DIGEST_SIZE)) strcpy(solve_result, "research|product|test|public");

if (flag_error == 1) strcpy(solve_result, "error");
if (flag_null == 1) strcpy(solve_result, "null ");
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/4-1685544871.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/3-1685544871.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/4-1685544872.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/9-1685544872.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/9-1685544872.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/05/10-1685544874.gif)