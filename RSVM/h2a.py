#TODO: make decl be decl r0 (you define which register)

#high assembly to assembly
import copy

ulabelnum = 0

statevars = {}
statevars["__x"] = "s0"
statevars["__y"] = "s1"
statevars["__angle"] = "s2"
statevars["__targetx"] = "s3"
statevars["__targety"] = "s4"
statevars["__velx"] = "s7"
statevars["__vely"] = "s8"
statevars["__accx"] = "s9"
statevars["__accy"] = "s10"
statevars["__mass"] = "s11"
statevars["__movechildren"] = "s12"
statevars["__oldx"] = "s16"
statevars["__oldy"] = "s17"
statevars["__thrustvel"] = "s18"
statevars["__thrustacc"] = "s19"
statevars["__userad"] = "s20"
statevars["__rotvel"] = "s21"
statevars["__rotacc"] = "s22"
statevars["__towardvel"] = "s23"
statevars["__towardacc"] = "s24"
statevars["__turnvel"] = "s25"
statevars["__turnacc"] = "s26"
statevars["__sprite"] = "s27"
statevars["__radius"] = "s28"
statevars["__parentid"] = "t0"
statevars["__selfid"] = "t1"
statevars["__returnval"] = "t3"
statevars["__condition"] = "t2"
statevars["__spawnid"] = "t4"
statevars["__numchildren"] = "t5"
statevars["__dead"] = "t6"
statevars["__stacksize"] = "t7"
statevars["__nummessages"] = "t8"
statevars["__stackloc"] = "t9"
statevars["__playerx"] = "v0"
statevars["__playery"] = "v1"

from . import high

