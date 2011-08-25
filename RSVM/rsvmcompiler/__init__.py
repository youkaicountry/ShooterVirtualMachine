from . import modules
from . import languages

#compilers have the proper languages loaded, so the host program simply
#loads the set of compilers, and this chain will build a graph of how
#to compile from any language to any other language.
class CompilerChain:
    def __init__(self, compilers):
        self.graph = None
        self.compilers = compilers
        self.__buildGraph()
        return
    
    def doCompile(self, code, from_lang, to_lang):
        return
    
    def __buildGraph(self):
        return
    
