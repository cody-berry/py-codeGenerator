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
        self.output.write('push ' + self.segmentEnumToVMSegmentMapping[segment] + ' ' + str(index))

    def test(self, function):
        match function:
            case 'push':
                self.writePush(Segments.CONST, 5)
            case 'pop':
                self.writePop(Segments.ARG, 6)
            case 'arithmetic':
                self.writeArithmetic(Command.NOT)
            case 'label':
                self.writeLabel('test')
            case 'goto':
                self.writeGoto('test')
            case 'if':
                self.writeIf('test')
            case 'call':
                self.writeCall('test', 10)
            case 'fun':
                self.writeFunction('test', 10)
            case 'return':
                self.writeReturn()















































































































































