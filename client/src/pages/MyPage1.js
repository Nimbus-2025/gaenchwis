import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../component/Header';
import SearchResult from './tab/SearchResult';
import Modal from './modal/Edit';
import ShowProfile from './tab/ShowProfile';
import ShowEssay from './tab/ShowEssay';
import ShowBookmark from './tab/ShowBookmark'; 
import Calendar from '../calendar';
import './MyPage1.css';
import LogoutButton from '../component/Logout';
import Jobposting from './UserPage'

const MyPage1 = ({bookmarkedJobs}) => {
  const [userData, setUserData] = useState(JSON.parse(sessionStorage.getItem('user')) || {});
  const [selectedButton, setSelectedButton] = useState('profile');
  const [content, setContent] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const [coverLetter, setCoverLetter] = useState('');
  const [isPopupOpen, setIsPopupOpen] = useState(false); 
  const [searchText, setSearchText] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearchResults, setShowSearchResults] = useState(false);
  
  useEffect(() => {
    const storedUserData = sessionStorage.getItem('user');
    if (storedUserData) {
      try {
        const parsedData = JSON.parse(storedUserData);
        setUserData(parsedData);
      } catch (error) {
        console.error('Error parsing user data from localStorage:', error);
      }
    }
    

    if (!showSearchResults) {
      jobposting();
    }
  }, []);// content 의존성 제거

  const onSearch = (searchQuery) => {
    setSearchText(searchQuery);
    setSelectedButton('search'); // 검색 시 선택된 버튼 상태 변경
    setShowSearchResults(true);
    setContent(<SearchResult searchQuery={searchQuery} />);
  };

const handleSearch = (query) => {
  setSearchQuery(query);
  setShowSearchResults(true);
};

  const jobposting = () => {
    setSelectedButton('job');
    setContent(<Jobposting userData={userData} onSave={handleSaveClick} />);
  };
  const handleSaveClick = (updatedUserData) => {
    setUserData(updatedUserData);
    sessionStorage.setItem('user', JSON.stringify(updatedUserData));
    setIsModalOpen(false);
  };
  const confirmPopup = () => {
    navigate('/'); // firstpage.js로 이동
  };
  const closePopup = () => {
    setIsPopupOpen(false); // 팝업 닫기
  };

  const showProfile = () => {
    if (!userData?.user_id) {
      setIsPopupOpen(true); // 팝업 표시
    } else {
      setSelectedButton('profile');
      setContent(<ShowProfile userData={userData} onSave={handleSaveClick} />);
    }

  const handleShowBookmarks = () => {
    if (!userData?.user_id) {
      setIsPopupOpen(true); // 팝업 표시
    } else {
      setContent(<ShowBookmark bookmarkedJobs={bookmarkedJobs} />); // 북마크된 공고 표시
    }
  };
  };
  const showEssay = () => {
    setSelectedButton('essay');
    setContent(<ShowEssay userData={userData} onSave={handleSaveClick} />);
  };
  const handleShowBookmarks = () => {
    if (!userData?.email) {
      setIsPopupOpen(true); // 팝업 표시
    } else {
      setContent(<ShowBookmark bookmarkedJobs={bookmarkedJobs} />);
    }
  };
  const showBookmark = () => {
     if (!userData?.email) {
      setIsPopupOpen(true); // 팝업 표시
    } else {
    setSelectedButton('bookmark');
    setContent(<ShowBookmark userData={userData} onSave={handleSaveClick} />);
    }
  };

 
  const showCalendar = () => {
    setSelectedButton('calendar');
    setContent(<Calendar />);
  };

  useEffect(() => {
    jobposting(); // 기본 프로필 화면 보여주기
  }, []);

  return (
    <div>
      <Header userData={userData}
        onSearch={onSearch}
      />
  
      <div className="button-logout-container">
        <div className="button-container">
          <button
            className={selectedButton === 'job' ? 'active' : ''}
            onClick={jobposting} 
          >
            채용공고
          </button>
          <button
            className={selectedButton === 'profile' ? 'active' : ''}
            onClick={showProfile}
          >
            프로필
          </button>
          <button
            className={selectedButton === 'bookmark' ? 'active' : ''}
            onClick={showBookmark}
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
          <LogoutButton />
        </div>
      </div>

      <div className="rectangle-container">
        <div className="rectangle">
          {content}
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
      {isPopupOpen && (
        <div className="login-popup">
          <div className="login-popup-content">
            <p>로그인이 필요합니다.</p>
            <button onClick={confirmPopup}>확인</button>
            <button onClick={closePopup}>취소</button>
          </div>
        </div>
      )}
    </div>
);
};

export default MyPage1;