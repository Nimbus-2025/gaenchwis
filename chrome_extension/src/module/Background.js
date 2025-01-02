chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {
    chrome.scripting.executeScript({
      target: { tabId: sender.tab.id },
      function: () => {
        let pageContent = document.documentElement.innerHTML;
        console.log(pageContent);
        chrome.runtime.sendMessage({ message: 'detected_essay', content: pageContent });
      }
    });
  }
});
