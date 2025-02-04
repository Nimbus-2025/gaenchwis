const Logout = () => {
  chrome.storage.local.remove('phone');
  chrome.storage.local.remove('email');
  chrome.storage.local.remove('name');
  chrome.storage.local.remove('access_token');
  chrome.storage.local.remove('refresh_token');
  chrome.storage.local.remove('id_token');
  chrome.storage.local.remove('user_id');
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'logout'){
    Logout();
    sendResponse({ message: 'Logout' });
    chrome.runtime.sendMessage({ message: 'logout_success' });
  }
  return true;
});