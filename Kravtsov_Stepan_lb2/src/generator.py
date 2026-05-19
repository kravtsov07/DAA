import random

UPPER_LIMIT = 10
is_sym = False

n = int(input())

matrix = [[0] * n for _ in range(n)]

if is_sym:
    for i in range(n):
        for j in range(i + 1, n):
            w = random.randint(1, UPPER_LIMIT)

            matrix[i][j] = w
            matrix[j][i] = w
else:
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = random.randint(1, UPPER_LIMIT)
     
with open("matrix.txt", "w") as f:
    f.write(str(n))
    
    for row in matrix:
        f.write("\n" + " ".join(map(str, row)))
