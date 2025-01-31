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
  const [error, setError] = useState(null);
  const [isEducationModalOpen, setIsEducationModalOpen] = useState(false);
  const [allLocationTags, setAllLocationTags] = useState([]);
  const [isPositionModalOpen, setIsPositionModalOpen] = useState(false);
  const [selectedPositionTags, setSelectedPositionTags] = useState([]);
  const [isLocationTagModalOpen, setIsLocationTagModalOpen] = useState(false);
  const [isEducationTagModalOpen, setIsEducationTagModalOpen] = useState(false); // 추가
  const [allEducationTags, setAllEducationTags] = useState([]);
  const [educationTags, setEducationTags] = useState([]);
  const [isPositionTagModalOpen, setIsPositionTagModalOpen] = useState(false);

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
        // 초기에는 선택된 태그 없음
      } catch (error) {
        console.error('Error fetching education tags:', error);
      }
    };

    fetchEducationTags();
  }, []);

  

  useEffect(() => {
    fetchUserLocationTags();
  }, []);

  const fetchUserLocationTags = async () => {
    try {
      const user = JSON.parse(sessionStorage.getItem('user'));
      const token = sessionStorage.getItem('token');  // 토큰 가져오기
      const userId = user?.user_id;
      
      if (!userId) {
        console.error('사용자 정보를 찾을 수 없습니다.');
        return;
      }
      
      const response = await fetch('http://localhost:8005/api/v1/user/tags/location', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // 토큰 추가
          'User-Id': userId,
        },
        credentials: 'include'
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log('불러온 위치 태그:', data);
      
      // 데이터 구조에 따라 처리
      if (Array.isArray(data)) {
        setSelectedLocations(data);
      } else if (data.tags && Array.isArray(data.tags)) {
        setSelectedLocations(data.tags.map(tag => 
          typeof tag === 'string' ? tag : tag.tag_name
        ));
      }
    } catch (error) {
      console.error('위치 태그 조회 중 에러:', error);
    }
  };
  useEffect(() => {
    const fetchUserEducationTags = async () => {
      try {
        const user = JSON.parse(sessionStorage.getItem('user'));
        const token = sessionStorage.getItem('token');
        const userId = user?.user_id;
        
        if (!userId) {
          console.error('사용자 정보를 찾을 수 없습니다.');
          return;
        }
        
        const response = await fetch('http://localhost:8005/api/v1/user/tags/education', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            'User-Id': userId,
          },
          credentials: 'include'
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log('교육 태그 원본 데이터:', data);
        
        if (data.tags && Array.isArray(data.tags)) {
          const tagNames = data.tags.map(tag => tag.tag_name);
          console.log('변환된 교육 태그:', tagNames);
          setEducationTags(prev => {
            console.log('이전 교육 태그:', prev);
            console.log('새로운 교육 태그:', tagNames);
            return tagNames;
          });
        }
      } catch (error) {
        console.error('교육 태그 조회 중 에러:', error);
      }
    };

    fetchUserEducationTags();
  }, []);

  // 교육 태그 변경 감지
  useEffect(() => {
    console.log('교육 태그 상태 변경됨:', educationTags);
  }, [educationTags]);

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

  useEffect(() => {
    const fetchPositionTags = async () => {
      try {
        const user = JSON.parse(sessionStorage.getItem('user'));
        const token = sessionStorage.getItem('token');
        const userId = user?.user_id;
        
        if (!userId) return;

        const response = await fetch('http://localhost:8005/api/v1/user/tags/position', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            'User-Id': userId,
          },
          credentials: 'include'
        });

        if (!response.ok) {
          throw new Error('태그 조회 실패');
        }

        const data = await response.json();
        console.log('불러온 직무 태그:', data);
        
        if (data.tags && Array.isArray(data.tags)) {
          const tagNames = data.tags.map(tag => tag.tag_name);
          setPositionTags(tagNames);
        }
      } catch (error) {
        console.error('직무 태그 조회 중 에러:', error);
      }
    };

    fetchPositionTags();
  }, []);

  const handlePositionTagApply = async (selectedTags) => {
    try {
      const user = JSON.parse(sessionStorage.getItem('user'));
      const token = sessionStorage.getItem('token');
      const userId = user?.user_id;

      const response = await fetch('http://localhost:8005/api/v1/user/tags/position', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'User-Id': userId,
        },
        credentials: 'include',
        body: JSON.stringify({
          tags: selectedTags.map(tag => ({
            tag_id: tag,
            tag_name: tag,
            tag_type: 'position'
          }))
        })
      });

      if (!response.ok) {
        throw new Error('태그 저장 실패');
      }

      setPositionTags(selectedTags);
    } catch (error) {
      console.error('직무 태그 저장 중 에러:', error);
    }
  };


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


  const handleApplyLocations = async (selectedTags) => {
    try {
      const user = JSON.parse(sessionStorage.getItem('user'));
      const userId = user?.user_id;
  
      // 선택된 태그들을 API 요청 형식으로 변환
      const tagsData = selectedTags.map((tagName, index) => ({
        tag_id: `loc_${index + 1}`,
        tag_name: tagName,
        tag_type: 'location'
      }));
  
      // fetch를 사용한 API 호출
      const response = await fetch(`http://localhost:8005/api/v1/user/tags/location`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'User-Id': userId || '',
          'Origin': 'http://localhost:3000'
        },
        mode: 'cors',
        credentials: 'include',
        body: JSON.stringify({
          tags: tagsData
        })
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      console.log('태그 저장 응답:', data);
  
      // 상태 업데이트
      setSelectedLocations(selectedTags);
      setIsModalOpen(false);
    } catch (error) {
      console.error('태그 저장 중 에러:', error);
      alert('태그 저장에 실패했습니다.');
    }
  };


