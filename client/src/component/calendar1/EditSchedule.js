import React, { useRef, useState, useEffect } from 'react';
import styled from 'styled-components';
import { MdChevronLeft } from 'react-icons/md';
import Datepicker from './Datepicker';
import { useDispatch, useSelector } from 'react-redux';
import {
  deleteSchedule,
  openEditPopup,
  updateSchedule
} from './redux/modules/schedule';

const EditSchedule = ({ history }) => {
  const dispatch = useDispatch();
  const { currentSchedule } = useSelector((state) => state.schedule);

  const inputTitle = useRef();
  const inputDescription = useRef();
  const [titleError, setTitleError] = useState(false);
  const [date, setDate] = useState('');


  useEffect(() => {
    if (currentSchedule) {
      const d = currentSchedule.date;
      const t = currentSchedule.time;
      setDate(
        d.slice(0, 4) +
        '-' +
        d.slice(4, 6) +
        '-' +
        d.slice(6) +
        'T' +
        (t ? (t.slice(0, 2) + ':' + t.slice(2)) : '00:00')
      );
    }
  }, [currentSchedule]);

  // 데이터가 없을 경우 예외처리
  if (!currentSchedule) {
    return null;
  }

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
        description,
        id: currentSchedule.id,
        type: currentSchedule.type || 'schedule'
      };

      dispatch(updateSchedule(data));
      dispatch(openEditPopup({ isOpen: false }));
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

  return (
    <Popup>
      <Header>
        <MdChevronLeft
          onClick={() => {
            dispatch(openEditPopup({ isOpen: false }));
          }}
        />
        {currentSchedule.type === 'announcement' ? '공고 보기' : '일정 보기'}
        <i />
      </Header>
      <Body>
        <Datepicker setDate={setDate} date={date} />
        <InputField>
          <input
            type="text"
            placeholder={currentSchedule.type === 'announcement' ? "공고 제목" : "어떤 일정이 있나요?"}
            defaultValue={currentSchedule.title}
            ref={inputTitle}
            className={titleError ? 'error' : ''}
          />
        </InputField>
        <TextArea>
          <textarea
            placeholder={currentSchedule.type === 'announcement' ? "공고 내용" : "간단 메모"}
            defaultValue={currentSchedule.description}
            ref={inputDescription}
            rows={4}
          />
        </TextArea>
        
        {currentSchedule.type === 'announcement' && (
          <InputField>
            <input
              type="url"
              placeholder="공고 링크"
              defaultValue={currentSchedule.link}
              name="link"
            />
          </InputField>
        )}

        <ButtonGroup>
          {currentSchedule.type !== 'announcement' && (
            <StyledButton
              disabled={currentSchedule.completed}
              onClick={onComplete}
              color="secondary"
            >
              완료
            </StyledButton>
          )}
          <StyledButton onClick={onSave} color="secondary">
            저장
          </StyledButton>
          <StyledButton onClick={onDelete} color="secondary">
            삭제
          </StyledButton>
        </ButtonGroup>
      </Body>
    </Popup>
  );
};

const Popup = styled.div`
  position: fixed;
  background-color: #fff3f3;
  transition: all 1s easy;
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

const InputField = styled.div`
  width: 250px;
  margin: 0 8px;
  text-align: center;

  input {
    width: 100%;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #ddd;
    background-color: transparent;
    font-size: 16px;

    &:focus {
      outline: none;
      border-bottom-color: #ff9aa3;
    }

    &.error {
      border-bottom-color: red;
    }
  }
`;

const TextArea = styled.div`
  width: 250px;
  margin: 0 8px;
  text-align: center;

  textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: transparent;
    font-size: 16px;
    resize: none;

    &:focus {
      outline: none;
      border-color: #ff9aa3;
    }
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 8px;
`;

const StyledButton = styled.button`
  padding: 6px 16px;
  border: none;
  background-color: #ff9aa3;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #ff8591;
  }

  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
`;

export default EditSchedule;