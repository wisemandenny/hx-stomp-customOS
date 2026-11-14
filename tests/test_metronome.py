"""tools/features/metronome.py and src/m4/metronome.s: the Metronome block's slot category in unicorn, and its block category and
hook in the firmware they build."""
import re
import struct

import pytest

import features
import patch_click
import patch_menu as pm
import setting_ids
from features import metronome as mt
from firmware import branch_target, built

MODS = features.load()
IDS = setting_ids.by_name()
CODE = 0x28e60000
VOLUME_PAN, LOOPER = 0x10, 0x12


class Slot:
    """metronome_slot in unicorn, called as the bl at the site is: the caller's block info at sp+4."""

    def __init__(self, m4emu):
        code, self.sym = m4emu.assemble('src/m4/metronome.s', MODS, IDS)
        self.m = m4emu.M4(code, CODE)
        self.sp = m4emu.STACK_TOP

    def __call__(self, preset_id, category):
        info = bytearray(0x34)
        struct.pack_into('<BI', info, 0, 1, preset_id & 0xffffffff)
        info[0xc] = category
        self.m.write(self.sp + 4, info)
        self.m.call(CODE + self.sym['metronome_slot'])
        return self.m.reg('r2')


@pytest.fixture
def slot(m4emu):
    return Slot(m4emu)


def test_the_metronome_gets_volume_pans_teal_pictures(slot):
    assert slot(patch_click.PRESET_ID, LOOPER) == VOLUME_PAN


@pytest.mark.parametrize('preset_id', (patch_click.PRESET_ID + 0x100, 0x1b5 + 0x10000, 509, 0, -1))
def test_every_other_block_keeps_its_category(slot, preset_id):
    assert slot(preset_id, LOOPER) == LOOPER
    assert slot(preset_id, 5) == 5


STUBS = {stub for _, _, stub, _ in mt.LOOPER_TESTS}


def category_load(m4emu, stub, preset_id, category):
    """A looper test site's stand-in in unicorn, with the caller's block info where its stub name says (reg, category offset)."""
    code, sym = m4emu.assemble('src/m4/metronome.s', MODS, IDS)
    m = m4emu.M4(code, CODE)
    reg, off = stub.split('_')[2:]
    info = bytearray(0x34)
    struct.pack_into('<BI', info, 0, 1, preset_id & 0xffffffff)
    info[0xc] = category
    m.write(m4emu.STACK_TOP + int(off, 16) - 0xc, info)
    m.call(CODE + sym[stub])
    return m.reg(reg)


@pytest.mark.parametrize('stub', sorted(STUBS))
def test_the_looper_tests_see_the_metronome_as_a_plain_effect(m4emu, stub):
    assert category_load(m4emu, stub, patch_click.PRESET_ID, LOOPER) not in (LOOPER, 0)


@pytest.mark.parametrize('stub', sorted(STUBS))
@pytest.mark.parametrize('preset_id', (patch_click.PRESET_ID + 0x100, 0x1b5 + 0x10000, 509, 0, -1))
def test_the_looper_tests_see_every_other_block_as_it_is(m4emu, stub, preset_id):
    assert category_load(m4emu, stub, preset_id, LOOPER) == LOOPER
    assert category_load(m4emu, stub, preset_id, VOLUME_PAN) == VOLUME_PAN


def test_each_looper_test_site_loads_the_category_its_stub_reads():
    for site, stock, stub, _ in mt.LOOPER_TESTS:
        reg, off = stub.split('_')[2:]
        ldrb = bytes.fromhex(stock)
        assert ldrb[:2] == bytes.fromhex('9df8') and ldrb[2] == int(off, 16) and ldrb[3] >> 4 == int(reg[1:]), hex(site)


VOLUME, UNKNOWN = 0x0e, 0x19


def assign_category(m4emu, preset_id, result=0, category=UNKNOWN):
    """metronome_assign_cat in unicorn, the block category getter stubbed to store category and return result: (r0, the byte)."""
    code, sym = m4emu.assemble('src/m4/metronome.s', MODS, IDS)
    m = m4emu.M4(code, CODE)
    out = m4emu.STACK_TOP - 0x100
    m.stub(mt.BLOCK_CATEGORY, lambda m: (m.u8(m.reg('r2'), category), m.reg('r0', result)))
    r0 = m.call(CODE + sym['metronome_assign_cat'], 0x28a00000, preset_id & 0xffffffff, out)
    assert [regs[:3] for regs in m.calls(mt.BLOCK_CATEGORY)] == [(0x28a00000, preset_id & 0xffffffff, out)]
    return r0, m.read(out, 1)[0]


def test_the_footswitch_assign_sees_the_metronome_as_volume(m4emu):
    assert assign_category(m4emu, patch_click.PRESET_ID) == (0, VOLUME)
    assert assign_category(m4emu, patch_click.PRESET_ID, result=7)[0] == 7


