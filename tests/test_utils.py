import pytest

from jpeg import utils


BITS_INT = {
    '1111101': 125,
    '1111110': 126,
    '1111111': 127,
    '1111': 15,
    '1110': 14,
    '1101': 13,
    '1100': 12,
    '1011': 11,
    '1010': 10,
    '1001': 9,
    '0111': 7,
    '1000': 8,
    '0110': 6,
    '0101': 5,
    '0100': 4,
    '0011': 3,
    '0010': 2,
    '0001': 1,
    '0000': 0,
}


def test_bits_to_int():
    for bits, int_ in BITS_INT.items():
        assert utils.bits_to_int(bits) == int_


def test_int_to_bits():
    for bits, int_ in BITS_INT.items():
        assert utils.int_to_bits(int_).zfill(len(bits)) == bits


def test_bits_to_int_and_back():
    for bits in BITS_INT.keys():
        int_ = utils.bits_to_int(bits)
        assert utils.int_to_bits(int_).zfill(len(bits)) == bits


def test_int_to_bits_and_back():
    for int_ in BITS_INT.values():
        bits = utils.int_to_bits(int_)
        assert utils.bits_to_int(bits) == int_


@pytest.mark.parametrize(
    "bits,expected",
    [('11101001', 233),
     ('1010110101', 693),
     ('1111000100', 964),
     ('1001111001', 633),
     ('1101101101', 877)]
)
def test_bits_to_int_large_numbers(bits, expected):
    assert utils.bits_to_int(bits) == expected


def test_zfill_bits_to_int():
    bits = '1010'
    assert utils.bits_to_int(bits) == utils.bits_to_int(bits.zfill(10))


@pytest.mark.parametrize(
    "number,expected",
    [(233, '11101001'),
     (693, '1010110101'),
     (964, '1111000100'),
     (633, '1001111001'),
     (877, '1101101101')]
)
def test_int_to_bits_large_numbers(number, expected):
    assert utils.int_to_bits(number) == expected
