import './App.css';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './page/Main'
import Login from './page/Login'
import SaveEssay from './page/SaveEssay'
import LoadEssay from './page/LoadEssay'
import DetectEssay from './page/DetectEssay'
import LoadEssayList from './page/LoadEssayList';
import NotSupport from './page/NotSupport';
import Logo from './component/Logo'

function App() {
  return (
    <Router>
      <div className="App">
        <header>
          <Logo />
        </header>
        <main>
          <Routes>
            <Route exact path="/" element={<Main />} />
            <Route path="/login" element={<Login />} />
            <Route path="/saveessay" element={<SaveEssay />} />
            <Route path="/loadessay" element={<LoadEssayList />} />
            <Route path="/loadessay/:id" element={<LoadEssay />} />
            <Route path="/detectessay" element={<DetectEssay />} />
            <Route path="/notsupport" element={<NotSupport />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;