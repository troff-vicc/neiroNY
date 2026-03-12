import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';


const Home = () => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate('/img');
  };

  const handleGreetingClick = () => {
    navigate('/text');
  };

  const handleVideoClick = () => {
    navigate('/video');
    
  };




  return (

    <div className="main1">
      {/* Первый экран с фоновым изображением */}
      <div className="hero-section">
         <a href="/login" className='log'>
          <img src="Vector.png" alt="login" className='logimg'/>
        </a>

      <div className="hero-text">
        
    <p className="hero-subtitle">
      Создай незабываемое поздравление к Новому году
    </p>
  </div>
  </div>


      {/* Второй экран с кнопками */}
      <div className="buttons-section">
        <div className="buttons-container">
          <button
            className="action-button red-border-button"
            onClick={handleCardClick}
          >
            <span className="button-text">создать открытку</span>
          </button>

          <button
            className="action-button red-border-button"
            onClick={handleGreetingClick}
          >
            <span className="button-text">придумать поздравление</span>
          </button>

          <button
            className="action-button red-border-button"
            onClick={handleVideoClick}
          >
            <span className="button-text">создать видео</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;