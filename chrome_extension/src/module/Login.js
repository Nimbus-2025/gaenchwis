chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'login_data'){
    console.log(request);
    fetch(`${Config.server}/user_load`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "access_token": request.token.access_token,
        "id_token": request.token.id_token,
        "user_id": request.data["cognito:username"]
      }
    }).then(async (response) => {
      const userData=await response.json();
      console.log(userData);
      const loginData = {
        phone: userData.phone,
        email: userData.email,
        name: userData.name,
        id_token: request.token.id_token,
        access_token: request.token.access_token,
        refresh_token: request.token.refresh_token,
        user_id: request.data["cognito:username"]
      }

      chrome.storage.local.set(loginData);
      sendResponse({ message: 'User data saved' });
      chrome.runtime.sendMessage({ message: 'login_success', name: userData.name});
    });
  }
  else if (request.message === 'userdata_load'){
    chrome.storage.local.get(null, (result)=>{
      fetch(`${Config.server}/user_load`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "access_token": result.access_token,
          "id_token": result.id_token,
          "user_id": result.user_id
        }
      }).then(async (response) => {
        const userData=await response.json();
        console.log(userData);
        const loginData = {
          phone: userData.phone,
          email: userData.email,
          name: userData.name
        }
  
        chrome.storage.local.set(loginData);
        sendResponse({ message: 'User data loaded', name: userData.name});
      });
    });
  }
  return true;
});