# first_follow.py to compute first and follow 

# خواندن گرامر از فایل ادیت‌شده
with open("grammar_edited.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# تعریف کلاس NonTerminal
class NonTerminal:
    def __init__(self, symbol):
        self.symbol = symbol
        self.rules = []
        self.first = []
        self.firstdepen = []
        self.followdepen = []
        self.follow = []

# تعریف کلاس Rule
class Rule:
    def __init__(self, s: str, nont: NonTerminal):
        self.s = s
        self.nont = nont
        self.nont.rules.append(self)

# ساخت NonTerminal و Rule ها
nonterminals = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    symbol, rule = line.split(" => ")
    nonterminal = NonTerminal(symbol)
    nonterminals.append(nonterminal)
    rules = rule.split(" | ")
    for r in rules:
        Rule(r, nonterminal)

# افزودن $ به Follow اولین NonTerminal (شروع گرامر)
nonterminals[0].follow.append("$")

# تابع محاسبه First
def first(nt):
    for rule in nt.rules:
        if rule.s[0].islower() or rule.s[0] in "()$+-*/id":  # اگر ترمینال باشد
            nt.first.append(rule.s[0])
        elif rule.s[0].isupper():  # اگر نان‌ترمینال باشد
            for c in rule.s:
                if c.isupper():
                    nt2 = next((n for n in nonterminals if n.symbol == c), None)
                    if nt2 not in nt.firstdepen:
                        nt.firstdepen.append(nt2)
                        nt.firstdepen.extend(nt2.firstdepen)
                        d = first(nt2)
                        nt.first.extend([x for x in d if x != "ε"])
                        if "ε" in d:
                            if c == rule.s[-1]:
                                nt.first.append("ε")
                            continue
                        else:
                            break
                    else:
                        if "ε" in nt2.first:
                            continue
                        else:
                            break
                else:
                    nt.first.append(c)
                    break
        else:  # اگر ε باشد
            nt.first.append("ε")
    nt.first = list(set(nt.first))
    return nt.first

# محاسبه First برای همه نان‌ترمینال‌ها
for nt in nonterminals:
    if len(nt.first) == 0:
        first(nt)

# چاپ First ها
for nt in nonterminals:
    print(f"First({nt.symbol}): ", "{", end="")
    for i in range(len(nt.first)):
        print(f" {nt.first[i]}", end="")
        if i != len(nt.first) - 1:
            print(",", end="")
        else:
            print(" }")

# تابع محاسبه Follow
def follow():
    for nt in nonterminals:
        for rule in nt.rules:
            for j in range(len(rule.s)):
                if rule.s[j].isupper():
                    nt2 = next(n for n in nonterminals if n.symbol == rule.s[j])
                    if j == len(rule.s) - 1:
                        nt2.followdepen.append(nt)
                        continue
                    else:
                        for c in range(j + 1, len(rule.s)):
                            if rule.s[c].isupper():
                                nt3 = next(n for n in nonterminals if n.symbol == rule.s[c])
                                nt2.follow.extend([b for b in nt3.first if b != "ε"])
                                if "ε" in nt3.first:
                                    continue
                                else:
                                    break
                            else:
                                nt2.follow.append(rule.s[c])
                                break

    for nt in nonterminals:
        nt.follow = list(set(nt.follow))
        if nt.symbol in nt.follow:
            nt.follow.remove(nt.symbol)

# آپدیت Follow با توجه به وابستگی‌ها
def upd_follow(nt: NonTerminal):
    for depen in nt.followdepen:
        nt.follow.extend(depen.follow)
    revdep = [n for n in nonterminals if nt in n.followdepen]
    for dep in revdep:
        dep.follow.extend(nt.follow)
        dep.follow = list(set(dep.follow))
    nt.follow = list(set(nt.follow))

# محاسبه Follow
follow()
for nt in nonterminals:
    upd_follow(nt)

# چاپ Follow ها
for nt in nonterminals:
    print(f"Follow({nt.symbol}): ", "{", end="")
    for i in range(len(nt.follow)):
        print(f" {nt.follow[i]}", end="")
        if i != len(nt.follow) - 1:
            print(",", end="")
        else:
            print(" }")
