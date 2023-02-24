const HOSTNAME = "owen.feik.xyz";
const PATH = "redirect";

browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    let url = new URL(tab.url);
    if (
        url.hostname == HOSTNAME
        && new RegExp(`\/${PATH}.*`).test(url.pathname)
    ) {
        let tabUrl = url.searchParams.get("url");
        browser.tabs.query({ url: tabUrl }).then(console.log);
    }
});
