def square(a,b):
    for i in range(a,b+1):
        yield i*i
a = int(input())
b = int(input())
for v in square(a,b):
    print(v)