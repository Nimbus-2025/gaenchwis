import React, { useState } from 'react';
import LoadEssayContent from './LoadEssayContent';
import '../style/essay.css';

function LoadEssayList({data}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedTitle, setSelectedTitle] = useState(null);
  const [selectedContent, setSelectedContent] = useState(null);
  const [selectedPost, setSelectedPost] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);

  const ModalOff = () => {
    setIsModalOpen(false);
  };

  const ModalOn = (title, content, post, date) => {
    setSelectedTitle(title);
    setSelectedContent(content);
    setSelectedPost(post);
    setSelectedDate(date);
    setIsModalOpen(true);
  };
  return (
    <div className="essay">
      {
        data.title.map((title, idx) => (
          <div 
            className="list-content"
            key={idx} 
            onClick={
              () => ModalOn(
                title, 
                data.content[idx],
                data.post ? data.post[idx] : data.post,
                data.date ? data.date[idx] : data.date
              )
            }
          >
            <div className="essay_text">문항 : {title}</div>
            {data.date && (
              <div className="essay_text">공고 : {data.post ? data.post[idx] : "지원한 공고 없음"}</div>
            )}
            {data.date && (
              <div className="essay_text">{data.date[idx]}</div>
            )}
          </div>
        ))
      }
      {
        isModalOpen && (
          <LoadEssayContent
            title={selectedTitle} 
            content={selectedContent} 
            post={selectedPost} 
            date={selectedDate} 
            onClose={ModalOff} 
          />
        )
      }
    </div>
  );
}

export default LoadEssayList;
