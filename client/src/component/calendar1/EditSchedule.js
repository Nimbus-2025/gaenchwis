import React, { useRef, useState, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { MdChevronLeft } from 'react-icons/md';
import Datepicker from './Datepicker';
import { Button, TextField, makeStyles, ButtonGroup } from '@material-ui/core';
import { useDispatch, useSelector } from 'react-redux';
import {
  deleteSchedule,
  openEditPopup,
  updateSchedule
} from './redux/modules/schedule';

// useStyles를 컴포넌트 외부로 이동
const useStyles = makeStyles((theme) => ({
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 250,
    textAlign: 'center'
  }
}));

const EditSchedule = () => {
  const dispatch = useDispatch();
  const { currentSchedule } = useSelector((state) => state.schedule);

  const initialDate = useMemo(() => {
    const { date: d, time: t } = currentSchedule;
    return `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6)}T${t.slice(0, 2)}:${t.slice(2)}`;
  }, [currentSchedule]);

  const [date, setDate] = useState(initialDate);
  const [titleError, setTitleError] = useState(false);
  
  const inputTitle = useRef();
  const inputDescription = useRef();
  const classes = useStyles();

  const checkValid = useCallback(() => {
    const title = inputTitle.current.value;
    if (!title || !title.trim()) {
      setTitleError(true);
      return false;
    }
    return true;
  }, []);

  const onSave = useCallback(() => {
    if (checkValid()) {
      const [yyyymmdd, time] = date.split('T');
      const data = {
        date: yyyymmdd.replaceAll('-', ''),
        time: time.replaceAll(':', ''),
        title: inputTitle.current.value,
        description: inputDescription.current.value,
        id: currentSchedule.id
      };

      dispatch(updateSchedule(data));
      dispatch(openEditPopup(false));
    }
  }, [date, currentSchedule.id, dispatch, checkValid]);

  const onComplete = useCallback(() => {
    dispatch(updateSchedule({ ...currentSchedule, completed: true }));
    dispatch(openEditPopup(false));
  }, [currentSchedule, dispatch]);

  const onDelete = useCallback(() => {
    dispatch(deleteSchedule(currentSchedule.id));
    dispatch(openEditPopup(false));
  }, [currentSchedule.id, dispatch]);

  const handleClose = useCallback(() => {
    dispatch(openEditPopup(false));
  }, [dispatch]);

  return (
    <Popup>
      <Header>
        <MdChevronLeft onClick={handleClose} />
        일정 보기 &nbsp;&nbsp;&nbsp;
        <i />
      </Header>
      <Body>
        <Datepicker setDate={setDate} date={date} />
        <TextField
          id="standard-basic"
          label="어떤 일정이 있나요?"
          defaultValue={currentSchedule.title}
          error={titleError}
          className={classes.textField}
          inputRef={inputTitle}
          helperText={titleError ? "제목을 입력해주세요" : ""}
        />
        <TextField
          id="outlined-multiline-static"
          label="간단 메모"
          multiline
          defaultValue={currentSchedule.description}
          inputRef={inputDescription}
          className={classes.textField}
          rows={4}
          variant="outlined"
        />
        <ButtonGroup
          color="secondary"
          aria-label="outlined secondary button group"
        >
          <Button 
            disabled={currentSchedule.completed} 
            onClick={onComplete}
          >
            완료
          </Button>
          <Button onClick={onSave}>저장</Button>
          <Button onClick={onDelete}>삭제</Button>
        </ButtonGroup>
      </Body>
    </Popup>
  );
};

const Popup = styled.div`
  position: fixed;
  background-color: #fff3f3;
  transition: all 1s ease;
  box-shadow: 5px 10px 20px gray;
  border-radius: 20px;
  z-index: 1000;

  @media screen and (max-width: 767px) {
    width: 100%;
    top: 0;
    height: 100%;
    box-shadow: none;
    border-radius: 0;
  }

  @media screen and (min-width: 768px) and (max-width: 991px) {
    width: 350px;
    top: 5vh;
    left: 32vw;
    height: 80vh;
  }

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

EditSchedule.propTypes = {
  currentSchedule: PropTypes.shape({
    id: PropTypes.string.isRequired,
    date: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string,
    completed: PropTypes.bool
  })
};

export default EditSchedule;