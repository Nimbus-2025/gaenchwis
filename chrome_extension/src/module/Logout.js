const Logout = () => {
  chrome.storage.local.remove('email');
  chrome.storage.local.remove('name');
  chrome.storage.local.remove('access_token');
  chrome.storage.local.remove('refresh_token');
  chrome.storage.local.remove('id_token');
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'logout'){
    console.log(request)
    Logout();
    sendResponse({ message: 'Logout' });
  }
  return true;
});