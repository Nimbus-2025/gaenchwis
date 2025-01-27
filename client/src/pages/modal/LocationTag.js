import React, { useState } from 'react';
import './LocationTag.css';

const LocationTag = ({ isOpen, onClose, allLocationTags, selectedTags, onApply }) => {
  const [tempSelectedTags, setTempSelectedTags] = useState(selectedTags);

  const handleTagClick = (tag) => {
    if (tempSelectedTags.includes(tag)) {
      setTempSelectedTags(tempSelectedTags.filter(t => t !== tag));
    } else {
      setTempSelectedTags([...tempSelectedTags, tag]);
    }
  };

  // 지역 전체 선택 처리
  const handleRegionSelect = (region, tags) => {
    if (tags.every(tag => tempSelectedTags.includes(tag))) {
      // 해당 지역 태그들을 모두 해제
      setTempSelectedTags(tempSelectedTags.filter(tag => !tags.includes(tag)));
    } else {
      // 해당 지역 태그들을 모두 선택
      const newTags = [...tempSelectedTags];
      tags.forEach(tag => {
        if (!newTags.includes(tag)) {
          newTags.push(tag);
        }
      });
      setTempSelectedTags(newTags);
    }
  };

  if (!isOpen || !allLocationTags) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>지역 태그 선택</h3>
        <div className="tag-selection">
          {Object.entries(allLocationTags).map(([region, tags]) => (
            <div key={region} className="region-section">
              <div className="region-header">
                <label className="region-checkbox">
                  <input
                    type="checkbox"
                    checked={tags.every(tag => tempSelectedTags.includes(tag))}
                    onChange={() => handleRegionSelect(region, tags)}
                  />
                  <h4>{region} 전체</h4>
                </label>
              </div>
              <div className="tags-container">
                {tags.map((tag, index) => (
                  <button
                    key={index}
                    className={`tag-button ${tempSelectedTags.includes(tag) ? 'selected' : ''}`}
                    onClick={() => handleTagClick(tag)}
                  >
                    {tag.replace(`${region} `, '')}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="modal-buttons">
          <button className="apply-button" onClick={() => onApply(tempSelectedTags)}>적용</button>
          <button className="cancel-button" onClick={onClose}>취소</button>
        </div>
      </div>
    </div>
  );
};

export default LocationTag;