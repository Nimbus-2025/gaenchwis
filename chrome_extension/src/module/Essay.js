chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'save_dragged_essay') {
    chrome.storage.local.get(null, (result) => {
      const headers= {
        "Content-Type": "application/json",
        "access_token": result.access_token,
        "id_token": result.id_token,
        "user_id": result.user_id
      }
      if (result.post_id){
        headers["post_id"]=result.post_id
      }
      fetch(`${Config.server}/chrome_extension/essay_save`, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({
          title: request.title,
          content: request.content
        })
      }).then(async (response) => {
        const result=await response.json();
        console.log(result);
        sendResponse({ success: true, time: result.time });
      });
    });
  }
  else if(request.message === 'load_drag_essay'){
    load_drag_essay(sendResponse);
  }
  return true;
});



function load_essay(){
  chrome.storage.local.get("user_id", (result) => {
    console.log(result)
    fetch(`${Config.server}/chrome_extension/essay_load`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "access_token": result.access_token,
        "user_id": result.user_id,
      }
    }).then(async (response) => {
      console.log(response)
      const data = await response.json();
      console.log(data)
      const message='loaded'
      chrome.runtime.sendMessage({ message: message, data: data });
    });
  });
}

function load_drag_essay(sendResponse=false){
  chrome.storage.local.get(null, (result) => {
    const title = result.title;
    const content = result.content;
    const data={ title: title, content: content }
    const message='dragged'
    console.log(data);
    if (sendResponse){
      sendResponse({ success: true, data: data });
    }
    else{
      chrome.runtime.sendMessage({ message: message, data: data });
    }
  });
}