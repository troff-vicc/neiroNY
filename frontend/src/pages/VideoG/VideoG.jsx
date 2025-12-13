import React, { useState } from 'react';
import './VideoG.css';

const VideoG = () => {
  const [inputText, setInputText] = useState('');
  const [videoUrl, setVideoUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputText.trim()) {
      setError('Пожалуйста, введите текст для генерации');
      return;
    }

    setIsLoading(true);
    setError(null);
    setVideoUrl(null);
    setCopied(false);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}video/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: inputText,
        }),
      });

      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }

      const data = await response.json();

      if (data.video_url) {
        setVideoUrl(data.video_url);
      } else {
        throw new Error('Не удалось получить URL видео');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла неизвестная ошибка');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyUrl = () => {
    if (videoUrl) {
      navigator.clipboard.writeText(videoUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleClear = () => {
    setInputText('');
    setVideoUrl(null);
    setError(null);
    setCopied(false);
  };

  return (
    <div className="video-generator-container">
      <header className="header">
        <h1 className="title">🎄 Генератор Новогодних Видео Поздравлений</h1>
        <p className="subtitle">Создайте уникальное видео-поздравление с помощью ИИ</p>
      </header>

      <div className="content">
        <div className="input-section">
          <form onSubmit={handleSubmit} className="generator-form">
            <div className="form-group">
              <label htmlFor="prompt" className="form-label">
                Введите текст для генерации поздравления:
              </label>
              <textarea
                id="prompt"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Например: Деде мороз кладёт подарки под ёлку"
                className="text-input"
                rows={5}
                disabled={isLoading}
              />
              <div className="char-count">
                {inputText.length} символов
              </div>
            </div>

            <div className="button-group">
              <button
                type="submit"
                className="generate-button"
                disabled={isLoading || !inputText.trim()}
              >
                {isLoading ? (
                  <>
                    <span className="spinner"></span>
                    Генерируем видео...
                  </>
                ) : (
                  '🎬 Сгенерировать видео'
                )}
              </button>

              <button
                type="button"
                onClick={handleClear}
                className="clear-button"
                disabled={isLoading}
              >
                Очистить
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          {isLoading && (
            <div className="loading-section">
              <div className="loading-spinner"></div>
              <p className="loading-text">
                Создаем ваше новогоднее видео...<br />
                Это может занять несколько минут
              </p>
            </div>
          )}
        </div>

        {videoUrl && !isLoading && (
          <div className="result-section">
            <h2 className="result-title">🎉 Ваше видео готово!</h2>

            <div className="video-container">
              <video
                controls
                className="video-player"
                src={videoUrl}
                poster="/api/placeholder/640/360"
              >
                Ваш браузер не поддерживает воспроизведение видео.
              </video>
            </div>

            <div className="video-actions">
              <a
                href={videoUrl}
                download="new-year-greeting.mp4"
                className="download-button"
              >
                ⬇️ Скачать видео
              </a>

              <button
                onClick={handleCopyUrl}
                className="copy-button"
              >
                {copied ? '✅ Скопировано!' : '📋 Копировать ссылку'}
              </button>
            </div>

            <div className="video-info">
              <p className="share-text">Поделитесь видео с друзьями:</p>
              <div className="share-links">
                {/* Здесь можно добавить кнопки для соцсетей */}
              </div>
            </div>
          </div>
        )}

        {!videoUrl && !isLoading && (
          <div className="instructions">
            <h3>📝 Как это работает:</h3>
            <ol className="instructions-list">
              <li>Напишите текст для генерации</li>
              <li>Нажмите "Сгенерировать видео"</li>
              <li>Дождитесь создания видео (обычно 1-3 минуты)</li>
              <li>Скачайте или поделитесь готовым видео</li>
            </ol>

            <div className="examples">
              <h4>Примеры запросов:</h4>
              <ul className="examples-list">
                <li>"Для коллег: Дед мороз в костюме вручает премию работнику"</li>
                <li>"Для семьи: Всё семья стоит вместе и мама превращаеться в снегурочку"</li>
                <li>"Для друзей: Школа разрывается от подарков"</li>
              </ul>
            </div>
          </div>
        )}
      </div>

      <footer className="footer">
        <p>🎅 Создано с новогодним настроением!</p>
      </footer>
    </div>
  );
};

export default VideoG;