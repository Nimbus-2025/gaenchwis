import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import logo from './images/cloud.png'; // 로고 이미지 경로
import backgroundGif from './images/background.gif'; // 배경 GIF 경로
import { jwtDecode } from 'jwt-decode';
import LoginButton from './login-service/LoginButton';

const FirstPage = () => {
    const navigate = useNavigate();
    const handleLogoClick = () =>{
        navigate('/MyPage1');
    }
  

const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // 구글 로그인 성공 처리 로직
      const decoded = jwtDecode(credentialResponse.credential);

      // 액세스 토큰을 로컬 스토리지에 저장
      const accessToken = credentialResponse.credential; // JWT 형식의 액세스 토큰
      localStorage.setItem('accessToken', accessToken);

      // 리프레시 토큰은 구글 API에서 직접 요청해야 하므로, 서버에서 처리하는 것이 일반적입니다.
      // 서버에 요청하여 리프레시 토큰을 받아오는 로직을 추가할 수 있습니다.
      const userData = {
        userId: decoded.sub,
        name: decoded.name,
        email: decoded.email,
        profileImage: decoded.picture,
        accessToken: accessToken,
    };
        localStorage.setItem('user', JSON.stringify(userData));

        navigate('/MyPage1');
    } catch (error) {
      console.error('구글 로그인 처리 중 오류:', error);
      alert('로그인 처리 중 오류가 발생했습니다.');
    }
  };
const handleLoginFailure = () => {
    console.error('구글 로그인 실패');
    alert('로그인에 실패했습니다.');
  };

const login = (data) => {
    // 예시: 사용자 정보를 로컬 스토리지에 저장
    localStorage.setItem('user', JSON.stringify(data));
  };

const PageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url(${backgroundGif});
  background-size: cover;
  background-position: center;
  padding-top: 50px;
`;

const Logo = styled.img`
  width: 500px;
  height: 600px;
  margin-top: 20px;
  cursor: pointer;
`;
const LoginButtonWrapper = styled.div`
  margin-top: 20px; /* 로고와 버튼 사이의 간격 */
`;
return (
    <GoogleOAuthProvider clientId="800144464912-bjdvo0b4vru9sp0i1segrktsgbk9kngu.apps.googleusercontent.com">
    <PageWrapper>
      <Logo src={logo} alt="Logo" onClick={handleLogoClick}/>
      <LoginButtonWrapper>
        <LoginButton />
       
       </LoginButtonWrapper>
    </PageWrapper>
     </GoogleOAuthProvider>
  );
};

export default FirstPage;