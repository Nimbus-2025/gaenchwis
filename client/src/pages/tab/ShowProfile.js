import React, { useState, useEffect } from 'react';
import LocationTag from '../modal/LocationTag';
import Modal from '../modal/Edit';
import './ShowProfile.css';
import Config from '../../api/Config';
import Api from '../../api/api';
import { format } from 'date-fns';
import EducationTag from '../modal/EducationTag';
import PositionTag from '../modal/PositionTag';



const ShowProfile = ({ userData }) => {
  const [selectedLocations, setSelectedLocations] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedDistricts, setSelectedDistricts] = useState({});
  const [isEditModalOpen, setIsEditModalOpen] = useState(false); // 수정 모달 상태
  const [phone, setPhone] = useState(userData?.phone || '등록되지 않음');
  const [email, setEmail] = useState(userData?.email || '정보 없음');
  const [name, setName] = useState(userData?.name || '정보 없음');
  const [positionTags, setPositionTags] = useState([]);
  const [educationTags, setEducationTags] = useState([]);
  const [error, setError] = useState(null);
  const [isEducationModalOpen, setIsEducationModalOpen] = useState(false);
  const [allEducationTags, setAllEducationTags] = useState([]);
  const [allLocationTags, setAllLocationTags] = useState([]);
  const [isPositionModalOpen, setIsPositionModalOpen] = useState(false);
  const [selectedPositionTags, setSelectedPositionTags] = useState([]);

  const tagOrder = {
    '대학교(4년)': 1,
    '대학(2,3년)': 2,
    고졸: 3,
    석사: 4,
    박사: 5,
    학력무관: 6,
  };
  const today = new Date(); // today 변수 추가
  useEffect(() => {
    const fetchEducationTags = async () => {
      try {
        const data = await Api(`${Config.server}:8003/api/tags/education`, 'GET')

        // 태그 정렬
        const sortedTags = data.sort(
          (a, b) => (tagOrder[a] || 999) - (tagOrder[b] || 999),
        );

        setAllEducationTags(sortedTags);  // 모든 가능한 태그 설정
        setEducationTags([]); // 초기에는 선택된 태그 없음
      } catch (error) {
        console.error('Error fetching education tags:', error);
      }
    };

    fetchEducationTags();
  }, []);

  useEffect(() => {
    const fetchLocationTags = async () => {
      try {
        const response = await fetch('http://localhost:8003/api/tags/location');
        if (!response.ok) {
          throw new Error('Failed to fetch location tags');
        }
        const data = await response.json();
        console.log('Fetched location tags:', data); // 데이터 확인용
        setAllLocationTags(data);
      } catch (error) {
        console.error('Error fetching location tags:', error);
      }
    };

    fetchLocationTags();
  }, []);

  const handleApplyEducationTags = (selectedTags) => {
    setEducationTags(selectedTags);
    setIsEducationModalOpen(false);
  };

  const handlePositionTagsApply = (tags) => {
    console.log('선택된 태그들:', tags); // 디버깅용
    setSelectedPositionTags(tags);
    // 여기서 선택된 태그들을 저장하거나 처리
  };

  
  const handleSave = async (name, email, phone) => {
    setName(name);
    setEmail(email);
    setPhone(phone);
    userData.phone = phone;
    userData.email = email;
    userData.name = name;
    sessionStorage.setItem('user', JSON.stringify(userData));

    const body = {
      userId: userData.user_id,
      name: name,
      email: email,
      phone: phone,
    };
    const response = await Api(`${Config.server}/user_save`, 'POST', body);
    console.log(response);
  };

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
             
            </div>
            <div className="profile-details">
                <p>이름: {name}</p>
                <p>전화번호: {phone}</p>
                <p>이메일 주소: {email}</p>
                 
          </div>
        </div>
        <button className="edit-button" onClick={openEditModal}>개인정보 수정</button>
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
        </div>
        </div>
      </div>

      <div className="profile-info">
      <div className="today-schedule">
    <h4>오늘의 일정입니다</h4>
    <p className="today-date">{format(new Date(), 'yyyy년 MM월 dd일')}</p>
    </div>
    <div className="today-schedule">
   
    <h4>다가오는 일정</h4>
    
    </div>
     
    </div>
    </div>
      <div>
      <h4>My tag</h4>
      
        <div className="info-box-container">
        
        <div className="info-box-row">
          <div className="info-box">
          <div className="info-box-header">
            <h4>지역</h4>
            <button  
            className="add-tag-button"
          onClick={() => setIsModalOpen(true)}
        >
          +
        </button>
        </div>
           <div className="tag-list">
      {selectedLocations.length > 0 ? (
        selectedLocations.map((location, index) => (
          <span key={index} className="tag-item">
            {location}
          </span>
        ))
      ) : (
        <span className="no-tags">태그 없음</span>
      )}
    </div>
  </div>
                    <div className="info-box">
                    <div className="info-box-header">
                    <h4>학력</h4>
                    <button 
          className="add-tag-button"
          onClick={() => setIsEducationModalOpen(true)}
        >
          +
        </button>
        </div>
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
          <div className="info-box1">
          <div className="info-box-header">
          <h4>관심 직무</h4>
          <button 
            className="add-tag-button"
            onClick={() => setIsPositionModalOpen(true)}
          >
            +
          </button>
        </div>
        <div className="tag-list">
          {selectedPositionTags.length > 0 ? (
            selectedPositionTags.map((tag, index) => (
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
      <LocationTag
      isOpen={isModalOpen}
      onClose={() => setIsModalOpen(false)}
      allLocationTags={allLocationTags}
      selectedTags={selectedLocations}
      onApply={(selectedTags) => {
        setSelectedLocations(selectedTags);
        setIsModalOpen(false);
      }}
    />
       <Modal 
                isOpen={isEditModalOpen} 
                onClose={() => setIsEditModalOpen(false)} 
                onSave={handleSave}
                name={name}
                email={email}
                phone={phone}
            />
        <EducationTag
        isOpen={isEducationModalOpen}
        onClose={() => setIsEducationModalOpen(false)}
        allEducationTags={allEducationTags}
        selectedTags={educationTags}
        onApply={handleApplyEducationTags}
      />
      <PositionTag
  isOpen={isPositionModalOpen}
  onClose={() => setIsPositionModalOpen(false)}
  selectedTags={selectedPositionTags}
  onApply={handlePositionTagsApply}
/>
    </div>
    
  );
};

export default ShowProfile;