const handleEducationTagApply = async (selectedTags) => {
  try {
    const user = JSON.parse(sessionStorage.getItem('user'));
    const userId = user?.user_id;

    // 선택된 태그들을 API 요청 형식으로 변환
    const tagsData = selectedTags.map((tagName, index) => ({
      tag_id: `loc_${index + 1}`,
      tag_name: tagName,
      tag_type: 'education'
    }));

    // fetch를 사용한 API 호출
    const response = await fetch(`http://localhost:8005/api/v1/user/tags/education`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'User-Id': userId || '',
        'Origin': 'http://localhost:3000'
      },
      mode: 'cors',
      credentials: 'include',
      body: JSON.stringify({
        tags: tagsData
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('태그 저장 응답:', data);

    // 상태 업데이트
    setEducationTags(selectedTags);
    setIsEducationTagModalOpen(false); 
  } catch (error) {
    console.error('태그 저장 중 에러:', error);
    alert('태그 저장에 실패했습니다.');
  }
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
        <div className="button-wrapper">
        <button className="edit-button" onClick={openEditModal}>개인정보 수정</button>
        </div>
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
          onClick={() => setIsEducationTagModalOpen(true)}
        >
          +
        </button>
        </div>
            <div className="tag-list">
                {console.log('렌더링 시점 educationTags:', educationTags)}
                {Array.isArray(educationTags) && educationTags.length > 0 ? (
                  educationTags.map((tag, index) => (
                    <span key={index} className="tag-item">
                      {console.log('렌더링하는 태그:', tag)}
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
          <h4>관심 직무 / 스킬</h4>
          <button 
            className="add-tag-button"
            onClick={() => setIsPositionTagModalOpen(true)}
          >
            +
          </button>
        </div>
        <div className="tag-list">
          {positionTags && positionTags.length > 0 ? (
            positionTags.map((tag, index) => (
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
        onApply={handleApplyLocations}  // 수정된 핸들러 사용
      />
       <Modal 
                isOpen={isEditModalOpen} 
                onClose={() => setIsEditModalOpen(false)} 
                onSave={handleSave}
                name={name}
                email={email}
                phone={phone}
            />
       {isEducationTagModalOpen && (
        <EducationTag
          isOpen={isEducationTagModalOpen}
          onClose={() => setIsEducationTagModalOpen(false)}
          allEducationTags={allEducationTags}
          selectedTags={educationTags}
          onApply={handleEducationTagApply}
        />
      )}
      {isPositionTagModalOpen && (
      <PositionTag
  isOpen={isPositionTagModalOpen}
  onClose={() => setIsPositionTagModalOpen(false)}
  selectedTags={positionTags}
  onApply={handlePositionTagApply}
/>
)}
    </div>
    
  );
};

export default ShowProfile;
