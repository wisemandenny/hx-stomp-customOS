"""Block probe (diagnostic): the Edit view's top right corner shows the block-object allocator's last call, the current path's block
objects in use against its pool limit, and the request branch an add goes through."""
FLAG = 'HX_BLOCK_PROBE'
CONFLICTS = ('dsp_meter',)      # both draw in the Edit view's top right corner

EDIT_PAINT_LIT, EDIT_PAINT = 0x28d96da0, 0x28dc27f9     # the Edit view top half's paint function (block slots), as registered
SPIED = (       # (function, its first instructions, what, the spy that takes its entry)
    (0x28df4d24, bytes.fromhex('2de9f04f'), 'the block-object allocator', 'spy_alloc'),  # push.w {r4-r11,lr}
    (0x28e02ee0, bytes.fromhex('f0b599b0'), 'the request branch', 'spy_branch'),         # push {r4-r7,lr}; sub sp,#0x64
)


def apply(p):
    m = p.module('src/m4/block_probe.s')
    p.chain_ptr(EDIT_PAINT_LIT, EDIT_PAINT, after=m['paint'])
    for fn, stock, what, spy in SPIED:
        p.own_entry(fn, stock, what, m[spy])    # a spy needs the result, which a chain cannot see
