import React from 'react';
import heartImage from '../../images/heart.png';
import starImage from '../../images/star.png';
 
const ShowBookmark = () => {
  
  return (
      <div className="bookmark-interest-container">
        <div className="section">
          <h2 className="title">북마크 공고 <img src={starImage} alt="북마크" className="star-icon" /></h2>
          <div className="bookmark-box"> 
        
    
    </div>
    </div>
        <div className="section">
          <h2 className="title">관심기업 공고 <img src={heartImage} alt="관심기업" className="heart-icon" /></h2>
          <div className="bookmark-box"></div>
        </div>
      </div>
    );
  
};

export default ShowBookmark;