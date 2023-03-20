"""
Script to query open Firefox tabs based on a search string. Tabs returned might
be slightly out of date as they're loaded from the session store file on disk.
"""

import difflib
import os
import time
import urllib.parse

from . import lz4


class Cacher:
    """Caches session files and tab lists to save effort."""

    def __init__(self):
        self.last_update = 0
        self.tabs_by_file = {}

        # Get list of session files
        self.update_sessions()

    def update_sessions(self):
        """Reloads session list."""

        self.session_files = session_files()

    def update_tabs(self):
        """Reloads tabs from sessions which have changed since last update."""
        
        for file in self.session_files:
            if os.path.getmtime(file) > self.last_update:
                self.tabs_by_file[file] = load_session_tabs(file)
        self.last_update = time.time()

    def update(self):
        """Reloads sessions and tabs which have changed since last update."""
        
        self.update_sessions()
        self.update_tabs()

    def all_tabs(self, update=True):
        """List all known open tabs. If update is True, reloads the list."""
        
        if update:
            self.update_tabs()

        all_tabs = set()
        for tab_list in self.tabs_by_file.values():
            all_tabs.update(tab_list)

        return all_tabs


def tab_info(data):
    """From a sessionstore JSON file, return a list of tabs [(title, url)]."""

    tabs = []
    for window in data["windows"]:
        for tab in window["tabs"]:
            for entry in tab["entries"]:
                tabs.append((entry["title"], entry["url"]))
    return tabs


def diff_value(query, title, url):
    """Sum of difflib ratios for title and various url parts."""

    parts = urllib.parse.urlparse(url)

    matcher = difflib.SequenceMatcher()
    matcher.set_seq1(query)

    strings = [title, url, parts.hostname, parts.path]

    total = 0
    for string in strings:
        if string:
            matcher.set_seq2(string)
            total += matcher.ratio()

    return total


def value(query, tab):
    """A numeric closeness score for a given query, pair."""

    MIN_LENGTH = 3  # Minimum exact string match length.
    EXACT_VALUE = 3  # Score for finding an exact match.
    RATIO_COEFF = 1  # Multiplied by diff_value result.

    (title, url) = tab

    query = query.lower()
    title = title.lower()
    url = url.lower()

    total = 0

    if len(query) >= MIN_LENGTH:
        if query in title:
            total += EXACT_VALUE
        if query in url:
            total += EXACT_VALUE

    total += diff_value(query, title, url) * RATIO_COEFF

    return total


def suggest_tabs(tabs, query):
    """Suggest tabs from data which match query well."""

    THRESHOLD = 1.5  # Minimum value to return.
    filter(lambda tab: value(query, tab) > THRESHOLD, tabs)


def session_files():
    """Returns a list of discovered sessionstore files. Windows only."""

    FILENAME = "sessionstore.jsonlz4"
    FALLBACK = "sessionstore-backups/recovery.jsonlz4"

    if os.name == "nt":
        profile_folder = os.path.join(
            os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles"
        )
    else:
        profile_folder = os.path.join(
            os.path.expanduser("~"), ".mozilla", "firefox"
        )

    files = []
    for profile in os.listdir(profile_folder):
        primary = os.path.join(profile_folder, profile, FILENAME)
        if os.path.isfile(primary):
            files.append(primary)

        fallback = os.path.join(profile_folder, profile, FALLBACK)
        if os.path.isfile(fallback):
            files.append(fallback)

    return files


def load_session_tabs(path):
    """Load the list of tabs from a sessionstor file path."""

    data = lz4.read_jsonlz4(path)
    return tab_info(data)


def load_all_tabs():
    """Load all tabs from sessionstore files."""

    tabs = set()
    for file in session_files():
        tabs.update(load_session_tabs(file))
    return tabs


def handle_query(query, nmax=10):
    """Search all tabs with a search query."""

    return sorted(
        load_all_tabs(),
        key=lambda tab: -value(query, tab),
    )[:nmax]


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        query = sys.argv[1]
        suggested = suggest_tabs(load_all_tabs(), query)
    else:
        suggested = load_all_tabs()

    for i, tab in enumerate(suggested, 1):
        print(f"[{i}]", tab)
