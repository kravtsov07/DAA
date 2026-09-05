a = input()
b = input()

if len(a) > len(b):
    a, b = b, a

n = len(a)
m = len(b)

prev_row = [i for i in range(n + 1)]
cur_row = [0] * (n + 1)

prev_sub = [0] * (n + 1)
cur_sub = [0] * (n + 1)

max_len = 0
end_pos = 0

for i in range(1, m + 1):
    cur_row[0] = i
    
    print(f"Шаг {i}: символ b: '{b[i-1]}':")
    #Последовательность преобразований над исходной строкой
    for j in range(1, n + 1):
        print(f"  Сравнение '{b[i-1]}' и '{a[j-1]}': ", end="")
        if a[j-1] == b[i-1]:
            cur_row[j] = prev_row[j-1]
            print(f"Совпадение cur_row[{j}] = prev_row[{j-1}] = {prev_row[j-1]}")
        else:
            cost = min(prev_row[j], prev_row[j-1], cur_row[j-1]) + 1
            cur_row[j] = cost
            print(f"Несовпадение cur_row[{j}] = {cost}")
        
        if a[j-1] == b[i-1]:
            cur_sub[j] = prev_sub[j-1] + 1
            
            if cur_sub[j] > max_len:
                max_len = cur_sub[j]
                end_pos = j
        else:
            cur_sub[j] = 0
    
    print(f"  prev_row - {prev_row}")
    print(f"  cur_row: {cur_row}")

    prev_row[:] = cur_row[:]
    prev_sub[:] = cur_sub[:]

print(prev_row[n])
print(a[end_pos - max_len:end_pos], max_len)