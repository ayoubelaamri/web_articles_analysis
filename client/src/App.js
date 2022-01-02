import React from 'react';
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

import './assets/css/App.css';

import Landing from './components/Landing'
import NotFound from './components/NotFound'
import Dash from './components/Dash';

function App() {

  return (
    <div className="App">
      <Router>
          <Routes>

            <Route path='*' element={<NotFound />} />
            <Route path="/" element={<Landing />}/>
            <Route path="/dashboard" element={<Dash />}/>

          </Routes>
      </Router>
    </div>
  );
}

export default App;
