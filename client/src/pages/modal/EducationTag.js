import React, { useState } from 'react';
import './EducationTag.css';

const EducationTag = ({ isOpen, onClose, allEducationTags, selectedTags, onApply }) => {
  const [tempSelectedTags, setTempSelectedTags] = useState(selectedTags);

  const handleTagClick = (tag) => {
    if (tempSelectedTags.includes(tag)) {
      setTempSelectedTags(tempSelectedTags.filter(t => t !== tag));
    } else {
      setTempSelectedTags([...tempSelectedTags, tag]);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>학력 태그 선택</h3>
        <div className="tag-selection">
          {allEducationTags.map((tag, index) => (
            <button
              key={index}
              className={`tag-button ${tempSelectedTags.includes(tag) ? 'selected' : ''}`}
              onClick={() => handleTagClick(tag)}
            >
              {tag}
            </button>
          ))}
        </div>
        <div className="modal-buttons">
          <button className="tag-apply-button" onClick={() => onApply(tempSelectedTags)}>적용</button>
          <button className="tag-cancel-button" onClick={onClose}>취소</button>
        </div>
      </div>
    </div>
  );
};

export default EducationTag;