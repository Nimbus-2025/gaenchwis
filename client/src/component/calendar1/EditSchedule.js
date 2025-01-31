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
import api from '../../api/api';  // 수정된 부분
import Proxy from '../../api/Proxy';  // 수정된 import

const EditSchedule = ({ setSchedules }) => {
  const dispatch = useDispatch();
  const { currentSchedule, schedules = [] } = useSelector((state) => state.schedule || {});
  
  // schedules가 없을 때는 빈 배열 사용
  const safeSchedules = schedules || [];
  
  const [isEditing, setIsEditing] = useState(false);
  const [showResumePopup, setShowResumePopup] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);

  
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    documentResultDate: '',
    deadlineDate: '',
    interviewDate: '',
    finalDate: '',
    content: '',
    date: ''
  });

  // 일정 상세 정보 조회
  const fetchScheduleDetail = async () => {
    try {
      const userData = sessionStorage.getItem('user');
      if (!userData) {
        alert('로그인이 필요합니다.');
        return;
      }

      setFormData({
        title:currentSchedule.title,
        company:currentSchedule.company,
        deadlineDate:currentSchedule.schedule_deadline,
        interviewDate:currentSchedule.interview_date,
        documentResultDate:currentSchedule.document_result_date,
        finalDate:currentSchedule.final_date,
        content:currentSchedule.schedule_content,
        date:currentSchedule.date
      });
    } catch (error) {
      console.error('일정 조회 중 오류:', error);
      alert('일정을 불러오는데 실패했습니다.');
    }
  };

  // 컴포넌트 마운트 시 상세 정보 조회
  useEffect(() => {
    if (currentSchedule?.id) {
      fetchScheduleDetail();
    }
  }, [currentSchedule]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const onSave = async (type) => {
    const userData = sessionStorage.getItem('user');
      if (!userData) {
        alert('로그인이 필요합니다.');
        return;
      }

    const requestData = {
      ...formData,
      type:type
    };

    const response = await api(
      `${Proxy.server}:8006/api/v1/schedules/${currentSchedule.id}`,
      'PUT',
      requestData
    );
    
    if (response && Array.isArray(response)) {
      const scheduleList = response.map(schedule => ({
        type: schedule.schedule_type ? schedule.schedule_type : "schedule",
        id: schedule.schedule_id,
        title: schedule.schedule_title,
        date: schedule.schedule_date ? schedule.schedule_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
        schedule_deadline: schedule.schedule_deadline ? schedule.schedule_deadline.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
        document_result_date: schedule.document_result_date ? schedule.document_result_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
        interview_date: schedule.interview_date ? schedule.interview_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
        final_date: schedule.final_date ? schedule.final_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
        schedule_content: schedule.schedule_content,
        is_completes: schedule.is_completes
      }));
      console.log('변환된 일정 목록:', scheduleList);
      setSchedules(scheduleList);
      dispatch(openEditPopup({ isOpen: false }));
      setIsEditing(false);
    };
  }

  const isGeneralSchedule = currentSchedule?.type === 'schedule';

  // 일정 수정 핸들러
  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const userData = sessionStorage.getItem('user');
      if (!userData) {
        alert('로그인이 필요합니다.');
        return;
      }

      const parsedUserData = JSON.parse(userData);
      console.log('파싱된 유저 데이터:', {
        access_token: parsedUserData.access_token,
        id_token: parsedUserData.id_token,
        user_id: parsedUserData.user_id
      });

      // 날짜 형식 변환 (YYYY-MM-DD -> YYYYMMDD)
      const requestData = {
        ...formData
      };

      console.log('요청 URL:', `${Proxy.server}:8006/api/v1/schedules/${currentSchedule.id}`);
      console.log('전송할 데이터:', requestData);
      
      const response = await api(
        `${Proxy.server}:8006/api/v1/schedules/${currentSchedule.id}`,
        'PUT',
        requestData
      );

      console.log('서버 응답:', response);

      if (response instanceof Error) {
        throw response;
      }

      alert('일정이 성공적으로 수정되었습니다.');
      dispatch(openEditPopup({ isOpen: false }));
    } catch (error) {
      console.error('일정 수정 중 오류:', error);
      console.error('에러 상세:', error.response || error);
      alert('일정 수정에 실패했습니다.');
    }
  };
  // 일정 삭제 핸들러
  const handleDelete = async () => {
    try {
      const userData = sessionStorage.getItem('user');
      if (!userData) {
        alert('로그인이 필요합니다.');
        return;
      }

      const parsedUserData = JSON.parse(userData);
      console.log('파싱된 유저 데이터:', {
        access_token: parsedUserData.access_token,
        id_token: parsedUserData.id_token,
        user_id: parsedUserData.user_id
      });

      console.log('요청 URL:', `${Proxy.server}:8006/api/v1/schedules/${currentSchedule.id}`);
      
      const response = await api(
        `${Proxy.server}:8006/api/v1/schedules/${currentSchedule.id}`,
        'DELETE'
      );

      if (response && Array.isArray(response)) {
        const scheduleList = response.map(schedule => ({
          type: schedule.schedule_type ? schedule.schedule_type : "schedule",
          id: schedule.schedule_id,
          title: schedule.schedule_title,
          date: schedule.schedule_date ? schedule.schedule_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          schedule_deadline: schedule.schedule_deadline ? schedule.schedule_deadline.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          document_result_date: schedule.document_result_date ? schedule.document_result_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          interview_date: schedule.interview_date ? schedule.interview_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          final_date: schedule.final_date ? schedule.final_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          schedule_content: schedule.schedule_content,
          is_completes: schedule.is_completes
        }));
        console.log('변환된 일정 목록:', scheduleList);
        setSchedules(scheduleList);
      }

      if (response instanceof Error) {
        throw response;
      }

      alert('일정이 성공적으로 삭제되었습니다.');
      dispatch(openEditPopup({ isOpen: false }));
    } catch (error) {
      console.error('일정 삭제 중 오류:', error);
      console.error('에러 상세:', error.response || error);
      alert('일정 삭제에 실패했습니다.');
    }
  };

  if (!currentSchedule) return null;

  return (
    <Popup>
      <Header>
        <MdChevronLeft onClick={() => dispatch(openEditPopup({ isOpen: false }))} />
        {isGeneralSchedule ? '일정 확인' : currentSchedule.title}
        <i />
      </Header>
      <Body>
        {isGeneralSchedule ? (
          // 일반 일정 확인 양식
          <>
            <FormGroup>
              <Label>일정내용</Label>
              <Input
                type="text"
                name="title"
                value={isEditing ? formData.title : currentSchedule.title || ''}
                onChange={handleChange}
                readOnly={!isEditing}
              />
            </FormGroup>
            <FormGroup>
              <Label>날짜</Label>
              <Input
                type={isEditing ? "date" : "text"}
                name="date"
                value={isEditing ? 
                  formData.date : 
                  moment(currentSchedule.date, 'YYYY-MM-DD').format('YYYY년 MM월 DD일')}
                onChange={handleChange}
                readOnly={!isEditing}
              />
            </FormGroup>
            <FormGroup>
              <Label>메모</Label>
              <TextArea>
                <textarea
                  name="content"
                  value={isEditing ? formData.content : currentSchedule.schedule_content || ''}
                  onChange={handleChange}
                  readOnly={!isEditing}
                />
              </TextArea>
            </FormGroup>
            <ButtonContainer>
              <ActionButtonGroup>
                {!isEditing ? (
                  <>
                    <Button onClick={() => setIsEditing(true)}>수정</Button>
                    <Button onClick={() => handleDelete()}>삭제</Button>
                    <Button onClick={() => dispatch(openEditPopup({ isOpen: false }))}>
                      닫기
                    </Button>
                  </>
                ) : (
                  <>
                    <Button onClick={() => onSave('schedule')}>저장</Button>
                    <Button onClick={() => setIsEditing(false)}>취소</Button>
                  </>
                )}
              </ActionButtonGroup>
            </ButtonContainer>
          </>
        ) : (
          // 공고 확인 모달창 수정
          <>
            <FormGroup>
              <Label>공고명</Label>
              <Input
                type="text"
                name="title"
                value={formData.title ? formData.title : ""}
                onChange={handleChange}
                readOnly={true}
              />
            </FormGroup>
            <FormGroup>
              <Label>기업명</Label>
              <Input
                type="text"
                name="company"
                value={formData.company ? formData.company : ""}
                onChange={handleChange}
                readOnly={true}
              />
            </FormGroup>
            <FormGroup>
              <Label>공고 마감</Label>
              <Input
                type={isEditing ? "date" : "text"}
                name="deadlineDate"
                value={formData.deadlineDate ? formData.deadlineDate : ""}
                onChange={handleChange}
                readOnly={true}
              />
            </FormGroup>
            <FormGroup>
              <Label>서류 발표 일정</Label>
              <Input
                type={isEditing ? "date" : "text"}
                name="documentResultDate"
                value={isEditing ? 
                  formData.documentResultDate : 
                  (currentSchedule.document_result_date ?
                    moment(currentSchedule.document_result_date, 'YYYY-MM-DD').format('YYYY년 MM월 DD일')
                  : "")}
                onChange={handleChange}
                readOnly={!isEditing}
              />
            </FormGroup>
            <FormGroup>
              <Label>면접 일정</Label>
              <Input
                type={isEditing ? "date" : "text"}
                name="interviewDate"
                value={isEditing ? 
                  formData.interviewDate : 
                  (currentSchedule.interview_date ?
                    moment(currentSchedule.interview_date, 'YYYY-MM-DD').format('YYYY년 MM월 DD일')
                  : "")}
                onChange={handleChange}
                readOnly={!isEditing}
              />
            </FormGroup>
            <FormGroup>
              <Label>최종 발표 일정</Label>
              <Input
                type={isEditing ? "date" : "text"}
                name="finalDate"
                value={isEditing ? 
                  formData.finalDate : 
                  (currentSchedule.final_date ?
                    moment(currentSchedule.final_date, 'YYYY-MM-DD').format('YYYY년 MM월 DD일')
                  : "")}
                onChange={handleChange}
                readOnly={!isEditing}
              />
            </FormGroup>
            <FormGroup>
              <Label>메모</Label>
              <TextArea>
                <textarea
                  name="content"
                  value={isEditing ? formData.content : currentSchedule.schedule_content || ''}
                  onChange={handleChange}
                  readOnly={!isEditing}
                />
              </TextArea>
            </FormGroup>
            <ButtonContainer>
              <ActionButtonGroup>
                {!isEditing ? (
                  <>
                    <Button onClick={() => setIsEditing(true)}>수정</Button>
                    <Button onClick={() => dispatch(openEditPopup({ isOpen: false }))}>
                      닫기
                    </Button>
                  </>
                ) : (
                  <>
                    <Button onClick={() => onSave('post')}>저장</Button>
                    <Button onClick={() => setIsEditing(false)}>취소</Button>
                  </>
                )}
              </ActionButtonGroup>
            </ButtonContainer>
          </>
        )}
      </Body>
    </Popup>
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

    &.current {
      background-color: rgba(255, 154, 163, 0.1);
      padding: 8px;
      border-radius: 4px;
      margin: -4px -8px 4px -8px;
    }

    .label {
      width: 120px;
      color: #868e96;
      flex-shrink: 0;
    }
    
    .value {
      color: #495057;
      
      .current-tag {
        margin-left: 8px;
        color: #ff9aa3;
        font-size: 12px;
      }
    }
  }
`;

export default EditSchedule;