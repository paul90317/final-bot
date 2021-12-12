import re
print(re.escape('https://www.%python.org'))
r=re.compile('https?:\/\/([a-zA-Z0-9]+\.)*[a-zA-Z0-9]+(\/\S*)?')
print(r.fullmatch('https://44//'))
print(r.fullmatch('http://skfjalsd;f/'))
