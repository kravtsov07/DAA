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
    for i in range(1, m):
        while j > 0 and b[i] != b[j]:
            j = pi[j-1]
        if b[i] == b[j]:
            j += 1
        pi[i] = j
    
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