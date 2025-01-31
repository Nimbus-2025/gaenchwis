import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import styled from 'styled-components';
import Calendar from './component/calendar1';
import { Routes, Route } from 'react-router-dom';
import EditSchedule from './component/calendar1/EditSchedule';
import AddSchedule from './component/calendar1/AddSchedule';
import { closeAddSchedule, openAddSchedule } from './component/calendar1/redux/modules/schedule';

const theme = createTheme({
  spacing: 8, // 기본 spacing 설정
  // 기타 테마 설정
});

const App = () => {
  const { isOpenEditPopup, isOpenAddPopup } = useSelector((state) => state.schedule);
  const dispatch = useDispatch();
  const [schedules, setSchedules] = useState([]);

  const handleCloseAdd = () => {
    console.log('닫기 함수 호출');
    dispatch(closeAddSchedule());
  };

  const handleOpenAdd = () => {
    dispatch(openAddSchedule());
  };

  return (
    <ThemeProvider theme={theme}>
      <AppWrapper>
        <Title>CALENDAR</Title>
        <ContentWrapper>
          <Routes>
            <Route path="/" element={<Calendar schedules={schedules} setSchedules={setSchedules}/>} />
            <Route path="/edit/:id" element={<EditSchedule setSchedules={setSchedules}/>} />
          </Routes>
          {isOpenEditPopup && <EditSchedule setSchedules={setSchedules}/>}
          {isOpenAddPopup && <AddSchedule onClose={handleCloseAdd} 
            type="schedule"
            setSchedules={setSchedules}
          />}
        </ContentWrapper>
      </AppWrapper>
    </ThemeProvider>
  );
};

const AppWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f5f5f5;
`;

const ContentWrapper = styled.div`
  flex: 1;
  display: flex;
  justify-content: center;
  position: relative;
`;

const Title = styled.div`
  color: gray;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 5vh;
  font-size: 1.5em;
  font-weight: bold;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

export default App; 