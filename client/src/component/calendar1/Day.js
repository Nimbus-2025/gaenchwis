import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { openEditPopup } from './redux/modules/schedule';

// 스타일 컴포넌트 정의
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

const ScheduleContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: calc(100% - 30px);
  gap: 2px; // 일정 사이 간격 추가
`;

const MoreButton = styled.div`
  font-size: 0.8em;
  color: #666;
  cursor: pointer;
  padding: 2px 4px;
  margin-top: 2px;
  background-color: #f5f5f5;
  border-radius: 4px;
  width: fit-content;
  
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
  const maxVisibleSchedules = 3;

  const openPopup = (schedule) => {
    dispatch(openEditPopup({ isOpen: true, schedule }));
  };

  schedule.sort((a, b) => a.time - b.time);
  
  const renderSchedules = (schedules, limit = null) => {
    const items = limit ? schedules.slice(0, limit) : schedules;
    return items.map((s, idx) => (
      <Plan
        key={`${s.id || idx}`}
        className={`${s.completed ? 'completed' : ''}`}
        data={s}
        onClick={e => {
          e.stopPropagation();
          openPopup(s);
        }}
      >
        {s.title}
      </Plan>
    ));
  };

  return (
    <>
      <D className={className}>
        <span className="title">{dateInfo.day}</span>
        <ScheduleContainer>
          {renderSchedules(schedule, 1)}
          {schedule.length > 0 && 
            <MoreButton 
              onClick={e => {
                e.stopPropagation();
                setIsModalOpen(true);
              }}
            >
              + 더보기
            </MoreButton>
          }
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