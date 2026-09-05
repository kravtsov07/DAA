def tsp_dp(n, graph):
    memo = [[-1] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    memo_counter = 0
    
    def get_dist(u, v):
        d = graph[u][v]
        return d if d > 0 or u == v else float('inf')

    def dp(mask, u, depth=0):
        nonlocal memo_counter
        indent = "    " * depth
        bin_mask = bin(mask)[2:]
        formatted_mask = '0' * (n - len(bin_mask)) + bin_mask
        
        print(f"\n{indent}DP(mask={formatted_mask}, city={u}):")

        if mask == (1 << n) - 1:
            dist_to_0 = get_dist(u, 0)
            print(f"{indent}Все города посещены -> возврат в 0 за {dist_to_0}")
            return dist_to_0

        if memo[mask][u] != -1:
            memo_counter += 1
            print(f"{indent}Взято из memo[{formatted_mask}][{u}]: {memo[mask][u]}")
            return memo[mask][u]

        res = float('inf')

        for v in range(n):
            if not (mask & (1 << v)):
                d_uv = get_dist(u, v)
                
                if d_uv != float('inf'):
                    next_mask = mask | (1 << v)
                    next_mask_bin = bin(next_mask)[2:]
                    next_mask_bin = '0' * (n - len(next_mask_bin)) + next_mask_bin
                    
                    print(f"{indent}  Переход {u} -> {v} (стоимость: {d_uv}). Шаг в DP(mask={next_mask_bin}, city={v})")
                    
                    new_dist = d_uv + dp(next_mask, v, depth + 1)

                    print(f"{indent}Возврат в DP(mask={formatted_mask}, city={u}) из ветки {v}. Итог ветки: {new_dist}")

                    if new_dist < res:
                        res = new_dist
                        parent[mask][u] = v
                        print(f"{indent}  Новый минимум для {u}: лучший шаг -> {v}, стоимость = {res}")
                else:
                    print(f"{indent}  Переход {u} -> {v} невозможен (нет пути)")

        memo[mask][u] = res
        print(f"{indent}  Сохранено: memo[{formatted_mask}][{u}] = {res}")
        
        return res

    min_cost = dp(1, 0)

    if min_cost == float('inf'):
        return "no path", None

    print("\nВосстановление пути:")

    path = []

    curr_mask = 1
    curr_city = 0

    while curr_city != -1:
        path.append(curr_city)

        print(f"  Город {curr_city}")

        next_city = parent[curr_mask][curr_city]

        if next_city == -1:
            break

        curr_mask |= (1 << next_city)
        curr_city = next_city

    path.append(0)

    print(f"memo использовано {memo_counter} раз")
    return min_cost, path

graph = []

with open("matrix.txt", "r") as f:
    n = int(f.readline().strip())
    for _ in range(n):
        graph.append(list(map(int, f.readline().split())))

cost, path = tsp_dp(n, graph)

if cost == "no path":
    print("no path")
else:
    print(cost)
    print(*(path))
