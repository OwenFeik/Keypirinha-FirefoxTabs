import ctypes
import json
import os
import subprocess

# In the Keypirinha interpreter, lz4 is unavailable, so we check the import.
LZ4_LIB_AVAIBLE = True
try:
    import lz4.block
except ImportError:
    LZ4_LIB_AVAIBLE = False


def locate_lz4_install():
    """Returns the path of lz4, if any. Windows only."""

    with subprocess.Popen(["where", "lz4"], stdout=subprocess.PIPE) as proc:
        return proc.stdout.read().decode().splitlines()[-1]


lz4_dll = None


def load_lz4_dll():
    """Load lz4 DLL. Windows only."""

    global lz4_dll

    if lz4_dll is not None:
        return lz4_dll

    DLL_NAME = "msys-lz4-1.dll"

    exe_path = locate_lz4_install()
    dll_path = os.path.join(os.path.dirname(exe_path), "dll", DLL_NAME)

    lz4_dll = ctypes.cdll.LoadLibrary(dll_path)

    # See https://github.com/lz4/lz4/blob/dev/lib/lz4.c#L2373
    lz4_dll.LZ4_decompress_safe.restype = ctypes.c_int  # Bytes decompressed
    lz4_dll.LZ4_decompress_safe.argtypes = (
        ctypes.c_char_p,  # Source buffer
        ctypes.c_char_p,  # Destination buffer
        ctypes.c_int,  # Source size
        ctypes.c_int,  # Destination size
    )

    return lz4_dll


def lz4_decompress_safe(block):
    """Use LZ4_decompress_safe function to decompress. Windows only."""

    DST_CAPACITY = len(block) + 1024 * 1024 * 1024  # compressed + 1MB

    dst = ctypes.create_string_buffer(DST_CAPACITY)

    dll = load_lz4_dll()
    _ret = dll.LZ4_decompress_safe(
        ctypes.c_char_p(block),
        dst,
        ctypes.c_int(len(block)),
        ctypes.c_int(DST_CAPACITY),
    )

    if _ret < 0:
        # Failed to decode block.
        return ""

    return dst.value.decode()


def read_lz4_system(block):
    """Discovers installed system lz4 and uses it to decode block."""

    return lz4_decompress_safe(block)


def read_lz4_python(block):
    """Decode LZ4 block using the lz4 Python library."""

    return lz4.block.decompress(block)


def read_jsonlz4(path):
    """Load .jsonlz4 file as JSON."""

    # Remove mozilla custom file header. This is 12 bytes long, looks something
    # like:
    #
    # 6d 6f 7a 4c 7a 34 30 00 c9 e8 0f 00
    #  m  o  z  l  z  4  .  .  .  .  .  .
    MOZ_HEADER_LEN = len("mozlz4") + 6

    with open(path, "rb") as f:
        f.read(MOZ_HEADER_LEN)
        block = f.read()  # Block of LZ4

    # Use Python library if available, fall back to system install.
    if LZ4_LIB_AVAIBLE:
        text = read_lz4_python(block)
    else:
        text = read_lz4_system(block)

    return json.loads(text)
