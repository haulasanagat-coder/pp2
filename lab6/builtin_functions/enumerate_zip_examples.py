#enumerate
fruits = ["apple", "banana", "orange"]

for i, v in enumerate(fruits):
    print(i, v)

#zip
names = ["A", "B", "C"]
scores = [90, 85, 100]

for n, s in zip(names, scores):
    print(n, s)