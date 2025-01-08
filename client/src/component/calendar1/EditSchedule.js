import React, { useState, useEffect } from 'react';  // useEffect 추가
import { useDispatch, useSelector } from 'react-redux';  // useSelector 추가
import styled from 'styled-components';
import { MdChevronLeft } from 'react-icons/md';
import { 
  openEditPopup, 
  updateSchedule, 
  deleteSchedule 
} from './redux/modules/schedule';  // 경로 수정


// 자기소개서 확인 팝업 컴포넌트
const ResumeViewPopup = ({ onClose, content }) => {
  return (
    <PopupOverlay onClick={onClose}>
      <PopupWrapper onClick={e => e.stopPropagation()}>
        <PopupHeader>
          <h2>자기소개서 확인</h2>
          <CloseButton onClick={onClose}>&times;</CloseButton>
        </PopupHeader>
        <PopupContent>
          <TextArea>
            <textarea
              value={content}
              readOnly
              rows={10}
            />
          </TextArea>
          <ActionButtonGroup>
            <Button onClick={onClose}>닫기</Button>
          </ActionButtonGroup>
        </PopupContent>
      </PopupWrapper>
    </PopupOverlay>
  );
};

const EditSchedule = ({ history }) => {
  const dispatch = useDispatch();
  const { currentSchedule } = useSelector((state) => state.schedule);
  const [isEditing, setIsEditing] = useState(false);
  const [showResumePopup, setShowResumePopup] = useState(false);
  
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    tag: '',
    date: '',
    deadlineDate: '',
    interviewDate: '',
    finalDate: '',
    content: '',
    resume: ''
  });

  useEffect(() => {
    if (currentSchedule) {
      const formatDate = (dateString) => {
        if (!dateString) return '';
        return `${dateString.slice(0, 4)}-${dateString.slice(4, 6)}-${dateString.slice(6)}`;
      };

      setFormData({
        title: currentSchedule.title || '',
        company: currentSchedule.company || '',
        tag: currentSchedule.tag || '',
        date: formatDate(currentSchedule.date),
        deadlineDate: formatDate(currentSchedule.deadlineDate),
        interviewDate: formatDate(currentSchedule.interviewDate),
        finalDate: formatDate(currentSchedule.finalDate),
        content: currentSchedule.content || '',
        resume: currentSchedule.resume || ''
      });
    }
  }, [currentSchedule]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const onSave = () => {
    const formatDate = (dateString) => dateString.replaceAll('-', '');
    
    dispatch(updateSchedule({
      ...currentSchedule,
      ...formData,
      date: formatDate(formData.date),
      deadlineDate: formData.deadlineDate ? formatDate(formData.deadlineDate) : '',
      interviewDate: formData.interviewDate ? formatDate(formData.interviewDate) : '',
      finalDate: formData.finalDate ? formatDate(formData.finalDate) : ''
    }));
    
    setIsEditing(false);
  };

  const onDelete = () => {
    dispatch(deleteSchedule(currentSchedule.id));  // id만 전달하도록 수정
    dispatch(openEditPopup({ isOpen: false }));
  };

  const onComplete = () => {
    dispatch(updateSchedule({
      ...currentSchedule,
      completed: true
    }));
  };

  if (!currentSchedule) return null;

  return (
    <>
      <Popup>
        <Header>
          <MdChevronLeft onClick={() => dispatch(openEditPopup({ isOpen: false }))} />
          {currentSchedule.type === 'announcement' ? '공고 보기' : '일정 보기'}
          <i />
        </Header>
        <Body>
          {currentSchedule.type === 'announcement' ? (
            <>
              <FormGroup>
                <Label>공고명</Label>
                <Input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  readOnly={!isEditing}
                />
              </FormGroup>
              <FormGroup>
                <Label>기업명</Label>
                <Input
                  type="text"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  readOnly={!isEditing}
                />
              </FormGroup>
              <FormGroup>
                <Label>태그</Label>
                <Input
                  type="text"
                  name="tag"
                  value={formData.tag}
                  onChange={handleChange}
                  readOnly={!isEditing}
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
                      value={formData.date}
                      onChange={handleChange}
                      readOnly={!isEditing}
                    />
                  </DateItem>
                  <DateItem>
                    <SubLabel>공고 마감 일자</SubLabel>
                    <Input
                      type="date"
                      name="deadlineDate"
                      value={formData.deadlineDate}
                      onChange={handleChange}
                      readOnly={!isEditing}
                    />
                  </DateItem>
                  <DateItem>
                    <SubLabel>면접 일자</SubLabel>
                    <Input
                      type="date"
                      name="interviewDate"
                      value={formData.interviewDate}
                      onChange={handleChange}
                      readOnly={!isEditing}
                    />
                  </DateItem>
                  <DateItem>
                    <SubLabel>최종 발표 날짜</SubLabel>
                    <Input
                      type="date"
                      name="finalDate"
                      value={formData.finalDate}
                      onChange={handleChange}
                      readOnly={!isEditing}
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
                  value={formData.title}
                  onChange={handleChange}
                  readOnly={!isEditing}
                />
              </FormGroup>
              <FormGroup>
                <Label>날짜</Label>
                <Input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleChange}
                  readOnly={!isEditing}
                />
              </FormGroup>
            </>
          )}
          <FormGroup>
            <Label>내용</Label>
            <Textarea
              name="content"
              value={formData.content}
              onChange={handleChange}
              readOnly={!isEditing}
            />
          </FormGroup>
          <ButtonContainer>
            {!isEditing && currentSchedule.type === 'announcement' && (
              <ActionButtonGroup>
                <Button onClick={() => setShowResumePopup(true)}>
                  자기소개서 확인
                </Button>
              </ActionButtonGroup>
            )}
            <ActionButtonGroup>
              {!isEditing ? (
                <>
                  <Button onClick={() => setIsEditing(true)}>
                    수정
                  </Button>
                  {currentSchedule.type !== 'announcement' && (
                    <Button
                      disabled={currentSchedule.completed}
                      onClick={onComplete}
                    >
                      완료
                    </Button>
                  )}
                  <Button onClick={onDelete}>
                    삭제
                  </Button>
                </>
              ) : (
                <>
                  <Button onClick={onSave}>
                    저장
                  </Button>
                  <Button onClick={() => setIsEditing(false)}>
                    취소
                  </Button>
                </>
              )}
            </ActionButtonGroup>
          </ButtonContainer>
        </Body>
      </Popup>
      {showResumePopup && (
        <ResumeViewPopup 
          onClose={() => setShowResumePopup(false)}
          content={formData.resume || '자기소개서가 없습니다.'}
        />
      )}
    </>
  );
};

