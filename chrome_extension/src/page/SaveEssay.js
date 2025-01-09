import React, { useState, useEffect } from 'react';

function SaveEssay() {
  const [save,setSave]=useState(
    <div>
      <h2>저장하는 중입니다....</h2>
    </div>
  );

  useEffect(() => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'saved') {
        setSave(
          <div>
            <h2>저장되었습니다!</h2>
          </div>
        );

        setTimeout(() => {
          chrome.runtime.sendMessage({ message: 'save_to_page_main' });
        }, 2000);
        
        sendResponse({ status: 'saved' });
      }
      return true;
    });
  }, []);

  return (<div>{save}</div>);
}

export default SaveEssay;
