def my_coord_low(coef, pow, x0):
    # считаем производные
    deriv_coefs = []
    deriv_pows = []
    for y in range(0, 2):
        # решаем по x1 потом по x2
        deriv_coefs_tmp = []
        # перекидываю данные из переменной, чтобы с ними работать
        for x in range(0, len(coef)):
            deriv_coefs_tmp.append(coef[x])
        deriv_pows_tmp = []
        # аналогично
        for x in range(0, len(pow)):
            pows_tmp = []
            for z in range(0, len(pow[x])):
                pows_tmp.append(pow[x][z])
            deriv_pows_tmp.append(pows_tmp)
        # умножаем коэффициент на степень
        for x in range(0, len(coef)):
            deriv_coefs_tmp[x] *= deriv_pows_tmp[y][x]
        # пересчитываем степени
        for x in range(0, len(coef)):
            if deriv_pows_tmp[y][x] > 0:
                for z in range(0, 2):
                    if z == y:
                        deriv_pows_tmp[z][x] -= 1
            else:
                for z in range(0, 2):
                    deriv_pows_tmp[z][x] = 0
        # добавляем результат для соответствующей переменной
        deriv_coefs.append(deriv_coefs_tmp)
        deriv_pows.append(deriv_pows_tmp)
    # начинаем работу посредственного алгоритма
    success = False
    while not success:
        # считаем значения производной от x0
        x1 = []
        for x in range(0, len(deriv_coefs)):
            # x - номер уравнения
            # y - номер коэфициента
            # z - номер переменной
            # выбираем уравнение, потом берём коэфициент и умножаем его на значения переменных
            x1_tmp = 0
            for y in range(0, len(deriv_coefs[x])):
                x1_mul_tmp = deriv_coefs[x][y]
                for z in range(0, len(x0)):
                    x1_mul_tmp *= x0[z] ** deriv_pows[x][z][y]
                x1_tmp += x1_mul_tmp
            x1.append(x1_tmp)
        # если значения функции нулевые, то закрываем алгоритм
        success = True
        for x in range(0, len(x1)):
            success = x1[x] == 0 and success
        if not success:
            # иначе продолжаем
            # покоординатный метод
            index = 0
            max = 0
            # ищем максимальный по модулю из x1
            for x in range(0, len(x1)):
                if (abs(x1[x]) > max):
                    index = x
                    max = abs(x1[x])
            s = []
            # если он положительный, умножаем вектор на -1 (или меняем нужное значение на -1)
            for x in range(0, len(x1)):
                s.append(0)
            s[index] = 1
            if x1[index] > 0:
                s[index] = -1
            t_coef = []
            t_pow = []
            s_pow = []
            # ищем вектор y, на который будем заменять значения x в функции
            for x in range(0, len(s)):
                s_pow.append(abs(s[x]))
            # s_pow определяет, в каком из значений вектора y будет стоять t
            # t_pow и t_coef определяют вектор y
            for x in range(0, len(x0)):
                t_coef_tmp = []
                t_pow_tmp = []
                # зависимости от значения вектора добавляем значения в вектор y
                if s_pow[x] != 0:
                    t_coef_tmp.append(x0[x])
                    t_pow_tmp.append(0)
                    t_coef_tmp.append(s[x])
                    t_pow_tmp.append(s_pow[x])
                else:
                    t_coef_tmp.append(s[x] + x0[x])
                    t_pow_tmp.append(0)
                t_pow.append(t_pow_tmp)
                t_coef.append(t_coef_tmp)
            t_func_coef = []
            t_func_pow = []
            # определяем функцию f(y)
            for x in range(0, len(coef)):
                # сначала берём степени переменных
                pows_tmp = []
                for y in range(0, len(pow)):
                    pows_tmp.append(pow[y][x])
                difficulty = 0
                # далее смотрим, как преобразовывать функцию в зависимости от степеней
                # difficulty = 0 -> [0,0]
                # difficulty = 1 -> [1,0] или [0,1]
                # difficulty = 2 -> [1,1]
                # difficulty = 3 -> [2,0] или [0,2]
                if pows_tmp[0] == 0:
                    if pows_tmp[1] == 0:
                        difficulty = 0
                    elif pows_tmp[1] == 1:
                        difficulty = 1
                    elif pows_tmp[1] == 2:
                        difficulty = 3
                elif pows_tmp[0] == 1:
                    if pows_tmp[1] == 0:
                        difficulty = 1
                    elif pows_tmp[1] == 1:
                        difficulty = 2
                    elif pows_tmp[1] == 2:
                        difficulty = -1
                elif pows_tmp[0] == 2:
                    if pows_tmp[1] == 0:
                        difficulty = 3
                    elif pows_tmp[1] == 1:
                        difficulty = -1
                    elif pows_tmp[1] == 2:
                        difficulty = -1
                # [2,0] [1,0] [0,1] [0,2] [0,0] [1,1]
                # действуем в зависимости от степеней
                if difficulty != 0:
                    if difficulty == 1:
                        # тут легко, умножаем одно из значений вектора на коэффициент
                        # в случае выражения, добавляется по два значения
                        for i in range(0, len(pows_tmp)):
                            if pows_tmp[i] != 0:
                                for j in range(0, len(t_coef[i])):
                                    t_func_coef.append(t_coef[i][j] * coef[x])
                                    t_func_pow.append(t_pow[i][j] * pows_tmp[i])
                    elif difficulty == 2:
                        # всегда в векторе y будет присутствувать значение без выражения
                        # находим это значение и умножаем на выражение
                        # действия аналогичны 1
                        for i in range(0, len(t_pow)):
                            found = False
                            j = 0
                            while (not found) and j < len(t_pow[i]):
                                found = t_pow[i][j] > 0 or found
                                j += 1
                            if not found:
                                index = i
                        multiplier = coef[x] * t_coef[index][0]
                        index = 1 - index
                        for j in range(0, len(t_coef[index])):
                            t_func_coef.append(t_coef[index][j] * multiplier)
                            t_func_pow.append(t_pow[index][j] * pows_tmp[index])
                    elif difficulty == 3:
                        # узнаём, стоит ли у нас выражение под степенью 2
                        # если да, то раскрываем его как квадрат суммы
                        # иначе, просто добавляем квадрат значения вектора y
                        formulaIndex = 0
                        squareIndex = 0
                        for i in range(0, len(pows_tmp)):
                            isFormula = False
                            j = 0
                            for j in range(0, len(t_pow[i])):
                                isFormula = t_pow[i][j] > 0 or isFormula
                            if isFormula:
                                formulaIndex = i
                        for i in range(0, len(pows_tmp)):
                            if pows_tmp[i] == 2:
                                squareIndex = i
                        if formulaIndex != squareIndex:
                            t_func_coef.append(coef[x] * t_coef[squareIndex][0] ** 2)
                            t_func_pow.append(0)
                        else:
                            t_index = 0
                            sv_index = 0
                            for i in range(0, len(t_pow[formulaIndex])):
                                if t_pow[formulaIndex][i] > 0:
                                    t_index = i
                                    sv_index = 1 - t_index
                            t_func_coef.append(coef[x] * t_coef[squareIndex][t_index]
                                               * t_coef[squareIndex][sv_index] * 2)
                            t_func_pow.append(1)
                            t_func_coef.append(coef[x] * (t_coef[squareIndex][t_index] ** 2))
                            t_func_pow.append(2)
                            t_func_coef.append(coef[x] * (t_coef[squareIndex][sv_index] ** 2))
                            t_func_pow.append(0)
                elif difficulty == 0:
                    # в случае свободного члена он остаётся неизменным
                    t_func_coef.append(coef[x])
                    t_func_pow.append(0)
            t_func_deriv_pow = []
            t_func_deriv_coef = []
            # далее ищем производную от этой функции
            # умножаем коэфициенты на степени
            # уменьшаем степени на 1
            for x in range(0, len(t_func_pow)):
                t_func_deriv_pow.append(t_func_pow[x])
            for x in range(0, len(t_func_coef)):
                t_func_deriv_coef.append((t_func_coef[x]))
            for x in range(0, len(t_func_deriv_coef)):
                t_func_deriv_coef[x] *= t_func_deriv_pow[x]
                if t_func_deriv_pow[x] > 0:
                    t_func_deriv_pow[x] -= 1
            num = 0
            divider = 0
            # далее ищем значение t
            # прибавляем все значения коэф. свободных членов и все значения коэф. переменных
            # отдельно друг от друга
            for x in range(0, len(t_func_deriv_coef)):
                if t_func_deriv_pow[x] > 0:
                    divider += t_func_deriv_coef[x]
                else:
                    num += t_func_deriv_coef[x]
            t = -num / divider
            # найдя это значение, считаем сумму вектора s, умноженного на t и x0
            ts = []
            for x in range(0, len(t_pow)):
                func = 0
                num = 0
                for y in range(0, len(t_pow[x])):
                    if t_pow[x][y] > 0:
                        func += t_coef[x][y]
                    else:
                        num += t_pow[x][y]
                ts.append(func + num)
            x0ts = []
            # далее считаем сумму векторов x0 и предыдущего, это значения вектора y
            for x in range(0, len(ts)):
                x0ts.append(t * ts[x] + x0[x])
            fs = []
            # считаем значение производной от этого вектора
            for x in range(0, len(deriv_coefs)):
                f_tmp = 0
                for y in range(0, len(deriv_coefs[x])):
                    f_mul_tmp = deriv_coefs[x][y]
                    for z in range(0, len(x0ts)):
                        f_mul_tmp *= x0ts[z] ** deriv_pows[x][z][y]
                    f_tmp += f_mul_tmp
                fs.append(f_tmp)
        else:
            x0ts = x0
            fs = x1
        success = True
        # если все производной от вектора 0, завершаем алгоримт
        # вектор y - точка локального минимума
        for x in range(0, len(fs)):
            success = (fs[x] == 0) and success
        if not success:
            x0 = x0ts
        f = 0
        # подсчёт функции
        for x in range(0, len(coef)):
            f += coef[x] * (x0ts[0] ** pow[0][x]) * (x0ts[1] ** pow[1][x])
        # вывод значений на экран
        print('Значение функции: ' + str(f))
        print(x0ts)