// 스타일 컴포넌트들
const Popup = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 700px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
`;

const Header = styled.div`
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;

  svg {
    cursor: pointer;
    font-size: 24px;
    color: #666;
    
    &:hover {
      color: #333;
    }
  }
`;

const Body = styled.div`
  padding: 20px 30px;
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  box-sizing: border-box;
`;

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
  
  &:read-only {
    background-color: #f5f5f5;
    cursor: default;
  }
`;

const Textarea = styled.textarea`
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  min-height: 100px;
  
  &:focus {
    outline: none;
    border-color: #ff9aa3;
  }
  
  &:read-only {
    background-color: #f5f5f5;
    cursor: default;
  }
`;

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
`;

const ActionButtonGroup = styled.div`
  display: flex;
  justify-content: center;
  gap: 12px;
`;

const Button = styled.button`
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #ff9aa3;
  color: white;
  cursor: pointer;
  
  &:hover {
    background-color: #ff8591;
  }
  
  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
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

const TextArea = styled.div`
  margin-bottom: 15px;
  
  textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
    min-height: 100px;
    
    &:focus {
      outline: none;
      border-color: #ff9aa3;
    }
    
    &:read-only {
      background-color: #f5f5f5;
      cursor: default;
    }
  }
`;

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

const PopupContent = styled.div`
  padding: 20px;
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

export default EditSchedule;