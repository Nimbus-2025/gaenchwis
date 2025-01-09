import React, { useState, useEffect } from 'react';
import Home from './Home';
import DetectEssay from './DetectEssay';
import LoadEssay from './LoadEssay'
import SaveEssay from './SaveEssay';

function Main() {
  const [page,setPage]=useState(<Home />);

  useEffect(() => {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.message === 'move_page_main') {
        setPage(<Home />);
        sendResponse({ move: 'Page Home' });
      }
      else if (request.message === 'move_page_detectessay') {
        setPage(<DetectEssay />);
        sendResponse({ move: 'Page DetectEssay' });
      }
      else if (request.message === 'move_page_loadessay') {
        setPage(<LoadEssay />);
        sendResponse({ move: 'Page LoadEssay' });
      }
      else if (request.message === 'move_page_saveessay') {
        setPage(<SaveEssay />);
        sendResponse({ move: 'Page SaveEssay' });
      }
      return true;
    });
  }, []);

  return (<div>{page}</div>);
}

export default Main;
