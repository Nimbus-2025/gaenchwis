chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'page_main') {
    chrome.runtime.sendMessage({ message: 'move_page_main' });
    sendResponse({ message: 'Page Home' });
  }
  else if (request.message === 'page_detectpost') {
    chrome.runtime.sendMessage({ message: 'move_page_detectpost' });
    sendResponse({ message: 'Page DetectPost' });
  }
  else if (request.message === 'page_loadessay') {
    chrome.runtime.sendMessage({ message: 'move_page_loadessay' });
    setTimeout(() => {
      load_drag_essay()
      load_essay();
    }, 100);
    sendResponse({ message: 'Page LoadEssay' });
  }
  return true;
});