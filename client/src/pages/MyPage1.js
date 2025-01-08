import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header1 from '../component/Header';
import Modal from './modal/Edit';
import ShowProfile from './tab/ShowProfile';
import ShowEssay from './tab/ShowEssay';
import Calendar from '../calendar';
import heartImage from '../images/heart.png';
import starImage from '../images/star.png';
import './MyPage1.css';
import LogoutButton from '../component/Logout';

const MyPage1 = () => {
  const [userData, setUserData] = useState(JSON.parse(localStorage.getItem('user')) || {});
  const [selectedButton, setSelectedButton] = useState('profile');
  const [content, setContent] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const [coverLetter, setCoverLetter] = useState('');
  useEffect(() => {
    const storedUserData = localStorage.getItem('user');
    if (storedUserData) {
      try {
        const parsedData = JSON.parse(storedUserData);
        setUserData(parsedData);
      } catch (error) {
        console.error('Error parsing user data from localStorage:', error);
      }
    }
  }, []);



  const handleSaveClick = (updatedUserData) => {
    setUserData(updatedUserData);
    localStorage.setItem('user', JSON.stringify(updatedUserData));
    setIsModalOpen(false);
  };

  const showProfile = () => {
    setSelectedButton('profile');
    setContent(<ShowProfile userData={userData} onSave={handleSaveClick} />);
  };
  const showEssay = () => {
    setSelectedButton('essay');
    setContent(<ShowEssay userData={userData} onSave={handleSaveClick} />);
  };

  const showBookmarks = () => {
    setSelectedButton('bookmarks');
    setContent(
      <div className="bookmark-interest-container">
        <div className="section">
          <h2 className="title">북마크 공고 <img src={starImage} alt="북마크" className="star-icon" /></h2>
          <div className="bookmark-box"></div>
        </div>
        <div className="section">
          <h2 className="title">관심기업 공고 <img src={heartImage} alt="관심기업" className="heart-icon" /></h2>
          <div className="bookmark-box"></div>
        </div>
      </div>
    );
  };
  const showCoverLetter = () => {
    setSelectedButton('coverLetter'); 
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

  const showCalendar = () => {
    setSelectedButton('calendar');
    setContent(<Calendar />);
  };

  useEffect(() => {
    showProfile(); // 기본 프로필 화면 보여주기
  }, []);

  return (
    <div>
      <Header1 userData={userData} /> {/* Header1 컴포넌트 적용 */}
  
      <div className="button-logout-container">
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
            북마크 / 관심기업
          </button>
          <button
            className={selectedButton === 'calendar' ? 'active' : ''}
            onClick={showCalendar}
          >
            캘린더
          </button>
          <button
            className={selectedButton === 'essay' ? 'active' : ''}
            onClick={showEssay}
          >
            자기소개서
          </button>
        </div>
  
        <div className="logout-container">
          {userData ? (
            <LogoutButton />
          ) : (
            <button className="header-login-btn" onClick={() => navigate('/')}>
              로그인
            </button>
          )}
        </div>
      </div>
      <div className="rectangle-container">
        <div className="rectangle">{content}</div>
      </div>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
};

export default MyPage1;