def encode(line, key, key2):
    return ''.join(chr(x ^ ord(line[x]) ^ ord(key[::-1][x]) ^ ord(key2[x])) for x in range(len(line)))


# t = '-M7\x10wG06a\x04*c|\x0eFYn\x03(DK\x12\x0f\x17!=\x062\x02YB\\!Q.{\x13jGZ\x1cG'
t = '-M7\x10wI`7k\x07!5r\x0eF\x0enS(D\x10\x1d\x0c\x17x?\x01c\x02\\@\x0cqW"{A<@\x0f\x19G'

print(encode(t, 'GQIS5EmzfZA1Ci8NslaoMxPXqrvFB7hYOkbg9y20W3',
      'xwdFqMck1vA0pl7B8WO3DrGLma4sZ2Y6ouCPEHSQVT'))
