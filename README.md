# ASM Jump Tree

This is string processing project	

The main aim of this project is to visualize
the flow of ASM instruction.

ASM instructions can be get from Olly debugger

This code will generate the OUTPUT.gv file 
it can be viewed by Graphviz
Download Link : https://graphviz.gitlab.io/download/

# Try to analyze this!

0040B226  /$>MOV EDI,EDI\
0040B228  |.>PUSH EBP\
0040B229  |.>MOV EBP,ESP\
0040B22B  |.>SUB ESP,10\
0040B22E  |.>MOV EAX,DWORD PTR DS:[424174]\
0040B233  |.>AND DWORD PTR SS:[EBP-8],0\
0040B237  |.>AND DWORD PTR SS:[EBP-4],0\
0040B23B  |.>PUSH EBX\
0040B23C  |.>PUSH EDI\
0040B23D  |.>MOV EDI,BB40E64E\
0040B242  |.>MOV EBX,FFFF0000\
0040B247  |.>CMP EAX,EDI\
....



# Now see this!
![alt text](https://github.com/Andh001/ASM-Jump-Tree/blob/master/output.png)


Tree building is very simple..\
This tree is totally depends on the jump instructions..\

There are two types of jump instruction\
Conditional and Non conditional\

for conditional jump instructions we have two jumps ie true jump and false jump..(jne, je, jz, etc..)\
and for non conditional jump instruction ("JMP") have only one location..\

Logic:

global array = [] # contains the list of trees...


process until any jmp instructions is not found and store it into a array\
  if jump is conditional then create its 2 empty childs\
  else it must non conditional like "jmp" instruction then create only one empty child\
  
  above root node will going to be store as tree into the global array..\
  
  Now next time we are going to process other instructions..\
  and also create the empty nodes.. before this we are going to search into the global array..\
  if node is found then simply attach according to jump condition else add new root node into global array..!\
  
  
  
