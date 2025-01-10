importScripts("Config.js");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "refresh_tokens") {
    sendResponse({ success: refreshToken() });
  }
  return true;
});

async function refreshTokens() {
  try {
    const refreshToken = await new Promise((resolve) => {
      chrome.storage.local.get("refresh_token", (result) => {
        resolve(result.refresh_token);
      });
    });
    const response = await fetch(Config.tokenUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        client_id: Config.cliendId,
        refresh_token: refreshToken
      }),
    });

    if (!response.ok) {
      return {status: false, response: response};
    }

    const tokens = await response.json();

    return {status: true, token: tokens};
  } catch (error) {
    return {status: false, error: error};
  }
}
