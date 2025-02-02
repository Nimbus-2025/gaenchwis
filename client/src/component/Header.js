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
    const [selectedCategories, setSelectedCategories] = useState({
      직무: [],
      학력: [],
      지역: [],
      경력: []
    });
    const toggleCategoryPopup = () => {
        setIsCategoryOpen(!isCategoryOpen); // 카테고리 팝업 상태 토글
      };
      const handleLogoClick = () => {
        if (userData) { // 로그인 상태일 때만 유저 페이지로 이동
          navigate('/mypage1'); // 유저 페이지로 이동
        }
      };
      const handleSearch = () => {
        fetch(`your-api-endpoint?query=${searchText}&categories=${JSON.stringify(selectedCategories)}`)
          .then(response => response.json())
          .then(results => {
            onSearch(results); // 검색 결과를 상위 컴포넌트로 전달
          });
      };
      const handleCategoryApply = (categories) => {
        console.log("Categories received:", categories); 
        setSelectedCategories(categories);
        setIsCategoryOpen(false);
        // 현재 검색어가 있다면 카테고리와 함께 검색 실행
      };
      const handleSearchClick = (e) => {
        e.preventDefault(); // 폼 기본 동작 방지
        if (searchText.trim()) {
          onSearch(searchText.trim(),  selectedCategories);
          setSearchText(''); 
        }
      };
      const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(searchText, selectedCategories);  // 검색어와 카테고리 정보 함께 전달
      };
    return (
      <header className="header">
        
    
        <div className="left-section">
          <img src={logo} alt="로고" className="header-logo"
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
        onClick={() => window.open('https://chromewebstore.google.com/detail/gaenchwis/lomllodaddlcklkmdhoidmldhbmoickc', '_blank')}
          data-tooltip="크롬 익스텐션"
        >
    </button>
      </form>

      <CategoryPopup 
        isOpen={isCategoryOpen} 
        onClose={() => setIsCategoryOpen(false)}
        onApply={handleCategoryApply}
        initialCategories={selectedCategories}
      />
    </header>
  );
};
  

export default Header;