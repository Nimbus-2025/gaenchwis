chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type === "refresh_tokens") {
    const response = await refreshToken()
    sendResponse({ ...response });
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
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": Config.redirectUrl
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        client_id: Config.clientId,
        refresh_token: refreshToken
      }),
    });
    if (!response.ok) {
      return {status: false, response: response};
    }
    else{
      const tokens = await response.json();
      return {status: true, tokens: tokens};
    }
  } catch (error) {
    return {status: false, error: error};
  }
}