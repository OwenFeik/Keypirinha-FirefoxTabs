const PARAM = "kpfftredirect";
const REGEX = new RegExp(`(\\?|&)${PARAM}=go`)

// Whenever a tab is opened, if PARAM is present in URL params, attempt to find
// a tab with the URL specified by PARAM and switch to it. If one is found,
// close the current tab, otherwise leave it open.
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    let match = REGEX.exec(tab.url);
    if (match) {
        tabUrl = tab.url.replaceAll(match[0], "");
        browser.tabs.query({}).then(tabs => tabs.forEach(tab => {
            if (tab.url == tabUrl) {
                browser.tabs.update(tab.id, { active: true });
                browser.windows.update(tab.windowId, { focused: true });
                browser.tabs.remove(tabId);
            }
        }));
    }    
});
