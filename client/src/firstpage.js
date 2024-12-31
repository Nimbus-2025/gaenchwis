import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import logo from './images/cloud.png'; // 로고 이미지 경로
import backgroundGif from './images/background.gif'; // 배경 GIF 경로
import { jwtDecode } from 'jwt-decode';

const FirstPage = () => {
    const navigate = useNavigate();
    const handleLogoClick = () =>{
        navigate('/mainpage');
    }
  

const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // 구글 로그인 성공 처리 로직
      const decoded = jwtDecode(credentialResponse.credential);
      console.log('구글 로그인 사용자 정보:', decoded);

      const response = await fetch('http://localhost:5000/auth/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          credential: credentialResponse.credential,
          userData: decoded
        })
      });

      if (response.ok) {
        const data = await response.json();
        login(data);
        localStorage.setItem('user', JSON.stringify(data.user));
        navigate('/userpage');
      }
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
    <PageWrapper>
      <Logo src={logo} alt="Logo" onClick={handleLogoClick}/>
      <LoginButtonWrapper>
       <GoogleLogin
        onSuccess={handleGoogleSuccess}
        onError={handleLoginFailure}
        />
       </LoginButtonWrapper>
    </PageWrapper>
  );
};

export default FirstPage;