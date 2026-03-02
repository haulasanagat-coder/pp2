#1
import re

pattern = r'ab*'

text = input("Enter a string: ")

if re.fullmatch(pattern, text):
    print("Match found!")
else:
    print("No match.")


#2
import re

pattern = r'ab{2,3}'
text = input()

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")


#3
import re

pattern = r'^[a-z]+(_[a-z]+)+$'
text = input()

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")


#4
import re

pattern = r'^[A-Z][a-z]+$'
text = input()

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")


#5
import re

pattern = r'^a.*b$'
text = input()

if re.fullmatch(pattern, text):
    print("Match found")
else:
    print("No match")