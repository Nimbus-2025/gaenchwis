import React, { useState, useEffect } from 'react';
import LoginButton from './LoginButton';
import "../style/background.css";

function User() {
  const [login, setLogin]=useState(0);
  const [name, setName]=useState("");
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
      {login===1 && <p>환영합니다! {name}님</p>}
      {login===2 && <LoginButton />}
    </div>
  );
}

export default User;