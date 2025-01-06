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
  openEditPopup
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

const Calendar = () => {
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
          <AddSchedule onClose={() => setIsAddPopupOpen(false)} />
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
              e.stopPropagation();
              onFilter(false);
            }}
            className={'filterBtn subBtn'}
          />
        ) : (
          <MdDoneAll
            onClick={(e) => {
              e.stopPropagation();
              onFilter(true);
            }}
            className={'filterBtn subBtn'}
          />
        )}
        <MdEdit
          onClick={(e) => {
            e.stopPropagation();
            setIsAddPopupOpen(true);
          }}
          className={'writeBtn subBtn'}
        />
        <MdDehaze className={'menuBtn'} />
      </ButtonWrapper>
    </Body>
  );
};

export default Calendar;