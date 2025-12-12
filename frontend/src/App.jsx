import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home/Home';
import TextG from './pages/TextG/TextG';
import './App.css';

function App() {
  return (
    <div className="app">
      <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/text" element={<TextG />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;