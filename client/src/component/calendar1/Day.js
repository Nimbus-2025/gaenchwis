import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { openEditPopup } from './redux/modules/schedule';
import { holidays } from './holidays';

const Day = ({ dateInfo, className }) => {
  const dispatch = useDispatch();
  const { isVisible } = useSelector(state => state.schedule);
  const schedule = dateInfo.currentSch || [];
  
  const openPopup = (schedule) => {
    dispatch(openEditPopup({ isOpen: true, schedule }));
  };

  schedule.sort((a, b) => a.time - b.time);
  
  const sortedSchedule = [...schedule].sort((a, b) => 
    parseInt(a.time) - parseInt(b.time)
  );

  const isHoliday = () => {
    const month = dateInfo.fullDate.substring(4, 6);
    const day = dateInfo.fullDate.substring(6, 8);
    return holidays[month + day] !== undefined;
  };

  const mapToPlan = schedule.map((s, idx) => {
    if (!isVisible) return null;
    
    return (
      <Plan
      key={s.id || idx}
      className={`${s.completed ? 'completed' : ''}`}
      onClick={(e) => {
        e.stopPropagation();
        openPopup(s);
        }}
      >
        <PlanTime>{s.time.substring(0, 2)}:{s.time.substring(2)}</PlanTime>
        <PlanTitle>{s.title}</PlanTitle>
      </Plan>
    );
  });

  return (
    <D 
      className={className} 
      data-dow={dateInfo.dow}
      data-holiday={isHoliday()}
    >
      <DayTitle className="title">
        {dateInfo.day}
      </DayTitle>
      <PlansContainer>
        {mapToPlan}
      </PlansContainer>
      {isHoliday() && (
        <HolidayName>
          {holidays[dateInfo.fullDate.substring(4, 8)]}
        </HolidayName>
      )}
    </D>
  );
};


const D = styled.div`
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
  
  // 토요일 (dow: 6)
  &[data-dow= "6"]> .title {
    color: #4b87ff;
  }
  
  // 일요일 (dow: 0)
  &[data-dow= "0"]> .title,
  &[date-holiday="true"] > .title {
    color: #ff4b4b;
  }

  &.today > .title {
    color: white;
    background-color: skyblue;
  }
`;

const DayTitle = styled.span`
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  margin-bottom: 4px;
`;

const PlansContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
  max-height: calc(12vh - 40px);
`;

const Plan = styled.span`
  display: flex;
  align-items: center;
  font-size: 0.8em;
  padding: 2px 4px;
  margin: 0 2px;
  background-color: #ff9aa3;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    transform: scale(1.02);
  }
  
  &.completed {
    background-color: #bfbfbf;
  }
`;

const PlanTime = styled.span`
  font-size: 0.9em;
  margin-right: 4px;
  opacity: 0.8;
`;

const PlanTitle = styled.span`
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;

const HolidayName = styled.span`
  font-size: 0.7em;
  color: #ff4b4b;
  margin-top: 2px;
`;

export default Day;