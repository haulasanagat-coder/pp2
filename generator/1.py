def square_generator(N):
    for i in range(1,N+1):
        yield i*i
gen = square_generator(5)
for num in gen:
    print(num)
