import subprocess


def exec_stdout(args):
    """Run a command, returning stdout as a string."""

    with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
        return proc.stdout.read().decode().strip()

def launch_firefox(url):
    """Launch Firefox to switch to the given URL."""

    FIREFOX_PATH = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    SWITCHER_URL = "owen.feik.xyz/redirect?url={}"


    exec_stdout([FIREFOX_PATH, SWITCHER_URL.format(url)])
