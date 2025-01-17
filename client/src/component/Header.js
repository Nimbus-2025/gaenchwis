import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/cloud.png';
import './Header.css';
import CategoryPopup from '../component/CategoryPopup';
import SearchResult from '../pages/tab/SearchResult';

const Header = ({ userData, onSearch }) => {
  const [searchText, setSearchText] = useState('');
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
      const handleSearchClick = (e) => {
        e.preventDefault(); // 폼 기본 동작 방지
        if (searchText.trim()) {
          onSearch(searchText.trim());
          setSearchText(''); 
        }
      };
    return (
      <header className="header">
        
    
        <div className="left-section">
          <img src={logo} alt="로고" className="header-logo"
          onClick={handleLogoClick}
          style={{ cursor: 'pointer' }}
           />
        
        </div>
        
        <form onSubmit={handleSearchClick} className="search-section">
        <button 
          type="button"
          className="category-btn"
          onClick={() => setIsCategoryOpen(!isCategoryOpen)}
        >
          카테고리
        </button>
        <input
          type="text"
          placeholder="검색어를 입력하세요"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
          className="search-input"
        />
        <button type="submit" className="header-search-btn">
        </button>
      </form>

      <CategoryPopup 
        isOpen={isCategoryOpen} 
        onClose={() => setIsCategoryOpen(false)}
      />
    </header>
  );
};
  

export default Header;