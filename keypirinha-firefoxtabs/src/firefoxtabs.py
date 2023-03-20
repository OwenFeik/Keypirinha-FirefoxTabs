# Keypirinha launcher (keypirinha.com)

import time

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

from .lib import tabs, utils


class FirefoxTabs(kp.Plugin):
    """
    Switches to open Firefox tabs.
    """

    ITEM_TEMPLATE = "Tab \u2022 {}"
    FUZZY_TRESH = 400

    def __init__(self):
        super().__init__()
        self.cacher = tabs.Cacher()

    def on_start(self):
        self.cacher.update()

    def on_catalog(self):
        self.cacher.update()
        self.set_catalog([self._create_item("Tab", "Switch to an open tab")])

    def on_suggest(self, user_input, items_chain):
        suggestions = []
        open_tabs = self.cacher.all_tabs()

        for tab in open_tabs:
            (title, url) = tab
            if (
                len(user_input) == 0
                or kpu.fuzzy_score(user_input, title) > FirefoxTabs.FUZZY_TRESH
                or kpu.fuzzy_score(user_input, url) > FirefoxTabs.FUZZY_TRESH
            ):
                suggestion = self._create_item_from_tab(tab)
                suggestions.append(suggestion)

        if suggestions:
            self.set_suggestions(suggestions)

    def on_execute(self, item, action):
        if item:
            utils.launch_firefox(item.target())

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass

    def on_events(self, flags):
        pass

    def _create_item_from_tab(self, tab):
        (title, url) = tab
        item = self._create_item(
            FirefoxTabs.ITEM_TEMPLATE.format(title), url, target=url
        )
        return item

    def _create_item(self, label, short_desc, target="tab"):
        return self.create_item(
            category=kp.ItemCategory.URL,
            label=label,
            short_desc=short_desc,
            target=target,
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.NOARGS,
        )
