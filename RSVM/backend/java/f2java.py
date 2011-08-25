import re

code2sign = {}
code2sign[0.0] = "=="
code2sign[1.0] = "<"
code2sign[2.0] = ">"
code2sign[3.0] = ">="
code2sign[4.0] = "<="
code2sign[5.0] = "!="

#OPTIONS
debug = True
optimize = True
traceInstructions = set([50.0, 51.0, 52.0, 53.0])
fulltrace = False

#compile the regular expressions
re_reg = re.compile(r"sthread[.]registers[\[]([0-9]+)[\]]")
re_state = re.compile(r"sthread[.]state[\[]([0-9]+)[\]]")
re_mem = re.compile(r"this[.]mem[\[]([0-9]+)[\]]")
re_vm = re.compile(r"this[.]vmdata[\[]([0-9]+)[\]]")
re_tv = re.compile(r"sthread[.]threadvars[\[]([0-9]+)[\]]")
re_ret = re.compile(r"return")

def __getVal(v1, v2, owner):
   if v1 == 0.0:
      return owner+".registers["+str(int(v2))+"]"
   if v1 == 1.0:
      return str(v2)+"f"
   if v1 == 2.0:
      return owner+".state["+str(int(v2))+"]"
   if v1 == 3.0:
      return "this.mem["+str(int(v2))+"]"
   if v1 == 4.0:
      return "this.vmdata["+str(int(v2))+"]"
   if v1 == 7.0:
      if v2 == 5.0:
         return owner+".children.size()"
      return owner+".threadvars["+str(int(v2))+"]"
   return "0"

def __getValBase(v1, v2, owner):
   if v1 == 0.0:
      return (owner+".registers[", str(int(v2)))
   if v1 == 2.0:
      return (owner+".state[", str(int(v2)))
   if v1 == 3.0:
      return ("this.mem[", str(int(v2)))
   if v1 == 4.0:
      return ("this.vmdata[", str(int(v2)))
   if v1 == 7.0:
      #if v2 == 5.0:
      #   return owner+".children.size()"
      return (owner+".threadvars[", str(int(v2)))
   return ("e", "e")

def __addTabWidth(lines, tabwidth):
   return [((" "*4)*tabwidth) + l for l in lines]
   #print lines
   
def __addSemi(lines):
    return [l + ";" for l in lines]

