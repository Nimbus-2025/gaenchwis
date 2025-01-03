import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../images/cloud.png'; // 로고 이미지 경로
import '../component/Header.css';
import './UserPage.css';
import Header from '../component/Header';
import './MyPage1.css';
import heartImage from '../images/heart.png';
import starImage from '../images/star.png';
import Calendar from '../calendar';
import Modal from './modal/Edit';

const MyPage1 = () => {
  const [searchText, setSearchText] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [content, setContent] = useState(null); 
  const [userProfile, setUserProfile] = useState(null);
  const [userData, setUserData] = useState(JSON.parse(localStorage.getItem('user')));
  const [coverLetterVisible, setCoverLetterVisible] = useState(false);
  const [isEditing, setIsEditing] = useState(false); // 수정 모드 상태
  const [phoneNumber, setPhoneNumber] = useState(userData?.phoneNumber || ''); // 전화번호 상태
  const navigate = useNavigate();
  const [selectedButton, setSelectedButton] = useState(null); 
  const [isModalOpen, setIsModalOpen] = useState(false); 

useEffect(() => {
  const storedUserData = localStorage.getItem('user');
  if (storedUserData) {
  try {// 로컬 스토리지에서 사용자 정보 가져오기
   const parsedData = JSON.parse(storedUserData);
   setUserData(parsedData); // JSON 문자열을 객체로 변환하여 상태에 저장
} catch (error) {
  console.error('Error parsing user data from localStorage:', error);
}
}
}, []);
useEffect(() => {
  if (userData) {
  showProfile();
  } // 프로필 자동 표시
}, [userData]);

  
  const handleSearch = () => {
    console.log('검색:', searchText);
  };

  const handleLoginClick = () => {
    navigate('/'); // 로그인 페이지로 이동
  };

  const handleMyPageClick = () => {
    navigate('/mypage'); // 마이페이지로 이동
  };
  const handleLogoutClick = () => {
    // 로그아웃 처리
    localStorage.removeItem('user'); // 로컬 스토리지에서 사용자 정보 삭제
    navigate('/'); // 메인 페이지로 이동
  };
  const handleSaveClick = () => {
    const updatedUserData = { ...userData, phoneNumber }; // 전화번호 추가
    setUserData(updatedUserData); // 상태 업데이트
    localStorage.setItem('user', JSON.stringify(updatedUserData)); // 로컬 스토리지에 저장
    setIsModalOpen(false); // 모달 닫기
};
  const showProfile = () => {
    setSelectedButton('profile');
    setContent(
      <div>
      <h2 style={{ marginLeft: '20px' }}>개인정보</h2>
      <div className="profile-info">
      <div className="profile-header">
              <div className="profile-picture">
              <img src={userData.profileImage} alt="Profile" className="profile-image" />
              </div>
              <div className="profile-details">
              <p>이름: {userData?.name || '정보 없음'}</p>
              <p>전화번호: {userData.phoneNumber || '등록되지 않음'}</p> {/* 전화번호 표시 */}
              <p>이메일 주소: {userData?.email || '정보 없음'}</p>
              </div>
          </div>
            <button className="edit-button" onClick={() => setIsModalOpen(true)}>개인정보 수정</button> {/* 수정 버튼 */}
          </div>
        <div>
          <h2 style={{ marginLeft: '20px', marginTop: '70px' }}>태그</h2>
          <div className="info-container">
          <div className="info-box">
                  <h4>지역</h4>
                  <div className="tag-list">
                
              </div>
              </div>
              <div className="info-box">
                  <h4>관심 직무</h4>
                  <div className="tag-list">
                  
                  
              </div>
              </div>
              <div className="info-box">
                  <h4>학력 및 경력</h4>
                  <div className="tag-list">
              </div>
              </div>
              <div className="info-box">
                  <h4>소유 자격증</h4>
                  <div className="tag-list">
              </div>
              </div>
              </div>
          </div>
          <Modal 
                isOpen={isModalOpen} 
                onClose={() => setIsModalOpen(false)} 
                onSave={handleSaveClick} 
                phoneNumber={phoneNumber} 
                setPhoneNumber={setPhoneNumber} 
            />
      </div>
    );
};

const showBookmarks = () => {
  setSelectedButton('bookmarks');
    setContent(
      <div className="bookmark-interest-container">
            <div className="section">
                <h2 className="title">북마크 공고
                <img src={starImage} className="star-icon" /> {/* 별 이미지 추가 */}
                </h2>
                <div className="bookmark-box"/> 
            </div>
            <div className="section">
                <h2 className="title">관심기업 공고
                <img src={heartImage} className="heart-icon" /> {/* 별 이미지 추가 */}
                </h2>
                <div className="bookmark-box"></div> 
            </div>
        </div>
    );
};

const showCalendar = () => {
    setSelectedButton('calendar'); 
    setContent(
      <div className="box"> {/* 사각형 */}
          <Calendar /> {/* 캘린더 컴포넌트 */}
      </div>
    );
};

const showCoverLetter = () => {
  setContent(
    <div style={{ marginTop: '20px', width: '100%' }}>
        <textarea
            rows="4"
            cols="50"
            placeholder="자기소개서를 입력하세요..."
            value={coverLetter}
            onChange={(e) => setCoverLetter(e.target.value)}
            style={{ width: '100%', marginBottom: '10px' }} // 텍스트 영역 스타일
        />
        <button onClick={saveCoverLetter}>저장</button>
    </div>
);
};

const saveCoverLetter = () => {
  setSelectedButton('coverLetter');
  localStorage.setItem('coverLetter', coverLetter); // 로컬 스토리지에 자기소개서 저장
        setCoverLetter(''); // 입력 필드 초기화
        setContent(null); // 
};


  return (
    <div>
      <Header 
        userData={userData} 
        onLogout={handleLogoutClick} 
        searchText={searchText} 
        setSearchText={setSearchText} 
        onSearch={handleSearch} 
        handleMyPageClick={handleMyPageClick} 
      />
    
    <div className="button-container">
                <button 
                    className={selectedButton === 'profile' ? 'active' : ''} 
                    onClick={showProfile}
                >
                    프로필
                </button>
                <button 
                    className={selectedButton === 'bookmarks' ? 'active' : ''} 
                    onClick={showBookmarks}
                >
                    북마크 및 관심기업
                </button>
                <button 
                    className={selectedButton === 'calendar' ? 'active' : ''} 
                    onClick={showCalendar}
                >
                    캘린더
                </button>
                <button 
                    className={selectedButton === 'coverLetter' ? 'active' : ''} 
                    onClick={showCoverLetter}
                >
                    자기소개서
                </button>
            </div>
            <div className="rectangle-container"> 
                <div className="rectangle">
                    {content}
                </div>
            </div>
        </div>
       
  );
};
export default MyPage1;