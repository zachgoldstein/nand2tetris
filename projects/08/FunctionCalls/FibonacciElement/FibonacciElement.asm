// bootstrapping code
@256
D=A
@SP
M=D
// call Sys.init 0
@Sys.init.RETURN.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init.RETURN.0)
// function Main.fibonacci 0
(Main.fibonacci)
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
// ArithmeticCommandTypes.LT
@SP
A=M-1
D=M
A=A-1
D=M-D
@COND_JUMP.4
D;JLT
@SP
A=M-1
A=A-1
M=0
@COND_JUMP_END.4
0;JMP
(COND_JUMP.4)
@SP
A=M-1
A=A-1
M=-1
(COND_JUMP_END.4)
@SP
M=M-1
// if-goto IF_TRUE
@SP
A=M-1
D=M
@SP
M=M-1
@IF_TRUE
D;JNE
// goto IF_FALSE
@IF_FALSE
0;JMP
// label IF_TRUE
(IF_TRUE)
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
// return
@LCL
D=M
@endframe
M=D
@endframe
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M+1
@SP
M=D
@endframe
D=M
@1
A=D-A
D=M
@THAT
M=D
@endframe
D=M
@2
A=D-A
D=M
@THIS
M=D
@endframe
D=M
@3
A=D-A
D=M
@ARG
M=D
@endframe
D=M
@4
A=D-A
D=M
@LCL
M=D
@retAddr
A=M
0;JMP
// label IF_FALSE
(IF_FALSE)
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
// call Main.fibonacci 1
@Main.fibonacci.RETURN.14
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci.RETURN.14)
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
// call Main.fibonacci 1
@Main.fibonacci.RETURN.18
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci.RETURN.18)
// ArithmeticCommandTypes.ADD
@SP
A=M-1
D=M
A=A-1
M=D+M
@SP
M=M-1
// return
@LCL
D=M
@endframe
M=D
@endframe
D=M
@5
D=D-A
A=D
D=M
@retAddr
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@SP
M=M-1
@ARG
D=M+1
@SP
M=D
@endframe
D=M
@1
A=D-A
D=M
@THAT
M=D
@endframe
D=M
@2
A=D-A
D=M
@THIS
M=D
@endframe
D=M
@3
A=D-A
D=M
@ARG
M=D
@endframe
D=M
@4
A=D-A
D=M
@LCL
M=D
@retAddr
A=M
0;JMP
// function Sys.init 0
(Sys.init)
// CommandType.C_PUSH SegmentTypes.CONSTANT 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Main.fibonacci 1
@Main.fibonacci.RETURN.23
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci.RETURN.23)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
