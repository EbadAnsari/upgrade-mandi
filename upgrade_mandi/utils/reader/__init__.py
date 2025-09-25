import ctypes
from os.path import join as __join
from pathlib import Path as __Path

# Get the current file path for the DLL location
# because the working directory may vary
path = __Path(__file__)

test = True
whole_path = (
    __join(path.parent, "reader", "dll", "release", "reader.dll")
    if test
    else __join(path.parent, "reader.dll")
)

# Load the DLL
dll = ctypes.CDLL(whole_path)


class Cell(ctypes.Structure):
    _fields_ = [("value", ctypes.c_char_p), ("kind", ctypes.c_int8)]


# Define Table struct matching Rust
class Table(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(Cell if test else ctypes.c_char_p)),
        ("rows", ctypes.c_size_t),
        ("cols", ctypes.c_size_t),
    ]


# Define function signatures
dll.read_excel.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
dll.read_excel.restype = ctypes.POINTER(Table)

# free table function pointer to free the memory that rust allocated the memory
dll.free_table.argtypes = [ctypes.POINTER(Table)]
dll.free_table.restype = None
