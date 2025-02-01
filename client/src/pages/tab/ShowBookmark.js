import React, { useState, useEffect } from 'react';
import JobCard from '../../component/JobCard';
import Config from '../../api/Config';
import Api from '../../api/api';
import './ShowBookmark.css';

const ShowBookmark = () => {
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [favoriteCompanies, setFavoriteCompanies] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);

  const fetchBookmarks = async () => {
    try {
      setLoading(true);
      const data = await Api(`${Config.server}:8005/api/v1/bookmarks`, 'GET');
      console.log('받아온 북마크 데이터:', data);
      setBookmarkedJobs(data.bookmarks || []);
    } catch (error) {
      console.error('북마크 목록 조회 중 에러:', error);
      setError('북마크 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const handleBookmarkToggle = async (postId) => {
    try {
      await Api(`${Config.server}:8005/api/v1/bookmark/${postId}`, 'DELETE');
      setBookmarkedJobs(prev => prev.filter(job => job.post_id !== postId));
    } catch (error) {
      console.error('북마크 처리 중 에러:', error);
      alert('북마크 처리에 실패했습니다.');
    }
  };

  const handleFavoriteToggle = (companyName) => {
    setFavoriteCompanies(prev => 
      prev.includes(companyName)
        ? prev.filter(name => name !== companyName)
        : [...prev, companyName]
    );
  };

  const handleAppliedToggle = (postId) => {
    setAppliedJobs(prev => 
      prev.includes(postId)
        ? prev.filter(id => id !== postId)
        : [...prev, postId]
    );
  };

  return (
    <div className="bookmark-interest-container">
      <div className="section">
        <div className="section-header">
          <h2 className="title">북마크 공고</h2>
          <span className="bookmark-count">총 {bookmarkedJobs.length}개</span>
        </div>
        
        <div className="bookmarked-box">
          {loading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>북마크 목록을 불러오는 중...</p>
            </div>
          ) : error ? (
            <div className="error-message">
              <p>{error}</p>
              <button onClick={fetchBookmarks}>다시 시도</button>
            </div>
          ) : bookmarkedJobs.length === 0 ? (
            <div className="empty-message">
              <p>북마크한 공고가 없습니다.</p>
              <p>관심있는 채용공고를 북마크해보세요!</p>
            </div>
          ) : (
            <div className="job-cards-container">
              {bookmarkedJobs.map((job) => (
                <JobCard
                  key={job.post_id}
                  job={job}
                  favoriteCompanies={favoriteCompanies}
                  bookmarkedJobs={bookmarkedJobs.map(job => job.post_id)}
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