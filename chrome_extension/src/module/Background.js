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

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: (saramin, jobkorea, essay) => {
          const url = window.location.href;

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
  if (request.message === 'loadessay') {
    
  }
  if (request.message === 'saveessay') {
    
  }

  if (request.message === 'page_main') {
    chrome.runtime.sendMessage({ message: 'move_page_main' });
  }
  if (request.message === 'page_detectessay') {
    chrome.runtime.sendMessage({ message: 'move_page_detectessay' });
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
    }, 500);
  }
  if (request.message === 'page_saveessay') {
    chrome.runtime.sendMessage({ message: 'move_page_saveessay' });
    setTimeout(() => {
      chrome.runtime.sendMessage({ message: 'saved' },
        (response) => {
          console.log(response);
        }
      );
    }, 500);
  }
});