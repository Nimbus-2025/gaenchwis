import React, { useState, useEffect } from 'react';

function DetectEssay() {
  const [detect,setDetect]=useState(
    <div>
      <h2>잠시만 기다려주세요!</h2>
    </div>
  );
  useEffect(() => {
    const messageListener = (request, sender, sendResponse) => {
      if (request.message === 'detected_essay') {
        const essay_num=2
        setDetect(
          <div>
            <h2>{essay_num}개의 자기소개서 문항이 탐지되었습니다!</h2>
          </div>
        );
      }
      if (request.message === 'undetected_essay'){
        setDetect(
          <div>
            <h2>탐지된 자기소개서 문항이 없습니다!</h2>
          </div>
        );
      }
    };
  }, []);

  return (
    <div>
      <h2>{detect}</h2>
    </div>
  );
}

export default DetectEssay;
