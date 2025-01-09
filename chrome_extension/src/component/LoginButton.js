import React from 'react';
import { jwtDecode } from 'jwt-decode';

function LoginButton() {
  const clientId="2utkst2075aft2udaumgb4n156"
  const redirectUrl=`https://${chrome.runtime.id}.chromiumapp.org`;
  const handleLogin = () => {
    const domain="https://gaenchwis.auth.ap-northeast-2.amazoncognito.com";
    const scope="email openid profile"
    const loginUrl=`${domain}/login?client_id=${clientId}&response_type=code&scope=${scope}&redirect_uri=${redirectUrl}`;
    
    chrome.identity.launchWebAuthFlow(
      { url: loginUrl, interactive: true },
      (redirectUrl) => {
        if (chrome.runtime.lastError || !redirectUrl) {
          chrome.runtime.sendMessage({ message: 'error', error: chrome.runtime.lastError });
          return;
        }
    
        const urlParams = new URLSearchParams(new URL(redirectUrl).search);
        const code = urlParams.get('code');

        if (code) {
          console.log('Authorization Code:', code);
          exchangeCodeForToken(code);
        } else {
          console.error('No authorization code found.');
        }
    });
  }
  const exchangeCodeForToken = async (authorizationCode) => {
    const tokenUrl = "https://gaenchwis.auth.ap-northeast-2.amazoncognito.com/oauth2/token";

    try {
      const response = await fetch(tokenUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          grant_type: 'authorization_code',
          client_id: clientId,
          code: authorizationCode,
          redirect_uri: redirectUrl,
        }),
      });

      const data = await response.json();
      const idTokenPayload = jwtDecode(data.id_token);

      chrome.runtime.sendMessage({ message: 'login_data', data: idTokenPayload, token: data });
    } catch (error) {
      console.error('Failed to exchange code for token:', error);
    }
  };

  return (
    <button onClick={handleLogin}>로그인</button>
  );
};

export default LoginButton;