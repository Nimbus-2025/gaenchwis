// ShowEssay.js
import { useState, useEffect } from 'react';
import './ShowEssay.css';
import axios from 'axios';


const ShowEssay = () => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [essayTitle, setEssayTitle] = useState('');
  const [questions, setQuestions] = useState([{ question: '', answer: '' }]);
  const [essays, setEssays] = useState([]); // 자기소개서 목록 상태 추가
  const [selectedEssay, setSelectedEssay] = useState(null);
  const [bookmarks, setBookmarks] = useState(new Set());
  const [postingSelects, setPostingSelects] = useState([{ id: 1 }]);
  const [sortOrder, setSortOrder] = useState('latest'); // 'latest' 또는 'oldest'
  const [searchType, setSearchType] = useState('title');
  const [searchTerm, setSearchTerm] = useState('');  // 추가
  const [filteredEssays, setFilteredEssays] = useState([]); // 추가
  const [searchResults, setSearchResults] = useState([]);  // 검색 결과를 위한 상태
  const [splitView, setSplitView] = useState(false);      // 분할 뷰 상태
  

  

  // 북마크 토글 함수도 백엔드와 연동
const toggleBookmark = async (essayId, e) => {
  e.stopPropagation();
  
  try {
    const essay = essays.find(e => e.id === essayId);
    const updatedBookmarkStatus = !essay.isBookmarked;
    
    // 백엔드에 북마크 상태 업데이트 요청
    await axios.patch(`/api/essays/${essayId}/bookmark`, {
      isBookmarked: updatedBookmarkStatus
    });

    setEssays(prevEssays => {
      const currentIndex = prevEssays.findIndex(essay => essay.id === essayId);
      
      return prevEssays.map((essay, index) => {
        if (essay.id === essayId) {
          return {
            ...essay,
            isBookmarked: updatedBookmarkStatus,
            originalIndex: !updatedBookmarkStatus ? currentIndex : essay.originalIndex
          };
        }
        return essay;
      }).sort((a, b) => {
        if (a.isBookmarked === b.isBookmarked) {
          return a.originalIndex - b.originalIndex;
        }
        return a.isBookmarked ? -1 : 1;
      });
    });
  } catch (error) {
    console.error('북마크 상태 업데이트 실패:', error);
    alert('북마크 상태 업데이트에 실패했습니다.');
  }
};

  // 정렬 함수
  const sortEssays = (essays, order) => {
    return [...essays].sort((a, b) => {
      // 북마크된 항목은 항상 최상단 유지
      if (a.isBookmarked !== b.isBookmarked) {
        return a.isBookmarked ? -1 : 1;
      }
      
      // 북마크되지 않은 항목들끼리는 날짜순 정렬
      if (order === 'latest') {
        return b.id - a.id; // 최신순 (id가 큰 순)
      } else {
        return a.id - b.id; // 오래된순 (id가 작은 순)
      }
    });
  };

  // 정렬 순서 변경 핸들러
  const handleSortChange = (order) => {
    setSortOrder(order);
    setEssays(prevEssays => sortEssays(prevEssays, order));
  };


  // 자기소개서 추가
  const addQuestion = () => {
    setQuestions([...questions, { question: '', answer: '' }]);
  };

  const handleQuestionChange = (index, field, value) => {
    const newQuestions = [...questions];
    newQuestions[index][field] = value;
    setQuestions(newQuestions);
  };

  const handleEssayClick = (essay) => {
    if (selectedEssay?.id === essay.id) {
      setSelectedEssay(null);
    } else {
      setSelectedEssay(essay);
    }
  };

  const handleEditEssay = (essay) => {
    setIsPopupOpen(true);
    setEssayTitle(essay.title);
    setQuestions(essay.questions);
  };

  // useEffect를 사용하여 초기 데이터 로드 시 최신순 정렬 적용
  useEffect(() => {
    setEssays(prevEssays => sortEssays(prevEssays, 'latest'));
  }, []); // 컴포넌트 마운트 시 1회 실행



  const saveEssay = async (essayData) => {
    try {
      // essayData.questions 배열의 각 문항에 대해
      for (const question of essayData.questions) {
        // 각 문항을 개별 자기소개서로 생성
        const individualEssay = {
          title: `${essayData.title} - ${question.questionNumber}번 문항`, // 제목에 문항 번호 추가
          questions: [{
            questionNumber: question.questionNumber,
            questionText: question.questionText,
            answerText: question.answerText
          }],
          relatedPostings: essayData.relatedPostings
        };

        // 개별 자기소개서 저장
        await axios.post('/api/essays', individualEssay);
      }

      // 모든 저장이 완료된 후
      await fetchEssays(); // 목록 새로고침
      setIsModalOpen(false); // 모달 닫기
      
    } catch (error) {
      console.error('자기소개서 저장 실패:', error);
    }
  };
  
  // 모달 닫기 함수
  const onClose = () => {
    setIsModalOpen(false);
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // 각 문항을 개별 자기소개서로 생성
      const savePromises = questions.map(async (question, index) => {
        const essayData = {
          title: question.question, // 문항 내용을 타이틀로 사용
          questions: [{
            question: question.question,
            answer: question.answer
          }],
          isBookmarked: false,
          company: '', // 필요한 경우 회사 정보 추가
          createdAt: new Date().toISOString()
        };
  
        // 백엔드 API 호출
        const response = await axios.post('/api/essays', essayData);
        return response;
      });
  
      // 모든 저장 요청 실행
      const responses = await Promise.all(savePromises);
      
      if (responses.every(response => response.status === 200 || response.status === 201)) {
        // 저장 성공 후 최신 목록 다시 불러오기
        await fetchEssays();
        
        alert('자기소개서 저장이 완료되었습니다.');
        setIsPopupOpen(false);
        setEssayTitle('');
        setQuestions([{ question: '', answer: '' }]);
      }
    } catch (error) {
      console.error('자기소개서 저장 실패:', error);
      alert('자기소개서 저장에 실패했습니다.');
    }
  };
  
  // 자기소개서 목록 조회 함수
  const fetchEssays = async () => {
    try {
      const response = await axios.get('/api/essays');
      const sortedEssays = sortEssays(response.data, sortOrder);
      setEssays(sortedEssays);
    } catch (error) {
      console.error('자기소개서 목록을 불러오는데 실패했습니다:', error);
      alert('자기소개서 목록을 불러오는데 실패했습니다.');
    }
  };



