# -*- coding: utf-8 -*-

textData = '''40 : UnlimitedCount (type: System.Boolean)
				44 : BuyRestrictionMax (type: System.Int32)
				48 : BuyRestrictionCurrent (type: System.Int32)
				4c : StackObjectsCount (type: System.Int32)
				50 : Version (type: System.Int32)
				10 : Id (type: System.String)
				18 : Parent (type: a)
				20 : atemplate (type: EFT.InventoryLogic.ItemTemplate)
				28 : OnLoadAction (type: System.Action<System.Boolean>)
				30 : Components (type: System.Collections.Generic.List<>)
				38 : Qualities (type: System.Collections.Generic.List<>)
'''

def parseClassName(cName):
    if len(cName) > 2:
        if cName[-2:] == '[]':
            return 'Array<' + parseClassName(cName[:-2]) + '>*'
        else:
            if cName == 'System.String':
                return 'UnicodeString*'
            if cName == 'System.Int32':
                return 'int'
            if cName == 'System.Single':
                return 'float'
            if cName == 'System.Boolean':
                return 'bool'
        return cName
    else:
        return 'Empty'

def parseLine(input):
    tup = input.partition(':')
    offset = tup[0].expandtabs().replace(' ', '').upper()
    tup = tup[2].partition('(')
    variable = tup[0].replace(' ', '')
    tup = tup[2].partition(('type: '))
    variableType = tup[2].partition(')')[0]
    parsedVariableType = parseClassName(variableType)
    if parsedVariableType == 'bool':
        print parsedVariableType + ' ' + variable + '; // 0x' + offset
        print 'char pad_00XX[0x3]; // 0xXX'
    else:
        print parsedVariableType + ' ' + variable + '; // 0x' + offset

def parseInput():
    for line in textData.splitlines():
        parseLine(line)

def main():
    parseInput()

if __name__ == "__main__":
    main()