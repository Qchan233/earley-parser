from utils import terminal
from collections import defaultdict

grammar = [
    ('A', ),
    ('A', 'B'),
    ('B', 'A')
]

def nullable(grammar):
    terminals = set()
    nonterminals = set()
    
    lhs_table = {}
    rhs_table = {}

    empty_rules = set()


    rhs_dict = defaultdict(list)
    nullable = set()
    for rule in grammar:
        lhs, rhs = rule[0], rule[1:]
        for sym in rhs:
            if not terminal(sym):
                rhs_dict[sym].append((lhs, rhs))
        if not rhs:
            nullable.add(lhs)

    workset = nullable.copy()
    while workset:
        work_sym = workset.pop()
        for rule in rhs_dict[work_sym]:
            lhs, rhs = rule
            if lhs in nullable:
                continue

            for sym in rhs:
                if sym not in nullable:
                    break
            else:
                nullable.add(lhs)
                workset.add(lhs)
    
    return nullable

if __name__ == "__main__":
    print(nullable(grammar))
            