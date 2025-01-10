import React, { useEffect, useState } from 'react';

const SearchResult = ({ query }) => {
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (query) {
      fetchResults(query);
    }
  }, [query]);

  const fetchResults = (query) => {
    const dummyData = [
      { id: 1, title: 'React 튜토리얼', description: 'React 기본부터 고급까지.' },
      { id: 2, title: 'JavaScript 가이드', description: '모던 자바스크립트 완벽 가이드.' },
      { id: 3, title: 'HTML5 시작하기', description: 'HTML5의 모든 것.' },
    ];

    const filteredResults = dummyData.filter((item) =>
      item.title.toLowerCase().includes(query.toLowerCase())
    );
    setResults(filteredResults);
  };

  return (
    <div>
      <h1>공고 검색 결과</h1>
      <p>검색어: {query}</p>
      {results.length > 0 ? (
        <ul>
          {results.map((result) => (
            <li key={result.id}>
              <h3>{result.title}</h3>
              <p>{result.description}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>검색 결과가 없습니다.</p>
      )}
    </div>
  );
};

export default SearchResult;