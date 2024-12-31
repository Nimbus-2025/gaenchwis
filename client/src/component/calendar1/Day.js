import React from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { openEditPopup } from './redux/modules/schedule';
import { holidays } from './holidays';

const Day = ({ dateInfo, className }) => {
  const schedule = dateInfo.currentSch;
  const dispatch = useDispatch();
  
  const openPopup = (schedule) => {
    dispatch(openEditPopup({ isOpen: true, schedule }));
  };

  schedule.sort((a, b) => a.time - b.time);
  
  const isHoliday = () => {
    const month = dateInfo.fullDate.substring(4, 6);
    const day = dateInfo.fullDate.substring(6, 8);
    return holidays[month + day] !== undefined;
  };

  const mapToPlan = schedule.map((s, idx) => {
    return (
      <Plan
        key={idx}
        className={`${s.completed ? 'completed' : ''}`}
        data={s}
        onClick={() => {
          openPopup(s);
        }}
      >
        {s.title}
      </Plan>
    );
  });

  return (
    <D className={className} 
    data-dow={dateInfo.dow}
    date-holiday={isHoliday()}>
      <span className="title">{dateInfo.day}</span>
      {mapToPlan}
      {isHoliday() && (
        <HolidayName>{holidays[dateInfo.fullDate.substring(4, 8)]}</HolidayName>
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

  & > .title {
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    width: 30px;
    height: 30px;
  }
`;

const Plan = styled.span`
  text-align: center;
  font-size: 0.8em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin: 1px 0;
  height: 20px;
  width: 100%;
  border-radius: 7px;
  background-color: #ff9aa3;
  color: white;
  cursor: pointer;
  
  &.completed {
    background-color: #bfbfbf;
  }
`;

const HolidayName = styled.span`
  font-size: 0.7em;
  color: #ff4b4b;
  margin-top: -5px;
`;

export default Day;