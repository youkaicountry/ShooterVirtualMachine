graph_info = [None, None, 1] #from, to

def doCompile(code):
    high = code[1][0]
    fcode = []
    for x in high:
        a = x.split()
        fcode = fcode + op2func[a[0]](a[1:])
    return (None, [fcode])

def __getVal(val):
   if val[0] == "r": return (0.0, float(val[1:]))
   if val[0] == "s": return (2.0, float(val[1:]))
   if val[0] == "m": return (3.0, float(val[1:]))
   if val[0] == "v": return (4.0, float(val[1:]))
   if val[0] == "t": return (7.0, float(val[1:]))
   if val == "=" or val == "==": return (5.0, 0.0)
   if val == "<" : return (5.0, 1.0)
   if val == ">" : return (5.0, 2.0)
   if val == ">=" or val == "=>" : return (5.0, 3.0)
   if val == "<=" or val == "=<" : return (5.0, 4.0)
   if val == "!=" or val == "><" or val == "<>" : return (5.0, 5.0)
   return (1.0, float(val))

def __makeInst(opcode, params):
   out = [opcode]
   for x in params:
      for y in x:
         out.append(y)
   while len(out) < 9:
      out.append(0.0)
   return out

def __a2f_halt(params):
   if len(params) == 0:
      v = __getVal("1")
   else:
      v = __getVal(params[0])
   return __makeInst(1.0, (v,))
   #return [1.0, v[0],v[1], 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0]
   
def __a2f_mov(params):
   tgt = __getVal(params[0])
   a = __getVal(params[1])
   return __makeInst(2.0, (tgt, a))
   
def __a2f_terminate(params):
   return __makeInst(3.0, ())

def __a2f_jmp(params):
   j = __getVal(params[0])
   return __makeInst(4.0, (j,))

def __a2f_add(params):
   if len(params) == 2:
      tgt = __getVal(params[0])
      a = tgt
      b = __getVal(params[1])
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      b = __getVal(params[2])
   return __makeInst(5.0, (tgt, a, b))
   
def __a2f_sub(params):
   if len(params) == 2:
      tgt = __getVal(params[0])
      a = tgt
      b = __getVal(params[1])
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      b = __getVal(params[2])
   return __makeInst(6.0, (tgt, a, b))

def __a2f_mul(params):
   if len(params) == 2:
      tgt = __getVal(params[0])
      a = tgt
      b = __getVal(params[1])
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      b = __getVal(params[2])
   return __makeInst(7.0, (tgt, a, b))

def __a2f_div(params):
   if len(params) == 2:
      tgt = __getVal(params[0])
      a = tgt
      b = __getVal(params[1])
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      b = __getVal(params[2])
   return __makeInst(8.0, (tgt, a, b))
   
def __a2f_atan2(params):
   if len(params) == 2:
      tgt = __getVal(params[0])
      a = tgt
      b = __getVal(params[1])
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      b = __getVal(params[2])
   return __makeInst(38.0, (tgt, a, b))
   
def __a2f_cos(params):
   if len(params) == 1:
      tgt = __getVal(params[0])
      a = tgt
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
   return __makeInst(10.0, (tgt, a))

def __a2f_sin(params):
   if len(params) == 1:
      tgt = __getVal(params[0])
      a = tgt
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
   return __makeInst(9.0, (tgt, a))
   
def __a2f_rnd(params):
   tgt = __getVal(params[0])
   return __makeInst(16.0, (tgt,))
   
def __a2f_mod(params):
   if len(params) == 2:
      tgt = __getVal(params[0])
      a = tgt
      b = __getVal(params[1])
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      b = __getVal(params[2])
   return __makeInst(15.0, (tgt, a, b))

def __a2f_pop(params):
   a = __getVal(params[0])
   return __makeInst(29.0, (a,))

def __a2f_push(params):
   a = __getVal(params[0])
   return __makeInst(28.0, (a,))
   
def __a2f_call(params):
   l = __getVal(params[0])
   return __makeInst(19.0, (l,))

def __a2f_return(params):
   if len(params) == 1:
      v = __getVal(params[0])
   else:
      v = __getVal("0")
   return __makeInst(20.0, (v,))
   
def __a2f_cmp(params):
   if len(params) == 4:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
      sign = __getVal(params[2])
      b = __getVal(params[3])
   else:
      a = __getVal(params[0])
      sign = __getVal(params[1])
      b = __getVal(params[2])
      tgt = a
   return __makeInst(21.0, (tgt, a, sign, b)) 

def __a2f_cndjmp(params):
   l = __getVal(params[0])
   return __makeInst(26.0, (l,))
   
def __a2f_cndcall(params):
   l = __getVal(params[0])
   return __makeInst(27.0, (l,))

