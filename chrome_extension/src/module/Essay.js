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

function load_drag_essay(){
  chrome.storage.local.get(null, (result) => {
    const title = result.title;
    const content = result.content;
    const data={ title: title, content: content }
    const message='dragged'
    chrome.runtime.sendMessage({ message: message, data: data });
  });
}