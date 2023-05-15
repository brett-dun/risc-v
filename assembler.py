"""
Generate .mem files from RISC-V assembly code.
"""

import sys
from typing import Dict, Literal


class AssemblerError(RuntimeError):
    '''
    Generic runtime error from the assembler.
    '''
    pass


class RegisterError(AssemblerError):
    '''
    Error occurs when the specified register does not exist or
    is invalid in the current context.
    '''
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


# TODO: in hindsight it might have been better to use a dataclass
RTypeFormat = Dict[Literal['opcode', 'funct3', 'funct7'], int]
ITypeFormat = Dict[Literal['opcode', 'funct3'], int]
ITypeSpecialFormat = Dict[Literal['opcode', 'funct3', 'imm'], int]
STypeFormat = Dict[Literal['opcode', 'funct3'], int]
BTypeFormat = Dict[Literal['opcode', 'funct3'], int]
UTypeFormat = Dict[Literal['opcode'], int]
JTypeFormat = Dict[Literal['opcode'], int]


r_type_ops: Dict[str, RTypeFormat] = {
    'add': {
        'opcode': 0b0110011,
        'funct3': 0b000,
        'funct7': 0b0000000,
    },
    'sub': {
        'opcode': 0b0110011,
        'funct3': 0b000,
        'funct7': 0b0100000,
    },
    'sll': {
        'opcode': 0b0110011,
        'funct3': 0b001,
        'funct7': 0b0000000,
    },
    'slt': {
        'opcode': 0b0110011,
        'funct3': 0b010,
        'funct7': 0b0000000,
    },
    'sltu': {
        'opcode': 0b0110011,
        'funct3': 0b011,
        'funct7': 0b0000000,
    },
    'xor': {
        'opcode': 0b0110011,
        'funct3': 0b100,
        'funct7': 0b0000000,
    },
    'srl': {
        'opcode': 0b0110011,
        'funct3': 0b101,
        'funct7': 0b0000000,
    },
    'sra': {
        'opcode': 0b0110011,
        'funct3': 0b101,
        'funct7': 0b0100000,
    },
    'or': {
        'opcode': 0b0110011,
        'funct3': 0b110,
        'funct7': 0b0000000,
    },
    'and': {
        'opcode': 0b0110011,
        'funct3': 0b111,
        'funct7': 0b0000000,
    },
}

i_type_ops: Dict[str, ITypeFormat] = {
    'addi': {
        'opcode': 0b0010011,
        'funct3': 0b000,
    },
    'slti': {
        'opcode': 0b0010011,
        'funct3': 0b010,
    },
    'sltiu': {
        'opcode': 0b0010011,
        'funct3': 0b011,
    },
    'xori': {
        'opcode': 0b0010011,
        'funct3': 0b100,
    },
    'ori': {
        'opcode': 0b0010011,
        'funct3': 0b110,
    },
    'andi': {
        'opcode': 0b0010011,
        'funct3': 0b111,
    },
    'lb': {
        'opcode': 0b0000011,
        'funct3': 0b000,
    },
    'lh': {
        'opcode': 0b0000011,
        'funct3': 0b001,
    },
    'lw': {
        'opcode': 0b0000011,
        'funct3': 0b010,
    },
    'lbu': {
        'opcode': 0b0000011,
        'funct3': 0b100,
    },
    'lhu': {
        'opcode': 0b0000011,
        'funct3': 0b101,
    },
    'jalr': {
        'opcode': 0b1100111,
        'funct3': 0b000,
    }
}

i_type_special_ops: Dict[str, ITypeSpecialFormat] = {
    'slli': {
        'opcode': 0b0010011,
        'funct3': 0b001,
        'imm': 0b0000000,
    },
    'srli': {
        'opcode': 0b0010011,
        'funct3': 0b101,
        'imm': 0b0000000,
    },
    'srai': {
        'opcode': 0b0010011,
        'funct3': 0b101,
        'imm': 0b0100000,
    }
}

s_type_ops: Dict[str, STypeFormat] = {
    'sb': {
        'opcode': 0b0100011,
        'funct3': 0b000,
    },
    'sh': {
        'opcode': 0b0100011,
        'funct3': 0b001,
    },
    'sw': {
        'opcode': 0b0100011,
        'funct3': 0b010,
    },
}

