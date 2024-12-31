import React, { useEffect, useState } from 'react';
import moment from 'moment';
import 'moment/locale/ko';
import styled from 'styled-components';
import {
  MdChevronLeft,
  MdChevronRight,
  MdDehaze,
  MdCheck,
  MdDoneAll,
  MdEdit
} from 'react-icons/md';
import { useDispatch, useSelector } from 'react-redux';
import {
  readSchedule,
  setIsFilter,
  openEditPopup
} from './redux/modules/schedule';
import Day from './Day';
import EditSchedule from './EditSchedule';
import AddSchedule from './AddSchedule';

const Calendar = ({ history }) => {
  const { thisMonth, isOpenEditPopup, isFilter } = useSelector(
    (state) => state.schedule
  );
  const [isAddPopupOpen, setIsAddPopupOpen] = useState(false);
  const [current, setCurrent] = useState(moment());
  const dispatch = useDispatch();

  useEffect(() => {
    const startDay = current.clone().startOf('month').format('YYYYMMDD');
    const endDay = current.clone().endOf('month').format('YYYYMMDD');
    dispatch(readSchedule({ startDay, endDay }));
  }, [current, dispatch, isOpenEditPopup, isFilter]);

  const movePrevMonth = () => {
    setCurrent(current.clone().subtract(1, 'month'));
  };

  const moveNextMonth = () => {
    setCurrent(current.clone().add(1, 'month'));
  };

  const goToAddSchedule = () => {
    setIsAddPopupOpen(true);
  };

  const generate = () => {
    const startWeek = current.clone().startOf('month').week();
    const endWeek =
      current.clone().endOf('month').week() === 1
        ? 53
        : current.clone().endOf('month').week();

    let calendar = [];

    for (let w = startWeek; w <= endWeek; w++) {
      calendar.push(
        <Weekend key={w}>
          {Array(7)
            .fill(0)
            .map((n, idx) => {
              const noFormatDate = current
                .clone()
                .startOf('year')
                .week(w)
                .startOf('week')
                .add(idx, 'day');

              const day = noFormatDate.format('D');
              const fullDate = noFormatDate.format('l').replaceAll('.', '');
              const isToday =
                noFormatDate.format('YYYYMMDD') === moment().format('YYYYMMDD')
                  ? 'today'
                  : '';
              const isGrayed =
                noFormatDate.format('MM') === current.format('MM')
                  ? ''
                  : 'grayed';

              const currentSch = thisMonth.filter((s) => {
                return s.date === fullDate;
              });

              const dateInfo = { day, fullDate, dow: idx, currentSch };
              return (
                <Day
                  key={n + idx}
                  dateInfo={dateInfo}
                  className={`${isGrayed} ${isToday}`}
                />
              );
            })}
        </Weekend>
      );
    }
    return calendar;
  };

  const onFilter = (isFilter) => {
    dispatch(setIsFilter(isFilter));
  };

  return (
    <div>
      <CalendarWrapper>
        {isOpenEditPopup && <EditSchedule />}
        {isAddPopupOpen && (
          <AddSchedule
            onClose={() => setIsAddPopupOpen(false)}
          />
        )}
        <Header>
          <YearDisplay>{current.format('YYYY')}</YearDisplay>
          <HeaderContent>
            <MdChevronLeft
              className="dir"
              onClick={movePrevMonth}
            ></MdChevronLeft>
            <span>{current.format('MMMM')}</span>
            <MdChevronRight
              className="dir"
              onClick={moveNextMonth}
            ></MdChevronRight>
          </HeaderContent>
        </Header>
        <DateContainer>
          <Weekend className="row">
            <Dow color="#ff4b4b">
              <span>S</span>
            </Dow>
            <Dow>
              <span>M</span>
            </Dow>
            <Dow>
              <span>T</span>
            </Dow>
            <Dow>
              <span>W</span>
            </Dow>
            <Dow>
              <span>T</span>
            </Dow>
            <Dow>
              <span>F</span>
            </Dow>
            <Dow color="#4b87ff">
              <span>S</span>
            </Dow>
          </Weekend>
          {generate()}
        </DateContainer>
      </CalendarWrapper>
      <ButtonWrapper>
        {isFilter ? (
          <MdCheck
            onClick={() => onFilter(false)}
            className={'filterBtn subBtn'}
          />
        ) : (
          <MdDoneAll
            onClick={() => onFilter(true)}
            className={'filterBtn subBtn'}
          />
        )}
        <MdEdit 
          onClick={goToAddSchedule}
          className={'writeBtn subBtn'}
        />
        <MdDehaze className={'menuBtn'} />
      </ButtonWrapper>
    </div>
  );
};

const ButtonWrapper = styled.div`
  position: fixed;
  right: 50px;
  bottom: 50px;
  text-align: center;
  padding-bottom: 3px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  height: 150px;

  &:hover .subBtn {
    opacity: 1;
    visibility: visible;
    top: 0;
  }

  & > svg {
    cursor: pointer;
    border-radius: 50%;
    color: white;
    width: 25px;
    height: 25px;
    padding: 10px;

    &.filterBtn {
      background-color: pink;
      z-index: 1;
      transition: all 0.4s ease;
    }

    &.writeBtn {
      background-color: skyblue;
      z-index: 2;
      transition: all 0.5s ease;
    }

    &.menuBtn {
      background-color: #ffdb0d;
      z-index: 3;
    }

    &.subBtn {
      opacity: 0;
      visibility: hidden;
      top: 60px;
      position: relative;
    }
  }
`;

const CalendarWrapper = styled.div`
  position: relative;
  max-width: 1600px;
  margin: 0 auto;
  padding: 20px 40px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
`;

const Header = styled.div`
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px;
  font-size: 2em;
`;

const YearDisplay = styled.div`
  color: #666;
  font-size: 1em;
  margin-bottom: 5px;
  margin-left: 10px;
`;

const HeaderContent = styled.div`
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

  & > span {
    margin: 0 100px;
  }
  & > .dir {
    color: #cccccc;
    transition: all 0.3s ease;
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    position: relative;

    &:hover {
      cursor: pointer;
      color: #ffdb0d;
      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 219, 13, 0.1);
        border-radius: 50%;
        z-index: -1;
      }
    }
    &:active {
      transform: scale(0.95);
      &::after {
        background-color: rgba(255, 219, 13, 0.2);
      }
    }
  }
`;

const DateContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 1vw;
  padding: 20px 0;
`;

const Weekend = styled.div`
  display: flex;
  margin-bottom: 10px;
`;

const Dow = styled.div`
  border-bottom: 1px solid gray;
  width: 100%;
  height: 50px;
  font-size: 1.2em;
  color: ${(props) => (props.color ? props.color : 'black')};
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const DayWrapper = styled.div`
  padding-top: 4px;
  height: 120px;
  display: flex;
  align-items: center;
  width: 100%;
  flex-direction: column;
  flex-wrap: nowrap;
  overflow: hidden;
  border: 1px solid #eee;

  &:hover {
    background-color: #f8f9fa;
  }

  &.grayed {
    color: gray;
  }

  &.today > .title {
    color: skyblue;
    border: 2px solid skyblue;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  & > .title {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
  }
`;

export default Calendar; 