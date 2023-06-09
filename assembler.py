"""
Generate .mem files from RISC-V assembly code.
"""

import sys
from typing import Dict, List, Literal


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
    'x0': 0,
    'zero': 0, # hard-wired zero
    'x1': 1,
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


BitArray = List[Literal[0, 1]]


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


def int_to_bit_array(i: int, size: int = None) -> BitArray:
    res = [int(digit) for digit in bin(i)[2:]]
    if size is not None:
        while len(res) < size:
            res.insert(0, 0)
    return res


def build_r_type(op: str, rd: str, rs1: str, rs2: str) -> BitArray:
    if op not in r_type_ops:
        raise AssemblerError()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")
    if rs1 not in registers:
        raise RegisterError(f"rs1='{rs1}' is not a valid RISC-V register.")
    if rs2 not in registers:
        raise RegisterError(f"rs2='{rs2}' is not a valid RISC-V register.")
    
    op_def: RTypeFormat = r_type_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], size=7)
    funct3: BitArray = int_to_bit_array(op_def['funct3'], size=3)
    funct7: BitArray = int_to_bit_array(op_def['funct7'], size=7)
    rd_val: BitArray = int_to_bit_array(registers[rd], size=5)
    rs1_val: BitArray = int_to_bit_array(registers[rs1], size=5)
    rs2_val: BitArray = int_to_bit_array(registers[rs2], size=5)

    res = funct7 + rs2_val + rs1_val + funct3 + rd_val + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'
    
    return res


def build_i_type(op: str, rd: str, rs1: str, imm: int) -> BitArray:
    if op not in i_type_ops:
        raise AssemblerError()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")
    if rs1 not in registers:
        raise RegisterError(f"rs1='{rs1}' is not a valid RISC-V register.")

    op_def: ITypeFormat = i_type_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], size=7)
    funct3: BitArray = int_to_bit_array(op_def['funct3'], size=3)
    rd_val: BitArray = int_to_bit_array(registers[rd], size=5)
    rs1_val: BitArray = int_to_bit_array(registers[rs1], size=5)
    imm_bits: BitArray = int_to_bit_array(imm, size=12)

    res = imm_bits + rs1_val + funct3 + rd_val + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'

    return res


# TODO: test me
def build_i_type_special(op: str, rd: str, rs1: str, sham: int) -> BitArray:
    if op not in i_type_special_ops:
        raise AssemblerError()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")
    if rs1 not in registers:
        raise RegisterError(f"rs1='{rs1}' is not a valid RISC-V register.")

    op_def: ITypeSpecialFormat = i_type_special_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], 7)
    funct3: BitArray = int_to_bit_array(op_def['funct3'], 3)
    rd_val: BitArray = int_to_bit_array(registers[rd], size=5)
    rs1_val: BitArray = int_to_bit_array(registers[rs1], size=5)
    shamt_bits: BitArray = int_to_bit_array(sham, 5)
    imm: BitArray = int_to_bit_array(op_def['imm'], 7)

    res = imm + shamt_bits + rs1_val + funct3 + rd_val + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'

    return res


# TODO: test me
def build_s_type(op: str, rs1: str, rs2: str, imm: int) -> BitArray:
    if op not in s_type_ops:
        raise AssemblerError()
    if rs1 not in registers:
        raise RegisterError(f"rd='{rs1}' is not a valid RISC-V register.")
    if rs2 not in registers:
        raise RegisterError(f"rs1='{rs2}' is not a valid RISC-V register.")
    
    op_def: STypeFormat = s_type_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], 7)
    funct3: BitArray = int_to_bit_array(op_def['funct3'], 3)
    rs1_val: BitArray = int_to_bit_array(registers[rs1], 5)
    rs2_val: BitArray = int_to_bit_array(registers[rs2], 5)
    imm_bits: BitArray = int_to_bit_array(imm, 12)

    res = imm_bits[5:11+1] + rs2_val + rs1_val + funct3 + imm_bits[0:4+1] + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'

    return res


