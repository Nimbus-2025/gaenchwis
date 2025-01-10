chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'login_data'){
    console.log(request)
    chrome.storage.local.set({ 
      email: request.data.email,
      name: request.data.name,
      access_token: request.token.access_token,
      refresh_token: request.token.refresh_token,
      id_token: request.token.id_token
    });
    sendResponse({ message: 'User data saved' });
  }
  return true;
});