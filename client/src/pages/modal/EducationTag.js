import React, { useState } from 'react';
import './EducationTag.css';
import Api from '../../api/api';
import Config from '../../api/Config';


const EducationTag = ({ isOpen, onClose, allEducationTags, selectedTags, onApply }) => {
  const [tempSelectedTags, setTempSelectedTags] = useState(selectedTags);
  const [isLoading, setIsLoading] = useState(false);
  const [savedTags, setSavedTags] = useState([]);

  const handleTagClick = (tag) => {
    if (tempSelectedTags.includes(tag)) {
      setTempSelectedTags(tempSelectedTags.filter(t => t !== tag));
    } else {
      setTempSelectedTags([...tempSelectedTags, tag]);
    }
  };

  if (!isOpen) return null;

  const handleApply = async () => {
    setIsLoading(true);
    try {
      const user = JSON.parse(sessionStorage.getItem('user'));
      const token = sessionStorage.getItem('token');  // 토큰 가져오기
      const userId = user?.user_id;
      
      const tagsData = tempSelectedTags.map(tag => ({
        tag_id: tag.id || '',  // tag_id가 없을 경우 빈 문자열
        tag_name: tag,         // tag 자체가 문자열인 경우
        tag_type: 'education'
      }));
  
  
      const response = await Api(
        `${Config.server}:8003/api/v1/user/tags/location/${userId}`, 'PUT',
        {
          tags: tagsData
        });
      onApply(tempSelectedTags);
      onClose();
    } catch (error) {
      console.error('태그 저장 중 에러:', error);
      alert('태그 저장에 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };
  if (!isOpen || !allEducationTags) return null;


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
               {tag.tag_name || tag}
            </button>
          ))}
        </div>
        <div className="modal-buttons">
        <button 
            className="apply-button" 
            onClick={handleApply}
            disabled={isLoading}
          >
            {isLoading ? '저장 중...' : '적용'}
          </button>
          <button className="tag-cancel-button" onClick={onClose}>취소</button>
        </div>
      </div>
    </div>
  );
};

export default EducationTag;