def high2assembly(highcode, startname):
   middic = copy.deepcopy(highcode)

   #print middic

   #0. expand dotted labels
   for x in middic.keys():
      lastnormal = ""
      for linenum in range(len(middic[x]["code"])):
         if len(middic[x]["code"][linenum].split(":")) > 1:
            if middic[x]["code"][linenum].split(".")[0] == "":
               middic[x]["code"][linenum] = lastnormal + middic[x]["code"][linenum]
            else:
               lastnormal = middic[x]["code"][linenum][:-1]

   

   #1. nix decl's/associate varnames with 
   for x in middic.keys():
      middic[x]["vars"] = {}
      for line in middic[x]["code"]:
         if line.split()[0] == "decl":
            middic[x]["vars"][line.split()[1]] = line.split()[2] #the register number to associate the variable to
            
   for x in middic.keys():
      newcode = []
      for linenum in range(len(middic[x]["code"])):
         if middic[x]["code"][linenum].split()[0] != "decl":
            newcode.append(middic[x]["code"][linenum])
      middic[x]["code"] = newcode
      
   #find and prepare timers
   for x in middic.keys():
      middic[x]["timers"] = {}
      for line in middic[x]["code"]:
         if line.split()[0] == "setjmptimer":
            middic[x]["timers"][line.split()[1]] = (line.split()[2], line.split()[3], "jmp")
         if line.split()[0] == "setcalltimer":
            middic[x]["timers"][line.split()[1]] = (line.split()[2], line.split()[3], "call")    
   
   #add movechildren
   halts = {}
   for x in middic.keys():
      halts[x] = []
      for linenum in range(len(middic[x]["code"])):
         if middic[x]["code"][linenum].split()[0] == "halt": halts[x].append(linenum)
   
   for x in middic.keys():
      halts[x].reverse()
      for y in halts[x]:
         __exp_oldloc(middic[x]["code"], None, None, y) #set the conditions on the halt
         
   #collect initial labels
   for x in middic.keys():
      middic[x]["basiclabels"] = set()
      for line in middic[x]["code"]:
         if line.split(":")[0] != "":
            middic[x]["basiclabels"].add(line.split(":")[0])
      
   #2. expand special instructions
   for x in middic.keys():
      linenum = 0
      while True:
         
         line = middic[x]["code"][linenum]
         linesplit = line.split()
         #print linesplit
         if len(linesplit) > 0:
            if linesplit[0] == "update":
               __exp_update(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "ifjmp" or linesplit[0] == "ifcall":
               __exp_ifjmpcall(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "tgtself":
               __exp_tgtself(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "tgtparent":
               __exp_tgtparent(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "tgtplayer":
               __exp_tgtplayer(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "tgt":
               __exp_tgt(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "turn":
               __exp_turn(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "moveface":
               __exp_moveface(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "spawntgt":
               __exp_spawntgt(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "movechildren":
               __exp_movechildren(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "forallchildren":
               __exp_forallchildren(middic[x]["code"], line, linesplit, linenum, middic[x]["basiclabels"])
            if linesplit[0] == "setjmptimer" or linesplit[0] == "setcalltimer":
               __exp_settimer(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "inctimer":
               __exp_inctimer(middic[x]["code"], line, linesplit, linenum, middic[x]["timers"], middic[x]["basiclabels"])
            if linesplit[0] == "facetgt":
               __exp_facetgt(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "addfacevel":
               __exp_addfacevel(middic[x]["code"], line, linesplit, linenum)
            if linesplit[0] == "addfaceacc":
               __exp_addfaceacc(middic[x]["code"], line, linesplit, linenum)
            
         linenum += 1
         if linenum >= len(middic[x]["code"]): break
   
   
   
   #3. set variable names
   for x in middic.keys():
      for linenum in range(len(middic[x]["code"])):
         newline = middic[x]["code"][linenum]
         linep = newline.split()
         outline = linep[0]
         for y in linep[1:]:
            attach = y
            if y in statevars:
               attach = statevars[y]
            elif len(y.split(".")) > 1:
               scheck = ""
               for t in y.split(".")[:-1]:
                  scheck = scheck + t + "."
               if len(scheck) > 0 and scheck[-1] == ".": scheck = scheck[:-1]
               if scheck in middic:
                  #print "SCHECK:" + scheck
                  if y.split(".")[-1] in middic[scheck]["vars"]:
                     attach = "r" + str(middic[scheck]["vars"][y.split(".")[-1]])
            else:
               if y in middic[x]["vars"]:
                  attach = str(middic[x]["vars"][y])
            outline = outline + " " + attach
         middic[x]["code"][linenum] = outline.strip()
   
   #4. put label at top if none present
   for x in middic.keys():
      if middic[x]["code"][0] != "init:":
         middic[x]["code"].insert(0, "init:")
   
   templabels = set()
   #5a. rename labels
   for x in middic.keys():
      templabels = set()
      for linenum in range(len(middic[x]["code"])):
         if len(middic[x]["code"][linenum].split(":")) > 1:
            templabels.add(middic[x]["code"][linenum][:-1])
            middic[x]["code"][linenum] = x + "." + middic[x]["code"][linenum]
      #5b. rename reference to the labels
      for linenum in range(len(middic[x]["code"])):
         newline = middic[x]["code"][linenum]
         linep = newline.split()
         outline = linep[0]
         for y in linep[1:]:
            attach = y
            if y in templabels:
               attach = x + "." + y
            outline = outline + " " + attach
         middic[x]["code"][linenum] = outline.strip()
   
   #print middic
         
   #7. remove labels and store in dictionary
   for x in middic.keys():
      newinst = []
      middic[x]["labels"] = {}
      for linenum in range(len(middic[x]["code"])):
         if len(middic[x]["code"][linenum].split(":")) > 1:
            middic[x]["labels"][middic[x]["code"][linenum].split(":")[0]] = len(newinst)
         else:
            newinst.append(middic[x]["code"][linenum])
      middic[x]["code"] = newinst
      
   #8. Append bits of code into one large piece
   labeladd = 0
   alllabels = {}
   allcode = []
   allcode = allcode + middic[startname]["code"]
   for x in middic[startname]["labels"].keys():
      alllabels[x] = middic[startname]["labels"][x]
   labeladd = len(allcode)
   del middic[startname]   
   for c in middic.keys():
      allcode = allcode + middic[c]["code"]
      for x in middic[c]["labels"].keys():
         alllabels[x] = middic[c]["labels"][x] + labeladd
      labeladd = len(allcode)
   
   #9. Change labels
   for linenum in range(len(allcode)):
      newline = allcode[linenum]
      linep = newline.split()
      outline = linep[0]
      for y in linep[1:]:
         attach = y
         if y in alllabels:
            attach = str(alllabels[y])
         outline = outline + " " + attach
      allcode[linenum] = outline.strip()
   
   
   return allcode
   
   
def __exp_update(code, line, linesplit, linenum):
   code.pop(linenum)
   __insertCode(code, linenum, ["call lib_rsvm.update"])
   return
   
def __exp_tgtself(code, line, linesplit, linenum):
   code.pop(linenum)
   __insertCode(code, linenum, ["call lib_rsvm.tgtself"])
   return
   
def __exp_tgtparent(code, line, linesplit, linenum):
   code.pop(linenum)
   __insertCode(code, linenum, ["call lib_rsvm.tgtparent"])
   return

def __exp_tgtplayer(code, line, linesplit, linenum):
   code.pop(linenum)
   __insertCode(code, linenum, ["call lib_rsvm.tgtplayer"])
   return
   
def __exp_tgt(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   ins.append("mov __targetx "+linesplit[1])
   ins.append("mov __targety "+linesplit[2])
   __insertCode(code, linenum, ins)
   return
   
def __exp_turn(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   ins.append("add __angle "+linesplit[1])
   __insertCode(code, linenum, ins)
   return
   
def __exp_moveface(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   regs = __getTempRegs([linesplit[1]], 2)
   ins.append("push "+regs[0])
   ins.append("push "+regs[1])
   ins.append("cos "+regs[0]+" __angle")
   ins.append("sin "+regs[1]+" __angle")
   ins.append("mul "+regs[0]+" "+linesplit[1])
   ins.append("mul "+regs[1]+" "+linesplit[1])
   ins.append("add __x "+regs[0])
   ins.append("add __y "+regs[1])
   ins.append("pop "+regs[1])
   ins.append("pop "+regs[0])
   __insertCode(code, linenum, ins)
   return
   
def __exp_ifjmpcall(code, line, linesplit, linenum):
   #regs = __getTempRegs([linesplit[1], linesplit[3]], 1)
   code.pop(linenum)
   ins = []
   ins.append("cmp __condition "+linesplit[1]+" "+linesplit[2]+" "+linesplit[3])
   if linesplit[0] == "ifjmp": ins.append("cndjmp " + linesplit[4])
   else: ins.append("cndcall "+linesplit[4])
   __insertCode(code, linenum, ins)
   return
   
def __exp_spawntgt(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   ins.append("spawn "+linesplit[1])
   ins.append("stv __x __targetx __spawnid")
   ins.append("stv __y __targety __spawnid")
   ins.append("stv __angle __angle __spawnid")
   __insertCode(code, linenum, ins)
   return
   
def __exp_facetgt(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   ins.append("push __targetx")
   ins.append("push __targety")
   ins.append("sub __targetx __x")
   ins.append("sub __targety __y")
   ins.append("atan2 __angle __targety __targetx")
   ins.append("pop __targety")
   ins.append("pop __targetx")
   __insertCode(code, linenum, ins)
   return
   
def __exp_addfacevel(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   regs = __getTempRegs([linesplit[1]], 1)
   ins.append("push "+regs[0])
   ins.append("cos "+regs[0]+" __angle")
   ins.append("mul "+regs[0]+" "+linesplit[1])
   ins.append("add __velx "+regs[0])
   ins.append("sin "+regs[0]+" __angle")
   ins.append("mul "+regs[0]+" "+linesplit[1])
   ins.append("add __vely "+regs[0])
   ins.append("pop "+regs[0])
   __insertCode(code, linenum, ins)
   return

def __exp_addfaceacc(code, line, linesplit, linenum):
   code.pop(linenum)
   ins = []
   regs = __getTempRegs([linesplit[1]], 1)
   ins.append("push "+regs[0])
   ins.append("cos "+regs[0]+" __angle")
   ins.append("mul "+regs[0]+" "+linesplit[1])
   ins.append("add __accx "+regs[0])
   ins.append("sin "+regs[0]+" __angle")
   ins.append("mul "+regs[0]+" "+linesplit[1])
   ins.append("add __accy "+regs[0])
   ins.append("pop "+regs[0])
   __insertCode(code, linenum, ins)
   return

def __exp_oldloc(code, line, linesplit, linenum):
   ins = []
   ins.append("mov __oldx __x")
   ins.append("mov __oldy __y")
   __insertCode(code, linenum, ins)
   
   return

def __exp_forallchildren(code, line, linesplit, linenum, usedlabels):
   ins = []
   code.pop(linenum)
   #regs = __getTempRegs([linesplit[1]], 1)
   labs = __getUniqueLabels(usedlabels, 2)
   ins.append("mov "+linesplit[2]+" 0")
   ins.append(labs[0]+":")
   ins.append("cmp __condition "+linesplit[2]+" >= __numchildren")
   ins.append("cndjmp "+labs[1])
   ins.append("cid "+linesplit[1]+" "+linesplit[2]+" __selfid")
   ins.append("call "+linesplit[3])
   ins.append("add "+linesplit[2]+" 1")
   ins.append("jmp "+labs[0])
   ins.append(labs[1]+":")
   __insertCode(code, linenum, ins)
   return
   
def __exp_movechildren(code, line, linesplit, linenum):
   ins = []
   code.pop(linenum)
   ins.append("push r0")
   ins.append("push r1")
   ins.append("mov r0 __selfid")
   ins.append("sub r1 __x __oldx")
   ins.append("sub r2 __y __oldy")
   ins.append("call lib_rsvm.movechildren")
   ins.append("pop r1")
   ins.append("pop r0")
   __insertCode(code, linenum, ins)
   return
   
def __exp_inctimer(code, line, linesplit, linenum, timer, usedlabels):
   newlabels = __getUniqueLabels(usedlabels, 1)
   timervar = linesplit[1]
   if len(linesplit) == 2:
      amount = "1"
   else:
      amount = linesplit[2]
   ins = []
   code.pop(linenum)
   ins.append("sub "+timervar+" "+amount)
   ins.append("cmp __condition "+timervar+" > 0")
   ins.append("cndjmp "+newlabels[0])
   ins.append("mov "+timervar+" "+timer[timervar][0])
   ins.append(timer[timervar][2]+" "+timer[timervar][1])
   ins.append(newlabels[0]+":")
   __insertCode(code, linenum, ins)
   return
   
def __exp_settimer(code, line, linesplit, linenum):
   code.pop(linenum)
   __insertCode(code, linenum, ["mov "+linesplit[1]+" "+linesplit[2]])
   return
   
def __insertCode(code, where, what):
   i = where
   for x in what:
      code.insert(i, x)
      i = i + 1
   return

def __getUniqueLabels(used, num):
   out = []
   global ulabelnum
   while len(out) < num:
      if "tlab_"+str(ulabelnum) not in used:
         out.append("tlab_"+str(ulabelnum))
      ulabelnum += 1
   return out

#fill used with the strings of registers to be avoided ["r1", "r5"] and it will return
#a list of num useable ones.   
def __getTempRegs(used, num):
   out = []
   t = 0
   i = 0
   while t <= num:
      if "r"+str(i) not in used:
         out.append("r"+str(i))
         t += 1
      i += 1
   return out
   
   