@pytest.mark.parametrize('preset_id', (patch_click.PRESET_ID + 0x100, 0x1b5 + 0x10000, 509, 0, -1))
def test_the_footswitch_assign_sees_every_other_block_as_it_is(m4emu, preset_id):
    assert assign_category(m4emu, preset_id) == (0, UNKNOWN)
    assert assign_category(m4emu, preset_id, category=5) == (0, 5)
    assert assign_category(m4emu, preset_id, result=-22 & 0xffffffff)[0] == -22 & 0xffffffff


STOCK_LED = 0x28e70000


def led_colour(m4emu, category, on=1):
    """metronome_led_colour in unicorn, r12 at a stub of the stock lookup: the category and on/off it passes on."""
    code, sym = m4emu.assemble('src/m4/metronome.s', MODS, IDS)
    m = m4emu.M4(code, CODE)
    m.stub(STOCK_LED)
    m.reg('r12', STOCK_LED | 1)
    m.call(CODE + sym['metronome_led_colour'], category, on)
    return m.calls(STOCK_LED)[0][:2]


def test_the_metronomes_led_takes_volumes_colour(m4emu):
    assert led_colour(m4emu, mt.METRONOME) == (VOLUME, 1)
    assert led_colour(m4emu, mt.METRONOME, on=0) == (VOLUME, 0)


@pytest.mark.parametrize('category', (0, 4, 7, VOLUME, 0x16, 0x17, 0x18, 0x1a, 0xff))
def test_every_other_leds_category_is_left_alone(m4emu, category):
    assert led_colour(m4emu, category) == (category, 1)


def test_its_constants_are_the_click_tools():
    asm = open(pm.ROOT + '/src/m4/metronome.s').read()
    assert int(re.search(r'\.equ PRESET_ID, (\d+)', asm).group(1)) == patch_click.PRESET_ID
    assert int(re.search(r'\.equ METRONOME, (0x[0-9a-f]+)', asm).group(1), 16) == mt.METRONOME
    assert mt.NAME == patch_click.DISPLAY.encode() and mt.FLAG == 'HX_CLICK' and not getattr(mt, 'SETTINGS', ())


@pytest.mark.firmware
def test_build_sends_the_slot_category_load_to_the_module(m4emu):
    code, sym = m4emu.assemble('src/m4/metronome.s', MODS, IDS)
    read, on = built({'HX_CLICK': '1'})
    assert 'metronome' in on
    module = branch_target(mt.SLOT_CATEGORY, read(mt.SLOT_CATEGORY, 4)) - sym['metronome_slot']
    assert read(module, len(code)) == code
    assert read(mt.SLOT_CATEGORY + 4, 4) == bytes.fromhex('83f8 3720'), 'the stock strb.w r2, [r3, #0x37] follows'
    for site, _, stub, what in mt.LOOPER_TESTS:
        assert branch_target(site, read(site, 4)) == module + sym[stub], what
    assert branch_target(mt.ASSIGN_CATEGORY, read(mt.ASSIGN_CATEGORY, 4)) == module + sym['metronome_assign_cat']
    tramp = branch_target(mt.LED_COLOUR, read(mt.LED_COLOUR, 4))
    assert branch_target(tramp + 8, read(tramp + 8, 4)) == module + sym['metronome_led_colour'], 'movw/movt r12, then b.w'


@pytest.mark.firmware
def test_build_makes_the_unknown_block_category_metronome_with_icon_tempo():
    read, _ = built({'HX_CLICK': '1'})
    rec = read(mt.CATEGORIES + 0x2c * mt.METRONOME, 0x2c)
    assert rec[:0x11].rstrip(b'\0') == rec[0x11:0x1c].rstrip(b'\0') == b'Metronome'
    colour, dim, icon, off = struct.unpack_from('<4I', rec, 0x1c)
    assert (colour, dim, icon) == (0x3cceb5, 0x21665d, pm.ICONS['Icon_Tempo']) and off not in (icon, 0xde)
    assert read(mt.CATEGORIES + 0x2c * 0x18, 0x2c)[:4] == b'None', 'the record before it is stock'


@pytest.mark.firmware
def test_without_the_flag_both_stay_stock():
    read, on = built({})
    assert 'metronome' not in on
    assert read(mt.SLOT_CATEGORY, 4) == mt.SLOT_CATEGORY_STOCK
    assert read(mt.CATEGORIES + 0x2c * mt.METRONOME, 0x2c) == mt.UNKNOWN_STOCK
    for site, stock, _, what in mt.LOOPER_TESTS:
        assert read(site, 4) == bytes.fromhex(stock), what
    assert branch_target(mt.ASSIGN_CATEGORY, read(mt.ASSIGN_CATEGORY, 4)) == mt.BLOCK_CATEGORY
    assert read(mt.LED_COLOUR, 4) == mt.LED_COLOUR_STOCK
