list1 = {'M':'ACEG','R':'ADEG','K':'BCEG','S':'BDEG','A':'ACEH','B':'ADEH','L':'BCEH','U':'BDEH','D':'ACEI','C':'ADEI','N':'BCEI','V':'BDEI','H':'ACFG','F':'ADFG','O':'BCFG','W':'BDFG','T':'ACFH','G':'ADFH','P':'BCFH','X':'BDFH','E':'ACFI','I':'ADFI','Q':'BCFI','Y':'BDFI'}
list2 = original_list = ['M','R','K','S','A','B','L','U','D','C','N','V','H','F','O','W','T','G','P','X','E','I','Q','Y']
list2_re =list2[::-1]

ori_str = 'BCEHACEIBDEIBDEHBDEHADEIACEGACFIBDFHACEGBCEHBCFIBDEGBDEGADFGBDEHBDEGBDFHBCEGACFIBCFGADEIADEIADFH'

flag_1 = ''
for i in range(0,len(ori_str),4):
    _val = ori_str[i:i+4]
    for key, val in list1.items():
        if val == _val:
            flag_1 += key
print(flag_1)
flag = ''
for i in flag_1:
    for j,k in enumerate(list2):
        if i == k:
            flag += list2_re[j]
print(flag)