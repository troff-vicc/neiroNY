import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home/Home';
import TextG from './pages/TextG/TextG';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import ImgG from './pages/ImgG/ImgG';
import VideoG from './pages/VideoG/VideoG';
import './App.css';

function App() {
  return (
    <div className="app">
      <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/text" element={<TextG />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/img" element={<ImgG />} />
            <Route path="/video" element={<VideoG />} />
          </Routes>
      </Router>
    </div>
  );
}

export default App;