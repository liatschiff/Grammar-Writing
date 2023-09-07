from collections import defaultdict
import random
import argparse

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._tree = False

    def set_tree(self, b):
        self._tree = b

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol): return symbol
        else:
            expansion = self.random_expansion(symbol)
            output = " ".join(self.gen(s) for s in expansion)
            if self._tree:
                return "(" + symbol + " " + output + ")"
            return output

    def random_sent(self):
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


if __name__ == '__main__':

    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("grammar")
    parser.add_argument('-n', type=int, default=1, help='number of sentences to parse')
    parser.add_argument('-t', action='store_true', help='print tree')
    args = parser.parse_args()

    pcfg = PCFG.from_file(sys.argv[1])
    if args.t:
        pcfg.set_tree(True)
    for i in range(args.n):
        print(pcfg.random_sent())
