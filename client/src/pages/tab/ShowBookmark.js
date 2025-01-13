import React from 'react';
import heartImage from '../../images/heart.png';
import starImage from '../../images/star.png';
import dummyJobListings from './DummyData'; 
const ShowBookmark = ({bookmarkedJobs=[]}) => {
  const bookmarkedResults = dummyJobListings.filter(job => bookmarkedJobs.includes(job._id));
  return (
      <div className="bookmark-interest-container">
        <div className="section">
          <h2 className="title">북마크 공고 <img src={starImage} alt="북마크" className="star-icon" /></h2>
          <div className="bookmark-box"> {bookmarkedResults.length > 0 ? (
        bookmarkedResults.map(job => (
          <div key={job._id} className="bookmark-box">
            <h3>{job.title}</h3>
            <p>{job.company}</p>
            <p>{job.location}</p>
          </div>
        ))
      ) : (
        <p>북마크된 공고가 없습니다.</p>
      )}
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