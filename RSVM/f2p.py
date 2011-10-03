code2sign = {}
code2sign[0.0] = "=="
code2sign[1.0] = "<"
code2sign[2.0] = ">"
code2sign[3.0] = ">="
code2sign[4.0] = "<="
code2sign[5.0] = "!="

def __getVal(v1, v2, owner):
   if v1 == 0.0:
      return owner+".registers["+str(int(v2))+"]"
   if v1 == 1.0:
      return str(v2)
   if v1 == 2.0:
      return owner+".state["+str(int(v2))+"]"
   if v1 == 3.0:
      return "self.mem["+str(int(v2))+"]"
   if v1 == 4.0:
      return "self.vmdata["+str(int(v2))+"]"
   if v1 == 7.0:
      if v2 == 5.0:
         return "len("+owner+".children)"
      return owner+".threadvars["+str(int(v2))+"]"
   return "0"

def __addTabWidth(lines, tabwidth):
   return [((" "*3)*tabwidth) + l for l in lines]
   #print lines

def __inst_halt(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("thread.sleep = "+__getVal(inst[1], inst[2], "thread"))
   out.append("return "+str(blocknum+1))
   out = __addTabWidth(out, tabwidth)
   return out

def __inst_mov(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append(__getVal(inst[1], inst[2], "thread")+" = "+__getVal(inst[3], inst[4], "thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_terminate(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("tid = thread.threadvars[1]")
   out.append("if thread.threadvars[0] >= 0:")
   out.append("   self.threads[thread.threadvars[0]].children.remove(tid)")
   out.append("for x in thread.children:")
   out.append("   self.threads[x].threadvars[0] = -1")
   out.append("del self.threads[tid]")
   out.append("thread.threadvars[6] = 1.0")
   out.append("thread.sleep = 1")
   out.append("return 0")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_jmp(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("return self.__f"+str(lineinfo[int(inst[2])][2])+"(thread)")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_add(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = "+__getVal(inst[3],inst[4],"thread")+" + "+__getVal(inst[5],inst[6],"thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_sub(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = "+__getVal(inst[3],inst[4],"thread")+" - "+__getVal(inst[5],inst[6],"thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_mul(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = "+__getVal(inst[3],inst[4],"thread")+" * "+__getVal(inst[5],inst[6],"thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_div(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = "+__getVal(inst[3],inst[4],"thread")+" / "+__getVal(inst[5],inst[6],"thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_rnd(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append(__getVal(inst[1],inst[2],"thread")+" = self.r.random()")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_sin(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = math.sin("+__getVal(inst[3],inst[4],"thread")+")")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_cos(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = math.cos("+__getVal(inst[3],inst[4],"thread")+")")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_mod(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = "+__getVal(inst[3],inst[4],"thread")+" % "+__getVal(inst[5],inst[6],"thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_call(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("thread.codestack.append("+str(blocknum+1)+")")
   out.append("return self.__f"+str(lineinfo[int(inst[2])][2])+"(thread)")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_return(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("thread.threadvars[3] = " + __getVal(inst[1],inst[2],"thread"))
   out.append("return thread.codestack.pop()")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_cmp(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append(__getVal(inst[1],inst[2],"thread")+" = "+__getVal(inst[3],inst[4],"thread")+code2sign[inst[6]]+__getVal(inst[7],inst[8],"thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_cndjmp(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("if thread.threadvars[2]:")
   out.append("   return self.__f"+str(lineinfo[int(inst[2])][2])+"(thread)")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_cndcall(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("if thread.threadvars[2]:")
   out.append("   thread.codestack.append("+str(blocknum+1)+")")
   out.append("   return self.__f"+str(lineinfo[int(inst[2])][2])+"(thread)")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_push(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("thread.varstack.append("+__getVal(inst[1],inst[2],"thread")+")")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_pop(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append(__getVal(inst[1],inst[2],"thread")+" = thread.varstack.pop()")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_spawn(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   out.append("pid = thread.threadvars[1]")
   out.append("t = self.spawnThread("+str(lineinfo[int(inst[2])][2])+", 0, 0, 0, pid)")
   out.append("thread.threadvars[4] = t")
   out = __addTabWidth(out, tabwidth)
   return out
     
def __inst_gtv(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   owner = "self.threads["+__getVal(inst[5], inst[6], "thread")+"]"
   out.append(__getVal(inst[1],inst[2], "thread")+" = "+__getVal(inst[3], inst[4], owner))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_stv(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   owner = "self.threads["+__getVal(inst[5], inst[6], "thread")+"]"
   out.append(__getVal(inst[1],inst[2], owner)+" = "+__getVal(inst[3], inst[4], "thread"))
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_atan2(inst, tabwidth, blocknum, lineinfo, instnum):   
   out= []
   out.append("a = math.atan2("+__getVal(inst[3],inst[4],"thread")+", "+__getVal(inst[5], inst[6], "thread")+")")
   out.append("if a < 0:")
   out.append("   a += 6.28318531")
   out.append(__getVal(inst[1], inst[2], "thread")+" = a")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_trl(inst, tabwidth, blocknum, lineinfo, instnum):
   return ["line1", "line2..."]
   
def __inst_cid(inst, tabwidth, blocknum, lineinfo, instnum):
   pid = __getVal(inst[5], inst[6], "thread")
   num = __getVal(inst[3], inst[4], "thread")
   toval = __getVal(inst[1], inst[2], "thread")
   out = []
   out.append(toval+" = self.threads[int("+pid+")].children[int("+num+")]")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_sqrt(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   out.append(__getVal(inst[1],inst[2],"thread")+" = math.sqrt("+__getVal(inst[3],inst[4],"thread")+")")
   out = __addTabWidth(out, tabwidth)
   return out
   
op2func = {}
op2func[1.0] = __inst_halt      #halt
op2func[2.0] = __inst_mov       #mov
op2func[3.0] = __inst_terminate #terminate
op2func[4.0] = __inst_jmp       #jmp
op2func[5.0] = __inst_add       #add
op2func[6.0] = __inst_sub       #sub
op2func[7.0] = __inst_mul       #mul
op2func[8.0] = __inst_div       #div
op2func[9.0] = __inst_sin       #sin
op2func[10.0] = __inst_cos      #cos
op2func[15.0] = __inst_mod      #mod
op2func[16.0] = __inst_rnd      #rnd
op2func[19.0] = __inst_call     #call
op2func[20.0] = __inst_return   #return
op2func[21.0] = __inst_cmp      #cmp
op2func[26.0] = __inst_cndjmp   #cndjmp
op2func[27.0] = __inst_cndcall  #cndcall
op2func[28.0] = __inst_push     #push
op2func[29.0] = __inst_pop      #pop
op2func[31.0] = __inst_spawn    #spawn
op2func[35.0] = __inst_gtv      #gtv
op2func[36.0] = __inst_stv      #stv
op2func[38.0] = __inst_atan2    #atan2
op2func[39.0] = __inst_trl      #trl
op2func[40.0] = __inst_cid      #cid
op2func[41.0] = __inst_sqrt     #sqrt

def fcode2python(f):

   instructions = len(f) / 9   #the number of instructions in the program
   startpoints = []
   endpoints = []
   blocks = []
   lineinfo = []
   
   for i in xrange(instructions):
      lineinfo.append([False, False, -1])
   
   for i in xrange(0, len(f), 9):  #loop through the instructions
      if i > 0: #if this is not the first line
         if f[i-9] == 1.0: lineinfo[i/9][0] = True   #last line was a halt
         if f[i-9] == 19.0 or f[i-9] == 27.0: lineinfo[i/9][0] = True  #last line was a call or cndcall
      else:
         lineinfo[0][0] = True   #is the first line
      if f[i] == 4.0 or f[i] == 19.0 or f[i] == 27.0:  #is a jmp/call/cndcall
         lineinfo[int(f[i+2])][0] = True  #the location pointed to is a start point
         lineinfo[i/9][1] = True #this location is an end point
      if f[i] == 26.0 or f[i] == 31.0: #this is a cndjmp or a spawn
         lineinfo[int(f[i+2])][0] = True  #the location pointed to is a start point
      if f[i] == 20.0 or f[i] == 1.0: #line is a return or halt
         lineinfo[i/9][1] = True
   
   #mark the lines before start lines      
   for i in xrange(instructions):
      if i > 0:  #if this is not the first line
         if lineinfo[i][0]:  #if this line is a start line
            lineinfo[i-1][1] = True  #mark the last line as an end line

   #assign blocks to each instruction
   running = False
   blocknum = -1
   for i in xrange(instructions):
      if lineinfo[i][0]:
         running = True
         blocknum += 1
      if running:
         lineinfo[i][2] = blocknum
      if lineinfo[i][1]:
         running = False

   pcode = []
   pcode.append([]) #0 - top and thread class
   pcode[0].append("import math")
   pcode[0].append("import random")
   pcode[0].append("class Thread:")
   pcode[0].append("   def __init__(self, codeloc = 0.0, regsize=64):")
   pcode[0].append("      self.codeloc = codeloc")
   pcode[0].append("      self.registers = []")
   pcode[0].append("      for x in xrange(regsize):")
   pcode[0].append("         self.registers.append(0.0)")
   pcode[0].append("      self.state = []")
   pcode[0].append("      for x in xrange(30):")
   pcode[0].append("         self.state.append(0.0)")
   pcode[0].append("      self.sleep = 0")
   pcode[0].append("      self.children = []")
   pcode[0].append("      self.codestack=[]")
   pcode[0].append("      self.varstack=[]")
   pcode[0].append("      self.threadvars = []")
   pcode[0].append("      for x in xrange(8):")
   pcode[0].append("         self.threadvars.append(0.0)")
   pcode[0].append("      self.threadvars[0] = -1")

   pcode.append([]) #1 - RSVM declaration and init
   pcode[1].append("class RSVM:")
   pcode[1].append("   def __init__(self, r = random.Random(), memsize=64, regsize=32):")
   pcode[1].append("      self.threads = {}")
   pcode[1].append("      self.mem = []")
   pcode[1].append("      self.r = r")
   pcode[1].append("      self.vmdata = []")
   pcode[1].append("      self.vmdata.append(0.0)")
   pcode[1].append("      self.vmdata.append(0.0)")
   pcode[1].append("      self.regsize = regsize")
   pcode[1].append("      for i in xrange(memsize):")
   pcode[1].append("         self.mem.append(0.0)")
   pcode[1].append("      self.nextthread = 0.0")
   pcode[1].append("      self.block2func = {}")
   for x in xrange(blocknum+1):
      pcode[1].append("      self.block2func["+str(x)+"] = self.__f"+str(x))
   pcode[1].append("      self.statename = {}")
   pcode[1].append("      self.statename['x'] = 0")
   pcode[1].append("      self.statename['__x'] = 0")
   pcode[1].append("      self.statename['y'] = 1")
   pcode[1].append("      self.statename['__y'] = 1")
   pcode[1].append("      self.statename['angle'] = 2")
   pcode[1].append("      self.statename['__angle'] = 2")
   pcode[1].append("      self.statename['targetx'] = 3")
   pcode[1].append("      self.statename['__targetx'] = 3")
   pcode[1].append("      self.statename['targety'] = 4")
   pcode[1].append("      self.statename['__targety'] = 4")
   pcode[1].append("      self.statename['returnval'] = 5")
   pcode[1].append("      self.statename['__returnval'] = 5")
   pcode[1].append("      self.statename['condition'] = 6")
   pcode[1].append("      self.statename['__condition'] = 6")
   pcode[1].append("      self.statename['sprite'] = 27")
   pcode[1].append("      self.statename['__sprite'] = 27")
   pcode[1].append("      self.statename['radius'] = 28")
   pcode[1].append("      self.statename['__radius'] = 28")
   pcode[1].append("   def spawnThread(self, initloc, x, y, angle, parent=None):")
   pcode[1].append("      nt = self.nextthread")
   pcode[1].append("      self.threads[nt] = Thread(initloc, self.regsize)")
   pcode[1].append("      self.threads[nt].state[0] = x")
   pcode[1].append("      self.threads[nt].state[1] = y")
   pcode[1].append("      self.threads[nt].state[2] = angle")
   pcode[1].append("      self.threads[nt].threadvars[1] = nt")
   pcode[1].append("      if parent != None:")
   pcode[1].append("         self.threads[nt].threadvars[0] = parent")
   pcode[1].append("         self.threads[parent].children.append(nt)")
   pcode[1].append("      else:")
   pcode[1].append("         self.threads[nt].threadvars[0] = -1")
   pcode[1].append("      self.nextthread += 1")
   pcode[1].append("      return nt")
   pcode[1].append("   def setPlayerPosition(self, x, y):")
   pcode[1].append("      self.vmdata[0] = x")
   pcode[1].append("      self.vmdata[1] = y")
   pcode[1].append("      return")     
   pcode[1].append("   def getThreadParent(self, threadID):")
   pcode[1].append("      return self.threads[threadID].threadvars[0]")
   pcode[1].append("   def getThreadChildren(self, threadID):")
   pcode[1].append("      return self.threads[threadID].children")
   pcode[1].append("   def getState(self, threadID, name):")
   pcode[1].append("      return self.threads[threadID].state[self.statename[name]]")   
   pcode[1].append("   def getThreadIDs(self):")
   pcode[1].append("      return self.threads.keys()")
   pcode[1].append("   def run(self):")
   pcode[1].append("      trun = [self.threads[t] for t in self.threads.keys()]")
   pcode[1].append("      for thread in trun:")
   pcode[1].append("         while thread.sleep <= 0:")
   pcode[1].append("            thread.codeloc = self.block2func[thread.codeloc](thread)")
   pcode[1].append("         thread.sleep -= 1")
   pcode[1].append("      return")

   for x in xrange(blocknum+1):
      pcode.append(["   def __f"+str(x)+"(self, thread):"])
   
   for inst in xrange(instructions): 
      floc = inst*9
      if lineinfo[inst][2] != -1:
         blockindex = lineinfo[inst][2] + 2
         pcode[blockindex] = pcode[blockindex] + op2func[f[floc]](f[floc:floc+9], 2, lineinfo[inst][2], lineinfo, inst)
         #print pcode[blockindex]
   
   #return the next block if it has not been done
   for i in xrange(2,len(pcode)):
      if pcode[i][-1].strip().split()[0] != "return":
         pcode[i].append("      return self.__f"+str((i-2)+1)+"(thread)")
   
   #do optimization here
   
   #do math optimization
   #for xrange(
   
   #for x in lineinfo:
   #   print x
   out = [b for a in pcode for b in a]
   return out
