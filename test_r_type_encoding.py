
import pytest

from assembler import *

# Use this as a reference for writing the tests: https://gitlab.com/luplab/rvcodecjs/-/blob/main/tests/encoderTest.js (https://luplab.gitlab.io/rvcodecjs/)

def test_enc_rv32i_add():
    # add t0, t1, t2
    encoding: BitArray = build_r_type('add', 't0', 't1', 't2')
    val: int = bit_array_to_int(encoding)
    assert val == 0b00000000011100110000001010110011


def test_enc_rv32i_sub():
    # sub t1, t2, t0
    encoding: BitArray = build_r_type('sub', 't1', 't2', 't0')
    val: int = bit_array_to_int(encoding)
    assert val == 0b01000000010100111000001100110011


def test_enc_rv32i_sll():
    # sll t2, t1, t0
    encoding: BitArray = build_r_type('sll', 't2', 't1', 't0')
    val: int = bit_array_to_int(encoding)
    assert val == 0b00000000010100110001001110110011


def test_enc_rv32i_slt():
    # slt t1, t2, t0
    encoding: BitArray = build_r_type('slt', 't1', 't2', 't0')
    val: int = bit_array_to_int(encoding)
    assert val == 0b00000000010100111010001100110011


def test_enc_rv32i_sltu():
    pass


def test_enc_rv32i_xor():
    pass


def test_enc_rv32i_srl():
    pass


def test_enc_rv32i_sra():
    pass


def test_enc_rv32i_or():
    pass


def test_enc_rv32i_and():
    pass
