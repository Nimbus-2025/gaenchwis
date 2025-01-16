importScripts(
  'Drag.js', 
  'Page.js', 
  'Crawling.js',
  'Login.js',
  'Logout.js',
  'Session.js',
  'Config.js'
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
      chrome.storage.local.get("user_id", (result) => {
        console.log(result);
        fetch(`${Config.server}/user_load`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            userId: result.user_id,
            access_token: refresh.tokens.access_token,
            id_token: refresh.tokens.id_token
          })
        }).then(async (response) => {
          const userData=await response.json();
          console.log(userData);

          const loginData = {
            phone: userData.phone,
            email: userData.email,
            name: userData.name,
            id_token: refresh.tokens.id_token,
            access_token: refresh.tokens.access_token,
            user_id: result.user_id
          }
          sendResponse({ success: true, data: loginData });
        });
      });
    }
    else {
      sendResponse({ success: false });
    }
  }
  return true;
});
