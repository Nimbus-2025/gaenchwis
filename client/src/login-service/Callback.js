import React, { useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import Config from '../api/Config';
import Api from '../api/api';

function Callback() {
  let first = true;
  useEffect(() => {
    if (first) {
      first = !first;
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');

      if (code) {
        exchangeCodeForToken(code);
      } else {
        console.error('No authorization code found.');
      }
    }
  }, []);

  const exchangeCodeForToken = async (authorizationCode) => {
    const tokenUrl = Config.tokenUrl;
    const clientId = Config.clientId;
    const redirectUri = Config.redirectUrl;

    fetch(tokenUrl, {
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
    }).then(async (response) => {
        const data = await response.json();
        const idTokenPayload = jwtDecode(data.id_token);
        const userId = idTokenPayload['cognito:username'];

        const user = {
          access_token: data.access_token,
          id_token: data.id_token,
          user_id: userId,
        };
        sessionStorage.setItem('user', JSON.stringify(user));

        const userData = await Api(`${Config.server}/user_load`, 'GET');

        user["email"]=userData.email;
        user["name"]=userData.name;
        user["phone"]=userData.phone;
        sessionStorage.setItem('user', JSON.stringify(user));
        window.location.href = '/MyPage1';
      })
      .catch((error) => {
        console.error('Failed to exchange code for token:', error);
      });
  };

  return <div>Loading...</div>;
}

export default Callback;
