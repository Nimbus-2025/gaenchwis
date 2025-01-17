chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'crawling') {

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const url=tabs[0].url
      if (url.includes("saramin")){
        const searchParams = new URLSearchParams(new URL(url).search);
        const hasParam = searchParams.has("rec_idx");
        if (hasParam){
          const valueParam = searchParams.get("rec_idx");
          chrome.storage.local.get(null, (result) => {
            console.log(result)
            console.log(valueParam)
            fetch(`${Config.server}/chrome_extension/post_load`, {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                "access_token": result.access_token,
                "id_token": result.id_token,
                "user_id": result.user_id,
                "post_id": valueParam
              }
            }).then(async (response) => {
              const data = await response.json();
              console.log(data)
              const message='detect_post'
              chrome.runtime.sendMessage({ message: message, data: data.body });
            });
          });
        }
        else{
          const message='support'
          chrome.runtime.sendMessage({ message: message });
        }
      }
      else{
        const message='notsupport'
        chrome.storage.local.get(null, (result) => {
          const title = result.title || [];
          const content = result.content || [];
          const data={ title: title, content: content }
          chrome.runtime.sendMessage({ message: message, data: data });
        });
      }
    });
    sendResponse({ message: 'Crawling Process' });
  }
  return true;
});