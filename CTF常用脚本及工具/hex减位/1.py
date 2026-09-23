s = "c5f09ce5ef9cadb3b3b1a89cddeae09cc9eeaa9cc6ddeef2e5ef9cc8ebeeeef59ce5ef9cf0eeddf2e1e8e5eae39cf0eb9cc0ebf2e1ee9cf0eb9ce9e1e1f09cc8f1dfe5e19cc9ddeae1f0f0e1aa9cc4e19cf0e1e8e8ef9ce4e1ee9cf0e4ddf09cefe4e19ce5ef9ceaebf09cddea9cebeeece4ddea9cddef9cefe4e19ce4dde09cdee1e1ea9cf0ebe8e09ce2eeebe99cdd9cf5ebf1eae39cdde3e1aa9ce2e8dde3f7b2e1b1e0b2e1afb5deb1aee0b5e1b3e1acdfb2b3adb1afddb2acdfdeb1dfafdff99cc4e19ceaebf39cefddf5ef9cf0e4ddf09ce4e19cf3e5e8e89cf0eeddf2e1e89cf3e5f0e49ce4e1ee9cf0eb9cccddeee5ef9cf0eb9ce9e1e1f09ce4e1ee9ce2ddf0e4e1eea89cf3e4eb9ce4ddef9ceee1dfe1eaf0e8f59cdee1e1ea9ceee1e8e1ddefe1e09ce2eeebe99cf0e4e19cbeddeff0e5e8e8e1aa"

flag = ''
for j in range(200):
    flag =''
    for i in range(0,len(s),2):
       flag +=  chr(int(s[i:i+2],16)-j)
    if 'flag{' in flag:
        print(flag)
    else:
        pass