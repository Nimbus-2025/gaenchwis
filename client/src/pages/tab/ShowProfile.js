import React, { useState, useEffect } from 'react';
import LocationModal from '../modal/LocationModal';
import Modal from '../modal/Edit';
import './ShowProfile.css';
import Config from '../../api/Config';
import Api from '../../api/Api';

const ShowProfile = ({ userData }) => {
  const [selectedLocations, setSelectedLocations] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedDistricts, setSelectedDistricts] = useState({});
  const [isEditModalOpen, setIsEditModalOpen] = useState(false); // 수정 모달 상태
  const [positionTags, setPositionTags] = useState([]);
  const [educationTags, setEducationTags] = useState([]);
  const [error, setError] = useState(null);
  const tagOrder = {
    '대학교(4년)': 1,
    '대학(2,3년)': 2,
    '고졸': 3,
    '석사': 4,
    '박사': 5,
    '학력무관': 6
};

useEffect(() => {
  const fetchEducationTags = async () => {
      try {
          const response = await fetch('http://localhost:5001/api/tags/education');
          if (!response.ok) {
              throw new Error('Failed to fetch education tags');
          }
          const data = await response.json();
          
          // 태그 정렬
          const sortedTags = data.sort((a, b) => 
              (tagOrder[a] || 999) - (tagOrder[b] || 999)
          );
          
          setEducationTags(sortedTags);
      } catch (error) {
          console.error('Error fetching education tags:', error);
      }
  };

  fetchEducationTags();
}, []);

  const handleLocationSelect = (district) => {
    setSelectedDistricts((prev) => {
      const isSelected = prev[district]?.includes(district);
  
      return {
        ...prev,
        [district]: isSelected
          ? prev[district].filter((d) => d !== district)
          : [...(prev[district] || []), district],
      };
    });
  };
  const openEditModal = () => {
    setIsEditModalOpen(true); // 수정 모달 열기
};

  const handleApplyLocations = (locations) => {
    setSelectedLocations(locations);
    setIsModalOpen(false);
  };

  return (
    <div>
      <div className="profile-container">
      <div className="profile-info">
        <div className="profile-header">
          <div className="profile-picture">
            <img src={userData.profileImage || ''} alt="Profile" className="profile-image" />
          </div>
          <div className="profile-details">
            <p>이름: {name}</p>
            <p>전화번호: {phone}</p>
            <p>이메일 주소: {email}</p>
          </div>
        </div>
        <button className="edit-button" onClick={openEditModal}>개인정보 수정</button>
      </div>
      <div className="profile-info1">
      <h4>입사지원 현황</h4>
        <div className="status-box">
        <div className="status-container">
        <div className="status-item">
            <span>지원완료</span>
            <span>2</span>
        </div>
        <div className="divider"></div>
        <div className="status-item">
            <span>서류통과</span>
            <span>0</span>
        </div>
        <div className="divider"></div>
        <div className="status-item">
        <span>최종합격</span>
        <span>0</span>
        </div>
        <div className="divider"></div>
        <div className="status-item">
         <span>불합격</span>
         <span>0</span>
        </div>
        </div>
        </div>
    </div>
    </div>
      <div>
        <div className="info-box-container">
          <div className="info-box">
            <h4>지역</h4>
            <div className="tag-list">
            <p>선택된 지역: {selectedLocations.map(location => (
             <span key={location}>
             {location}({selectedDistricts[location]?.join(', ') || '지역구 없음'})
             </span>
             )).reduce((prev, curr) => prev ? [prev, ', ', curr] : [curr], '')}
            </p>
                  <button className="add-location-button" onClick={() => setIsModalOpen(true)}>+</button>
            </div>
          </div>
          <div className="info-box">
                        <h4>관심 직무</h4>
                        <div className="tag-list">
                            {/* 관심 직무 내용 추가 */}
                        </div>
                    </div>
                    <div className="info-box">
                    <h4>학력</h4>
            <div className="tag-list">
                {educationTags.length > 0 ? (
                    educationTags.map((tag, index) => (
                        <span key={index} className="tag-item">
                            {tag}
                        </span>
                    ))
                ) : (
                    <span className="no-tags">태그 없음</span>
                )}
                </div>
                    </div>
                    
        </div>
      </div>
      <LocationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onApply={handleApplyLocations}
      />
       <Modal 
                isOpen={isEditModalOpen} 
                onClose={() => setIsEditModalOpen(false)} 
                onSave={handleSave}
                name={name}
                email={email}
                phone={phone}
            />
    </div>
  );
};

export default ShowProfile;