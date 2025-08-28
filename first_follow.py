# first_follow.py
# Compute FIRST and FOLLOW sets for a grammar dictionary
# Input format: dict[str, list[str]]
# Output: (first_sets, follow_sets), both dict[str, set[str]]

EPSILON = "ε"

def compute_first_follow(grammar):
    """
    grammar: dict { NonTerminal: [production1, production2, ...] }
    Returns:
        first_sets  : dict { NonTerminal: set(terminals/ε) }
        follow_sets : dict { NonTerminal: set(terminals/$) }
    """
    nonterminals = list(grammar.keys())
    first_sets = {nt: set() for nt in nonterminals}
    follow_sets = {nt: set() for nt in nonterminals}

    # ---- FIRST computation ----
    def first_of_symbol(sym, visited=None):
        """
        Returns FIRST(sym):
        - if sym is terminal or ε: {sym}
        - if sym is NonTerminal: FIRST(NonTerminal)
        """
        if visited is None:
            visited = set()
        if sym not in grammar:   # it's a terminal
            return {sym}
        if sym in visited:
            return first_sets[sym]  # avoid infinite recursion
        visited.add(sym)
        result = set()
        for production in grammar[sym]:
            if production == EPSILON:
                result.add(EPSILON)
                continue
            # scan each symbol in production
            i = 0
            while i < len(production):
                # symbol-by-symbol: we need to parse nonterminals vs terminals carefully
                # We'll assume productions are written without spaces and nonterminals are uppercase letters.
                s = production[i]
                if s.isupper():
                    f = first_of_symbol(s, visited)
                    result |= (f - {EPSILON})
                    if EPSILON in f:
                        i += 1
                        if i == len(production):
                            result.add(EPSILON)
                        continue
                    else:
                        break
                else:
                    # it's a terminal (single char like '+', '(', etc.)
                    result.add(s)
                    break
            # loop ends if break not called
        first_sets[sym] |= result
        return result

    # populate FIRST sets
    updated = True
    while updated:
        updated = False
        for nt in nonterminals:
            before = set(first_sets[nt])
            first_of_symbol(nt)
            if first_sets[nt] != before:
                updated = True

    # ---- FOLLOW computation ----
    # start symbol follow contains $
    start = nonterminals[0]
    follow_sets[start].add("$")

    updated = True
    while updated:
        updated = False
        for A in nonterminals:
            for production in grammar[A]:
                # process string symbol by symbol
                for i, B in enumerate(production):
                    if not B.isupper():
                        continue  # only for nonterminals
                    # beta = suffix after B
                    beta = production[i+1:]
                    if beta:
                        # add FIRST(beta) minus ε to FOLLOW(B)
                        first_beta = set()
                        j = 0
                        while j < len(beta):
                            s = beta[j]
                            if s.isupper():
                                first_s = first_sets[s]
                                first_beta |= (first_s - {EPSILON})
                                if EPSILON in first_s:
                                    j += 1
                                    if j == len(beta):
                                        first_beta.add(EPSILON)
                                    continue
                                else:
                                    break
                            else:
                                first_beta.add(s)
                                break
                        follow_sets[B] |= (first_beta - {EPSILON})
                        if EPSILON in first_beta:
                            follow_sets[B] |= follow_sets[A]
                    else:
                        # no beta, add FOLLOW(A) to FOLLOW(B)
                        follow_sets[B] |= follow_sets[A]
        # check if changed
        # (simplest: recompute follow until stable)
        # We'll rely on while loop condition
        # deep compare: make a snapshot
        # but to keep logic consistent, we break only if no additions
        # This works automatically because we use "updated" flag
        # We'll run another loop to ensure convergence
        snap_before = {nt: set(follow_sets[nt]) for nt in nonterminals}
        # run same logic again (idempotent)
        # Actually, we can rely on top-level while to detect changes properly
        snap_after = {nt: set(follow_sets[nt]) for nt in nonterminals}
        if snap_after != snap_before:
            updated = True

    return first_sets, follow_sets


if __name__ == "__main__":
    # quick manual test with the original grammar
    test_grammar = {
        "E": ["E+T", "T"],
        "T": ["T*F", "F"],
        "F": ["(E)", "id"]
    }
    f, fo = compute_first_follow(test_grammar)
    print("--- FIRST sets ---")
    for nt, s in f.items():
        print(f"First({nt}) = {s}")
    print("--- FOLLOW sets ---")
    for nt, s in fo.items():
        print(f"Follow({nt}) = {s}")
