import React, { useState } from 'react';
import LoadEssayContent from './LoadEssayContent';

function LoadEssayList({data}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTitle, setSelectedTitle] = useState("");
  const [selectedContent, setSelectedContent] = useState("");

  const ModalOff = () => {
    setIsModalOpen(false);
  };

  const ModalOn = (title, content) => {
    setSelectedTitle(title);
    setSelectedContent(content);
    setIsModalOpen(true);
  };
  return (
    <div>
      {
        data['title'].map((title, idx) => (
          <div key={idx} onClick={() => ModalOn(title, data['content'][idx])}>
            <p>{title}</p>
          </div>
        ))
      }
      {
        isModalOpen && (
          <LoadEssayContent
            title={selectedTitle} 
            content={selectedContent} 
            onClose={ModalOff} 
          />
        )
      }
    </div>
  );
}

export default LoadEssayList;
