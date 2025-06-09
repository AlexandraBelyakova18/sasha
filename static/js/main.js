// Основные функции JavaScript для приложения
document.addEventListener('DOMContentLoaded', function() {
    
    // Автоматическое скрытие flash сообщений через 5 секунд
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 500);
            }
        }, 5000);
    });
    
    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.btn-danger[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Вы уверены?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Валидация форм на клиентской стороне
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Форматирование числовых полей
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            validateNumberInput(this);
        });
    });
    
    // Обработка загрузки изображений
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            previewImage(this);
        });
    });
    
    // Инициализация tooltips (если используется Bootstrap)
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

/**
 * Валидация формы
 */
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            showFieldError(field, 'Это поле обязательно для заполнения');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Специальная валидация для числовых полей
    const numberFields = form.querySelectorAll('input[type="number"]');
    numberFields.forEach(function(field) {
        if (field.value && !validateNumberInput(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Валидация числового поля
 */
function validateNumberInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.getAttribute('min'));
    const max = parseFloat(input.getAttribute('max'));
    let isValid = true;
    
    if (isNaN(value)) {
        showFieldError(input, 'Введите корректное число');
        isValid = false;
    } else if (min !== null && !isNaN(min) && value < min) {
        showFieldError(input, `Значение должно быть не менее ${min}`);
        isValid = false;
    } else if (max !== null && !isNaN(max) && value > max) {
        showFieldError(input, `Значение должно быть не более ${max}`);
        isValid = false;
    } else {
        clearFieldError(input);
    }
    
    return isValid;
}

/**
 * Показать ошибку поля
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Очистить ошибку поля
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorMessage = field.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

/**
 * Предварительный просмотр изображения
 */
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            let preview = input.parentNode.querySelector('.image-preview');
            if (!preview) {
                preview = document.createElement('img');
                preview.className = 'image-preview';
                preview.style.maxWidth = '200px';
                preview.style.maxHeight = '200px';
                preview.style.marginTop = '10px';
                input.parentNode.appendChild(preview);
            }
            preview.src = e.target.result;
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

/**
 * Показать/скрыть элемент с анимацией
 */
function toggleElement(element, show = null) {
    if (show === null) {
        show = element.style.display === 'none';
    }
    
    if (show) {
        element.style.display = 'block';
        element.style.opacity = '0';
        setTimeout(function() {
            element.style.transition = 'opacity 0.3s';
            element.style.opacity = '1';
        }, 10);
    } else {
        element.style.transition = 'opacity 0.3s';
        element.style.opacity = '0';
        setTimeout(function() {
            element.style.display = 'none';
        }, 300);
    }
}

/**
 * Форматирование числа с разделителями тысяч
 */
function formatNumber(num, decimals = 2) {
    return new Intl.NumberFormat('ru-RU', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(num);
}

/**
 * Debounce функция для оптимизации поиска
 */
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

/**
 * Показать загрузку
 */
function showLoading(element) {
    element.classList.add('loading');
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-border-sm';
    spinner.setAttribute('role', 'status');
    element.appendChild(spinner);
}

/**
 * Скрыть загрузку
 */
function hideLoading(element) {
    element.classList.remove('loading');
    const spinner = element.querySelector('.spinner-border');
    if (spinner) {
        spinner.remove();
    }
}
