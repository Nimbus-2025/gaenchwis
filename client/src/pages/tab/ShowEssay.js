// ShowEssay.js
import { useState, useEffect } from 'react';
import './ShowEssay.css';
import Config from '../../api/Config';
import Proxy from '../../api/Proxy';
import Api from '../../api/api';

const ShowEssay = () => {
  // 상태 관리
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [essays, setEssays] = useState([]);
  const [selectedEssay, setSelectedEssay] = useState(null);
  const [sortOrder, setSortOrder] = useState('asc');
  const [searchType, setSearchType] = useState('question');
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [splitView, setSplitView] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [questions, setQuestions] = useState([{ question: '', answer: '' }]);
  const [postingSelects, setPostingSelects] = useState([]);

  const PAGE_SIZE = 10;

  // 자기소개서 목록 조회
  const fetchEssays = async () => {
    try {
      const response = await Api(
        `${Proxy.server}:8002/api/v1/essays?sort_order=${sortOrder}&page=${currentPage}&page_size=${PAGE_SIZE}`,
        'GET',
      );
      if (response.essays) {
        setEssays(response.essays);
      }
    } catch (error) {
      console.error('자기소개서 목록을 불러오는데 실패했습니다:', error);
    }
  };

  // 자기소개서 상세 조회
  const fetchEssayDetail = async (essayId) => {
    try {
      const response = await Api(
        `${Proxy.server}:8002/api/v1/essays/${essayId}`,
        'GET',
      );
      setSelectedEssay(response);
    } catch (error) {
      console.error('자기소개서 상세 정보를 불러오는데 실패했습니다.', error);
    }
  };

  // 공고 목록 조회
  const fetchJobPostings = async () => {
    try {
      const response = await Api(
        `${Proxy.server}:8002/api/v1/job-postings`,
        'GET',
      );
      if (response.job_postings) {
        setJobPostings(response.job_postings);
      }
    } catch (error) {
      console.error('공고 목록을 불러오는데 실패했습니다:', error);
    }
  };

  // popUp이 열릴 때 공고 목록 조회
  useEffect(() => {
    if (isPopupOpen) {
      fetchJobPostings();
    }
  }, [isPopupOpen]);

  // 자기소개서 생성
  const createEssay = async (essayData = { questions, postingSelects }) => {
    try {
      const formattedData = {
        questions: essayData.questions.map((q) => ({
          essay_ask: q.question,
          essay_content: q.answer,
        })),
        job_postings: essayData.postingSelects
          .filter((select) => select.post_id && select.company_id)
          .map((select) => ({
            post_id: select.post_id,
            company_id: select.company_id,
          })),
      };

      const response = await Api(
        `${Proxy.server}:8002/api/v1/essays`,
        'POST',
        formattedData,
      );

      if (response.essay_ids) {
        await fetchEssays();
        setIsPopupOpen(false);
        setQuestions([{ question: '', answer: '' }]);
        setPostingSelects([]);
      }
    } catch (error) {
      console.error('자기소개서 생성에 실패했습니다:', error);
      alert('자기소개서 생성에 실패했습니다.');
    }
  };

  // 자기소개서 수정
  const updateEssay = async (essayId, updateData) => {
    try {
      const formattedData = {
        essay_ask: updateData.question,
        essay_content: updateData.answer,
      };

      await Api(
        `${Proxy.server}:8002/api/v1/essays/${essayId}`,
        'PATCH',
        formattedData,
      );

      await fetchEssayDetail(essayId);
    } catch (error) {
      console.error('자기소개서 수정에 실패했습니다.');
    }
  };

  // 자기소개서 삭제
  const deleteEssay = async (essayId) => {
    try {
      await Api(`${Proxy.server}:8002/api/v1/essays/${essayId}`, 'DELETE');

      setEssays((prevEssays) => {
        const newEssays = prevEssays.filter(
          (essay) => essay.essay_id !== essayId,
        );
        if (selectedEssay?.essay_id === essayId) {
          setSelectedEssay(null);
        }
        return newEssays;
      });
    } catch (error) {
      console.error('자기소개서 삭제에 실패했습니다:', error);
    }
  };

  // 검색 기능
  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      setSplitView(false);
      fetchEssays();
      return;
    }

    try {
      const response = await Api(
        `${
          Proxy.server
        }:8002/api/v1/essays/search?search_type=${searchType}&keyword=${encodeURIComponent(
          searchTerm,
        )}&sort_order=${sortOrder}&page=1&page_size=${PAGE_SIZE}`,
        'GET',
      );

      if (response.essays) {
        setSearchResults(response.essays);
        setSplitView(response.essays.length > 0);
      }
    } catch (error) {
      console.log('검색에 실패했습니다: ', error);
    }
  };

  // 정렬 순서 변경
  const handleSortChange = (order) => {
    setSortOrder(order);
    setCurrentPage(1);
  };

  // 자기소개서 클릭 핸들러
  const handleEssayClick = async (essay) => {
    if (selectedEssay?.essay_id === essay.essay_id) {
      setSelectedEssay(null);
    } else {
      await fetchEssayDetail(essay.essay_id);
    }
  };

  const handleQuestionChange = (index, field, value) => {
    const newQuestions = [...questions];
    newQuestions[index][field] = value;
    setQuestions(newQuestions);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (selectedEssay) {
        console.log('수정 요청 데이터: ', {
          essayId: selectedEssay.essay_id,
          questionData: questions[0],
        });

        await updateEssay(selectedEssay.essay_id, {
          question: questions[0].question,
          answer: questions[0].answer,
        });
      } else {
        await createEssay({ questions, postingSelects });
      }
      await fetchEssays();
      setIsPopupOpen(false);
      setSelectedEssay(null);
    } catch (error) {
      console.error('자기소개서 저장/수정에 실패했습니다:', error);
    }
  };

  const handlePostingSelectChange = (index, field, value) => {
    const newPostingSelects = [...postingSelects];
    newPostingSelects[index][field] = value;
    setPostingSelects(newPostingSelects);
  };

  const addQuestion = () => {
    setQuestions([...questions, { question: '', answer: '' }]);
  };

  const addPostingSelect = () => {
    const newId = postingSelects.length + 1;
    setPostingSelects([...postingSelects, { id: newId }]);
  };

  const resetPopup = () => {
    setQuestions([{ question: '', answer: '' }]);
    setPostingSelects([{ id: 1 }]);
    setIsPopupOpen(false);
  };

  // useEffect hooks
  useEffect(() => {
    fetchEssays();
  }, [sortOrder, currentPage]);

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      if (searchTerm) {
        handleSearch();
      }
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [searchTerm, searchType]);

  // 검색어 하이라이트 함수
  const highlightText = (text, searchTerm) => {
    if (!searchTerm) return text;
    const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
    return parts.map((part, index) =>
      part.toLowerCase() === searchTerm.toLowerCase() ? (
        <span key={index} className="highlight">
          {part}
        </span>
      ) : (
        part
      ),
    );
  };

  return (
    <div className="essay-container">
      {/* 검색 영역 */}
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
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button className="search-button">검색</button>
        <button
          className="plus-button"
          onClick={() => setIsPopupOpen(true)}
        ></button>
      </div>

      {/* 정렬 버튼 */}
      <div className="sort-buttons">
        <button
          className={`sort-button ${sortOrder === 'asc' ? 'active' : ''}`}
          onClick={() => handleSortChange('asc')}
        >
          최신순
        </button>
        <button
          className={`sort-button ${sortOrder === 'desc' ? 'active' : ''}`}
          onClick={() => handleSortChange('desc')}
        >
          오래된순
        </button>
      </div>

      {/* 콘텐츠 영역 */}
      <div className={`content-wrapper ${selectedEssay ? 'split' : ''}`}>
        <div
          className={`essay-list ${selectedEssay ? 'collapsed' : ''} ${
            searchTerm ? 'search-results' : ''
          }`}
        >
          {(searchTerm ? searchResults : essays).length > 0 ? (
            (searchTerm ? searchResults : essays).map((essay) => (
              <div
                key={essay.essay_id}
                className={`essay-rectangle ${
                  selectedEssay?.essay_id === essay.essay_id ? 'selected' : ''
                } 
                  ${searchTerm ? 'search-view' : 'normal-view'}`}
                onClick={() => handleEssayClick(essay)}
              >
                <div className="essay-content">
                  {searchTerm ? (
                    <>
                      <h3 className="search-title">
                        {searchType === 'question'
                          ? highlightText(essay.essay_ask, searchTerm)
                          : essay.essay_ask}
                      </h3>
                      <div className="content-preview">
                        {searchType === 'content'
                          ? highlightText(essay.essay_content || '', searchTerm)
                          : essay.essay_content}
                      </div>
                    </>
                  ) : (
                    <h3>{essay.essay_ask}</h3>
                  )}
                </div>
                <button
                  className="delete-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteEssay(essay.essay_id);
                  }}
                >
                  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM8 9h8v10H8V9zm7.5-5l-1-1h-5l-1 1H5v2h14V4h-3.5z" />
                  </svg>
                </button>
              </div>
            ))
          ) : (
            <div className="no-essay-message">
              {searchTerm
                ? '검색 결과가 없습니다.'
                : '등록된 자기소개서가 없습니다.'}
            </div>
          )}
        </div>

        {/* 상세 보기 패널 */}
        {selectedEssay && (
          <div className="essay-detail-panel">
            <div className="essay-detail-header">
              <h2>{selectedEssay.essay_ask}</h2>
              <div className="detail-buttons">
                <button
                  className="edit-button"
                  onClick={() => {
                    setQuestions([
                      {
                        question: selectedEssay.essay_ask,
                        answer: selectedEssay.essay_content,
                        essay_ask: selectedEssay.essay_ask,
                        essay_content: selectedEssay.essay_content,
                      },
                    ]);
                    setIsPopupOpen(true);
                  }}
                >
                  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                  </svg>
                </button>
                <button
                  className="delete-detail-button"
                  onClick={() => deleteEssay(selectedEssay.essay_id)}
                >
                  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="essay-detail-content">
              <div className="answer-text">{selectedEssay.essay_content}</div>
            </div>
            {selectedEssay.related_job_postings?.length > 0 && (
              <div className="essay-detail-related">
                <h3>연결된 공고</h3>
                <ul>
                  {selectedEssay.related_job_postings.map((posting, index) => (
                    <li key={index}>
                      {posting.company_name} - {posting.post_name}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* 자기소개서 추가/수정 팝업 */}
        {isPopupOpen && (
          <div className="popup-overlay">
            <div className="popup-content">
              <h2>{selectedEssay ? '자기소개서 수정' : '자기소개서 추가'}</h2>
              <form onSubmit={handleSubmit}>
                {questions.map((item, index) => (
                  <div key={index} className="question-section">
                    <div className="form-group">
                      <label>문항 {index + 1}</label>
                      <input
                        type="text"
                        placeholder="자기소개서 문항 내용을 입력하세요"
                        value={item.question}
                        onChange={(e) =>
                          handleQuestionChange(
                            index,
                            'question',
                            e.target.value,
                          )
                        }
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>답변</label>
                      <textarea
                        placeholder="문항에 대한 내용을 입력하세요"
                        value={item.answer}
                        onChange={(e) =>
                          handleQuestionChange(index, 'answer', e.target.value)
                        }
                        rows="6"
                        required
                      />
                    </div>
                  </div>
                ))}

                {!selectedEssay && (
                  <button
                    type="button"
                    className="add-question-button"
                    onClick={addQuestion}
                  >
                    + 문항 추가하기
                  </button>
                )}

                <div className="related-posting-section">
                  <div className="related-posting-header">
                    <h3 className="related-posting-title">
                      관련 공고 연결하기
                    </h3>
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
                      {/* 여기에 실제 채용공고 옵션들이 들어갈 예정 */}
                    </select>
                  ))}
                </div>

                <div className="popup-buttons">
                  <button type="submit" className="submit-button">
                    {selectedEssay ? '수정' : '추가'}
                  </button>
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
};

export default ShowEssay;
