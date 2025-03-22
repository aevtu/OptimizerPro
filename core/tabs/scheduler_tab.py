import schedule
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class SchedulerTab:
    """Вкладка для планирования задач"""
    TAB_NAME = "⏰ Планировщик"

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()

    def _create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        ttk.Label(
            self.frame,
            text="Планировщик задач",
            style='Header.TLabel'
        ).pack(pady=10)

        # Таблица для отображения задач
        self.tree = ttk.Treeview(
            self.frame,
            columns=('Время', 'Задача'),
            show='headings'
        )

        # Настройка столбцов
        self.tree.heading('Время', text='Время выполнения')
        self.tree.heading('Задача', text='Описание задачи')

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Панель управления
        control_frame = ttk.Frame(self.frame)
        ttk.Button(
            control_frame,
            text="Добавить задачу",
            command=self.add_task
        ).pack(pady=5)

        ttk.Button(
            control_frame,
            text="Удалить задачу",
            command=self.remove_task
        ).pack(pady=5)

        # Размещение элементов
        self.tree.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')
        control_frame.pack(side='right', padx=10)

    def add_task(self):
        """Добавление новой задачи"""
        time_str = simpledialog.askstring("Время", "Введите время в формате HH:MM")
        description = simpledialog.askstring("Задача", "Введите описание задачи:")
        if time_str and description:
            schedule.every().day.at(time_str).do(
                lambda: messagebox.showinfo("Планировщик", f"Выполнено: {description}")
            ).tag(description)
            self.tree.insert('', 'end', values=(time_str, description))

    def remove_task(self):
        """Удаление выбранной задачи"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления")
            return

        task_description = self.tree.item(selected[0])['values'][1]
        schedule.clear(task_description)
        self.tree.delete(selected[0])
        messagebox.showinfo("Успех", "Задача удалена")

    def _run_scheduler(self):
        """Фоновый процесс для выполнения задач"""
        while True:
            schedule.run_pending()
            time.sleep(1)