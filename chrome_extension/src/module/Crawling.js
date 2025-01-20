chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {
    chrome.storage.local.get("post_id", (result) => {
      if (result.post_id){
        PostLoad(result.post_id);
      }
      else{
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          const url=tabs[0].url;
          if (url.includes("saramin")){
            const searchParams = new URLSearchParams(new URL(url).search);
            const hasParam = searchParams.has("rec_idx");
            if (hasParam){
              const valueParam = searchParams.get("rec_idx");
              PostLoad(valueParam);
            }
            else{
              const message='support';
              chrome.runtime.sendMessage({ message: message });
            }
          }
          else{
            const message='notsupport';
            chrome.runtime.sendMessage({ message: message });
          }
        });
      }
    });
    
    sendResponse({ message: 'Crawling Process' });
  }
  return true;
});

function PostLoad(post_id){
  chrome.storage.local.get(null, (result) => {
    fetch(`${Config.server}/chrome_extension/post_load`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "access_token": result.access_token,
        "id_token": result.id_token,
        "user_id": result.user_id,
        "post_id": post_id
      }
    }).then(async (response) => {
      const message='detected_post';
      if (response.status===404 || !response.ok ){
        chrome.runtime.sendMessage({ message: message, success: false});
      }
      else{
        const data = await response.json();
        chrome.runtime.sendMessage({ message: message, success: true, post_id: post_id, data: data });  
      }
      });
  });
}