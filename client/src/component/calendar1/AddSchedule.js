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
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
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
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 250,
    textAlign: 'center' },
    button: {
    width: '250px',
    backgroundColor: 'skyblue',
    color: 'white',
    marginTop: theme.spacing(2)
  }
}));

const AddSchedule = ({ onClose }) => {
  const classes = useStyles();
  const [date, setDate] = useState(
    moment().format().split(':')[0] + ':' + moment().format().split(':')[1]
  );
  const [title, setTitle] = useState('');
  const dispatch = useDispatch();

  const checkValid = () => {
    return title.length > 0 && title.trim().length > 0;
  };

  const onAddSchedule = () => {
    if (onClose) {
      onClose();
    }
    if (checkValid()) {
      const yyyymmdd = date.split('T')[0].replaceAll('-', '');
      const time = date.split('T')[1].replaceAll(':', '');
      const data = { date: yyyymmdd, time, title };

      dispatch(createSchedule(data));
      onClose();
    }
  };

  return (
    <Overlay>
      <Wrapper>
        <CloseButton onClick={onClose}>×</CloseButton>
        <Datepicker setDate={setDate} date={date} />
        <TextField
          id="standard-basic"
          label="어떤 일정이 있나요?"
          className={classes.textField}
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <Button
          className={classes.button}
          variant="contained"
          onClick={onAddSchedule}
        >
          추가하기
        </Button>
      </Wrapper>
    </Overlay>
  );
};

export default AddSchedule;