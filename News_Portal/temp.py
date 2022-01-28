import re, random

pattern=r"\bсук[аи]+\w*\b|\bбляд\w*\b|\b\w*ху[ий]\w*\b|\b\w*[её]ба[тнл]\w*\b|\b\w*пизд\w*\b"

p=re.compile(pattern,re.IGNORECASE)
s1 = p.sub('***', "сука похуй блядь ебанная")

print(s1)
