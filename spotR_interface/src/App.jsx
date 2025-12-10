import React from 'react'
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import { BrowserRouter as Routes, Route } from 'react-router-dom';
import './App.css'
import { BrowserRouter } from 'react-router';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/dashboard' element={<Dashboard />} />
      </Routes>    
    </BrowserRouter>
  )
  
}

export default App
