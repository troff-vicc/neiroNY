import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = ({ onLogout }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (!localStorage.getItem('token')) {
      setError("Не вошли в аккаунт")
      return;
    }
    if (!window.confirm('Вы уверены, что хотите выйти?')) {
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');

      const response = await fetch(`${import.meta.env.VITE_API_URL}users/logout/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Token ${token}` : '',
        },
      });

      const data = await response.json();

      if (response.ok) {
        // Очищаем localStorage
        localStorage.removeItem('token');
        localStorage.removeItem('user');

        // Вызываем callback если передан
        if (onLogout) {
          onLogout();
        }

        // Перенаправляем на страницу входа
        navigate('/login');
      } else {
        setError(data.error || 'Ошибка при выходе');
      }
    } catch (error) {
      console.error('Logout error:', error);
      setError('Ошибка соединения');

      // Даже при ошибке очищаем локальное хранилище
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate('/login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {error && (
        <div className="logout-error">
          {error}
        </div>
      )}

      <button
        onClick={handleLogout}
        disabled={isLoading}
        className="logout-btn"
      >
        {isLoading ? (
          <span className="logout-spinner"></span>
        ) : (
          <>
            <svg className="logout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Выйти
          </>
        )}
      </button>
    </>
  );
};

export default Home;