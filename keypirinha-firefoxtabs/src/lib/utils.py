import subprocess
import urllib.parse


def exec_stdout(args):
    """Run a command, returning stdout as a string."""

    with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
        return proc.stdout.read().decode().strip()


def launch_firefox(url):
    """Launch Firefox to switch to the given URL."""

    FIREFOX_PATH = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    # Sentinel parameter to let the extension know to switch away from this
    # tab. Must be the same as in /extension/redirect.js
    PARAM = "kpfftredirect"

    target = url

    # Add param to the URLs query string.
    if "?" in url:
        target += "&"
    else:
        target += "?"
    target += f"{PARAM}={urllib.parse.quote(url)}"

    # Navigate to the URL, with the specified sentinel param.
    exec_stdout([FIREFOX_PATH, target])
