from .utils import source_execute

"""
one operand
two operand
inplace
loop
"""


def test_one_operand():
    source = """
a = 1
b = + a
c = - a

d = True
e = not d
f = ~ d

g = [1,2,3,4]

h = 0
for i in g:
    h += i
"""
    source_execute(source)


def test_two_operand():
    source = """
a = 375
b = 2

c = a ** b
d = a * b
# not implemented
# e = a @ b
f = a // b
g = a / b
h = a % b
i = a + b
j = a - b

k = [1,2,3,4]
l = k[2]
n = a << b
m = a >> b
o = a & b
p = a ^ b
q = a | b
"""
    source_execute(source)


def test_inplace():
    source = """
a = 532
a **= 2
a *= 3
# not implemented
# a @= 4
a //= 5
a /= 6
a %= 7
a += 8
a -= 9

b = [1,2,3,4]
b[2] = 3
del b[1]

c = 432523
c <<= 2
c >>= 3
c &= 2421
c ^= 3124
c |= 3322
"""
    source_execute(source)


def test_loop():
    source = """
a = 0
for i in range(10):
    a += i

b = 0
for i in range(100):
    if i == 95:
        break
    elif i % 2 == 0:
        b += 1

c = []
d = [1,9,3,1,7,0]
for e in reversed(d):
    c.append(e)
"""
    source_execute(source, {'reversed': reversed})