const handleSearch = (e) => {
  const term = e.target.value;
  setSearchTerm(term);

  if (!term.trim()) {
    setFilteredEssays(essays);
    setSearchResults([]);
    setSplitView(false);
    return;
  }

  const filtered = essays.filter(essay => {
    const searchTermLower = term.toLowerCase();
    
    if (searchType === 'question') {
      return essay.questions.some(q => 
        q.question.toLowerCase().includes(searchTermLower)
      );
    }
    else if (searchType === 'content') {
      return essay.questions.some(q => 
        q.answer.toLowerCase().includes(searchTermLower)
      );
    }
    return false;
  });

  setFilteredEssays(filtered);
  setSearchResults(filtered);
  setSplitView(filtered.length > 0);
};


  // 검색어 하이라이트 함수
const highlightText = (text, searchTerm) => {
  if (!searchTerm) return text;
  const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
  return parts.map((part, index) => 
    part.toLowerCase() === searchTerm.toLowerCase() 
      ? <span key={index} className="highlight">{part}</span>
      : part
  );
};


// renderEssayItem 함수
const renderEssayItem = (essay) => {
  if (searchTerm) {
    return (
      <div className="essay-content">
        {essay.questions.map((q, idx) => {
          const searchText = searchType === 'question' ? q.question : q.answer;
          
          if (searchText.toLowerCase().includes(searchTerm.toLowerCase())) {
            return (
              <div key={idx}>
                <div className="question-text">
                  {searchType === 'question' ? 
                    highlightText(q.question, searchTerm) : 
                    q.question
                  }
                </div>
                <div className="content-preview">
                  {searchType === 'content' ? 
                    highlightText(q.answer, searchTerm) : 
                    q.answer
                  }
                </div>
              </div>
            );
          }
          return null;
        })}
      </div>
    );
  } else {
    return (
      <div className="essay-content">
        <h3>{essay.title}</h3>
      </div>
    );
  }
};


