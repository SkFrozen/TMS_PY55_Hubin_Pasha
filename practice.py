from time import time

"""Algorithms"""

N = int(input("Enter a end of sequence: "))


def eratosthenes_sieve(N) -> list:
    """Searches simple numbers and return them"""
    A = [True] * N
    A[0] = A[1] = False
    S = []
    for k in range(2, N):
        if A[k]:
            for m in range(k * 2, N, k):
                A[m] = False
            S.append(k)
    return S


print(eratosthenes_sieve())


def bubble_sort(A):
    """Bubble sorting list A"""
    N = len(A)
    for bypass in range(1, N):
        for k in range(0, N - bypass):
            print(f"iteration: {k} list: {A}")
            if A[k] > A[k + 1]:
                A[k], A[k + 1] = A[k + 1], A[k]
    return A


print(bubble_sort([5, 3, 4, 6, 1, 2]))


def choise_sort(A):
    """Choise sorting list A"""
    N = len(A)
    for pos in range(0, N - 1):
        for k in range(pos + 1, N):
            if A[pos] > A[k]:
                A[pos], A[k] = A[k], A[pos]
    return A


print(choise_sort([5, 3, 4, 6, 1, 2]))


def insert_sort(A):
    """Insert sorting list A"""
    N = len(A)
    for top in range(1, N):
        k = top
        while k > 0 and A[k - 1] > A[k]:
            A[k], A[k - 1] = A[k - 1], A[k]
            k -= 1
    return A


print(insert_sort([5, 3, 4, 6, 1, 2]))


def nod(a, b):
    return a if b == 0 else nod(b, a % b)


print(nod(24, 30))


def nod_2(a, b):
    while b != 0:
        a, b = b, a % b
    return a


print(nod_2(24, 30))


def index_mass_body(h: int, m: int) -> str:
    imb = m / (h * 0.01) ** 2
    if imb < 18.5:
        return f"{imb} Недостаточная масса тела"
    elif 18.5 < imb < 25:
        return f"{imb} Норма"
    else:
        return f"{imb} Избыточная масса тела"


try:
    high = int(input("Enter yours high: "))
    mass = int(input("Enter yours mass: "))
    print(index_mass_body(high, mass))
except ValueError as e:
    print("Not valid data: ", e)
except ZeroDivisionError as e:
    print("Height cannot be zero: ", e)


def shift(A: list, step: int) -> list:
    if step < 0:
        for i in range(abs(step)):
            A.append(A.pop(0))
    else:
        for i in range(step):
            A.insert(0, A.pop())
    return A


print(shift([1, 2, 3, 4, 5], -2))


def prime_number(number: int):
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True


def high_prime_number_division(given_number: int):
    list_num = []
    for element in range(2, int(given_number**0.5) + 1):
        if given_number % element == 0:
            if prime_number(element):
                list_num.append(element)
    return list_num[-1]


print(high_prime_number_division(600851475143))


def issimple(a):
    r = int(a**0.5) + 1
    lst = []
    for i in range(3, r):
        if a % i == 0:
            if issimple(i) == []:
                lst.append(i)
    return lst


print(max(issimple(13195)))
"""Turtle"""
from math import pi, sin
import turtle as tt

angle = float(input("Enter a angle: "))
r = float(input("Enter a radius: "))
A = r * angle / (2 * pi)
forward = A * angle
for i in range(0, 180 * 3):
    tt.left(A)
    tt.forward(forward)
    forward += (A / (2 * pi)) * angle / 50

for i in range(0, 180):
    tt.forward(forward)
    tt.left(90)
    forward += (A / (2 * pi)) * angle


def many_anles(n, m):
    q = 360 / n
    for i in range(n):
        tt.left(q)
        tt.forward(m)


def turn_angle(k):
    n = 3
    r = 20
    for i in range(k):
        m = 2 * r * sin(pi / n)
        x = (180 - 360 / n) / 2
        tt.left(x)
        many_anles(n, m)
        tt.right(x)
        tt.penup()
        tt.forward(15)
        tt.pendown()
        n += 1
        r += 15
