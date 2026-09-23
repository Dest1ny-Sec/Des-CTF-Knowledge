from urllib.parse import unquote

with open('./data.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = unquote(line)
        line = line[line.find('))=')+3:line.find('--')]
        print(chr(int(line)),end="")
