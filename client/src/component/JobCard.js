import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart as solidHeart } from '@fortawesome/free-solid-svg-icons';
import { faHeart as regularHeart } from '@fortawesome/free-regular-svg-icons';
import { faStar as solidStar } from '@fortawesome/free-solid-svg-icons';
import { faStar as regularStar } from '@fortawesome/free-regular-svg-icons';
import { faCheck as solidCheck } from '@fortawesome/free-solid-svg-icons';  // 체크 아이콘 추가


const JobCard = ({ 
  job, 
  favoriteCompanies, 
  bookmarkedJobs, 
  appliedJobs, 
  onToggleFavorite, 
  onToggleBookmark,
  onToggleApplied 
}) => {
  return (
    <div className="job-card">
      <div className="job-header">
        <p className="job-company">
          {job.company_name}
          <FontAwesomeIcon
            icon={favoriteCompanies.includes(job.company_name) ? solidHeart : regularHeart}
            onClick={() => onToggleFavorite(job.company_name)}
            style={{ cursor: 'pointer', marginLeft: '10px', color: favoriteCompanies.includes(job.company_name) ? 'red' : 'gray' }}
          />
        </p>
        <div className="divider"></div>
        <div className="job-details">
          <h3 className="job-title">
            <a href={job.post_url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
              {job.post_name}
            </a>
            <FontAwesomeIcon 
              icon={bookmarkedJobs.includes(job.post_id) ? solidStar : regularStar}
              onClick={() => onToggleBookmark(job.post_id)}
              style={{ cursor: 'pointer', marginLeft: '10px', color: bookmarkedJobs.includes(job.post_id) ? 'gold' : 'gray' }}
            />
            <FontAwesomeIcon 
              icon={solidCheck}
              onClick={() => onToggleApplied(job.post_id)}
              style={{ 
                cursor: 'pointer', 
                marginLeft: '10px', 
                color: appliedJobs.includes(job.post_id) ? 'red' : 'lightgray',
                transition: 'color 0.2s ease'
              }}
              title={appliedJobs.includes(job.post_id) ? "지원완료" : "지원체크"}
              />
              <div className="job-location-experience">
            {job.is_closed && <span style={{ marginLeft: '100px', fontWeight: 'lighter' }}>마감: {job.is_closed}</span>}
          </div>
          </h3>
          <div className="job-tags">
            {job.tags && job.tags.length > 0 ? (
              job.tags.map((tag, index) => (
                <span key={index} className="job-tag">
                  {tag}
                </span>
              ))
            ) : (
              <span className="no-tags">태그 없음</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobCard;