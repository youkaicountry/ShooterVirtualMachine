import struct

def saveFCode(filename, fcode):
   FILE = open(filename, "w")
   
   for x in fcode:
      s = struct.pack("f", x)
      FILE.write(s)
   
   FILE.close()
   
def loadFCode(filename):
   fcode = []
   FILE = open(filename, "r")
   
   while True:
      a = FILE.read(4)
      if a == "": break
      fcode.append(*struct.unpack("f", a))
   
   FILE.close()
   #print fcode
   return fcode
