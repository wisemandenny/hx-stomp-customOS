"""Max Blocks (experiment): a preset may hold HX_MAX_BLOCKS blocks (9) instead of 8."""
import struct

from features import Input

FLAG = 'HX_MAX_BLOCKS'
INPUTS = (Input(FLAG, choices=('9',)),)     # a path struct has nine block objects, so 9 is the most; each kind has its own

# preset[0xac0] counts the free block slots; adding a block needs one. These three set it from a hard-coded 8.
INIT, INIT_STOCK = 0x28df5cf6, bytes.fromhex('0823')            # movs r3,#8, the preset init
CLEAR, CLEAR_STOCK = 0x28df4b40, bytes.fromhex('0822')          # movs r2,#8, a preset clear
RECOUNT, RECOUNT_STOCK = 0x28df85ee, bytes.fromhex('c6f10801')  # rsb.w r1,r6,#8: free = 8 - path A's count


def sites(n):
    """{address: (stock bytes, new bytes, what)} for a limit of n blocks."""
    return {INIT: (INIT_STOCK, bytes((n, 0x23)), 'the preset init'),
            CLEAR: (CLEAR_STOCK, bytes((n, 0x22)), 'a preset clear'),
            RECOUNT: (RECOUNT_STOCK, struct.pack('<2H', 0xf1c6, 0x0100 | n), 'the free-slot recount')}


def apply(p):
    n = int(p.input(FLAG))
    for va, (stock, new, what) in sites(n).items():
        p.expect(va, stock, what)
        p.put(va, new, what)
