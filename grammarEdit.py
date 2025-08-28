# grammarEdit.py to remove left recursion and factoring

def read_grammar(filename="grammar.txt"):
    grammar = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            lhs, rhs = line.split("=>")
            lhs = lhs.strip()
            prods = [r.strip() for r in rhs.split("|")]
            grammar[lhs] = prods
    return grammar

def remove_left_recursion(grammar):
    """
    حذف بازگشت چپ مستقیم (نسخه ساده)
    A -> Aα | β  ===>  
    A -> βA'
    A'-> αA' | ε
    """
    new_grammar = {}
    for A, prods in grammar.items():
        alpha = []  # تولیدهای بازگشتی چپ (Aα)
        beta = []   # تولیدهای دیگر
        for p in prods:
            if p.startswith(A):   # اگر شروع تولید با خودش باشه
                alpha.append(p[len(A):])  # بخش بعد از A
            else:
                beta.append(p)
        if alpha:  # یعنی بازگشت چپ داشتیم
            A_dash = A + "'"
            new_beta = [b + A_dash for b in beta]
            new_alpha = [a + A_dash for a in alpha] + ["ε"]
            new_grammar[A] = new_beta
            new_grammar[A_dash] = new_alpha
        else:
            new_grammar[A] = prods
    return new_grammar

def left_factoring(grammar):
    """
    الگوریتم ساده left factoring:
    اگر چند تولید با پیشوند مشترک باشند،
    آن‌ها را فاکتورگیری می‌کنیم.
    """
    import os
    changed = True
    while changed:
        changed = False
        new_grammar = {}
        for A, prods in grammar.items():
            prefix_map = {}
            for p in prods:
                prefix = p[0] if p != "ε" else "ε"
                prefix_map.setdefault(prefix, []).append(p)
            # اگر پیشوند مشترک داشتیم
            if any(len(v) > 1 for v in prefix_map.values() if v[0] != "ε"):
                changed = True
                # ساده‌ترین حالت: فقط اولین کاراکتر مشترک رو می‌گیریم
                for prefix, group in prefix_map.items():
                    if len(group) > 1 and prefix != "ε":
                        A_dash = A + "'"
                        # تولید A -> prefix A'
                        new_grammar.setdefault(A, []).append(prefix + A_dash)
                        # تولید A' -> بقیه suffix ها
                        suffixes = [g[1:] if len(g) > 1 else "ε" for g in group]
                        new_grammar[A_dash] = suffixes
                    else:
                        new_grammar.setdefault(A, []).extend(group)
            else:
                new_grammar[A] = prods
        grammar = new_grammar
    return grammar

def save_grammar(grammar, filename="grammar_edited.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for lhs, prods in grammar.items():
            f.write(f"{lhs} => {' | '.join(prods)}\n")

if __name__ == "__main__":
    g = read_grammar("grammar.txt")
    print("Grammar read from file:")
    print(g)

    g = remove_left_recursion(g)
    g = left_factoring(g)

    print("\nEdited grammar (after removing left recursion and factoring):")
    print(g)

    save_grammar(g, "grammar_edited.txt")
    print("\nEdited grammar saved to grammar_edited.txt")
