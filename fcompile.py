import RSVM
import sys

inf = ""
ind = ""
intype = sys.argv[1]
outtype = sys.argv[2].lower().split(",")
outfile = sys.argv[4]

sp = sys.argv[3].split("/")
if len(sp) > 1:
   inf = sp[-1]
   di = [x + "/" for x in sys.argv[3].split("/")[:-1] ]
   for x in di:
      ind = ind + x
else:
   inf = sys.argv[3]
   ind = "./"

#get the different types
if intype == "high":
   asm = RSVM.compileHighFileToAssemblyList(ind, inf)
   f   = RSVM.compileAssemblyListToFCodeList(asm)
   #p   = RSVM.compileFCodeListToPythonList(f)
   j   = RSVM.compileFCodeListToJavaList(f)
   #i   = RSVM.compileFCodeListToIntermediateList(f)

if "asm" in outtype or "fasm" in outtype:
   RSVM.saveAssembly(outfile + ".fasm", asm)

if "fcode" in outtype:
   RSVM.saveFCode(outfile + ".f", f)

if "python" in outtype:
   RSVM.savePython(outfile + ".py", p)

if "java" in outtype:
    RSVM.saveJava(outfile + ".java", j)

if "intermediate" in outtype:
    RSVM.saveIntermediate(outfile + ".i", i)

#asm = RSVM.compileHighFileToAssemblyList(ind, inf)
#RSVM.saveAssembly(outfile + ".fasm", asm)
#RSVM.compileAssemblyListToFCodeFile(asm, outfile+".f")
print "Done."
