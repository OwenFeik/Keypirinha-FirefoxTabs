const HOSTNAME = "owen.feik.xyz";
const PATH = "redirect";

// Whenever HOSTNAME/PATH is opened, close it and activate the tab specified by
// the parameter url=TAB_URL_TO_SWITCH_TO, if any.
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    let url = new URL(tab.url);
    if (
        url.hostname == HOSTNAME
        && new RegExp(`\/${PATH}.*`).test(url.pathname)
    ) {
        let tabUrl = url.searchParams.get("url");
        browser.tabs.query({}).then(tabs => tabs.forEach(tab => {
            if (tab.url == tabUrl) {
                browser.tabs.update(tab.id, { active: true });
                browser.windows.update(tab.windowId, { focused: true });
            }
        }));
        browser.tabs.remove(tabId);
    }
});
