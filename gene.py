import random

import math

import sys

from emulator import Bytecode, BFError, cyt_run


class Gene:
    _genes = "+-<>[]"

    def __init__(self, code: str):
        self._code = code
        self.bytecode = Bytecode(self._code)
        self.values = None
        self.error = None

    def __add__(self, other: "Gene"):
        while True:
            try:
                _code = ""
                for choises in zip(self._code, other._code):
                    _code += random.choice(choises)
                return Gene(_code)
            except BFError:
                pass

    def _try_mutate(self, p: float):
        """
        :param p: Вероятность мутации
        :return:
        """
        v = max(0, int(5 / p - 6))
        _code = ""
        for ch in self._code:
            _code += random.choice(self._genes + ch * v)

        if self._code != _code:
            self.bytecode = Bytecode(self._code)
            self.values = None
            self.error = None

    def mutate(self, p=0.1):
        while True:
            try:
                self._try_mutate(p)
                return True
            except BFError:
                pass

    def __str__(self):
        return f"{self.bytecode}\t\t{self.error}"


class World:
    def __init__(self,
                 creatures: int = 36,
                 count_genes: int = 10,
                 max_mem_size: int = 10
                 ):
        self.creatures_count = creatures
        self.genes_count = count_genes
        self.mem_size = max_mem_size

        if self.creatures_count % 6:
            raise ValueError("creatures_count must be % 6")

        self.creatures = [self._new_gene() for _ in range(self.creatures_count)]
        self._precalc()

    def _new_gene(self):
        while True:
            code = " ".join(
                random.choices("+-><[]", [1, 1, 1, 1, 1, 1], k=self.genes_count)
            )
            if "[]" in str(code) or "[-]" in str(code) or "[+]" in str(code):
                return None

            try:
                return Gene(code)
            except BFError:
                pass

    @staticmethod
    def _search_func(a, b):
        return (a + b) % 256

    def _precalc(self):
        self.values = []
        for a in range(256):
            for b in range(256):
                self.values.append((a, b, self._search_func(a, b)))

    def _calc(self, creature: Gene):
        creature.values = []
        creature.error = 0
        bc = creature.bytecode
        if "[]" in str(bc) or "[-]" in str(bc) or "[+]" in str(bc):
            return False

        for x, y, res in self.values:
            mem = [0] * self.mem_size
            mem[0] = x
            mem[1] = y

            try:
                mem = cyt_run(
                    bc.bytecode,
                    mem_size=self.mem_size,
                    max_cycles=10000,
                    mem=mem
                )
            except BFError:
                creature.error = math.inf
                creature.values = None
                return False

            creature.values.append(mem[0])
            creature.error += (mem[1] - res) ** 2

        return True

    def step(self, need_print=True):
        # Check
        creatures = []

        for creature in self.creatures:
            if creature.error is None and creature.values is None:
                while not self._calc(creature):
                    creature = self._new_gene()
                    print(",", end="")

                print(".", end="")
                sys.stdout.flush()

            creatures.append(creature)

        self.creatures = creatures

        print()

        # CROSSING
        creatures = [(creature, creature.error) for creature in self.creatures]

        creatures.sort(key=lambda x: x[1])

        self.creatures = [creature[0] for creature in creatures]

        yield self.creatures[0], self.creatures[0].error

        if need_print:
            self.print()

        self.creatures = self.creatures[:self.creatures_count // 3 * 2]

        random.shuffle(self.creatures)

        for i in range(self.creatures_count // 3):
            self.creatures.append(
                self.creatures[2 * i] + self.creatures[2 * i + 1]
            )

        # MUTATE

        for creature in self.creatures:
            creature.mutate()

    def print(self, creatures=None):
        creatures = creatures or self.creatures

        creatures.sort(key=lambda x: x.error or math.inf)

        for creature in creatures:
            print(f"{creature}")