// useEffect 설정
useEffect(() => {
  setFilteredEssays(essays);
  setSearchResults([]);
}, [essays]);

useEffect(() => {
  if (searchResults.length === 0) {
    setSelectedEssay(null);
    setSplitView(false);
  }
}, [searchResults]);





  // 자기소개서 삭제 함수도 백엔드와 연동
  const deleteEssay = async (id) => {
    try {
      await axios.delete(`/api/essays/${id}`);
      
      setEssays(prevEssays => {
        const deletedIndex = prevEssays.findIndex(essay => essay.id === id);
        const newEssays = prevEssays.filter(essay => essay.id !== id);

        if (newEssays.length > 0) {
          const nextEssay = deletedIndex > 0 ? newEssays[deletedIndex - 1] : newEssays[0];
          setSelectedEssay(nextEssay);
        } else {
          setSelectedEssay(null);
        }
        
        return newEssays;
      });
    } catch (error) {
      console.error('자기소개서 삭제 실패:', error);
      alert('자기소개서 삭제에 실패했습니다.');
    }
  };



  const addPostingSelect = () => {
    const newId = postingSelects.length + 1;
    setPostingSelects([...postingSelects, { id: newId }]);
  };

  const handleDeleteEssay = (id) => {
    if (window.confirm('정말 삭제하시겠습니까?')) {
      deleteEssay(id);
    }
  };
  
  const resetPopup = () => {
    setEssayTitle('');
    setQuestions([{ question: '', answer: '' }]);
    setIsPopupOpen(false);
  };





  return (
    <div className="essay-container">
      <div className="search-box">
      <select 
          className="search-type-select"
          value={searchType}
          onChange={(e) => setSearchType(e.target.value)}
        >
          <option value="question">문항 기반</option>
          <option value="content">내용 기반</option>
        </select>
        <input 
          type="text" 
          placeholder="자기소개서 문항을 검색하세요..." 
          value={searchTerm}
          onChange={handleSearch}
        />
        <button className="search-button">검색</button>
        <button className="plus-button" onClick={() => setIsPopupOpen(true)}></button>
      </div>
      {/* 정렬 버튼을 content-wrapper 바깥으로 이동 */}
      <div className="sort-buttons">
        <button 
          className={`sort-button ${sortOrder === 'latest' ? 'active' : ''}`}
          onClick={() => handleSortChange('latest')}
        >
          최신순
        </button>
        <button 
          className={`sort-button ${sortOrder === 'oldest' ? 'active' : ''}`}
          onClick={() => handleSortChange('oldest')}
        >
          오래된순
        </button>
      </div>
      <div className={`content-wrapper ${selectedEssay ? 'split' : ''}`}>
        <div className={`essay-list ${selectedEssay ? 'collapsed' : ''} ${searchTerm ? 'search-results' : ''}`}>
        {filteredEssays.length > 0 ? (
          filteredEssays.map((essay) => (
            <div 
              key={essay.id} 
              className={`essay-rectangle ${selectedEssay?.id === essay.id ? 'selected' : ''} 
                ${searchTerm ? 'search-view' : 'normal-view'}`}
              onClick={() => handleEssayClick(essay)}
            >
              <div className="essay-content">
                {searchTerm ? (
                  // 검색 시 레이아웃
                  <>
                    <h3 className="search-title">
                      {searchType === 'question' 
                        ? highlightText(essay.questions[0].question, searchTerm)
                        : essay.questions[0].question
                      }
                    </h3>
                    <div className="company-info">
                      {essay.company || '-'}
                    </div>
                    <div className="preview-text">
                      {searchType === 'content'
                        ? highlightText(essay.questions[0].answer, searchTerm)
                        : essay.questions[0].answer
                      }
                    </div>
                  </>
                ) : (
                  // 기본 레이아웃
                  <h3>{essay.questions[0].question}</h3>
                )}
              </div>
              <button 
                className={`bookmark-button ${essay.isBookmarked ? 'bookmarked' : ''}`}
                onClick={(e) => toggleBookmark(essay.id, e)}
              >
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M16 12V4h1V2H7v2h1v8l-2 2v2h5.2v6h2.6v-6H19v-2l-2-2z"/>
                </svg>
              </button>
              <button 
                className="delete-button"
                onClick={(e) => {
                  e.stopPropagation();
                  deleteEssay(essay.id);
                }}
              >
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4h-3.5z"/>
                </svg>
              </button>
            </div>
          ))
        ) : (
          <div className="no-essay-message">
            {searchTerm ? "검색 결과가 없습니다." : "등록된 자기소개서가 없습니다."}
          </div>
        )}
        </div>

        {selectedEssay && (
          <div className="essay-detail-panel">
            <div className="essay-detail-header">
              <h2>{selectedEssay.questions[0].question}</h2>
              <div className="detail-buttons">
                <button 
                  className={`bookmark-button ${selectedEssay.isBookmarked ? 'bookmarked' : ''}`}
                  onClick={(e) => toggleBookmark(selectedEssay.id, e)}
                >
                  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                  </svg>
                </button>
                <button 
                  className="edit-button"
                  onClick={() => handleEditEssay(selectedEssay)}
                >
                  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                  </svg>
                </button>
                <button 
                  className="delete-detail-button"
                  onClick={() => deleteEssay(selectedEssay.id)}
                >
                  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                  </svg>
                </button>
              </div>
            </div>
            <div className="essay-detail-content">
              <div className="answer-text">
                {selectedEssay.questions[0].answer}
              </div>
            </div>
            {selectedEssay.relatedPostings && selectedEssay.relatedPostings.length > 0 && (
              <div className="essay-detail-related">
                <h3>연결된 공고</h3>
                <ul>
                  {selectedEssay.relatedPostings.map((posting, index) => (
                    <li key={index}>
                      <a href={posting.url} target="_blank" rel="noopener noreferrer">
                        {posting.title || posting.url}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {isPopupOpen && (
          <div className="popup-overlay">
            <div className="popup-content">
              <h2>자기소개서 추가</h2>
              <form onSubmit={handleSubmit}>
                {questions.map((item, index) => (
                  <div key={index} className="question-section">
                    <div className="form-group">
                      <label>문항 {index + 1}</label>
                      <input
                        type="text"
                        placeholder="자기소개서 문항 내용을 입력하세요"
                        value={item.question}
                        onChange={(e) => handleQuestionChange(index, 'question', e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>답변</label>
                      <textarea
                        placeholder="문항에 대한 내용을 입력하세요"
                        value={item.answer}
                        onChange={(e) => handleQuestionChange(index, 'answer', e.target.value)}
                        rows="6"
                        required
                      />
                    </div>
                  </div>
                ))}

                <button
                  type="button"
                  className="add-question-button"
                  onClick={addQuestion}
                >
                  + 문항 추가하기
                </button>

                <div className="related-posting-section">
                  <div className="related-posting-header">
                    <h3 className="related-posting-title">관련 공고 연결하기</h3>
                    <button 
                      type="button"
                      className="add-posting-button"
                      onClick={addPostingSelect}
                    >
                      +
                    </button>
                  </div>
                  {postingSelects.map((select) => (
                    <select key={select.id} className="posting-select">
                      <option value="">공고를 선택해주세요</option>
                    </select>
                  ))}
                </div>

                <div className="popup-buttons">
                  <button type="submit" className="submit-button">추가</button>
                  <button
                    type="button"
                    className="cancel-button"
                    onClick={resetPopup}
                  >
                    취소
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div> 
  );  
}  

export default ShowEssay;