importScripts(
  'Drag.js', 
  'Page.js', 
  'Crawling.js',
  'SSO.js',
  'Login.js'
)

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'error'){
    console.log(request.error)
    sendResponse({ message: 'Error received' });
  }
  return true;
});