# TODO: test me
def build_b_type(op: str, rs1: str, rs2: str, imm: int) -> BitArray:
    if op not in b_type_ops:
        raise AssemblerError()
    if rs1 not in registers:
        raise RegisterError(f"rs1='{rs1}' is not a valid RISC-V register.")
    if rs2 not in registers:
        raise RegisterError(f"rs2='{rs2}' is not a valid RISC-V register.")
    
    op_def: BTypeFormat = b_type_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], 7)
    funct3: BitArray = int_to_bit_array(op_def['funct3'], 3)
    rs1_val: BitArray = int_to_bit_array(registers[rs1], 5)
    rs2_val: BitArray = int_to_bit_array(registers[rs2], 5)
    imm_bits: BitArray = int_to_bit_array(imm, 13)

    res = [imm_bits[12]] + imm_bits[5:10+1] + rs2_val + rs1_val + funct3 + imm_bits[1:4+1] + [imm_bits[11]] + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'

    return res


# TODO: test me
def build_u_type(op: str, rd: str, imm: int) -> BitArray:
    if op not in u_type_ops:
        raise AssemblerError()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")
    
    op_def: UTypeFormat = u_type_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], 7)
    rd_val: BitArray = int_to_bit_array(registers[rd], 5)
    imm_bits: BitArray = int_to_bit_array(imm, 32)

    res = imm_bits[12:31+1] + rd_val + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'

    return res


def build_j_type(op: str, rd: str, imm: int) -> BitArray:
    if op not in j_type_ops:
        raise AssemblerError()
    if rd not in registers:
        raise RegisterError(f"rd='{rd}' is not a valid RISC-V register.")

    op_def: JTypeFormat = j_type_ops[op]
    opcode: BitArray = int_to_bit_array(op_def['opcode'], 7)
    rd_val: BitArray = int_to_bit_array(registers[rd], 5)
    imm_bits: BitArray = int_to_bit_array(imm, 21)

    res = [imm_bits[20]] + imm_bits[1:10+1] + [imm_bits[11]] + imm_bits[12:19+1] + rd_val + opcode
    assert len(res) == 32, f'len(res)={len(res)} (expected 32)'

    return res


def bit_array_to_int(x: BitArray) -> int:
    return int(''.join(str(d) for d in x), 2)


