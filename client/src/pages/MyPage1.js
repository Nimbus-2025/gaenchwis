import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/cloud.png'; // 로고 이미지 경로
import '../component/Header.css';
import './UserPage.css';
import Header from '../component/Header';
import './MyPage1.css';
const MyPage1 = () => {
  const [searchText, setSearchText] = useState('');
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  const handleSearch = () => {
    console.log('검색:', searchText);
  };

  const handleLoginClick = () => {
    navigate('/'); // 로그인 페이지로 이동
  };

  const handleMyPageClick = () => {
    navigate('/mypage'); // 마이페이지로 이동
  };
  const handleLogoutClick = () => {
    // 로그아웃 처리
    localStorage.removeItem('user'); // 로컬 스토리지에서 사용자 정보 삭제
    navigate('/'); // 메인 페이지로 이동
  };


  useEffect(() => {
    try {
      const storedUserData = localStorage.getItem('user');
      if (storedUserData) {
        setUserData(JSON.parse(storedUserData));
      }
    } catch (error) {
      console.error('Error parsing user data from localStorage:', error);
    }
  }, []);

  return (
    <div>
      <Header 
        userData={userData} 
        onLogout={handleLogoutClick} 
        searchText={searchText} 
        setSearchText={setSearchText} 
        onSearch={handleSearch} 
        handleMyPageClick={handleMyPageClick} 
      />
    
        <div className="button-container">
        <button onClick={() => navigate('/profile')}>프로필</button>
        <button onClick={() => navigate('/bookmarks')}>북마크 및 관심기업</button>
        <button onClick={() => navigate('/calendar')}>캘린더</button>
        <button onClick={() => navigate('/cover-letter')}>자기소개서</button>
        </div>
    </div>
  );
};
export default MyPage1;