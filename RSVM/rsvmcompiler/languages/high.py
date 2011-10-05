import sys

def constructOutputFiles(code, fname="gen.ssc"):
    gen = __constructMainFile(code, high)
    return bp.update(gen)

def fromString(string):
    return None

def optimize(code, options={}):
    return

def __constructMainFile(code, fname):
    ucode = code[1]
    outdic={}
    ent=[]
    
    for l in ucode:
        ent.append(l)
    
    outdic[fname] = ent
    return outdic

def __getBoilerPlateFiles():
    return {}
   
def __repr__():
    return "high"


def loadFromFile(directory, filename, lib=("./lib/","lib_rsvm.ssc")):
   if len(directory) > 0:
      if directory[-1] != "/":
         directory = directory + "/"
   #read the file
   files = [[directory, filename]]
   filestoload = [[directory, filename]]
   namespaces = [""]
   for x in range(0,len(lib),2):
      files.append([lib[x], lib[x+1]])
      filestoload.append([lib[x], lib[x+1]])
      namespaces.append("")
   codes = {}
   
   mainns = __getNamespace(directory.split("/"))
   #print "MAIN_NS: " + mainns
   while len(filestoload) > 0:
      #print filestoload
      f = open(filestoload[0][0]+filestoload[0][1], "r")

      instructions = []

      for x in f:
         b = x.split("#")[0]
         a = b.split()
         if len(a) == 0:
            continue
         if a[0].lower() == "import":
            p = __getParts(a[1])
            ns = __getNamespace((filestoload[0][0]+p[0]).split("/"))
            ns = ns.replace(mainns, "", 1)
            if len(ns) > 0 and ns[0] == ".": ns = ns[1:]
            #print "FOR P1: " + str(p[1]) + " NAMESPACE IS: " + ns
            realp = [filestoload[0][0]+p[0], p[1]]
            if realp not in files:
               files.append(realp)
               filestoload.append(realp)
               namespaces.append(ns)
               #print "NS:" + str(namespaces)
         else:
            #print b.strip().lower()
            instructions.append(b.strip().lower())
            #print instructions

      f.close()
      name = __getName(filestoload[0][1])
      cname = namespaces[0]+"."+name
      if cname[0] == ".": cname = cname[1:]
      """codes[cname] = {}
      codes[cname]["code"] = instructions #(name, code)""" #use cname for full directory namespaces
      codes[name] = {}
      codes[name]["code"] = instructions
      filestoload.pop(0)
      namespaces.pop(0)
   return [sys.modules[__name__], codes, __getName(filename)] 
   
def __getName(filename):
   return filename.split("/")[-1].split(".")[0]
   
def __getParts(name):
   f = name.split("/")[-1]
   d = name[:-len(f)]
   return [d, f]
   
def __getNamespace(inp):
   nsa = [x for x in inp if x != "." and x != ""]
   st = ""
   for x in nsa:
      st = st + str(x) + "."
   if st[:-1] == None: return ""
   return st[:-1] 
   
