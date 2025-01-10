import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/cloud.png';
import './Header.css';
import CategoryPopup from '../component/CategoryPopup';
import SearchResult from '../pages/tab/SearchResult';

const Header = ({ userData, onLogout, searchText, setSearchText, onSearch }) => {
    const navigate = useNavigate();
    const [isCategoryOpen, setIsCategoryOpen] = useState(false);
    const toggleCategoryPopup = () => {
        setIsCategoryOpen(!isCategoryOpen); // 카테고리 팝업 상태 토글
      };
      const handleLogoClick = () => {
        if (userData) { // 로그인 상태일 때만 유저 페이지로 이동
          navigate('/mypage1'); // 유저 페이지로 이동
        }
      };
      const handleSearchClick = () => {
        onSearch(); // Call the onSearch function passed as a prop
      };
    
    return (
      <header className="header">
        
    
        <div className="left-section">
          <img src={logo} alt="로고" className="header-logo"
          onClick={handleLogoClick}
          style={{ cursor: 'pointer' }}
           />
        
        </div>
        
        <div className="search-section">
        <button 
            className="category-btn"
            onClick={toggleCategoryPopup}
          >
            카테고리
          </button>
          <input
            type="text"
            placeholder="검색어를 입력하세요"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                handleSearchClick(); // 엔터 키가 눌리면 검색 실행
              }
            }}
            className="search-input"
          />
          <button className="header-search-btn" onClick={handleSearchClick}>
          
          </button>
        </div>
  
        <CategoryPopup 
        isOpen={isCategoryOpen} 
        onClose={() => setIsCategoryOpen(false)} // 팝업 닫기 핸들러
      />
      </header>
    );
  };
  

export default Header;