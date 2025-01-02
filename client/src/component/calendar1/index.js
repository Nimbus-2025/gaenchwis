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
    <Body>
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
      <ButtonWrapper onClick={() => dispatch(openEditPopup(false))}>
      {isFilter ? (
        <MdCheck
          onClick={(e) => {
            e.stopPropagation();  // 이벤트 버블링 방지
            onFilter(false);
          }}
          className={'filterBtn subBtn'}
        />
      ) : (
        <MdDoneAll
          onClick={(e) => {
            e.stopPropagation();  // 이벤트 버블링 방지
            onFilter(true);
          }}
          className={'filterBtn subBtn'}
        />
      )}
      <MdEdit 
        onClick={(e) => {
          e.stopPropagation();  // 이벤트 버블링 방지
          goToAddSchedule();
        }}
        className={'writeBtn subBtn'}
      />
      <MdDehaze className={'menuBtn'} />
    </ButtonWrapper>
    </Body>
  );
};
const Body = styled.div`
  width: 50%;
  position: relative;  // 추가
`;

const ButtonWrapper = styled.div`
  position: fixed; 
  right: 350px;   
  bottom: 50px;  
  text-align: center;
  padding-bottom: 3px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  height: 150px;
  z-index: 1000;

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
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);  // 그림자 효과 추가

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
`;

const Header = styled.div`
  height: 7vh;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px;
  font-size: 1.5em;
`;

const YearDisplay = styled.div`
  color: #666;
  font-size: 0.8em;
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

    &:hover {
      cursor: pointer;
      color: #ffdb0d;
      background-color: rgba(255, 219, 13, 0.1);
    }
    &:active {
      transform: scale(0.95);
      background-color: rgba(255, 219, 13, 0.2);
    }
  }
`;

const DateContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 1vw;
  padding: 20px;
`;

const Weekend = styled.div`
  display: flex;
`;

const Dow = styled.div`
  border-bottom: 1px solid gray;
  width: 100%;
  height: 35px;
  color: ${(props) => (props.color ? props.color : 'black')};
  text-align: center;
`;

const DayWrapper = styled.div`
  padding-top: 4px;
  height: 12vh;
  display: flex;
  align-items: center;
  width: 100%;
  flex-direction: column;
  flex-wrap: nowrap;
  overflow: hidden;

  &.grayed {
    color: gray;
  }

  &.today > .title {
-   color: white;
-   background-color: skyblue;
+   color: skyblue;
+   border: 2px solid skyblue;
+   border-radius: 50%;
+   width: 30px;
+   height: 30px;
+   display: flex;
+   justify-content: center;
+   align-items: center;
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