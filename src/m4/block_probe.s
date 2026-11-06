@ block_probe.s - a diagnostic in the Edit view's top right corner: three lines at 2x, four signed values each:
@   top:    the block-object allocator 0x28df4d24(ctx, path struct, kind): calls / got one (1) or none (0) / the kind / the struct's
@           pool limit, byte 0xac4
@   middle: the current path struct's ([dsp + 0x43fc]) nine block objects (0x9f4 bytes from +0xaf0, bit 0 of +0x24 in use): in use
@           below the pool limit / the limit / in use from it on / 9
@   bottom: 0x28e02ee0(ctx, r1, r2), the request dispatcher's (0x28e0fc14) branch an add goes through: calls / result / r1 / r2
@ tools/features/block_probe.py chains paint after the Edit view top half's stock paint and owns each function's entry with its spy;
@ patch_menu.py assembles this at build time.
.syntax unified
.thumb
.equ RIGHT, 316
.equ TOP, 232
.equ GAP, 14                        @ from one line's top to the next one's
.equ SCALE, 2
.equ MINUS, 11                      @ the glyph
.equ OBJECTS, 9

.thumb_func
spy_alloc:                          @ the entry of 0x28df4d24
    push {r4-r6, lr}
    mov r4, r2
    ldrb.w r5, [r1, #0xac4]
    bl alloc
    adr.w r6, seen
    ldr r1, [r6]
    adds r1, #1
    str r1, [r6]
    cmp r0, #0
    ite ne
    movne r1, #1
    moveq r1, #0
    strd r1, r4, [r6, #4]
    str r5, [r6, #12]
    pop {r4-r6, pc}

.thumb_func
spy_branch:                         @ the entry of 0x28e02ee0
    push {r4-r6, lr}
    mov r4, r1
    mov r5, r2
    bl branch
    adr.w r6, seen + 16
    ldr r1, [r6]
    adds r1, #1
    strd r1, r0, [r6]
    strd r4, r5, [r6, #8]
    pop {r4-r6, pc}

alloc:                              @ each stock function: its first instructions, then the rest of it, returning to its spy
    push.w {r4-r11, lr}
    ldr r12, =0x28df4d29
    bx r12
branch:
    push {r4-r7, lr}
    sub sp, #0x64
    ldr r12, =0x28e02ee5
    bx r12

.thumb_func
paint:                              @ r0 the framebuffer, r1 the Edit view's top half, after its stock paint
    push {r4-r7, lr}
    sub sp, #20                     @ 0 the objects' line
    mov r4, r0
    movs r0, #0
    strd r0, r0, [sp]
    strd r0, r0, [sp, #8]
    ldr r7, =0x28449e78             @ the DSP model
    ldr r7, [r7]
    cmp r7, #0
    beq objects_read
    movs r0, #0
    ldr r3, =0x28e07845             @ its lock; never held with the widget lock
    blx r3
    add.w r1, r7, #0x4000
    ldr r1, [r1, #0x3fc]
    cbz r1, objects_done
    ldrb.w r5, [r1, #0xac4]
    str r5, [sp, #4]
    movs r0, #OBJECTS
    str r0, [sp, #12]
    addw r2, r1, #0xaf0
    movs r6, #0
object:
    ldr r3, [r2, #0x24]
    lsls r3, r3, #31
    beq object_next
    cmp r6, r5
    ite lo
    addlo r0, sp, #0
    addhs r0, sp, #8
    ldr r3, [r0]
    adds r3, #1
    str r3, [r0]
object_next:
    addw r2, r2, #0x9f4
    adds r6, #1
    cmp r6, #OBJECTS
    bne object
objects_done:
    movs r0, #0
    ldr r3, =0x28e0785d
    blx r3
objects_read:
    ldr r3, =0x28e24971             @ the widget lock
    blx r3
    adr.w r0, seen
    movs r2, #TOP
    bl line
    mov r0, sp
    movs r2, #TOP - GAP
    bl line
    adr.w r0, seen + 16
    movs r2, #TOP - 2 * GAP
    bl line
    ldr r3, =0x28e24ae9
    blx r3
    movs r0, #0
    add sp, #20
    pop {r4-r7, pc}

.equ VALUES, 4
.equ WIDEST, VALUES * 5 - 1         @ glyphs: '-' and three digits a value, '/' between
line:                               @ r0 four words, r2 top edge, r4 the framebuffer: right-aligned, white, '/' between
    push {r5-r8, lr}
    sub sp, #36                     @ 0 fill height, 4 colour, 8 anchor, 12 glyphs (WIDEST at most)
    mov r5, r0
    movs r6, #VALUES
    mov r8, r2
    movs r0, #SCALE * 5
    str r0, [sp]
    movs r0, #0                     @ black: the last value may have been longer
    str r0, [sp, #4]
    str r0, [sp, #8]
    movw r1, #RIGHT - (WIDEST * 4 - 1) * SCALE
    sub.w r2, r8, #SCALE * 5
    movw r3, #(WIDEST * 4 - 1) * SCALE
    mov r0, r4
    ldr.w r12, =0x100017e9          @ the ROM rectangle fill (fb, x, y, w, h, colour, anchor)
    blx r12
    add r7, sp, #12
values:
    ldr r0, [r5], #4
    mov r1, r7
    bl digits
    mov r7, r0
    subs r6, #1
    beq built
    movs r2, #10
    strb r2, [r7], #1
    b values
built:
    add r0, sp, #12
    subs r1, r7, r0                 @ how many glyphs
    lsls r2, r1, #2
    subs r2, r2, #1
    movs r3, #SCALE
    mul r2, r2, r3
    rsb.w r2, r2, #RIGHT
    mov r3, r8
    bl put
    add sp, #36
    pop {r5-r8, pc}

digits:                             @ r0 a signed number (beyond 999 shows 999), r1 where its glyphs go -> r0 past them
    push {r4, lr}
    cmp r0, #0
    bge positive
    movs r2, #MINUS
    strb r2, [r1], #1
    negs r0, r0
positive:
    movw r2, #999
    cmp r0, r2
    it hi
    movhi r0, r2
    movs r3, #1
    cmp r0, #10
    it hs
    movhs r3, #2
    cmp r0, #100
    it hs
    movhs r3, #3
    adds r1, r1, r3
    mov r4, r1
    movs r2, #10
digit:
    udiv r12, r0, r2
    mls r3, r12, r2, r0
    strb r3, [r1, #-1]!
    movs r0, r12
    bne digit
    mov r0, r4
    pop {r4, pc}

put:                                @ r0 glyphs (0..9, 10 /, 11 -), r1 how many, r2 left edge, r3 top edge, r4 the framebuffer: white, at SCALE
    push {r5-r11, lr}
    sub sp, #16                     @ 0 fill height (the scale), 4 colour, 8 anchor, 12 top edge
    movs r5, #SCALE
    str r5, [sp]
    mvn r5, #0xff000000
    str r5, [sp, #4]
    movs r5, #0
    str r5, [sp, #8]                @ anchor 0: x, y the bottom left corner
    str r3, [sp, #12]
    mov r8, r0
    mov r7, r1
    mov r5, r2
    cmp r7, #0
    beq put_out
glyph:
    ldrb r0, [r8], #1
    adr.w r1, font
    ldrh.w r9, [r1, r0, lsl #1]
    ldr r6, [sp, #12]
    subs r6, r6, #SCALE             @ the top row's bottom edge
    movs r10, #5
row:
    movs r11, #0
col:
    tst r9, #0x4000
    beq off
    movs r3, #SCALE
    mla r1, r11, r3, r5
    mov r2, r6
    mov r0, r4
    ldr.w r12, =0x100017e9
    blx r12
off:
    lsl.w r9, r9, #1
    adds r11, #1
    cmp r11, #3
    bne col
    subs r6, r6, #SCALE
    subs r10, #1
    bne row
    add.w r5, r5, #SCALE * 4
    subs r7, #1
    bne glyph
put_out:
    add sp, #16
    pop {r5-r11, pc}

.ltorg
.balign 4
seen:                               @ the allocator's line, then the branch's: calls, last result, two more values
    .word 0, 0, 0, 0
    .word 0, 0, 0, 0
font:                               @ 3x5 glyphs, bit 14 the top left pixel, rows of 3 bits: 0..9, /, -
    .hword 0b111101101101111, 0b010110010010111, 0b111001111100111, 0b111001111001111, 0b101101111001001
    .hword 0b111100111001111, 0b111100111101111, 0b111001001001001, 0b111101111101111, 0b111101111001111
    .hword 0b001001010100100, 0b000000111000000
