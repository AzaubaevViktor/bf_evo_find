
from .bytecode import BFError

cpdef run(bytecode,
          int mem_size=10,
          int max_cycles=30000,
          list mem=None
          ):

    cdef int cycles_count = 0
    mem = mem or []
    mem = mem[:mem_size] + [0] * (mem_size - len(mem))
    cdef int MP = 0
    cdef int CP = 0


    cdef str c = ' '
    cdef int ptr = 0
    while CP < len(bytecode):
        c = bytecode[CP][0]
        ptr = bytecode[CP][1]

        if '+' == c:
            mem[MP] += ptr
            mem[MP] %= 256
        elif '-' == c:
            mem[MP] -= ptr
            mem[MP] %= 256
        elif '<' == c:
            MP -= ptr
        elif '>' == c:
            MP += ptr
        elif '[' == c:
            if 0 == mem[MP]:
                CP = ptr
            else:
                cycles_count += 1
        elif ']' == c:
            CP = ptr - 1

        CP += 1

        if MP >= mem_size:
            raise BFError(f"Out of memory ({mem_size} cells)")
        if MP < 0:
            raise BFError(f"Out of memory (0 cell)")

        if cycles_count > max_cycles:
            raise BFError(f"More than {max_cycles} steps")

    return mem