import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import './SearchResult.css';
import JobCard from '../../component/JobCard';
import Config from '../../api/Config';
import Api from '../../api/api';

const ITEMS_PER_PAGE = 10; // 페이지당 공고

const SearchResult = ({ searchQuery, selectedCategories }) => {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [totalItems, setTotalItems] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [favoriteCompanies, setFavoriteCompanies] = useState([]);
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]);
  const [appliedJobs, setAppliedJobs] = useState([]);

  const createUrlWithParams = (baseUrl, query, page, perPage, categories) => {
    let url = baseUrl;
    const params = [];

    // 기본 파라미터 추가
    if (query) {
      params.push(`query=${query}`);
    }

    if (page) {
      params.push(`page=${page}`);
    }

    if (perPage) {
      params.push(`per_page=${perPage}`);
    }

    // 카테고리 파라미터 추가 (값이 있는 경우에만)
    if (categories && Object.keys(categories).length > 0) {
      Object.entries(categories).forEach(([category, values]) => {
        if (Array.isArray(values) && values.length > 0) {
          values.forEach((value) => {
            // 카테고리와 값은 encodeURIComponent를 사용하지 않음
            params.push(`categories[${category}]=${value}`);
          });
        }
      });
    }

    const finalUrl = `${url}?${params.join('&')}`;
    console.log('최종 URL:', finalUrl);
    return finalUrl;
  };

  useEffect(() => {
    const fetchSearchResults = async () => {
      if (!searchQuery) return;
      console.log('검색 쿼리:', searchQuery);

      setIsLoading(true);
      setError(null);

      try {
        const apiUrl = createUrlWithParams(
          `${Config.server}:8003/api/jobs`,
          searchQuery,
          currentPage,
          ITEMS_PER_PAGE,
          selectedCategories,
        );

        console.log('검색 쿼리:', searchQuery);
        console.log(
          '선택된 카테고리:',
          JSON.stringify(selectedCategories, null, 2),
        );
        console.log('API 요청 URL:', apiUrl);

        const response = await Api(apiUrl, 'GET');

        if (!response || response.error) {
          throw new Error(
            response?.error || '데이터를 불러오는데 실패했습니다',
          );
        }

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
  }, [searchQuery, currentPage, selectedCategories]);

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
    window.scrollTo(0, 0); // 페이지 상단으로 스크롤
  };

  const toggleFavorite = (company) => {
    setFavoriteCompanies((prev) =>
      prev.includes(company)
        ? prev.filter((c) => c !== company)
        : [...prev, company],
    );
  };

  const toggleBookmark = (jobId) => {
    setBookmarkedJobs((prev) =>
      prev.includes(jobId)
        ? prev.filter((id) => id !== jobId)
        : [...prev, jobId],
    );
  };

  const toggleApplied = (jobId) => {
    setAppliedJobs((prev) =>
      prev.includes(jobId)
        ? prev.filter((id) => id !== jobId)
        : [...prev, jobId],
    );
  };

  if (error) {
    return <div className="error-message">에러: {error}</div>;
  }

  return (
    <div>
      <h1>공고 검색 결과</h1>
      <div className="search-summary">
        <p>
          검색어: {searchQuery}
          {!isLoading && (
            <span className="result-count">(총: {totalItems}건)</span>
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
                  style={{
                    fontWeight: currentPage === index + 1 ? 'bold' : 'normal',
                  }}
                >
                  {index + 1}
                </button>
              ))}
              <button
                onClick={() =>
                  setCurrentPage((prev) => Math.min(prev + 1, totalPages))
                }
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