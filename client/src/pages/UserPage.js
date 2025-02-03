import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../component/Header.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import './UserPage.css';
import Header from '../component/Header';
import Config from '../api/Config';
import Api from '../api/api';

import JobCard from '../component/JobCard';

const UserPage = () => {

  const [userData, setUserData] = useState({
    bookmarks: [],        // 초기값을 빈 배열로 설정
    appliedJobs: [],      // 초기값을 빈 배열로 설정
    favoriteCompanies: [] // 초기값을 빈 배열로 설정
  });
  const [jobs, setJobs] = useState([]); 
  const [loading, setLoading] = useState(true); // 로딩 상태 추가
  const navigate = useNavigate();
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [favoriteCompanies, setFavoriteCompanies] = useState([]);
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]); // 지원한 공고 목록 상태 추가
  const [recommendedJobs, setRecommendedJobs] = useState([]); // 추천 공고를 위한 state 추가
  const [recommendLoading, setRecommendLoading] = useState(true);
  
  const isLoggedIn = !!sessionStorage.getItem('user');

    const fetchRecommendedJobs = async () => {
      try {
        setRecommendLoading(true);
        const user = JSON.parse(sessionStorage.getItem('user'));
        
        if (!user) return;
  
        const response = await Api('https://alb.gaenchwis.click/recommendation', 'GET');
        console.log(response)
  
        setRecommendedJobs(response['data']);
      } catch (error) {
        console.error('추천 공고 조회 중 에러:', error);
      } finally {
        setRecommendLoading(false);
      }
    }; 


    useEffect(() => {
      try {
        const storedUserData = sessionStorage.getItem('user');
        if (storedUserData) {
          setUserData(JSON.parse(storedUserData));
          fetchUserData();
        }
      } catch (error) {
        console.error('Error parsing user data from localStorage:', error);
      }
    }, []);
  
    const fetchUserData = async () => {
        try {
          const userData = JSON.parse(sessionStorage.getItem('user'));
        
        if (!userData) {
          console.log('로그인이 필요합니다.');
          return;
        }

        const bookmarkResponse = await Api(
          `${Config.server}:8005/api/v1/bookmarks`,
          'GET',
          null,
          {
            'Content-Type': 'application/json',
          }
        );

        const favoriteResponse = await Api(
          `${Config.server}:8005/api/v1/interest-companies`,
          'GET',
          null,
          {
            'Content-Type': 'application/json',
          }
        );
        const appliedResponse = await Api(
          `${Config.server}:8005/api/v1/applies`,
          'GET',
          null,
          {
            'Content-Type': 'application/json',
          }
        );
        console.log('지원한 공고 데이터:', appliedResponse); // 데이터 확인용 로그

        if (appliedResponse && Array.isArray(appliedResponse['applied_jobs'])) {
          const appliedIds = appliedResponse['applied_jobs'].map(apply => apply.post_id);
          console.log(appliedIds)
          setAppliedJobs(appliedIds);
          console.log('설정된 지원 공고 ID들:', appliedIds);
        }
  
        
        // bookmarkResponse.bookmarks 배열에서 post_id만 추출
        if (bookmarkResponse && bookmarkResponse.bookmarks) {
          const bookmarkIds = bookmarkResponse.bookmarks.map(bookmark => bookmark.post_id);
          setBookmarkedJobs(bookmarkIds);
    
        }

        // 관심기업 데이터 변환
        if (favoriteResponse && favoriteResponse.companies) {
          const allJobPostings = favoriteResponse.companies.flatMap(company => {
            return (company.job_postings || []).map(job => ({
              ...job,
              post_name: job.title,
              company_name: company.company_name,
              company_id: company.company_id,
              PK: `COMPANY#${company.company_id}`,
              SK: `JOB#${job.post_id}`,
              deadline: job.deadline,
              tags: job.tags || []
            }));
          });

          // company_id로 설정하도록 수정
          const companyIds = favoriteResponse.companies.map(company => company.company_id);
          setFavoriteCompanies(companyIds);
          console.log('설정된 관심기업 ID들:', companyIds);
        }

      } catch (error) {
        console.error('사용자 데이터 가져오기 실패:', error);
      }
    };

      useEffect(() => {
        fetchUserData();
      }, []); // 컴포넌트 마운트 시 한 번만 실행
    
    
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
        const data = await Api(`${Config.server}:8003/api/jobs?page=${page}&per_page=10`, 'GET');

        setJobs(data.items);
        setTotalPages(data.total_pages);
      } catch (error) {
        console.error('Error fetching jobs:', error);
      } finally {
        setLoading(false);
      }
    };

    
 
  useEffect(() => {
    if (isLoggedIn) {
      fetchRecommendedJobs();
    }
    fetchJobs(currentPage);
  }, [currentPage]);
  const handleToggleBookmark = (postId) => {
    setBookmarkedJobs(prev => 
      prev.includes(postId) 
        ? prev.filter(id => id !== postId)
        : [...prev, postId]
    );
  };
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    window.scrollTo(0, 0); // 페이지 상단으로 스크롤
  };
  return (
    <div>
      {/* 로그인 상태일 때만 맞춤공고 섹션 표시 */}
      {isLoggedIn && (
        <>
          <h1 className="job-header">
          {userData?.name || '사용자'} 님의 맞춤공고 입니다.
        </h1>
          <div className="job-container">
            {recommendLoading ? (
              <div>맞춤 공고 로딩 중...</div>
            ) : recommendedJobs && recommendedJobs.length > 0 ? (
              recommendedJobs.map((job) => (
                <JobCard
                  key={"Rec"+job[1].post_id}
                  job={job[1]}
                  favoriteCompanies={favoriteCompanies || []}
                  bookmarkedJobs={bookmarkedJobs || []}
                  appliedJobs={appliedJobs || []}
                  onToggleFavorite={toggleFavorite}
                  onToggleBookmark={toggleBookmark}
                  onToggleApplied={toggleApplied}
                />
              ))
            ) : (
              <div>맞춤 공고가 없습니다.</div>
            )}
          </div>
        </>
      )}
      

      <h1 className="job-header">최근 업데이트된 공고입니다.</h1>
      <div className="job-container">
        
        {loading ? (
          <div>로딩 중...</div>
        ) : (
          <>
            {jobs.map(job => (
              <JobCard
                key={"Post"+job.post_id}
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