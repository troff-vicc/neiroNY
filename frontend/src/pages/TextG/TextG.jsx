import React, { useState } from 'react';
import './TextG.css';

const TextG = () => {
  const [inputText, setInputText] = useState('');
  const [generatedText, setGeneratedText] = useState('');
  const [additionalRequest, setAdditionalRequest] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [sessionId, setSessionId] = useState(`user_${Date.now()}`);
  const [requestHistory, setRequestHistory] = useState([]);

  const handleGenerate = async () => {
    if (!inputText.trim()) {
      setError('Пожалуйста, введите описание для поздравления');
      return;
    }

    setIsLoading(true);
    setError('');
    setAdditionalRequest('');

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
        console.log(response)
        throw new Error('Ошибка при генерации текста');
      }

      const result = await response.json();
      const text = result.response;
      setGeneratedText(text);

      setRequestHistory(prev => [...prev, {
        type: 'initial',
        request: inputText,
        response: text,
        timestamp: new Date().toLocaleTimeString()
      }]);
    } catch (error) {
      console.error('Error generating text:', error);
      setError('Не удалось сгенерировать текст. Попробуйте еще раз.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = async () => {
    if (!additionalRequest.trim()) {
      setError('Пожалуйста, введите дополнительный запрос');
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
          message: additionalRequest,
          session_id: sessionId
        }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при регенерации текста');
      }

      const result = await response.json();
      const text = result.response;
      setGeneratedText(text);

      setRequestHistory(prev => [...prev, {
        type: 'regenerate',
        request: additionalRequest,
        response: text,
        timestamp: new Date().toLocaleTimeString()
      }]);

      setAdditionalRequest('');
    } catch (error) {
      console.error('Error regenerating text:', error);
      setError('Не удалось обновить текст. Попробуйте еще раз.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickRequest = (request) => {
    setAdditionalRequest(request);
  };

  const handleReset = () => {
    setInputText('');
    setGeneratedText('');
    setAdditionalRequest('');
    setError('');
    setSessionId(`user_${Date.now()}`);
    setRequestHistory([]);
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(generatedText)
  };

  const showPreviousVersion = (index) => {
    const prevItem = requestHistory[index];
    if (prevItem) {
      setGeneratedText(prevItem.response);
    }
  };

  return (
    <div className="text-generator-container">
      <div className="header-section">
        <a href="/"><h1>🎄 Генератор Новогодних Поздравлений</h1></a>
        <a href="/"><p className="subtitle">Создайте уникальное новогоднее настроение</p></a>
      </div>

      <div className="main-content">
        {/* Левая колонка - ввод */}
        <div className="left-column">
          <div className="input-section">
            <h2>📝 Опишите ваше поздравление:</h2>
            <textarea
              className="input-textarea"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Пример: Новогоднее поздравление для семьи с теплыми пожеланиями..."
              rows={6}
              disabled={isLoading || generatedText}
            />

            <div className="examples">
              <p className="examples-title">Быстрый выбор:</p>
              <div className="example-buttons">
                <button
                  onClick={() => setInputText("Сгенерируй новогоднее поздравление для семьи. Сделай его теплым и душевным.")}
                  disabled={isLoading || generatedText}
                >
                  Для семьи
                </button>
                <button
                  onClick={() => setInputText("Создай веселое новогоднее поздравление для друзей с юмором и мемами.")}
                  disabled={isLoading || generatedText}
                >
                  Для друзей
                </button>
                <button
                  onClick={() => setInputText("Придумай идею для новогоднего видео-поздравления с неожиданным поворотом.")}
                  disabled={isLoading || generatedText}
                >
                  Идея для видео
                </button>
              </div>
            </div>

            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={isLoading || !inputText.trim() || generatedText}
            >
              {isLoading ? 'Генерация...' : '🎄 Сгенерировать'}
            </button>

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
          </div>

          {/* Подсказки для видео-идей */}
          {!generatedText && !isLoading && (
            <div className="tips-section">
              <h3>💡 Идеи для видео-поздравлений:</h3>
              <div className="tips-grid">
                <div className="tip-card">
                  <h4>🎬 Семейная история</h4>
                  <p>Архивные фото и видео уходящего года</p>
                  <button
                    onClick={() => setInputText("Придумай сценарий для семейного видео-поздравления с архивными фотографиями.")}
                    className="tip-use-btn"
                  >
                    Использовать
                  </button>
                </div>
                <div className="tip-card">
                  <h4>🤣 Юмористическое</h4>
                  <p>Пародия на новогоднее обращение</p>
                  <button
                    onClick={() => setInputText("Напиши сценарий юмористического видео-поздравления в виде пародии.")}
                    className="tip-use-btn"
                  >
                    Использовать
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Правая колонка - результат */}
        {generatedText && (
          <div className="right-column">
            <div className="result-section">
              <div className="result-header">
                <h2>🎁 Ваше поздравление:</h2>
                <div className="header-actions">
                  <button
                    className="copy-btn"
                    onClick={handleCopyToClipboard}
                    title="Копировать в буфер обмена"
                  >
                    📋 Копировать
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

              <div className="generated-text">
                {generatedText}
              </div>

              {/* История запросов */}
              {requestHistory.length > 1 && (
                <div className="history-section">
                  <h3>📜 История изменений:</h3>
                  <div className="history-list">
                    {requestHistory.map((item, index) => (
                      <div
                        key={index}
                        className={`history-item ${item.type}`}
                        onClick={() => showPreviousVersion(index)}
                      >
                        <span className="history-type">
                          {item.type === 'initial' ? '🎯 Первоначальный' : '🔄 Перегенерация'}
                        </span>
                        <span className="history-request">{item.request}</span>
                        <span className="history-time">{item.timestamp}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Дополнительный запрос для регенерации */}
              <div className="regenerate-section">
                <h3>Хотите что-то изменить?</h3>

                <textarea
                  className="additional-request-textarea"
                  value={additionalRequest}
                  onChange={(e) => setAdditionalRequest(e.target.value)}
                  placeholder="Например: Сделай более формальным, добавь шуток, укороти текст..."
                  rows={3}
                  disabled={isLoading}
                />

                <div className="quick-requests">
                  <p>Быстрые запросы:</p>
                  <div className="quick-buttons">
                    <button
                      onClick={() => handleQuickRequest("Сделай более формальным")}
                      disabled={isLoading}
                    >
                      🏢 Формальный
                    </button>
                    <button
                      onClick={() => handleQuickRequest("Добавь больше шуток")}
                      disabled={isLoading}
                    >
                      😄 Больше юмора
                    </button>
                    <button
                      onClick={() => handleQuickRequest("Укороти текст")}
                      disabled={isLoading}
                    >
                      ✂️ Сократить
                    </button>
                  </div>
                </div>

                <button
                  className="regenerate-btn"
                  onClick={handleRegenerate}
                  disabled={isLoading || !additionalRequest.trim()}
                >
                  {isLoading ? 'Перегенерация...' : '🔄 Перегенерировать'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

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