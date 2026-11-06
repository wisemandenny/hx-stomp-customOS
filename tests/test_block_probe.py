"""tools/features/block_probe.py and src/m4/block_probe.s: the spies on the block-object allocator and the request branch, the path
struct's block objects, and the lines they draw in the Edit view's top right corner, run in unicorn against fakes, and its hooks."""
import os
import types

import pytest

import features
import patch_amp as pa
import patch_menu as pm
import setting_ids
from features import block_probe

MODS = features.load()
IDS = setting_ids.by_name()

CODE, FB = 0x28e60000, 0x28d1ce98
DSP_PTR, DSP, PATH = 0x28449e78, 0x28500000, 0x28600000
FILL, WIDGET_LOCK, WIDGET_UNLOCK = 0x100017e8, 0x28e24970, 0x28e24ae8
DSP_LOCK, DSP_UNLOCK = 0x28e07844, 0x28e0785c
# Each stock function past the instructions its spy runs itself: (spy, where it continues, the pop that ends the fake)
BODIES = {'spy_alloc': (0x28df4d28, bytes.fromhex('bde8f08f')),         # pop.w {r4-r11,pc}
          'spy_branch': (0x28e02ee4, bytes.fromhex('19b0f0bd'))}        # add sp,#0x64; pop {r4-r7,pc}
FONT = {                            # what the glyphs must look like, independent of the module's encoding
    '0': ('###', '#.#', '#.#', '#.#', '###'), '1': ('.#.', '##.', '.#.', '.#.', '###'),
    '2': ('###', '..#', '###', '#..', '###'), '3': ('###', '..#', '###', '..#', '###'),
    '4': ('#.#', '#.#', '###', '..#', '..#'), '5': ('###', '#..', '###', '..#', '###'),
    '6': ('###', '#..', '###', '#.#', '###'), '7': ('###', '..#', '..#', '..#', '..#'),
    '8': ('###', '#.#', '###', '#.#', '###'), '9': ('###', '#.#', '###', '..#', '###'),
    '/': ('..#', '..#', '.#.', '#..', '#..'), '-': ('...', '...', '###', '...', '...'),
}
GLYPH = {tuple(rows): ch for ch, rows in FONT.items()}
WHITE, BLACK = 0xffffff, 0
TOP, GAP = 232, 14
ALLOC, OBJECTS, BRANCH = TOP, TOP - GAP, TOP - 2 * GAP


