def saveJava(filename, java):
   writelist = [x+"\n" for x in java]
   FILE = open(filename, "w")
   FILE.writelines(writelist)
   FILE.close()
   return

