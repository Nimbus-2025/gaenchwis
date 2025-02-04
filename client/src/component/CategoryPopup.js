import React from 'react';
import './CategoryPopup.css';

function CategoryPopup({
  isOpen,
  onClose,
  selectedCategories,
  setSelectedCategories,
}) {
  // Header의 상태와 일치하도록 카테고리 구조 수정
  const categories = {
    직무: ['개발', '기획', '디자인', '영업'],
    학력: ['4년제 졸업', '전문대 졸업', '고졸'],
    지역: ['서울', '경기', '인천'],
    경력: ['신입', '경력'],
  };

  const handleCheckboxChange = (category, item) => {
    setSelectedCategories((prev) => ({
      ...prev,
      [category]: prev[category]?.includes(item)
        ? prev[category].filter((i) => i !== item)
        : [...(prev[category] || []), item],
    }));
  };

  if (!isOpen) return null;

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>

        <div className="categories-container">
          {Object.entries(categories).map(([category, items]) => (
            <div key={category} className="category-section">
              <h3>{category}</h3>
              <div className="checkbox-group">
                {items.map((item) => (
                  <label key={item} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={
                        selectedCategories[category]?.includes(item) || false
                      }
                      onChange={() => handleCheckboxChange(category, item)}
                    />
                    {item}
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="popup-buttons">
          <button
            className="apply-btn"
            onClick={() => {
              onClose();
            }}
          >
            적용하기
          </button>
        </div>
      </div>
    </div>
  );
}

export default CategoryPopup;