class Probe:
    def __init__(self, m4emu):
        code, self.sym = m4emu.assemble('src/m4/block_probe.s', MODS, IDS)
        self.m = m4emu.M4(code, CODE)
        self.fills, self.events, self.result, self.args = [], [], 0, None
        self.m.stub(FILL, self._fill)
        for fn, name in ((WIDGET_LOCK, 'widget lock'), (WIDGET_UNLOCK, 'widget unlock'), (DSP_LOCK, 'dsp lock'),
                         (DSP_UNLOCK, 'dsp unlock')):
            self.m.stub(fn, lambda m, name=name: self.events.append(name))
        for at, pop in BODIES.values():
            self.m.stub(at, self._body, code=pop)
        self.m.u32(DSP_PTR, DSP)
        self.m.u32(DSP + 0x43fc, PATH)
        self.pool(5)

    def _body(self, m):
        self.args = tuple(m.reg(f'r{i}') for i in range(4))
        m.reg('r0', self.result)

    def _fill(self, m):
        h, colour, anchor = m.stack_args(3)
        self.fills.append((m.reg('r1'), m.reg('r2'), m.reg('r3'), h, colour & 0xffffff, anchor & 0xff))
        self.events.append('fill')

    def pool(self, limit, *used):
        """The path struct's pool limit and which of its nine block objects are in use (bit 0 of +0x24)."""
        self.m.u8(PATH + 0xac4, limit)
        for k in range(9):
            self.m.u32(PATH + 0xaf0 + 0x9f4 * k + 0x24, 0x10 | (k in used))
        return self

    def call(self, spy, r1, r2, result):
        """The spied function called with (0x1234, r1, r2, 0x5678), its stock body returning result."""
        self.result = result
        got = self.m.call(CODE + self.sym[spy], 0x1234, r1, r2, 0x5678)
        assert got == result & 0xffffffff, 'the stock result goes back to the caller'
        assert self.args == (0x1234, r1 & 0xffffffff, r2 & 0xffffffff, 0x5678), 'the stock body gets the caller\'s arguments'
        return self

    def paint(self):
        self.fills.clear()
        self.events.clear()
        assert self.m.call(CODE + self.sym['paint'], FB, 0, 0, 0) == 0
        return self

    def lines(self):
        """{top edge: text} of the white glyphs, read back as the font draws them."""
        cells = {(x, y) for x, y, w, h, c, a in self.fills if c == WHITE and a == 0 and w == h == 2}
        out = {}
        for top in (ALLOC, OBJECTS, BRANCH):
            pts = {(x, y) for x, y in cells if top - 10 <= y < top}
            if not pts:
                continue
            left, right = min(x for x, _ in pts), max(x for x, _ in pts) + 2
            assert right == 316, 'right-aligned'
            text = ''
            for g in range((right - left + 2) // 8):
                rows = tuple(''.join('#' if (left + 8 * g + 2 * c, top - 2 * (r + 1)) in pts else '.' for c in range(3))
                             for r in range(5))
                text += GLYPH.get(rows, '?')
            out[top] = text
        return out


@pytest.fixture
def probe(m4emu):
    return Probe(m4emu)


def test_starts_with_no_calls_and_the_pool(probe):
    assert probe.paint().lines() == {ALLOC: '0/0/0/0', OBJECTS: '0/5/0/9', BRANCH: '0/0/0/0'}


def test_allocator_shows_whether_it_found_one_the_kind_and_the_limit(probe):
    probe.call('spy_alloc', PATH, 3, 0x28700000)
    assert probe.paint().lines()[ALLOC] == '1/1/3/5'
    probe.pool(7).call('spy_alloc', PATH, 0x21, 0)
    assert probe.paint().lines()[ALLOC] == '2/0/33/7'


def test_objects_in_use_below_and_from_the_limit(probe):
    assert probe.pool(5, 0, 1, 2, 3, 4, 6).paint().lines()[OBJECTS] == '5/5/1/9'
    assert probe.pool(9, 0, 8).paint().lines()[OBJECTS] == '2/9/0/9'


def test_no_objects_without_a_path_struct(probe):
    probe.m.u32(DSP + 0x43fc, 0)
    assert probe.paint().lines()[OBJECTS] == '0/0/0/0'
    assert probe.events[:3] == ['dsp lock', 'dsp unlock', 'widget lock']


def test_branch_shows_calls_result_and_arguments(probe):
    probe.call('spy_branch', 7, 3, 0).call('spy_branch', 7, 5000, -0x13)
    assert probe.paint().lines()[BRANCH] == '2/-19/7/999'


def test_lines_are_cleared_at_their_widest(probe):
    probe.paint()
    clears = [f for f in probe.fills if f[4] == BLACK]
    assert clears == [(316 - 150, top - 10, 150, 10, BLACK, 0) for top in (ALLOC, OBJECTS, BRANCH)]


def test_locks_are_taken_in_turn(probe):
    ev = probe.paint().events
    assert ev[:3] == ['dsp lock', 'dsp unlock', 'widget lock'], 'the DSP model lock is released before the widget lock is taken'
    assert ev[-1] == 'widget unlock'


def test_flag_conflict_and_spies():
    assert block_probe.FLAG == 'HX_BLOCK_PROBE'
    assert block_probe.CONFLICTS == ('dsp_meter',)
    assert [s for *_, s in block_probe.SPIED] == list(BODIES)


def stock_e0():
    stock = os.environ.get('HX_STOMP_HXF')
    if not stock:
        pytest.skip('HX_STOMP_HXF is not set')
    data, _ = pa.load_l6ia_from_any(stock)
    return pa.get_entry_swapped(data, 0)


@pytest.mark.firmware
def test_hooks_the_edit_paint_and_the_spied_functions():
    e0 = stock_e0()
    segs = pa._parse_e0_segments(e0)
    lit = pa._e0_vaddr_to_foff(segs, block_probe.EDIT_PAINT_LIT, 4)
    assert int.from_bytes(e0[lit:lit + 4], 'little') == block_probe.EDIT_PAINT
    for fn, stock, _, spy in block_probe.SPIED:
        o = pa._e0_vaddr_to_foff(segs, fn, len(stock))
        assert bytes(e0[o:o + len(stock)]) == stock
        assert BODIES[spy][0] == fn + len(stock), 'the stock body continues right after the instructions the spy copies'
    new, on = pm.menu_entry0(e0, MODS, {'HX_BLOCK_PROBE': '1'})
    assert 'block_probe' in [features.name(m) for m in on]
    assert int.from_bytes(new[lit:lit + 4], 'little') != block_probe.EDIT_PAINT
    for fn, stock, _, _ in block_probe.SPIED:
        o = pa._e0_vaddr_to_foff(segs, fn, len(stock))
        assert bytes(new[o:o + len(stock)]) != stock


@pytest.mark.firmware
def test_the_spied_functions_are_the_probes_alone():
    def other(p):
        p.chain_entry(block_probe.SPIED[1][0], block_probe.SPIED[1][1], after=p.add(b'\x70\x47'))
    demo = types.SimpleNamespace(__name__='features.demo', ORDER=200, apply=other)
    with pytest.raises(SystemExit, match='which block_probe owns'):
        pm.menu_entry0(stock_e0(), MODS + [demo], {'HX_BLOCK_PROBE': '1'})
