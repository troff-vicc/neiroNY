import React, { useState } from 'react';
import './TextG.css';

const TextG = () => {
  const [inputText, setInputText] = useState('');
  const [generatedText, setGeneratedText] = useState('');
  const [editText, setEditText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [sessionId, setSessionId] = useState(`user_${Date.now()}`);

  // Генерация первоначального поздравления
  const handleGenerate = async () => {
    if (!inputText.trim()) {
      setError('Пожалуйста, введите описание для поздравления');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}text/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputText,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при генерации текста');
      }

      const result = await response.json();

      // Предполагаем, что API возвращает текст в поле 'text' или 'message'
      const text = result.text || result.message || JSON.stringify(result);
      setGeneratedText(text);
      setEditText(text);
    } catch (error) {
      console.error('Error generating text:', error);
      setError('Не удалось сгенерировать текст. Попробуйте еще раз.');
    } finally {
      setIsLoading(false);
    }
  };

  // Регенерация с учетом правок
  const handleRegenerate = async () => {
    if (!editText.trim()) {
      setError('Пожалуйста, введите текст для регенерации');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}text/regenerate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: editText,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при регенерации текста');
      }

      const result = await response.json();

      // Предполагаем, что API возвращает текст в поле 'text' или 'message'
      const text = result.text || result.message || JSON.stringify(result);
      setGeneratedText(text);
      setEditText(text);
    } catch (error) {
      console.error('Error regenerating text:', error);
      setError('Не удалось обновить текст. Попробуйте еще раз.');
    } finally {
      setIsLoading(false);
    }
  };

  // Сброс формы
  const handleReset = () => {
    setInputText('');
    setGeneratedText('');
    setEditText('');
    setError('');
    setSessionId(`user_${Date.now()}`);
  };

  // Копирование текста в буфер обмена
  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(generatedText)
      .then(() => {
        alert('Текст скопирован в буфер обмена!');
      })
      .catch(err => {
        console.error('Ошибка копирования:', err);
      });
  };

  return (
    <div className="text-generator-container">
      <h1>🎄 Генератор Новогодних Поздравлений</h1>
      <p className="subtitle">Создайте уникальное поздравление или идею для видео-поздравления</p>

      {/* Поле для первоначального запроса */}
      <div className="input-section">
        <h2>Опишите ваше поздравление:</h2>
        <textarea
          className="input-textarea"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Пример: Сгенерируй новогоднее поздравление для коллег. Добавь немного юмора и пожеланий карьерного роста."
          rows={4}
          disabled={isLoading}
        />

        <div className="examples">
          <p>Примеры запросов:</p>
          <ul>
            <li onClick={() => setInputText("Сгенерируй новогоднее поздравление для семьи. Сделай его теплым и душевным.")}>
              Для семьи
            </li>
            <li onClick={() => setInputText("Создай веселое новогоднее поздравление для друзей с юмором и мемами.")}>
              Для друзей
            </li>
            <li onClick={() => setInputText("Придумай идею для новогоднего видео-поздравления с неожиданным поворотом.")}>
              Идея для видео
            </li>
          </ul>
        </div>

        <button
          className="generate-btn"
          onClick={handleGenerate}
          disabled={isLoading || !inputText.trim()}
        >
          {isLoading ? 'Генерация...' : 'Сгенерировать поздравление ✨'}
        </button>
      </div>

      {/* Отображение ошибок */}
      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {/* Результат генерации */}
      {generatedText && (
        <div className="result-section">
          <div className="result-header">
            <h2>🎁 Ваше новогоднее поздравление:</h2>
            <button
              className="copy-btn"
              onClick={handleCopyToClipboard}
              title="Копировать в буфер обмена"
            >
              📋
            </button>
          </div>

          <div className="generated-text">
            {generatedText}
          </div>

          {/* Редактирование и регенерация */}
          <div className="edit-section">
            <h3>Хотите что-то изменить?</h3>
            <p className="edit-hint">Отредактируйте текст ниже и нажмите "Перегенерировать"</p>

            <textarea
              className="edit-textarea"
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              placeholder="Внесите правки здесь..."
              rows={6}
              disabled={isLoading}
            />

            <div className="action-buttons">
              <button
                className="regenerate-btn"
                onClick={handleRegenerate}
                disabled={isLoading}
              >
                {isLoading ? 'Перегенерация...' : '🔄 Перегенерировать'}
              </button>

              <button
                className="reset-btn"
                onClick={handleReset}
                disabled={isLoading}
              >
                🗑️ Новый запрос
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Подсказки для видео-идей */}
      {!generatedText && !isLoading && (
        <div className="tips-section">
          <h3>💡 Идеи для новогодних видео-поздравлений:</h3>
          <div className="tips-grid">
            <div className="tip-card">
              <h4>🎬 Семейная история</h4>
              <p>Снимите видео с архивными фото и видео уходящего года</p>
            </div>
            <div className="tip-card">
              <h4>🤣 Юмористическое</h4>
              <p>Пародия на новогоднее обращение с шутками и мемами</p>
            </div>
            <div className="tip-card">
              <h4>✨ Творческое</h4>
              <p>Анимация или рисованное поздравление</p>
            </div>
            <div className="tip-card">
              <h4>🎵 Музыкальное</h4>
              <p>Перепойте известную песню с новогодними словами</p>
            </div>
          </div>
        </div>
      )}

      {/* Индикатор загрузки */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="spinner">🎄</div>
          <p>Дед Мороз пишет поздравление...</p>
        </div>
      )}
    </div>
  );
};

export default TextG;