# -*- coding: utf-8 -*-
import string
import math

textData = """FileHeader
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
			base class"""

# translation of built-in functions of C# to C++
# you may set up your own translation here
BUILT_IN_FUNC = {
    "System.Byte":      "uint8_t",
    "System.UInt16":    "uint16_t",
    "System.UInt32":    "uint32_t",
    "System.UInt64":    "uint64_t",
    "System.Int16":     "int16_t",
    "System.Int32":     "int32_t",
    "System.Int64":     "int64_t",
    "System.UIntPtr":   "uintptr_t",
    "System.IntPtr":    "intptr_t",
    "System.Single":    "float",
    "System.Void":      "void",
    "System.Boolean":   "bool",
    # below are my custom implementations
    "System.String":    "UnicodeString",
    "System.Object":    "Object"
}

# Helper function to parse class name
def parse_class_name(class_name, is_array = False):
    if class_name[-2:] == "[]":
        # First we need to know if it's an array
        # Ex. Transform[] -> Array<Transform>*
        # Array<> is my personal implementation
        return "Array<" + parse_class_name(class_name[:-2], True) + ">" + ("" if is_array else "*")
    elif len(class_name) >= 33 and class_name[:31] == "System.Collections.Generic.List":
        # Next we need to know if it's a list
        # Ex. System.Collections.Generic.List<Transform> -> List<Transform>*
        # List<> is my personal implementation
        return "List<" + parse_class_name(class_name[32:-1], True) + ">" + ("" if is_array else "*")
    elif len(class_name) >= 34 and class_name[:32] == "System.Collections.Generic.Stack":
        # Next we need to know if it's a stack
        # Ex. System.Collections.Generic.Stack<Transform> -> Stack<Transform>*
        # Stack<> is my personal implementation
        return "Stack<" + parse_class_name(class_name[33:-1], True) + ">" + ("" if is_array else "*")
    elif len(class_name) >= 39 and class_name[:37] == "System.Collections.Generic.Dictionary":
        # Next we need to know if it's an dictionary
        # Ex. System.Collections.Generic.Dictionary<Player, Transform> -> Dictionary<Player, Transform>*
        # Dictionary<> is my personal implementation
        comma_index = class_name.find(",")
        if comma_index > 0:
            first_var = class_name[38:comma_index]
            second_var = class_name[comma_index+1:-1]
            return "Dictionary<" + parse_class_name(first_var, True) + ", " + parse_class_name(second_var, True) + ">" + ("" if is_array else "*")
        elif comma_index == 0:
            # We are not sure about this special case
            print("[!] Warning: Dictionary Parser found a special case: " + class_name)
        else:
            print("[!] Error: Dictionary Parser found encountered an error: " + class_name)
        return class_name
    elif len(class_name) >= 13 and class_name[:11] == "System.Func":
        # Next we need to know if it's a Func
        # Ex. System.Func<Player, Transform> -> Func<Player, Transform>*
        # Func<> is my personal implementation
        comma_index = class_name.find(",")
        if comma_index > 0:
            first_var = class_name[12:comma_index]
            second_var = class_name[comma_index+1:-1]
            return "Func<" + parse_class_name(first_var, True) + ", " + parse_class_name(second_var, True) + ">" + ("" if is_array else "*")
        elif comma_index == 0:
            # We are not sure about this special case
            print("[!] Warning: Func Parser found a special case: " + class_name)
        else:
            print("[!] Error: Func Parser found encountered an error: " + class_name)
        return class_name
    # TO-DO: Handle System.Action and System.Action<>
    # I have a personal preference here, ex. UnityEngine.Transform -> Transform*
    elif len(class_name) >= 12 and class_name[:12] == "UnityEngine.":
        return class_name[12:] + ("" if is_array else "*")
    else:
        # First we parse some built-in nameing
        if class_name == "System.Byte":
            return "uint8_t"
        elif class_name == "System.UInt16":
            return "uint16_t"
        elif class_name == "System.UInt32":
            return "uint32_t"
        elif class_name == "System.UInt64":
            return "uint64_t"
        elif class_name == "System.Int16":
            return "int16_t"
        elif class_name == "System.Int32":
            return "int32_t"
        elif class_name == "System.Int64":
            return "int64_t"
        elif class_name == "System.UIntPtr":
            return "void*"
        elif class_name == "System.IntPtr":
            return "void*"
        elif class_name == "System.Single":
            return "float"
        elif class_name == "System.Boolean":
            # We'll do special handling in offset for booleans
            return "bool"
        elif class_name == "System.String":
            # UnicodeString is my personal implementation of System.String
            return "UnicodeString" if is_array else "UnicodeString*"
        else:
            # Normally everything is pointer so we just add * anyway.
            # We'll sway all . to _ as well
            return class_name.replace(".", "_") + ("" if is_array else "*")

