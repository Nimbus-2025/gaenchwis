// ShowEssay.js
import { useState, useEffect } from 'react';
import './ShowEssay.css';

const ShowEssay = () => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [essayTitle, setEssayTitle] = useState('');
  const [questions, setQuestions] = useState([{ question: '', answer: '' }]);
  const [essays, setEssays] = useState([]); // 자기소개서 목록 상태 추가
  const [selectedEssay, setSelectedEssay] = useState(null);
  const [bookmarks, setBookmarks] = useState(new Set());
  const [postingSelects, setPostingSelects] = useState([{ id: 1 }]);
  const [sortOrder, setSortOrder] = useState('latest'); // 'latest' 또는 'oldest'
  

  // 북마크 토글 함수 추가
  const toggleBookmark = (essayId, e) => {
    e.stopPropagation(); // 클릭 이벤트 전파 방지
    setEssays(prevEssays => {
      return prevEssays.map(essay => {
        // 클릭된 에세이만 상태 변경
        if (essay.id === essayId) {
          const newBookmarkState = !essay.isBookmarked;
          return {
            ...essay,
            isBookmarked: newBookmarkState,
            originalIndex: newBookmarkState 
              ? prevEssays.findIndex(e => e.id === essayId)
              : essay.originalIndex
          };
        }
        return essay;
      }).sort((a, b) => {
        if (a.isBookmarked === b.isBookmarked) {
          // 북마크 상태가 같으면 originalIndex 기준으로 정렬
          return a.originalIndex - b.originalIndex;
        }
        // 북마크된 항목을 위로
        return a.isBookmarked ? -1 : 1;
      });
    });
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

  // 새 에세이 추가 시 originalIndex 포함
  const handleSubmit = (e) => {
    e.preventDefault();
    const newEssay = {
      id: Date.now(),
      title: essayTitle,
      questions: questions,
      isBookmarked: false,
      originalIndex: essays.length // 새 에세이의 원래 위치
    };
    setEssays(prevEssays => {
      // 새 에세이를 배열 맨 앞에 추가하고 정렬
      const updatedEssays = [newEssay, ...prevEssays];
      return sortEssays(updatedEssays, sortOrder);
    });
    
    resetPopup();
  };



  // 삭제 시 originalIndex 업데이트
  const deleteEssay = (id) => {
    setEssays(prevEssays => {
      const deletedIndex = prevEssays.findIndex(essay => essay.id === id);
      const newEssays = prevEssays
        .filter(essay => essay.id !== id)
        .map(essay => ({
          ...essay,
          originalIndex: essay.originalIndex > deletedIndex 
            ? essay.originalIndex - 1 
            : essay.originalIndex
        }));

      if (newEssays.length > 0) {
        const nextEssay = deletedIndex > 0 ? newEssays[deletedIndex - 1] : newEssays[0];
        setSelectedEssay(nextEssay);
      } else {
        setSelectedEssay(null);
      }
      
      return newEssays;
    });
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
        <input type="text" placeholder="자기소개서 문항을 검색하세요..." />
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
        <div className={`essay-list ${selectedEssay ? 'collapsed' : ''}`}>
          {/* 기존 리스트 내용 */}
        </div>
        {/* 나머지 내용 */}
      </div>
      <div className={`content-wrapper ${selectedEssay ? 'split' : ''}`}>
        <div className={`essay-list ${selectedEssay ? 'collapsed' : ''}`}>
          {essays.length > 0 ? (
            essays.map((essay) => (
              <div 
                key={essay.id} 
                className={`essay-rectangle ${selectedEssay?.id === essay.id ? 'selected' : ''}`}
                onClick={() => handleEssayClick(essay)}
              >
                <div className="essay-content">
                  <h3>{essay.title}</h3>
                </div>
                <button 
                  className={`bookmark-button ${essay.isBookmarked ? 'bookmarked' : ''}`}
                  onClick={(e) => toggleBookmark(essay.id, e)}
                >
                  <svg 
                    viewBox="0 0 24 24" 
                    xmlns="http://www.w3.org/2000/svg"
                  >
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
              등록된 자기소개서가 없습니다.
            </div>
          )}
        </div>

        {selectedEssay && (
          <div className="essay-detail-panel">
            <div className="essay-detail-header">
              <h2>{selectedEssay.title}</h2>
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
              {selectedEssay.questions.map((q, index) => (
                <div key={index} className="question-detail">
                  <div className="question-header">
                    <h4>문항 {index + 1}</h4>
                    <span className="question-text">{q.question}</span>
                  </div>
                  <p className="answer-text">{q.answer}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {isPopupOpen && (
        <div className="popup-overlay">
          <div className="popup-content">
            <h2>자기소개서 추가</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>자기소개서 제목</label>
                <input
                  type="text"
                  placeholder="자기소개서 제목을 입력하세요"
                  value={essayTitle}
                  onChange={(e) => setEssayTitle(e.target.value)}
                  required
                />
              </div>

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
  );
};

export default ShowEssay;