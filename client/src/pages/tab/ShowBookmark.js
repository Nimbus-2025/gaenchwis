import React, { useState, useEffect } from 'react';
import heartImage from '../../images/heart.png';
import starImage from '../../images/star.png';
import JobCard from '../../component/JobCard';
import Config from '../../api/Config';
import Api from '../../api/api';
import './ShowBookmark.css';


const ShowBookmark = () => {
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 북마크 목록 가져오기
  const fetchBookmarks = async () => {
    try {
      const data = await Api(`${Config.server}:8005/api/v1/bookmarks`, 'GET');
      console.log('받아온 북마크 데이터:', data);  // 데이터 확인용 로그
      setBookmarkedJobs(data.bookmarks || []); // 빈 배열을 기본값으로 설정
    } catch (error) {
      console.error('북마크 목록 조회 중 에러:', error);
      setBookmarkedJobs([]); // 에러 시 빈 배열로 설정
    }
  };

  useEffect(() => {
    fetchBookmarks();
  }, []);

  // 북마크 상태가 변경될 때마다 목록 새로고침
  const handleBookmarkToggle = async (job) => {
    try {
      if (bookmarkedJobs.some(bookmark => bookmark.post_id === job.post_id)) {
        // 북마크 삭제
        await Api(`${Config.server}:8005/api/v1/bookmark/${job.post_id}`, 'DELETE');
      } else {
        // 북마크 추가
        await Api(`${Config.server}:8005/api/v1/bookmark`, 'POST', {
          post_id: job.post_id,
          company_id: job.company_id,
          company_name: job.company_name,
          post_name: job.post_name,
          post_url: job.post_url,
          tags: job.tags || [],
          is_closed: job.is_closed || null
        });
      }
      // 북마크 목록 새로고침
      fetchBookmarks();
    } catch (error) {
      console.error('북마크 처리 중 에러:', error);
      alert(error.message || '북마크 처리 중 오류가 발생했습니다.');
    }
  };
  console.log('현재 상태 - loading:', loading);
  console.log('현재 상태 - bookmarkedJobs:', bookmarkedJobs);

  return (
    <div className="bookmark-interest-container">
      <div className="section">
        <h2 className="title">
          북마크 공고 <img src={starImage} alt="북마크" className="star-icon" />
        </h2>
        <div className="bookmark-box">
          {loading ? (
            <div className="loading">로딩 중...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : bookmarkedJobs.length === 0 ? (
            <div className="empty-message">북마크한 공고가 없습니다.</div>
          ) : (
            <div className="bookmarked-jobs">
              {bookmarkedJobs.map((job) => (
                <div key={job.post_id} className="job-card">
                  <h3>{job.post_name}</h3>
                  <p>작성일: {new Date(job.created_at).toLocaleDateString('ko-KR')}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};


export default ShowBookmark;