class Line:
    def parse_line(self):
        # Helper function that seperate by " : "
        index = self.content.find(" : ")
        if index > 0:
            self.offset = int("0x" + self.content[:index].lower(), 0)
            self.name = self.content[index+3:]
        elif index == 0:
            # We are not sure about this special case
            print("[!] Warning: Line Parser found a special case: " + self.content)
        else:
            print("[!] Error: Line Parser found encountered an error: " + self.content)

    def parse_cpp_style(self):
        # Parse name to C++ style
        # Ex. intensity (type: System.Single) will be type -> float and name -> intensity
        # This only works for "fields"
        index = self.name.find("(type: ")
        if index > 0:
            cpp_temp = self.name[index:]
            if cpp_temp[:7] != "(type: ":
                print("[!] Error: Style Parser found encountered an error: " + cpp_temp)
            else:
                class_name = cpp_temp[7:-1]
                self.type_name = parse_class_name(class_name, False)
                self.name = self.name[:index-1]
        elif index == 0:
            # We are not sure about this special case
            print("[!] Warning: Style Parser found a special case: " + self.content)
        else:
            print("[!] Error: Style Parser found encountered an error: " + self.content)

    def debug_display_line(self, display_raw_content = False, is_cpp_style = False):
        if self.tabs == 3:
            print("\t" + self.content)
        else:
            if is_cpp_style:
                print("\t" + self.type_name + "\t" + self.name + ";\t\t//" + hex(self.offset))
            else:
                print("\toffset: " + hex(self.offset) + ", name: " + self.name + (", content: " + self.content if display_raw_content else ""))

    def __init__(self, tabs = 0, content = "", offset = 0, name = "Empty", type_name = "EmptyClass*"):
        self.tabs = tabs
        self.content = content
        # We do not pass these two
        self.offset = offset # offset are stored in decimal
        self.name = name
        self.type_name = type_name

        if tabs == 1 or tabs == 2 or tabs == 4:
            # Only parse line because 0 is file header, 3 is "field" or "method"
            self.parse_line()

# Helper function to find a section which returns the index of the end of this section
# Pass the line of parent-level
def find_section(lines, index, tabs):
    length = 0
    for i in range(index, len(lines)):
        if i == index:
            # This is the starting line
            continue
        if lines[i].tabs == tabs:
            # We are in another Same-level section
            return index + length
        elif lines[i].tabs < tabs:
            # We are in another Parent-level section
            return index + length
        else:
            # This is what we want
            length += 1
    return index + length

# Helper function to perform bubble sort on array
def bubble_sort(lines):
    # Walk the list in reverse order, get the index
    for x in range(len(lines) - 1, 0 , -1):
        for y in range(x):
            if lines[y].offset > lines[y+1].offset:
                tmp = lines[y]
                lines[y] = lines[y+1]
                lines[y+1] = tmp

