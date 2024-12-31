import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/cloud.png';
import './Header.css';
import CategoryPopup from '../component/CategoryPopup';
const Header = ({ userData, onLogout, searchText, setSearchText, onSearch, onMyPageClick }) => {
    const navigate = useNavigate();
    const [isCategoryOpen, setIsCategoryOpen] = useState(false);
    const toggleCategoryPopup = () => {
        setIsCategoryOpen(!isCategoryOpen); // 카테고리 팝업 상태 토글
      };
      const handleLogoClick = () => {
        if (userData) { // 로그인 상태일 때만 유저 페이지로 이동
          navigate('/userpage'); // 유저 페이지로 이동
        }
      };
      const handleMyPageClick = () => {
        navigate('/mypage1'); // 마이페이지로 이동
      };
  
    return (
      <header className="header">
        <div className="left-section">
          <img src={logo} alt="로고" className="header-logo"
          onClick={handleLogoClick}
          style={{ cursor: 'pointer' }}
           />
          <button 
            className="category-btn"
            onClick={toggleCategoryPopup}
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
          <button className="search-btn" onClick={onSearch}>
            검색
          </button>
          <button className="mypage-btn" onClick={handleMyPageClick}>
            마이페이지
          </button>
        </div>
  
        <div className="right-section">
          {userData ? (
            <button className="header-logout-btn" onClick={onLogout}>로그아웃</button>
          ) : (
            <button className="header-login-btn" onClick={() => navigate('/')}>로그인</button>
          )}
        </div>
        <CategoryPopup 
        isOpen={isCategoryOpen} 
        onClose={() => setIsCategoryOpen(false)} // 팝업 닫기 핸들러
      />
      </header>
    );
  };
  

export default Header;