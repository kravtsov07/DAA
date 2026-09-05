def calc_L(n, graph, visited, path):

    start = path[0]
    end = path[-1]

    min_in = float('inf')
    min_out = float('inf')

    for v in range(n):
        if not visited[v]:
            if graph[v][start] > 0:
                min_in = min(min_in, graph[v][start])
            if graph[end][v] > 0:
                min_out = min(min_out, graph[end][v])

    if min_in == float('inf'):
        min_in = 0

    if min_out == float('inf'):
        min_out = 0

    return (min_in + min_out) / 2

def alsh_1(n, graph):
    visited = [False] * n
    path = [0]
    visited[0] = True
    total_cost = 0
    curr = 0

    for i in range(n - 1):
        next_city = -1
        best_f, best_s, best_L = float('inf'), 0, 0

        print(f"Шаг {i + 1}")
        print(f"Текущий город: {curr}")

        for v in range(n):

            if not visited[v] and graph[curr][v] > 0:
                s = graph[curr][v]

                visited[v] = True
                L = calc_L(n, graph, visited, path)
                f = s + L

                print(f"  Проверка {curr} -> {v}")
                print(f"    s + L = {s} + {L} = {f}")

                visited[v] = False

                if f < best_f:
                    best_f, best_s, best_L = f, s, L
                    next_city = v

        print(f"\n  Выбран город: {next_city}")
        print(f"  Лучшее значение: s + L = {best_s} + {best_L} = {best_f}") 

        if next_city == -1:
            return "no path", None

        path.append(next_city)
        visited[next_city] = True
        total_cost += graph[curr][next_city]
        
        print(f"  Стоимость = {total_cost}")

        curr = next_city

    if graph[curr][0] > 0:

        total_cost += graph[curr][0]

        path.append(0)

        print(f"\nВозврат в 0 за {graph[curr][0]}")

        return total_cost, path

    return "no path", None

graph = []

with open("matrix.txt", "r") as f:
    n = int(f.readline().strip())
    for _ in range(n):
        graph.append(list(map(int, f.readline().split())))

cost, path = alsh_1(n, graph)

if cost == "no path":
    print("no path")
else:
    print(cost)
    print(*(path))
