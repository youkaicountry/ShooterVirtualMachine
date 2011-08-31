from . import modules
from . import languages
import YoukaiTools
from YoukaiTools import GraphEngine
    

#compilers have the proper languages loaded, so the host program simply
#loads the set of compilers, and this chain will build a graph of how
#to compile from any language to any other language.
class CompilerChain:
    def __init__(self, compilers):
        self.graph = None
        self.compilers = compilers
        self.__buildGraph()
        return
    
    def doCompile(self, code, to_lang):
        path = YoukaiTools.GraphEngine.GraphTools.Paths.dijkstraPaths(self.graph, code[0], to_lang, "cost")
        curcode = code
        for node in path:
            if node[1] is not None:
                curcode = node[1].doCompile(curcode)
        return curcode
    
    def __buildGraph(self):
        g = GraphEngine.BasicGraph()
        for comp in self.compilers:
            for lang in comp.graph_info[:2]:
                if not g.containsVertex(lang):
                    g.addVertex(lang)
        
        for comp in self.compilers:
            g.addEdge(comp.graph_info[0], comp.graph_info[1], True, comp)
            g.setEdgeData(comp, "cost", comp.graph_info[2])
        
        self.graph = g
        return
    
