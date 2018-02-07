class BFError(Exception):
    pass


fucking = [
    "[]", "[-]", "[+]", "[>]", "[<]"
]


class Bytecode:
    def __init__(self, code: str):
        self.code = code
        if not self._check_brace():
            raise BFError("count(`[`) != count(`]`)")
        self.bytecode = self._to_bytecode(self.code)
        self._optimize()
        self.calc_brace()
        self._to_str()

    def _check_brace(self):
        if self.code.count("[") != self.code.count("]"):
            return False

        count = 0
        for ch in self.code:
            if ch == '[':
                count += 1
            elif ch == ']':
                count -= 1

            if count < 0:
                return False

        return count == 0

    @staticmethod
    def _to_bytecode(code: str):
        for ch in code:
            if ch in "+-><[]":
                yield (ch, 1)

    def _optimize(self):
        first = self._optimize_1(self.bytecode)
        second = self._optimize_2(first)
        self.bytecode = list(second)

    @staticmethod
    def _optimize_1(bc):
        """ Change `-` to `+` and  `<` to `>`"""
        for opcode in bc:
            if opcode[0] == '-':
                yield ('+', -1)
            elif opcode[0] == '<':
                yield ('>', -1)
            else:
                yield opcode

    @staticmethod
    def _optimize_2(bc):
        """ Change `----` to `('+', -4)`, etc. """
        cmd = 'S'
        count = 0

        for opcode in bc:
            if opcode[0] in "[]":
                yield (cmd, count)
                cmd, count = opcode
            elif opcode[0] == cmd:
                count += opcode[1]
            elif opcode[0] != cmd:
                yield (cmd, count)
                cmd, count = opcode

        yield (cmd, count)

    def calc_brace(self):
        bytecode = []
        poss = []
        CP = 0

        for opcode in self.bytecode:
            if '[' == opcode[0]:
                poss.append(CP)
                bytecode.append('[')
            elif ']' == opcode[0]:
                pos = poss.pop(-1)
                bytecode.append((']', pos))
                bytecode[pos] = (bytecode[pos], CP)
            else:
                bytecode.append(opcode)

            CP += 1

        self.bytecode = bytecode

    def _to_str(self):
        self.code = ""
        for opcode in self.bytecode:
            if opcode[0] in "+-":
                ch = opcode[0]
                if opcode[1] < 0:
                    ch = '+' if ch == '-' else '-'
                self.code += ch * abs(opcode[1])
            elif opcode[0] in '<>':
                ch = opcode[0]
                if opcode[1] < 0:
                    ch = '<' if ch == '>' else '>'
                self.code += ch * abs(opcode[1])
            elif opcode[0] in "[]":
                self.code += opcode[0]

    def __str__(self):
        return self.code