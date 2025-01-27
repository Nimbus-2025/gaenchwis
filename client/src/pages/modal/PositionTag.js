import React, { useState, useEffect } from 'react';
import './PositionTag.css';

// 미리 정의된 직무 카테고리
const PREDEFINED_CATEGORIES = [
  "개발자",
  "디자이너",
  "기획자",
  "엔지니어"
];

const PositionTag = ({ isOpen, onClose, selectedTags, onApply }) => {
  const [allPositionTags, setAllPositionTags] = useState({});
  const [tempSelectedCategories, setTempSelectedCategories] = useState([]);
  const [matchingTags, setMatchingTags] = useState([]);

  // API에서 태그 데이터 가져오기
  useEffect(() => {
    const fetchPositionTags = async () => {
      try {
        const response = await fetch('http://localhost:5001/api/tags/skill');
        const data = await response.json();
        console.log('받아온 태그 데이터:', data); 
        setAllPositionTags(data);
      } catch (error) {
        console.error('태그 데이터 가져오기 실패:', error);
      }
    };

    if (isOpen) {
      fetchPositionTags();
    }
  }, [isOpen]);

  // 카테고리 선택 시 해당하는 태그들 찾기
  const handleCategoryClick = (category) => {
    console.log('선택된 카테고리:', category); // 디버깅용
    console.log('현재 allPositionTags:', allPositionTags); // 디버깅용
    
    setTempSelectedCategories(prev => {
      const newSelection = prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category];
      
      // 선택된 카테고리들에 해당하는 태그들 찾기
      const newMatchingTags = newSelection.length > 0
        ? newSelection.flatMap(cat => allPositionTags[cat] || [])
        : [];
      
      setMatchingTags(newMatchingTags);
      return newSelection;
    });
  };

  const handleApply = () => {
    console.log('적용할 태그들:', matchingTags); // 디버깅용
    if (matchingTags.length > 0) {
      onApply(matchingTags);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>관심 직무 선택</h3>
        <div className="category-selection">
          {PREDEFINED_CATEGORIES.map((category) => (
            <button
              key={category}
              className={`category-button ${tempSelectedCategories.includes(category) ? 'selected' : ''}`}
              onClick={() => handleCategoryClick(category)}
            >
              {category}
            </button>
          ))}
        </div>
        
        {matchingTags.length > 0 && (
          <div className="matching-tags-preview">
            <h4>선택된 직무 태그:</h4>
            <div className="tags-preview">
              {matchingTags.map((tag) => (
                <span key={tag} className="preview-tag">
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="modal-buttons">
          <button 
            className="apply-button" 
            onClick={handleApply}
            disabled={matchingTags.length === 0}
          >
            적용
          </button>
          <button className="cancel-button" onClick={onClose}>
            취소
          </button>
        </div>
      </div>
    </div>
  );
};

export default PositionTag;