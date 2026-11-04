@ dsp_meter.s - the per-block DSP usage meter: each block in the Edit view's signal-flow row shows its share of the DSP in per cent, in black.
@ The Edit view's top half (0x281282f8) has eight block slots, image widgets at view+0x4a4+0x24k, hidden when empty.
@ A block's DSP cost is the firmware's own, in hundredths of a per cent (the preset total adds 1500 and must stay within 9000).
@ Entry table: +0 the Edit view top half's paint function.
@ Position independent; tools/m4asm.py turns it into the bytes patch_menu.py appends to the code segment.
.syntax unified
.thumb
.global paint
.thumb_func
paint:                              @ r0 the framebuffer, r1 the Edit view's top half
    push {r4-r7, lr}
    sub sp, #36                     @ the eight slots' DSP costs, -1 for none
    mov r4, r0
    mov r5, r1
    ldr r3, =0x28dc27f9             @ the stock paint
    blx r3
    movs r6, #0
    mvn r0, #0
none:
    str.w r0, [sp, r6, lsl #2]
    adds r6, #1
    cmp r6, #8
    bne none
    ldr r7, =0x28449e78             @ the DSP model: block records of 0x54 bytes
    ldr r7, [r7]
    cbz r7, costed
    movs r0, #0
    ldr r3, =0x28e07845             @ its lock, as the stock block lookup 0x28e0fe94 takes it; never held with the widget lock
    blx r3
    movs r6, #0
cost:
    ldr r1, =0x2812c590             @ the slot model: the second row's categories at +0x3f
    adds r1, r1, r6
    ldrb r1, [r1, #0x3f]
    mov r0, r6
    cbz r1, first_row
    adds r0, #8                     @ the slot shows the second row's block, as the layout 0x28dc1a86 picks its image
first_row:
    movs r2, #0x54
    mla r0, r0, r2, r7
    ldr r0, [r0, #0x14]             @ the block's handle among the preset's nodes
    cmp r0, #0x4b
    bhi next_cost
    add.w r1, r7, #0x4400           @ the node table, as 0x28e0904c and 0x28dfa864 find it
    ldr r1, [r1]
    add.w r1, r1, r0, lsl #2
    ldr r1, [r1, #0x24]
    cbz r1, next_cost
    ldrb r2, [r1, #5]
    cmp r2, #1
    bne next_cost                   @ kind 1: a block object
    ldr r0, [r1, #0x44]             @ its cost, set at block load and summed into the preset total
    str.w r0, [sp, r6, lsl #2]
next_cost:
    adds r6, #1
    cmp r6, #8
    bne cost
    movs r0, #0
    ldr r3, =0x28e0785d
    blx r3
costed:
    ldr r3, =0x28e24971             @ the widget lock
    blx r3
    addw r5, r5, #0x4a4
    movs r6, #0
slot:                               @ the numbers are in the framebuffer only, so a slot the stock paint redrew or hid has lost its number
    ldrb r0, [r5, #0x1d]
    cbz r0, next
    ldr r0, [r5]
    cmp r0, #0x67
    beq next                        @ image 0x67 is every state of an empty slot, i.e. the cursor for placing a block
    ldr.w r1, [sp, r6, lsl #2]
    cmp r1, #0
    blt next
    adds r1, #50
    movs r2, #100
    udiv r1, r1, r2
    mov r0, r5
    bl number
next:
    adds r5, #0x24
    adds r6, #1
    cmp r6, #8
    bne slot
    ldr r3, =0x28e24ae9
    blx r3
    movs r0, #0
    add sp, #36
    pop {r4-r7, pc}

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
