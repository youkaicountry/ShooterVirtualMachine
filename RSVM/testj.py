a = 'mov r10 200\n\
sub r10 1\n\
cmp t2 r10 > 0\n\
cndjmp 6\n\
mov r10 200\n\
jmp 11\n\
call 36\n\
mov s16 s0\n\
mov s17 s1\n\
halt\n\
jmp 1\n\
mov r2 0\n\
cmp t2 r2 >= t5\n\
cndjmp 18\n\
cid r1 r2 t1\n\
call 32\n\
add r2 1\n\
jmp 12\n\
mov s16 s0\n\
mov s17 s1\n\
halt 100\n\
mov r2 0\n\
cmp t2 r2 >= t5\n\
cndjmp 28\n\
cid r1 r2 t1\n\
call 34\n\
add r2 1\n\
jmp 22\n\
mov s16 s0\n\
mov s17 s1\n\
halt 200\n\
jmp 1\n\
stv r0 1 r1\n\
return\n\
stv r1 1 r1\n\
return\n\
rnd s2\n\
mul s2 6.28318531\n\
call 158\n\
spawn 70\n\
stv s0 s3 t4\n\
stv s1 s4 t4\n\
stv s2 s2 t4\n\
rnd r1\n\
mul r1 3\n\
add r1 2\n\
stv s18 r1 t4\n\
rnd s2\n\
mul s2 6.28318531\n\
call 158\n\
spawn 70\n\
stv s0 s3 t4\n\
stv s1 s4 t4\n\
stv s2 s2 t4\n\
rnd r1\n\
mul r1 3\n\
add r1 2\n\
stv s18 r1 t4\n\
rnd s2\n\
mul s2 6.28318531\n\
call 158\n\
spawn 70\n\
stv s0 s3 t4\n\
stv s1 s4 t4\n\
stv s2 s2 t4\n\
rnd r1\n\
mul r1 3\n\
add r1 2\n\
stv s18 r1 t4\n\
return\n\
mov r2 200\n\
cmp t2 r0 == 1\n\
cndjmp 78\n\
call 99\n\
mov s16 s0\n\
mov s17 s1\n\
halt\n\
jmp 71\n\
mov s18 0\n\
cmp t2 r1 == 1\n\
cndjmp 85\n\
mov s16 s0\n\
mov s17 s1\n\
halt\n\
jmp 79\n\
rnd s2\n\
mul s2 6.28318531\n\
mov s19 .02\n\
sub r2 1\n\
cmp t2 r2 > 0\n\
cndjmp 93\n\
mov r2 200\n\
jmp 98\n\
call 99\n\
mov s16 s0\n\
mov s17 s1\n\
halt\n\
jmp 88\n\
terminate\n\
push r0\n\
push r1\n\
push r2\n\
push r3\n\
push r4\n\
push r5\n\
push r6\n\
add s7 s9\n\
add s8 s10\n\
add s0 s7\n\
add s1 s8\n\
add s18 s19\n\
cos r0 s2\n\
mul r0 s18\n\
add s0 r0\n\
sin r0 s2\n\
mul r0 s18\n\
add s1 r0\n\
add s25 s26\n\
add s2 s25\n\
add s21 s22\n\
add s23 s24\n\
sub r0 s0 s3\n\
sub r1 s1 s4\n\
mul r0 r0\n\
mul r1 r1\n\
add r0 r1\n\
sqrt r2 r0\n\
mov r3 s21\n\
cmp t2 s20 == 1.0\n\
cndjmp 131\n\
div r3 r2\n\
cos r4 r3\n\
sin r3 r3\n\
sub r0 s0 s3\n\
sub r1 s1 s4\n\
mul r5 r4 r0\n\
mul r6 r3 r1\n\
sub r5 r6\n\
add s0 s3 r5\n\
mul r5 r3 r0\n\
mul r6 r4 r1\n\
add r5 r6\n\
add s1 s4 r5\n\
div r2 1.0 r2\n\
mul r0 s23\n\
mul r0 r2\n\
add s0 s0 r0\n\
mul r1 s23\n\
mul r1 r2\n\
add s1 s1 r1\n\
pop r6\n\
pop r5\n\
pop r4\n\
pop r3\n\
pop r2\n\
pop r1\n\
pop r0\n\
return\n\
mov s3 s0\n\
mov s4 s1\n\
return\n\
cmp t2 t0 >= 0\n\
cndjmp 164\n\
return\n\
gtv s3 s0 t0\n\
gtv s4 s1 t0\n\
return\n\
mov s3 v0\n\
mov s4 v1\n\
return\n\
pop s4\n\
pop s3\n\
return\n\
push r3\n\
gtv r3 t5 r0\n\
sub r3 1\n\
cmp t2 r3 < 0\n\
cndjmp 190\n\
push r0\n\
cid r0 r3 r0\n\
push m1\n\
gtv m1 s0 r0\n\
add m1 r1\n\
stv s0 m1 r0\n\
gtv m1 s1 r0\n\
add m1 r2\n\
stv s1 m1 r0\n\
pop m1\n\
pop r0\n\
jmp 175\n\
pop r3\n\
return'.split("\n")

import rsvmcompiler
from rsvmcompiler.modules import FCode2Java
from rsvmcompiler.modules import FASM2FCode
from rsvmcompiler.languages import java
from rsvmcompiler.languages import fcode
from rsvmcompiler.languages import fasm

code = [fasm, [a]]

com = rsvmcompiler.CompilerChain([FCode2Java, FASM2FCode])
outcode = com.doCompile(code, java)

for l in outcode[1]:
    for o in l:
        print(o)
#print(com.graph.getVertexList())

#for l in gen["gen.java"]:
#    print(l)
    
