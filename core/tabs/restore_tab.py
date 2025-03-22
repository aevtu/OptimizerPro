import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
from datetime import datetime
import logging
from core.utilities import check_logger

class RestoreTab:
    """Вкладка для управления точками восстановления"""
    # Обязательный атрибут для имени вкладки
    TAB_NAME = "🔙 Восстановление"  # <-- Добавьте эту строку
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()  # Важно: вызываем создание виджетов
        self.load_restore_points()

    def _create_widgets(self):
        """Создание элементов интерфейса"""
        # Панель управления
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(pady=10, fill='x')

        # Поле ввода описания
        self.description_entry = ttk.Entry(control_frame, width=40)
        self.description_entry.pack(side='left', padx=5)

        # Кнопка создания точки
        create_btn = ttk.Button(
            control_frame,
            text="Создать точку",
            command=self.create_restore_point
        )
        create_btn.pack(side='left', padx=5)

        # Таблица с точками восстановления
        self.tree = ttk.Treeview(
            self.frame,
            columns=("Дата", "Описание"),
            show="headings"
        )
        self.tree.heading("Дата", text="Дата создания")
        self.tree.heading("Описание", text="Описание")
        self.tree.pack(fill='both', expand=True)

    def load_restore_points(self):
        """Загрузка списка точек восстановления"""
        self.tree.delete(*self.tree.get_children())
        try:
            result = subprocess.run(
                'powershell -Command "Get-ComputerRestorePoint | '
                'Select-Object CreationTime, Description | '
                'ConvertTo-Json -Compress"',
                capture_output=True,
                text=True,
                shell=True,
                encoding='utf-8'
            )

            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                for point in data:
                    creation_time = datetime.strptime(
                        point['CreationTime'].split('.')[0],
                        '%m/%d/%Y %H:%M:%S'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                    self.tree.insert('', 'end', values=(
                        creation_time, 
                        point.get('Description', 'Без описания')
                    ))

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки точек: {str(e)}")

    

    def create_restore_point(self):
        """Создание точки восстановления с обработкой ошибок и логированием"""
        check_logger()  # Проверяем состояние логгера
        try:
            description = self.description_entry.get() or "Создано приложением"
            
            # Логируем нажатие кнопки
            logging.info("Нажата кнопка 'Создать точку восстановления'")
            
            # Запуск PowerShell с обработкой кодировки
            result = subprocess.run(
                [
                    'powershell', 
                    '-Command', 
                    f'Checkpoint-Computer -Description "{description}"'
                ],
                capture_output=True,
                shell=True,
                encoding='utf-8',
                errors='replace'  # Заменяем нечитаемые символы
            )

            # Проверка результата
            if result.returncode == 0:
                logging.info(f"Точка восстановления создана: {description}")
                messagebox.showinfo("Успех", "Точка восстановления создана")
            else:
                # Обработка ошибки PowerShell
                error_msg = result.stderr if result.stderr else result.stdout
                error_msg = error_msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                
                logging.error(f"Ошибка создания точки восстановления: {error_msg}")
                
                if "servicedisabled" in error_msg.lower() or "не удается запустить службу" in error_msg.lower():
                    msg = """Требуется включить службу VSS:
                    1. Нажмите Win+R
                    2. Введите services.msc
                    3. Найдите 'Теневое копирование тома'
                    4. Установите тип запуска 'Вручную'"""
                    messagebox.showerror("Ошибка службы", msg)
                else:
                    messagebox.showerror("Ошибка", f"Ошибка PowerShell:\n{error_msg}")

        except Exception as e:
            # Логируем непредвиденную ошибку
            logging.error(f"Непредвиденная ошибка: {str(e)}")
            messagebox.showerror(
                "Неизвестная ошибка", 
                f"Произошла непредвиденная ошибка:\n{str(e)}"
            )
            
        finally:
            self.load_restore_points()
            self.description_entry.delete(0, 'end')