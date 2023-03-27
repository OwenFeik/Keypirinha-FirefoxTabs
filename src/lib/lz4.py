import ctypes
import io
import json
import os
import urllib.request
import zipfile

from . import utils

# In the Keypirinha interpreter, lz4 is unavailable, so we check the import.
LZ4_LIB_AVAIBLE = True
try:
    import lz4.block
except ImportError:
    LZ4_LIB_AVAIBLE = False

DATA_DIR = os.path.join(
    os.getenv("APPDATA"), "Keypirinha", "PackageData", "FirefoxTabs"
)
DLL_NAME = "msys-lz4-1.dll"
DLL_FILE = os.path.join(DATA_DIR, DLL_NAME)


def download_lz4_dll():
    """Using the GitHub API, download the latest version of the DLL."""

    # https://docs.github.com/en/rest/releases/releases#get-the-latest-release
    URL = "https://api.github.com/repos/lz4/lz4/releases/latest"

    with urllib.request.urlopen(URL) as resp:
        data = json.loads(resp.read().decode())

    # 32 bit windows has 4 word pointers, 64 bit 8 word.
    # https://stackoverflow.com/a/1406210
    is_32_bit = ctypes.sizeof(ctypes.c_void_p) == 4
    goal_asset_prefix = "lz4_win32" if is_32_bit else "lz4_win64"

    for asset in data["assets"]:
        if asset["name"].startswith(goal_asset_prefix):
            zipurl = asset["url"]
            break
    else:
        print("Failed to find win64 lz4.")

    # https://docs.github.com/en/rest/releases/assets#get-a-release-asset
    request = urllib.request.Request(zipurl)
    request.add_header("accept", "application/octet-stream")
    with urllib.request.urlopen(request) as resp:
        lz4zip = zipfile.ZipFile(io.BytesIO(resp.read()))

    # Create data dir, don't worry if it already exists.
    try:
        os.makedirs(DATA_DIR)
    except Exception:
        pass

    # Extract DLL there
    with open(DLL_FILE, "wb") as f:
        f.write(lz4zip.read("dll/" + DLL_NAME))


def locate_lz4_install():
    """Returns the path of lz4, if found in PATH. Windows only."""

    return utils.exec_stdout(["where", "lz4.exe"])


def ensure_lz4_install():
    """Checks for an existing lz4 DLL install or downloads it. Returns path."""

    # First try previously downloaded DLL
    if os.path.isfile(DLL_FILE):
        return DLL_FILE

    # Fallback to checking PATH
    exe_path = locate_lz4_install()
    dll_path = os.path.join(os.path.dirname(exe_path), "dll", DLL_NAME)
    if os.path.isfile(dll_path):
        return dll_path

    # Finally download the DLL ourselves
    download_lz4_dll()
    return DLL_FILE


lz4_dll = None


def load_lz4_dll():
    """Load lz4 DLL. Windows only."""

    global lz4_dll

    if lz4_dll is not None:
        return lz4_dll

    dll_path = ensure_lz4_install()
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

    # Failed to decode block.
    if _ret < 0:
        raise RuntimeError("Failed to decompress block.")

    # Sometimes there is a few random characters after the end of the JSON.
    # Strip remove these.
    data = dst.value.decode()
    i = len(data)
    while data[i - 1] != "}":
        i -= 1
    return data[:i]


def read_lz4_system(block):
    """Discovers installed system lz4 and uses it to decode block."""

    if os.name != "nt":
        raise NotImplementedError("Unsupported OS.")

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