if __name__ == "__main__":
    fname_in = sys.argv[1]
    fname_out = 'riscv.mem' if len(sys.argv) < 3 else sys.argv[2]

    obj_code: List[BitArray] = []

    with open(fname_in, encoding='utf-8') as f:
        for lino, line in enumerate(f.readlines()):
            # TODO: at some point I need to handle labels
            op, instr = line.rstrip().split(' ', 1)
            if op in r_type_ops:
                rd, rs1, rs2 = instr.split(', ')
                obj_code.append(build_r_type(op, rd, rs1, rs2))
            elif op in i_type_ops:
                rd, rs1, imm = instr.split(', ')
                imm = int(imm)
                obj_code.append(build_i_type(op, rd, rs1, imm))
            elif op in i_type_special_ops:
                raise NotImplementedError()
            elif op in s_type_ops:
                raise NotImplementedError('s-type instructions are not implemented yet.')
            elif op in b_type_ops:
                rs1, rs2, offset = instr.split(', ')
                offset = int(offset)
                obj_code.append(build_b_type(op, rs1, rs2, offset))
            elif op in u_type_ops:
                rd, imm = instr.split(', ')
                imm = int(imm)
                obj_code.append(build_u_type(op, rd, imm))
            elif op in j_type_ops:
                raise NotImplementedError('j-type instructions are not implemented yet.')
            else:
                # handle pseudo-instructions
                if op == 'nop':
                    obj_code.append(build_i_type('addi', 'x0', 'x0', 0))
                elif op == 'li':
                    # TODO: Implement this using some combination of lui + addi.
                    #   The exact instructions needed will depend on the specific
                    #   value of the immediate value being loaded.
                    raise NotImplementedError('li is not implemented yet.')
                elif op == 'mv':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_i_type('addi', rd, rs, 0))
                elif op == 'not':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_i_type('xori', rd, rs, -1))
                elif op == 'neg':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_r_type('sub', rd, 'x0', rs))
                elif op == 'negw':
                    raise NotImplementedError('negw is not implemented yet.')
                elif op == 'sext.w':
                    raise NotImplementedError('sext.w is not implemented yet.')
                elif op == 'seqz':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_i_type('sltiu', rd, rs, 1))
                elif op == 'snez':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_r_type('sltu', rd, 'x0', rs))
                elif op == 'sltz':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_r_type('slt', rd, rs, 'x0'))
                elif op == 'sgtz':
                    rd, rs = instr.split(', ')
                    obj_code.append(build_r_type('slt', rd, 'x0', rs))
                elif op == 'beqz':
                    rs, offset = instr.split(', ')
                    obj_code.append(build_b_type('beq', rs, 'x0', offset))
                elif op == 'bnez':
                    rs, offset = instr.split(', ')
                    obj_code.append(build_b_type('bne', rs, 'x0', offset))
                elif op == 'blez':
                    rs, offset = instr.split(', ')
                    obj_code.append(build_b_type('bge', 'x0', rs, offset))
                elif op == 'bgez':
                    rs, offset = instr.split(', ')
                    obj_code.append(build_b_type('bge', rs, 'x0', offset))
                elif op == 'bltz':
                    rs, offset = instr.split(', ')
                    obj_code.append(build_b_type('blt', rs, 'x0', offset))
                elif op == 'bgtz':
                    rs, offset = instr.split(', ')
                    obj_code.append(build_b_type('blt', 'x0', rs, offset))
                elif op == 'bgt':
                    rs, rt, offset = instr.split(', ')
                    obj_code.append(build_b_type('blt', rt, rs, offset))
                elif op == 'ble':
                    rs, rt, offset = instr.split(', ')
                    obj_code.append(build_b_type('bge', rt, rs, offset))
                elif op == 'bgtu':
                    rs, rt, offset = instr.split(', ')
                    obj_code.append(build_b_type('bltu', rt, rs, offset))
                elif op == 'bleu':
                    rs, rt, offset = instr.split(', ')
                    obj_code.append(build_b_type('bgeu', rt, rs, offset))
                elif op == 'j':
                    offset = instr
                    obj_code.append(build_j_type('jal', 'x0', offset))
                elif op == 'jal':
                    raise NotImplementedError()
                elif op == 'jr':
                    rs = instr
                    obj_code.append(build_i_type('jalr', 'x0', rs, 0))
                elif op == 'jalr':
                    raise NotImplementedError()
                elif op == 'ret':
                    obj_code.append(build_i_type('jalr', 'x0', 'x1', 0))
                elif op == 'call':
                    # TODO: implement
                    # auipc x1, offset[31 : 12] + offset[11]
                    # jalr x1, offset[11:0](x1)
                    raise NotImplementedError('call is not implemented yet.')
                elif op == 'tail':
                    # TODO: implement
                    # auipc x6, offset[31 : 12] + offset[11]
                    # jalr x0, offset[11:0](x6)
                    raise NotImplementedError('tail is not implemented yet.')
                else:
                    raise AssemblerError(f"'{instr[0]}' not recognized.")

    # Instruction memory expects 128 instructions.
    while len(obj_code) < 128:
        obj_code.append([0 for _ in range(32)])

    with open(fname_out, 'w', encoding='utf-8') as wf:
        for x in obj_code:
            num = int(''.join(str(d) for d in x), 2)
            s = f'{num:08x}'
            wf.write(s+'\n')
