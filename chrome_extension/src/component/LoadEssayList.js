import React, { useState } from 'react';
import LoadEssayContent from './LoadEssayContent';
import DeleteImage from '../image/delete.png'
import SaveImage from '../image/save.png'
import '../style/essay.css';
import "../style/icon.css";

function LoadEssayList({essayData, EssaySave=null, EssayDelete=null}) {
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
        essayData.title.map((title, idx) => (
          <div 
            className="list-content"
            onClick={
              () => ModalOn(
                title, 
                essayData.content[idx],
                essayData.post?.[idx] ? essayData.post[idx] : essayData.post,
                essayData.date?.[idx] ? essayData.date[idx] : essayData.date
              )
            }
          >
            {essayData.date && (
              <div className="essay_text">{essayData.date[idx]}</div>
            )}
            {!essayData.date && EssaySave && (
              <div className="essay-icon">
                <img 
                  onClick={(e)=>EssayDelete(e, idx)}
                  src={DeleteImage} 
                  className="delete-icon" 
                />
                <img 
                  onClick={(e)=>EssaySave(e, idx)}
                  src={SaveImage} 
                  className="save-icon" 
                />
              </div>
            )}
            <div className="essay_text">문항 : {title} </div>
            {essayData.date && (
              <div className="essay_text">공고 : {essayData.post?.[idx] ? essayData.post[idx] : "지원한 공고 없음"}</div>
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
