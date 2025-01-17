import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './SearchResult.css';
import JobCard from '../../component/JobCard';

const ITEMS_PER_PAGE = 10; // 페이지당 공고 
const SearchResult = ({ searchQuery }) => {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false); 
  const [error, setError] = useState(null);  // 에러 상태 추가
  const location = useLocation();  // location 훅 사용
  const [favoriteCompanies, setFavoriteCompanies] = useState([]); // 관심 기업 상태
  const [currentPage, setCurrentPage] = useState(1);
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]); // 북마크된 공고 상태
  const [totalPages, setTotalPages] = useState(0);
  const [appliedJobs, setAppliedJobs] = useState([]); // 지원한 공고 목록 상태 추가
  const [totalItems, setTotalItems] = useState(0);

  // ... 기존 코드 ...

  const toggleApplied = (jobId) => {
    setAppliedJobs((prev) => 
      prev.includes(jobId) ? prev.filter(id => id !== jobId) : [...prev, jobId]
    );
  };
  

   // 데이터 가져오기


   useEffect(() => {
    const fetchSearchResults = async () => {
      if (!searchQuery) return;
      console.log('검색 쿼리:', searchQuery);
      
      setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:5001/api/jobs?query=${encodeURIComponent(searchQuery)}&page=${currentPage}&per_page=10`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('받은 데이터:', data);
      
      // 데이터가 배열인 경우 직접 설정
      if (Array.isArray(data)) {
        setResults(data);
        setTotalPages(Math.ceil(data.length / 10));
      } 
      // 데이터가 객체인 경우 items 배열 확인
      else if (data && data.items) {
        setResults(data.items);
        setTotalPages(data.total_pages);
        setTotalItems(data.total_items);
      }
      // 둘 다 아닌 경우 빈 배열로 설정
      else {
        setResults([]);
        setTotalPages(0);
      }
    } catch (err) {
      console.error('Error fetching results:', err);
      setError(err.message);
      setResults([]);
      setTotalPages(0);
    } finally {
      setIsLoading(false);
    }
  };

    fetchSearchResults();
  }, [searchQuery, currentPage]);
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    window.scrollTo(0, 0); // 페이지 상단으로 스크롤
  };
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
  // 페이지네이션 로직


  return (
    <div>
      <h1>공고 검색 결과</h1>
      <div className="search-summary">
        <p>
          검색어: {searchQuery}
          {!isLoading && (
            <span className="result-count">
            (총: {totalItems}건)
            </span>
          )}
        </p>
      </div>
      {isLoading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>데이터를 불러오는 중입니다...</p>
        </div>
      ) : results.length > 0 ? (
        <div>
          {results.map((result) => (
            <JobCard
              key={result.post_id}
              job={result}
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
                  onClick={() => setCurrentPage(index + 1)}
                  style={{ fontWeight: currentPage === index + 1 ? 'bold' : 'normal' }}
                >
                  {index + 1}
                </button>
              ))}
              <button
                onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
              >
                다음 페이지
              </button>
            </div>
          </div>
        </div>
      ) : (
        <p>검색 결과가 없습니다.</p>
      )}
    </div>
  );
};

export default SearchResult;