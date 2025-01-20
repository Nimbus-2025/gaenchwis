window.addEventListener("message", (event) => {
  if (event.source !== window || !event.data.type) return;
  if (event.data.type === "web_login_request"){
    chrome.runtime.sendMessage({ message: 'web_login_request' }, (response) => {
      chrome.runtime.sendMessage({ message: 'log', log: response});
      window.postMessage({ type: "web_login_response", ...response }, "*");
    });
  }
});