import h2a
import a2f
import f2p
import fcode
import high
import f2j
import f2i

def compileHighFileToAssemblyList(directory, filename):
   h = high.loadHigh(directory, filename)
   return h2a.high2assembly(*h)
   
def compileHighListToFCodeList(high):
   a = h2a.high2assembly(high)
   return a2f.assembly2high(a)
   
def compileHighFileToFCodeList(directory, filename):
   al = compileHighFileToAssemblyList(directory, filename)
   return compileHighListToFCodeList(al)
   
def compileAssemblyListToFCodeFile(asm, outfile):
   f = a2f.assembly2fcode(asm)
   fcode.saveFCode(outfile, f)
   return
   
def compileAssemblyListToFCodeList(asm):
   return a2f.assembly2fcode(asm)
   
def compileHighFileToFCodeFile(directory, filename, outfile):
   f = compileHighFileToFCodeList(directory, filename)
   fcode.saveFCode(outfile, f)
   return
   
def compileFCodeListToPythonFile(python, outfile):
   p = f2p.fcode2python(python)
   python.savePython(outfile, p)
   return
   
def compileFCodeListToPythonList(python):
   p = f2p.fcode2python(python)
   return p

def compileFCodeListToJavaFile(java, outfile):
   p = f2p.fcode2python(python)
   python.savePython(outfile, p)
   return
   
def compileFCodeListToJavaList(java):
   p = f2j.fcode2java(java)
   return p

def compileFCodeListToIntermediateFile(java, outfile):
   p = f2p.fcode2intermediate(python)
   python.savePython(outfile, p)
   return

def compileFCodeListToIntermediateList(intermediate):
   p = f2i.fcode2intermediate(intermediate)
   return p

