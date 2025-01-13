import React, { useEffect, useState } from 'react';
import dummyJobListings from './DummyData';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart as solidHeart } from '@fortawesome/free-solid-svg-icons';
import { faHeart as regularHeart } from '@fortawesome/free-regular-svg-icons';
import { faStar as solidStar } from '@fortawesome/free-solid-svg-icons'; // 별 아이콘
import { faStar as regularStar } from '@fortawesome/free-regular-svg-icons'; // 빈 별 아이콘
import './SearchResult.css';

const ITEMS_PER_PAGE = 2; // 페이지당 공고 
const SearchResult = ({ query }) => {
  const [results, setResults] = useState([]);
  const [favoriteCompanies, setFavoriteCompanies] = useState([]); // 관심 기업 상태
  const [currentPage, setCurrentPage] = useState(1);
  const [bookmarkedJobs, setBookmarkedJobs] = useState([]); // 북마크된 공고 상태

  useEffect(() => {
    if (query) {
      fetchResults(query);
    } else {
      setResults([]); // 수정된 부분
    }
  }, [query]);
  const fetchResults = (query) => {
    const filteredResults = dummyJobListings.filter((job) =>
      job.title.toLowerCase().includes(query.toLowerCase()) || // 제목 검색
      job.location.toLowerCase().includes(query.toLowerCase()) || // 지역 검색
      job.description.toLowerCase().includes(query.toLowerCase()) // 설명 검색
    );
    setResults(filteredResults);
    console.log(results); 
  };


  const toggleFavorite = (company) => {
    setFavoriteCompanies((prev) => {
      if (prev.includes(company)) {
        return prev.filter((c) => c !== company); // 관심 기업에서 제거
      } else {
        return [...prev, company]; // 관심 기업에 추가
      }
    });
  };
  const toggleBookmark = (jobId) => {
    setBookmarkedJobs((prev) => {
      if (prev.includes(jobId)) {
        return prev.filter((id) => id !== jobId); // 북마크에서 제거
      } else {
        return [...prev, jobId]; // 북마크에 추가
      }
    });
  };
  // 페이지네이션 로직
  const totalPages = Math.ceil(results.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const currentResults = results.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  

  return (
    <div>
      <h1>공고 검색 결과</h1>
      <p>검색어: {query}</p>
      {currentResults.length > 0 ? (
        <div>
        {currentResults.map((result) => (
          <div className="job-card" key={result._id}>
            <div className="job-header">
            <p className="job-company">
              {result.company}
              <FontAwesomeIcon
                icon={favoriteCompanies.includes(result.company) ? solidHeart : regularHeart}
                onClick={() => toggleFavorite(result.company)}
                style={{ cursor: 'pointer', marginLeft: '10px', color: favoriteCompanies.includes(result.company) ? 'red' : 'gray' }}
              />
            </p>
            <div className="divider"></div>
        <div className="job-details">
            <h3 className="job-title">{result.title} 
                <FontAwesomeIcon 
               icon={bookmarkedJobs.includes(result._id) ? solidStar : regularStar} // 북마크 아이콘 추가
            onClick={() => toggleBookmark(result._id)} // 북마크 추가/해제 함수 호출
            style={{ cursor: 'pointer', marginLeft: '10px', color: bookmarkedJobs.includes(result._id) ? 'gold' : 'gray' }}/>
            </h3>
        <div className="job-location-experience">
        <span className="job-experience">{result.experienceLevel}</span> {/* 신입/경력 정보 추가 */}
          <p className="job-location">{result.location}</p>
        
        </div>
        <p className="job-description">{result.description}</p>
          </div>
          </div>
          </div>
        ))}
        {/* 페이지네이션 버튼 */}
        <div className="pagination-container">
          <div className="pagination">
            <button
              onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
            >
              이전 페이지
            </button>
            {Array.from({ length: Math.min(totalPages, 10) }, (_, index) => (
              <button
                key={index + 1}
                onClick={() => setCurrentPage(index + 1)}
                style={{ fontWeight: currentPage === index + 1 ? 'bold' : 'normal' }} // 현재 페이지 강조
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