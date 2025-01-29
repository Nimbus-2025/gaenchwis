import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';  // useSelector 추가
import styled from 'styled-components';
import moment from 'moment';
import { 
  createSchedule,
  updateSchedule  // updateSchedule 추가
} from './redux/modules/schedule';
import api from '../../api/api';
import Proxy from '../../api/Proxy';

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
  width: 95%;
  
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

const AddSchedule = ({ 
  onClose, 
  type, 
  initialData = null, 
  isEditing = false,
  currentSchedule = null,
  onSave
}) => {
  const dispatch = useDispatch();
  const { schedules = [] } = useSelector((state) => state.schedule || {});
  const currentYear = moment().format('YYYY');
  const [scheduleData, setScheduleData] = useState(
    initialData || {
      title: '',
      company: '',
      tag: '',
      date: `${currentYear}-`,
      deadlineDate: `${currentYear}-`,
      interviewDate: `${currentYear}-`,
      finalDate: `${currentYear}-`,
      content: '',
      completed: false
    }
  );

  // 날짜 포맷팅 함수를 컴포넌트 내부에 정의
  const formatDate = (dateString) => {
    if (!dateString || dateString === `${currentYear}-`) return '';
    const formattedDate = moment(dateString).format('YYYYMMDD');
    return formattedDate;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setScheduleData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (type === 'schedule') {
      try {
        const userData = sessionStorage.getItem('user');
        console.log('세션 스토리지 데이터:', userData); // 디버깅용
        
        if (!userData) {
          alert('로그인이 필요합니다.');
          return;
        }
        
        // 세션 데이터 확인 및 로깅
        const parsedUserData = JSON.parse(userData);
        console.log('파싱된 유저 데이터:', {
          access_token: parsedUserData.access_token,
          id_token: parsedUserData.id_token,
          user_id: parsedUserData.user_id
        });

        // 날짜 형식 변환 (YYYY-MM-DD -> YYYYMMDD)
        const formattedDate = scheduleData.date.replaceAll('-', '');

        const requestData = {
          title: scheduleData.title,
          date: formattedDate,
          content: scheduleData.content || ''
        };
        
        console.log('전송할 데이터:', requestData);
        console.log('요청 URL:', `${Proxy.server}:8006/api/v1/schedules`);
        console.log('요청 헤더:', {
          access_token: parsedUserData.access_token,
          id_token: parsedUserData.id_token,
          user_id: parsedUserData.user_id
        });

        const response = await api(
          `${Proxy.server}:8006/api/v1/schedules`,
          'POST',
          requestData
        );

        console.log('서버 응답:', response);

        if (response instanceof Error) {
          throw response;
        }

        alert('일정이 성공적으로 저장되었습니다.');
        onClose();
        if (typeof onSave === 'function') {
          onSave();
        }
      } catch (error) {
        console.error('일정 저장 중 오류:', error);
        console.error('에러 상세:', error.response || error); // 상세 에러 정보 출력
        alert('일정 저장에 실패했습니다.');
      }
    } else if (type === 'announcement') {
      const hasAnyDate = scheduleData.date.length > currentYear.length + 1 ||
                      scheduleData.deadlineDate.length > currentYear.length + 1 ||
                      scheduleData.interviewDate.length > currentYear.length + 1 ||
                      scheduleData.finalDate.length > currentYear.length + 1;

      if (!hasAnyDate) {
        alert('최소 하나의 날짜를 선택해주세요.');
        return;
      }

      if (isEditing && currentSchedule) {
        const baseSchedule = {
          type: 'announcement',
          company: scheduleData.company,
          tag: scheduleData.tag,
          content: scheduleData.content,
          createdAt: currentSchedule.createdAt,
          backgroundColor: '#ff9aa3'
        };

        // 현재 수정 중인 일정만 업데이트
        if (currentSchedule.title.includes('공고 마감')) {
          if (scheduleData.date.length > currentYear.length + 1) {
            dispatch(updateSchedule({
              ...currentSchedule,
              ...baseSchedule,
              title: `${scheduleData.company} 공고 마감`,
              date: formatDate(scheduleData.date)
            }));
          }
        } else if (currentSchedule.title.includes('서류 합격 발표')) {
          if (scheduleData.deadlineDate.length > currentYear.length + 1) {
            dispatch(updateSchedule({
              ...currentSchedule,
              ...baseSchedule,
              title: `${scheduleData.company} 서류 합격 발표`,
              date: formatDate(scheduleData.deadlineDate)
            }));
          }
        } else if (currentSchedule.title.includes('면접')) {
          if (scheduleData.interviewDate.length > currentYear.length + 1) {
            dispatch(updateSchedule({
              ...currentSchedule,
              ...baseSchedule,
              title: `${scheduleData.company} 면접일`,
              date: formatDate(scheduleData.interviewDate)
            }));
          }
        } else if (currentSchedule.title.includes('최종 발표')) {
          if (scheduleData.finalDate.length > currentYear.length + 1) {
            dispatch(updateSchedule({
              ...currentSchedule,
              ...baseSchedule,
              title: `${scheduleData.company} 최종 발표`,
              date: formatDate(scheduleData.finalDate)
            }));
          }
        }

        // 새로운 날짜가 있는 경우에만 새 일정 추가
        if (!currentSchedule.title.includes('공고 마감') && scheduleData.date.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 공고 마감`,
            date: formatDate(scheduleData.date)
          }));
        }
        if (!currentSchedule.title.includes('서류 합격 발표') && scheduleData.deadlineDate.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 서류 합격 발표`,
            date: formatDate(scheduleData.deadlineDate)
          }));
        }
        if (!currentSchedule.title.includes('면접') && scheduleData.interviewDate.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 면접일`,
            date: formatDate(scheduleData.interviewDate)
          }));
        }
        if (!currentSchedule.title.includes('최종 발표') && scheduleData.finalDate.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 최종 발표`,
            date: formatDate(scheduleData.finalDate)
          }));
        }
      } else {
        // 새로운 공고 일정 추가
        const baseSchedule = {
          type: 'announcement',
          company: scheduleData.company,
          tag: scheduleData.tag,
          content: scheduleData.content,
          backgroundColor: '#ff9aa3'
        };

        // 공고 마감 일정
        if (scheduleData.date.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 공고 마감`,
            date: scheduleData.date.replaceAll('-', '')
          }));
        }

        // 서류 합격 발표 일정
        if (scheduleData.deadlineDate.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 서류 합격 발표`,
            date: scheduleData.deadlineDate.replaceAll('-', '')
          }));
        }

        // 면접 일정
        if (scheduleData.interviewDate.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 면접일`,
            date: scheduleData.interviewDate.replaceAll('-', '')
          }));
        }

        // 최종 발표 일정
        if (scheduleData.finalDate.length > currentYear.length + 1) {
          dispatch(createSchedule({
            ...baseSchedule,
            title: `${scheduleData.company} 최종 발표`,
            date: scheduleData.finalDate.replaceAll('-', '')
          }));
        }
      }
    }
    
    onClose();
  };

  return (
    <PopupOverlay onClick={onClose}>
      <PopupWrapper onClick={e => e.stopPropagation()}>
        <PopupHeader>
          <h2>{isEditing ? '공고 수정' : (type === 'schedule' ? '일정 추가' : '공고 추가')}</h2>
          <CloseButton onClick={onClose}>&times;</CloseButton>
        </PopupHeader>
        <PopupContent>
          <Form onSubmit={handleSubmit}>
            {type === 'announcement' ? (
              <>
                <FormGroup>
                  <Label>공고명</Label>
                  <Select
                    name="title"
                    value={scheduleData.title}
                    onChange={handleChange}
                    required
                  >
                    <option value="">공고를 선택하세요</option>
                    {/* 여기에 나중에 백엔드에서 받아온 데이터를 매핑할 예정 */}
                  </Select>
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
                      <SubLabel>공고 마감 일자</SubLabel>
                      <Input
                        type="date"
                        name="date"
                        value={scheduleData.date}
                        onChange={handleChange}
                      />
                    </DateItem>
                    <DateItem>
                      <SubLabel>서류 합격 발표</SubLabel>
                      <Input
                        type="date"
                        name="deadlineDate"
                        value={scheduleData.deadlineDate}
                        onChange={handleChange}
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
                      <SubLabel>최종 발표 일자</SubLabel>
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
              <Label>메모</Label>
              <Textarea
                name="content"
                value={scheduleData.content}
                onChange={handleChange}
              />
            </FormGroup>
            <ActionButtonGroup>
              <SubmitButton type="submit">
                {isEditing ? '수정하기' : (type === 'schedule' ? '일정 추가' : '공고 추가')}
              </SubmitButton>
              <CancelButton type="button" onClick={onClose}>
                취소
              </CancelButton>
            </ActionButtonGroup>
          </Form>
        </PopupContent>
      </PopupWrapper>
    </PopupOverlay>
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
  z-index: 1100;  // EditSchedule의 z-index보다 높게 설정
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
  max-height: 70vh; // 뷰포트 높이의 70%로 제한
  overflow-y: auto; // 세로 스크롤 추가
`;

const Form = styled.form``;

const FormGroup = styled.div`
  margin-bottom: 15px;

  input, textarea {
    width: 97%; // 너비를 늘림
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    
    &:focus {
      outline: none;
      border-color: #ff9aa3;
    }
  }
`;

const Label = styled.label`
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
`;

const Input = styled.input`
  width: 97%; // 너비를 늘림
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  
  &:focus {
    outline: none;
    border-color: #ff9aa3;
  }
`;

const Textarea = styled.textarea`
  width: 97%; // textarea 너비도 늘림
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  height: 3cm;
  min-height: 3cm;
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

const CloseButton = styled.button`  background: none;
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
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-right: 20px;
`;

// Select 스타일 컴포넌트 추가
const Select = styled.select`
  width: 100%; // 너비를 98%로 늘림
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  box-sizing: border-box;
  height: 35px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 1em;
  padding-right: 40px;
  
  &:focus {
    outline: none;
    border-color: #ff9aa3;
  }
`;

export default AddSchedule;