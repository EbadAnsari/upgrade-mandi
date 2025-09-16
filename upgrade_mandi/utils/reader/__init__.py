import ctypes
from os.path import join
from pathlib import Path

# Get the current file path for the DLL location
# because the working directory may vary
path = Path(__file__)

# Load the DLL
dll = ctypes.CDLL(join(path.parent, "reader.dll"))


# Define Table struct matching Rust
class Table(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_char_p)),
        ("rows", ctypes.c_size_t),
        ("cols", ctypes.c_size_t),
    ]


# Define function signatures
dll.read_excel.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
dll.read_excel.restype = ctypes.POINTER(Table)

# free table function pointer to free the memory that rust allocated the memory
dll.free_table.argtypes = [ctypes.POINTER(Table)]
dll.free_table.restype = None
