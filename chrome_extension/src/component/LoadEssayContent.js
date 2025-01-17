import React from 'react';
import '../style/modal.css'
import '../style/essay.css'

function LoadEssayContent({title,content,post,date,onClose}) {
  return (
    <div className="modal">
      <div className="modal-content">
        {post && (
          <div className="modal-essay-content">
            <div className="essay_text_bold">공고</div>
            <div className="essay_text">{post}</div>
          </div>
        )}
        {date && (
          <div className="modal-essay-content">
            <div className="essay_text">{date}</div>
          </div>
        )}
        <div className="modal-essay-content">
          <div className="essay_text_bold">문항</div>
          <div className="essay_text">{title}</div>
        </div>
        <div className="modal-essay-content modal-essay-min-height">
          <div className="essay_text_bold">내용</div>
          <div className="essay_text">{content ? content : "내용이 없습니다."}</div>
        </div>
        <span className="close" onClick={onClose}>닫기</span>
      </div>
    </div>
  );
}

export default LoadEssayContent;