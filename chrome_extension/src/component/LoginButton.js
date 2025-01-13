import React from 'react';
import { jwtDecode } from 'jwt-decode';
import Config from './Config';
import TextButton from './TextButton';

function LoginButton() {
  const clientId=Config.clientId;
  const redirectUrl=Config.redirectUrl;
  const handleLogin = () => {
    const loginUrl=`${Config.domain}/login?client_id=${clientId}&response_type=code&scope=${Config.scope}&redirect_uri=${redirectUrl}`;
    
    chrome.identity.launchWebAuthFlow(
      { url: loginUrl, interactive: true },
      (redirectUrl) => {
        if (chrome.runtime.lastError || !redirectUrl) {
          chrome.runtime.sendMessage({ message: 'error', error: chrome.runtime.lastError});
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
    const tokenUrl = Config.tokenUrl;

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
    <TextButton title="Login" onClick={handleLogin} />
  );
};

export default LoginButton;