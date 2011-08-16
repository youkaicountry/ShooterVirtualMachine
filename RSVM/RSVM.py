import math
import random

class Thread:
   def __init__(self, codeloc = 0.0, regsize=64):
      self.codeloc = codeloc
      self.registers = []
      for x in xrange(regsize):
         self.registers.append(0.0)
      self.state = []
      self.state.append(0.0) #0 -  x
      self.state.append(0.0) #1 -  y
      self.state.append(0.0) #2 -  angle
      self.state.append(0.0) #3 -  target x
      self.state.append(0.0) #4 -  target y
      self.state.append(0.0) 
      self.state.append(0.0) 
      self.state.append(0.0) #7 -  velocity x
      self.state.append(0.0) #8 -  velocity y
      self.state.append(0.0) #9 -  acceleration x
      self.state.append(0.0) #10 - acceleration y
      self.state.append(0.0) #11 - mass
      self.state.append(0.0)
      self.state.append(0.0)  
      self.state.append(0.0) 
      self.state.append(0.0) 
      self.state.append(0.0) #16 - oldx
      self.state.append(0.0) #17 - oldy
      self.state.append(0.0) #18 - thrustvel
      self.state.append(0.0) #19 - thrustacc
      self.state.append(0.0) #20 - userad
      self.state.append(0.0) #21 - rotvel
      self.state.append(0.0) #22 - rotacc
      self.state.append(0.0) #23 - towardvel
      self.state.append(0.0) #24 - towardacc
      self.state.append(0.0) #25 - turnvel
      self.state.append(0.0) #26 - turnacc
      self.sleep = 0
      self.children = []
      self.codestack=[]
      self.varstack=[]
      self.threadvars = []
      self.threadvars.append(-1)    #0 - parentid
      self.threadvars.append(0.0)   #1 - selfid
      self.threadvars.append(0.0)   #2 - condition
      self.threadvars.append(0.0)   #3 - returnval
      self.threadvars.append(0.0)   #4 - spawnid
      self.threadvars.append(0.0)   #5 - numchildren
      self.threadvars.append(0.0)   #6 - dead
      
   def __str__(self):
      return "REGISTERS: " + str(self.registers) + "\n" + "STATE: " + str(self.state)
      
