import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import moment from 'moment';
import { createSchedule } from './redux/modules/schedule';  // 경로 수정

const QuestionSet = styled.div`
  margin-bottom: 30px;
  width: 100%;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const AddButton = styled.button`
  width: 100%;
  padding: 10px;
  margin: 20px 0;
  background-color: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 4px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background-color: #e9ecef;
    color: #333;
    border-color: #ced4da;
  }

  &:active {
    background-color: #dee2e6;
  }
`;

const TextAreaWrapper = styled.div`
  margin-bottom: 15px;
  width: 100%;
  
  textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
    height: 3cm;
    resize: none;
    overflow-y: auto;
    
    &:focus {
      outline: none;
      border-color: #ff9aa3;
    }

    &.fixed-height {
      height: 3cm;
    }
  }
`;

const ResumePopupWrapper = styled.div`
  width: 850px;  // 자기소개서 입력 팝업창만 850px로 설정
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  position: relative;
`;

// 자기소개서 입력 팝업 컴포넌트
const ResumePopup = ({ onClose, onSave }) => {
  const [questions, setQuestions] = useState([{ title: '', content: '' }]);

  const handleQuestionChange = (index, field, value) => {
    const newQuestions = [...questions];
    newQuestions[index][field] = value;
    setQuestions(newQuestions);
  };

  const addQuestionSet = () => {
    setQuestions([...questions, { question: '', answer: '' }]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ content: questions });
    onClose();
  };

  return (
    <PopupOverlay onClick={onClose}>
      <PopupWrapper onClick={e => e.stopPropagation()}>
        <PopupHeader>
          <h2>자기소개서 입력</h2>
          <CloseButton onClick={onClose}>&times;</CloseButton>
        </PopupHeader>
        <PopupContent>
          <Form onSubmit={handleSubmit}>
            {questions.map((q, index) => (
              <QuestionSet key={index}>
                <TextAreaWrapper>
                  <textarea
                    placeholder="문항을 입력하세요"
                    value={q.title}
                    onChange={(e) => handleQuestionChange(index, 'title', e.target.value)}
                    className="fixed-height"
                  />
                </TextAreaWrapper>
                <TextAreaWrapper>
                  <textarea
                    placeholder="자기소개서 내용을 입력하세요"
                    value={q.content}
                    onChange={(e) => handleQuestionChange(index, 'content', e.target.value)}
                    className="fixed-height"
                  />
                </TextAreaWrapper>
              </QuestionSet>
            ))}
            <AddButton type="button" onClick={addQuestionSet}>
              + 문항 추가하기
            </AddButton>
            <ActionButtonGroup>
              <SubmitButton type="submit">저장</SubmitButton>
              <CancelButton type="button" onClick={onClose}>취소</CancelButton>
            </ActionButtonGroup>
          </Form>
        </PopupContent>
      </PopupWrapper>
    </PopupOverlay>
  );
};

const AddSchedule = ({ onClose, type }) => {
  const dispatch = useDispatch();
  const [showResumePopup, setShowResumePopup] = useState(false);
  const [resumeContent, setResumeContent] = useState('');
  const [scheduleData, setScheduleData] = useState({
    title: '',
    company: '',
    tag: '',
    date: moment().format('YYYY-MM-DD'),
    deadlineDate: moment().format('YYYY-MM-DD'),
    interviewDate: moment().format('YYYY-MM-DD'),
    finalDate: moment().format('YYYY-MM-DD'),
    content: '',
    resume: '',
    completed: false
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setScheduleData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleResumeSubmit = (data) => {
    setResumeContent(data.content);
    setShowResumePopup(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (type === 'announcement') {
      dispatch(createSchedule({
        ...scheduleData,
        resume: resumeContent,
        date: moment(scheduleData.date).format('YYYYMMDD'),
        type: type
      }));

      // 공고 마감일 일정 추가
      dispatch(createSchedule({
        title: `${scheduleData.company} 공고 마감`,
        date: moment(scheduleData.deadlineDate).format('YYYYMMDD'),
        content: `${scheduleData.company} 공고 마감일입니다.`,
        type: 'schedule'
      }));

      // 서류 합격 발표 일정 추가 (마감일 +7일로 설정)
      dispatch(createSchedule({
        title: `${scheduleData.company} 서류 합격 발표`,
        date: moment(scheduleData.deadlineDate).add(7, 'days').format('YYYYMMDD'),
        content: `${scheduleData.company} 서류 합격 발표일입니다.`,
        type: 'schedule'
      }));

      // 면접일 일정 추가
      if (scheduleData.interviewDate) {
        dispatch(createSchedule({
          title: `${scheduleData.company} 면접일`,
          date: moment(scheduleData.interviewDate).format('YYYYMMDD'),
          content: `${scheduleData.company} 면접일입니다.`,
          type: 'schedule'
        }));
      }

      // 최종 발표일 일정 추가
      if (scheduleData.finalDate) {
        dispatch(createSchedule({
          title: `${scheduleData.company} 최종 발표`,
          date: moment(scheduleData.finalDate).format('YYYYMMDD'),
          content: `${scheduleData.company} 최종 발표일입니다.`,
          type: 'schedule'
        }));
      }

    } else {
      dispatch(createSchedule({
        ...scheduleData,
        date: moment(scheduleData.date).format('YYYYMMDD'),
        type: type
      }));
    }
    
    onClose();
  };

  return (
    <>
      <PopupOverlay onClick={onClose}>
        <PopupWrapper onClick={e => e.stopPropagation()}>
          <PopupHeader>
            <h2>{type === 'schedule' ? '일정 추가' : '공고 추가'}</h2>
            <CloseButton onClick={onClose}>&times;</CloseButton>
          </PopupHeader>
          <PopupContent>
            <Form onSubmit={handleSubmit}>
              {type === 'announcement' ? (
                <>
                  <FormGroup>
                    <Label>공고명</Label>
                    <Input
                      type="text"
                      name="title"
                      value={scheduleData.title}
                      onChange={handleChange}
                      required
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label>기업명</Label>
                    <Input
                      type="text"
                      name="company"
                      value={scheduleData.company}
                      onChange={handleChange}
                      required
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label>태그</Label>
                    <Input
                      type="text"
                      name="tag"
                      value={scheduleData.tag}
                      onChange={handleChange}
                      placeholder="예: #IT #개발자 #신입"
                    />
                  </FormGroup>
                  <DateSection>
                    <Label>날짜</Label>
                    <DateGroup>
                      <DateItem>
                        <SubLabel>공고 추가 일자</SubLabel>
                        <Input
                          type="date"
                          name="date"
                          value={scheduleData.date}
                          onChange={handleChange}
                          required
                        />
                      </DateItem>
                      <DateItem>
                        <SubLabel>공고 마감 일자</SubLabel>
                        <Input
                          type="date"
                          name="deadlineDate"
                          value={scheduleData.deadlineDate}
                          onChange={handleChange}
                          required
                        />
                      </DateItem>
                      <DateItem>
                        <SubLabel>면접 일자</SubLabel>
                        <Input
                          type="date"
                          name="interviewDate"
                          value={scheduleData.interviewDate}
                          onChange={handleChange}
                        />
                      </DateItem>
                      <DateItem>
                        <SubLabel>최종 발표 날짜</SubLabel>
                        <Input
                          type="date"
                          name="finalDate"
                          value={scheduleData.finalDate}
                          onChange={handleChange}
                        />
                      </DateItem>
                    </DateGroup>
                  </DateSection>
                </>
              ) : (
                <>
                  <FormGroup>
                    <Label>제목</Label>
                    <Input
                      type="text"
                      name="title"
                      value={scheduleData.title}
                      onChange={handleChange}
                      required
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label>날짜</Label>
                    <Input
                      type="date"
                      name="date"
                      value={scheduleData.date}
                      onChange={handleChange}
                      required
                    />
                  </FormGroup>
                </>
              )}
              <FormGroup>
                <Label>내용</Label>
                <Textarea
                  name="content"
                  value={scheduleData.content}
                  onChange={handleChange}
                  required
                />
              </FormGroup>
              <ButtonGroup>
                {type === 'announcement' && (
                  <Button type="button" onClick={() => setShowResumePopup(true)}>
                    자기소개서 입력
                  </Button>
                )}
                <div>
                  <SubmitButton type="submit">
                    {type === 'schedule' ? '일정 추가' : '공고 추가'}
                  </SubmitButton>
                  <CancelButton type="button" onClick={onClose}>
                    취소
                  </CancelButton>
                </div>
              </ButtonGroup>
            </Form>
          </PopupContent>
        </PopupWrapper>
      </PopupOverlay>
      {showResumePopup && (
        <ResumePopup 
          onClose={() => setShowResumePopup(false)}
          onSave={handleResumeSubmit}
        />
      )}
    </>
  );
};

// 스타일 컴포넌트들
const PopupOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const PopupWrapper = styled.div`
  width: 700px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
