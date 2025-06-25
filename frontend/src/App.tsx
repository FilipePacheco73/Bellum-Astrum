import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import SpaceBackground from './components/SpaceBackground';
import Home from './pages/Home';
import Users from './pages/Users';
import Ships from './pages/Ships';
import Market from './pages/Market';
import Battle from './pages/Battle';
import Register from './pages/Register';
import './App.css';

function App() {
  return (
    <Router>
      <SpaceBackground>
        <Navbar />
        <div className="max-w-4xl mx-auto mt-8 text-slate-50">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/users" element={<Users />} />
            <Route path="/ships" element={<Ships />} />
            <Route path="/market" element={<Market />} />
            <Route path="/battle" element={<Battle />} />
          </Routes>
        </div>
      </SpaceBackground>
    </Router>
  );
}

export default App;
