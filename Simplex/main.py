from ast import literal_eval
import Simplex as smp

# открываем файл с данными и считываем его
with open('data.csv') as numbers:
    data = numbers.read().splitlines()
c = list(literal_eval(data[0]))
b = list(literal_eval(data[1]))
a = []
for x in range(2, len(data)):
    a.append(list(literal_eval(data[x])))
print('СИМПЛЕКС-МЕТОД')
print('Исходные данные:')
print('Таблица коэффицентов и знаков:')
for x in range(0, len(a)):
    print(a[x])
print('Коэфиценты целевой функции:')
print(c)
print('Ограничения:')
print(b)
# используем алгоритм симплекс-метода
# алгоритм максимизации, поэтому flio = True
# количество доп. переменных 0
result = smp.my_simplex(a, b, c, flip=True, saveslack=True, counter=0)
a_new = result[0]
print('Результат работы симлпекс-метода:')
print('Таблица коэффицентов:')
for x in range(0, len(a_new)):
    print(a_new[x])
f = result[4]
print('Значение целевой функции:')
print(f)
print('Значения переменных целевой функции:')
print(result[5])
# вытаскиваем преобразованную симплекс-таблицу
# вытаскиваем номера базисных столбцов
bases_prime = result[2]
# пусть увеличим все ограничения в два раза
print('АНАЛИЗ НА ЧУВСТВИТЕЛЬНОСТЬ')
print('Увеличим ограничения в два раза:')
b_new = list(literal_eval(data[1]))
for x in range(0, len(b_new)):
    b_new[x] *= 2
print(b_new)
# вытаскиваем преобразованные в процессе работы симплекс метода базисны столбцы
bases_current = []
for x in range(0, len(bases_prime)):
    column = []
    for y in range(0, len(a)):
        column.append(a[y][bases_prime[x]])
    bases_current.append(column)
print('Пересчитанные в процессе работы симплекс метода базисные столбцы (столбцы записаны в строку):')
for x in range(0, len(bases_current)):
    print(bases_current[x])
# перемножение столбцов базиса на вектор b_new, получим новый вектор ограничений при полном пересчёте
# далее находим значение целевой функции при новом векторе
f_new = 0
print('Перемножим матрицу на вектор:')
bases = result[3]
new_vector = []
for y in range(0, len(bases_current[0])):
    value = 0
    for x in range(0, len(bases_current)):
        value += bases_current[x][y] * b_new[x]
    new_vector.append(value)
print(new_vector)
print('Все значения остались положительными.')
print('Решение осталось оптимальным. Тогда пересчитаем значение целевой функции, пересчитав только последний шаг:')
c = list(literal_eval(data[0]))
for x in range(0, len(bases)):
    if bases[x] > -1:
        f_new += new_vector[bases[x]] * c[x]
print(f_new)
if f_new > f:
    str1 = "увеличилось"
    diff = f_new/f
else:
    str1 = "уменьшилось"
    diff = f/f_new
print('Значение целевой функции ' + str1 + ' в ' + str(diff) + ' раз(а), что требовалось ожидать.')
# теперь изменим значения b_new так, чтобы пропорции значений изменились
# сделаем так, чтобы в новом векторе ограничений появилось отрицательное значение
# для этого попробуем постепенно увеличивать на 1 значения вектора ограничений
b_new = list(literal_eval(data[1]))
print('Теперь непропорционально изменим значения ограничений, чтобы сделать одно из значений вектора значений')
print('переменных целевой функции отрицательным:')
positive = True
while positive:
    b_new[0] += 1
    new_vector = []
    for y in range(0, len(bases_current[0])):
        value = 0
        for x in range(0, len(bases_current)):
            value += bases_current[x][y] * b_new[x]
        new_vector.append(value)
    success = True
    for x in range(0, len(new_vector)):
        positive = positive and new_vector[x] >= 0
print(b_new)
print('Значения вектора:')
print(new_vector)
print('Решение больше не является оптимальным.')
print('Теперь нужно пересчитать симплекс-таблицу, используя двойственный симплекс-метод:')
print('Таблица коэффицентов:')
for x in range(0, len(a_new)):
    print(a_new[x])
print('Коэфиценты целевой функции:')
c_new = result[6]
for x in range(0, len(c_new)):
    c_new[x] = -c_new[x]
print(c_new)
print('Значения ограничений:')
print(new_vector)
# если получится, тогда пересчитаем симплекс-таблицу, используя двойственный симплекс-метод
result_new = smp.my_simplex_double(a_new, new_vector, c_new, flip=True, saveslack=True, counter=result[7])
print('Результат работы двойственного симлпекс-метода:')
a_new = result_new[0]
print('Таблица коэффициентов:')
for x in range(0, len(a_new)):
    print(a_new[x])
f_new = result_new[4]
print('Значение целевой функции:')
print(f_new)
print('Значения переменных целевой функции:')
print(result_new[5])
if f_new > f:
    str1 = "увеличилось"
    diff = f_new/f
    str2 = 'более'
else:
    str1 = "уменьшилось"
    diff = f/f_new
    str2 = 'менее'
print('Значение целевой функции ' + str1 + ' в ' + str(diff) + ' раз(а). Отсюда эта ситуация нам ' + str2 + ' выгодная.')