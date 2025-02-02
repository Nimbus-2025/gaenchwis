import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Logout.css';



const LogoutButton = () => {
  const [isLogoutPopupOpen, setIsLogoutPopupOpen] = useState(false);
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  useEffect(() => {
    const storedUser = sessionStorage.getItem('user');
    if (storedUser) {
      setUserData(JSON.parse(storedUser));
    }
  }, []);

  // 로그아웃 팝업 보이기
  const showLogoutPopup = () => {
    setIsLogoutPopupOpen(true);
  };

  // 로그아웃 처리
  const handleLogoutConfirm = () => {
    sessionStorage.removeItem('user'); // 사용자 정보 제거
    navigate('/'); // 홈으로 이동
  };

  // 로그아웃 팝업 닫기
  const closeLogoutPopup = () => {
    setIsLogoutPopupOpen(false);
  };
  const handleLoginClick = () => {
    navigate('/');
  }

  return (
    <div>
      {/* 로그인 상태에 따라 다른 버튼 표시 */}
      {userData ? (
        <>
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
        </>
      ) : (
        // 로그인 버튼
        <button className="logout-button" onClick={handleLoginClick}>로그인</button>
      )}
    </div>
  );
};

export default LogoutButton;