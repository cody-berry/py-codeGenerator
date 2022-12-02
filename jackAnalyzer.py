from jackTokenizer import *
from compilationEngine import *
file = 'Planning/test.jack'
tokenizer = JackTokenizer(file)
compileEngine = CompilationEngine(file, tokenizer)

