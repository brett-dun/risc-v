
import pytest

from assembler import *


def test_enc_rv32i_jal():
    encoding: BitArray = build_j_type('jal', 'a7', 116088)
    val: int = bit_array_to_int(encoding)
    assert val == 0b01010111100000011100100011101111
