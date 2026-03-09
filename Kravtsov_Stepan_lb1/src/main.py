import time 

N = int(input())
n = N
board = []

def place(r: int, c: int, w: int, mode: str =""):
    
    prefix = "Ставим" if mode == "add" else "Убираем"
    if mode: print(f"{prefix} квадрат {w} в ({r+1}, {c+1})")
    
    mask = ((1 << w) - 1) << c
    for i in range(r, r + w):
        board[i] ^= mask

def find_empty():
    full = (1 << n) - 1
    for r in range(n):
        if board[r] != full:
            row = board[r]
            c = 0
            while (row >> c) & 1:
                c += 1
            return r, c
    return -1, -1

def max_square_w(r: int, c: int):
    max_w = min(n - r, n - c)
    for w in range(1, max_w + 1):
        mask = ((1 << w) - 1) << c
        for i in range(r, r + w):
            if board[i] & mask:
                return w - 1
    return max_w if max_w < N else N - 1

start = time.time()
multiplier = 1
delimiter = 2

while delimiter * delimiter <= n:
    if n % delimiter == 0:
        multiplier = n // delimiter
        n = delimiter
        break
    delimiter += 1

if n % 2 == 0:
    half = N // 2
    print(f"Четный случай")
    print(f"Квадрат {N}x{N} делится на 4 квадрата со сторонами {half}")
    print(4)
    print(1, 1, half)
    print(1, half + 1, half)
    print(half + 1, 1, half)
    print(half + 1, half + 1, half)
    exit()

print(f"Начало поиска для N={n}, Масштаб x{multiplier}")

board = [0] * n

w1 = (n + 1) // 2
w2 = (n - 1) // 2

place(0, 0, w1)
place(0, w1, w2)
place(w1, 0, w2)

current_res = [(1, 1, w1), (1, w1 + 1, w2), (w1 + 1, 1, w2)]
stack = []
min_k = n * n
best_res = []

r, c = find_empty()
mw = max_square_w(r, c)
print(f"Первая пустая клетка найдена в ({r+1}, {c+1}). Макс. размер там: {mw}")
place(r, c, mw, mode="add")
stack.append([r, c, mw]) 
current_res.append((r + 1, c + 1, mw))

while stack:
    k = len(current_res)
    r_empty, c_empty = find_empty()

    if r_empty == -1 and c_empty == -1:
        print(f"Найдено решение: {k} квадратов")
        if k <= min_k:
            min_k = k
            best_res = list(current_res)
            print(f"Новое лучшее решение - {min_k}")
    
    if k >= min_k:
        while stack:
            print(f'Состояний стека - ', len(stack))
            prev_r, prev_c, curr_w = stack.pop()
            
            place(prev_r, prev_c, curr_w, mode="del")
            current_res.pop()
            
            if curr_w > 1:
                next_w = curr_w - 1
                print(f"Уменьшаем квадрат, теперь {next_w} в ({prev_r+1}, {prev_c+1})")
                place(prev_r, prev_c, next_w, mode="add")
                current_res.append((prev_r + 1, prev_c + 1, next_w))
                stack.append([prev_r, prev_c, next_w])
                break 
            else:
                print(f"Все варианты для ({prev_r+1}, {prev_c+1}) исчерпаны, идем выше по стеку")
        else:
            break 
    else:
        mw = max_square_w(r_empty, c_empty)
        place(r_empty, c_empty, mw, mode="add")
        current_res.append((r_empty + 1, c_empty + 1, mw))
        stack.append([r_empty, c_empty, mw])

print()
print(time.time() - start, "секунд")
print(min_k)
for r, c, w in best_res:
    print(f"({(r - 1) * multiplier + 1}, {(c - 1) * multiplier + 1}) {w * multiplier}")
