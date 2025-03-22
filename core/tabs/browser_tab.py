import os
import glob
import tkinter as tk
from tkinter import ttk, messagebox
from core.utilities import format_size

class BrowserTab:
    """Вкладка для очистки кэша браузеров"""
    TAB_NAME = "🌐 Браузеры"
    
    # Пути к кэшу популярных браузеров
    BROWSER_PATHS = {
        'Chrome': [
            os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
            os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Media Cache')
        ],
        'Firefox': [
            os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles/*/cache2'),
            os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles/*/thumbnails')
        ],
        'Edge': [
            os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
            os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Media Cache')
        ]
    }

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()

    def _create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        ttk.Label(
            self.frame,
            text="Очистка кэша браузеров",
            style='Header.TLabel'
        ).pack(pady=10)

        # Кнопки для каждого браузера
        for browser_name in self.BROWSER_PATHS:
            ttk.Button(
                self.frame,
                text=f"Очистить кэш {browser_name}",
                command=lambda name=browser_name: self.clean_browser_cache(name)
            ).pack(pady=5, fill='x', padx=20)

    def clean_browser_cache(self, browser_name):
        """Очистка кэша для конкретного браузера"""
        if not messagebox.askyesno("Подтверждение", f"Очистить кэш {browser_name}?"):
            return

        total_size = 0
        deleted_files = 0

        for path_pattern in self.BROWSER_PATHS[browser_name]:
            for path in glob.glob(path_pattern):
                if os.path.exists(path):
                    for root, _, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                total_size += file_size
                                deleted_files += 1
                            except Exception as e:
                                continue

        messagebox.showinfo(
            "Результат",
            f"Удалено файлов: {deleted_files}\n"
            f"Освобождено места: {format_size(total_size)}"
        )