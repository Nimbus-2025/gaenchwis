import React, { useState, useEffect } from 'react';

function LoadEssay() {
  const [load,setLoad]=useState(
    <div>
      <h2>불러오는 중입니다....</h2>
    </div>
  );

  useEffect(() => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'loaded') {
        setLoad(
          <div>
            <h2>불러왔습니다!</h2>
          </div>
        );

        sendResponse({ status: 'loaded'})
        return true;
      }
    });
  }, []);

  return (<div>{load}</div>);
}

export default LoadEssay;
