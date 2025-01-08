import React from 'react';
import './ShowEssay.css';

const ShowEssay = () => {
    
  return (
    <div className="essay-container">
      {/* 검색창 */}
      <div className="search-box">
        <input type="text" placeholder="자기소개서 문항을 검색하세요..." />
        <button className="search-button">검색</button>
        <button className="plus-button"></button>
      </div>

      {/* 사각형 3개 수직으로 배치 */}
      <div className="rectangles">
        <div className="essay-rectangle"> <button className="delete-button"></button></div>
        <div className="essay-rectangle"> <button className="delete-button"></button></div>
        <div className="essay-rectangle"> <button className="delete-button"></button></div>
      </div>
    </div>
  );
};

export default ShowEssay;