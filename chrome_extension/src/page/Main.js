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
      }
      if (request.message === 'move_page_detectessay') {
        setPage(<DetectEssay />);
      }
      if (request.message === 'move_page_loadessay') {
        setPage(<LoadEssay />);
      }
      if (request.message === 'move_page_saveessay') {
        setPage(<SaveEssay />);
      }
    });
  }, []);

  return (<div>{page}</div>);
}

export default Main;
