def saveIntermediate(filename, intermediate):
   writelist = [x+"\n" for x in intermediate]
   FILE = open(filename, "w")
   FILE.writelines(writelist)
   FILE.close()
   return

