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
  favoriteCompanies = [],
  bookmarkedJobs,
  appliedJobs,
  onToggleFavorite,
  onToggleBookmark,
  onToggleApplied,
}) => {
  


  
  const handleFavoriteToggle = async (e) => {
    e.stopPropagation();
    try {
      const userData = JSON.parse(sessionStorage.getItem('user'));
    
      if (!userData) {
        alert('로그인이 필요한 서비스입니다.');
        return;
      }

      // company_id 추출 로직 수정
      const company_id = job.company_id || (job.PK ? job.PK.replace('COMPANY#', '') : null);
      
      if (!company_id) {
        console.error('회사 정보를 찾을 수 없습니다:', job);
        alert('회사 정보를 찾을 수 없습니다.');
        return;
      }

      const requestData = {
        company_id: company_id,
        company_name: job.company_name
      };

      const response = await Api(
        `${Config.server}:8005/api/v1/interest-company`,
        'POST',
        requestData,
        {
          
          'Content-Type': 'application/json'
        }
      );

      if (response) {
        onToggleFavorite(company_id);
      }
    } catch (error) {
      console.error('관심기업 처리 중 에러:', error);
      alert('관심기업 처리에 실패했습니다. 다시 시도해주세요.');
    }
  };

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
            deadline: job.jeadline
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
  
  // company_id 가져오기
  const getCompanyId = () => {
    if (job.company_id) return job.company_id;
    if (job.PK) return job.PK.replace('COMPANY#', '');
    return null;
  };

  // 관심기업 여부 확인
  const isFavorite = () => {
    const companyId = getCompanyId();
    return companyId && favoriteCompanies.includes(companyId);
  };




  const handleApplyToggle = async () => {
    try {
      const userData = JSON.parse(sessionStorage.getItem('user'));
    
      if (!userData) {
        alert('로그인이 필요한 서비스입니다.');
        return;
      }

      const isApplied = appliedJobs.includes(job.post_id);
      
      if (isApplied) {
        // 지원 취소
        await Api(
          `${Config.server}:8005/api/v1/apply/${job.post_id}`,
          'DELETE'
        );
      } else {
        // 지원 추가
        await Api(
          `${Config.server}:8005/api/v1/apply`,
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
      if (onToggleApplied) {
        onToggleApplied(job.post_id);
      }
    } catch (error) {
      console.error('지원 처리 중 에러:', error);
      alert(error.message || '지원 처리 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="job-card">
      <div className="job-header">
        <p className="job-company">
          {job.company_name}
          
          <FontAwesomeIcon
            icon={isFavorite() ? solidHeart : regularHeart}
            onClick={handleFavoriteToggle}
            style={{
              cursor: 'pointer',
              marginLeft: '10px',
              color: isFavorite() ? 'red' : 'gray',
              transition: 'color 0.2s ease',
            }}
            title={isFavorite() ? '관심기업 해제' : '관심기업 등록'}
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
              onClick={handleApplyToggle}
              style={{
                cursor: 'pointer',
                marginLeft: '10px',
                color: appliedJobs.includes(job.post_id) ? 'red' : 'lightgray',
                transition: 'color 0.2s ease',
              }}
              title={appliedJobs.includes(job.post_id) ? '지원완료' : '지원체크'}
            />
            <div className="job-location-experience">
              {job.deadline && (
                <span style={{ marginLeft: '100px', fontWeight: 'lighter' }}>
                  마감: {job.deadline}
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