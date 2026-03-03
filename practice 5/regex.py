#1
import re

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)
#2
import re

txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)
#3
import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)
#4
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())
#5
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())