import styled from 'styled-components';

export const Body = styled.div`
  width: 80%;
  position: relative;
  margin: 0 auto;
`;

export const ButtonWrapper = styled.div`
  position: fixed; 
  right: 500px;   
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
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);

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
  position: fixed; 
  right: 350px;   
  bottom: 50px;  
  text-align: center;
  padding-bottom: 3px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: visible;
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
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);

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
  .popup-buttons {
    position: absolute;
    left: calc(100% + 5mm);
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 10px;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }

  .writeBtn:hover ~ .popup-buttons,
  .popup-buttons:hover {
    opacity: 1;
    visibility: visible;
  }

  .popup-button {
    background-color: skyblue;
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
    white-space: nowrap;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    
    &:hover {
      background-color: #7ac7e6;
    }
  }
`;

export const CalendarWrapper = styled.div`
  position: relative;
  width: 100%; 
  margin: 0 auto
`;

export const Header = styled.div`
  height: 7vh;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px;
  font-size: 1.5em;
`;

export const YearDisplay = styled.div`
  color: #666;
  font-size: 0.8em;
  margin-bottom: 5px;
  margin-left: 10px;
`;

export const HeaderContent = styled.div`
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

export const DateContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-top: 1vw;
  padding: 20px;
  width: 100%;
`;

export const Weekend = styled.div`
  display: flex;
  height: 140px;  // 높이를 좀 더 늘림
`;

export const Dow = styled.div`
  border-bottom: 1px solid gray;
  width: 100%;
  height: 35px;
  color: ${(props) => (props.color ? props.color : 'black')};
  text-align: center;
`;

// 날짜 그리드를 감싸는 컨테이너
export const DateGrid = styled.div`
  display: flex;
  flex-direction: column;
`;

export const DayWrapper = styled.div`
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  padding: 8px;
  box-sizing: border-box;

  // today 스타일 유지
  &.today > .title {
    color: white;
    background-color: skyblue;
  }

  // 날짜 숫자 스타일
  .title {
    margin-bottom: 8px;
    font-size: 1em;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    width: 30px;
    height: 30px;
  }

  // 일정 목록 컨테이너
  .schedule-list {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-height: 0;  // flex-grow가 제대로 작동하도록
  }

  // 각 일정 아이템 스타일
  .schedule-item {
    background-color: #ff9aa3;
    padding: 4px 8px;  // 패딩 줄임
    border-radius: 4px;
    font-size: 0.85em;  // 글자 크기 약간 줄임
    height: 24px;  // 높이 줄임 (기존 35px)
    min-height: 24px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-bottom: 2px;
    width: calc(100% - 4px);
  }

  // 더보기 버튼 스타일
  .more-button {
    font-size: 0.8em;
    color: #666;
    cursor: pointer;
    padding: 2px 4px;
    margin-top: auto;  // 하단에 고정
    background-color: #f5f5f5;
    border-radius: 4px;
    width: fit-content;
    align-self: center;  // 중앙 정렬
    
    &:hover {
      background-color: #e0e0e0;
    }
  }
`;

export const ScheduleContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  height: calc(100% - 38px);  // 날짜 높이(30px)와 마진(8px) 제외
  padding: 0 4px;
`;


// 모달 스타일 추가
export const ScheduleModal = styled.div`
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
  max-height: 80vh;
  overflow-y: auto;

  .modal-header {
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

    .close-button {
      cursor: pointer;
      padding: 4px;
      color: #666;
      
      &:hover {
        color: #333;
      }
    }
  }

  .schedule-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .schedule-item {
    background-color: #ffcdd2;
    padding: 12px;
    border-radius: 4px;
    font-size: 0.9em;
  }
`;

// 모달 배경 스타일 추가
export const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  z-index: 999;
`;