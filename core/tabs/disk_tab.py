import psutil
import tkinter as tk
from tkinter import ttk
from core.utilities import format_size

class DiskTab:
    """Вкладка для анализа дискового пространства"""
    TAB_NAME = "💾 Диски"

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()
        self.update_disk_info()

    def _create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        ttk.Label(
            self.frame,
            text="Анализ дискового пространства",
            style='Header.TLabel'
        ).pack(pady=10)

        # Таблица для отображения информации о дисках
        self.tree = ttk.Treeview(
            self.frame,
            columns=('Диск', 'Всего', 'Использовано', 'Свободно', 'Использование (%)'),
            show='headings'
        )

        # Настройка столбцов
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Кнопка обновления
        ttk.Button(
            self.frame,
            text="Обновить",
            command=self.update_disk_info
        ).pack(pady=5)

        # Размещение элементов
        self.tree.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')

    def update_disk_info(self):
        """Обновление информации о дисках"""
        self.tree.delete(*self.tree.get_children())
        for partition in psutil.disk_partitions():
            if partition.fstype:
                usage = psutil.disk_usage(partition.mountpoint)
                self.tree.insert('', 'end', values=(
                    partition.device,
                    format_size(usage.total),
                    format_size(usage.used),
                    format_size(usage.free),
                    f"{usage.percent}%"
                ))