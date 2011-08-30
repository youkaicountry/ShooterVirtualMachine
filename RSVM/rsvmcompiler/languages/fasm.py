def constructOutputFiles(code, fname="gen.fasm"):
    gen = __constructMainFile(code, fcode)
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
    return "fasm"
    
