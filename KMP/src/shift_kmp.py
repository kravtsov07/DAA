def shift_kmp(a, b):
    n = len(a)
    m = len(b)

    if n != m:
        print("-1")
        return
    if n == 0:
        print("0")
        return

    print(f"\nВычисляем префикс-функцию для шаблона '{b}'")
    pi = [0] * m
    j = 0
    #aabaaab
    for i in range(1, m):
        print(f"Шаг префикс-функции {i}: Сравниваем p[{i}]='{b[i]}' и p[{j}]='{b[j]}'")
        while j > 0 and b[i] != b[j]:
            print(f"   Несовпадение, откат: j был {j}, стал pi[{j}-1] = {pi[j-1]}")
            j = pi[j-1]
            print(f"   Теперь сравниваем p[{i}]='{b[i]}' и p[{j}]='{b[j]}'")
        if b[i] == b[j]:
            j += 1
            print(f"   Символы совпали, увеличиваем j до {j}")
        else:
            print(f"   Символы не совпали, j остается {j}")
        pi[i] = j
        print(f"   Итог шага: pi[{i}] = {j}")
    
    print(f"pi-массив = {pi}")
   
    q = 0
    for i in range(2 * n):
        print(f"Шаг {i}: Символ текста A[{i % n}] = '{a[i % n]}', сопоставляем с B[{q}] = '{b[q]}'")
        
        while q > 0 and a[i % n] != b[q]:
            q = pi[q-1]
            print(f"   Символы не совпали, откат по префикс функции: q = {q}")
        
        if a[i % n] == b[q]:
            q += 1
            print(f"   Символы совпали идем вперед по префикс-функции: q = {q}")
            
        if q == m:
            print(f"   Найдено вхождение, Индекс начала: {i - m + 1}")
            print(i - m + 1)
            return

    print("-1")

shift_kmp(input(), input())