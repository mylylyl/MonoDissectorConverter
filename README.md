# MonoDissectorConverter
Convert Mono Dissector's Output to C++ style

A little converter for my handy usage on Unity Games.

UnicodeString is my implemetation of System.String

# Example
input:
```cpp
10 : Name (type: System.String)
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
```

output:
```cpp
UnicodeString* Name; // 0x10
UnicodeString* ShortName; // 0x18
UnicodeString* Description; // 0x20
float Weight; // 0x68
bool ExaminedByDefault; // 0x6C
char pad_XXX[0x3]; // XXX
float ExamineTime; // 0x70
bool QuestItem; // 0x74
char pad_XXX[0x3]; // XXX
JsonType.TaxonomyColor BackgroundColor; // 0x78
int Width; // 0x7C
int Height; // 0x80
int ExtraSizeLeft; // 0x84
int ExtraSizeRight; // 0x88
int ExtraSizeUp; // 0x8C
int ExtraSizeDown; // 0x90
bool ExtraSizeForceAdd; // 0x94
char pad_XXX[0x3]; // XXX
int StackMaxSize; // 0x98
int StackObjectsCount; // 0x9C
int CreditsPrice; // 0xA0
UnicodeString* ItemSound; // 0x28
EFT.ResourceKey Prefab; // 0x30
EFT.ResourceKey UsePrefab; // 0x38
JsonType.ELootRarity Rarity; // 0xA4
float SpawnChance; // 0xA8
bool NotShownInSlot; // 0xAC
char pad_XXX[0x3]; // XXX
int LootExperience; // 0xB0
bool HideEntrails; // 0xB4
char pad_XXX[0x3]; // XXX
int ExamineExperience; // 0xB8
int RepairCost; // 0xBC
int RepairSpeed; // 0xC0
bool MergesWithChildren; // 0xC4
char pad_XXX[0x3]; // XXX
System.String[] ConflictingItems; // 0x40
UnicodeString* _id; // 0x48
UnicodeString* _name; // 0x50
UnicodeString* _parent; // 0x58
EFT.InventoryLogic.NodeType _type; // 0xC8
顓€[] _items; // 0x60
```
