def func(li):
    for i in li:
        yield(i*i)

sq_nums=func([1,2,3,4,5])
print(next(sq_nums))