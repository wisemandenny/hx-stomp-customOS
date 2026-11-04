@ dsp_meter.s - the per-block DSP usage meter in the Edit view's signal-flow row; for now each block shows its number, 1 to 8 left to right, in black.
@ The Edit view's top half (0x281282f8) has eight block slots, image widgets at view+0x4a4+0x24k, hidden when empty.
@ Entry table: +0 the Edit view top half's paint function.
@ Position independent; tools/m4asm.py turns it into the bytes patch_menu.py appends to the code segment.
.syntax unified
.thumb
.global paint
.thumb_func
paint:                              @ r0 the framebuffer, r1 the Edit view's top half
    push {r3-r7, lr}
    mov r4, r0
    mov r5, r1
    ldr r3, =0x28dc27f9             @ the stock paint
    blx r3
    ldr r3, =0x28e24971             @ the widget lock
    blx r3
    addw r5, r5, #0x4a4
    movs r6, #8
    movs r7, #0
slot:                               @ the numbers are in the framebuffer only, so a slot the stock paint redrew or hid has lost its number
    ldrb r0, [r5, #0x1d]
    cbz r0, next
    ldr r0, [r5]
    cmp r0, #0x67
    beq next                        @ image 0x67 is every state of an empty slot, i.e. the cursor for placing a block
    adds r7, #1
    mov r0, r5
    mov r1, r7
    bl number
next:
    adds r5, #0x24
    subs r6, #1
    bne slot
    ldr r3, =0x28e24ae9
    blx r3
    movs r0, #0
    pop {r3-r7, pc}

number:                             @ r0 an image widget, r1 a number 0..999, r4 the framebuffer
    push {r5-r11, lr}
    sub sp, #24                     @ 0 fill height (the scale), 4 colour, 8 anchor, 12 digits, 16 top edge, 20 block side
    mov r5, r0
    movw r3, #999
    cmp r1, r3
    it hi
    movhi r1, r3
    add r8, sp, #15
    movs r7, #0
    movs r3, #10
split:                              @ least significant first, so stored backwards
    udiv r2, r1, r3
    mls r0, r2, r3, r1
    strb r0, [r8, #-1]!
    adds r7, #1
    movs r1, r2
    bne split
    ldr r9, [r5, #0x14]
    ldr r10, [r5, #0x18]
    cmp r10, r9
    ite hi
    movhi r0, r9
    movls r0, r10
    str r0, [sp, #20]               @ the block is the square at the top of its image: move mode lifts it in a 28x40 one
    movs r11, #2
fit:                                @ the icon redraw erases only its own rectangle, so the digits must stay a pixel inside it
    lsls r0, r7, #2
    mul r0, r0, r11
    sub r0, r0, r11                 @ width: 3 columns and a 1-column gap per digit, at the scale
    adds r1, r0, #2
    cmp r1, r9
    bgt smaller
    add r1, r11, r11, lsl #2
    adds r1, #2
    ldr r2, [sp, #20]
    cmp r1, r2
    ble fits
smaller:
    subs r11, #1
    bne fit
    b out
fits:
    str r11, [sp]
    movs r1, #0
    str r1, [sp, #4]                @ black
    str r1, [sp, #8]                @ anchor 0: x, y the bottom left corner
    mov r6, r0
    ldrb r3, [r5, #0x1c]            @ the widget's anchor 0..8: column picks no, half or whole width left of x, row the same for height below y
    movs r2, #3
    udiv r1, r3, r2
    mls r0, r1, r2, r3
    mul r0, r0, r9
    mul r1, r1, r10
    ldr r2, [r5, #0xc]
    sub.w r2, r2, r0, asr #1
    add.w r2, r2, r9, asr #1        @ centre x
    sub.w r9, r2, r6, asr #1        @ the number's left edge
    ldr r2, [r5, #0x10]
    sub.w r2, r2, r1, asr #1
    add r2, r2, r10                 @ top edge
    ldr r3, [sp, #20]
    sub.w r2, r2, r3, asr #1        @ centre y of the block
    add r3, r11, r11, lsl #2
    adds r3, #1
    add.w r2, r2, r3, lsr #1
    str r2, [sp, #16]
    mov r5, r9
digit:
    ldrb r0, [r8], #1
    adr.w r1, font
    ldrh.w r9, [r1, r0, lsl #1]
    ldr r6, [sp, #16]
    ldr r3, [sp]
    subs r6, r6, r3                 @ the top row's bottom edge
    movs r10, #5
row:
    movs r11, #0
col:
    tst r9, #0x4000
    beq off
    ldr r3, [sp]
    mla r1, r11, r3, r5
    mov r2, r6
    mov r0, r4
    ldr.w r12, =0x100017e9          @ the ROM rectangle fill (fb, x, y, w, h, colour, anchor)
    blx r12
off:
    lsl.w r9, r9, #1
    adds r11, #1
    cmp r11, #3
    bne col
    ldr r3, [sp]
    subs r6, r6, r3
    subs r10, #1
    bne row
    ldr r3, [sp]
    add.w r5, r5, r3, lsl #2
    subs r7, #1
    bne digit
out:
    add sp, #24
    pop {r5-r11, pc}

.ltorg
.balign 2
font:                               @ 3x5 digits, bit 14 the top left pixel, rows of 3 bits
    .hword 0b111101101101111, 0b010110010010111, 0b111001111100111, 0b111001111001111, 0b101101111001001
    .hword 0b111100111001111, 0b111100111101111, 0b111001001001001, 0b111101111101111, 0b111101111001111
