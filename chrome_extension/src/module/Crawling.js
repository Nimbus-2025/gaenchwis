chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: Crawling,
        args: [
          "",//"saramin.co.kr"
          "",//"jobkorea.co.kr"
          "abcde"
        ]
      });
    });
    sendResponse({ message: 'Crawling Process' });
  }
  return true;
});

function Crawling(saramin, jobkorea, essay){
  const url = window.location.href;
  let message=""
  let data=""
  if (url.includes(essay) && (url.includes(saramin) || url.includes(jobkorea))){
    message='detected_essay'
    const pageContent = document.documentElement.innerHTML;
    data=pageContent
    chrome.runtime.sendMessage({ message: message, data: data });
  }
  else {
    message='notsupport'
    chrome.storage.local.get(null, (result) => {
      const title = result.title || [];
      const content = result.content || [];
      data={ title: title, content: content }
      chrome.runtime.sendMessage({ message: message, data: data });
    });
  }
}

//function PreProcessing(){}