from jackTokenizer import *
from compilationEngine import *
import pathlib

# file = 'Planning/test.jack'
file = 'ComplexArrays'
nextLabel = 0
if file[-5:] == '.jack':
    tokenizer = JackTokenizer(file)
    compileEngine = CompilationEngine(file, tokenizer, 0)
else:
    for path in pathlib.Path(
            file).iterdir():  # iterate through all the files in the directory
        print(path)
        if path.__str__()[-4:] == 'jack':
            tokenizer = JackTokenizer(path.__str__())
            compileEngine = CompilationEngine(path.__str__(), tokenizer, nextLabel)
            nextLabel = compileEngine.ifAndWhileLabels
            print("accepted!")