`;

const PopupHeader = styled.div`
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;

  h2 {
    margin: 0;
    font-size: 1.2rem;
  }
`;

const PopupContent = styled.div`
  padding: 20px;
`;

const Form = styled.form``;

const FormGroup = styled.div`
  margin-bottom: 15px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
`;

const Input = styled.input`
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  
  &:focus {
    outline: none;
    border-color: #ff9aa3;
  }
`;

const Textarea = styled.textarea`
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  height: 3cm;  // 정확히 3cm로 설정
  min-height: 3cm;  // 최소 높이도 3cm로 설정
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: #ff9aa3;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  justify-content: space-between;  // 양쪽 끝으로 정렬
  margin-top: 20px;
  width: 100%;

  > div {  // 오른쪽 버튼들을 감싸는 div
    display: flex;
    gap: 10px;  // 추가/취소 버튼 사이 간격
  }
`;

const Button = styled.button`
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #6c757d; 
  color: white;
  cursor: pointer;
  
  &:hover {
    background-color: #4dabf7;
  }
`;

const SubmitButton = styled(Button)`
  background-color: #74c0fc;  // 제출 버튼 하늘색으로 변경
  
  &:hover {
    background-color: #4dabf7;  // hover 시 약간 더 진한 하늘색
  }
`;


const CancelButton = styled(Button)`
  background-color: #6c757d;
  
  &:hover {
    background-color: #5a6268;
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  color: #666;
  
  &:hover {
    color: #333;
  }
`;

const DateSection = styled.div`
  margin-bottom: 20px;
`;

const DateGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  margin-left: 20px;
`;

const DateItem = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const SubLabel = styled.label`
  min-width: 120px;
  font-size: 14px;
  color: #666;
`;


const ActionButtonGroup = styled.div`
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 20px;
`;
export default AddSchedule;