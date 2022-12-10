from jackTokenizer import *
from compilationEngine import *
# file = 'Planning/test.jack'
file = 'ConvertToBin/Main.jack'
tokenizer = JackTokenizer(file)
compileEngine = CompilationEngine(file, tokenizer)

