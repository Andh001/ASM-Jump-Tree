# ASM Jump Tree

This is string processing project	

The main aim of this project is to visualize
the flow of ASM instruction.

ASM instructions can be get from Olly debugger

This code will generate the OUTPUT.gv file 
it can be viewed by Graphviz
Download Link : https://graphviz.gitlab.io/download/

# Try to analysis this!

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
