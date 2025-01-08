import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header1 = ({ userData, selectedButton, showProfile, showBookmarks, showCalendar, showEssay, onLogout }) => {
  const navigate = useNavigate();

  return (
    <div className="button-container">
      <button className={selectedButton === 'profile' ? 'active' : ''} onClick={showProfile}>프로필</button>
      <button className={selectedButton === 'bookmarks' ? 'active' : ''} onClick={showBookmarks}>북마크 / 관심기업</button>
      <button className={selectedButton === 'calendar' ? 'active' : ''} onClick={showCalendar}>캘린더</button>
      <button className={selectedButton === 'essay' ? 'active' : ''} onClick={showEssay}>자기소개서</button>
      
      <div className="logout-container">
        {userData ? (
          <button className="logout-btn" onClick={onLogout}>로그아웃</button>
        ) : (
          <button className="header-login-btn" onClick={() => navigate('/')}>로그인</button>
        )}
      </div>
    </div>
  );
};

export default Header1;