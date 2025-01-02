import React, { useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import moment from 'moment';
import styled from 'styled-components';
import { makeStyles } from '@mui/styles';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import { 
  MdChevronLeft, 
  MdEdit, 
  MdVisibility, 
  MdVisibilityOff 
} from 'react-icons/md';
import {
  deleteSchedule,
  updateSchedule,
  toggleScheduleVisibility,
  addSchedule,
  createSchedule,
  openEditPopup
} from './redux/modules/schedule';
import Datepicker from './Datepicker';

// muiStyled를 styled로 변경하거나, @mui/material/styles에서 import
import { styled as muiStyled } from '@mui/material/styles';

// MUI 스타일드 컴포넌트
const StyledTextField = muiStyled(TextField)(({ theme }) => ({
  marginLeft: theme.spacing(1),
  marginRight: theme.spacing(1),
  width: 250,
  textAlign: 'center'
}));

// AddSchedulePopup 컴포넌트
const AddSchedulePopup = ({ onClose }) => {
  const dispatch = useDispatch();
  const [newDate, setNewDate] = useState(new Date().toISOString().slice(0, 16));
  const newTitleRef = useRef();
  const newDescriptionRef = useRef();
  const [newTitleError, setNewTitleError] = useState(false);

  const handleSave = () => {
    const title = newTitleRef.current.value;
    if (!title || title.trim().length === 0) {
      setNewTitleError(true);
      return;
    }

    const yyyymmdd = newDate.split('T')[0].replaceAll('-', '');
    const time = newDate.split('T')[1].replaceAll(':', '');
    
    const data = {
      date: yyyymmdd,
      time,
      title,
      description: newDescriptionRef.current.value,
      completed: false
    };

    dispatch(addSchedule(data));
    onClose();
  };

  // EditSchedule.js - Part 2 (AddSchedulePopup 컴포넌트의 return 부분)

  return (
    <PopupOverlay>
      <AddPopup>
        <PopupHeader>
          <h3>새 일정 추가</h3>
          <CloseButton onClick={onClose}>&times;</CloseButton>
        </PopupHeader>
        <PopupBody>
          <Datepicker setDate={setNewDate} date={newDate} />
          <StyledTextField
            id="new-schedule-title"
            label="일정 제목"
            error={newTitleError}
            inputRef={newTitleRef}
            sx={{ marginTop: '20px' }}
            onChange={() => setNewTitleError(false)}
          />
          <StyledTextField
            id="new-schedule-description"
            label="상세 내용"
            multiline
            inputRef={newDescriptionRef}
            rows={4}
            variant="outlined"
            sx={{ marginTop: '20px' }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleSave}
            sx={{ marginTop: '20px' }}
          >
            저장
          </Button>
        </PopupBody>
      </AddPopup>
    </PopupOverlay>
  );
};

// EditSchedule 메인 컴포넌트
const EditSchedule = ({ history }) => {
  const dispatch = useDispatch();
  const { currentSchedule, isVisible } = useSelector((state) => state.schedule);
  const [showAddPopup, setShowAddPopup] = useState(false);

  const d = currentSchedule?.date || '';
  const t = currentSchedule?.time || '';
  const [date, setDate] = useState(
    d ? `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6)}T${t.slice(0, 2)}:${t.slice(2)}` : ''
  );

  const inputTitle = useRef();
  const inputDescription = useRef();
  const [titleError, setTitleError] = useState(false);
  const [showManageButtons, setShowManageButtons] = useState(false);
  // EditSchedule.js - Part 3 (EditSchedule 컴포넌트의 핸들러 함수들)

  // 일정 추가 핸들러
  const handleAddSchedule = () => {
    setShowAddPopup(true);
    setShowManageButtons(false);
  };

  // 일정 표시/숨김 토글 핸들러
  const handleToggleVisibility = () => {
    dispatch(toggleScheduleVisibility());
    setShowManageButtons(false);
  };

  const onSave = () => {
    if (checkValid()) {
      const yyyymmdd = date.split('T')[0].replaceAll('-', '');
      const time = date.split('T')[1].replaceAll(':', '');
      const title = inputTitle.current.value;
      const description = inputDescription.current.value;
  
      const data = {
        date: yyyymmdd,
        time,
        title,
        description
      };
  
      console.log('Saving schedule:', data); // 데이터 확인용 로그 추가
      
      if (currentSchedule?.id) {
        dispatch(updateSchedule({ ...data, id: currentSchedule.id }));
      } else {
        dispatch(createSchedule(data));
      }
      
      dispatch(openEditPopup(false));
    }
  };

  const checkValid = () => {
    const title = inputTitle.current.value;

    if (title.length === 0 || title.trim().length === 0) {
      setTitleError(true);
      return false;
    }

    return true;
  };

  const onComplete = () => {
    const data = { ...currentSchedule, completed: true };
    dispatch(openEditPopup(false));
    dispatch(updateSchedule(data));
  };

  const onDelete = () => {
    dispatch(openEditPopup(false));
    dispatch(deleteSchedule(currentSchedule.id));
  };

  // EditSchedule.js - Part 4 (EditSchedule 컴포넌트의 return 부분)

  return (
    <Popup>
      <Header>
        <MdChevronLeft
          onClick={() => {
            dispatch(openEditPopup(false));
          }}
        />
        일정 보기
        <ManageButtonContainer>
          <MainButton onClick={() => setShowManageButtons(!showManageButtons)}>
            일정 관리
          </MainButton>
          {showManageButtons && (
            <ButtonsDropdown>
              <DropdownButton onClick={handleAddSchedule}>
                <MdEdit /> 일정 추가
              </DropdownButton>
              <DropdownButton onClick={handleToggleVisibility}>
                {isVisible ? <MdVisibilityOff /> : <MdVisibility />}
                일정 {isVisible ? '숨기기' : '보이기'}
              </DropdownButton>
            </ButtonsDropdown>
          )}
        </ManageButtonContainer>
      </Header>
      <Body>
        <Datepicker setDate={setDate} date={date} />
        <StyledTextField
          id="standard-basic"
          label="어떤 일정이 있나요?"
          defaultValue={currentSchedule?.title}
          error={titleError}
          inputRef={inputTitle}
          sx={{ marginTop: '40px' }}
          onChange={(e) => {
            setTitleError(false);
          }}
        />
        <StyledTextField
          id="outlined-multiline-static"
          label="간단 메모"
          multiline
          defaultValue={currentSchedule?.description}
          inputRef={inputDescription}
          rows={4}
          variant="outlined"
          onChange={(e) => {}}
        />
        <ButtonGroup
          variant="contained"
          color="secondary"
          aria-label="outlined secondary button group"
          sx={{ marginTop: '20px' }}
        >
          <Button 
            disabled={currentSchedule?.completed} 
            onClick={onComplete}
          >
            완료
          </Button>
          <Button onClick={onSave}>저장</Button>
          <Button onClick={onDelete}>삭제</Button>
        </ButtonGroup>
      </Body>
      {showAddPopup && (
        <AddSchedulePopup onClose={() => setShowAddPopup(false)} />
      )}
    </Popup>
  );
};

// EditSchedule.js - Part 5 (styled-components)

const Popup = styled.div`
  position: fixed;
  background-color: #fff3f3;
  transition: all 1s ease;
  box-shadow: 5px 10px 20px gray;
  border-radius: 20px;
  /* Mobile Device */
  @media screen and (max-width: 767px) {
    width: 100%;
    top: 0;
    height: 100%;
    box-shadow: none;
    border-radius: 0px;
  }

  /* Tablet Device */
  @media screen and (min-width: 768px) and (max-width: 991px) {
    width: 350px;
    top: 5vh;
    left: 32vw;
    height: 80vh;
  }

  /* Desktop Device */
  @media screen and (min-width: 992px) {
    top: 5vh;
    left: 38vw;
    width: 25vw;
    height: 80vh;
  }
`;

const Header = styled.div`
  height: 7vh;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 3px;
  font-size: 1.5em;

  & * {
    color: #cccccc;
  }

  & > svg {
    cursor: pointer;
  }
`;

const Body = styled.div`
  padding-top: 6vh;
  height: 50vh;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
`;

const ManageButtonContainer = styled.div`
  position: relative;
  display: inline-block;
`;

const MainButton = styled.button`
  padding: 8px 16px;
  background-color: #ffd700;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  &:hover {
    background-color: #ffed4a;
  }
`;

const ButtonsDropdown = styled.div`
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  z-index: 1000;
`;

const DropdownButton = styled.button`
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 16px;
  border: none;
  background: none;
  cursor: pointer;
  white-space: nowrap;
  
  &:hover {
    background-color: #f5f5f5;
  }
  
  &:first-child {
    color: #87ceeb;
  }
  
  &:last-child {
    color: #ff69b4;
  }
`;

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

const AddPopup = styled.div`
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
`;

const PopupHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const PopupBody = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  color: #666;
  
  &:hover {
    color: #000;
  }
`;

export default EditSchedule;