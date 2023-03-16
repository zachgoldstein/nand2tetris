// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// R1 is how many times to add R1 to R0
// keep looping and decrementing until done
; i = R1
; R2 = R0
; Loop
;     R2 += R1
;     i--
;     if i > 0
;         goto loop
;     else 
;         end

    @R1
    D=M

    @i
    M=D

    @R2
    M=0

(LOOP)
    @i
    D=M

    @STOP
    D;JEQ

    @R0
    D=M

    @R2
    M=M+D

    @i
    M=M-1

    @LOOP
    0;JMP
(STOP)
    @STOP
    0;JMP