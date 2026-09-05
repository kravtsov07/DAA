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

class AhoCorasickWildCard:
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
                print(f"  [Автомат] Ссылка: {v.id} -> {v.up.id}")
        return v.up

    def process_text_with_wildcards(self, text, parts, full_pattern_len):
        print(f"{f'\nПОИСК В ТЕКСТЕ {text}':^40}")
        counts = [0] * len(text)
        cur = self.root

        for i in range(len(text)):
            char = text[i]
            next_node = self.get_link(cur, char)
            print(f"Позиция {i}: '{char}' | {cur.id} -> {next_node.id}")
            cur = next_node

            temp = cur
            while temp != self.root:
                if temp.is_leaf:
                    for p_idx in temp.leaf_pattern_numbers:
                        offset = parts[p_idx][1]
                        start_pos = i - self.pattern_lengths[p_idx] - offset + 1
                        
                        print(f"    Совпадение: часть №{p_idx}, возможный старт = {start_pos}")
                        if 0 <= start_pos <= len(text) - full_pattern_len:
                            counts[start_pos] += 1
                            print(f"        Засчитано в counts[{start_pos}] = {counts[start_pos]}")

                temp = self.get_up(temp)
        
        return counts
    
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
    pattern = input()
    wildcard = input()

    parts = []
    start = -1

    print(f"{'\nРАЗБИЕНИЕ ШАБЛОНА':^40}")
    for i in range(len(pattern)):
        if pattern[i] != wildcard:
            if start == -1:
                start = i
        else:
            if start != -1:
                parts.append((pattern[start:i], start))
                print(f"Часть: '{pattern[start:i]}' с offset {start}")
                start = -1

    if start != -1:
        parts.append((pattern[start:], start))
        print(f"Часть: '{pattern[start:]}' с offset {start}")

    ac = AhoCorasickWildCard()

    print(f"{'\nПОСТРОЕНИЕ БОРА':^40}")
    for i in range(len(parts)):
        print(f"Строка '{parts[i][0]}'")
        ac.add_string(parts[i][0], i)

    counts = ac.process_text_with_wildcards(text, parts, len(pattern))
    
    print(f"{'\nПРОВЕРКА СОВПАДЕНИЙ':^40}")
    num_parts = len(parts)
    for i in range(len(counts)):
        if counts[i] == num_parts:
            print(f"Совпадение полного шаблона с позиции {i + 1}")
            
    ac.print_automaton()
    

""" 
abacabadaba
a$a
$
"""