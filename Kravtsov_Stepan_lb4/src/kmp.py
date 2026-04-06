def kmp(p, t):
    m = len(p)
    n = len(t)

    if m == 0:
        return

    print(f"\nВычисляем префикс-функцию для шаблона '{p}'")
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and p[i] != p[j]:
            j = pi[j-1]
        if p[i] == p[j]:
            j += 1
        pi[i] = j

    print(f"pi-массив = {pi}")

    print(f"Начинаем поиск в тексте длиной {n} символов")
    res = []
    q = 0  
    for i in range(n):
        print(f"Шаг {i}: Текущий символ текста '{t[i]}', пытаемся сопоставить с '{p[q]}' (q={q})")
        while q > 0 and p[q] != t[i]:
            q = pi[q-1]
            print(f"   Символы не совпали, откат по префикс функции: q = {q}")
        
        if p[q] == t[i]:
            q += 1
            print(f"   Символы совпали идем вперед по префикс-функции: q = {q}")
        
        if q == m:
            start_index = i - m + 1
            print(f"   Найдено вхождение, индекс начала: {start_index}")
            res.append(str(start_index))
            q = pi[q-1]
            print(f"   Сдвигаемся для поиска перекрытий, новый q = {q}")
    
    return res

res = kmp(input(), input())

if not res:
    print("-1")
else:
    print("Индексы вхождений:", ",".join(res))