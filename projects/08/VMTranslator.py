from io import TextIOWrapper
import argparse
from typing import List, Union, Literal
from dataclasses import dataclass
from enum import Enum
import pathlib
from os.path import isdir
from os import listdir


# non-pythonic class definitions and method names are from project instructions for consistency
class CommandType(Enum):
    C_ARITHMETIC = "C_ARITHMETIC"
    C_POP = "C_POP"
    C_PUSH = "C_PUSH"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IFGOTO = "C_IFGOTO"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"

class ArithmeticCommandTypes(Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

class SegmentTypes(Enum):    
    LOCAL = "local"
    ARGUMENT = "argument"
    THIS = "this"
    THAT = "that"
    CONSTANT = "constant"
    STATIC = "static"
    TEMP = "temp"
    POINTER = "pointer"

class Parser():
    # parses each VM command into its lexical elements

    @dataclass
    class FileLines():
        filename: str
        lines: List[str]

    fileReader: TextIOWrapper
    line_index:int = 0
    lines: List[str] = []
    file_data: List[FileLines]

    def __init__(self, file_location):
        self.file_data = []

        # Find if file_location is directory, load all .vm files if so
        if isdir(file_location):
            for file in listdir(file_location):
                if file.endswith(".vm"):
                    if DEBUG:
                        print(f"reading lines from file : {file}")
                    self.fileReader = open(f"{file_location}/{file}", "r")
                    lines = self.fileReader.readlines()
                    self.fileReader.close()
                    fileLines = self.FileLines(filename=file.strip(".vm"),lines=lines)
                    self.file_data.append(fileLines)

        else:
            if DEBUG:
                print(f"reading lines from file : {file_location}")
            self.fileReader = open(file_location, "r")
            lines = self.fileReader.readlines()
            self.fileReader.close()
            path = pathlib.PurePath(file_location)
            fileLines = self.FileLines(filename=path.name.strip(".vm"),lines=lines)
            self.file_data.append(fileLines)

        self.lines = self.cleanLines(self.lines)
        self.line_index = 0

    def useFileLines(self, file:FileLines):
        self.lines = self.cleanLines(file.lines)
        self.line_index = 0
    
    def cleanLines(self, lines: List[str]) -> List[str]:
        # just read the whole file, trim out whitespace, empty lines
        cleanLines = []
        for line in lines:
            cleanLine = self.trimLine(line)
            if cleanLine == "\n":
                continue
            cleanLines.append(cleanLine)
        return cleanLines

    def trimLine(self, line):
        # if DEBUG:
        #     print(f"trimming line:'{line}' ")
        # remove comments and whitespace
        lstripped = line.lstrip()
        # remove lines that start with comment
        if lstripped[0:2] == "//":
            # if DEBUG:
            #     print("trimmed to '\n'")
            return "\n"
        # remove comments at end of line
        if "//" in lstripped:
            lstripped = lstripped.split('//')[0]

        # strip newlines
        line_trimmed = lstripped.rstrip()
        # if DEBUG:
        #     print(f"trimmed to:'{line_trimmed}'")
        return line_trimmed

    def hasMoreLines(self) -> bool:
        if self.line_index >= len(self.lines) -1:
            return False
        return True

    def advance(self):
        if self.hasMoreLines():
            self.line_index += 1
            # print(f"advanced to line: {self.curr_line}")

    @property
    def curr_line(self) -> str:
        return self.lines[self.line_index]

    # Ex input: "push constant 10", returns C_PUSH
    @property
    def commandType(self) -> CommandType:
        command = self.curr_line.split(" ")[0]
        # if DEBUG:
        #     print(f"command: {command}")
        if command == "pop":
            return CommandType.C_POP
        elif command == "push":
            return CommandType.C_PUSH
        elif command == "return":
            return CommandType.C_RETURN
        elif command in [cmd.value for cmd in ArithmeticCommandTypes]:
            return CommandType.C_ARITHMETIC
        elif command == "label":
            return CommandType.C_LABEL
        elif command == "goto":
            return CommandType.C_GOTO
        elif command == "if-goto":
            return CommandType.C_IFGOTO
        elif command == "function":
            return CommandType.C_FUNCTION
        elif command == "return":
            return CommandType.C_RETURN
        elif command == "call":
            return CommandType.C_CALL
        raise Exception(f"Cannot find command type for '{command}'")
    
    @property
    def arithmeticCommandType(self) -> ArithmeticCommandTypes:
        command = self.curr_line.split(" ")[0]
        # if DEBUG:
        #     print(f"command: {command}")

        for cmd in ArithmeticCommandTypes:
            if command == cmd.value:
                return cmd
        raise Exception(f"Cannot find command type for '{command}'")

    # Return first argument. If C_ARITHMETIC, return command
    def arg1(self) -> str:
        if self.commandType == CommandType.C_RETURN:
            raise Exception("arg1 cannot be called when command type is CommandType.C_RETURN")
        if self.commandType == CommandType.C_ARITHMETIC:
            if DEBUG:
                print(f"arg1 called for arithmetic command {self.commandType}, not expected")
            return self.curr_line.split(" ")[0]
        return self.curr_line.split(" ")[1]
    
    def getSegmentType(self, segment_name: str) -> SegmentTypes:
        if segment_name == "local":
            return SegmentTypes.LOCAL
        elif segment_name == "argument":
            return SegmentTypes.ARGUMENT
        elif segment_name == "this":
            return SegmentTypes.THIS
        elif segment_name == "that":
            return SegmentTypes.THAT
        elif segment_name == "constant":
            return SegmentTypes.CONSTANT
        elif segment_name == "static":
            return SegmentTypes.STATIC
        elif segment_name == "temp":
            return SegmentTypes.TEMP
        elif segment_name == "pointer":
            return SegmentTypes.POINTER
        raise Exception(f"Unexpected segment type encountered {segment_name}")

    def arg2(self) -> int:
        if self.commandType == CommandType.C_RETURN:
            raise Exception("arg2 cannot be called when command type is CommandType.C_RETURN")
        if self.commandType not in [CommandType.C_PUSH, CommandType.C_POP, CommandType.C_FUNCTION, CommandType.C_CALL]:
            raise Exception(f"arg2 cannot be called when command type is {self.commandType}")
        return self.curr_line.split(" ")[2]


class CodeWriter():
    # writes the assembly code that implements the parsed command

    fileWriter: TextIOWrapper
    stack: List[str] = []
    labelCounter: int = 0
    file_name: str

    def __init__(self, file_location):
        path = pathlib.PurePath(file_location)
        self.file_location = path.name
        self.fileWriter = open(file_location, "w")
        self.file_name = ""

    @property
    def jumpLabel(self):
        return f"COND_JUMP.{self.labelCounter}"

    @property
    def endLabel(self):
        return f"COND_JUMP_END.{self.labelCounter}"

    def close(self):
        self.fileWriter.close()

    def bootstrap(self):
        asm = []
        if DEBUG:
            asm.append(f"// bootstrapping code")

        asm.append(f"@256")
        asm.append(f"D=A")
        asm.append(f"@SP")
        asm.append(f"M=D")
        
        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")        
        
        self.writeCall("Sys.init", 0)

    def writeFunction(self, function_name:str, nArgs:int):
        """
        We have to:
        • Inject an entry point label into the code
        • Initialize the local segment of the callee
        """
        asm = []
        if DEBUG:
            asm.append(f"// function {function_name} {nArgs}")
        
        asm.append(f"({function_name})")
        # Loop nArgs times, setting local segment to 0
        for _ in range(nArgs):
            asm.extend(self.getPushAsm(SegmentTypes.CONSTANT, 0))

        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")

    def writeCall(self, function_name:str, nArgs:int):
        returnAddrLabel = f"{function_name}.RETURN.{self.labelCounter}"
        asm = []
        if DEBUG:
            asm.append(f"// call {function_name} {nArgs}")

        """
        We have to:
        • Save the return address
        • Save the caller’s segment pointers
        • Reposition ARG (for the callee)
        • Reposition LCL (for the callee)
        • Go to execute the callee’s code
        """
        """
        // call function_name nArgs
        push retAddrLabel // Generates and pushes this label 
        push LCL // Saves the caller’s LCL
        push ARG // Saves the caller’s ARG
        push THIS // Saves the caller’s THIS 
        push THAT // Saves the caller’s THAT
        ARG=SP–5–nArgs //RepositionsARG
        LCL = SP // Repositions LCL
        goto function_name // Transfers control to the callee
        (retAddrLabel) // Injects this label into the code        
        """        
        # Save return address
        asm.append(f"@{returnAddrLabel}")
        asm.append(f"D=A")
        asm.append(f"@SP")
        asm.append(f"A=M")
        asm.append(f"M=D")
        asm.append(f"@SP")
        asm.append(f"M=M+1")

        # Save caller's segment pointers
        for segment in ["@LCL", "@ARG","@THIS", "@THAT"]:
            asm.append(segment)
            asm.append(f"D=M")
            asm.append(f"@SP")
            asm.append(f"A=M")
            asm.append(f"M=D")
            asm.append(f"@SP")
            asm.append(f"M=M+1")

        # ARG=SP–5–nArgs //RepositionsARG
        asm.append(f"@SP")
        asm.append(f"D=M")
        asm.append(f"@5")
        asm.append(f"D=D-A")
        asm.append(f"@{nArgs}")
        asm.append(f"D=D-A")
        asm.append(f"@ARG")
        asm.append(f"M=D")

        # LCL = SP // Repositions LCL
        asm.append(f"@SP")
        asm.append(f"D=M")
        asm.append(f"@LCL")
        asm.append(f"M=D")

        # goto function_name // Transfers control to the callee
        asm.append(f"@{function_name}")
        asm.append(f"0;JMP")

        asm.append(f"({returnAddrLabel})")
        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")


    def writeReturn(self):
        """
        We have to:
        1. Replace the arguments that the caller pushed with the value returned by the callee
        2. Recycle the memory used by the callee
        3. Reinstate the caller’s segment pointers
        4. Jump to the return address
        """
        asm = []
        if DEBUG:
            asm.append(f"// return")
        
        # endFrame = LCL // store the end of the frame in general purpose memory
        asm.append("@LCL")
        asm.append("D=M")
        asm.append("@endframe") # @endframe == R13
        asm.append("M=D")
        # retAddr = *(endFrame – 5) // store the return address (endframe - 5) in general purpose memory
        # load RAM[endFrame] into D
        asm.append("@endframe")
        asm.append("D=M")
        # D = RAM[RAM[endFrame] - 5]
        asm.append("@5")
        asm.append("D=D-A")
        asm.append("A=D")
        asm.append("D=M")
        asm.append("@retAddr")
        asm.append("M=D")
        # *ARG = pop()
        asm.append("@SP")
        asm.append("A=M-1")
        asm.append("D=M")
        asm.append("@ARG")
        asm.append("A=M")
        asm.append("M=D")
        asm.append("@SP")
        asm.append("M=M-1")
        # SP = ARG + 1
        asm.append("@ARG")
        asm.append("D=M+1")
        asm.append("@SP")
        asm.append("M=D")
        # Set THAT, THIS, ARG, LOCAL = endFrame - n
        n = 1
        for segment in ["THAT", "THIS", "ARG", "LCL"]:
            asm.append("@endframe") # @endframe == R13 (general purpose register)
            asm.append("D=M")
            asm.append(f"@{n}")
            asm.append("A=D-A")
            asm.append("D=M")
            asm.append(f"@{segment}")
            asm.append("M=D")
            n += 1

        # Go to return address
        asm.append("@retAddr")
        asm.append("A=M")
        asm.append("0;JMP")

        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")


    def writeLabel(self, label: str):
        asm = []
        if DEBUG:
            asm.append(f"// label {label}")
        
        asm.append(f"({label})")

        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")

    def writeGoto(self, label:str):
        asm = []
        if DEBUG:
            asm.append(f"// goto {label}")
        asm.append(f"@{label}")
        asm.append("0;JMP")

        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")

    def writeIfGoto(self, label:str):
        asm = []
        if DEBUG:
            asm.append(f"// if-goto {label}")
        # Pop off stack, into D reg
        asm.append("@SP")
        asm.append("A=M-1")
        asm.append("D=M")
        # Decrement SP 
        asm.append("@SP")
        asm.append("M=M-1")
        # Compare D Reg, if != 0, Goto label
        asm.append(f"@{label}")
        asm.append("D;JNE")
        
        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")

    def writeArithmetic(self, command: ArithmeticCommandTypes):
        if DEBUG:
            print(f"writeArithmetic command: {command}")
        asm = []
        if DEBUG:
            asm.append(f"// {command}")
        asm.extend(self.getArithmeticAsm(command))
        
        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")

    def getArithmeticAsm(self, command:ArithmeticCommandTypes) -> List[str]:
        asm = []
        # all commands pop the first time into A register
        asm.append("@SP")
        asm.append("A=M-1")
        # NOT or NEG just modify the popped value
        if command == ArithmeticCommandTypes.NOT:
            asm.append("M=!M")
            return asm
        if command == ArithmeticCommandTypes.NEG:
            asm.append("M=-M")
            return asm
        # Some commands pop a second time
        asm.append("D=M")
        asm.append("A=A-1")

        # ADD SUB AND OR are just calcs
        if command == ArithmeticCommandTypes.AND:
            asm.append("M=D&M")
        elif command == ArithmeticCommandTypes.OR:
            asm.append("M=D|M")
        elif command == ArithmeticCommandTypes.ADD:
            asm.append("M=D+M")
        elif command == ArithmeticCommandTypes.SUB:
            asm.append("M=M-D")
        elif command in [ArithmeticCommandTypes.LT, ArithmeticCommandTypes.GT, ArithmeticCommandTypes.EQ]:
            # Get difference for comparison
            asm.append("D=M-D")

            asm.append(f"@{self.jumpLabel}")
            # Jump if the statement is True.
            # Else update the Stack to False.
            if command == ArithmeticCommandTypes.LT:
                asm.append("D;JLT")
            elif command == ArithmeticCommandTypes.GT:
                asm.append("D;JGT")
            elif command == ArithmeticCommandTypes.EQ:
                asm.append("D;JEQ")
            # Push false to stack -1
            asm.append("@SP")
            asm.append("A=M-1")
            asm.append("A=A-1")
            asm.append("M=0")
            asm.append(f"@{self.endLabel}")
            asm.append('0;JMP')
            # # Jump label for the True state.
            asm.append(f"({self.jumpLabel})")
            asm.append('@SP')
            asm.append('A=M-1')
            asm.append('A=A-1')
            asm.append('M=-1')
            asm.append(f"({self.endLabel})")

        # Adjust stack top
        asm.append('@SP')
        asm.append('M=M-1')
        return asm
    
    def writePushPop(self, command: Literal[CommandType.C_PUSH, CommandType.C_POP], segment: SegmentTypes, index: int):
        if DEBUG:
            print(f"writePushPop command: {command}")
        asm = []
        if DEBUG:
            asm.append(f"// {command} {segment} {index}")
        if command == CommandType.C_PUSH:
            asm.extend(self.getPushAsm(segment, int(index)))
        elif command == CommandType.C_POP:
            asm.extend(self.getPopAsm(segment, int(index)))

        for asmLine in asm:
            if DEBUG:
                print(f"{asmLine}")
            self.fileWriter.write(f"{asmLine}\n")


    def getPushAsm(self, segment: SegmentTypes, index: int) -> List[str]:
        asm = []
        temp = "5"
        # From slides:
        # // push local i 
        # addr ← LCL + i
        # RAM[SP] ← RAM[addr] 
        # SP++

        if segment == SegmentTypes.CONSTANT:
            # constant: accessing constant i should result in supplying the constant i

            # Put constant in D register
            asm.append(f"@{index}")
            asm.append(f"D=A")

        elif segment == SegmentTypes.STATIC:
            # static: accessing static i within file Foo.vm should result in accessing
            # the assembly variable Foo.i

            # Put label in D register
            asm.append(f"@{self.file_name}.{index}")
            asm.append("D=M")

        # local, argument, this, that:
        # allocated dynamically to the RAM (in project 8)
        # The base addresses of these allocations are kept in the segment pointers LCL, ARG, THIS, THAT
        # accessing segment i should result in accessing RAM[segmentPointer + i]
        elif segment in [SegmentTypes.LOCAL,SegmentTypes.ARGUMENT, SegmentTypes.THIS, SegmentTypes.THAT]:
            # Add up segmentPointer + index

            # Put index in D register for adding
            asm.append(f"@{index}")
            asm.append(f"D=A")
            # Put segmentPointer in A register
            if segment == SegmentTypes.LOCAL:
                asm.append("@LCL")
            elif segment == SegmentTypes.ARGUMENT:
                asm.append("@ARG")
            elif segment == SegmentTypes.THIS:
                asm.append("@THIS")
            elif segment == SegmentTypes.THAT:
                asm.append("@THAT")
            asm.append("A=M")
            # Add index + segmentPointer, put into A
            asm.append("A=D+A")
            # Put the source value into D (used to set SP later)
            asm.append("D=M")

        elif segment == SegmentTypes.TEMP:
            # temp: fixed segment, mapped on RAM addresses 5-12.
            # accessing temp i should result in accessing RAM[5 + i]
            # For now just use @5 for temp

            # Put index in D register for adding
            asm.append(f"@{index}")
            asm.append(f"D=A")
            # Put temp in A reg for adding
            asm.append(f"@{temp}")
            # Add index + temp, put into A
            asm.append("A=D+A")
            # Put the source value into D (used to set SP later)
            asm.append("D=M")

        elif segment == SegmentTypes.POINTER:
            # pointer: fixed segment, mapped on RAM addresses 3-4.
            # accessing pointer 0 should result in accessing THIS accessing pointer 1 should result in accessing THAT
            # RAM[SP] = THIS|THAT
            pointerType = ""
            if index == 0:
                pointerType = "THIS"
            else:
                pointerType = "THAT"

            asm.append(f"@{pointerType}")
            # A = RAM[THIS]
            asm.append(f"A=M") 
            # Put RAM[THIS] in D reg
            asm.append(f"D=A")
 
        # RAM[SP] = D
        asm.append(f"@SP")
        asm.append(f"A=M")
        asm.append(f"M=D")

        # Increment stack pointer
        asm.append(f"@SP")
        asm.append(f"M=M+1")

        return asm

    def getPopAsm(self, segment: SegmentTypes, index: int) -> List[str]:
        # // pop local i 
        # addr ← LCL + i
        # SP--
        # RAM[addr] ← RAM[SP]

        asm = []
        temp = "5"
        general_use = "R13"

        if segment == SegmentTypes.CONSTANT:
            raise Exception("Cannot pop with 'constant' segment")

        if segment == SegmentTypes.STATIC:
            # Set A reg to RAM[SP]-1
            asm.append("@SP")
            asm.append("A=M-1")
            # D reg = RAM[A]
            asm.append("D=M")
            asm.append(f"@{self.file_name}.{index}")
            asm.append("M=D")
            # SP--
            asm.append("@SP")
            asm.append("M=M-1")
            return asm

        # addr ← LCL + i
        if segment in [SegmentTypes.LOCAL,
                        SegmentTypes.ARGUMENT, 
                        SegmentTypes.THIS, 
                        SegmentTypes.THAT, 
                        SegmentTypes.TEMP]:
            # Add up segmentPointer + index

            asm.append(f"@{index}")
            asm.append(f"D=A")
            # Put segmentPointer in A register
            if segment == SegmentTypes.LOCAL:
                asm.append("@LCL")
                asm.append("A=M")
                asm.append("D=D+A")
            elif segment == SegmentTypes.ARGUMENT:
                asm.append("@ARG")
                asm.append("A=M")
                asm.append("D=D+A")
            elif segment == SegmentTypes.THIS:
                asm.append("@THIS")
                asm.append("A=M")
                asm.append("D=D+A")
            elif segment == SegmentTypes.THAT:
                asm.append("@THAT")
                asm.append("A=M")
                asm.append("D=D+A")
            elif segment == SegmentTypes.TEMP:
                asm.append(f"@{temp}")
                asm.append("D=D+A")

            # Store the addr value in R13 for later use. (Need D reg for RAM[SP])
            asm.append(f"@{general_use}")
            asm.append("M=D")

        elif segment == SegmentTypes.POINTER:
            # RAM[SP] = THIS|THAT
            pointerType = ""
            if index == 0:
                pointerType = "THIS"
            else:
                pointerType = "THAT"
            asm.append(f"@{pointerType}")
            # Put RAM[THIS] in D reg
            asm.append(f"D=A")
            
            # Store the addr value in R13 for later use. (Need D reg for RAM[SP])
            asm.append(f"@{general_use}")
            asm.append("M=D")

        # Now do RAM[addr] ← RAM[SP]

        # A reg = RAM[SP]-1
        asm.append(f"@SP")
        asm.append(f"A=M-1")

        # Set D reg to RAM[SP]
        asm.append(f"D=M")

        # Set A = RAM[R13] (RAM[R13] is addr)
        asm.append(f"@{general_use}")
        asm.append(f"A=M")

        # Set RAM[addr] = D reg
        asm.append(f"M=D")

        # SP-- b/c we want to decrement SP
        asm.append(f"@SP")
        asm.append(f"M=M-1")
    
        return asm



def main():
    global DEBUG
    argparser = argparse.ArgumentParser(description='Assembler')
    argparser.add_argument('--fileread')
    argparser.add_argument('--filewrite')
    argparser.add_argument('--debug', action=argparse.BooleanOptionalAction)
    argparser.add_argument('--nobootstrap', action=argparse.BooleanOptionalAction)

    args = argparser.parse_args()
    if args.debug is not None:
        DEBUG = args.debug
    if DEBUG:
        print("Running VMTranslator")
        print(f"reading from {args.fileread}")
        print(f"writing to {args.filewrite}")
        print(f"nobootstrap? {args.nobootstrap}")

    parser = Parser(args.fileread)
    codeWriter = CodeWriter(args.filewrite)

    # If multiple files, always use Main.vm first

    # Call Sys.Init first
    # option to disable this for files like SimpleFunction
    if args.nobootstrap is None:
        codeWriter.file_name = parser.file_data[0].filename
        codeWriter.bootstrap()

    for fileLines in parser.file_data:
        if DEBUG:
            print(f"using file {fileLines.filename}")
        parser.useFileLines(fileLines)
        codeWriter.file_name = fileLines.filename

        # Read in each line and translate it
        while parser.hasMoreLines():
            parser.advance()
            if parser.curr_line == "":
                continue
            # Increment label counter so we always have a unique label
            # needed for jumps during gt, lt, eq
            codeWriter.labelCounter += 1

            if DEBUG:
                print(f"interpreting line '{parser.curr_line}'")
            if parser.commandType == CommandType.C_ARITHMETIC:
                codeWriter.writeArithmetic(parser.arithmeticCommandType)
            elif parser.commandType in [CommandType.C_POP, CommandType.C_PUSH]:
                parser_arg1 = parser.arg1()
                segment = parser.getSegmentType(parser_arg1)
                index = parser.arg2()
                codeWriter.writePushPop(parser.commandType, segment, int(index))
            elif parser.commandType == CommandType.C_LABEL:
                label = parser.arg1()
                codeWriter.writeLabel(label)
            elif parser.commandType == CommandType.C_GOTO:
                label = parser.arg1()
                codeWriter.writeGoto(label)
            elif parser.commandType == CommandType.C_IFGOTO:
                label = parser.arg1()
                codeWriter.writeIfGoto(label)
            elif parser.commandType == CommandType.C_FUNCTION:
                functionName = parser.arg1()
                nArgs = parser.arg2()
                codeWriter.writeFunction(functionName, int(nArgs))
            elif parser.commandType == CommandType.C_RETURN:
                codeWriter.writeReturn()
            elif parser.commandType == CommandType.C_CALL:
                functionName = parser.arg1()
                # filename = functionName.split(".")[0]
                # function = functionName.split(".")[1]
                nArgs = parser.arg2()
                codeWriter.writeCall(functionName, int(nArgs))


    codeWriter.close()

DEBUG = True

if __name__ == "__main__":
    main()