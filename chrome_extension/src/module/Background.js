importScripts(
  'Drag.js', 
  'Page.js', 
  'Crawling.js',
  'Login.js',
  'Logout.js',
  'Session.js'
)

chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.message === 'error'){
    console.log(request.error)
    sendResponse({ message: 'Error received' });
  }
  else if (request.message === "web_login_request") {
    const refresh=await refreshTokens();
    console.log(refresh);
    if (refresh.status){
      chrome.storage.local.set({
        access_token: refresh.tokens.access_token,
        id_token: refresh.tokens.id_token,
      });
      chrome.storage.local.get(null, (result) => {
        const loginData = {
          email: result.email,
          name: result.name,
          id_token: refresh.tokens.id_token,
          access_token: refresh.tokens.access_token
        }
        sendResponse({ success: true, data: loginData });
      });
    }
    else {
      sendResponse({ success: false });
    }
  }
  return true;
});
