import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../component/Button';

function Main() {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript({
        target: { tabId: tabs[0].id },
        function: () => {
          chrome.runtime.sendMessage({ message: 'crawling' });
        }
      });
    });
    navigate("/detectessay")
  };

  return (
    <div>
      <h4>자기소개서 관리 서비스입니다!</h4>
      <h4>현재 페이지에서 자기소개서를 탐색할까요?</h4>
      <Button
        title="탐색"
        onClick={handleButtonClick}
      />
    </div>
  );
}

export default Main;
