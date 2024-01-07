def count():
    list=[1,2,3,4,5,6,7,13,55,23,22]
    d = 0
    for i in list:
        if i % 2 == 0:
            d += 1
    print(d)
count()

def sum(nums):
    total = 1
    for i in nums:
        total *=i
    return(total)
print(sum((8,2,3,1,1,7)))


def hh():
    g = input('LLL:')
    if g < str(0):
        print('Число отрицательное')
    else:
        print('OK')
hh()


def square():
    list=[]
    for i in range(1,31):
        b = i ** 2
        list.append(b)
    print(list)
square()


