chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'post-applies') {
    chrome.storage.local.get(null, (result) => {
      const headers= {
        "Content-Type": "application/json",
        "access_token": result.access_token,
        "id_token": result.id_token,
        "user_id": result.user_id,
        "post_id": request.post_id
      }
      const body={
        post_name: request.post_name,
        deadline_date: request.deadline_date
      }
      if (request.loadessay){
        body["title"]=result.title;
        body["content"]=result.content;
      }
      fetch(`${Config.server}/chrome_extension/post_applies`, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(body)
      }).then(async (response) => {
        const result=await response.json();
        console.log(result);
        if (request.loadessay){
          await chrome.storage.local.remove("title");
          await chrome.storage.local.remove("content");
        }
        await chrome.storage.local.remove("post_id");
        sendResponse({ success: true, data: result.data});
      });
    });
  }
  return true;
});