import psutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

class ServicesTab:
    """Вкладка для управления системными службами"""
    TAB_NAME = "🛡 Службы"

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()
        self.update_services()

    def _create_widgets(self):
        """Создание элементов интерфейса"""
        # Заголовок
        ttk.Label(
            self.frame,
            text="Управление системными службами",
            style='Header.TLabel'
        ).pack(pady=10)

        # Таблица для отображения служб
        self.tree = ttk.Treeview(
            self.frame,
            columns=('Служба', 'Состояние', 'Тип запуска'),
            show='headings'
        )

        # Настройка столбцов
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor=tk.CENTER)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Панель управления
        control_frame = ttk.Frame(self.frame)
        ttk.Button(
            control_frame,
            text="Обновить",
            command=self.update_services
        ).pack(side='left', padx=2)

        ttk.Button(
            control_frame,
            text="Остановить",
            command=lambda: self.control_service('stop')
        ).pack(side='left', padx=2)

        ttk.Button(
            control_frame,
            text="Запустить",
            command=lambda: self.control_service('start')
        ).pack(side='left', padx=2)

        # Размещение элементов
        self.tree.pack(side='top', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')
        control_frame.pack(side='bottom', pady=5)

    def update_services(self):
        """Обновление списка служб"""
        self.tree.delete(*self.tree.get_children())
        try:
            for service in psutil.win_service_iter():
                info = service.as_dict()
                self.tree.insert('', 'end', values=(
                    info['name'],
                    info['status'],
                    info['start_type']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def control_service(self, action):
        """Управление службой (запуск/остановка)"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите службу")
            return

        service_name = self.tree.item(selected[0])['values'][0]
        try:
            subprocess.run(['net', action, service_name], check=True)
            self.update_services()
            messagebox.showinfo("Успех", f"Служба {service_name} {action} успешно")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Ошибка", str(e))