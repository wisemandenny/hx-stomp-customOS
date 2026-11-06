"""tools/features/max_blocks.py: the free-block-slot counter's three hard-coded 8s, raised to HX_MAX_BLOCKS."""
import os

import pytest

import features
import patch_amp as pa
import patch_menu as pm
from features import max_blocks


def stock_e0():
    stock = os.environ.get('HX_STOMP_HXF')
    if not stock:
        pytest.skip('HX_STOMP_HXF is not set')
    data, _ = pa.load_l6ia_from_any(stock)
    return pa.get_entry_swapped(data, 0)


def read(e0, va, n):
    o = pa._e0_vaddr_to_foff(pa._parse_e0_segments(e0), va, n)
    return bytes(e0[o:o + n])


def test_flag_takes_only_9():
    (i,) = max_blocks.INPUTS
    assert max_blocks.FLAG == i.var == 'HX_MAX_BLOCKS'
    assert i.choices == ('9',), 'a path struct has nine block objects: a pool limit above 9 would run past them'


@pytest.mark.parametrize('n', [8, 9])
def test_new_bytes_decode_to_the_stock_instructions_with_n(n):
    s = max_blocks.sites(n)
    assert s[max_blocks.INIT][1] == bytes((n, 0x23))                # movs r3,#n
    assert s[max_blocks.CLEAR][1] == bytes((n, 0x22))               # movs r2,#n
    assert s[max_blocks.RECOUNT][1] == bytes((0xc6, 0xf1, n, 0x01))  # rsb.w r1,r6,#n
    assert all(len(stock) == len(new) for stock, new, _ in s.values())
    if n == 8:
        assert all(new == stock for stock, new, _ in s.values()), 'n 8 is the stock count'


@pytest.mark.firmware
def test_build_writes_only_the_three_sites():
    e0 = stock_e0()
    for va, (stock, _, _) in max_blocks.sites(9).items():
        assert read(e0, va, len(stock)) == stock
    new, on = pm.menu_entry0(e0, features.load(), {'HX_MAX_BLOCKS': '9'})
    assert 'max_blocks' in [features.name(m) for m in on]
    base, _ = pm.menu_entry0(e0, features.load(), {})
    for va, (stock, want, _) in max_blocks.sites(9).items():
        assert read(base, va, len(stock)) == stock
        assert read(new, va, len(want)) == want


@pytest.mark.firmware
def test_refuses_bytes_that_are_not_stock():
    e0 = bytearray(stock_e0())
    o = pa._e0_vaddr_to_foff(pa._parse_e0_segments(e0), max_blocks.RECOUNT, 4)
    e0[o:o + 4] = b'\xff\xff\xff\xff'
    with pytest.raises(SystemExit, match='the free-slot recount'):
        pm.menu_entry0(bytes(e0), features.load(), {'HX_MAX_BLOCKS': '9'})
