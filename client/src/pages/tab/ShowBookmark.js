import React, { useState, useEffect } from 'react';
import JobCard from '../../component/JobCard';
import Config from '../../api/Config';
import Api from '../../api/api';
import './ShowBookmark.css';
import starIcon from '../../images/star.png'; // 이미지 import
import heartIcon from '../../images/heart.png';
const ShowBookmark = () => {
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
  const [interestedJobs, setInterestedJobs] = useState([]); // 관심기업 공고
  const [loading, setLoading] = useState({
    bookmarks: true,
    interested: true
  });
  const [error, setError] = useState({
    bookmarks: null,
    interested: null
  });
  const [favoriteCompanies, setFavoriteCompanies] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);
  const [jobs, setJobs] = useState([]); // jobs 상태 추가


  const fetchAppliedJobs = async () => {
    try {
      const response = await Api(
        `${Config.server}:8005/api/v1/applies`,
        'GET'
      );
      
      if (response && response.applied_jobs) {
        const appliedIds = response.applied_jobs.map(apply => apply.post_id);
        setAppliedJobs(appliedIds);
      }
    } catch (error) {
      console.error('지원한 공고 목록 가져오기 실패:', error);
      setAppliedJobs([]);
    }
  };
  const fetchBookmarks = async () => {
    try {
      setLoading(true);
      const data = await Api(`${Config.server}:8005/api/v1/bookmarks`, 'GET');
      setBookmarkedJobs(data.bookmarks || []);
    } catch (error) {
      console.error('북마크 목록 조회 중 에러:', error);
      setError(prev => ({ ...prev, bookmarks: '북마크 목록을 불러오는데 실패했습니다.' }));
    } finally {
      setLoading(false);
    }
  };


  const handleBookmarkToggle = async (postId) => {
    try {
      await Api(`${Config.server}:8005/api/v1/bookmark/${postId}`, 'DELETE');
      setBookmarkedJobs(prev => prev.filter(job => job.post_id !== postId));
    } catch (error) {
      console.error('북마크 처리 중 에러:', error);
      alert('북마크 처리에 실패했습니다.');
    }
  };

  const handleFavoriteToggle = async (companyName) => {
    try {
      // 관심기업 토글 API 호출 (필요한 경우)
      setFavoriteCompanies(prev => 
        prev.includes(companyName)
          ? prev.filter(name => name !== companyName)
          : [...prev, companyName]
      );
      // 관심기업 목록이 변경되면 공고 목록 다시 불러오기
      
    } catch (error) {
      console.error('관심기업 처리 중 에러:', error);
      alert('관심기업 처리에 실패했습니다.');
    }
  };


  const handleAppliedToggle = (postId) => {
    setAppliedJobs(prev => 
      prev.includes(postId)
        ? prev.filter(id => id !== postId)
        : [...prev, postId]
    );
  };
  

  // 관심기업 목록 가져오기
  const fetchFavoriteCompanies = async () => {
    try {
      const userData = JSON.parse(sessionStorage.getItem('user'));
    
      if (!userData) {
        alert('로그인이 필요한 서비스입니다.');
        return;
      }
  
      const response = await Api(
        `${Config.server}:8005/api/v1/interest-companies`,
        'GET',
      );
  
      // 응답 구조 확인을 위한 디버깅
      if (response) {
        
        // response.companies가 있는 경우
        if (response.companies && Array.isArray(response.companies)) {
          const allJobPostings = response.companies.flatMap(company => {
            return (company.job_postings || []).map(job => {
              return {
                ...job,
                post_name: job.title,
                company_name: company.company_name,
                company_id: company.company_id,
                PK: `COMPANY#${company.company_id}`,
                SK: `JOB#${job.post_id}`,
                deadline: job.deadline,
                tags: job.tags || []
              };
            });
          });
  
          setJobs(allJobPostings);
  
          const companyIds = response.companies.map(company => company.company_id);
          setFavoriteCompanies(companyIds);
        }
  
      }
    } catch (error) {
      console.error('관심기업 목록 가져오기 실패:', error);
      console.error('에러 상세:', error.response || error);
      setJobs([]);
      setFavoriteCompanies([]);
    }
  };

  // 컴포넌트 마운트 시 데이터 가져오기
  useEffect(() => {
    fetchFavoriteCompanies();
    fetchBookmarks();
    fetchAppliedJobs();
  }, []);


  return (
    <div className="bookmark-interest-container">
      <div className="section">
        <div className="section-header">
        <div className="title-with-icon">
        <h2 className="bookmark-title">북마크 공고</h2>
        <img src={starIcon} alt="star" className="star-icon" />
        </div>
          <span className="bookmark-count">총 {bookmarkedJobs.length}개</span>
        </div>
        
        <div className="bookmarked-box">
          {loading.bookmarks ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>북마크 목록을 불러오는 중...</p>
            </div>
          ) : error.bookmarks ? (
            <div className="error-message">
              <p>{error.bookmarks}</p>
              <button onClick={fetchBookmarks}>다시 시도</button>
            </div>
          ) : (
            <div className="job-cards-container">
              {bookmarkedJobs.map((job) => (
                <JobCard
                  key={job.post_id}
                  job={job}
                  favoriteCompanies={favoriteCompanies}
                  bookmarkedJobs={bookmarkedJobs.map(j => j.post_id)}
                  appliedJobs={appliedJobs}
                  onToggleFavorite={handleFavoriteToggle}
                  onToggleBookmark={handleBookmarkToggle}
                  onToggleApplied={handleAppliedToggle}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="section">
        <div className="section-header">
        <div className="title-with-icon">
          <h2 className="bookmark-title">관심기업 공고</h2>
          <img src={heartIcon} alt="heart" className="heart-icon" />
          </div>
          <span className="bookmark-count">총 {jobs.length}개</span>
        </div>
        
        <div className="company-box">
          {loading.interested ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>관심기업 공고를 불러오는 중...</p>
            </div>
          ) : error.interested ? (
            <div className="error-message">
              <p>{error.interested}</p>
            </div>
          ) : (
            <div className="job-cards-container">
              {jobs.map((job) => (
                <JobCard
                  key={job.post_id}
                  job={job}
                  favoriteCompanies={favoriteCompanies}
                  bookmarkedJobs={bookmarkedJobs.map(j => j.post_id)}
                  appliedJobs={appliedJobs}
                  onToggleFavorite={handleFavoriteToggle}
                  onToggleBookmark={handleBookmarkToggle}
                  onToggleApplied={handleAppliedToggle}
                />
              ))}
            </div>
      )}
      </div>
    </div>
  </div>
  );
};

export default ShowBookmark;