import React, { useState, useEffect } from 'react';
import LoadEssayList from '../component/LoadEssayList';
import '../style/essay.css';

function LoadEssay() {
  const [dragEssay,setDragEssay]=useState(false);
  const [loadEssay,setLoadEssay]=useState(false);

  const EssaySave = (e, idx) => {
    e.stopPropagation();
    const title=dragEssay.title[idx];
    const content=dragEssay.content[idx];
    chrome.runtime.sendMessage({ 
      message: 'save_dragged_essay', 
      title: [title],
      content: [content]
    }, (response)=>{
      const temp = {...loadEssay};
      temp.title=[title, ...temp.title];
      temp.content=[content, ...temp.content];
      temp.post=[null, ...temp.post];
      temp.date=[response.time, ...temp.date];
      setLoadEssay(temp);
    });
    EssayDelete(e, idx);
  }
  const EssayDelete = async (e, idx) => {
    e.stopPropagation();
    const temp = {...dragEssay};
    temp.title=temp.title.filter((_, i) => i !== idx);
    temp.content=temp.content.filter((_, i) => i !== idx);
    if (temp.title.length > 0){
      setDragEssay(temp);
      await chrome.storage.local.set({
        title: temp.title,
        content: temp.content
      });
    }
    else{
      setDragEssay(false);
      await chrome.storage.local.remove('title');
      await chrome.storage.local.remove('content');
    }
  }

  useEffect(() => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'dragged' && request.data.title) {
        setDragEssay(request.data)
        sendResponse({ status: 'dragged loaded'});
      }
      else if (request.message === 'loaded' && request.data.title) {
        setLoadEssay(request.data)
        sendResponse({ status: 'loaded'});
      }
      return true;
    });
  }, []);

  return (<div className="essay-background">
    {dragEssay && (
      <div className="essay-background essay-background-padding-border-bottom">
        <div>
          드래그한 자기소개서
        </div>
        <LoadEssayList 
          essayData={dragEssay}
          EssaySave={(e, idx)=>EssaySave(e, idx)}
          EssayDelete={(e, idx)=>EssayDelete(e, idx)}
        />
      </div>
    )}
    {loadEssay && (
      <div className="essay-background essay-background-padding-border-bottom">
        <div>저장된 자기소개서</div>
        <LoadEssayList 
          essayData={loadEssay}
        />
      </div>
    )}
    {!loadEssay && !dragEssay && (
      <div>
        <h2>자기소개서가 없습니다.</h2>
      </div>
    )}
  </div>);
}

export default LoadEssay;
