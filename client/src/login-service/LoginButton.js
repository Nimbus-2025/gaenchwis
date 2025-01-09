import React from 'react';

function LoginButton() {
  const loginRedirect = () => {
    const domain="https://gaenchwis.auth.ap-northeast-2.amazoncognito.com";
    const clientId="72m8d04kfkj5osdsvjtclp2cbb"
    const scope="email+openid+profile"
    const redirectUrl="http://localhost:3000/callback"; //"https://gaenchwis.click/callback";
    const loginUrl=`${domain}/login?client_id=${clientId}&response_type=code&scope=${scope}&redirect_uri=${redirectUrl}`;
    
    window.location.href = loginUrl;
  }
  return (
    <button onClick={loginRedirect}>로그인</button>
  );
};

export default LoginButton;