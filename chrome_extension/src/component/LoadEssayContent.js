import React from 'react';
import '../style/modal.css'
import '../style/essay.css'

function LoadEssayContent({title,content,onClose}) {
  return (
    <div className="modal">
      <div className="modal-content">
        <div className="title">
          <p>{title}</p>
        </div>
        <div className="content">
          <p>{content!=null ? content : "내용을 입력해주세요."}</p>
        </div>
        <span className="close" onClick={onClose}>닫기</span>
      </div>
    </div>
  );
}

export default LoadEssayContent;