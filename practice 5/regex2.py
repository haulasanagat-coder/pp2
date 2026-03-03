#1
import re

pattern = r"^ab*$"

test_strings = ["a", "ab", "abb", "ac", "b"]

for s in test_strings:
    if re.match(pattern, s):
        print("Match")
    else:
        print("No match")
#2
pattern = r"^ab{2,3}$"
string="abbb"
if re.search(pattern,string):
    print("Yes")
else:
    print("No")

#3
text = "hello_world my_Name test_case example_test_string"
pattern = r"\b[a-z]+_[a-z]+\b"

matches = re.findall(pattern, text)
print(matches)

#4
text = "Hello world Test Python ABC"
pattern = r"\b[A-Z][a-z]+\b"

matches = re.findall(pattern, text)
print(matches)

#5
pattern = r"a.*b"
text = "a123b"

if re.search(pattern, text):
    print("Match found")
else:
    print("No match")

#6
text = "Hello, world. Python is good"

result = re.sub(r"[ ,\.]", ":", text)

print(result)

#7
text = "hello_world"

result = re.sub(r'_([a-z])', lambda x: x.group(1).upper(), text)

print(result)

#8
text = "HelloWorldPython"

result = re.split(r"(?=[A-Z])", text)

print(result)

#9
text = "HelloWorldPython"

result = re.sub(r"([A-Z])", r" \1", text)

print(result.strip())

#10
text = "helloWorldTest"

result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)