// CommandType.C_PUSH SegmentTypes.ARGUMENT 1
@1
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP SegmentTypes.POINTER 1
@THAT
D=A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH SegmentTypes.CONSTANT 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP SegmentTypes.THAT 0
@0
D=A
@THAT
A=M
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH SegmentTypes.CONSTANT 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_POP SegmentTypes.THAT 1
@1
D=A
@THAT
A=M
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH SegmentTypes.ARGUMENT 0
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.CONSTANT 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// ArithmeticCommandTypes.SUB
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// CommandType.C_POP SegmentTypes.ARGUMENT 0
@0
D=A
@ARG
A=M
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// label MAIN_LOOP_START
(MAIN_LOOP_START)
// CommandType.C_PUSH SegmentTypes.ARGUMENT 0
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT
@SP
A=M-1
D=M
@SP
M=M-1
@COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM
@END_PROGRAM
0;JMP
// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// CommandType.C_PUSH SegmentTypes.THAT 0
@0
D=A
@THAT
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.THAT 1
@1
D=A
@THAT
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// ArithmeticCommandTypes.ADD
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
// CommandType.C_POP SegmentTypes.THAT 2
@2
D=A
@THAT
A=M
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH SegmentTypes.POINTER 1
@THAT
A=M
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.CONSTANT 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// ArithmeticCommandTypes.ADD
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
// CommandType.C_POP SegmentTypes.POINTER 1
@THAT
D=A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// CommandType.C_PUSH SegmentTypes.ARGUMENT 0
@0
D=A
@ARG
A=M
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.CONSTANT 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// ArithmeticCommandTypes.SUB
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
M=M-1
// CommandType.C_POP SegmentTypes.ARGUMENT 0
@0
D=A
@ARG
A=M
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
// label END_PROGRAM
(END_PROGRAM)
