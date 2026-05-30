# 2024 CISCN x 长城杯 初赛逆向0解题-VT 解题全流程

> 原文: https://www.ctfiot.com/232235.html
> ID: 232235

作者论坛账号：Tkazer

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
uint32_t calc(uint8_t* data, int len)
{
        uint32_t ret_value = -1;
        for (int count = 0; count < len; count++)
        {
                ret_value ^= data[count];
                for (int i = 0; i < 8; i++)
                {
                        if (ret_value & 1)
                        {
                                ret_value = (ret_value >> 1) ^ 0xEDB88320;
                        }
                        else
                        {
                                ret_value >>= 1;
                        }
                }
        }
        return ~ret_value;
}
复制代码 隐藏代码
    #include 

uint32_t calc(uint8_t* data, int len)
{
        uint32_t ret_value = -1;
        for (int count = 0; count < len; count++)
        {
                ret_value ^= data[count];
                for (int i = 0; i < 8; i++)
                {
                        if (ret_value & 1)
                        {
                                ret_value = (ret_value >> 1) ^ 0xEDB88320;
                        }
                        else
                        {
                                ret_value >>= 1;
                        }
                }
        }
        return ~ret_value;
}

int main()
{
        short Param1 = 0;
    // 爆破2字节
        for (int i = 0; i < 0xffff; i++)
        {
                Param1 = i;
        // ida条件断点得到的key值列表
                uint8_t KeyList[]{
                        82,225,68,226,57,225,94,155,81,220,
                        25,152,80,146,57,193,80,158,82,130,
                        39,130,38,231,83,128,36,128,66,220,
                        57,158,2,148,39,129,69,131,81,147,
                        2,128,68,129,68,129,68,129 };
                uint8_t Enc[48]{};
                uint8_t* pParam1 = (uint8_t*)(uint64_t)(&Param1);

        // calc之前的异或计算
                for (int j = 0; j < 48; j++)
                {
                        Enc[j] = pParam1[j % 2] ^ KeyList[j];
                }

                auto calc_value = calc(Enc, 48);
                if (calc_value == 0xF703DF16)
                {
                        printf("Cracked:%02X%02Xn", pParam1[0], pParam1[1]);
                        break;
                }
        }

        return0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-4438290622337b0a301031419ead2dc6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-1c694600bb648825ec0765136cf40dbc.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-808bdb4c635f80dceed771b972f30189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-db54cfe2643dcf36c4e23bb2d870886d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-48d496f7d8ca0dcc0ec4eb98daec02ce.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-45e81d6ec7ea828b7d7f1a4c0552b9d1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-a7fba504a19fd27e615b3d7874db0bea.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-1821dcfc475d17ace3c41dc31116ab03.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-cb36f321dd69053d6df837218019b5ab.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/03/wxsync-2025-03-52967cf7cccb50bbb2ebff63aadaf3e2.png)