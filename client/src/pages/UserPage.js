import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../component/Header.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import './UserPage.css';
import Header from '../component/Header';

import JobCard from '../component/JobCard';

const UserPage = () => {

  const [userData, setUserData] = useState(null);
  const [jobs, setJobs] = useState([]); 
  const [loading, setLoading] = useState(true); // 로딩 상태 추가
  const navigate = useNavigate();
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
    const [favoriteCompanies, setFavoriteCompanies] = useState([]);
    const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
    const [appliedJobs, setAppliedJobs] = useState([]); // 지원한 공고 목록 상태 추가

    const toggleFavorite = (company) => {
      setFavoriteCompanies((prev) => 
        prev.includes(company) ? prev.filter(c => c !== company) : [...prev, company]
      );
    };

  const toggleBookmark = (jobId) => {
    setBookmarkedJobs((prev) => 
      prev.includes(jobId) ? prev.filter(id => id !== jobId) : [...prev, jobId]
    );
  };
  const toggleApplied = (jobId) => {
    setAppliedJobs((prev) => 
      prev.includes(jobId) ? prev.filter(id => id !== jobId) : [...prev, jobId]
    );
  };

  const handleLoginClick = () => {
    navigate('/'); // 로그인 페이지로 이동
  };

  const handleLogoutClick = () => {
    // 로그아웃 처리
    sessionStorage.removeItem('user'); // 로컬 스토리지에서 사용자 정보 삭제
    navigate('/'); // 메인 페이지로 이동
  };


  useEffect(() => {
    try {
      const storedUserData = sessionStorage.getItem('user');
      if (storedUserData) {
        setUserData(JSON.parse(storedUserData));
      }
    } catch (error) {
      console.error('Error parsing user data from localStorage:', error);
    }
  }, []);



    const fetchJobs = async (page) => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5001/api/jobs?page=${page}&per_page=10`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setJobs(data.items);
        setTotalPages(data.total_pages);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      } finally {
        setLoading(false);
      }
    };

 
  useEffect(() => {
    fetchJobs(currentPage);
  }, [currentPage]);

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    window.scrollTo(0, 0); // 페이지 상단으로 스크롤
  };
  return (
    <div>
      <h1 className="job-header">최근 업데이트된 공고입니다.</h1>
      <div className="job-container">
        
        {loading ? (
          <div>로딩 중...</div>
        ) : (
          <>
            {jobs.map(job => (
              <JobCard
                key={job.post_id}
                job={job}
                favoriteCompanies={favoriteCompanies}
                bookmarkedJobs={bookmarkedJobs}
                appliedJobs={appliedJobs} 
                onToggleFavorite={toggleFavorite}
                onToggleBookmark={toggleBookmark}
                onToggleApplied={toggleApplied}
              />
            ))}
            
            {/* 페이지네이션 버튼 */}
            <div className="pagination-container">
              <div className="pagination">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  이전 페이지
                </button>
                {Array.from({ length: Math.min(totalPages, 10) }, (_, index) => (
                  <button
                    key={index + 1}
                    onClick={() => handlePageChange(index + 1)}
                    style={{ fontWeight: currentPage === index + 1 ? 'bold' : 'normal' }}
                  >
                    {index + 1}
                  </button>
                ))}
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}
                >
                  다음 페이지
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default UserPage;