import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/cloud.png';
import './Header.css';
import CategoryPopup from '../component/CategoryPopup';

const Header = ({ userData, onSearch }) => {
  const [searchText, setSearchText] = useState('');
  const navigate = useNavigate();
  const [isCategoryOpen, setIsCategoryOpen] = useState(false);
  const [selectedCategories, setSelectedCategories] = useState({
    직무: [],
    학력: [],
    지역: [],
    경력: [],
  });

  const handleLogoClick = () => {
    if (userData) {
      navigate('/mypage1');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (searchText.trim()) {
      // 검색 실행 시 선택된 카테고리와 함께 전달
      onSearch(searchText.trim(), selectedCategories);
      console.log('검색어:', searchText.trim());
      console.log('선택된 카테고리:', selectedCategories);
    }
  };

  return (
    <header className="header">
      <div className="left-section">
        <img
          src={logo}
          alt="로고"
          className="header-logo"
          onClick={handleLogoClick}
          style={{ cursor: 'pointer' }}
        />
      </div>

      <form onSubmit={handleSubmit} className="search-section">
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
        <button
          className="chrome-button"
          onClick={() =>
            window.open(
              'https://chromewebstore.google.com/detail/gaenchwis/lomllodaddlcklkmdhoidmldhbmoickc',
              '_blank',
            )
          }
          data-tooltip="크롬 익스텐션"
        />
      </form>

      <CategoryPopup
        isOpen={isCategoryOpen}
        onClose={() => setIsCategoryOpen(false)}
        selectedCategories={selectedCategories}
        setSelectedCategories={setSelectedCategories}
      />
    </header>
  );
};

export default Header;