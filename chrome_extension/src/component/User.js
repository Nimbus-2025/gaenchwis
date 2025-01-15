import React, { useState, useEffect } from 'react';
import LoginButton from './LoginButton';
import TextButton from './TextButton';
import "../style/background.css";

function User() {
  const [login, setLogin]=useState(0);
  const [name, setName]=useState("");
  const [logoutPopup, setLogoutPopup]=useState(false);

  const togglePopup = () => {
    setLogoutPopup(!logoutPopup);
  };

  const handleLogout = () => {
    setLogoutPopup(false);
    chrome.runtime.sendMessage({ message: "logout" });
  };

  useEffect(() => {
    chrome.storage.local.get("access_token",(result)=>{
      if (result.access_token){
        setLogin(1);
        chrome.storage.local.get("name",(result)=>{
          setName(result.name);
        });
      }
      else{
        setLogin(2);
      }
    });
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'login_success'){
        setLogin(1);
        chrome.storage.local.get("name",(result)=>{
          setName(result.name);
        });
        sendResponse({ message: 'User header login state' });
      }
      else if (request.message === 'logout_success'){
        setLogin(2);
        setName("");
        sendResponse({ message: 'User header logout state' });
      }
      return true;
    });
  }, []);

  return (
    <div className="header-div">
      {login===1 && <TextButton 
        title={`환영합니다! ${name}님`} 
        onClick={togglePopup} 
        login={true} 
      />}
      {login===2 && <LoginButton />}
      {logoutPopup && (
        <div className="popup">
          <TextButton
            title="Logout"
            onClick={handleLogout}
            login={true} 
          />
        </div>
      )}
    </div>
  );
}

export default User;