import styled from 'styled-components';

export const Body = styled.div`
  width: 50%;
  position: relative;
`;

export const ButtonWrapper = styled.div`
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
`;

export const CalendarWrapper = styled.div`
  position: relative;
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
`;

export const Weekend = styled.div`
  display: flex;
`;

export const Dow = styled.div`
  border-bottom: 1px solid gray;
  width: 100%;
  height: 35px;
  color: ${(props) => (props.color ? props.color : 'black')};
  text-align: center;
`;

export const DayWrapper = styled.div`
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

  .schedule-list {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: 2px;
  }

  .schedule-item {
    background-color: #bbdefb;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 0.8em;
    cursor: pointer;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    &:hover {
      background-color: #90caf9;
    }

    &.completed {
      background-color: #e0e0e0;
      &:hover {
        background-color: #bdbdbd;
      }
    }
  }
`;
