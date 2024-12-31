import React, { useState } from 'react';
import './MainPage.css';
import logo from '../images/cloud.png';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import CategoryPopup from '../component/CategoryPopup';

function MainPage() {
  const [searchText, setSearchText] = useState('');
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const navigate = useNavigate();
  const handleLoginClick = () => {
    navigate('/'); // 로그인 페이지로 이동
  };

  const handleMyPageClick = () => {
    navigate('/mypage'); // 마이페이지로 이동
  };

  const handleSearch = () => {
    console.log('검색:', searchText);
  };

  return (
    <div className="main-page">
      <header className="header">
        <div className="left-section">
          <img src={logo} alt="로고" className="header-logo" />
          <button 
            className="category-btn"
            onClick={() => setIsPopupOpen(true)}
          >
            카테고리
          </button>
        </div>
        
        <div className="search-section">
          <input
            type="text"
            placeholder="검색어를 입력하세요"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            className="search-input"
          />
          <button className="search-btn" onClick={handleSearch}>
            검색
          </button>
          <button className="mypage-btn" onClick={handleMyPageClick}>마이페이지</button>
        </div>

        <div className="right-section">
          <button className="header-login-btn" onClick={handleLoginClick}>로그인</button>
        </div>
      </header>

      <CategoryPopup 
        isOpen={isPopupOpen}
        onClose={() => setIsPopupOpen(false)}
      />
    </div>
  );
}

export default MainPage;