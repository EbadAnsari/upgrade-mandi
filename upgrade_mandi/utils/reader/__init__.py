import ctypes
from os.path import join
from pathlib import Path

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

dll.free_table.argtypes = [ctypes.POINTER(Table)]
dll.free_table.restype = None
