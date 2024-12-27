import React from 'react';
import styled from 'styled-components';
import Calendar from './component/calendar1';
import { Route, Switch } from 'react-router-dom';
import { withRouter } from 'react-router';
import EditSchedule from './component/calendar1/EditSchedule';
import { useSelector } from 'react-redux';

const App = ({ history }) => {
  const { isOpenEditPopup } = useSelector((state) => state.schedule);

  return (
    <AppWrapper>
      <Title>CALENDAR</Title>
      <ContentWrapper>
        <Switch>
          <Route exact path="/" component={Calendar} />
          <Route exact path="/edit/:id" component={EditSchedule} />
        </Switch>
        {isOpenEditPopup && <EditSchedule />}
      </ContentWrapper>
    </AppWrapper>
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

export default withRouter(App); 