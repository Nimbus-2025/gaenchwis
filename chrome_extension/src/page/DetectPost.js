import React, { useState, useEffect } from 'react';
import Post from '../component/Post';

function DetectPost() {
  const [detect,setDetect]=useState(
    <div>
      <h2>잠시만 기다려주세요!</h2>
    </div>
  );


  useEffect(() => {
    chrome.runtime.sendMessage({ message: 'crawling' });
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'detected_post') {
        if (request.success){
          setDetect(
            <Post postData={request.data} post_id={request.post_id}/>
          );
        }
        else{
          setDetect(
            <div>
              <h2>확인할 수 없는 공고입니다!</h2>
            </div>
          )
        }
        sendResponse({ message: 'Detected Post' });
      }
      else if (request.message === 'support'){
        setDetect(
          <div>
            <h2>지원하는 사이트입니다!</h2>
            <h2>채용 공고에 들어가 지원해보세요!</h2>
          </div>
        );
        sendResponse({ message: 'Support' });
      }
      else if (request.message === 'notsupport'){
        setDetect(
          <div>
            <h2>지원하지 않는 사이트입니다.</h2>
          </div>
        );
        sendResponse({ message: 'Not Support' });
      }
      return true;
    });
  }, []);

  return (<div>{detect}</div>);
}

export default DetectPost;
