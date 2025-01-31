import React, { useState, useEffect } from 'react';
import './PositionTag.css';

const PREDEFINED_CATEGORIES = [
  "개발자",
  "디자이너",
  "기획자",
  "엔지니어",
  "데이터",
  "보안"
];

const SKILL_CATEGORIES = [
  "개발",
  "디자인",
  "데이터",
  "서버/네트워크",
  "일반"
];

const PositionTag = ({ isOpen, onClose, selectedTags, onApply }) => {
  const [allPositionTags, setAllPositionTags] = useState({});
  const [allSkillTags, setAllSkillTags] = useState({});
  const [tempSelectedCategories, setTempSelectedCategories] = useState([]);
  const [tempSelectedSkillCategories, setTempSelectedSkillCategories] = useState([]);
  const [matchingTags, setMatchingTags] = useState([]);
  const [matchingSkillTags, setMatchingSkillTags] = useState([]);
  const [selectedPositionTags, setSelectedPositionTags] = useState(selectedTags || []);
  const [selectedSkillTags, setSelectedSkillTags] = useState([]);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const [positionResponse, skillResponse] = await Promise.all([
          fetch('http://localhost:8003/api/tags/position'),
          fetch('http://localhost:8003/api/tags/skill')
        ]);
        
        const positionData = await positionResponse.json();
        const skillData = await skillResponse.json();
        
        console.log('Position Data:', positionData);
        console.log('Skill Data:', skillData);
        
        setAllPositionTags(positionData);
        setAllSkillTags(skillData);
      } catch (error) {
        console.error('태그 데이터 가져오기 실패:', error);
      }
    };

    if (isOpen) {
      fetchTags();
      setSelectedPositionTags(selectedTags || []);
    }
  }, [isOpen, selectedTags]);

  const handleCategoryClick = (category) => {
    setTempSelectedCategories(prev => {
      const newSelection = prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category];
      
      const newMatchingTags = newSelection.length > 0
        ? newSelection.flatMap(cat => allPositionTags[cat] || [])
        : [];
      
      setMatchingTags(newMatchingTags);
      return newSelection;
    });
  };

  const handleSkillCategoryClick = (category) => {
    setTempSelectedSkillCategories(prev => {
      const newSelection = prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category];
      
      const newMatchingTags = newSelection.length > 0
        ? newSelection.flatMap(cat => allSkillTags[cat] || [])
        : [];
      
      setMatchingSkillTags(newMatchingTags);
      return newSelection;
    });
  };

  const handleTagClick = (tag) => {
    setSelectedPositionTags(prev => {
      if (prev.includes(tag)) {
        return prev.filter(t => t !== tag);
      }
      return [...prev, tag];
    });
  };

  const handleSkillTagClick = (tag) => {
    setSelectedSkillTags(prev => {
      if (prev.includes(tag)) {
        return prev.filter(t => t !== tag);
      }
      return [...prev, tag];
    });
  };

  const handleApply = () => {
    const allSelectedTags = [...selectedPositionTags, ...selectedSkillTags];
    if (allSelectedTags.length > 0) {
      onApply(allSelectedTags);
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
              {allPositionTags[category] && ` (${allPositionTags[category].length})`}
            </button>
          ))}
        </div>

        {matchingTags.length > 0 && (
          <div className="matching-tags-preview">
            <h4>선택 가능한 직무 태그:</h4>
            <div className="tags-preview">
              {matchingTags.map((tag) => (
                <span
                  key={tag}
                  className={`preview-tag ${selectedPositionTags.includes(tag) ? 'selected' : ''}`}
                  onClick={() => handleTagClick(tag)}
                >
                  {tag} {selectedPositionTags.includes(tag) && '✓'}
                </span>
              ))}
            </div>
          </div>
        )}

        <h3>관심 스킬 선택</h3>
        <div className="category-selection">
          {SKILL_CATEGORIES.map((category) => (
            <button
              key={category}
              className={`category-button ${tempSelectedSkillCategories.includes(category) ? 'selected' : ''}`}
              onClick={() => handleSkillCategoryClick(category)}
            >
              {category}
              {allSkillTags[category] && ` (${allSkillTags[category].length})`}
            </button>
          ))}
        </div>

        {matchingSkillTags.length > 0 && (
          <div className="matching-tags-preview">
            <h4>선택 가능한 스킬 태그:</h4>
            <div className="tags-preview">
              {matchingSkillTags.map((tag) => (
                <span
                  key={tag}
                  className={`preview-tag ${selectedSkillTags.includes(tag) ? 'selected' : ''}`}
                  onClick={() => handleSkillTagClick(tag)}
                >
                  {tag} {selectedSkillTags.includes(tag) && '✓'}
                </span>
              ))}
            </div>
          </div>
        )}

        {(selectedPositionTags.length > 0 || selectedSkillTags.length > 0) && (
          <div className="selected-tags-preview">
            <h4>선택된 태그:</h4>
            <div className="tags-preview">
              {selectedPositionTags.map((tag) => (
                <span
                  key={tag}
                  className="preview-tag selected"
                  onClick={() => handleTagClick(tag)}
                >
                  {tag} ✕
                </span>
              ))}
              {selectedSkillTags.map((tag) => (
                <span
                  key={tag}
                  className="preview-tag selected"
                  onClick={() => handleSkillTagClick(tag)}
                >
                  {tag} ✕
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="modal-buttons">
          <button 
            className="apply-button" 
            onClick={handleApply}
            disabled={selectedPositionTags.length === 0 && selectedSkillTags.length === 0}
          >
            적용 ({selectedPositionTags.length + selectedSkillTags.length})
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