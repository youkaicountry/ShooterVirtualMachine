import rsvmcompiler
from rsvmcompiler.modules import FCode2Python
from rsvmcompiler.modules import FASM2FCode
from rsvmcompiler.modules import High2FASM
from rsvmcompiler.languages import python
from rsvmcompiler.languages import fcode
from rsvmcompiler.languages import fasm
from rsvmcompiler.languages import high

code = high.loadFromFile("./barrages/cirno/", "cirno1.ssc")

print(code)

com = rsvmcompiler.CompilerChain([FCode2Python, FASM2FCode, High2FASM])
outcode = com.doCompile(code, python)

#for l in outcode[1]:
#    for o in l:
#        print(o)

opf = python.constructOutputFiles(outcode)
print(opf)

for k in opf:
    f = open(k, "w")
    ll = [l+"\n" for l in opf[k]]
    f.writelines(ll)
    f.close()

#print(com.graph.getVertexList())

#for l in gen["gen.java"]:
#    print(l)
    
