s = "1234567890abcdef1234567890abcdef"
start = "4"
end = "e"
print(s.find(start))
print(s[s.find(start)])
aa = s[s.find(start):s.find(end)]
print(aa)
