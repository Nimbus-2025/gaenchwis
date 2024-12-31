import React, { useState } from 'react';
import CalendarApp from '../calendar';
import './MyPage.css';


const MyPage = () => {
  const [searchText, setSearchText] = useState('');

  const handleSearch = () => {
    console.log('검색:', searchText);
  };

  return (
    <div>
      <div className="content">
        <h1>마이페이지</h1>
        <div className="calendar-container">
          <CalendarApp />
        </div>
      </div>
    </div>
  );
};

export default MyPage;