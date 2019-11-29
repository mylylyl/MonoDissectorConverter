# MonoDissectorConverter

Convert output of Cheat Engine's (version 5.6) Mono Dissector to C++ style code
(note that CE 5.6 has a different output with previous version)

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

```c#
FileHeader
	52cd540 : Assembly-CSharp
		17876c2abe0 : System.IO.FileStreamAsyncResult
			static fields
			fields
				10 : state (type: System.Object)
				40 : completed (type: System.Boolean)
				41 : done (type: System.Boolean)
				18 : exc (type: System.Exception)
				20 : wh (type: System.Threading.ManualResetEvent)
				28 : cb (type: System.AsyncCallback)
				42 : completedSynch (type: System.Boolean)
				30 : Buffer (type: System.Byte[])
				44 : Offset (type: System.Int32)
				48 : Count (type: System.Int32)
				4c : OriginalCount (type: System.Int32)
				50 : BytesRead (type: System.Int32)
				38 : realcb (type: System.AsyncCallback)
			methods
				178788c7ca0 : .ctor (cb: System.AsyncCallback; state: object):System.Void
				178788c7cc8 : CBWrapper (ares: System.IAsyncResult):System.Void
				178788c7d18 : SetComplete (e: System.Exception; nbytes: int):System.Void
				178788c7cf0 : SetComplete (e: System.Exception):System.Void
				178788c7d40 : SetComplete (e: System.Exception; nbytes: int; synch: bool):System.Void
				178788c7d68 : get_AsyncState ():System.Object
				178788c7db8 : get_AsyncWaitHandle ():System.Threading.WaitHandle
				178788c7d90 : get_CompletedSynchronously ():System.Boolean
				178788c7e30 : get_Done ():System.Boolean
				178788c7e08 : get_Exception ():System.Exception
				178788c7de0 : get_IsCompleted ():System.Boolean
				178788c7e58 : set_Done (value: bool):System.Void
			base class
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
