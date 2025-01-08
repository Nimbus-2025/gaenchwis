import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Logout.css';


const LogoutButton = () => {
  const [isLogoutPopupOpen, setIsLogoutPopupOpen] = useState(false);
  const navigate = useNavigate();

  // 로그아웃 팝업 보이기
  const showLogoutPopup = () => {
    setIsLogoutPopupOpen(true);
  };

  // 로그아웃 처리
  const handleLogoutConfirm = () => {
    localStorage.removeItem('user'); // 사용자 정보 제거
    navigate('/'); // 홈으로 이동
  };

  // 로그아웃 팝업 닫기
  const closeLogoutPopup = () => {
    setIsLogoutPopupOpen(false);
  };

  return (
    <div>
      {/* 로그아웃 버튼 */}
      <button className="logout-button" onClick={showLogoutPopup}>로그아웃</button>

      {/* 로그아웃 팝업 */}
      {isLogoutPopupOpen && (
        <div className="popup">
          <div className="popup-content">
            <p>로그아웃 하시겠습니까?</p>
            <button onClick={handleLogoutConfirm}>확인</button>
            <button onClick={closeLogoutPopup}>취소</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default LogoutButton;