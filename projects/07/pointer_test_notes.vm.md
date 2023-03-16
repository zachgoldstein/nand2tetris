// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/MemoryAccess/PointerTest/PointerTest.vm

// Executes pop and push commands using the 
// pointer, this, and that segments.
push constant 3030
pop pointer 0 = pop RAM[THIS] => 3
push constant 3040
pop pointer 1 = pop RAM[THAT] => 4
push constant 32
pop this 2 = pop RAM[RAM[THIS] +2] => pop RAM[3030 +2] => 3032
push constant 46 
pop that 6 = pop RAM[RAM[THAT] +6] => pop RAM[3040 +6] => 3046
push pointer 0 =>  [3030]
push pointer 1 =>  [3030, 3040]
add => [6070]
push this 2 => [6070, 32]
sub => [6038]
push that 6 => [6038, 46]
add => [6084]
