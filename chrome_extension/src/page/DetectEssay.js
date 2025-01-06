import React, { useState, useEffect } from 'react';
import Button from '../component/Button';
import LoadEssayList from '../component/LoadEssayList';

function DetectEssay() {
  const [detect,setDetect]=useState(
    <div>
      <h2>잠시만 기다려주세요!</h2>
    </div>
  );

  const data="abc"
  const saveessay = () => {
    chrome.runtime.sendMessage({ message: 'page_saveessay', data: data });
  };

  useEffect(() => {
    chrome.runtime.sendMessage({ message: 'crawling' });
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'detected_essay') {
        const essay_num=2;
        setDetect(
          <div>
            <h2>{essay_num}개의 자기소개서 문항이 탐지되었습니다!</h2>
            <h2>저장하시겠습니까?</h2>
            <Button
              title="저장"
              onClick={saveessay}
            />
          </div>
        );
        sendResponse({ message: 'Detected Essay' });
      }
      else if (request.message === 'notsupport'){
        setDetect(
          <div>
            <h2>자기소개서 탐지를 지원하지 않는 사이트입니다.</h2>
            <h2>자기소개서 문항과 내용을 드래그 우클릭하여 추가해보세요!</h2>
            <LoadEssayList 
              data={request.data}
            />
            <Button
              title="저장"
              onClick={saveessay}
            />
          </div>
        );
        sendResponse({ message: 'Not Support' });
      }
      return true;
    });
  }, []);

  return (<div>{detect}</div>);
}

export default DetectEssay;
