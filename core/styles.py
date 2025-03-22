from tkinter import ttk
from ttkthemes import ThemedStyle

class AppStyles:
    """Класс для управления стилями приложения."""
    def __init__(self):
        """Инициализация стилей."""
        self.style = ThemedStyle()  # Используем ThemedStyle из ttkthemes
        self._configure_light_theme()  # Настраиваем светлую тему
    
    def _configure_light_theme(self):
        """Настройка светлой темы."""
        self.style.set_theme("arc")  # Устанавливаем тему "arc"
        
        # Цветовая палитра
        self.colors = {
            'primary': '#4A90D9',  # Синий цвет для кнопок
            'button_text': '#000000',  # Черный текст на кнопках
            'text': '#000000',  # Черный текст для меток
            'background': '#FFFFFF'  # Белый фон
        }
        
        # Настройка стилей для кнопок
        self.style.configure(
            'TButton',
            background=self.colors['primary'],  # Синий фон
            foreground=self.colors['button_text'],  # Черный текст
            font=('Segoe UI', 10, 'bold'),  # Шрифт
            borderwidth=1,  # Толщина границы
            padding=10  # Отступы внутри кнопки
        )
        
        # Стиль для активной кнопки (при наведении)
        self.style.map(
            'TButton',
            background=[('active', self.colors['primary'])],  # Цвет при наведении
            foreground=[('active', self.colors['button_text'])]  # Цвет текста при наведении
        )
        
        # Настройка стилей для меток
        self.style.configure(
            'TLabel',
            background=self.colors['background'],  # Белый фон
            foreground=self.colors['text'],  # Черный текст
            font=('Segoe UI', 10)  # Шрифт
        )
        
        # Настройка стилей для статусной строки
        self.style.configure(
            'Status.TLabel',
            background=self.colors['background'],  # Белый фон
            foreground=self.colors['text'],  # Черный текст
            font=('Segoe UI', 9)  # Шрифт
        )