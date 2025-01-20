import React, { useState, useEffect } from 'react';
import Home from './Home';
import DetectPost from './DetectPost';
import LoadEssay from './LoadEssay'
import '../style/background.css';

function Main() {
  const [page,setPage]=useState(<Home />);
  
  useEffect(() => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'move_page_main') {
        setPage(<Home />);
        sendResponse({ move: 'Page Home' });
      }
      else if (request.message === 'move_page_detectpost') {
        chrome.storage.local.get("user_id", (result)=>{
          if (result.user_id){
            setPage(<DetectPost />);
            sendResponse({ move: 'Page DetectPost' });
          }
          else{
            alert("로그인이 필요합니다.")
          }
        })
      }
      else if (request.message === 'move_page_loadessay') {
        chrome.storage.local.get("user_id", (result)=>{
          if (result.user_id){
            setPage(<LoadEssay />);
            sendResponse({ move: 'Page LoadEssay' });
          }
          else{
            alert("로그인이 필요합니다.")
          }
        })
      }
      return true;
    });
  }, []);

  return (<div className="full">{page}</div>);
}

export default Main;
