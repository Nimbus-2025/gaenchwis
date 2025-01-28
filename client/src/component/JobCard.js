import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart as solidHeart } from '@fortawesome/free-solid-svg-icons';
import { faHeart as regularHeart } from '@fortawesome/free-regular-svg-icons';
import { faStar as solidStar } from '@fortawesome/free-solid-svg-icons';
import { faStar as regularStar } from '@fortawesome/free-regular-svg-icons';
import { faCheck as solidCheck } from '@fortawesome/free-solid-svg-icons'; // 체크 아이콘 추가
import Config from '../api/Config';
import Api from '../api/api';

const JobCard = ({
  job,
  favoriteCompanies,
  bookmarkedJobs,
  appliedJobs,
  onToggleFavorite,
  onToggleBookmark,
  onToggleApplied,
}) => {
  

  // 북마크 상태 초기화
 
  const isBookmarked = bookmarkedJobs.includes(job.post_id);
  const handleBookmarkToggle = async () => {
    try {
      const userData = JSON.parse(sessionStorage.getItem('user'));
    
      if (!userData) {
        alert('로그인이 필요한 서비스입니다.');
        return;
      }
  
      if (isBookmarked) {
        // 북마크 삭제
        await Api(
          `${Config.server}:8005/api/v1/bookmark/${job.post_id}`,
          'DELETE'
        );
      } else {
        // 북마크 추가
        await Api(
          `${Config.server}:8005/api/v1/bookmark`,
          'POST',
          {
            post_id: job.post_id,
            company_id: job.company_id,
            company_name: job.company_name,
            post_name: job.post_name,
            post_url: job.post_url,
            tags: job.tags || [],
            is_closed: job.is_closed || null,
          }
        );
      }
  
      // 부모 컴포넌트에 상태 변경 알림
      if (onToggleBookmark) {
        onToggleBookmark(job.post_id);
      }
    } catch (error) {
      console.error('북마크 처리 중 에러:', error);
      alert(error.message || '북마크 처리 중 오류가 발생했습니다.');
    }
  };
  

  return (
    <div className="job-card">
      <div className="job-header">
        <p className="job-company">
          {job.company_name}
          <FontAwesomeIcon
            icon={favoriteCompanies.includes(job.company_name) ? solidHeart : regularHeart}
            onClick={() => onToggleFavorite(job.company_name)}
            style={{
              cursor: 'pointer',
              marginLeft: '10px',
              color: favoriteCompanies.includes(job.company_name) ? 'red' : 'gray',
            }}
          />
        </p>
        <div className="divider"></div>
        <div className="job-details">
          <h3 className="job-title">
            <a
              href={job.post_url}
              target="_blank"
              rel="noopener noreferrer"
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              {job.post_name}
            </a>
            <FontAwesomeIcon
              icon={isBookmarked ? solidStar : regularStar}
              onClick={handleBookmarkToggle}
              style={{
                cursor: 'pointer',
                marginLeft: '10px',
                color: isBookmarked ? 'gold' : 'gray',
                transition: 'all 0.2s ease',
              }}
              title={isBookmarked ? '북마크 취소' : '북마크 추가'}
            />
            <FontAwesomeIcon
              icon={solidCheck}
              onClick={() => onToggleApplied(job.post_id)}
              style={{
                cursor: 'pointer',
                marginLeft: '10px',
                color: appliedJobs.includes(job.post_id) ? 'red' : 'lightgray',
                transition: 'color 0.2s ease',
              }}
              title={appliedJobs.includes(job.post_id) ? '지원완료' : '지원체크'}
            />
            <div className="job-location-experience">
              {job.is_closed && (
                <span style={{ marginLeft: '100px', fontWeight: 'lighter' }}>
                  마감: {job.is_closed}
                </span>
              )}
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