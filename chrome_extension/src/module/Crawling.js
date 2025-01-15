chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {
    const essay="abcded";
    const saramin="";
    const jobkorea="";
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url=tabs[0].url
      if (url.includes(essay) && (url.includes(saramin) || url.includes(jobkorea))){
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          function: Crawling
        });
      }
      else{
        const message='notsupport'
        chrome.storage.local.get(null, (result) => {
          const title = result.title || [];
          const content = result.content || [];
          const data={ title: title, content: content }
          chrome.runtime.sendMessage({ message: message, data: data });
        });
      }
    });
    sendResponse({ message: 'Crawling Process' });
  }
  return true;
});

function Crawling(){
  message='detected_essay'
  const pageContent = document.documentElement.innerHTML;
  data=pageContent
  chrome.runtime.sendMessage({ message: message, data: data });
}

//function PreProcessing(){}