def loadAssembly(filename):
   out = []
   FILE = open(filename, "r")
   for x in FILE:
      out.append(x)
   FILE.close()
   return out
   
def saveAssembly(filename, assembly):
   writelist = [x+"\n" for x in assembly]
   FILE = open(filename, "w")
   FILE.writelines(writelist)
   FILE.close()
   return
