import os
import time

from . import tabs


class Cacher:
    def __init__(self):
        self.last_update = 0
        self.session_files = tabs.session_files()
        self.tabs_by_file = {}

    def update(self):
        for file in self.session_files:
            if os.path.getmtime(file) > self.last_update:
                self.tabs_by_file[file] = tabs.load_session_tabs(file)
        self.last_update = time.time()

    def all_tabs(self, update=True):
        if update:
            self.update()

        all_tabs = set()
        for tab_list in self.tabs_by_file.values():
            all_tabs.update(tab_list)

        return all_tabs