class RSVM:
   def __init__(self, fcode, r = random.Random(), memsize=64, regsize=32):
      self.threads = {}
      self.mem = []
      self.r = r
      self.vmdata = []
      self.vmdata.append(0.0) #0 - playerx
      self.vmdata.append(0.0) #1 - playery
      self.regsize = regsize
      for i in xrange(memsize):
         self.mem.append(0.0)
      self.code = fcode
      self.nextthread = 0.0
      self.op2func = {}
      self.op2func[1.0] = self.__inst_halt      #halt
      self.op2func[2.0] = self.__inst_mov       #mov
      self.op2func[3.0] = self.__inst_terminate #terminate
      self.op2func[4.0] = self.__inst_jmp       #jmp
      self.op2func[5.0] = self.__inst_add       #add
      self.op2func[6.0] = self.__inst_sub       #sub
      self.op2func[7.0] = self.__inst_mul       #mul
      self.op2func[8.0] = self.__inst_div       #div
      self.op2func[9.0] = self.__inst_sin       #sin
      self.op2func[10.0] = self.__inst_cos      #cos
      self.op2func[15.0] = self.__inst_mod      #mod
      self.op2func[16.0] = self.__inst_rnd      #rnd
      self.op2func[19.0] = self.__inst_call     #call
      self.op2func[20.0] = self.__inst_return   #return
      self.op2func[21.0] = self.__inst_cmp      #cmp
      self.op2func[26.0] = self.__inst_cndjmp   #cndjmp
      self.op2func[27.0] = self.__inst_cndcall  #cndcall
      self.op2func[28.0] = self.__inst_push     #push
      self.op2func[29.0] = self.__inst_pop      #pop
      self.op2func[31.0] = self.__inst_spawn    #spawn
      self.op2func[35.0] = self.__inst_gtv      #gtv
      self.op2func[36.0] = self.__inst_stv      #stv
      self.op2func[38.0] = self.__inst_atan2    #atan2
      self.op2func[39.0] = self.__inst_trl      #trl
      self.op2func[40.0] = self.__inst_cid      #cid
      self.op2func[41.0] = self.__inst_sqrt     #sqrt
      
      self.statename = {}
      self.statename["x"] = 0
      self.statename["__x"] = 0
      self.statename["y"] = 1
      self.statename["__y"] = 1
      self.statename["angle"] = 2
      self.statename["__angle"] = 2
      self.statename["targetx"] = 3
      self.statename["__targetx"] = 3
      self.statename["targety"] = 4
      self.statename["__targety"] = 4
      self.statename["returnval"] = 5
      self.statename["__returnval"] = 5
      self.statename["condition"] = 6
      self.statename["__condition"] = 6
      
      
   def spawnThread(self, initloc, x, y, angle, parent=None):
      nt = self.nextthread
      self.threads[nt] = Thread(initloc, self.regsize)
      self.threads[nt].state[0] = x
      self.threads[nt].state[1] = y
      self.threads[nt].state[2] = angle
      self.threads[nt].threadvars[1] = nt
      if parent != None:
         self.threads[nt].threadvars[0] = parent
         self.threads[parent].children.append(nt)
      else:
         self.threads[nt].threadvars[0] = -1
      self.nextthread += 1
      return nt
      
   def setPlayerPosition(self, x, y):
      self.vmdata[0] = x
      self.vmdata[1] = y
      return
      
   def getThreadParent(self, threadID):
      return self.threads[threadID].threadvars[0]
      
   def getThreadChildren(self, threadID):
      return self.threads[threadID].children
      
   def getState(self, threadID, name):
      return self.threads[threadID].state[self.statename[name]]
   
   def getThreadIDs(self):
      return self.threads.keys()
   
   def __str__(self):
      st = ""
      for x in self.threads.keys():
         st = st + "Thread#"+str(int(x)) + ": " + str(self.threads[x])
      return st
   
   #given the 2 floats involved in a val code, returns the physical value
   def __getVal(self, thread, val0, val1):
      if val0 == 0.0:
         return thread.registers[int(val1)]
      if val0 == 1.0:
         return val1
      if val0 == 2.0:
         return thread.state[int(val1)]
      if val0 == 3.0:
         return self.mem[int(val1)]
      if val0 == 4.0: 
         return self.vmdata[int(val1)]
      if val0 == 7.0:
         if val1 == 5.0:
            return len(thread.children)
         return thread.threadvars[int(val1)]
      return 0.0
   
   #sets the location at the val code to the given number
   def __setVal(self, thread, val0, val1, number):
      if val0 == 0:
         thread.registers[int(val1)] = number
      elif val0 == 2:
         #if val1 == 0.0 and thread.state[12] == 1.0:   #move children
         #   for x in thread.children:
         #      self.__setVal(self.threads[x], 2.0, 0.0, self.threads[x].state[0]+(number-thread.state[0]))
         #elif val1 == 1.0 and thread.state[12] == 1.0: #move children
         #   for x in thread.children:
         #      self.__setVal(self.threads[x], 2.0, 1.0, self.threads[x].state[1]+(number-thread.state[1]))
         thread.state[int(val1)] = number
         if val1 == 2.0: #mod if an angle change
            thread.state[2] = thread.state[2] % 6.283185
      elif val0 == 3:
         self.mem[int(val1)] = number
      elif val0 == 4:
         self.vmdata[int(val1)] = number
      elif val0 == 7:
         thread.threadvars[int(val1)] = number
            
   
   #runs all the threads
   def run(self):
      trun = [self.threads[t] for t in self.threads.keys()]
      for thread in trun:
         while thread.sleep <= 0:
            cl = int(thread.codeloc * 9)
            thread.codeloc += self.op2func[self.code[cl]](thread, self.code[cl+1], self.code[cl+2], self.code[cl+3], self.code[cl+4], self.code[cl+5], self.code[cl+6], self.code[cl+7], self.code[cl+8])
         thread.sleep -= 1
      return
      
   """def __inst_decl(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      num = self.__getVal(thread, v10, v11)
      thread.registers = []
      for x in xrange(num):
         thread.registers.append(0.0)
      return 1"""
      
   def __inst_halt(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      v = self.__getVal(thread, v10, v11)
      thread.sleep = v
      return 1
      
   def __inst_mov(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      v = self.__getVal(thread, v20, v21)
      self.__setVal(thread, v10, v11, v)
      return 1
      
   def __inst_jmp(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      loc = self.__getVal(thread, v10, v11)
      return loc-thread.codeloc
   
   def __inst_add(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      b = self.__getVal(thread, v30, v31)
      self.__setVal(thread, v10, v11, a+b)
      return 1
      
   def __inst_sub(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      b = self.__getVal(thread, v30, v31)
      self.__setVal(thread, v10, v11, a-b)
      return 1
      
   def __inst_mul(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      b = self.__getVal(thread, v30, v31)
      self.__setVal(thread, v10, v11, a*b)
      return 1
      
   def __inst_div(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      b = self.__getVal(thread, v30, v31)
      self.__setVal(thread, v10, v11, a/b)
      return 1
      
   def __inst_rnd(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      self.__setVal(thread, v10, v11, self.r.random())
      return 1
   
   #make sure future implementations do the stupid correction   
   def __inst_atan2(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      y = self.__getVal(thread, v20, v21)
      x = self.__getVal(thread, v30, v31)
      if x == 0 and y == 0: self.__setVal(thread, v10, v11, 0)
      a = math.atan2(y, x)
      if a < 0:
         a += 6.28318531
      self.__setVal(thread, v10, v11, a)
      return 1
   
   #make sure negatives wrap properly in future implementations   
   def __inst_mod(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      b = self.__getVal(thread, v30, v31)
      self.__setVal(thread, v10, v11, a%b)
      return 1
      
   def __inst_sin(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      self.__setVal(thread, v10, v11, math.sin(a))
      return 1
      
   def __inst_cos(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      self.__setVal(thread, v10, v11, math.cos(a))
      return 1
   
   def __inst_sqrt(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      self.__setVal(thread, v10, v11, math.sqrt(a))
      return 1
   
   def __inst_terminate(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      tid = thread.threadvars[1]
      if thread.threadvars[0] >= 0:
         self.threads[thread.threadvars[0]].children.remove(tid)
      for x in thread.children:
         self.threads[x].threadvars[0] = -1
      del self.threads[tid]
      thread.threadvars[6] = 1.0
      thread.sleep = 1
      return 1
      
   def __inst_push(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      v = self.__getVal(thread, v10, v11)
      #print "PUSH: " + str(self.threads[threadnum].codeloc)
      thread.varstack.append(v)
      return 1
      
   def __inst_pop(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      #print "POP: " + str(self.threads[threadnum].codeloc)
      self.__setVal(thread, v10, v11, thread.varstack.pop())
      return 1
      
   def __inst_call(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      thread.codestack.append(thread.codeloc + 1)
      loc = self.__getVal(thread, v10, v11)
      return loc-thread.codeloc
      
   def __inst_return(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      thread.threadvars[3] = self.__getVal(thread, v10, v11)
      loc = thread.codestack.pop()
      return loc-thread.codeloc
      
   def __inst_cmp(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      a = self.__getVal(thread, v20, v21)
      b = self.__getVal(thread, v40, v41)
      if v31 == 0.0: val = a == b
      elif v31 == 1.0: val = a < b
      elif v31 == 2.0: val = a > b
      elif v31 == 3.0: val = a >= b
      elif v31 == 4.0: val = a <= b
      elif v31 == 5.0: val = a != b 
      self.__setVal(thread, v10, v11, val)
      return 1      
      
   def __inst_cndjmp(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      if thread.threadvars[2] == 1.0:
         loc = self.__getVal(thread, v10, v11)
         return loc-thread.codeloc
      else:
         return 1
   
   def __inst_cndcall(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      if thread.threadvars[2] == 1.0:
         thread.codestack.append(thread.codeloc + 1)
         loc = self.__getVal(thread, v10, v11)
         return loc-thread.codeloc
      else:
         return 1  
         
   def __inst_gtv(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      tid = self.__getVal(thread, v30, v31)
      val = self.__getVal(self.threads[tid], v20, v21)
      self.__setVal(thread, v10, v11, val)
      return 1
      
   def __inst_stv(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      tid = self.__getVal(thread, v30, v31)
      val = self.__getVal(thread, v20, v21)
      self.__setVal(self.threads[tid], v10, v11, val)
      return 1
      
   def __inst_spawn(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      #x = thread.state[3] #targety
      #y = thread.state[4] #targetx
      #angle = thread.state[2] #angle
      pid = thread.threadvars[1] #selfid
      l = self.__getVal(thread, v10, v11)
      #num = self.__getVal(thread, v20, v21)
      t = self.spawnThread(l, 0, 0, 0, pid)
      self.__setVal(thread, 7.0, 4.0, t)
      return 1
      
   def __inst_trl(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      tgtpid = self.__getVal(thread, v10, v11)
      tgtcid = self.__getVal(thread, v20, v21)
      oldpid = self.__getVal(thread, v30, v31)
      oldcid = self.__getVal(thread, v40, v41)
      #verify that the given pid-cid exists
      
   def __inst_cid(self, thread, v10, v11, v20, v21, v30, v31, v40, v41):
      num = self.__getVal(thread, v20, v21)
      pid = self.__getVal(thread, v30, v31)
      self.__setVal(thread, v10, v11, self.threads[int(pid)].children[int(num)])
      return 1
   