def __a2f_gtv(params):
   tgt = __getVal(params[0])
   val = __getVal(params[1])
   tid = __getVal(params[2])
   return __makeInst(35.0, (tgt, val, tid))
   
def __a2f_stv(params):
   tgt = __getVal(params[0])
   val = __getVal(params[1])
   tid = __getVal(params[2])
   return __makeInst(36.0, (tgt, val, tid))
   
def __a2f_spawn(params):
   l = __getVal(params[0])
   return __makeInst(31.0, (l,))

def __a2f_trl(params):
   pid1 = __getVal(params[0])
   cid1 = __getVal(params[1])
   pid2 = __getVal(params[2])
   cid2 = __getVal(params[3])
   return __makeInst(39.0, (pid1, cid1, pid2, cid2))
   
def __a2f_cid(params):
   tgt = __getVal(params[0])
   num = __getVal(params[1])
   pid = __getVal(params[2])
   return __makeInst(40.0, (tgt, num, pid))
   
def __a2f_sqrt(params):
   if len(params) == 1:
      tgt = __getVal(params[0])
      a = tgt
   else:
      tgt = __getVal(params[0])
      a = __getVal(params[1])
   return __makeInst(41.0, (tgt, a))
   
def __a2f_recvwait(params):
   return __makeInst(50.0, (__getVal(params[0]), __getVal(params[1]),
                            __getVal(params[2]), __getVal(params[3])))

def __a2f_recv(params):
   return __makeInst(51.0, (__getVal(params[0]), __getVal(params[1]),
                            __getVal(params[2]), __getVal(params[3])))

def __a2f_send(params):
   return __makeInst(52.0, (__getVal(params[0]), __getVal(params[1]),
                            __getVal(params[2])))

def __a2f_acceptmsg(params):
   return __makeInst(53.0, (__getVal(params[0]),))

def __a2f_trace(params):
   return __makeInst(54.0, (__getVal(params[0]),))

def __a2f_peek(params):
    a = __getVal(params[0])
    return __makeInst(60.0, (a,))

def __a2f_peekat(params):
    tgt = __getVal(params[0])
    l = __getVal(params[1])
    return __makeInst(61.0, (tgt, l))

def __a2f_pokeat(params):
    val = __getVal(params[0])
    l = __getVal(params[1])
    return __makeInst(62.0, (val, l))

def __a2f_sat(params):
    base = __getVal(params[0])
    offset = __getVal(params[1])
    val = __getVal(params[2])
    return __makeInst(70.0, (base, offset, val))

def __a2f_gat(params):
    tgt = __getVal(params[0])
    base = __getVal(params[1])
    offset = __getVal(params[2])
    return __makeInst(71.0, (tgt, base, offset))

def __a2f_gof(params):
    tgt = __getVal(params[0])
    var = __getVal(params[1])
    offset = __getVal(params[2])
    return __makeInst(72.0, (tgt, var, offset))

def __a2f_xupdate(params):
    return __makeInst(256.0, ())

op2func = {}
op2func["halt"] = __a2f_halt
op2func["mov"] = __a2f_mov
op2func["terminate"] = __a2f_terminate
op2func["jmp"] = __a2f_jmp
op2func["add"] = __a2f_add
op2func["sub"] = __a2f_sub
op2func["div"] = __a2f_div
op2func["mul"] = __a2f_mul
op2func["rnd"] = __a2f_rnd
op2func["pop"] = __a2f_pop
op2func["push"] = __a2f_push
op2func["call"] = __a2f_call
op2func["return"] = __a2f_return
op2func["cmp"] = __a2f_cmp
op2func["cndjmp"] = __a2f_cndjmp
op2func["cndcall"] = __a2f_cndcall
op2func["gtv"] = __a2f_gtv
op2func["stv"] = __a2f_stv
op2func["spawn"] = __a2f_spawn
op2func["mod"] = __a2f_mod
op2func["cos"] = __a2f_cos
op2func["sin"] = __a2f_sin
op2func["trl"] = __a2f_trl
op2func["cid"] = __a2f_cid
op2func["sqrt"] = __a2f_sqrt
op2func["atan2"] = __a2f_atan2

op2func["recvwait" ] = __a2f_recvwait    #recvwait
op2func["recv"     ] = __a2f_recv        #recv
op2func["send"     ] = __a2f_send        #send
op2func["acceptmsg"] = __a2f_acceptmsg   #accept
op2func["trace"    ] = __a2f_trace       #trace

op2func["peek"] = __a2f_peek
op2func["peekat"] = __a2f_peekat
op2func["pokeat"] = __a2f_pokeat

op2func["sat"] = __a2f_sat
op2func["gat"] = __a2f_gat
op2func["gof"] = __a2f_gof

op2func["xupdate"] = __a2f_xupdate
