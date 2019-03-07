# MonoDissectorConverter
Convert output of Cheat Engine's Mono Dissector to C++ style code

This is a handy tool for my personal project, and it's only for educational purposes

UnicodeString is my implementation of System.String



Current this script only support the exact formatting of output file of Mono Dissector which looks like this

```
Header (usually an address, 0 indent)
	File Header (usually an address with file name, 1 indent)
		Package Header (usually an address with package name, 2 indents)
			fields (declearing the following content to be "fields", 3 indents)
				variables_and_offsets (4 indents)
            methods (declearing the following content to be "methods", 3 indents)
            	methods_and_offsets (4 inddents)
```



# Example

Input:

```cpp
FileHeader
	52cd540 : Assembly-CSharp
		276f8f40 : System.IO:FileStreamAsyncResult
			fields
				10 : state (type: System.Object)
				18 : completed (type: System.Boolean)
				19 : done (type: System.Boolean)
				20 : exc (type: System.Exception)
				28 : wh (type: System.Threading.ManualResetEvent)
				30 : cb (type: System.AsyncCallback)
				38 : completedSynch (type: System.Boolean)
				40 : Buffer (type: System.Byte[])
				48 : Offset (type: System.Int32)
				4c : Count (type: System.Int32)
				50 : OriginalCount (type: System.Int32)
				54 : BytesRead (type: System.Int32)
				58 : realcb (type: System.AsyncCallback)
			methods
				2788f5d0 : .ctor
				2788f600 : CBWrapper
				2788f630 : SetComplete
				2788f660 : SetComplete
				2788f690 : SetComplete
				276e9368 : get_AsyncState
				276e9398 : get_CompletedSynchronously
				276e93c8 : get_AsyncWaitHandle
				276e93f8 : get_IsCompleted
				2788f6c0 : get_Exception
				2788f6f0 : get_Done
				2788f720 : set_Done
```

Output:
```cpp
System_Object*  state;          //0x10
bool    completed;              //0x18
bool    done;           //0x19
System_Exception*       exc;            //0x20
System_Threading_ManualResetEvent*      wh;             //0x28
System_AsyncCallback*   cb;             //0x30
bool    completedSynch;         //0x38
Array<uint8_t>* Buffer;         //0x40
int32_t Offset;         //0x48
int32_t Count;          //0x4c
int32_t OriginalCount;          //0x50
int32_t BytesRead;              //0x54
System_AsyncCallback*   realcb;         //0x58
```
