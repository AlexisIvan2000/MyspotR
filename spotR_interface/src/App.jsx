import React from 'react'
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import { BrowserRouter,Routes, Route } from 'react-router-dom';
import './App.css'


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home/>} />
        <Route path='/dashboard' element={<Dashboard/>} />       
      </Routes>    
    </BrowserRouter>
  )
  
}

export default App