class Package:
    # This is something like Transform

    def populate_fields(self):
        if len(self.lines) >= 3:
            # This is a standard package when 1 header, 1 "fields" and 1 "methods"
            if self.lines[1].content != "fields":
                print("[!] Error: 'Fields' is not what it should be: " + self.lines[1].content)
            else:
                section_end = find_section(self.lines, 1, 3)
                for i in range(2, section_end + 1):
                    self.fields.append(self.lines[i])
        else:
            print("[!] Error: There are something wrong with this package: ")
            print("[!] Error: Package length: " + str(len(self.lines)))
            for line in self.lines:
                print("[!] Error: Package line : " + line.content)

    def populate_methods(self):
        if len(self.lines) >= 3:
            # This is a standard package when 1 header, 1 "fields" and 1 "methods"
            index = 1 + len(self.fields) + 1
            if self.lines[index].content != "methods":
                print("[!] Error: 'Methods' is not what it should be: " + self.lines[index].content)
            else:
                section_end = find_section(self.lines, index, 3)
                for i in range(index + 1, section_end + 1):
                    self.methods.append(self.lines[i])
        else:
            print("[!] Error: There are something wrong with this package: ")
            print("[!] Error: Package length: " + str(len(self.lines)))
            for line in self.lines:
                line.debug_display_line(True)

    def debug_display_package(self):
        print("Package: " + self.header.name + " at " + hex(self.header.offset))
        print("\tfields:")
        for line in self.fields:
            line.debug_display_line(False, True)
        print("\tmethods:")
        for line in self.methods:
            line.debug_display_line(False)

    def to_cpp_style(self):
        for line in self.fields:
            line.parse_cpp_style()

    def __init__(self, lines = []):
        self.lines = lines
        # We don't pass these three
        self.header = ""
        self.fields = []
        self.methods = []

        if len(self.lines) > 0:
            self.header = self.lines[0]
            self.populate_fields()
            self.populate_methods()

            # We need to sort it!
            bubble_sort(self.fields)

            self.to_cpp_style()

class Library:
    # This is something like Assembly-CSharp.dll

    def populate_packages(self):
        for i in range(len(self.lines)):
            if i == 0:
                # This is the first line of file, which is typically an offset
                continue
            if self.lines[i].tabs == 2:
                # This is the header of a package
                section_end = find_section(self.lines, i, 2)
                self.packages.append(Package(self.lines[i : section_end + 1]))
    
    def debug_display_library(self):
        print("Library: " + self.header.name + " at " + hex(self.header.offset))
        for package in self.packages:
            package.debug_display_package()

    def __init__(self, lines = []):
        self.lines = lines
        # We don't pass these two
        self.header = Line()
        self.packages = []

        if len(self.lines) > 0:
            self.header = self.lines[0]

            self.populate_packages()

class File:
    # The whole file, contains multiple Line

    def populate_lines(self):
        # read file, standardize and populate them
        lines = self.data.splitlines()
        # Use index to display percentage
        for i in range(len(lines)):
            print("[+] Processing " + str(math.ceil(i/len(lines)*100)) + "% of the file")
            line = lines[i]
            if line[:4] == "\t\t\t\t":
                self.lines.append(Line(4, line[4:]))
            elif line[:3] == "\t\t\t":
                self.lines.append(Line(3, line[3:]))
            elif line[:2] == "\t\t":
                self.lines.append(Line(2, line[2:]))
            elif line[:1] == "\t":
                self.lines.append(Line(1, line[1:]))
            else:
                self.lines.append(Line(0, line))
    
    def populate_libraries(self):
        for i in range(len(self.lines)):
            if i == 0:
                # This is the first line of file, which is typically an offset
                continue
            if self.lines[i].tabs == 1:
                # This is the header of a library
                section_end = find_section(self.lines, i, 1)
                self.libraries.append(Library(self.lines[i : section_end + 1]))
    
    def debug_display_lines(self):
        for line in self.lines:
            print("tabs: " + str(line.tabs) + ", offset: " + line.offset + ", name: " + line.name)

    def debug_display_libraries(self):
        for lib in self.libraries:
            lib.debug_display_library()

    def __init__(self, data):
        self.data = data
        self.lines = []
        self.libraries = []

        self.populate_lines()
        self.populate_libraries()

def main():
    _file = File(textData)
    #_file.debug_display_lines()
    _file.debug_display_libraries()

if __name__ == "__main__":
    main()