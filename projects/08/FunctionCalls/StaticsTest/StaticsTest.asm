// bootstrapping code
@256
D=A
@SP
M=D
// call Sys.init 0
@Sys.init.RETURN
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
(Sys.init.RETURN)
// function Class1.set 0
(Class1.set)
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
// CommandType.C_POP SegmentTypes.STATIC 0
@SP
A=M-1
D=M
@Class1.0
M=D
@SP
M=M-1
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
// CommandType.C_POP SegmentTypes.STATIC 1
@SP
A=M-1
D=M
@Class1.1
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
// function Class1.get 0
(Class1.get)
// CommandType.C_PUSH SegmentTypes.STATIC 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.STATIC 1
@Class1.1
D=M
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
// CommandType.C_PUSH SegmentTypes.CONSTANT 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.CONSTANT 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
@Class1.set.RETURN
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set.RETURN)
// CommandType.C_POP SegmentTypes.TEMP 0
@0
D=A
@5
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
// CommandType.C_PUSH SegmentTypes.CONSTANT 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.CONSTANT 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
@Class2.set.RETURN
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set.RETURN)
// CommandType.C_POP SegmentTypes.TEMP 0
@0
D=A
@5
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
// call Class1.get 0
@Class1.get.RETURN
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
@Class1.get
0;JMP
(Class1.get.RETURN)
// call Class2.get 0
@Class2.get.RETURN
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
@Class2.get
0;JMP
(Class2.get.RETURN)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
// function Class2.set 0
(Class2.set)
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
// CommandType.C_POP SegmentTypes.STATIC 0
@SP
A=M-1
D=M
@Class2.0
M=D
@SP
M=M-1
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
// CommandType.C_POP SegmentTypes.STATIC 1
@SP
A=M-1
D=M
@Class2.1
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
// function Class2.get 0
(Class2.get)
// CommandType.C_PUSH SegmentTypes.STATIC 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.C_PUSH SegmentTypes.STATIC 1
@Class2.1
D=M
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
