# 腾讯云安全挑战赛·COS提权与利用 WP

> 原文: https://www.ctfiot.com/271105.html
> ID: 271105

点击蓝字

关注我们

声明

本文作者：neko本文字数：5274字

阅读时长：约15分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

腾讯云安全挑战赛 COS提权与利用

2025-09-10 10:00:00 至 2025-09-14 20:00:00

https://zc.tencent.com/competition

COS提权与利用，点击开始挑战，会创建一个环境，并且给一个jar包。

这次我们团队研究出了两种解题思路，这里放出来供大家一起参考学习，师傅们还有更多思路可以在评论区留言交流～，点击加群按钮发送 云安全 可加入交流群。

作者

Neko

每一个地方都有可学习的知识

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
AbstractHashMap中存在加解密逻辑以及密钥private static String LiLiLLLiiiLLiiLLi = "Q8Ro9cHYVAdBaRD8";这个是AES密钥CrackMe中存在大量xor加密内容static { GIiIiLA.add("et/PKBfnONJfu7xmL9JR+NN2OfYfr0UsEq+h56UuhghQmwDY/NpzRY1203tEnFTGKXGFtlXDGddgdzsIadgQbwqDwV3gD8wU95Fzxxx2ELw="); GIiIiLA.add("UttCT9jj0Abx/BonoRnVDapMG29jd58oCoQTQM8mpDlXEFSmDPv9hVYOdTzocqHImJeRne0y2LYXsH1TabbMPL3L8oHM1q+yOOXjKtWjjLSdkC/eQ26vqSG4NMWbjIq6TkW1AWxzLFRw+E0VLNhyCEHwzNB+LVTS3FXkyTK1lzffuKXzbR+N+2nawgPg3FM5RtrN/bITV+U/rWJdgd7QcyMZZz0XIeGdaBShZ/gn23c="); GIiIiLA.add("+VDxoUvEOGFLmzYk2rMuQQ=="); GIiIiLA.add("5W2GvnjuVloFILjAr252UQ=="); GIiIiLA.add("OPSuJq77r95Vt5BMQvmlq9thxi6gXHrvufXkPYxZbAQ="); GIiIiLA.add("Fs7sFJP3PWMkALT4xp8Now=="); GIiIiLA.add("Fs7sFJP3PWMkALT4xp8Now=="); GIiIiLA.add("xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ="); GIiIiLA.add("bPF0xv4MwrLyDXGFDwinsQ=="); GIiIiLA.add("e4X/u1BffArwH4yhQbMbC/bK92Pa8L/uKxGcAAs2nJs="); GIiIiLA.add("xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ="); GIiIiLA.add("xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ="); GIiIiLA.add("FJxfLbo6rzGFZdTPsEYqztthxi6gXHrvufXkPYxZbAQ="); GIiIiLA.add("cQi4+TSZGSXO7WMPWx5Hnx4PPt5BHBEzcg0F7aGWEyPBsjVxZ/kKpRar+peUj1Ek"); GIiIiLA.add("cQi4+TSZGSXO7WMPWx5Hn4btogYL6S3VIqqq0BnMEknBsjVxZ/kKpRar+peUj1Ek"); GIiIiLA.add("cQi4+TSZGSXO7WMPWx5Hn1Iiaa41jVNbC/tROKX6UEve3TMqlmumJ+OhGFl95w+q"); GIiIiLA.add("DO3IcaKrhrZGwiKjLBkljA=="); GIiIiLA.add("22HGLqBceu+59eQ9jFlsBA=="); GIiIiLA.add("QnBlhV2AwD8tdPd/zaq5dxxP/VC2kkn0mn+gDNNAWi8ZMwALth4id6O/6ZFMKRTyXhiQFxz1/bvq99ldKYvxOw6WbtJ92/l1N7BCDnDdd9bcumdYPP8TBkgAi89j29uZ"); GIiIiLA.add("xuYEVBmRA8/1kHZURfiq2FlqHvlCtPmHXO3bGolRIJP8d7gA5Fwgmz1Qbj1aU1UJegGY4RdwaGtnCBFqqKI3FA=="); GIiIiLA.add("3OBVSOApuWl0PPqu3xau0qaz40nY2K894jJ1tWzJwDBr6A0pvJ5k9ACRPEK975+VCl/6iEHBbDYbK0x3aewqiJHWXgWQE7W+X46lDYdBVa96ZV8+wlgZYJj4mcMRZb/2pQF5U3AG+iFHqkcUA7OnD6aaa+QRWar/g/iC1FuicKD+muempacvGqCcl+ZtkhkPzuC0u9QK0akptBl2krF3Z+SFW/eN1D5iW4NR0tFbdLNrfkMiQp+dtGq/JVS+Jtirvk0taG35AkDON+SPjF2OvGuUd6/3fjdUHE0SOg9039TXp6jN+Yhzwm4gDkcnqcFBPVrSM9N2cgm2VstPy0MCha3J4aaMEk5/+oR4iyywfw2PZmmHeOg4DavFBxaax1L65Wxe+joD1v2Be8T/+ORicmaAb3RPq4QA5I7RZR4k/AtqYsnqRnGb7cbiePbQdCyiGWUcboIaeHWPzKOrHMyvEL1JsMYtYQvdBKWjY/MRvkHWDAAG0rvo94iNcgmxa7OvayxPmbSNHzVVQTlgWY8gBszkgfIQmLZ9N+zISMad9/E0IOtyu0qGXvLJKrTzBB127MqY9cr2w9eIhU5dI+mEJQPUTbdvk8vHH6zp51wxOC6d7MOPro9gOFV5AtNVT8trh1aoU3FnW/WSVxY7gsF1BbDExqPI/tBr/N8amFUU6AI+wwYf9wy/HZy4JXHAYOPe1GUQ77+sI5byWuv2ck2hx101s+edcNjUB2M5wmAy9JShNr0CmRzVFg5VxQIoo7VrA1wqjuWIhsVa4lAT6pF5gcw6iihaY2yt4TUlhlyRfrfyPpJJju5J7YbcH2G9boqnHKEI4EODwORbTXfxNAljeicwc4kyTVkqTtRP6hQX518UugqqpAFG59N70g4biim5YC0ZwV2KLqr9WiojeFZFtK+haiMBB9kCY5JIo/gXl7lt0T6ZNveNZWoaaapGNH1LrxFWMVCiCB+mJn2vtn8fPolcKfUZT3KGg6w98xqKwydYN2B/Cwx0ycclh3xD3wX5ghzcPuObljFbknJLBiYjz3NW9+6hNvbSdvaRc+4oMzO9eTRDcGr0UVbZ1CPKQGRorC5hs31HswHop9tTyVW0Q7iSfrtd4kFyZ7ngoQtpsIyjAxAjG9MGUwnvHQecI/QbML94szHUiY5Y1fQJ9sCxTEf1K9LbhJw2+ly1OUHW1wouU/vEKgN0AybcLgmjZtprIu6vT0Qhk/cJLEanINCzhCzB312mJg5GRsv/tgrPnNjizH6Ca4cl+4BKjLUv7CbJNi49bSvxJ7yLlnbWfXR7cQ=="); GIiIiLA.add("xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ="); GIiIiLA.add("8We0FEiIidCS4oPIqKpA/o6AjxC3EQ/0vOiXv9iP+fYSk6xBzI06Lcyr/xPb4Gdb22HGLqBceu+59eQ9jFlsBA=="); GIiIiLA.add("PW/w96ZBN2XlpfC4XNnPsc7Gj4/4PTHV0+lWesFkJSz3BXar7xTfOU4p//Muq6ZY"); GIiIiLA.add("6JH45v4QgiEN39TgOJs+p38Hnxj62dKlTNH9+GL+ouI=");
import base64from Crypto.Cipher import AES
# 从1.txt提取的新AES密钥KEY = "Q8Ro9cHYVAdBaRD8".encode('utf-8')
# AES解密函数
def aes_decrypt(encrypted_data): try: cipher = AES.new(KEY, AES.MODE_ECB) decoded_data = base64.b64decode(encrypted_data) decrypted_data = cipher.decrypt(decoded_data) pad_len = decrypted_data[-1] return decrypted_data[:-pad_len].decode('utf-8', errors='ignore') 
except Exception as e: return f"AES解密失败: {str(e)}"# 计算deobfuscate参数
def calculate_obfuscation_params(): # i_start计算式：(11963830 ^ 57816743) ^ (15501129 ^ 52968536) a = 11963830 ^ 57816743 b = 15501129 ^ 52968536 i_start = a ^ b # xor_key计算式：(95558172 ^ 72233696) ^ (85510964 ^ 82109419) c = 95558172 ^ 72233696 d = 85510964 ^ 82109419 xor_key = c ^ d return i_start, xor_key
# deobfuscate处理
def deobfuscate(data_str, i_start, xor_key): try: decode = base64.b64decode(data_str) decode_list = list(decode) for i in range(i_start, len(decode_list)): decode_list[i] = decode_list[i] ^ xor_key return bytes(decode_list).decode('utf-8', errors='ignore') 
except Exception as e: return f"Deobfuscate失败: {str(e)}"# 从2.txt提取的GIiIiLA数组前20项GIiIiLA = [ "et/PKBfnONJfu7xmL9JR+NN2OfYfr0UsEq+h56UuhghQmwDY/NpzRY1203tEnFTGKXGFtlXDGddgdzsIadgQbwqDwV3gD8wU95Fzxxx2ELw=", "UttCT9jj0Abx/BonoRnVDapMG29jd58oCoQTQM8mpDlXEFSmDPv9hVYOdTzocqHImJeRne0y2LYXsH1TabbMPL3L8oHM1q+yOOXjKtWjjLSdkC/eQ26vqSG4NMWbjIq6TkW1AWxzLFRw+E0VLNhyCEHwzNB+LVTS3FXkyTK1lzffuKXzbR+N+2nawgPg3FM5RtrN/bITV+U/rWJdgd7QcyMZZz0XIeGdaBShZ/gn23c=", "+VDxoUvEOGFLmzYk2rMuQQ==", "5W2GvnjuVloFILjAr252UQ==", "OPSuJq77r95Vt5BMQvmlq9thxi6gXHrvufXkPYxZbAQ=", "Fs7sFJP3PWMkALT4xp8Now==", "Fs7sFJP3PWMkALT4xp8Now==", "xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ=", "bPF0xv4MwrLyDXGFDwinsQ==", "e4X/u1BffArwH4yhQbMbC/bK92Pa8L/uKxGcAAs2nJs=", "xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ=", "xCPI5tDZJkFIUbHqUO5UoRCWq77rr5pYDz48byPJTQQ=", "FJxfLbo6rzGFZdTPsEYqztthxi6gXHrvufXkPYxZbAQ=", "cQi4+TSZGSXO7WMPWx5Hnx4PPt5BHBEzcg0F7aGWEyPBsjVxZ/kKpRar+peUj1Ek", "cQi4+TSZGSXO7WMPWx5Hn4btogYL6S3VIqqq0BnMEknBsjVxZ/kKpRar+peUj1Ek", "cQi4+TSZGSXO7WMPWx5Hn1Iiaa41jVNbC/tROKX6UEve3TMqlmumJ+OhGFl95w+q", "DO3IcaKrhrZGwiKjLBkljA==", "22HGLqBceu+59eQ9jFlsBA==", "QnBlhV2AwD8tdPd/zaq5dxxP/VC2kkn0mn+gDNNAWi8ZMwALth4id6O/6ZFMKRTyXhiQFxz1/bvq99ldKYvxOw6WbtJ92/l1N7BCDnDdd9bcumdYPP8TBkgAi89j29uZ", "xuYEVBmRA8/1kHZURfiq2FlqHvlCtPmHXO3bGolRIJP8d7gA5Fwgmz1Qbj1aU1UJegGY4RdwaGtnCBFqqKI3FA==" "3OBVSOApuWl0PPqu3xau0qaz40nY2K894jJ1tWzJwDBr6A0pvJ5k9ACRPEK975+VCl/6iEHBbDYbK0x3aewqiJHWXgWQE7W+X46lDYdBVa96ZV8+wlgZYJj4mcMRZb/2pQF5U3AG+iFHqkcUA7OnD6aaa+QRWar/g/iC1FuicKD+muempacvGqCcl+ZtkhkPzuC0u9QK0akptBl2krF3Z+SFW/eN1D5iW4NR0tFbdLNrfkMiQp+dtGq/JVS+Jtirvk0taG35AkDON+SPjF2OvGuUd6/3fjdUHE0SOg9039TXp6jN+Yhzwm4gDkcnqcFBPVrSM9N2cgm2VstPy0MCha3J4aaMEk5/+oR4iyywfw2PZmmHeOg4DavFBxaax1L65Wxe+joD1v2Be8T/+ORicmaAb3RPq4QA5I7RZR4k/AtqYsnqRnGb7cbiePbQdCyiGWUcboIaeHWPzKOrHMyvEL1JsMYtYQvdBKWjY/MRvkHWDAAG0rvo94iNcgmxa7OvayxPmbSNHzVVQTlgWY8gBszkgfIQmLZ9N+zISMad9/E0IOtyu0qGXvLJKrTzBB127MqY9cr2w9eIhU5dI+mEJQPUTbdvk8vHH6zp51wxOC6d7MOPro9gOFV5AtNVT8trh1aoU3FnW/WSVxY7gsF1BbDExqPI/tBr/N8amFUU6AI+wwYf9wy/HZy4JXHAYOPe1GUQ77+sI5byWuv2ck2hx101s+edcNjUB2M5wmAy9JShNr0CmRzVFg5VxQIoo7VrA1wqjuWIhsVa4lAT6pF5gcw6iihaY2yt4TUlhlyRfrfyPpJJju5J7YbcH2G9boqnHKEI4EODwORbTXfxNAljeicwc4kyTVkqTtRP6hQX518UugqqpAFG59N70g4biim5YC0ZwV2KLqr9WiojeFZFtK+haiMBB9kCY5JIo/gXl7lt0T6ZNveNZWoaaapGNH1LrxFWMVCiCB+mJn2vtn8fPolcKfUZT3KGg6w98xqKwydYN2B/Cwx0ycclh3xD3wX5ghzcPuObljFbknJLBiYjz3NW9+6hNvbSdvaRc+4oMzO9eTRDcGr0UVbZ1CPKQGRorC5hs31HswHop9tTyVW0Q7iSfrtd4kFyZ7ngoQtpsIyjAxAjG9MGUwnvHQecI/QbML94szHUiY5Y1fQJ9sCxTEf1K9LbhJw2+ly1OUHW1wouU/vEKgN0AybcLgmjZtprIu6vT0Qhk/cJLEanINCzhCzB312mJg5GRsv/tgrPnNjizH6Ca4cl+4BKjLUv7CbJNi49bSvxJ7yLlnbWfXR7cQ=="]# 计算参数i_start, xor_key = calculate_obfuscation_params()print(f"计算得到i_start: {i_start}, xor_key: {xor_key}")
# 执行解密decrypted_results = []for idx, item in enumerate(GIiIiLA): aes_result = aes_decrypt(item) deob_result = deobfuscate(aes_result, i_start, xor_key) if not aes_result.startswith("AES解密失败") else "N/A" decrypted_results.append(f"元素 {idx}:
nAES解密: {aes_result}nDeobfuscate结果: {deob_result}n{'-'*50}")
# 保存结果with open("新一轮解密结果_v2.txt", "w", encoding="utf-8") as f: f.write("n".join(decrypted_results))print("新一轮解密结果已保存到 '新一轮解密结果_v2.txt'")
元素 0:
AES解密: https://1368851814-lkdv0r76fv.ap-guangzhou.tencentscf.com/challenge_001Deobfuscate结果: J|z>i(/}䄕<QQ5Xn--------------------------------------------------元素 1:
AES解密: {"data":"Z0FBQUFBQm93OXZTemNpMzNNQTdHRzNveFpYTjNRWmhmVU5McV9xTGpzRkRZUExIcFFOa1RsOFdWN2o0Tkp3V0NQbWdHN05UbmpWNWVpOW1ra2F1UnhjUWZIYmZkOXdwdG1EV0JfSGQwLTdkaFZzSEMtZW5yeGc9"}Deobfuscate结果: VyDbbbbbaLTUpY@JnbddL[y{mryKEvmoR|RoIPegzsokSrmHwOtuImiTt`sNDdmwMIuFJNHHBVq[@rEkAEGTSWNgta|kGGKuPk`FMQ[D--------------------------------------------------元素 2:
AES解密: POSTDeobfuscate结果: ǰ--------------------------------------------------元素 3:
AES解密: Content-TypeDeobfuscate结果: Deobfuscate失败: Incorrect padding--------------------------------------------------元素 4:
AES解密: application/jsonDeobfuscate结果: IF厩ܭ--------------------------------------------------元素 5:
AES解密: utf-8Deobfuscate结果:--------------------------------------------------元素 6:
AES解密: utf-8Deobfuscate结果:--------------------------------------------------元素 7:
AES解密: [获取COS地址失败]Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 8:
AES解密: http://Deobfuscate结果: Deobfuscate失败: Incorrect padding--------------------------------------------------元素 9:
AES解密: .cos.ap-guangzhou.myqcloud.comDeobfuscate结果: Deobfuscate失败: Invalid base64-encoded string: number of data characters (25) cannot be 1 more than a multiple of 4--------------------------------------------------元素 10:
AES解密: [获取COS地址失败]Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 11:
AES解密: [获取COS地址失败]Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 12:
AES解密: Java CrackMe CTFDeobfuscate结果: Deobfuscate失败: Incorrect padding--------------------------------------------------元素 13:
AES解密: 请输入云服务临时凭据AK:
Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 14:
AES解密: 请输入云服务临时凭据SK:
Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 15:
AES解密: 请输入云服务临时凭据TOKEN:
Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 16:
AES解密: 提交Deobfuscate结果: Deobfuscate失败: string argument should contain only ASCII characters--------------------------------------------------元素 17:
AES解密:
Deobfuscate结果:--------------------------------------------------元素 18:
AES解密: YmhqZxBGdlJ1E3F3R2tCcXIVc0ZaZVlMVnV1cFBHEkAWTHYXR0RbW25wR0ZTWlpwWg4Qd1lhdRFiUBZBUE51eUYVb3Q=Deobfuscate结果: AKID3eUqV0RTdHaRQ6PeyFzouVVSsd1c5oU4dgxxMSdepyySy-3TzBV2As5bsmVZe6LW--------------------------------------------------元素 19:
AES解密: FUpJQk9GSE5zE1QWQRdKSkJXdnl1UUprV0cQSmd3UxobUEFMVAxmS2RkZh4=Deobfuscate结果: 6ijalekmP0w5b4iiatUZVriHtd3iDTp98sbow/EhGGE=--------------------------------------------------### 元素20解密结果元素20:
AES解密结果: G3F0VFdLe2AQUUtvUlJQFRN1V0hFR1FoEXJ1V3FPVkISRkJAGhpGGkFHE0UTGxIVGhoQERBCQhtGGkVBRUITFWdaemITSkURalNGG3daTRVSSBVRelZUZGdpVlppR3dLGxZGZFRAdBFHYWJocRZORWpSdGlFZFBbFVoXYGZIWxFaWRUUSBpKbUpFYGpXUm9GE3VrT1VRaWpvSWZUEBV6cWoOcW1taFpSekoUYGR7ERJrS1ZvS0FiS2pgWhVGUWlJZXYRSkATYRpGc2hZT1ZpYHkOGk1oFmRwSmkTckt0E2tmW3lucWYSTWxJEGlBURpUW2V3S25MdFdnEm9lb0hnQFkXWmpLcFR2VklaaWtIdE1EQXBzanVBUE53dGoOe1txTkBCZ2F3GkFpGmYVc0dJdXBFZlMaa0h8EEJMRU5CUFFHb3kRWkVgZnlNF2gaUGhrb0ZEUm9LWnJSU2xSYQ5AFHdEbXNraHdMahd5bHxOGhVLaXYUFU1mGlBlFnxscxRTR050RVYUfEgSfFFSaExbThQOF2plDkpmGhViU2VodRZMYGtyS1BmUxVPRnpsRRVwFGZ2QFt8QBdiE1Nqd3lzRWxhfBByc3tpVktAQmR8VkZ7QnpIS0d1F3dvWUxPU0REb3ATQmF5UmhNdk8RQRdpDhNRTFREU0dIRBViVEV6DmpNdBpGWnlQQmBxG257Z1lwF1B0a3QWUkZLdhRabUARbHB8URdPYkpqVGEbdRBRQFJIR2lVWWpQEmRXW1ZRaFkXUU9MTE9TVhRhbHNnFmYTFFJMSBFpSklmTGlwGlBZehdySVp7TxFBaEZSbUQVamVSFVJNcXcXV09rYXtuS3UVQVJ1elpLUUZXRw5FeRVLbBdqV2drQhNCb1pWZk95EnRzEHZCb0JWeUBLelZRVhVzRXwWG1oaS3BUEUpmFkxxRHsSeUVGehp5TkZmRHF0EHN5ERtRU2Zyu0008u0008u0008u0008u0008u0008u0008u0008Deobfuscate结果: (待处理)--------------------------------------------------Deobfuscate结果: 8RWwthXC3rhLqqs60VtkfdrK2QVtRlua1eac99e9bd0f081699323aa8e9fbfa06DyYA0if2Ipe8Tyn6qk6rYuwGDJuyJdTh85eGwcW2dBAKR5mfIqWJfGsx6y4CEkx2yz67k9iNifCItqLe0VHlvrJILjEw36YRI-RNNKyqYi7CGX21HhuLhbAhICy6erJjFU2ic0B9ePKzluJCZ-9nK5GSiJ0QhW0HExZMRE1nOj3Jbr9wxFThMoWtD1LFLkDcz4yIhSwUujyJHkWngbSPIVbsmTWI-XxRmcaDBT9bJ9E6PdjVSfEp9Hk_3aofmasrdLZ2yfCEZn4K9sKHLegqLhyQqpOqB-c7TgNPHKToI4ZO_m96hJU76nE9sF5_OP7pdmWfu7_k1_rqKoxm7-4IF-iE96ApFKV5oCHQhsEp6leYOf6S7EUcx_c4A0pITZPfOB_3QPXJuhcaG_ueXaYkhdV4TLzolpggLS0aBZqKnUl2b4J-0rowgpdkg6AwfY-InW9eyZsaCR8MXDzS4sWHW5qehU7yNc2OS_r4lAiIwB8V3rcqkdJvzIs1GtxurKz4rloolpu7BOPD5E07qok2JijEoJS9szY4QjyXl2bKeqNg6IFq6qnRT4tlHBXMhV6bqVYyhretd-fZ6hO4ItDHa0aLyuElZ1WP3UaLauZchYuru6Pf_58y9hSw2iE5oRgX1ZfeY9ZmeEgRW3PZ28rpEQ--------------------------------------------------
元素 18:
AES解密: YmhqZxBGdlJ1E3F3R2tCcXIVc0ZaZVlMVnV1cFBHEkAWTHYXR0RbW25wR0ZTWlpwWg4Qd1lhdRFiUBZBUE51eUYVb3Q=Deobfuscate结果: AKID3eUqV0RTdHaRQ6PeyFzouVVSsd1c5oU4dgxxMSdepyySy-3TzBV2As5bsmVZe6LW--------------------------------------------------元素 19:
AES解密: FUpJQk9GSE5zE1QWQRdKSkJXdnl1UUprV0cQSmd3UxobUEFMVAxmS2RkZh4=Deobfuscate结果: 6ijalekmP0w5b4iiatUZVriHtd3iDTp98sbow/EhGGE=--------------------------------------------------### 元素20解密结果元素20:
AES解密结果: G3F0VFdLe2AQUUtvUlJQFRN1V0hFR1FoEXJ1V3FPVkISRkJAGhpGGkFHE0UTGxIVGhoQERBCQhtGGkVBRUITFWdaemITSkURalNGG3daTRVSSBVRelZUZGdpVlppR3dLGxZGZFRAdBFHYWJocRZORWpSdGlFZFBbFVoXYGZIWxFaWRUUSBpKbUpFYGpXUm9GE3VrT1VRaWpvSWZUEBV6cWoOcW1taFpSekoUYGR7ERJrS1ZvS0FiS2pgWhVGUWlJZXYRSkATYRpGc2hZT1ZpYHkOGk1oFmRwSmkTckt0E2tmW3lucWYSTWxJEGlBURpUW2V3S25MdFdnEm9lb0hnQFkXWmpLcFR2VklaaWtIdE1EQXBzanVBUE53dGoOe1txTkBCZ2F3GkFpGmYVc0dJdXBFZlMaa0h8EEJMRU5CUFFHb3kRWkVgZnlNF2gaUGhrb0ZEUm9LWnJSU2xSYQ5AFHdEbXNraHdMahd5bHxOGhVLaXYUFU1mGlBlFnxscxRTR050RVYUfEgSfFFSaExbThQOF2plDkpmGhViU2VodRZMYGtyS1BmUxVPRnpsRRVwFGZ2QFt8QBdiE1Nqd3lzRWxhfBByc3tpVktAQmR8VkZ7QnpIS0d1F3dvWUxPU0REb3ATQmF5UmhNdk8RQRdpDhNRTFREU0dIRBViVEV6DmpNdBpGWnlQQmBxG257Z1lwF1B0a3QWUkZLdhRabUARbHB8URdPYkpqVGEbdRBRQFJIR2lVWWpQEmRXW1ZRaFkXUU9MTE9TVhRhbHNnFmYTFFJMSBFpSklmTGlwGlBZehdySVp7TxFBaEZSbUQVamVSFVJNcXcXV09rYXtuS3UVQVJ1elpLUUZXRw5FeRVLbBdqV2drQhNCb1pWZk95EnRzEHZCb0JWeUBLelZRVhVzRXwWG1oaS3BUEUpmFkxxRHsSeUVGehp5TkZmRHF0EHN5ERtRU2Zyu0008u0008u0008u0008u0008u0008u0008u0008Deobfuscate结果: (待处理)Deobfuscate结果: 8RWwthXC3rhLqqs60VtkfdrK2QVtRlua1eac99e9bd0f081699323aa8e9fbfa06DyYA0if2Ipe8Tyn6qk6rYuwGDJuyJdTh85eGwcW2dBAKR5mfIqWJfGsx6y4CEkx2yz67k9iNifCItqLe0VHlvrJILjEw36YRI-RNNKyqYi7CGX21HhuLhbAhICy6erJjFU2ic0B9ePKzluJCZ-9nK5GSiJ0QhW0HExZMRE1nOj3Jbr9wxFThMoWtD1LFLkDcz4yIhSwUujyJHkWngbSPIVbsmTWI-XxRmcaDBT9bJ9E6PdjVSfEp9Hk_3aofmasrdLZ2yfCEZn4K9sKHLegqLhyQqpOqB-c7TgNPHKToI4ZO_m96hJU76nE9sF5_OP7pdmWfu7_k1_rqKoxm7-4IF-iE96ApFKV5oCHQhsEp6leYOf6S7EUcx_c4A0pITZPfOB_3QPXJuhcaG_ueXaYkhdV4TLzolpggLS0aBZqKnUl2b4J-0rowgpdkg6AwfY-InW9eyZsaCR8MXDzS4sWHW5qehU7yNc2OS_r4lAiIwB8V3rcqkdJvzIs1GtxurKz4rloolpu7BOPD5E07qok2JijEoJS9szY4QjyXl2bKeqNg6IFq6qnRT4tlHBXMhV6bqVYyhretd-fZ6hO4ItDHa0aLyuElZ1WP3UaLauZchYuru6Pf_58y9hSw2iE5oRgX1ZfeY9ZmeEgRW3PZ28rpEQ
# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Clientimport sysimport osimport loggingimport jsonlogging.basicConfig(level=logging.INFO, stream=sys.stdout)secret_id = "AKID3eUqV0RTdHaRQ6PeyFzouVVSsd1c5oU4dgxxMSdepyySy-3TzBV2As5bsmVZe6LW"secret_key = "6ijalekmP0w5b4iiatUZVriHtd3iDTp98sbow/EhGGE="token = "8RWwthXC3rhLqqs60VtkfdrK2QVtRlua1eac99e9bd0f081699323aa8e9fbfa06DyYA0if2Ipe8Tyn6qk6rYuwGDJuyJdTh85eGwcW2dBAKR5mfIqWJfGsx6y4CEkx2yz67k9iNifCItqLe0VHlvrJILjEw36YRI-RNNKyqYi7CGX21HhuLhbAhICy6erJjFU2ic0B9ePKzluJCZ-9nK5GSiJ0QhW0HExZMRE1nOj3Jbr9wxFThMoWtD1LFLkDcz4yIhSwUujyJHkWngbSPIVbsmTWI-XxRmcaDBT9bJ9E6PdjVSfEp9Hk_3aofmasrdLZ2yfCEZn4K9sKHLegqLhyQqpOqB-c7TgNPHKToI4ZO_m96hJU76nE9sF5_OP7pdmWfu7_k1_rqKoxm7-4IF-iE96ApFKV5oCHQhsEp6leYOf6S7EUcx_c4A0pITZPfOB_3QPXJuhcaG_ueXaYkhdV4TLzolpggLS0aBZqKnUl2b4J-0rowgpdkg6AwfY-InW9eyZsaCR8MXDzS4sWHW5qehU7yNc2OS_r4lAiIwB8V3rcqkdJvzIs1GtxurKz4rloolpu7BOPD5E07qok2JijEoJS9szY4QjyXl2bKeqNg6IFq6qnRT4tlHBXMhV6bqVYyhretd-fZ6hO4ItDHa0aLyuElZ1WP3UaLauZchYuru6Pf_58y9hSw2iE5oRgX1ZfeY9ZmeEgRW3PZ28rpEQ"region = "ap-guangzhou"scheme = 'https'config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)client = CosS3Client(config)response = client.get_bucket_policy( Bucket='uwe2s90ktj9h-1313380398',)print(response)
python GetBucketPolicy.pyINFO:
qcloud_cos.cos_client:
generate built-in connection pool success. maxsize=10,10INFO:
qcloud_cos.cos_client:
bound built-in connection pool when new client. maxsize=10,10INFO:
qcloud_cos.cos_client:
get bucket policy, url=:
https://uwe2s90ktj9h-1313380398.cos.ap-guangzhou.myqcloud.com/ ,headers=:{}{'Policy': '{"Statement": [{"Action": ["name/cos:
PutBucketACL"], "Condition": {"ip_not_equal": {"qcs:ip": ["106.53.243.200", "172.16.0.129"]}}, "Effect": "Deny", "Principal": {"qcs": ["qcs::
cam::
uin/100026992078:
uin/100043488407"]}, "Resource": ["qcs::
cos:ap-guangzhou:
uid/1313380398:
uwe2s90ktj9h-1313380398/*"], "Sid": "costs-1757666257000000846088-172014-19"}], "version": "2.0"}'}
"Action": ["name/cos:
PutBucketACL"]"Condition": {"ip_not_equal": {"qcs:ip": ["106.53.243.200","172.16.0.129"]}}
# -*- coding: utf-8 -*-import osimport jsonfrom tencentcloud.common.common_client import CommonClientfrom tencentcloud.common import credentialfrom tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKExceptionfrom tencentcloud.common.profile.client_profile import ClientProfilefrom tencentcloud.common.profile.http_profile import HttpProfile
try: cred = credential.Credential("AKIDzW8kWxxxxazBCFZun0u_uooqap", "CzClytxxxxx=", "cIVuxxxxxxxxxxxxxEt7a52ESm8Rwgs3mHoHbJuuCH7DcBReqEEU_JgVHDUlLj1T68t_WRN20xcWb37sl7iRAFUgAseZ0HuRezPk2QNIq1F1mHh-xqh94NTWr15QF-L4HPu-h_GJGGexQGED7hvnQ59np2jiCsgMv5-_QAwJgMgrXQ44ztP2ZgUOqYYgao4eo5ABTKFMjdGXHK7mzHEfv5hqVnV5BNcR3aayAHqFgFW8pTNC71EVUx_cdukepaH0x_xNEb4XkvHKteVjWVXCI8BE8Jl5Qyr1HNO9x5vZx50yYXO0ZlxRXCPnPdtL9mvwK_hj2iU4TE_X4nwsQsdPdU_t-XdarmveUY77RPjrBD9giapUaXYuMrsjf1oILTM2MraAOmm6xk6PKumEUMiFcYpML0buizj6i-7LeyO5e5FgGuvygTDBcFS95jEyXdpfT2LS1I1CO0uvVm8I4ZG-ce3rzFY1oL6x11UO4vxBRTeDPl-KatdARcLK65SPLdr_4hmiULHDl4rMjrGv35TRdBJ0NvqamVwXo4GhHdl2yC7nP-dFfrQabusakzROhXpFNZMAAEeMOpw96gRDk8mXPqhhW_sYQAdcVqA") httpProfile = HttpProfile() httpProfile.endpoint = "cvm.tencentcloudapi.com" clientProfile = ClientProfile() clientProfile.httpProfile = httpProfile params = "{"InstanceIds":["ins-8xxxxx"],"Password":"Aa112211.","UserName":"root","ForceStop":
true}" common_client = CommonClient("cvm", "2017-03-12", cred, "ap-guangzhou", profile=clientProfile) print(common_client.call_json("ResetInstancesPassword", json.loads(params)))
except TencentCloudSDKException as err: print(err)
apt update && apt install python3-pip -y因为环境是debian的，我们直接pip install会报错，所以我们使用如下命令安装一下sdkpython3 -m pip install -U cos-python-sdk-v5 --break-system-packages
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156957-wxsync-2025-09-c1791da0e1cf4ba822cbb9abb096f2ce.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156959-wxsync-2025-09-2f51c95e7f9c72a1aa448b3e956af10b.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156960-wxsync-2025-09-8573085e48ee47724bab986cb7d48ead.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156962-wxsync-2025-09-0ac2b408b690667bc78c84079cb12464.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156964-wxsync-2025-09-12225eae5fa5d8c9654dadcf280631e5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156966-wxsync-2025-09-5eb6b34b1c854f0bae97a3b1f9442900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156967-wxsync-2025-09-e2925510e4bc59f1082cbe9e74f111cb.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156968-wxsync-2025-09-b58b5f9f18608fa4879b8a3925d7bb27.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156970-wxsync-2025-09-bd5a2ddfc9320a732c90be5514224354.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1758156971-wxsync-2025-09-9fce68c7f0f16b57275d59075945bb1c.png)