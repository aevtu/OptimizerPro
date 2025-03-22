# core/tabs/about_tab.py
import tkinter as tk
from tkinter import ttk
import webbrowser

class AboutTab:
    """Вкладка 'О программе'."""
    TAB_NAME = "ℹ️ О программе"

    def __init__(self, master):
        """Инициализация вкладки."""
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_content()  # Создание содержимого
        
    def _create_content(self):
        """Создание содержимого вкладки."""
        # Заголовок
        ttk.Label(
            self.frame,
            text="PC Optimizer Pro",
            style='Header.TLabel'
        ).pack(pady=10)

        # Основной текст
        about_text = """
        Версия: 1.0.0
        Разработчик: [Евтухов Андрей Дмитриевич]

        Функционал:
        - Очистка временных файлов
        - Управление автозагрузкой
        - Анализ дискового пространства
        - Управление системными службами
        - Создание точек восстановления
        - Планировщик задач
        """

        text_widget = tk.Text(
            self.frame,
            wrap=tk.WORD,
            height=12,
            font=('Segoe UI', 10)
        )
        text_widget.insert(tk.END, about_text)
        text_widget.configure(state='disabled')
        text_widget.pack(fill='both', expand=True, padx=20)

        # Ссылка на GitHub
        self._create_github_link()
        
    def _create_github_link(self):
        """Создание кликабельной ссылки."""
        link_frame = ttk.Frame(self.frame)
        ttk.Label(
            link_frame,
            text="GitHub репозиторий: "
        ).pack(side='left')

        link = ttk.Label(
            link_frame,
            text="https://github.com/your-repo",
            foreground='blue',
            cursor='hand2'
        )
        link.pack(side='left')
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com"))

        link_frame.pack(pady=10)