b_type_ops: Dict[str, BTypeFormat] = {
    'beq': {
        'opcode': 0b1100011,
        'funct3': 0b000,
    },
    'bne': {
        'opcode': 0b1100011,
        'funct3': 0b001,
    },
    'blt': {
        'opcode': 0b1100011,
        'funct3': 0b100,
    },
    'bge': {
        'opcode': 0b1100011,
        'funct3': 0b101,
    },
    'bltu': {
        'opcode': 0b1100011,
        'funct3': 0b110,
    },
    'bgeu': {
        'opcode': 0b1100011,
        'funct3': 0b111,
    },
}

u_type_ops: Dict[str, UTypeFormat] = {
    'lui': {
        'opcode': 0b0110111,
    },
    'auipc': {
        'opcode': 0b0010111,
    },
}

j_type_ops: Dict[str, JTypeFormat] = {
    'jal': {
        'opcode': 0b1100011,
    },
}


def build_r_type(op: str, rd: str, rs1: str, rs2: str) -> int:
    if op not in r_type_ops:
        raise AssemblerError()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")
    if rs1 not in registers:
        raise RegisterError(f"rs1='{rs1}' is not a valid RISC-V register.")
    if rs2 not in registers:
        raise RegisterError(f"rs2='{rs2}' is not a valid RISC-V register.")
    
    op_def: RTypeFormat = r_type_ops[op]
    opcode: int = op_def['opcode']
    funct3: int = op_def['funct3']
    funct7: int = op_def['funct7']
    rd_val: int = registers[rd]
    rs1_val: int = registers[rs1]
    rs2_val: int = registers[rs2]

    return opcode + (rd_val << 7) + (funct3 << 12) + (rs1_val << 15) + (rs2_val << 20) + (funct7 << 25)


def build_i_type(op: str, rd: str, rs1: str, imm: str) -> int:
    if op not in i_type_ops:
        raise AssemblerError()

    op_def: ITypeFormat = i_type_ops[op]
    opcode: int = op_def['opcode']
    funct3: int = op_def['funct3']

    # TODO
    return 0


def build_i_type_special(op: str, rd: str, rs1: str, sham: str) -> int:
    if op not in i_type_special_ops:
        raise AssemblerError()

    op_def: ITypeSpecialFormat = i_type_special_ops[op]
    opcode: int = op_def['opcode']
    funct3: int = op_def['funct3']
    imm: int = op_def['imm']

    # TODO
    return 0


def build_s_type(op: str, rs1: str, rs2: str, imm: str) -> int:
    if op not in s_type_ops:
        raise AssemblerError()
    
    op_def: STypeFormat = s_type_ops[op]

    # TODO
    return 0


def build_b_type(op: str, rs1: str, rs2: str, imm: str) -> int:
    if op not in b_type_ops:
        raise AssemblerError()
    
    op_def: BTypeFormat = b_type_ops[op]

    # TODO
    return 0


def build_u_type(op: str, rd: str, imm: str) -> int:
    if op not in u_type_ops:
        raise AssemblerError()
    
    op_def: UTypeFormat = u_type_ops[op]

    # TODO
    return 0


def build_j_type(op: str, rd: str, imm: str) -> int:
    if op not in j_type_ops:
        raise AssemblerError()

    op_def: JTypeFormat = j_type_ops[op]

    # TODO
    return 0


if __name__ == "__main__":
    fname_in = sys.argv[1]
    fname_out = 'riscv.mem' if len(sys.argv) < 3 else sys.argv[2]

    obj_code = []

    with open(fname_in, encoding='utf-8') as f:
        for lino, line in enumerate(f.readlines()):
            # TODO: at some point I need to handle labels
            op, instr = line.rstrip().split(' ', 1)
            if op in r_type_ops:
                rd, rs1, rs2 = instr.split(', ')
                obj_code.append(build_r_type(op, rd, rs1, rs2))
            elif op in i_type_ops:
                raise NotImplementedError()
            elif op in i_type_special_ops:
                raise NotImplementedError()
            elif op in s_type_ops:
                raise NotImplementedError()
            elif op in b_type_ops:
                raise NotImplementedError()
            elif op in u_type_ops:
                raise NotImplementedError()
            elif op in j_type_ops:
                raise NotImplementedError()
            else:
                # TODO: handle pseduo-instructions
                print(f"'{instr[0]}' not recognized.")

    # Instruction memory expects 128 instructions.
    while len(obj_code) < 128:
        obj_code.append(0)

    with open(fname_out, 'w', encoding='utf-8') as wf:
        for x in obj_code:
            s = f'{x:08x}'
            wf.write(s+'\n')
