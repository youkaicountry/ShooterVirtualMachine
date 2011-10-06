def constructOutputFiles(code, fname="gen.py"):
    bp = {}
    gen = __constructMainFile(code, fname)
    bp.update(gen)
    return bp

def fromString(string):
    return None

def optimize(code, options={}):
    return

def __constructMainFile(code, fname):
    ucode = code[1]
    outdic={}
    ent=[]
    #append the first part of the boilerplate code
    ent += bp_1
    
    #append the switch statement code
    for i in range(len(ucode)):
        ent.append("      self.block2func["+str(i)+"] = self.__f"+str(i))
    
    #append the second part of the boilerplate code
    ent += bp_2
    
    #append the generated code
    for i, block in enumerate(ucode):
        ent.append("   def __f"+str(i)+"(self, thread):")
        ent += block
    
    outdic[fname] = ent
    return outdic

def __repr__():
    return "python"

bp_1="import math\n\
import random\n\
class Thread:\n\
   def __init__(self, codeloc = 0.0, regsize=64):\n\
      self.codeloc = codeloc\n\
      self.registers = []\n\
      for x in xrange(regsize):\n\
         self.registers.append(0.0)\n\
      self.state = []\n\
      for x in xrange(30):\n\
         self.state.append(0.0)\n\
      self.sleep = 0\n\
      self.children = []\n\
      self.codestack=[]\n\
      self.varstack=[]\n\
      self.threadvars = []\n\
      for x in xrange(8):\n\
         self.threadvars.append(0.0)\n\
      self.threadvars[0] = -1\n\
\n\
class RSVM:\n\
   def __init__(self, r = random.Random(), memsize=64, regsize=32):\n\
      self.threads = {}\n\
      self.mem = []\n\
      self.r = r\n\
      self.vmdata = []\n\
      self.vmdata.append(0.0)\n\
      self.vmdata.append(0.0)\n\
      self.regsize = regsize\n\
      for i in xrange(memsize):\n\
         self.mem.append(0.0)\n\
      self.nextthread = 0.0\n\
      self.block2func = {}".split("\n")



bp_2="self.statename = {}\n\
      self.statename['x'] = 0\n\
      self.statename['__x'] = 0\n\
      self.statename['y'] = 1\n\
      self.statename['__y'] = 1\n\
      self.statename['angle'] = 2\n\
      self.statename['__angle'] = 2\n\
      self.statename['targetx'] = 3\n\
      self.statename['__targetx'] = 3\n\
      self.statename['targety'] = 4\n\
      self.statename['__targety'] = 4\n\
      self.statename['returnval'] = 5\n\
      self.statename['__returnval'] = 5\n\
      self.statename['condition'] = 6\n\
      self.statename['__condition'] = 6\n\
      self.statename['sprite'] = 27\n\
      self.statename['__sprite'] = 27\n\
      self.statename['radius'] = 28\n\
      self.statename['__radius'] = 28\n\
   def spawnThread(self, initloc, x, y, angle, parent=None):\n\
      nt = self.nextthread\n\
      self.threads[nt] = Thread(initloc, self.regsize)\n\
      self.threads[nt].state[0] = x\n\
      self.threads[nt].state[1] = y\n\
      self.threads[nt].state[2] = angle\n\
      self.threads[nt].threadvars[1] = nt\n\
      if parent != None:\n\
         self.threads[nt].threadvars[0] = parent\n\
         self.threads[parent].children.append(nt)\n\
      else:\n\
         self.threads[nt].threadvars[0] = -1\n\
      self.nextthread += 1\n\
      return nt\n\
      self.vmdata[0] = x\n\
      self.vmdata[1] = y\n\
      return\n\
   def getThreadParent(self, threadID):\n\
      return self.threads[threadID].threadvars[0]\n\
   def getThreadChildren(self, threadID):\n\
      return self.threads[threadID].children\n\
   def getState(self, threadID, name):\n\
      return self.threads[threadID].state[self.statename[name]]\n\
   def getThreadIDs(self):\n\
      return self.threads.keys()\n\
   def run(self):\n\
      trun = [self.threads[t] for t in self.threads.keys()]\n\
      for thread in trun:\n\
         while thread.sleep <= 0:\n\
            thread.codeloc = self.block2func[thread.codeloc](thread)\n\
         thread.sleep -= 1\n\
      return\n".split("\n")
      
