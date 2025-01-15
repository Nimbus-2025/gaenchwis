import React, { useState, useEffect } from 'react';  // useEffect 추가
import { useDispatch, useSelector } from 'react-redux';  // useSelector 추가
import styled from 'styled-components';
import { MdChevronLeft } from 'react-icons/md';
import { 
  openEditPopup, 
  updateSchedule, 
  deleteSchedule 
} from './redux/modules/schedule';  // 경로 수정
import moment from 'moment';
import AddSchedule from './AddSchedule';  


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
  const [showEditModal, setShowEditModal] = useState(false);

  
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

  const isAnnouncementRelated = currentSchedule.title?.includes('공고 마감') ||
    currentSchedule.title?.includes('서류 합격 발표') ||
    currentSchedule.title?.includes('면접') ||
    currentSchedule.title?.includes('최종 발표');

  if (!currentSchedule) return null;

  return (
    <>
      <Popup>
        <Header>
          <MdChevronLeft onClick={() => dispatch(openEditPopup({ isOpen: false }))} />
          {formData.title}
          <i />
        </Header>
        <Body>
          <FormGroup>
            <Label>{isAnnouncementRelated ? '공고명' : '제목'}</Label>
            <Input
              type="text"
              name="title"
              value={isAnnouncementRelated ? formData.title.split(' ')[0] : formData.title}
              onChange={handleChange}
              readOnly={!isEditing}
            />
            {isAnnouncementRelated && (
              <SubTitle>
                <div className="company">{currentSchedule.company}</div>
                <div className="announcement">{formData.title}</div>
              </SubTitle>
            )}
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
          {isAnnouncementRelated && (
            <RelatedDates>
              <h4>관련 중요 일자</h4>
              <div className="date-row">
                <span className="label">서류 합격 발표</span>
                <span className="value">
                  {formData.deadlineDate ? moment(formData.deadlineDate).format('YYYY년 MM월 DD일') : 'Invalid date'}
                </span>
              </div>
              <div className="date-row">
                <span className="label">면접 일자</span>
                <span className="value">
                  {formData.interviewDate ? moment(formData.interviewDate).format('YYYY년 MM월 DD일') : 'Invalid date'}
                </span>
              </div>
              <div className="date-row">
                <span className="label">최종 발표 일자</span>
                <span className="value">
                  {formData.finalDate ? moment(formData.finalDate).format('YYYY년 MM월 DD일') : 'Invalid date'}
                </span>
              </div>
            </RelatedDates>
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
            {isAnnouncementRelated && (
              <ActionButtonGroup>
                <Button onClick={() => setShowResumePopup(true)}>
                  자기소개서 확인
                </Button>
              </ActionButtonGroup>
            )}
            <ActionButtonGroup>
              {!isEditing ? (
                <>
                  <Button onClick={() => {
                    if (isAnnouncementRelated) {
                      setShowEditModal(true);
                    } else {
                      setIsEditing(true);
                    }
                  }}>
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


      {/* AddSchedule 모달 추가 */}
      {showEditModal && (
        <AddSchedule
          type="announcement"
          onClose={() => {
            setShowEditModal(false);
            dispatch(openEditPopup({ isOpen: false }));
          }}
          initialData={{
            title: currentSchedule.title.split(' ')[1],
            company: currentSchedule.title.split(' ')[0],
            tag: currentSchedule.tag || '',
            date: formData.date,
            deadlineDate: formData.deadlineDate,
            interviewDate: formData.interviewDate,
            finalDate: formData.finalDate,
            content: formData.content,
          }}
          isEditing={true}
          currentSchedule={currentSchedule}
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
  min-height: 10px;
  
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

const SubTitle = styled.div`
  font-size: 14px;
  color: #666;
  margin-top: 4px;
  padding-left: 4px;
  
  .company {
    margin-bottom: 2px;
  }
  
  .announcement {
    color: #868e96;
  }
`;

const RelatedDates = styled.div`
  margin: 15px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;

  h4 {
    margin: 0 0 12px 0;
    color: #495057;
    font-size: 14px;
    font-weight: 500;
  }

  .date-row {
    display: flex;
    margin-bottom: 8px;
    font-size: 14px;
    
    &:last-child {
      margin-bottom: 0;
    }

    .label {
      width: 120px;
      color: #868e96;
      flex-shrink: 0;
    }
    
    .value {
      color: #495057;
    }
  }
`;

export default EditSchedule;