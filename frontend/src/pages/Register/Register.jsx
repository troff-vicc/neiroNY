import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    firstName: ''
  });

  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [validationErrors, setValidationErrors] = useState({});

  const navigate = useNavigate();

  // Проверяем, если пользователь уже вошел
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/'); // Перенаправляем если уже авторизован
    }
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });

    // Очищаем ошибку валидации при изменении поля
    if (validationErrors[name]) {
      setValidationErrors({
        ...validationErrors,
        [name]: ''
      });
    }
  };

  // Валидация формы
  const validateForm = () => {
    const errors = {};

    if (!formData.username.trim()) {
      errors.username = 'Имя пользователя обязательно';
    } else if (formData.username.length < 3) {
      errors.username = 'Минимум 3 символа';
    }

    if (!formData.email.trim()) {
      errors.email = 'Email обязателен';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Некорректный email';
    }

    if (!formData.password) {
      errors.password = 'Пароль обязателен';
    } else if (formData.password.length < 8) {
      errors.password = 'Минимум 8 символов';
    }

    if (!formData.password2) {
      errors.password2 = 'Подтвердите пароль';
    } else if (formData.password !== formData.password2) {
      errors.password2 = 'Пароли не совпадают';
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}users/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          first_name: formData.firstName
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Сохраняем токен и данные пользователя
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));

        // Перенаправляем на главную
        navigate('/');
      } else {
        // Обработка ошибок сервера
        if (data.email) {
          setError(`Email: ${data.email.join(', ')}`);
        } else if (data.username) {
          setError(`Имя пользователя: ${data.username.join(', ')}`);
        } else if (data.password) {
          setError(`Пароль: ${data.password.join(', ')}`);
        } else if (data.non_field_errors) {
          setError(data.non_field_errors.join(', '));
        } else if (data.error) {
          setError(data.error);
        } else {
          setError('Ошибка регистрации. Попробуйте позже.');
        }
      }
    } catch (error) {
      console.error('Register error:', error);
      setError('Ошибка соединения. Проверьте интернет и попробуйте снова.');
    } finally {
      setIsLoading(false);
    }
  };

  // Демо заполнение
  const handleDemoFill = () => {
    const demoUsername = `user_${Math.floor(Math.random() * 10000)}`;
    const demoEmail = `${demoUsername}@example.com`;

    setFormData({
      username: demoUsername,
      email: demoEmail,
      password: 'DemoPass123',
      password2: 'DemoPass123',
      firstName: 'Демо'
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Регистрация</h1>
          <p>Создайте новый аккаунт</p>
        </div>

        {error && (
          <div className="alert alert-error">
            <span className="alert-icon">!</span>
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} className="auth-form">
          <div className="form-group">
            <label htmlFor="username">
              Имя пользователя *
              {validationErrors.username && (
                <span className="error-text"> - {validationErrors.username}</span>
              )}
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="username"
              required
              disabled={isLoading}
              className={`form-input ${validationErrors.username ? 'input-error' : ''}`}
              minLength="3"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">
              Email *
              {validationErrors.email && (
                <span className="error-text"> - {validationErrors.email}</span>
              )}
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your@email.com"
              required
              disabled={isLoading}
              className={`form-input ${validationErrors.email ? 'input-error' : ''}`}
            />
          </div>

          <div className="form-group">
            <label htmlFor="firstName">Имя (необязательно)</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              placeholder="Ваше имя"
              disabled={isLoading}
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              Пароль *
              {validationErrors.password && (
                <span className="error-text"> - {validationErrors.password}</span>
              )}
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Не менее 8 символов"
              required
              disabled={isLoading}
              className={`form-input ${validationErrors.password ? 'input-error' : ''}`}
              minLength="8"
            />
            <div className="password-hint">
              Используйте буквы, цифры и специальные символы
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password2">
              Подтвердите пароль *
              {validationErrors.password2 && (
                <span className="error-text"> - {validationErrors.password2}</span>
              )}
            </label>
            <input
              type="password"
              id="password2"
              name="password2"
              value={formData.password2}
              onChange={handleChange}
              placeholder="Повторите пароль"
              required
              disabled={isLoading}
              className={`form-input ${validationErrors.password2 ? 'input-error' : ''}`}
              minLength="8"
            />
          </div>

          <div className="form-agreement">
            <label className="checkbox">
              <input type="checkbox" required />
              <span>
                Я согласен с <Link to="/terms">условиями использования</Link> и{' '}
                <Link to="/privacy">политикой конфиденциальности</Link>
              </span>
            </label>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="btn btn-primary btn-block"
          >
            {isLoading ? (
              <span className="spinner">Регистрация...</span>
            ) : (
              'Зарегистрироваться'
            )}
          </button>

          <button
            type="button"
            onClick={handleDemoFill}
            className="btn btn-secondary btn-block"
            disabled={isLoading}
          >
            Заполнить демо данные
          </button>
        </form>

        <div className="auth-footer">
          <p>
            Уже есть аккаунт?{' '}
            <Link to="/login" className="auth-link">
              Войти
            </Link>
          </p>
        </div>

        <div className="divider">
          <span>или</span>
        </div>

        <div className="social-register">
          <button className="btn btn-google">
            <svg className="icon" viewBox="0 0 24 24">
              <path fill="currentColor" d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2C7.021,2,2.543,6.477,2.543,12s4.478,10,10.002,10c8.396,0,10.249-7.85,9.426-11.748L12.545,10.239z"/>
            </svg>
            Зарегистрироваться через Google
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;