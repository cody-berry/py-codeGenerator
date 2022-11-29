from jackTokenizer import *
from compilationEngine import *
file = 'Average/Main.jack'
tokenizer = JackTokenizer(file)
compileEngine = CompilationEngine(file, tokenizer)

