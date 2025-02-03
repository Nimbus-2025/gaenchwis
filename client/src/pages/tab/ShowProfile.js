import React, { useState, useEffect } from 'react';
import LocationTag from '../modal/LocationTag';
import Edit from '../modal/Edit';
import './ShowProfile.css';
import Config from '../../api/Config';
import Proxy from '../../api/Proxy';
import Api from '../../api/api';
import { format } from 'date-fns';
import EducationTag from '../modal/EducationTag';
import PositionTag from '../modal/PositionTag';
import AppliedJobsModal from '../modal/AppliedJobsModal';
import calendarIcon from '../../images/calendar.png';
import motivationIcon from '../../images/motivation.png';



const ShowProfile = ({ userData }) => {
  const [selectedLocations, setSelectedLocations] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
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
  const [dailyQuote, setDailyQuote] = useState(null);
  const [appliedCount, setAppliedCount] = useState(0); // 상태 추가
  const [isAppliedModalOpen, setIsAppliedModalOpen] = useState(false);
  const [favoriteCompanies, setFavoriteCompanies] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
  const [todaySchedules, setTodaySchedules] = useState([]);

  

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
        const response = await Api(`http://localhost:8003/api/tags/education`, 'GET');
      
      if (!response.ok) {
        throw new Error('교육 태그를 가져오는데 실패했습니다');
      }

      const data = await response.json();
      console.log('교육 태그 데이터:', data);
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

  const motivationalQuotes = [
    {
      quote: "성공은 매일 반복한 작은 노력들의 합이다.",
      author: "로버트 콜리어"
    },
    {
      quote: "당신의 직업을 사랑하라. 그러면 평생 일하지 않아도 된다.",
      author: "공자"
    },
    {
      quote: "기회는 준비된 자의 것이다.",
      author: "파스퇴르"
    },
    {
      quote: "오늘 할 수 있는 일을 내일로 미루지 마라.",
      author: "벤자민 프랭클린"
    },
    {
      quote: "꿈을 이루고자 하는 용기만 있다면 모든 꿈을 이룰 수 있다.",
      author: "월트 디즈니"
    },
    {
      quote: "나는 실패한 적이 없다. 그저 작동하지 않는 10,000가지 방법을 발견했을 뿐이다.",
      author: "토마스 에디슨"
    },
    {
      quote: "당신이 포기할 때, 그때가 바로 게임이 끝나는 때다.",
      author: "스튜어트 피어스"
    },
    {
      quote: "성공의 비결은 단 한 가지, 잘할 수 있는 일에 광적으로 집중하는 것이다.",
      author: "톰 모나건"
    },
    {
      quote: "열정을 잃지 않고 실패에서 실패로 걸어가는 것이 성공이다.",
      author: "윈스턴 처칠"
    },
    {
      quote: "당신의 미래는 당신이 지금 무엇을 하고 있느냐에 달려 있다.",
      author: "마하트마 간디"
    }
  ];

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
      
        
        if (data.tags && Array.isArray(data.tags)) {
          const tagNames = data.tags.map(tag => tag.tag_name);
      
          setEducationTags(prev => {
    
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

  
  const openEditModal = () => {
    setIsEditModalOpen(true); // 수정 모달 열기
  };
  const handleModalOpen = () => {
    console.log('모달 열기 시도');
    setIsAppliedModalOpen(true);
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
      const response = await fetch(`http://localhost:8003/api/v1/user/tags/location`, {
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
    
      // 상태 업데이트
      setSelectedLocations(selectedTags);
      setIsModalOpen(false);
    } catch (error) {

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
    const response = await fetch(`http://localhost:8003/api/v1/user/tags/education`, {
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
const fetchAppliedCount = async () => {
  try {
    const response = await Api(
      `${Config.server}:8005/api/v1/applies`,
      'GET',
      null,
      {
        'Content-Type': 'application/json',
      }
    );
    
    if (response && response.applied_jobs) {
      setAppliedJobs(response.applied_jobs);
      setAppliedCount(response.applied_jobs.length);
    }
  } catch (error) {
    console.error('지원한 공고 개수 가져오기 실패:', error);
    setAppliedCount(0);
  }
};
useEffect(() => {
  fetchAppliedCount();
}, []); 
useEffect(() => {
  // 랜덤 명언 선택
  const randomIndex = Math.floor(Math.random() * motivationalQuotes.length);
  setDailyQuote(motivationalQuotes[randomIndex]);
}, []); // 컴포넌트 마운트 시 한 번만 실행



// 토글 함수들
const handleToggleFavorite = async (companyId) => {
  try {
    // 관심기업 토글 로직
    console.log('관심기업 토글:', companyId);
  } catch (error) {
    console.error('관심기업 처리 중 에러:', error);
  }
};

const handleToggleBookmark = async (postId) => {
  try {
    // 북마크 토글 로직
    console.log('북마크 토글:', postId);
  } catch (error) {
    console.error('북마크 처리 중 에러:', error);
  }
};

const handleToggleApplied = async (postId) => {
  try {
    // 지원하기 토글 로직
    console.log('지원하기 토글:', postId);
  } catch (error) {
    console.error('지원하기 처리 중 에러:', error);
  }
};
useEffect(() => {
  const fetchTodaySchedules = async () => {
    try {
      // 오늘 날짜를 YYYYMMDD 형식으로 변환
      const today = new Date();
      const formattedDate = format(today, 'yyyyMMdd');
      
      // API 호출
      const response = await Api(`${Config.server}:8006/api/v1/schedules`, 'GET');
      console.log('일정 데이터:', response);

      // 오늘 날짜의 일정만 필터링
      const todayEvents = response.filter(
        schedule => schedule.schedule_date === formattedDate
      );
      
      setTodaySchedules(todayEvents);
    } catch (error) {
      console.error('일정 조회 중 오류:', error);
    }
  };

  fetchTodaySchedules();
}, []);

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
        <div className="status-item" onClick={() => setIsAppliedModalOpen(true)} style={{ cursor: 'pointer' }}>
          <div className="status-content">
            <span>지원완료</span>
            <div>
            <span className="status-number">{appliedCount}</span>
            </div>
        </div>
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
      <div className="schedule-container">
      {/* 명언 표시 섹션 추가 */}
      {dailyQuote && (
        <div className="daily-motivation">
          <div className="motivation-header">
          <h4>오늘의 동기부여 메시지</h4>
          <img src={motivationIcon} alt="motivation" className="motivation-icon" />
          </div>
          <p className="quote">"{dailyQuote.quote}"</p>
          <p className="author">- {dailyQuote.author}</p>
        </div>
      )}
  
      <div className="today-schedule">
      <div className="schedule-header">
      <p className="today-date">
      {format(new Date(), 'yyyy년 MM월 dd일')}  오늘의 일정입니다.
    </p>
    <img src={calendarIcon} alt="calendar" className="calendar-icon" />
    </div>
    <div className="schedules-container">
          {todaySchedules.length > 0 ? (
            todaySchedules.map((schedule, index) => (
              <div key={index} className="schedule-item">
                <h5 className="schedule-title">{schedule.schedule_title}</h5>
                <p className="schedule-content">{schedule.schedule_content}</p>
              </div>
            ))
          ) : (
            <p className="no-schedule">오늘 예정된 일정이 없습니다.</p>
          )}
          </div>
    </div>
    </div>
    </div>
    </div>
  
      <div>
      
        <div className="info-box-container">
        <h4>My Tag</h4>
        
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
       <Edit
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


 <AppliedJobsModal
        isOpen={isAppliedModalOpen}
        onClose={() => setIsAppliedModalOpen(false)}
        appliedJobs={appliedJobs}
        favoriteCompanies={favoriteCompanies}
        bookmarkedJobs={bookmarkedJobs}
        onToggleFavorite={handleToggleFavorite}
        onToggleBookmark={handleToggleBookmark}
        onToggleApplied={handleToggleApplied}
      />
    
    </div>
    
  );
};

export default ShowProfile;
