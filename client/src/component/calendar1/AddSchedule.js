import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { createSchedule } from './redux/modules/schedule';  // addSchedule을 createSchedule로 변경
import moment from 'moment';

const AddSchedule = ({ onClose, type }) => {
  const dispatch = useDispatch();
  const [scheduleData, setScheduleData] = useState({
    title: '',
    date: moment().format('YYYY-MM-DD'),
    content: '',
    completed: false
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setScheduleData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formattedDate = moment(scheduleData.date).format('YYYYMMDD');
    
    dispatch(createSchedule({   // addSchedule을 createSchedule로 변경
      ...scheduleData,
      date: formattedDate,
      type: type
    }));
    
    onClose();
  };

  const title = type === 'schedule' ? '일정 추가' : '공고 추가';
  
  return (
    <PopupOverlay onClick={onClose}>
      <PopupWrapper onClick={e => e.stopPropagation()}>
        <PopupHeader>
          <h2>{title}</h2>
          <CloseButton onClick={onClose}>&times;</CloseButton>
        </PopupHeader>
        <PopupContent>
          <Form onSubmit={handleSubmit}>
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
            
            <FormGroup>
              <Label>내용</Label>
              <Textarea
                name="content"
                value={scheduleData.content}
                onChange={handleChange}
                required
              />
            </FormGroup>

            {type === 'announcement' && (
              <FormGroup>
                <Label>공고 링크</Label>
                <Input
                  type="url"
                  name="link"
                  onChange={handleChange}
                  placeholder="https://"
                />
              </FormGroup>
            )}
            
            <ButtonGroup>
              <SubmitButton type="submit">
                {type === 'schedule' ? '일정 추가하기' : '공고 추가하기'}
              </SubmitButton>
              <CancelButton type="button" onClick={onClose}>
                취소
              </CancelButton>
            </ButtonGroup>
          </Form>
        </PopupContent>
      </PopupWrapper>
    </PopupOverlay>
  );
};

const PopupOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const PopupWrapper = styled.div`
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
`;

const PopupHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  h2 {
    margin: 0;
    color: #333;
  }
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  
  &:hover {
    color: #333;
  }
`;

const PopupContent = styled.div`
  width: 100%;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 15px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 5px;
`;

const Label = styled.label`
  font-weight: 500;
  color: #555;
`;

const Input = styled.input`
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  
  &:focus {
    outline: none;
    border-color: skyblue;
  }
`;

const Textarea = styled.textarea`
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-height: 100px;
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: skyblue;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
`;

const Button = styled.button`
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
`;

const SubmitButton = styled(Button)`
  background-color: skyblue;
  color: white;
  
  &:hover {
    background-color: #7ac7e6;
  }
`;

const CancelButton = styled(Button)`
  background-color: #e0e0e0;
  color: #666;
  
  &:hover {
    background-color: #bdbdbd;
  }
`;

export default AddSchedule;