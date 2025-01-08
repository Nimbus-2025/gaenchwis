import React, { useState, useEffect } from 'react';
import moment from 'moment';
import 'moment/locale/ko';
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
  openEditPopup,
  openAddSchedule,
  closeAddSchedule
} from './redux/modules/schedule';
import Day from './Day';
import EditSchedule from './EditSchedule';
import AddSchedule from './AddSchedule';
import {
  Body,
  ButtonWrapper,
  CalendarWrapper,
  Header,
  YearDisplay,
  HeaderContent,
  DateContainer,
  Weekend,
  Dow
} from './styles/CalendarStyles';

// 캘린더 렌더링
const Calendar = () => {
  const { thisMonth, isOpenEditPopup, isFilter, isOpenAddPopup } = useSelector(
    (state) => state.schedule
  );
  const [current, setCurrent] = useState(moment());
  const [activePopup, setActivePopup] = useState(null);
  const dispatch = useDispatch();

  useEffect(() => {
    const startDay = current.clone().startOf('month').format('YYYYMMDD');
    const endDay = current.clone().endOf('month').format('YYYYMMDD');
    dispatch(readSchedule({ startDay, endDay }));
  }, [current, dispatch, isOpenEditPopup]);

  const movePrevMonth = () => {
    setCurrent(current.clone().subtract(1, 'month'));
  };

  const moveNextMonth = () => {
    setCurrent(current.clone().add(1, 'month'));
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

              const currentSch = thisMonth.filter((s) => s.date === fullDate);

              const dateInfo = { day, fullDate, dow: idx, currentSch };
              return (
                <Day
                  key={`${w}-${idx}`}
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

  return (
    <Body>
      <CalendarWrapper>
        {isOpenEditPopup && <EditSchedule />}
        {activePopup === 'schedule' && (
          <AddSchedule onClose={() =>  setActivePopup(null)}
          type="schedule"
        />
        )}
        {activePopup === 'announcement' && (
          <AddSchedule 
            onClose={() => setActivePopup(null)}
            type="announcement"
          />
        )}
        <Header>
          <YearDisplay>{current.format('YYYY')}</YearDisplay>
          <HeaderContent>
            <MdChevronLeft className="dir" onClick={movePrevMonth} />
            <span>{current.format('MMMM')}</span>
            <MdChevronRight className="dir" onClick={moveNextMonth} />
          </HeaderContent>
        </Header>
        <DateContainer>
          <Weekend>
            <Dow color="#ff4b4b">S</Dow>
            <Dow>M</Dow>
            <Dow>T</Dow>
            <Dow>W</Dow>
            <Dow>T</Dow>
            <Dow>F</Dow>
            <Dow color="#4b87ff">S</Dow>
          </Weekend>
          {generate()}
        </DateContainer>
      </CalendarWrapper>
      <ButtonWrapper onClick={() => dispatch(openEditPopup({ isOpen: false }))}>
        {isFilter ? (
          <MdCheck
            onClick={(e) => {
              e.stopPropagation();
              dispatch(setIsFilter(false));
            }}
            className="filterBtn subBtn"
          />
        ) : (
          <MdDoneAll
            onClick={(e) => {
              e.stopPropagation();
              dispatch(setIsFilter(true));
            }}
            className="filterBtn subBtn"
          />
        )}
        <MdEdit className="writeBtn subBtn" />
        <div className="popup-buttons">
          <div 
            className="popup-button"
            onClick={(e) => {
              e.stopPropagation();
              setActivePopup('schedule');
            }}
          >
            일정 추가
          </div>
          <div 
            className="popup-button"
            onClick={(e) => {
              e.stopPropagation();
              setActivePopup('announcement');
            }}
          >
            공고 추가
          </div>
        </div>
        <MdDehaze className="menuBtn" />
      </ButtonWrapper>
    </Body>
  );
};

export default Calendar;