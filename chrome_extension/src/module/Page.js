let page='page_main'

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if ((page === 'page_saveessay' && request.message === 'save_to_page_main') || request.message === 'page_main') {
    chrome.runtime.sendMessage({ message: 'move_page_main' });
    page=request.message;
    sendResponse({ message: 'Page Home' });
  }
  else if (request.message === 'page_detectessay') {
    chrome.runtime.sendMessage({ message: 'move_page_detectessay' });
    page=request.message;
    sendResponse({ message: 'Page DetectEssay' });
  }
  else if (request.message === 'page_loadessay') {
    chrome.runtime.sendMessage({ message: 'move_page_loadessay' });
    setTimeout(() => {
      data="abc"
      chrome.runtime.sendMessage({ message: 'loaded', data: data },
        (response) => {
          console.log(response);
        }
      );
    }, 100);
    page=request.message;
    sendResponse({ message: 'Page LoadEssay' });
  }
  else if (request.message === 'page_saveessay') {
    chrome.runtime.sendMessage({ message: 'move_page_saveessay' });
    setTimeout(() => {
      chrome.runtime.sendMessage({ message: 'saved' },
        (response) => {
          console.log(response);
        }
      );
    }, 100);
    page=request.message;
    sendResponse({ message: 'Page SaveEssay' });
  }
  return true;
});