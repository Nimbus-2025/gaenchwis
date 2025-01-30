import React, { useState } from 'react';
import './LocationTag.css';
import Api from '../../api/api';
import Config from '../../api/Config';

const LocationTag = ({ isOpen, onClose, allLocationTags, selectedTags, onApply }) => {
  const [tempSelectedTags, setTempSelectedTags] = useState(selectedTags);
  const [isLoading, setIsLoading] = useState(false);

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
  const handleApply = async () => {
    setIsLoading(true);
    try {
      // 선택된 태그들을 API 요청 형식에 맞게 변환
      const tagsData = tempSelectedTags.map((tagName, tag, index) => ({
        tag_id: tag.tag_id,
        tag_name: tag.tag_name || tag, 
        tag_type: 'location'
      }));
      
      console.log('전송할 태그 데이터:', tagsData);  // 디버깅용
      // API 호출하여 태그 업데이트
      const response = await Api(
        `${Config.server}:8005/api/v1/user/tags/location`,
        'PUT',
        {
          tags: tagsData
        }
      );

      console.log('\n=== API 응답 데이터 ===');
      console.log('응답 전체:', response);
      console.log('업데이트된 태그들:', response.tags);

      // 성공적으로 저장되면 부모 컴포넌트에 알림
      onApply(tempSelectedTags);
      onClose();
    } catch (error) {
      console.error('태그 저장 중 에러:', error);
      alert('태그 저장에 실패했습니다.');
    } finally {
      setIsLoading(false);
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
          <button 
            className="apply-button" 
            onClick={handleApply}
            disabled={isLoading}
          >
            {isLoading ? '저장 중...' : '적용'}
          </button>
          <button 
            className="cancel-button" 
            onClick={onClose}
            disabled={isLoading}
          >
            취소
          </button>
        </div>
      </div>
    </div>
  );
};

export default LocationTag;