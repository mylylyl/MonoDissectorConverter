# -*- coding: utf-8 -*-

textData = '''10 : Name (type: System.String)
				18 : ShortName (type: System.String)
				20 : Description (type: System.String)
				68 : Weight (type: System.Single)
				6c : ExaminedByDefault (type: System.Boolean)
				70 : ExamineTime (type: System.Single)
				74 : QuestItem (type: System.Boolean)
				78 : BackgroundColor (type: JsonType.TaxonomyColor)
				7c : Width (type: System.Int32)
				80 : Height (type: System.Int32)
				84 : ExtraSizeLeft (type: System.Int32)
				88 : ExtraSizeRight (type: System.Int32)
				8c : ExtraSizeUp (type: System.Int32)
				90 : ExtraSizeDown (type: System.Int32)
				94 : ExtraSizeForceAdd (type: System.Boolean)
				98 : StackMaxSize (type: System.Int32)
				9c : StackObjectsCount (type: System.Int32)
				a0 : CreditsPrice (type: System.Int32)
				28 : ItemSound (type: System.String)
				30 : Prefab (type: EFT.ResourceKey)
				38 : UsePrefab (type: EFT.ResourceKey)
				a4 : Rarity (type: JsonType.ELootRarity)
				a8 : SpawnChance (type: System.Single)
				ac : NotShownInSlot (type: System.Boolean)
				b0 : LootExperience (type: System.Int32)
				b4 : HideEntrails (type: System.Boolean)
				b8 : ExamineExperience (type: System.Int32)
				bc : RepairCost (type: System.Int32)
				c0 : RepairSpeed (type: System.Int32)
				c4 : MergesWithChildren (type: System.Boolean)
				40 : ConflictingItems (type: System.String[])
				48 : _id (type: System.String)
				50 : _name (type: System.String)
				58 : _parent (type: System.String)
				c8 : _type (type: EFT.InventoryLogic.NodeType)
				60 : _items (type: [])
'''

def parseClassName(cName):
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
        print 'char pad_XXX[0x3]; // XXX'
    else:
        print parsedVariableType + ' ' + variable + '; // 0x' + offset

def parseInput():
    for line in textData.splitlines():
        parseLine(line)

def main():
    parseInput()


if __name__ == "__main__":
    main()