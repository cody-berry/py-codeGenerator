from enum import Enum


class Segments(Enum):
    CONST = 0
    ARG = 1
    LOCAL = 2
    STATIC = 3
    THIS = 4
    THAT = 5
    POINTER = 6
    TEMP = 7


class Command(Enum):
    ADD = 0
    SUB = 1
    NEG = 2
    EQ = 3
    GT = 4
    LT = 5
    AND = 6
    OR = 7
    NOT = 8


class VMWriter:
    def __init__(self, output):
        self.output = open(output, 'w')
        # now we need to map the segment enums to VM segments
        self.segmentEnumToVMSegmentMapping = {
            Segments.CONST: 'constant',
            Segments.ARG: 'arg',
            Segments.LOCAL: 'local',
            Segments.STATIC: 'static',
            Segments.THIS: 'this',
            Segments.THAT: 'that',
            Segments.POINTER: 'pointer',
            Segments.TEMP: 'temp'
        }
        # plus, we need to map the command enums to VM arithmetic logic commands
        self.commandEnumToVMArithmeticLogicCommandMapping = {
            Command.ADD: 'add',
            Command.SUB: 'sub',
            Command.NEG: 'neg',
            Command.EQ: 'eq',
            Command.GT: 'gt',
            Command.LT: 'lt',
            Command.AND: 'and',
            Command.OR: 'or',
            Command.NOT: 'not'
        }

    def writePush(self, segment, index):
        self.output.write('push ' + self.segmentEnumToVMSegmentMapping[segment] + ' ' + str(index) + '\n')

    def writePop(self, segment, index):
        self.output.write('pop ' + self.segmentEnumToVMSegmentMapping[segment] + ' ' + str(index) + '\n')

    def writeArithmetic(self, command):
        self.output.write(self.commandEnumToVMArithmeticLogicCommandMapping[command] + '\n')

    def test(self, function, test1=None, test2=None):
        match function:
            case 'push':
                self.writePush(test1, test2)
            case 'pop':
                self.writePop(test1, test2)
            case 'arithmetic':
                self.writeArithmetic(test1)
            case 'label':
                self.writeLabel(test1)
            case 'goto':
                self.writeGoto(test1)
            case 'if':
                self.writeIf(test1)
            case 'call':
                self.writeCall(test1, test2)
            case 'fun':
                self.writeFunction(test1, test2)
            case 'return':
                self.writeReturn()















































































































































