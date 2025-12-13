// App.jsx - Обновленная версия с получением base64
import React, { useState } from 'react';
import './ImgG.css';

function ImgG() {
  const [selectedTemplate, setSelectedTemplate] = useState('santa');
  const [textRequest, setTextRequest] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');
  const [processedImage, setProcessedImage] = useState(null); // Для полученного изображения

  const templates = [
    { id: 'santa', name: 'Лицо Деда Мороза', description: 'Новогодний шаблон с Дедом Морозом' },
    { id: 'tree', name: 'Модная Ёлка', description: 'Современный дизайн новогодней ёлки' }
  ];

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Проверяем размер файла (например, максимум 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('Файл слишком большой. Максимальный размер: 5MB');
      return;
    }

    setSelectedImage(file);
    
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
    
    // Очищаем предыдущий результат
    setProcessedImage(null);
    setResponseMessage('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedImage) {
      alert('Пожалуйста, загрузите изображение');
      return;
    }

    setIsLoading(true);
    setResponseMessage('');
    setProcessedImage(null); // Сбрасываем предыдущий результат

    const formData = new FormData();
    formData.append('template_type', selectedTemplate);
    formData.append('text', textRequest);
    formData.append('image_data', selectedImage);
    formData.append('image_format', selectedImage.name); // Можно добавить имя файла

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}img/generate/`, {
        method: 'POST',
        body: formData,
        // Для некоторых API может потребоваться авторизация
        // headers: {
        //   'Authorization': 'Bearer ваш_токен'
        // }
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Ошибка сервера: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      
      // Предполагаем, что сервер возвращает JSON с полем imageBase64
      if (result.success && result.imageBase64) {
        setProcessedImage(result.imageBase64);
        setResponseMessage(`✅ Успешно обработано! ${result.message || ''}`);
      } else {
        throw new Error(result.message || 'Сервер вернул некорректный ответ');
      }
      
    } catch (error) {
      console.error('Ошибка при отправке:', error);
      setResponseMessage(`❌ Ошибка: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // Функция для скачивания обработанного изображения
  const downloadProcessedImage = () => {
    if (!processedImage) return;
    
    const link = document.createElement('a');
    link.href = processedImage;
    link.download = `обработанное-${selectedTemplate}-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Новогодний Редактор</h1>
        <p>Отправляем файл → Получаем обработанное изображение в base64</p>
      </header>

      <main className="main-content">
        <div className="two-column-layout">
          {/* Левая колонка - форма */}
          <div className="left-column">
            <form className="upload-form" onSubmit={handleSubmit}>
              <div className="form-section">
                <h2>1. Выберите шаблон</h2>
                <div className="template-grid">
                  {templates.map(template => (
                    <div 
                      key={template.id}
                      className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
                      onClick={() => setSelectedTemplate(template.id)}
                    >
                      <div className="template-preview">
                        {template.id === 'santa' ? '🎅' : '🎄'}
                      </div>
                      <h3>{template.name}</h3>
                      <p>{template.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="form-section">
                <h2>2. Текстовый запрос</h2>
                <textarea
                  className="text-input"
                  placeholder="Например: 'Добавь снег', 'Сделай новогоднее настроение'..."
                  value={textRequest}
                  onChange={(e) => setTextRequest(e.target.value)}
                  rows={3}
                />
              </div>

              <div className="form-section">
                <h2>3. Загрузите изображение</h2>
                <p className="file-info">
                  Максимальный размер: 5MB. Отправляется как файл.
                </p>
                <div className="image-upload-area">
                  {previewUrl ? (
                    <div className="image-preview">
                      <img src={previewUrl} alt="Ваше изображение" />
                      <div className="image-actions">
                        <button 
                          type="button"
                          className="btn remove-btn"
                          onClick={() => {
                            setSelectedImage(null);
                            setPreviewUrl('');
                          }}
                        >
                          Удалить
                        </button>
                        <span className="file-size">
                          {(selectedImage?.size / 1024 / 1024).toFixed(2)} MB
                        </span>
                      </div>
                    </div>
                  ) : (
                    <label className="upload-label">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="file-input"
                      />
                      <div className="upload-placeholder">
                        <span className="upload-icon">📁</span>
                        <p>Нажмите для выбора файла</p>
                        <p className="upload-hint">Будет отправлен как файл (multipart/form-data)</p>
                      </div>
                    </label>
                  )}
                </div>
              </div>

              <div className="form-section">
                <button 
                  type="submit" 
                  className="submit-btn"
                  disabled={isLoading || !selectedImage}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner"></span>
                      Обработка...
                    </>
                  ) : 'Обработать изображение'}
                </button>
              </div>
            </form>
          </div>

          {/* Правая колонка - результат */}
          <div className="right-column">
            <div className="result-section">
              <h2>Результат обработки</h2>
              
              {responseMessage && (
                <div className={`response-message ${responseMessage.includes('❌') ? 'error' : 'success'}`}>
                  {responseMessage}
                </div>
              )}

              {processedImage ? (
                <div className="result-container">
                  <div className="result-preview">
                    <img 
                      src={processedImage} 
                      alt="Обработанное изображение" 
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlZWVlZWUiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE0IiBmaWxsPSIjOTk5Ij5FcnJvciBsb2FkaW5nIGltYWdlPC90ZXh0Pjwvc3ZnPg==';
                      }}
                    />
                  </div>
                  <div className="result-info">
                    <p><strong>Шаблон:</strong> {templates.find(t => t.id === selectedTemplate)?.name}</p>
                    <p><strong>Запрос:</strong> {textRequest || 'не указан'}</p>
                    <p><strong>Получен в формате:</strong> Base64 ({Math.round(processedImage.length * 0.75 / 1024)} KB)</p>
                  </div>
                  <button 
                    className="btn download-btn"
                    onClick={downloadProcessedImage}
                  >
                    ⬇️ Скачать результат
                  </button>
                </div>
              ) : (
                <div className="empty-result">
                  <div className="empty-icon">🖼️</div>
                  <p>Здесь появится обработанное изображение</p>
                  <p className="empty-hint">
                    Сервер вернет результат в формате Base64
                  </p>
                </div>
              )}

              <div className="technical-info">
                <h3>Техническая информация:</h3>
                <ul>
                  <li>📤 <strong>Отправка:</strong> Файл (multipart/form-data)</li>
                  <li>📥 <strong>Получение:</strong> Base64 строка (application/json)</li>
                  <li>⚡ <strong>Преимущество:</strong> Меньший размер передаваемых данных от сервера</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>Новогодний редактор © 2025 | Отправка: файл → Получение: base64</p>
      </footer>
    </div>
  );
}

export default ImgG;