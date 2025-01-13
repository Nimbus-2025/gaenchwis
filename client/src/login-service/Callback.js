import React, { useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import Config from './Config';

function Callback() {
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    if (code) {
      console.log('Authorization Code:', code);
      exchangeCodeForToken(code);
    } else {
      console.error('No authorization code found.');
    }
  }, []);

  const exchangeCodeForToken = async (authorizationCode) => {
    const tokenUrl = Config.tokenUrl;
    const clientId = Config.clientId;
    const redirectUri = Config.redirectUrl;

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
          redirect_uri: redirectUri,
        }),
      });

      const data = await response.json();
      const idTokenPayload = jwtDecode(data.id_token);

      const user = {
        email: idTokenPayload.email,
        name: idTokenPayload.name,
        access_token: data.access_token,
        id_token: data.id_token
      }
      sessionStorage.setItem('user', JSON.stringify(user));
      window.location.href = '/';
    } catch (error) {
      console.error('Failed to exchange code for token:', error);
    }
  };

  return <div>Loading...</div>;
};

export default Callback;