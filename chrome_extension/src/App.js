import './App.css';
import React from 'react';
import Footer from './component/Footer';
import Main from './page/Main';
import User from './component/User';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';

function App() {

  return (
    <div className="App">
      <header className="App-header">
       <User />
      </header>
      <main className="App-body">
        <Router>
          <Routes>
            <Route exact path="/" element={<Main />} />
          </Routes>
        </Router>
      </main>
      <footer className="App-footer">
        <Footer />
      </footer>
    </div>
  );
}

export default App;