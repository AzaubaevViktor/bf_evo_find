from .bytecode import BFError


def run(bytecode,
        mem_size=10,
        max_cycles=30000,
        mem=None
        ):
    cycles_count = 0
    mem = mem or []
    mem = mem[:mem_size] + [0] * (mem_size - len(mem))
    MP = 0
    CP = 0

    while CP < len(bytecode):
        c, ptr = bytecode[CP]

        if '+' == c:
            mem[MP] += ptr
            mem[MP] %= 256
        elif '-' == c:
            mem[MP] -= ptr
            mem[MP] %= 256
        elif '<' == c:
            MP -= ptr
            if MP < 0:
                raise BFError(f"Out of memory (0 cell)")
        elif '>' == c:
            MP += ptr
            if MP >= mem_size:
                raise BFError(f"Out of memory ({mem_size} cells)")
        elif '[' == c:
            if 0 == mem[MP]:
                CP = ptr
            else:
                cycles_count += 1
        elif ']' == c:
            CP = ptr - 1

        CP += 1

        if cycles_count > max_cycles:
            raise BFError(f"More than {max_cycles} steps")

    return mem

