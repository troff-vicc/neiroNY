// App.jsx - Отправка через base64
import React, { useState } from 'react';
import './ImgG.css';

function ImgG() {
  const [selectedTemplate, setSelectedTemplate] = useState('Father_Frost_Face');
  const [textRequest, setTextRequest] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [responseMessage, setResponseMessage] = useState('');
  const [processedImage, setProcessedImage] = useState(null);

  const templates = [
    { id: 'Father_Frost_Face', name: 'Дед Мороз' },
    { id: 'tree', name: 'Ёлка' },
    { id: 'new_t', name: 'Свой' }
  ];

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

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
    setProcessedImage(null);

    // Конвертируем файл в base64
    const reader = new FileReader();
    reader.readAsDataURL(selectedImage);
    
    reader.onload = async () => {
      const base64Data = reader.result.split(',')[1]; // Убираем префикс "data:image/..."
      const imageFormat = selectedImage.type.split('/')[1]; // Получаем формат (jpeg, png, etc)
      
      const requestData = {
        template_type: selectedTemplate,
        text: textRequest,
        image_data: base64Data,
        image_format: imageFormat
      };

      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}img/generate/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Ошибка сервера: ${response.status} - ${errorText}`);
        }

        const result = await response.json();
        console.log(result);
        if (result.success && result.generated_image) {
          // Добавляем префикс для отображения
          setProcessedImage(`data:image/${result.image_format || 'png'};base64,${result.generated_image}`);
          setResponseMessage('✅ Изображение успешно обработано!');
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

    reader.onerror = () => {
      setResponseMessage('❌ Ошибка чтения файла');
      setIsLoading(false);
    };
  };

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
      <header>
        <a href="/"><h1>Новогодний Редактор</h1></a>
      </header>

      <main>
        <div className="layout">
          {/* Левая колонка - форма */}
          <div className="form-column">
            <form onSubmit={handleSubmit}>
              <div className="section">
                <h2>Шаблон</h2>
                <div className="template-list">
                  {templates.map(template => (
                    <div 
                      key={template.id}
                      className={`template-item ${selectedTemplate === template.id ? 'selected' : ''}`}
                      onClick={() => setSelectedTemplate(template.id)}
                    >
                      <span>{template.id === 'Father_Frost_Face' ? '🎅' : '🎄'}</span>
                      <span>{template.name}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="section">
                <h2>Текстовый запрос</h2>
                <textarea
                  placeholder="Описание изменений..."
                  value={textRequest}
                  onChange={(e) => setTextRequest(e.target.value)}
                  rows={2}
                />
              </div>

              <div className="section">
                <h2>Изображение</h2>
                {previewUrl ? (
                  <div className="preview">
                    <img src={previewUrl} alt="Загруженное" />
                    <button 
                      type="button"
                      className="remove-btn"
                      onClick={() => {
                        setSelectedImage(null);
                        setPreviewUrl('');
                      }}
                    >
                      Удалить
                    </button>
                  </div>
                ) : (
                  <label className="upload-btn">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                    />
                    Выбрать файл
                  </label>
                )}
              </div>

              <button 
                type="submit" 
                className="submit-btn"
                disabled={isLoading || !selectedImage}
              >
                {isLoading ? 'Отправка...' : 'Отправить'}
              </button>
            </form>
          </div>

          {/* Правая колонка - результат */}
          <div className="result-column">
            <h2>Результат</h2>
            
            {responseMessage && (
              <div className={`message ${responseMessage.includes('❌') ? 'error' : 'success'}`}>
                {responseMessage}
              </div>
            )}

            {processedImage ? (
              <div className="result">
                <div className="image-container">
                  <img src={processedImage} alt="Результат" />
                </div>
                <button 
                  className="download-btn"
                  onClick={downloadProcessedImage}
                >
                  Скачать
                </button>
                <button
                  className="repost-btn"
                  onClick={downloadProcessedImage}
                >
                  Поделиться
                </button>
              </div>
            ) : (
              <div className="placeholder">
                <p>Здесь будет результат</p>
              </div>
            )}


          </div>
        </div>
      </main>
    </div>
  );
}

export default ImgG;