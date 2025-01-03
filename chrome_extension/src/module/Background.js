chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "dragTitle",
    title: "자기소개서 문항 저장",
    contexts: ["selection"]
  });
  chrome.contextMenus.create({
    id: "dragContent",
    title: "자기소개서 내용 저장",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "dragTitle" || info.menuItemId === "dragContent") {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: (type, content) => {
        chrome.runtime.sendMessage({ message: type, content: content });
      },
      args: [info.menuItemId,info.selectionText]
    });
  }
});

const page='page_main'

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: (saramin, jobkorea, essay) => {
          const url = window.location.href;
          console.log(url)
          if (url.includes(essay) && (url.includes(saramin) || url.includes(jobkorea))){
            let pageContent = document.documentElement.innerHTML;
            chrome.runtime.sendMessage({ message: 'detected_essay', content: pageContent });
          }
          else {
            chrome.runtime.sendMessage({ message: 'notsupport' });
          }
        },
        args: [
          "",//"saramin.co.kr"
          "",//"jobkorea.co.kr"
          ""
        ]
      });
    });
  }

  if (request.message === 'page_main') {
    if (page === 'page_saveessay'){
      chrome.runtime.sendMessage({ message: 'move_page_main' });
    }
    page=request.message
  }
  if (request.message === 'page_detectessay') {
    chrome.runtime.sendMessage({ message: 'move_page_detectessay' });
    page=request.message
  }
  if (request.message === 'page_loadessay') {
    chrome.runtime.sendMessage({ message: 'move_page_loadessay' });
    setTimeout(() => {
      data="abc"
      chrome.runtime.sendMessage({ message: 'loaded', data: data },
        (response) => {
          console.log(response);
        }
      );
    }, 100);
    page=request.message
  }
  if (request.message === 'page_saveessay') {
    chrome.runtime.sendMessage({ message: 'move_page_saveessay' });
    setTimeout(() => {
      chrome.runtime.sendMessage({ message: 'saved' },
        (response) => {
          console.log(response);
        }
      );
    }, 100);
    page=request.message
  }
});