def __inst_halt(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//halt")
   out.append("sthread.sleep = (int)("+__getVal(inst[1], inst[2], "sthread")+")")
   out.append("return "+str(blocknum+1))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_mov(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//mov")
   out.append(__getVal(inst[1], inst[2], "sthread")+" = "+__getVal(inst[3], inst[4], "sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

#make this an actual function in the header that is simply called
def __inst_terminate(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//terminate")
   out.append("this.ti1 = (int)(sthread.threadvars[1]);")
   out.append("if (sthread.threadvars[0] >= 0.0f)")
   out.append("{")
   out.append("    this.ti2 = this.threads.get((int)(sthread.threadvars[0])).children.indexOf((int)ti1);")
   out.append("    this.threads.get((int)(sthread.threadvars[0])).children.remove(ti2);")
   out.append("}")
   out.append("for (int i = 0; i < sthread.children.size(); i++)")
   out.append("{")
   out.append("    this.ti2 = sthread.children.get(i).intValue();")
   out.append("    this.threads.get(this.ti2).threadvars[0] = -1;")
   out.append("}")
   out.append("this.threads.remove(this.ti1);")
   out.append("sthread.threadvars[6] = 1.0f;")
   out.append("sthread.sleep = 1;")
   out.append("this.ready_threads.push(sthread);")
   out.append("return 0;")
   out = __addTabWidth(out, tabwidth)
   return out

def __inst_jmp(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//jmp")
   out.append("return this.f"+str(lineinfo[int(inst[2])][2])+"(sthread)")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_add(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//add")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = "+__getVal(inst[3],inst[4],"sthread")+" + "+__getVal(inst[5],inst[6],"sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_sub(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//sub")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = "+__getVal(inst[3],inst[4],"sthread")+" - "+__getVal(inst[5],inst[6],"sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_mul(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//mul")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = "+__getVal(inst[3],inst[4],"sthread")+" * "+__getVal(inst[5],inst[6],"sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_div(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//div")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = "+__getVal(inst[3],inst[4],"sthread")+" / "+__getVal(inst[5],inst[6],"sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_rnd(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//rnd")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = this.r.nextFloat()")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_sin(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//sin")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = (float)(Math.sin("+__getVal(inst[3],inst[4],"sthread")+"))")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_cos(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//cos")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = (float)(Math.cos("+__getVal(inst[3],inst[4],"sthread")+"))")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_mod(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//mod")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = "+__getVal(inst[3],inst[4],"sthread")+" % "+__getVal(inst[5],inst[6],"sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_call(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//call")
   out.append("sthread.codetop++")
   out.append("sthread.codestack[sthread.codetop] = "+str(blocknum+1))
   #out.append("sthread.codestack.add("+str(blocknum+1)+")")
   out.append("return f"+str(lineinfo[int(inst[2])][2])+"(sthread)")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_return(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//ret")
   out.append("this.ti1 = sthread.codestack[sthread.codetop]")
   out.append("sthread.threadvars[3] = "+__getVal(inst[1],inst[2],"sthread"))
   out.append("sthread.codetop--")
   out.append("return this.ti1")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_cmp(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//cmp")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = ("+__getVal(inst[3],inst[4],"sthread")+" "+code2sign[inst[6]]+" "+__getVal(inst[7],inst[8],"sthread")+") ? 1f : 0f")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_cndjmp(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//cndjmp")
   out.append("if (sthread.threadvars[2] == 1)")
   out.append("{")
   out.append("   return this.f"+str(lineinfo[int(inst[2])][2])+"(sthread);")
   out.append("}")
   out = __addTabWidth(out, tabwidth)
   return out

def __inst_cndcall(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//cndcall")
   out.append("if (thread.threadvars[2] == 1)")
   out.append("{")
   out.append("   sthread.codetop++;")
   out.append("   sthread.codestack[sthread.codetop] = "+str(blocknum+1)+";")
   out.append("   return this.f"+str(lineinfo[int(inst[2])][2])+"(sthread);")
   out.append("}")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_push(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//push")
   out.append("sthread.threadvars[9]+=1.0f")
   out.append("sthread.varstack[(int)(sthread.threadvars[9])] = "+__getVal(inst[1],inst[2],"sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_pop(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//pop")
   #out.append("this.ti1 = sthread.varstack.size()-1")
   #out.append("this.tf1 = sthread.varstack.get(this.ti1)")
   #out.append("sthread.varstack.remove(this.ti1)")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = sthread.varstack[(int)(sthread.threadvars[9])]")
   out.append("sthread.threadvars[9]-=1.0f")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out
   
def __inst_spawn(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//spawn")
   out.append("this.ti1 = (int)(sthread.threadvars[1])")
   out.append("this.ti2 = this.spawnThread("+str(lineinfo[int(inst[2])][2])+", 0, 0, 0, this.ti1)")
   out.append("sthread.threadvars[4] = (float)(this.ti2)")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out
     
def __inst_gtv(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//gtv")
   owner = "this.threads.get((int)("+__getVal(inst[5], inst[6], "sthread")+"))"
   out.append(__getVal(inst[1],inst[2], "sthread")+" = "+__getVal(inst[3], inst[4], owner))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_stv(inst, tabwidth, blocknum, lineinfo, instnum):
   out = []
   if debug: out.append("//stv")
   owner = "this.threads.get((int)("+__getVal(inst[5], inst[6], "sthread")+"))"
   out.append(__getVal(inst[1],inst[2], owner)+" = "+__getVal(inst[3], inst[4], "sthread"))
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out
   
def __inst_atan2(inst, tabwidth, blocknum, lineinfo, instnum):   
   out= []
   if debug: out.append("//atan2")
   out.append("this.tf1 = (float) Math.atan2("+__getVal(inst[3],inst[4],"sthread")+", "+__getVal(inst[5], inst[6], "sthread")+");")
   out.append("if (this.tf1 < 0.0f)")
   out.append("{")
   out.append("   this.tf1 += 6.28318531f;")
   out.append("}")
   out.append(__getVal(inst[1], inst[2], "sthread")+" = this.tf1;")
   out = __addTabWidth(out, tabwidth)
   return out
   
def __inst_trl(inst, tabwidth, blocknum, lineinfo, instnum):
   return ["line1", "line2..."]
   
def __inst_cid(inst, tabwidth, blocknum, lineinfo, instnum):
   pid = __getVal(inst[5], inst[6], "sthread")
   num = __getVal(inst[3], inst[4], "sthread")
   toval = __getVal(inst[1], inst[2], "sthread")
   out = []
   if debug: out.append("//cid")
   out.append(toval+" = this.threads.get((int)("+pid+")).children.get((int)("+num+"))")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out
   
def __inst_sqrt(inst, tabwidth, blocknum, lineinfo, instnum):
   out= []
   if debug: out.append("//sqrt")
   out.append(__getVal(inst[1],inst[2],"sthread")+" = (float)(Math.sqrt("+__getVal(inst[3],inst[4],"sthread")+"))")
   out = __addTabWidth(out, tabwidth)
   out = __addSemi(out)
   return out

def __inst_peek(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//peek")
    out.append(__getVal(inst[1],inst[2],"sthread")+" = sthread.varstack[(int)(sthread.threadvars[9])]")
    out = __addTabWidth(out, tabwidth)
    out = __addSemi(out)
    return out

def __inst_peekat(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//peekat")
    out.append(__getVal(inst[1],inst[2],"sthread")+" = sthread.varstack[(int)(sthread.threadvars[9]-"+__getVal(inst[3],inst[4],"sthread")+")]")
    out = __addTabWidth(out, tabwidth)
    out = __addSemi(out)
    return out

def __inst_pokeat(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//pokeat")
    out.append("sthread.varstack[(int)(sthread.threadvars[9]-"+__getVal(inst[3],inst[4],"sthread")+")] = "+__getVal(inst[1],inst[2],"sthread"))
    out = __addTabWidth(out, tabwidth)
    out = __addSemi(out)
    return out

def __inst_sat(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//sat")
    bv = __getValBase(inst[1], inst[2],"sthread")
    out.append(bv[0] + bv[1] + __getVal(inst[3], inst[4],"sthread") + "] = " + __getVal(inst[5], inst[6],"sthread"))
    out = __addTabWidth(out, tabwidth)
    out = __addSemi(out)
    return out

def __inst_gat(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//gat")
    bv = __getValBase(inst[3], inst[4],"sthread")
    out.append(__getVal(inst[1], inst[2],"sthread") + " = " + bv[0] + bv[1] + " + " + __getVal(inst[5], inst[6],"sthread"))
    out = __addTabWidth(out, tabwidth)
    out = __addSemi(out)
    return out

def __inst_gof(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//gof")
    bv = __getValBase(inst[3], inst[4],"sthread")
    out.append(__getVal(inst[1], inst[2],"sthread") + " = " + bv[1] + " + " + __getVal(inst[5], inst[6],"sthread"))
    out = __addTabWidth(out, tabwidth)
    out = __addSemi(out)
    return out

def __inst_recvwait(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//recvwait")
    out.append("if (!this.recvwait(sthread, "+__getVal(inst[1],inst[2],"sthread")+"))")
    out.append("   {")
    out.append("      return "+str(blocknum)+";")
    out.append("   }")
    out.append(__getVal(inst[3],inst[4],"sthread")+" = this.tf1;")
    out.append(__getVal(inst[5],inst[6],"sthread")+" = this.tf2;")
    out.append(__getVal(inst[7],inst[8],"sthread")+" = this.tf3;")
    out = __addTabWidth(out, tabwidth)
    return out

def __inst_recv(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//recv")
    out.append("this.recv(sthread, "+__getVal(inst[1],inst[2],"sthread")+");")
    out.append(__getVal(inst[3],inst[4],"sthread")+" = this.tf1;")
    out.append(__getVal(inst[5],inst[6],"sthread")+" = this.tf2;")
    out.append(__getVal(inst[7],inst[8],"sthread")+" = this.tf3;")
    out = __addTabWidth(out, tabwidth)
    return out

def __inst_send(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//send")
    out.append("this.sendMessage("+__getVal(inst[1],inst[2],"sthread")
                             +", "+__getVal(inst[3],inst[4],"sthread")
                             +", sthread"
                             +", "+__getVal(inst[5],inst[6],"sthread")+");")
    out = __addTabWidth(out, tabwidth)
    return out

def __inst_acceptmsg(inst, tabwidth, blocknum, lineinfo, instnum):
    out = []
    if debug: out.append("//acceptmsg")
    out.append("this.declareMessage(sthread, "+__getVal(inst[1],inst[2],"sthread")+");")
    out = __addTabWidth(out, tabwidth)
    return out

__traceflag = False

def __inst_trace(inst, tabwidth, blocknum, lineinfo, instnum):
    global __traceflag
    if inst[2] == 0.0:
       __traceflag = False
    elif inst[2] == 1.0:
       __traceflag = True
    else:
       raise RuntimeError("Unknown TRACE instruction")
    return []

def __createPreTraceCode(inst, tabwidth, blocknum, lineinfo, instnum):
   if not __traceflag and not fulltrace:
      return []
   out = []
   header = 'showFloat(sthread.threadvars[1])+" : '+op2name[inst[0]]+'"'
   toprint = ''
   for i,c in enumerate(op2args[inst[0]]):
      if c != 'i':
         continue
      toprint += '+" "+showFloat('+__getVal(inst[2*i+1], inst[2*i+2],"sthread")+')'
   if toprint != '':
      if debug: out.append("//pretrace")
      out.append("System.out.println("+header+toprint+");")
   out = __addTabWidth(out, tabwidth)
   return out

def __createPostTraceCode(inst, tabwidth, blocknum, lineinfo, instnum):
   if not __traceflag and not fulltrace:
      return []
   out = []
   header = '((int) sthread.threadvars[1])+" : '+op2name[inst[0]]+' returned"'
   toprint = ''
   for i,c in enumerate(op2args[inst[0]]):
      if c != 'o':
         continue
      toprint += '+" "+showFloat('+__getVal(inst[2*i+1], inst[2*i+2],"sthread")+')'
   if toprint != '':
      if debug: out.append("//posttrace")
      out.append("System.out.println("+header+toprint+");")
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
op2func[50.0] = __inst_recvwait #recvwait
op2func[51.0] = __inst_recv     #recv
op2func[52.0] = __inst_send     #send
op2func[53.0] = __inst_acceptmsg#accept
op2func[54.0] = __inst_trace    #trace
op2func[60.0] = __inst_peek
op2func[61.0] = __inst_peekat
op2func[62.0] = __inst_pokeat
op2func[70.0] = __inst_sat
op2func[71.0] = __inst_gat
op2func[72.0] = __inst_gof

op2args = {50.0 : "iooo",
           51.0 : "iooo",
           52.0 : "iii ",
           53.0 : "i   "}

op2name = {50.0 : "recvwait",
           51.0 : "recv",
           52.0 : "send",
           53.0 : "acceptmsg"}

def fcode2java(f):

   instructions = len(f) / 9   #the number of instructions in the program
   startpoints = []
   endpoints = []
   blocks = []
   lineinfo = []

   for i in range(int(instructions)):
      lineinfo.append([False, False, -1])

   for i in range(0, len(f), 9):  #loop through the instructions
      if i > 0: #if this is not the first line
         if f[i-9] in [1.0, 19.0, 27.0, 3.0]:
            lineinfo[int(i/9)][0] = True  #last line was: halt call cndcall terminate
      else:
         lineinfo[0][0] = True   #is the first line
      if f[i] == 4.0 or f[i] == 19.0 or f[i] == 27.0:  #is a jmp/call/cndcall
         lineinfo[int(f[i+2])][0] = True  #the location pointed to is a start point
         lineinfo[int(i/9)][1] = True #this location is an end point
      if f[i] == 26.0 or f[i] == 31.0: #this is a cndjmp or a spawn
         lineinfo[int(f[i+2])][0] = True  #the location pointed to is a start point
      if f[i] == 20.0 or f[i] == 1.0: #line is a return or halt
         lineinfo[int(i/9)][1] = True
      if f[i] == 50.0:   #line is a recvwait line
         lineinfo[int(i/9)][0] = True
      #n.b., the line OF a recvwait is the start of a block because
      #   a recvwait is essentially a conditional jump to itself

   #mark the lines before start lines
   for i in range(int(instructions)):
      if i > 0:  #if this is not the first line
         if lineinfo[i][0]:  #if this line is a start line
            lineinfo[i-1][1] = True  #mark the last line as an end line

   #assign blocks to each instruction
   running = False
   blocknum = -1
   for i in range(int(instructions)):
      if lineinfo[i][0]:
         running = True
         blocknum += 1
      if running:
         lineinfo[i][2] = blocknum
      if lineinfo[i][1]:
         running = False

   pcode = []
   pcode.append([]) #0 - top
   pcode[0].append("import java.util.ArrayList;")
   pcode[0].append("import java.util.Hashtable;")
   pcode[0].append("import java.util.Iterator;")
   pcode[0].append("import java.util.Map;")
   pcode[0].append("import java.util.Random;")
   pcode[0].append("import java.util.Set;")
   pcode[0].append("import java.util.Stack;")
   pcode[0].append("import java.util.TreeMap;")
   pcode[0].append("")

   pcode.append([]) #1 - RSVM declaration and init
   pcode[1].append("@SuppressWarnings(\"all\")")
   pcode[1].append("class RSVM implements ShooterVirtualMachine")
   pcode[1].append("   {")
   pcode[1].append("    public Hashtable<Integer, ShooterThread> threads;")
   pcode[1].append("    public Hashtable<String, Integer> statename;")
   pcode[1].append("    public float[] mem;")
   pcode[1].append("    public Random r = null;")
   pcode[1].append("    public float[] vmdata = new float[2];")
   pcode[1].append("    public int regsize;")
   pcode[1].append("    public int stacksize;")
   pcode[1].append("    public int nextthread;")
   pcode[1].append("    private float tf1, tf2, tf3;")
   pcode[1].append("    private int ti1, ti2;")
   pcode[1].append("    private Stack<ShooterThread> ready_threads;")
   pcode[1].append("    ")
   pcode[1].append("    //try 64, 32, 32, 32, null")
   pcode[1].append("    //if r is null, a new one is made.")
   pcode[1].append("    public RSVM(int memsize, int regsize, int stacksize, int initthreads, Random r)")
   pcode[1].append("    {")
   pcode[1].append("        if (r == null) {this.r = new Random();}")
   pcode[1].append("        this.ready_threads = new Stack<ShooterThread>();")
   pcode[1].append("        for (int i = 0; i < initthreads; i++)")
   pcode[1].append("        {")
   pcode[1].append("            this.ready_threads.push(new ShooterThread(0, regsize, stacksize));")
   pcode[1].append("        }")
   pcode[1].append("        this.threads = new Hashtable<Integer, ShooterThread>();")
   pcode[1].append("        this.mem = new float[memsize];")
   pcode[1].append("        this.regsize = regsize;")
   pcode[1].append("        this.stacksize = stacksize;")
   pcode[1].append("        this.nextthread = 0;")
   pcode[1].append("        this.mem[0] = 0;")
   pcode[1].append("        this.mem[1] = 0;")
   pcode[1].append("        this.statename = new Hashtable<String, Integer>();")
   pcode[1].append('        statename.put("x", new Integer(0));')
   pcode[1].append('        statename.put("__x", new Integer(0));')
   pcode[1].append('        statename.put("y", new Integer(1));')
   pcode[1].append('        statename.put("__y", new Integer(1));')
   pcode[1].append('        statename.put("angle", new Integer(2));')
   pcode[1].append('        statename.put("__angle", new Integer(2));')
   pcode[1].append('        statename.put("targetx", new Integer(3));')
   pcode[1].append('        statename.put("__targetx", new Integer(3));')
   pcode[1].append('        statename.put("targety", new Integer(4));')
   pcode[1].append('        statename.put("__targety", new Integer(4));')
   pcode[1].append('        statename.put("returnval", new Integer(5));')
   pcode[1].append('        statename.put("__returnval", new Integer(5));')
   pcode[1].append('        statename.put("condition", new Integer(6));')
   pcode[1].append('        statename.put("__condition", new Integer(6));')
   pcode[1].append('        statename.put("sprite", new Integer(27));')
   pcode[1].append('        statename.put("__sprite", new Integer(27));')
   pcode[1].append('        statename.put("radius", new Integer(28));')
   pcode[1].append('        statename.put("__radius", new Integer(28));')
   pcode[1].append("        return;")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    private int block2FuncCall(ShooterThread th)")
   pcode[1].append("    {")
   pcode[1].append("        int retval = 0;")
   pcode[1].append("        switch (th.codeloc)")
   pcode[1].append("        {")
   for x in range(blocknum+1):
      pcode[1].append("           case "+str(x)+": retval = this.f"+str(x)+"(th); break;")
   pcode[1].append("        }")
   pcode[1].append("        return retval;")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    public int spawnThread(int initloc, float x, float y, float angle, int parent)")
   pcode[1].append("    {")
   pcode[1].append("        int nt = this.nextthread;")

   pcode[1].append("        ShooterThread st;")
   pcode[1].append("        if (this.ready_threads.empty())")
   pcode[1].append("        {")
   pcode[1].append("            st = new ShooterThread(initloc, this.regsize, this.stacksize);")

   pcode[1].append("        }")
   pcode[1].append("        else")
   pcode[1].append("        {")
   pcode[1].append("            st = (ShooterThread)(this.ready_threads.pop());")
   pcode[1].append("            st.clear(initloc);")
   pcode[1].append("        }")
   pcode[1].append("        this.threads.put(nt, st);")

   pcode[1].append("        st.state[0] = x;")
   pcode[1].append("        st.state[1] = y;")
   pcode[1].append("        st.state[2] = angle;")
   pcode[1].append("        st.threadvars[1] = nt;")
   pcode[1].append("        if (parent >= 0)")
   pcode[1].append("        {")
   pcode[1].append("            st.threadvars[0] = parent;")
   pcode[1].append("            this.threads.get(parent).children.add(this.threads.get(parent).children.size(), nt);")
   pcode[1].append("        }")
   pcode[1].append("        else")
   pcode[1].append("        {")
   pcode[1].append("            st.threadvars[0] = -1;")
   pcode[1].append("        }")
   pcode[1].append("        this.nextthread++;")
   pcode[1].append("        this.scheduled_threads.write(nt);")
   pcode[1].append("        return nt;")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    public void setPlayerPosition(float x, float y)")
   pcode[1].append("    {")
   pcode[1].append("        this.vmdata[0] = x;")
   pcode[1].append("        this.vmdata[1] = y;")
   pcode[1].append("        return;")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    public int getThreadParent(int threadid)")
   pcode[1].append("    {")
   pcode[1].append("        return (int)(this.threads.get(threadid).threadvars[0]);")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    public ArrayList<Integer> getThreadChildren(int threadid)")
   pcode[1].append("    {")
   pcode[1].append("        return this.threads.get(threadid).children;")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    public float getState(int threadid, String state)")
   pcode[1].append("    {")
   pcode[1].append("        return this.threads.get(threadid).state[this.statename.get(state)];")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    public Iterator<Integer> getThreadIDs()")
   pcode[1].append("    {")
   pcode[1].append("        //int[] retval = new int[this.threads.size()];")
   pcode[1].append("        Set<Integer> s = this.threads.keySet();")
   pcode[1].append("        return s.iterator();")
   pcode[1].append("    }")
   pcode[1].append("    ")
   pcode[1].append("    private IntQueue scheduled_threads = new IntQueue();")
   pcode[1].append("    ")
   pcode[1].append("    public void run()")
   pcode[1].append("    {")
   pcode[1].append("        Iterator<Integer> it = this.getThreadIDs();")
   pcode[1].append("        while(it.hasNext())")
   pcode[1].append("        {")
   pcode[1].append("           int tid = it.next();")
   pcode[1].append("        	 ShooterThread th = threads.get(tid);")
   pcode[1].append("        	 if (!th.msg_isWaitingForMessage)")
   pcode[1].append("        	    scheduled_threads.write(tid);")
   pcode[1].append("        }")
   pcode[1].append("        while(true)")
   pcode[1].append("        {")
   pcode[1].append("            int tid = scheduled_threads.read();")
   pcode[1].append("            if (tid == IntQueue.NO_SUCH_ELEMENT)")
   pcode[1].append("               break;")
   pcode[1].append("            ShooterThread ct = this.threads.get(tid);")
   pcode[1].append("            while (ct.sleep <= 0)")
   pcode[1].append("            {")
   pcode[1].append("                if (ct.msg_isWaitingForMessage)")
   pcode[1].append("                   break;")
   pcode[1].append("                ct.codeloc = this.block2FuncCall(ct);")
   pcode[1].append("            }")
   pcode[1].append("            ct.sleep -= 1;")
   pcode[1].append("        }")
   pcode[1].append("        return;")
   pcode[1].append("    }")
   pcode[1].append("   ")
   pcode[1].append("   private boolean recvwait(ShooterThread th, float msgtype)")
   pcode[1].append("   {")
   pcode[1].append("      if (!getMessage(th, msgtype))")
   pcode[1].append("      {")
   pcode[1].append("         th.msg_isWaitingForMessage = true;")
   pcode[1].append("         return false;")
   pcode[1].append("      }")
   pcode[1].append("      th.msg_isWaitingForMessage = false;")
   pcode[1].append("      return true;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   /**")
   pcode[1].append("    * Send a message to the given thread from the given sending thread.")
   pcode[1].append("    *")
   pcode[1].append("    * This method is safe to call in instructions executed during run()")
   pcode[1].append("    * and is also safe to call outside of run() to generate external events.")
   pcode[1].append("    * If th_sender is null then a sending thread ID of -1 will be passed.")
   pcode[1].append("    */")
   pcode[1].append("   public void sendMessage(float msgtype, float msgdata, ShooterThread th_sender, float id_target)")
   pcode[1].append("   {")
   pcode[1].append("      float id_sender = (th_sender == null) ? -1 : (float) th_sender.threadvars[1];")
   pcode[1].append("      ShooterThread th_target = threads.get((int) id_target);")
   pcode[1].append("      sendMessageImpl(msgtype, msgdata, id_sender, th_target);")
   pcode[1].append("      if (!th_target.msg_isWaitingForMessage)")
   pcode[1].append("         return;")
   pcode[1].append("      scheduled_threads.write((int) th_target.threadvars[1]);")
   pcode[1].append("      th_target.msg_isWaitingForMessage = false;")
   pcode[1].append("      return;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   private void sendMessageImpl(float msgtype, float msgdata, float id_sender, ShooterThread th_target)")
   pcode[1].append("   {")
   pcode[1].append("      Map<Integer, FloatQueue> m = th_target.msg_queue_map;")
   pcode[1].append("      FloatQueue q;")
   pcode[1].append("      if (m != null)")
   pcode[1].append("      {")
   pcode[1].append("         q = m.get((int) msgtype);")
   pcode[1].append("         if (q == null)")
   pcode[1].append("            return;    // silently discard unexpected messages for threads using message declarations")
   pcode[1].append("      }")
   pcode[1].append("      else")
   pcode[1].append("         q = th_target.msg_queue_all;")
   pcode[1].append("      q.write(msgtype);");
   pcode[1].append("      q.write(msgdata);");
   pcode[1].append("      q.write(id_sender);");
   pcode[1].append("      return;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   public void declareMessage(ShooterThread th, float msgtype)")
   pcode[1].append("   {")
   pcode[1].append("       if (th.msg_queue_map == null)")
   pcode[1].append("          th.msg_queue_map = new TreeMap<Integer, FloatQueue>();")
   pcode[1].append("       int i = (int) msgtype;")
   pcode[1].append("       if (th.msg_queue_map.containsKey(i))")
   pcode[1].append("          return;")
   pcode[1].append("       FloatQueue q = new FloatQueue();")
   pcode[1].append("       th.msg_queue_map.put(i, q);")
   pcode[1].append("       separateMessages(th.msg_queue_all, q, (float) i);")
   pcode[1].append("       return;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   public static void separateMessages(FloatQueue src, FloatQueue dest, float msgtype)")
   pcode[1].append("   {")
   pcode[1].append("      // Move all messages of given type from src to dest.")
   pcode[1].append("      int n = src.length();")
   pcode[1].append("      if ((n%3) != 0)")
   pcode[1].append("         throw(new IllegalStateException(\"Message queue length not divisible by 3\"));")
   pcode[1].append("      for(int i=0;i<n;i+=3)")
   pcode[1].append("      {")
   pcode[1].append("         float itype    = src.read();")
   pcode[1].append("         float idata    = src.read();")
   pcode[1].append("         float isender  = src.read();")
   pcode[1].append("         FloatQueue q = (itype == msgtype) ? dest : src;")
   pcode[1].append("         q.write(itype);")
   pcode[1].append("         q.write(idata);")
   pcode[1].append("         q.write(isender);")
   pcode[1].append("      }")
   pcode[1].append("      return;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   public boolean getMessage(ShooterThread th, float msgtype)")
   pcode[1].append("   {")
   pcode[1].append("      if (th.msg_queue_map == null)")
   pcode[1].append("      {")
   pcode[1].append("         FloatQueue q = th.msg_queue_all;")
   pcode[1].append("         if (q.isEmpty())")
   pcode[1].append("            return false;")
   pcode[1].append("         if (msgtype == -1)")
   pcode[1].append("         {")
   pcode[1].append("            this.tf1 = q.read();")
   pcode[1].append("            this.tf2 = q.read();")
   pcode[1].append("            this.tf3 = q.read();")
   pcode[1].append("            return true;")
   pcode[1].append("         }")
   pcode[1].append("         throw(new IllegalStateException(\"If you want to filter messages, use message declarations!\"));")
   pcode[1].append("         // to implement this, you would pull messages from q until done or you get a message of the correct type")
   pcode[1].append("         // then put the irrelevant messages back")
   pcode[1].append("      }")
   pcode[1].append("      if (msgtype == -1)")
   pcode[1].append("      {")
   pcode[1].append("         for(FloatQueue q : th.msg_queue_map.values())")
   pcode[1].append("         {")
   pcode[1].append("            if (!q.isEmpty())")
   pcode[1].append("            {")
   pcode[1].append("               this.tf1 = q.read();")
   pcode[1].append("               this.tf2 = q.read();")
   pcode[1].append("               this.tf3 = q.read();")
   pcode[1].append("               return true;")
   pcode[1].append("            }")
   pcode[1].append("         }")
   pcode[1].append("         return false;")
   pcode[1].append("      }")
   pcode[1].append("      FloatQueue q = th.msg_queue_map.get((int) msgtype);")
   pcode[1].append("      if ((q == null) || (q.isEmpty()))")
   pcode[1].append("         return false;")
   pcode[1].append("      this.tf1 = q.read();")
   pcode[1].append("      this.tf2 = q.read();")
   pcode[1].append("      this.tf3 = q.read();")
   pcode[1].append("      return true;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   public static String showFloat(float f)")
   pcode[1].append("   {")
   pcode[1].append("      int i = (int) f;")
   pcode[1].append("      return (f == (float) i) ? \"\"+i : \"\"+f;")
   pcode[1].append("   }")
   pcode[1].append("   ")
   pcode[1].append("   public boolean isDone()")
   pcode[1].append("   {")
   pcode[1].append("      return (this.threads.size() == 0);")
   pcode[1].append("   }")
   pcode[1].append("   ")
   for x in range(blocknum+1):
      pcode.append(["    private int f"+str(x)+"(ShooterThread sthread)", "    {"])

   for inst in range(int(instructions)):
      floc = inst*9
      if lineinfo[inst][2] != -1:
         blockindex = lineinfo[inst][2] + 2
         if f[floc] in traceInstructions:
            pcode[blockindex] += __createPreTraceCode(f[floc:floc+9], 2, lineinfo[inst][2], lineinfo, inst)
         pcode[blockindex] = pcode[blockindex] + op2func[f[floc]](f[floc:floc+9], 2, lineinfo[inst][2], lineinfo, inst)
         if f[floc] in traceInstructions:
            pcode[blockindex] += __createPostTraceCode(f[floc:floc+9], 2, lineinfo[inst][2], lineinfo, inst)
         #print pcode[blockindex]

   #return the next block if it has not been done
   for i in range(2,len(pcode)):
      if pcode[i][-1].strip().split()[0] != "return":
         pcode[i].append("      return this.f"+str((i-2)+1)+"(sthread);")
      #add the ending brace
      pcode[i].append("    }")
      pcode[i].append("    ")

   #re_reg = re.compile(r"sthread[.]registers[\[]([0-9]+)[\]]")
   #re_state = re.compile(r"sthread[.]state[\[]([0-9]+)[\]]")
   #re_mem = re.compile(r"this[.]mem[\[]([0-9]+)[\]]")
   #re_vm = re.compile(r"this[.]vmdata[\[]([0-9]+)[\]]")
   #re_tv = re.compile(r"sthread[.]threadvars[\[]([0-9]+)[\]]")
   
   if optimize:
       for i in range(2,len(pcode)):
           pcode[i] = var_optimize(pcode[i], re_reg, "temp_register")
           pcode[i] = var_optimize(pcode[i], re_state, "temp_state")
           pcode[i] = var_optimize(pcode[i], re_mem, "temp_mem")
           pcode[i] = var_optimize(pcode[i], re_vm, "temp_vm")
           pcode[i] = var_optimize(pcode[i], re_tv, "temp_tv")
   
   #do math optimization
   #for xrange(
   
   #add the final class closing brace
   pcode.append("}")
   
   #for x in lineinfo:
   #   print x
   out = [b for a in pcode for b in a]
   return out

def makeregex(st):
    out = r""
    for c in st:
        if c == "[":
            out += r"\["
        elif c == "]":
            out += r"\]"
        elif c == ".":
            out += "[.]"
        else:
            out += c
    return out

def insert_after(main, index, stuff):
    out = main[:index]
    out += stuff
    out += main[index:]
    return out

def var_optimize(incodeblock, regex, tempname):
    codeblock = incodeblock[:]
    count_num = {}
    reg_hash = {}
    temp_name = {}
    ns = 0
    for line in codeblock:
        ns = 0
        while True:
            s = regex.search(line[ns:])
            if s is None: break
            ls = line[ns:][s.start():s.end()]
            #print(s.start(), s.end())
            if ls not in count_num:
                count_num[ls] = 1 #count_num = (count, id)
                nls = makeregex(ls)
                reg_hash[ls] = re.compile(nls)
                temp_name[ls] = tempname+line[ns:][s.start(1):s.end(1)]
            else:
                count_num[ls] += 1
            ns += s.end()-s.start()
    #print(count_num)
    for key in count_num:
        if count_num[key] < 2: continue
        for i, line in enumerate(codeblock):
            tl = line[:]
            while True:
                s = reg_hash[key].search(tl)
                if s is None: break
                nl = tl[:s.start()] + temp_name[key] + tl[s.end():]
                tl = nl[:]
            codeblock[i] = tl
            #print(tl)
    enter_code = []
    exit_code = []
    for key in count_num:
        if count_num[key] < 2: continue
        enter_code.append("    float " + temp_name[key] + " = " + key + ";")
        exit_code.append("    " + key + " = " + temp_name[key] + ";")
    ran = [a for a in range(len(codeblock))]
    ran.reverse()    
    for i in ran:
        s = re_ret.search(codeblock[i])
        if s is not None:
            codeblock = insert_after(codeblock, i, exit_code)
    codeblock = insert_after(codeblock, 2, enter_code)
    #print(codeblock)
    
    #print(enter_code)
    #print(exit_code)
    return codeblock
    
