class Node:
    _node_id_counter = 0

    def __init__(self, parent=None, char_to_parent=None):
        self.id = Node._node_id_counter
        Node._node_id_counter += 1
        self.son: dict[str, 'Node'] = {}
        self.go: dict[str, 'Node'] = {}
        self.parent: 'Node' = parent
        self.char_to_parent: str = char_to_parent
        self.suff_link: 'Node' = None
        self.up: 'Node' = None
        self.is_leaf: bool = False
        self.leaf_pattern_numbers: list[int] = []

class AhoCorasick:
    def __init__(self):
        Node._node_id_counter = 0
        self.root = Node()
        self.pattern_lengths = {}

    def add_string(self, s, pattern_number):
        cur = self.root
        for char in s:
            if char not in cur.son:
                new_node = Node(parent=cur, char_to_parent=char)
                cur.son[char] = new_node
                print(f"[Бор] Добавлен узел {new_node.id} из {cur.id} по символу '{char}'")
            else:
                print(f"[Бор] Уже существовал узел {cur.son[char].id} из {cur.id} по символу '{char}'")
            cur = cur.son[char]
        cur.is_leaf = True
        cur.leaf_pattern_numbers.append(pattern_number)
        self.pattern_lengths[pattern_number] = len(s)
        print(f"[Бор] Узел {cur.id} помечен как конец строки №{pattern_number}")

    def get_suff_link(self, v: Node):
        if v.suff_link is None:
            if v == self.root or v.parent == self.root:
                v.suff_link = self.root
            else:
                v.suff_link = self.get_link(self.get_suff_link(v.parent), v.char_to_parent)
            if v != self.root:
                print(f"  [Автомат] Ссылка π: {v.id} -> {v.suff_link.id}")
        return v.suff_link

    def get_link(self, v: Node, c: str):
        if c not in v.go:
            if c in v.son:
                v.go[c] = v.son[c]
            elif v == self.root:
                v.go[c] = self.root
            else:
                v.go[c] = self.get_link(self.get_suff_link(v), c)
        return v.go[c]

    def get_up(self, v: Node):
        if v.up is None:
            sl = self.get_suff_link(v)
            if sl.is_leaf:
                v.up = sl
            elif sl == self.root:
                v.up = self.root
            else:
                v.up = self.get_up(sl)
            if v != self.root:
                print(f"  [Автомат] Ссылка up: {v.id} -> {v.up.id}")
        return v.up

    def process_text(self, text: str):
        print(f"{f'\nПОИСК В ТЕКСТЕ {text}':^40}")
        results = []
        cur = self.root
        for i in range(len(text)):
            char = text[i]
            next_node = self.get_link(cur, char)
            print(f"Позиция {i}: '{char}' | Переход {cur.id} -> {next_node.id}")
            cur = next_node
            
            temp = cur
            while temp != self.root:
                if temp.is_leaf:
                    for p_idx in temp.leaf_pattern_numbers:
                        start_pos = i - self.pattern_lengths[p_idx] + 2
                        print(f"      Совпадение: Паттерн №{p_idx} в позиции {start_pos}")
                        results.append((start_pos, p_idx))
                temp = self.get_up(temp)
        return results
    
    def get_max_chains_from_root(self):
        stats = {"max_suff": 0, "max_up": 0}

        def dfs(v: Node):
            if v != self.root:
                curr_suff_len = 0
                temp = v
                while temp != self.root:
                    temp = self.get_suff_link(temp)
                    curr_suff_len += 1
                stats["max_suff"] = max(stats["max_suff"], curr_suff_len)

                curr_up_len = 0
                temp = v
                while temp != self.root:
                    temp = self.get_up(temp)
                    if temp != self.root:
                        curr_up_len += 1
                stats["max_up"] = max(stats["max_up"], curr_up_len)

            for char in sorted(v.son.keys()):
                dfs(v.son[char])

        dfs(self.root)
        return stats["max_suff"], stats["max_up"]
    
    def print_automaton(self):
        print(f"{'\nИТОГОВАЯ СТРУКТУРА АВТОМАТА':^60}")

        def show(v: Node, char="ROOT", prefix="", is_last=True):
            sl = self.get_suff_link(v)
            up = self.get_up(v)
            
            leaf_info = f" (TERM: {v.leaf_pattern_numbers})" if v.is_leaf else ""
            links = f" | π:{sl.id} up:{up.id}" if v != self.root else ""
            
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}'{char}' [ID:{v.id}]{leaf_info}{links}")

            new_prefix = prefix + ("    " if is_last else "│   ")
            child_chars = sorted(v.son.keys())
            for i, c in enumerate(child_chars):
                show(v.son[c], c, new_prefix, i == len(child_chars) - 1)

        show(self.root)
        
if __name__ == "__main__":
    
    text = input()
    n = int(input())
    patterns = []
    for _ in range(n):
        patterns.append(input())

    ac = AhoCorasick()
    print(f"{'ПОСТРОЕНИЕ БОРА':^40}")
    for i in range(n):
        print(f"Строка '{patterns[i]}'")
        ac.add_string(patterns[i], i+1)

    matches = ac.process_text(text)

    matches.sort()

    for pos, p_idx in matches:
        print(f"{pos} {p_idx}")
    
    suff_max, up_max = ac.get_max_chains_from_root()
    print("Максимальная цепочка суффиксных ссылок " + str(suff_max))
    print("Максимальная цепочка конечных ссылок " + str(up_max))
        
    ac.print_automaton()
    
""" 
abababac
4
babac
abac
bac
ac
"""