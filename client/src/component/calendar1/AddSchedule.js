import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import moment from 'moment';
import styled from 'styled-components';
import { makeStyles } from '@mui/styles';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { createSchedule } from './redux/modules/schedule';
import Datepicker from './Datepicker';

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Wrapper = styled.div`
  padding: 40px 20px 20px 20px;        // 상하 패딩만 유지하고 좌우 패딩 제거
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 270px;
  max-width: 500px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  position: relative;
`;

const CloseButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  &:hover {
    color: #333;
  }
`;

const useStyles = makeStyles((theme) => ({
  textField: {
    width: 250,           // 기존 입력창 너비 유지
    textAlign: 'center',
    '& .MuiInputBase-root': {
      height: '120px'     // 입력창 높이 유지
    }
  },
  spacer: {              // 날짜창과 입력창 사이 빈 공간
    height: '5px'       // 5mm 정도의 간격
  },
  smallSpacer: {         // 입력창과 버튼 사이 간격
    height: '10px'        // 0.5mm
  },
  button: {
    width: 250,          // 입력창과 동일한 너비
    backgroundColor: 'skyblue',
    color: 'white',
    marginTop: '32px',
    padding: '12px'
  }
}));

const AddSchedule = ({ onClose }) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const [date, setDate] = useState(
    moment().format().split(':')[0] + ':' + moment().format().split(':')[1]
  );
  const [title, setTitle] = useState('');
  const [error, setError] = useState(''); // 에러 상태 추가

  const checkValid = () => {
    if (!title || title.trim().length === 0) {
      setError('제목을 입력해주세요');
      return false;
    }
    return true;
  };

  const onAddSchedule = async () => {
    try {
      if (checkValid()) {
        console.log('Adding schedule - Initial data:', { date, title }); // 디버깅 로그

        const yyyymmdd = date.split('T')[0].replaceAll('-', '');
        const time = date.split('T')[1].replaceAll(':', '');
        
        const scheduleData = {
          date: yyyymmdd,
          time,
          title: title.trim(),
          completed: false
        };

        console.log('Processed schedule data:', scheduleData); // 디버깅 로그

        // createSchedule 액션 디스패치
        await dispatch(createSchedule(scheduleData));
        console.log('Schedule created successfully'); // 디버깅 로그

        // 팝업 닫기
        if (onClose) {
          onClose();
        }
      }
    } catch (error) {
      console.error('Error adding schedule:', error);
      setError('일정 추가 중 오류가 발생했습니다');
    }
  };

  return (
    <Overlay onClick={(e) => e.stopPropagation()}>
      <Wrapper>
        <CloseButton onClick={onClose}>×</CloseButton>
        <Datepicker setDate={setDate} date={date} />
        <div className={classes.spacer} />
        <TextField
          id="standard-basic"
          label="어떤 일정이 있나요?"
          className={classes.textField}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          error={!!error}
          helperText={error}
        />
        <div className={classes.smallSpacer} />
        <Button
          className={classes.button}
          variant="contained"
          onClick={onAddSchedule}
          disabled={!title.trim()}
        >
          추가하기
        </Button>
      </Wrapper>
    </Overlay>
  );
};

export default AddSchedule;