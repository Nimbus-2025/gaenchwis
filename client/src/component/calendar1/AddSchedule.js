import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { MdChevronLeft } from 'react-icons/md';
import Datepicker from './Datepicker';
import { Button, TextField } from '@mui/material';
import { makeStyles } from '@mui/styles';
import { createSchedule } from './redux/modules/schedule';
import moment from 'moment';


// 스타일 컴포넌트들을 먼저 정의
const Wrapper = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  z-index: 1000;
  padding: 0 10px;
  display: flex;
  flex-direction: column;
  align-items: center;

  /* Mobile Device */
  @media screen and (max-width: 767px) {
    width: 90vw;
    max-width: 400px;
  }

  /* Tablet Device */
  @media screen and (min-width: 768px) and (max-width: 991px) {
    width: 60vw;
    max-width: 500px;
  }

  /* Desktop Device */
  @media screen and (min-width: 992px) {
    width: 30vw;
    max-width: 400px;
  }
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
`;

const Header = styled.div`
  background-color: white;
  height: 7vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 3px;
  font-size: 1.5em;

  & * {
    color: #cccccc;
    cursor: pointer;
  }

  /* Mobile Device */
  @media screen and (max-width: 767px) {
    width: 100%;
  }

  /* Tablet Device */
  @media screen and (min-width: 768px) and (max-width: 991px) {
    width: 100%;
  }

  /* Desktop Device */
  @media screen and (min-width: 992px) {
    width: 100%;
  }
`;

const Body = styled.div`
  padding: 20px;
  height: calc(100% - 7vh);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; // 추가
  gap: 20px;

  /* 내용물을 감싸는 컨테이너 추가 */
  & > div:not(:first-child) {
    margin-top: 20px;
  }

  /* Datepicker와 입력 필드들을 포함하는 영역 */
  & > * {
    width: 100%;
    max-width: 250px;
    display: flex;
    justify-content: center;
  }
`;



// useStyles 정의
const useStyles = makeStyles((theme) => ({
  textField: {
    marginLeft: theme?.spacing?.(1) || '8px',
    marginRight: theme?.spacing?.(1) || '8px',
    width: 250,
    textAlign: 'center',
    '& label': {
      color: '#1976d2'
    },
    '& .MuiInput-underline:before': {
      borderBottom: '1px solid #1976d2'
    },
    '& .MuiInput-underline:hover:not(.Mui-disabled):before': {
      borderBottom: '2px solid #1976d2'
    },
    '& .MuiInput-underline:after': {
      borderBottomColor: '#1976d2'
    }
  },
  button: {
    width: '250px',
    backgroundColor: props => props.hasInput ? '#1976d2' : 'white',
    color: props => props.hasInput ? 'white' : 'rgba(0, 0, 0, 0.26)',
    border: props => props.hasInput ? 'none' : '1px solid rgba(0, 0, 0, 0.12)',
    '&:hover': {
      backgroundColor: props => props.hasInput ? '#115293' : 'white'
    }
  }
}));

// AddSchedule 컴포넌트 정의
const AddSchedule = ({ onClose }) => {  // onClose props 추가
  const dispatch = useDispatch();
  const [date, setDate] = useState(
    moment().format().split(':')[0] + ':' + moment().format().split(':')[1]
  );
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [titleError, setTitleError] = useState(false);
  const classes = useStyles({ hasInput: title.trim().length > 0 });

  const checkValid = () => {
    if (title.length === 0 || title.trim().length === 0) {
      setTitleError(true);
      return false;
    }
    return true;
  };

  const onAddSchedule = () => {
    if (checkValid()) {
      const yyyymmdd = date.split('T')[0].replaceAll('-', '');
      const time = date.split('T')[1].replaceAll(':', '');
      const scheduleData = {
        date: yyyymmdd,
        time,
        title,
        description,
      };

      dispatch(createSchedule(scheduleData));
      onClose();  // props로 받은 onClose 함수 호출
    }
  };

  const handleAddSchedule = () => {  // onAddSchedule을 handleAddSchedule로 이름 변경
    if (checkValid()) {
      const yyyymmdd = date.split('T')[0].replaceAll('-', '');
      const time = date.split('T')[1].replaceAll(':', '');
      const scheduleData = {
        date: yyyymmdd,
        time,
        title,
        description,
      };

      dispatch(createSchedule(scheduleData));
      onClose();  // 팝업 닫기
    }
  };

  return (
    <>
      <Overlay onClick={onClose} />
      <Wrapper>
        <Header>
          <MdChevronLeft onClick={onClose} />
          일정 추가 &nbsp;&nbsp;&nbsp;
          <i />
        </Header>
        <Body>
          <Datepicker setDate={setDate} date={date} />
          <TextField
            id="standard-basic"
            label="어떤 일정이 있나요?"
            error={titleError}
            className={classes.textField}
            onChange={(e) => {
              setTitle(e.target.value);
              if (titleError) setTitleError(false);
            }}
            value={title}
          />
          <TextField
            id="outlined-multiline-static"
            label="간단 메모"
            multiline
            rows={4}
            className={classes.textField}
            variant="outlined"
            onChange={(e) => setDescription(e.target.value)}
            value={description}
          />
          <Button
            className={classes.button}
            variant="contained"
            onClick={onAddSchedule}
            disabled={!title.trim()}
          >
            + ADD
          </Button>
        </Body>
      </Wrapper>
    </>
  );
};

export default AddSchedule;