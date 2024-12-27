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