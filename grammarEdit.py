# grammarEdit.py
# Remove direct left recursion and do simple left factoring


from collections import defaultdict
import itertools

EPSILON = "ε"

def read_grammar(filename="grammar.txt"):
    """
    Reads a grammar from a text file with lines like:
      E => E+T | T
    Returns: dict[str, list[str]]
    """
    grammar = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=>" not in line:
                raise ValueError(f"Invalid grammar line (no '=>'): {line}")
            lhs, rhs = line.split("=>", 1)
            lhs = lhs.strip()
            prods = [r.strip() for r in rhs.split("|")]
            grammar[lhs] = prods
    return grammar

def _fresh_name(base, existing):
    """
    Produce a fresh nonterminal name like A', A'' ... not clashing with existing.
    """
    candidate = base + "'"
    while candidate in existing:
        candidate += "'"
    return candidate

def remove_left_recursion(grammar):
    """
    Removes DIRECT left recursion:
      A -> Aα | β   ===>
      A -> β A'
      A'-> α A' | ε
    NOTE: This is per-nonterminal, direct only. (Indirect LR not handled here.)
    """
    new_grammar = {}
    for A, prods in grammar.items():
        alphas = []  # parts after the leading A in Aα
        betas  = []  # β (those not starting with A)
        for p in prods:
            if p.startswith(A):  # direct LR candidate
                alpha = p[len(A):]
                if alpha == "":   # avoid empty tail like A -> A
                    alpha = EPSILON
                alphas.append(alpha)
            else:
                betas.append(p)

        if alphas:  # has direct LR
            A_dash = _fresh_name(A, set(grammar.keys()) | set(new_grammar.keys()))
            # A -> β A'
            new_A_prods = []
            if betas:
                for b in betas:
                    if b == EPSILON:
                        # ε A' == A'  (but we keep explicit form to stay string-based)
                        new_A_prods.append(A_dash)
                    else:
                        new_A_prods.append(b + A_dash)
            else:
                # No β terms: standard fallback is A -> A' (to keep language with ε via A')
                new_A_prods.append(A_dash)

            # A' -> α A' | ε
            new_Adash_prods = []
            for a in alphas:
                if a == EPSILON:
                    new_Adash_prods.append(A_dash)  # ε A' == A' (kept as string concat)
                else:
                    new_Adash_prods.append(a + A_dash)
            new_Adash_prods.append(EPSILON)

            new_grammar[A] = new_A_prods
            new_grammar[A_dash] = new_Adash_prods
        else:
            new_grammar[A] = prods[:]
    return new_grammar

def _longest_common_prefix(strings):
    """
    Longest common prefix for a list of strings (empty if none).
    """
    if not strings:
        return ""
    s1 = min(strings)
    s2 = max(strings)
    i = 0
    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i += 1
    return s1[:i]

def left_factoring(grammar):
    """
    Very simple left factoring on STRING prefix basis.
    Groups productions with a common (>=1 char) prefix and factors them:
      A -> αβ1 | αβ2  ===>
      A -> α A'
      A'-> β1 | β2
    Repeats until no change.
    """
    changed = True
    while changed:
        changed = False
        result = {}
        for A, prods in grammar.items():
            # group by first character to keep this lightweight
            by_first = defaultdict(list)
            for p in prods:
                key = p[0] if p and p != EPSILON else p
                by_first[key].append(p)

            factored_here = False
            temp_acc = []
            new_symbols = {}

            for _, group in by_first.items():
                if len(group) < 2 or group[0] == EPSILON:
                    temp_acc.extend(group)
                    continue

                lcp = _longest_common_prefix(group)
                if not lcp:
                    temp_acc.extend(group)
                    continue

                # We will factor this group
                factored_here = True
                changed = True
                A_dash = new_symbols.get(lcp)
                if not A_dash:
                    A_dash = _fresh_name(A, set(grammar.keys()) | set(result.keys()))
                    new_symbols[lcp] = A_dash
                    # A -> α A'
                    temp_acc.append(lcp + A_dash)

                # A' -> suffixes (ε if suffix empty)
                suffixes = []
                for g in group:
                    suf = g[len(lcp):]
                    suffixes.append(suf if suf else EPSILON)
                result[A_dash] = suffixes

            if factored_here:
                # temp_acc may include duplicates; keep order stable-ish, remove dups
                seen = set()
                filtered = []
                for x in temp_acc:
                    if x not in seen:
                        filtered.append(x)
                        seen.add(x)
                result[A] = filtered
            else:
                result[A] = prods[:]

        grammar = result
    return grammar

def save_grammar(grammar, filename="grammar_edited.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for lhs, prods in grammar.items():
            f.write(f"{lhs} => {' | '.join(prods)}\n")

def edit_grammar(filename="grammar.txt", save_to_file=False, out_file="grammar_edited.txt"):
    """
    High-level API for main.py:
      - read the raw grammar
      - remove direct left recursion
      - left factoring
      - return the edited grammar AS A DICTIONARY
      - optionally also save to a file
    """
    g = read_grammar(filename)
    g = remove_left_recursion(g)
    g = left_factoring(g)
    if save_to_file:
        save_grammar(g, out_file)
    return g

if __name__ == "__main__":
    # quick manual test
    g = edit_grammar("grammar.txt", save_to_file=False)
    print("Edited grammar:")
    for k, v in g.items():
        print(f"{k} => {' | '.join(v)}")
