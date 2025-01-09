import './App.css';
import React from 'react';
import Footer from './component/Footer';
import Main from './page/Main';
import User from './component/User';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';

function App() {

  return (
    <Router>
      <div className="App">
        <header>
         <User />
        </header>
        <main>
          <Routes>
            <Route exact path="/" element={<Main />} />
          </Routes>
        </main>
        <footer>
          <Footer />
        </footer>
      </div>
    </Router>
  );
}

export default App;