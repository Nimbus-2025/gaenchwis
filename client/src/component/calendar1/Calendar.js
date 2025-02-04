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
  Dow,
  SelectDropdown,
  SelectOption,
  MonthDisplay,
  WeekdayHeader
} from './styles/CalendarStyles';
import styled from 'styled-components';
import api from '../../api/api';
import Proxy from '../../api/Proxy';

// 캘린더 렌더링
const Calendar = ({setSchedules, schedules}) => {
  const { thisMonth, isOpenEditPopup, isFilter, isOpenAddPopup } = useSelector(
    (state) => state.schedule
  );
  const dispatch = useDispatch();
  const [current, setCurrent] = useState(moment());
  const [activePopup, setActivePopup] = useState(null);
  const [filterType, setFilterType] = useState('all');
  const [showYearSelect, setShowYearSelect] = useState(false);
  const [showMonthSelect, setShowMonthSelect] = useState(false);

  // 년도 선택 옵션 생성 (현재 년도부터 1950년까지 내림차순)
  const yearOptions = Array.from(
    { length: moment().year() - 1950 + 1 }, 
    (_, i) => moment().year() - i
  );

  // 월 선택 옵션 생성
  const monthOptions = Array.from({ length: 12 }, (_, i) => i);

  // 년도 변경 핸들러
  const handleYearChange = (year) => {
    setCurrent(current.clone().year(year));
    setShowYearSelect(false);
  };

  // 월 변경 핸들러
  const handleMonthChange = (month) => {
    setCurrent(current.clone().month(month));
    setShowMonthSelect(false);
  };

  // 일정 조회 함수
  const fetchSchedules = async () => {
    try {
      const userData = sessionStorage.getItem('user');
      if (!userData) {
        alert('로그인이 필요합니다.');
        return;
      }

      const parsedUserData = JSON.parse(userData);
      const userId = parsedUserData.user_id;

      const response = await api(
        `${Proxy.server}:8006/api/v1/schedules`,
        'GET'
      );


      // 서버 응답에서 Array 데이터 직접 처리
      if (response && Array.isArray(response)) {
        const scheduleList = response.map(schedule => ({
          type: schedule.schedule_type ? schedule.schedule_type : "schedule",
          company: schedule.company,
          id: schedule.schedule_id,
          title: schedule.schedule_title,
          date: schedule.schedule_date ? schedule.schedule_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          schedule_deadline: schedule.schedule_deadline && schedule.schedule_deadline!=="채용시" ? schedule.schedule_deadline.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          document_result_date: schedule.document_result_date ? schedule.document_result_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          interview_date: schedule.interview_date ? schedule.interview_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          final_date: schedule.final_date ? schedule.final_date.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3') : null,
          schedule_content: schedule.schedule_content,
          is_completes: schedule.is_completes
        }));
        setSchedules(scheduleList);
      }
    } catch (error) {
      console.error('일정 조회 중 오류 발생:', error);
    }
  };

  // 컴포넌트 마운트 시 일정 조회
  useEffect(() => {
    fetchSchedules();
  }, []);

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
    const endWeek = current.clone().endOf('month').week() === 1
      ? 53
      : current.clone().endOf('month').week();

    let calendar = [];

    for (let w = startWeek; w <= endWeek; w++) {
      calendar.push(
        <Weekend key={w}>
          {Array(7).fill(0).map((n, idx) => {

            const noFormatDate = current
              .clone()
              .startOf('year')
              .week(w)
              .startOf('week')
              .add(idx, 'day');

            const day = noFormatDate.format('D');
            const fullDate = noFormatDate.format('YYYY-MM-DD');
            const isToday = fullDate === moment().format('YYYYMMDD') ? 'today' : '';
            const isGrayed = noFormatDate.format('MM') === current.format('MM') ? '' : 'grayed';
            const dow = idx; // 요일 정보 추가 (0: 일요일, 6: 토요일)

            const currentSch = schedules.filter((s) => (s.date === fullDate || 
              s.schedule_deadline === fullDate || 
              s.document_result_date === fullDate ||
              s.interview_date === fullDate ||
              s.final_date === fullDate)
            );

            return (
              <Day
                key={`${w}-${idx}`}
                dateInfo={{ day, fullDate, currentSch, dow }} // dow 추가
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
        <Header>
          <YearDisplay onClick={() => setShowYearSelect(!showYearSelect)}>
            {current.format('YYYY')}
            {showYearSelect && (
              <SelectDropdown>
                {yearOptions.map(year => (
                  <SelectOption 
                    key={year}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleYearChange(year);
                    }}
                    selected={year === current.year()}
                  >
                    {year}
                  </SelectOption>
                ))}
              </SelectDropdown>
            )}
          </YearDisplay>
          <HeaderContent>
            <MdChevronLeft className="dir" onClick={movePrevMonth} />
            <MonthDisplay onClick={() => setShowMonthSelect(!showMonthSelect)}>
              {current.format('MMMM')}
              {showMonthSelect && (
                <SelectDropdown>
                  {monthOptions.map(month => (
                    <SelectOption 
                      key={month}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleMonthChange(month);
                      }}
                      selected={month === current.month()}
                      isMonth={true}
                    >
                      {moment().month(month).format('MMMM')}
                    </SelectOption>
                  ))}
                </SelectDropdown>
              )}
            </MonthDisplay>
            <MdChevronRight className="dir" onClick={moveNextMonth} />
          </HeaderContent>
        </Header>
        <DateContainer>
          <Dow>
            <div>S</div>
            <div>M</div>
            <div>T</div>
            <div>W</div>
            <div>T</div>
            <div>F</div>
            <div>S</div>
          </Dow>
          {generate()}
        </DateContainer>
      </CalendarWrapper>
      <ButtonWrapper onClick={() => dispatch(openEditPopup({ isOpen: false }))}>
        <MdEdit className="writeBtn subBtn" />
        <div className="popup-buttons">
          <div 
            className="popup-button"
            onClick={(e) => {
              e.stopPropagation();
              dispatch(openAddSchedule());
            }}
          >
            일정 추가
          </div>
        </div>
        <MdDehaze className="menuBtn" />
      </ButtonWrapper>
    </Body>
  );
};

export default Calendar;