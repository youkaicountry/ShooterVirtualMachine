def savePython(filename, python):
   writelist = [x+"\n" for x in python]
   FILE = open(filename, "w")
   FILE.writelines(writelist)
   FILE.close()
   return

