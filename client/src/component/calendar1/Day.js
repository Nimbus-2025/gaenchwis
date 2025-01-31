import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { openEditPopup } from './redux/modules/schedule';
import { holidays } from './holidays';

// 스타일 컴포넌트 정의
const D = styled.div`
  padding-top: 4px;
  height: 16vh;
  display: flex;
  align-items: center;
  width: 100%;
  flex-direction: column;
  flex-wrap: nowrap;
  overflow: hidden;
  position: relative;

  &.grayed {
    color: gray;
    
    .title {
      color: gray !important;
    }
    
    .holiday-name {
      display: none;
    }
  }

  &.today > .title {
    color: white;
    background-color: skyblue;
  }

  & > .title {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin-bottom: 2px;
    
    &.sunday, &.holiday {
      color: #ff4b4b;
    }
    
    &.saturday {
      color: #4b87ff;
    }
  }

  .holiday-name {
    font-size: 0.8em;
    color: #ff4b4b;
    margin-top: 2px;
    text-align: center;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    position: relative;
    line-height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
`;

const Plan = styled.span`
  text-align: center;
  font-size: 0.7em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin: 1px 0;
  height: 15px;
  min-height: 15px;
  width: calc(100% - 8px);
  border-radius: 4px;
  background-color: ${props => {
    // 일반 일정인 경우
    if (props.scheduletype === 'schedule') {
      return '#74c0fc';  // 하늘색
    }
    // 취업 관련 일정인 경우
    return '#ff9aa3';    // 핑크색
  }};
  color: white;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  padding: 2px 4px;
  
  .title {
    font-weight: 500;
  }
  
  .announcement-title {
    font-size: 0.9em;
    opacity: 0.9;
  }
  
  &.completed {
    background-color: #bfbfbf;
  }
`;

const ScheduleContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: calc(100% - 20px);
  padding: 0 4px;
  gap: 1px;
`;

const MoreButton = styled.div`
  font-size: 0.7em;
  color: #666;
  cursor: pointer;
  padding: 1px 4px;
  margin-top: 1px;
  background-color: #f5f5f5;
  border-radius: 4px;
  width: fit-content;
  height: 16px;    // 높이 고정
  line-height: 16px;  // 텍스트 세로 중앙 정렬

  &:hover {
    background-color: #e0e0e0;
  }
`;

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  z-index: 999;
`;

const ScheduleModal = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1000;
  min-width: 300px;
  max-width: 500px;
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;

  h3 {
    margin: 0;
    color: #333;
  }
`;

const CloseButton = styled.div`
  cursor: pointer;
  padding: 4px;
  color: #666;
  
  &:hover {
    color: #333;
  }
`;

const ModalContent = styled.div`
  max-height: 60vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

// Day 컴포넌트
const Day = ({ dateInfo, className }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const schedule = dateInfo.currentSch;
  const dispatch = useDispatch();

  // 요일과 공휴일 확인
  const isHoliday = holidays[dateInfo.fullDate];
  const isSunday = dateInfo.dow === 0;
  const isSaturday = dateInfo.dow === 6;
  
  const titleClassName = `title ${isSunday ? 'sunday' : ''} ${isSaturday ? 'saturday' : ''} ${isHoliday ? 'holiday' : ''}`;

  const openPopup = (schedule) => {
    dispatch(openEditPopup({ isOpen: true, schedule}));
  };

  schedule.sort((a, b) => a.time - b.time);
  
  const renderSchedules = (schedules, limit = null) => {
    const sortedSchedules = [...schedules].sort((a, b) => {
      if (a.type === 'announcement' && b.type !== 'announcement') return -1;
      if (a.type !== 'announcement' && b.type === 'announcement') return 1;
      
      const isAnnouncementRelated = (schedule) => 
        schedule.title?.includes('공고 마감') ||
        schedule.title?.includes('서류 합격 발표') ||
        schedule.title?.includes('면접') ||
        schedule.title?.includes('최종 발표');
      
      if (isAnnouncementRelated(a) && !isAnnouncementRelated(b)) return -1;
      if (!isAnnouncementRelated(a) && isAnnouncementRelated(b)) return 1;
      
      return 0;
    });


    const displaySchedules = limit ? sortedSchedules.slice(0, limit) : sortedSchedules;

    return displaySchedules.map((s, idx) => (
      <Plan
        key={`${s.id || idx}`}
        className={`${s.completed ? 'completed' : ''}`}
        scheduletype={s.type}
        scheduletitle={s.title}
        onClick={e => {
          e.stopPropagation();
          openPopup(s);
        }}
      >
        {s.title}
        {(s.type === 'announcement' || s.title?.includes('공고 마감') || 
          s.title?.includes('서류 합격 발표') || s.title?.includes('면접') || 
          s.title?.includes('최종 발표')) && s.company && (
            <div className="announcement-title">{s.company}</div>
        )}
      </Plan>
    ));
  };


  return (
    <>
      <D className={className}>
        <span className={titleClassName}>{dateInfo.day}</span>
        {isHoliday && <span className="holiday-name">{holidays[dateInfo.fullDate]}</span>}
        <ScheduleContainer>
          {renderSchedules(schedule, 2)}
          {schedule && schedule.length > 0 && (
            <MoreButton 
              onClick={(e) => {
                e.stopPropagation();
                setIsModalOpen(true);
              }}
            >
              {schedule.length > 2 ? `+${schedule.length - 2}` : '더보기'}
            </MoreButton>
          )}
        </ScheduleContainer>
      </D>
  
      {isModalOpen && (
        <>
          <ModalOverlay onClick={() => setIsModalOpen(false)} />
          <ScheduleModal>
            <ModalHeader>
              <h3>{dateInfo.fullDate} 일정</h3>
              <CloseButton onClick={() => setIsModalOpen(false)}>✕</CloseButton>
            </ModalHeader>
            <ModalContent>
              {renderSchedules(schedule)}
            </ModalContent>
          </ScheduleModal>
        </>
      )}
    </>
  );
};

export default Day;