# main.py to control everything

import grammarEdit
import first_follow
import ll1Com

def main():
    # مرحله 1: اصلاح گرامر
    grammar = grammarEdit.edit_grammar("grammar.txt")
    print("\n--- Edited Grammar ---")
    for nt, rules in grammar.items():
        print(f"{nt} => {' | '.join(rules)}")

    # مرحله 2: محاسبه First و Follow
    first_sets, follow_sets = first_follow.compute_first_follow(grammar)
    print("\n--- FIRST sets ---")
    for nt, s in first_sets.items():
        print(f"First({nt}) = {s}")
    print("\n--- FOLLOW sets ---")
    for nt, s in follow_sets.items():
        print(f"Follow({nt}) = {s}")

    # مرحله 3: ساخت جدول LL(1)
    table, is_ll1 = ll1Com.build_ll1_table(grammar, first_sets, follow_sets)
    print("\n--- LL(1) Parsing Table ---")
    if is_ll1:
        for nt, row in table.items():
            print(nt, ":", row)
    else:
        print("Grammar is not LL(1)")

if __name__ == "__main__":
    main()
