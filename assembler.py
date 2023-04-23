"""
Generate .mem files from RISC-V assembly code.
"""

import sys
from typing import Dict


class AssemblerError(RuntimeError):
    pass


class RegisterError(AssemblerError):
    pass


registers: Dict[str, int] = {
    'zero': 0, # hard-wired zero
    'ra': 1,   # return address
    'sp': 2,   # stack pointer
    'gp': 3,   # global pointer
    'tp': 4,   # thread pointer
    't0': 5,   # temporary/alternate link register
    't1': 6,   # temporary
    't2': 7,   # temporary
    's0': 8,   # saved register
    'fp': 8,   # frame pointer (same register as s0)
    's1': 9,   # saved register
    'a0': 10,  # function argument/return value
    'a1': 11,  # function argument/return value
    'a2': 12,  # function argument
    'a3': 13,  # function argument
    'a4': 14,  # function argument
    'a5': 15,  # function argument
    'a6': 16,  # function argument
    'a7': 17,  # function argument
    's2': 18,  # saved register
    's3': 19,  # saved register
    's4': 20,  # saved register
    's5': 21,  # saved register
    's6': 22,  # saved register
    's7': 23,  # saved register
    's8': 24,  # saved register
    's9': 25,  # saved register
    's10': 26, # saved register
    's11': 27, # saved register
    't3': 28,  # temporary
    't4': 29,  # temporary
    't5': 30,  # temporary
    't6': 31,  # temporary
}


r_type_ops = {
    'add': {
        'opcode': 0b0110011,
        'funct3': 0x0,
        'funct7': 0x0,
    },
    'sub': {
        'opcode': 0b0110011,
        'funct3': 0x0,
        'funct7': 0x20,
    },
    'and': {
        'opcode': 0b0110011,
        'funct3': 0x7,
        'funct7': 0x0,
    },
}


def build_r_type(op: str, rd: str, rs1: str, rs2: str) -> int:
    if op not in r_type_ops:
        raise Exception()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")
    if rs1 not in registers:
        raise RegisterError(f"rs1='{rs1}' is not a valid RISC-V register.")
    if rs2 not in registers:
        raise RegisterError(f"rs2='{rs2}' is not a valid RISC-V register.")
    
    op_def = r_type_ops[op]
    opcode = op_def['opcode']
    funct3 = op_def['funct3']
    funct7 = op_def['funct7']
    rd_val = registers[rd]
    rs1_val = registers[rs1]
    rs2_val = registers[rs2]

    return opcode + (rd_val << 7) + (funct3 << 12) + (rs1_val << 15) + (rs2_val << 20) + (funct7 << 25)


if __name__ == "__main__":
    fname_in = sys.argv[1]
    fname_out = 'riscv.mem' if len(sys.argv) < 3 else sys.argv[2]

    obj_code = []

    with open(fname_in, encoding='utf-8') as f:
        for lino, line in enumerate(f.readlines()):
            op, instr = line.rstrip().split(' ', 1)
            match op:
                case 'add':
                    rd, rs1, rs2 = instr.split(', ')
                    obj_code.append(build_r_type('add', rd, rs1, rs2))
                case 'sub':
                    rd, rs1, rs2 = instr.split(', ')
                    obj_code.append(build_r_type('sub', rd, rs1, rs2))
                case 'and':
                    rd, rs1, rs2 = instr.split(', ')
                    obj_code.append(build_r_type('and', rd, rs1, rs2))
                case _:
                    print(f"'{instr[0]}' not recognized.")

    # Instruction memory expects 128 instructions.
    while len(obj_code) < 128:
        obj_code.append(0)

    with open(fname_out, 'w', encoding='utf-8') as wf:
        for x in obj_code:
            s = f'{x:08x}'
            wf.write(s+'\n')


