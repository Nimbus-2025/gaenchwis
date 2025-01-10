import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../component/Header.css';
import './UserPage.css';
import Header from '../component/Header';
const UserPage = () => {

  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();


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
    //   <div className="user-content">
    //     {userData ? (
    //       <div>
    //         <p>환영합니다, {userData.name}님!</p>
    //       </div>
    //     ) : (
    //       <p>사용자 정보를 불러오는 중...</p>
    //     )}
       <div className="job-sections">
          <div className="recommended-jobs">
          {userData && (
            <h2>{userData.name} 님을 위한 추천 채용공고 입니다!</h2>
            )}
            <div className="job-list">
                <p>공고 1</p>
            </div>
          </div>
          <div className="latest-jobs">
            <h2>최근 업데이트된 최신 공고 입니다!</h2>
            <div className="job-list">
                <p>공고 1</p>
            </div>
            {/* 최신 공고 목록을 여기에 추가 */}
          </div>
        </div>
      
    
  );
};

export default UserPage;