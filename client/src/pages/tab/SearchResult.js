import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './SearchResult.css';
import JobCard from '../../component/JobCard';
import Config from '../../api/Config';
import Api from '../../api/api';

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
        const apiUrl = `${Config.server}:8003/api/jobs?query=${encodeURIComponent(searchQuery)}&page=${currentPage}&per_page=10`;
        console.log('요청 URL:', apiUrl);
        
        const response = await Api(apiUrl, 'GET');
        console.log('응답 데이터:', response);
        
        if (!response || response.error) {
          throw new Error(response?.error || '데이터를 불러오는데 실패했습니다');
        }
        
        // response가 이미 JSON 데이터이므로 바로 사용
        setResults(response.items || []);
        setTotalItems(response.total_items || 0);
        setTotalPages(Math.ceil((response.total_items || 0) / ITEMS_PER_PAGE));
        
      } catch (err) {
        console.error('검색 결과 조회 중 오류:', err);
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