import RSVM
from RSVM.backend import java
import sys
import os

infile = sys.argv[1]
outfile = sys.argv[2]

ind, inf = os.path.split(infile)

asm = RSVM.compileHighFileToAssemblyList(ind, inf)
f   = RSVM.compileAssemblyListToFCodeList(asm)

j = java.fcode2java(f)
RSVM.output.saveFile(outfile, j)

