import React, { useState, useEffect } from 'react';
import LoadEssayList from '../component/LoadEssayList';
import '../style/essay.css';

function LoadEssay() {
  const [dragLoad, setDragLoad]=useState(false);
  const [dragData, setDragData]=useState(<div></div>);
  const [load,setLoad]=useState(false);
  const [data,setData]=useState(<div></div>);

  useEffect(() => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'dragged' && request.data.title) {
        chrome.runtime.sendMessage({ message: 'log', log: request.data});
        setDragLoad(true);
        setDragData(
          <div className="essay-background">
            <div>
              드래그한 자기소개서
            </div>
            <LoadEssayList 
              data={request.data}
            />
          </div>
        );
        sendResponse({ status: 'dragged loaded'});
      }
      else if (request.message === 'loaded' && request.data.title) {
        setLoad(true);
        setData(
          <div className="essay-background">
            <div>저장된 자기소개서</div>
            <LoadEssayList 
              data={request.data}
            />
          </div>
        );
        sendResponse({ status: 'loaded'});
      }
      return true;
    });
  }, []);

  return (<div className="essay-background">
    {dragLoad && (dragData)}
    {load && (data)}
    {!load && !dragLoad && (
      <div>
        <h2>자기소개서가 없습니다.</h2>
      </div>
    )}
  </div>);
}

export default LoadEssay;
