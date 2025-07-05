from dataclasses import dataclass
from ordered_set import OrderedSet
from collections import defaultdict
from utils import terminal
from nullable import nullable

# grammar = [
#     ('S', 'S', '+', 'P'),
#     ('S', 'P'),
#     ('P', 'P', '*', 'F'),
#     ('P', 'F'),
#     ('F', '(', 'S', ')'),
#     ('F', 'n'),
# ]

grammar = [
    ('A', ),
    ('A', 'B'),
    ('B', 'A')
]

S = ()


@dataclass
class EarleyItem:
    rule: tuple
    dot: int
    start: int
    index: int

    def __repr__(self) -> str:
        return f"{self.rule[0]} -> {' '.join(self.rule[1: self.dot])} • {' '.join(self.rule[self.dot:])}\t({self.start})"

    def __hash__(self) -> int:
        return hash((self.index, self.dot))

    def completed(self):
        return self.dot == len(self.rule)

class EarleyRecognizer:
    def __init__(self, grammar):
        self.grammar = grammar
        self.start_symbol = grammar[0][0]
        self.build_grammar()
        self.nullable = nullable(grammar)

    def build_grammar(self):
        self.grammar_dict = defaultdict(list)
        self.grammar_to_index = {}
        for i, rule in enumerate(self.grammar):
            self.grammar_dict[rule[0]].append(rule)
            self.grammar_to_index[rule] = i

    def recognize(self, input_string):
        self.chart = [OrderedSet([]) for _ in range(len(input_string) + 1)]
        for rule in self.grammar_dict[self.start_symbol]:
            self.chart[0].add(EarleyItem(rule, 1, 0, self.grammar_to_index[rule]))
        
        N = len(input_string)
        for i in range(N + 1):
            j = 0
            items = self.chart[i]
            while j < len(self.chart[i]):
                item = items[j]
                j += 1
                if item.completed():
                    start_pos = item.start
                    for candidate in self.chart[start_pos]:
                        if candidate.completed():
                            continue
                        if candidate.rule[candidate.dot] == item.rule[0]:
                            print(f'complete {candidate}')
                            self.chart[i].add(EarleyItem(candidate.rule, candidate.dot + 1, candidate.start, candidate.index))
                    continue

                focus = item.rule[item.dot]
                if not terminal(focus):
                    # predict
                    rules = self.grammar_dict[focus]
                    if focus in self.nullable:
                        self.chart[i].add(EarleyItem(item.rule, item.dot + 1, item.start, item.index))
                    for rule in rules:
                        self.chart[i].add(EarleyItem(rule, 1, i, self.grammar_to_index[rule]))
                else:
                    # scan
                    if i < N:
                        ch = input_string[i]
                        if focus == ch:
                            self.chart[i + 1].add(EarleyItem(item.rule, item.dot + 1, item.start, item.index))

            print(f'==== {i} ====')
            for item in self.chart[i]:
                print(item)

        for item in self.chart[N]:
            if item.completed() and item.rule[0] == self.start_symbol:
                return True
        return False

if __name__ == "__main__":
    recognizer = EarleyRecognizer(grammar)
    recognizer.recognize(S)