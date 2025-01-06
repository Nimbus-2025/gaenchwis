import React from 'react';
import '../style/LoadEssayContent.css'

function LoadEssayContent({title,content,onClose}) {
  return (
    <div className="modal">
      <div className="modal-content">
        <span onClick={onClose}>abc</span>
        <div>
          <p>{title}</p>
        </div>
        <div>
          <p>{content}</p>
        </div>
      </div>
    </div>
  );
}

export default LoadEssayContent;