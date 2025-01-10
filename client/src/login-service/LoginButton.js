import React from 'react';
import Config from './Config';

function LoginButton() {
  const loginRedirect = () => {
    const loginUrl=`${Config.domain}/login?client_id=${Config.clientId}&response_type=code&scope=${Config.scope}&redirect_uri=${Config.redirectUrl}`;
    
    window.location.href = loginUrl;
  }
  return (
    <button onClick={loginRedirect}>로그인</button>
  );
};

export default LoginButton;