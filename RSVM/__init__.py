import RSVM as RSVMmod
import compiler as compilermod
import fcode as fcodemod
import assembly as assemblymod
import python as pythonmod
import java as javamod
import intermediate as intermediatemod

RSVM = RSVMmod.RSVM

compileHighFileToAssemblyList = compilermod.compileHighFileToAssemblyList
compileHighListToFCodeList = compilermod.compileHighListToFCodeList
compileHighFileToFCodeList = compilermod.compileHighFileToFCodeList
compileAssemblyListToFCodeFile = compilermod.compileAssemblyListToFCodeFile
compileAssemblyListToFCodeList = compilermod.compileAssemblyListToFCodeList
compileFCodeListToPythonList = compilermod.compileFCodeListToPythonList
compileFCodeListToJavaList = compilermod.compileFCodeListToJavaList
compileFCodeListToIntermediateList = compilermod.compileFCodeListToIntermediateList


loadFCode = fcodemod.loadFCode
saveFCode = fcodemod.saveFCode
loadAssembly = assemblymod.loadAssembly
saveAssembly = assemblymod.saveAssembly
savePython = pythonmod.savePython
saveJava = javamod.saveJava
saveIntermediate = intermediatemod.saveIntermediate

