# ll1Com.py
# Build LL(1) parsing table

EPSILON = "ε"

def build_ll1_table(grammar, first_sets, follow_sets):
    """
    Build LL(1) table:
    table[A][a] = production string chosen for (A, a)
    Returns: (table, is_ll1)
    """
    table = {nt: {} for nt in grammar.keys()}
    is_ll1 = True

    for A, productions in grammar.items():
        for prod in productions:
            # FIRST(prod)
            first_prod = set()
            i = 0
            epsilon_in_all = True
            while i < len(prod):
                symbol = prod[i]
                if symbol.isupper():
                    first_prod |= (first_sets[symbol] - {EPSILON})
                    if EPSILON in first_sets[symbol]:
                        i += 1
                        if i == len(prod):
                            first_prod.add(EPSILON)
                        continue
                    else:
                        epsilon_in_all = False
                        break
                else:
                    first_prod.add(symbol)
                    epsilon_in_all = False
                    break

            # برای هر a در FIRST(prod) بدون ε جدول را پر کن
            for terminal in first_prod - {EPSILON}:
                if terminal in table[A]:
                    # conflict!
                    is_ll1 = False
                table[A][terminal] = prod

            # اگر ε در FIRST(prod)، برای هر b در FOLLOW(A) جدول را پر کن
            if EPSILON in first_prod or (epsilon_in_all and prod == EPSILON):
                for terminal in follow_sets[A]:
                    if terminal in table[A]:
                        # conflict!
                        is_ll1 = False
                    table[A][terminal] = EPSILON

    return table, is_ll1


if __name__ == "__main__":
    # quick test
    test_grammar = {
        "E": ["TA"],
        "A": ["+TA", "ε"],
        "T": ["FB"],
        "B": ["*FB", "ε"],
        "F": ["(E)", "id"]
    }
    test_first = {
        "E": {"(", "id"},
        "A": {"+", "ε"},
        "T": {"(", "id"},
        "B": {"*", "ε"},
        "F": {"(", "id"}
    }
    test_follow = {
        "E": {")", "$"},
        "A": {")", "$"},
        "T": {"+", ")", "$"},
        "B": {"+", ")", "$"},
        "F": {"*", "+", ")", "$"}
    }
    table, ok = build_ll1_table(test_grammar, test_first, test_follow)
    print("--- LL(1) table ---")
    for nt, row in table.items():
        print(nt, ":", row)
    print("Is LL(1)?", ok)
