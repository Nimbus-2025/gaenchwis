import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { store } from './component/calendar1/redux/configStore';
import { GoogleOAuthProvider } from '@react-oauth/google';
import FirstPage from './firstpage'
import MyPage from './pages/MyPage';
import UserPage from './pages/UserPage';
import MyPage1 from './pages/MyPage1';
import Callback from './login-service/Callback';
import LoginfromChromeExtension from "./login-service/LoginfromChromeExtension"

LoginfromChromeExtension();

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId="800144464912-bjdvo0b4vru9sp0i1segrktsgbk9kngu.apps.googleusercontent.com">
      <Provider store={store}>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<FirstPage />} />
        <Route path="/mypage" element={<MyPage />} />
        <Route path="/mypage1" element={<MyPage1 />} />
        <Route path="/userpage" element={<UserPage />} />
        <Route path="/callback" element={<Callback />} />
      </Routes>
      </BrowserRouter>
      </Provider>
    </GoogleOAuthProvider>
  </React.StrictMode>
);