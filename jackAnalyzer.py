from jackTokenizer import *
from compilationEngine import *
file = 'Seven/Main.jack'
tokenizer = JackTokenizer(file)
compileEngine = CompilationEngine(file, tokenizer)

