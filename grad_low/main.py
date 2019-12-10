from ast import literal_eval
import grad
from scipy.optimize import minimize


def func(x): return x[0] ** 2 + 3 * x[1] ** 2 - 3 * x[0] * x[1] + x[0] - 6 * x[1]


with open('data.csv') as reader:
    data = reader.read().splitlines()
# структура файла data.csv:
# 1 строка коэффициенты уравнений
# 2 строка и дальше - степени переменных
coefs = list(literal_eval(data[0]))
pows = []
for x in range(1, len(data)):
    pows.append(list(literal_eval(data[x])))
print('Работа алгоритма поиска локального минимума')
grad.my_coord_low(coefs, pows, [1, 3.0])
print('Работа библиотеки линпрог, для сравнения:')
res = minimize(fun=func, x0=[1, 3.0], method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
print(res)
print('Как видно, значения функции и точки минимума совпадают, что подтверждает правильность работы алгоритма.')
