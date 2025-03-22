import os
import glob
import tkinter as tk
from tkinter import ttk, messagebox
from core.utilities import log_action

class CleanerTab:
    """Вкладка для очистки временных файлов."""
    TAB_NAME = "🛠 Очистка"
    
    TEMP_PATHS = [
        os.environ.get('TEMP'),
        os.environ.get('TMP'),
        'C:/Windows/Temp',
        os.path.expanduser('~/AppData/Local/Temp')
    ]
    
    def __init__(self, master):
        """Инициализация вкладки."""
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()
        
    def _create_widgets(self):
        """Создание элементов интерфейса."""
        # Панель управления
        control_frame = ttk.Frame(self.frame)
        ttk.Button(
            control_frame,
            text="Сканировать",
            command=self.scan_temp_files
        ).pack(side='left', padx=5)
        
        ttk.Button(
            control_frame,
            text="Очистить",
            command=self.clean_temp_files
        ).pack(side='left', padx=5)
        control_frame.pack(pady=10, fill='x')
        
        # Область результатов
        self.result_text = tk.Text(
            self.frame,
            wrap=tk.WORD,
            height=15
        )
        self.result_text.pack(pady=10, padx=10, fill='both', expand=True)
    
    def scan_temp_files(self):
        """Сканирование временных файлов."""
        log_action("Нажата кнопка 'Сканировать'")
        try:
            self.result_text.delete(1.0, tk.END)
            total_size = 0
            file_count = 0
            
            for directory in self.TEMP_PATHS:
                if directory and os.path.exists(directory):
                    for root, _, files in os.walk(directory):
                        for file in files:
                            path = os.path.join(root, file)
                            try:
                                size = os.path.getsize(path)
                                total_size += size
                                file_count += 1
                                self.result_text.insert(tk.END, f"{path} - {size//1024} KB\n")
                            except Exception as e:
                                log_action(f"Ошибка доступа к файлу: {path}", status="ERROR", details=str(e))
            
            self.result_text.insert(tk.END, f"\nФайлов: {file_count}, Размер: {total_size//1024//1024} MB")
            log_action("Сканирование завершено")
        except Exception as e:
            log_action("Ошибка при сканировании", status="ERROR", details=str(e))
            messagebox.showerror("Ошибка", str(e))
        
    def clean_temp_files(self):
        """Очистка временных файлов."""
        log_action("Нажата кнопка 'Очистить'")
        if not messagebox.askyesno("Подтверждение", "Удалить временные файлы?"):
            return
            
        try:
            total_cleaned = 0
            errors = 0
            
            for directory in self.TEMP_PATHS:
                if directory and os.path.exists(directory):
                    for root, _, files in os.walk(directory):
                        for file in files:
                            path = os.path.join(root, file)
                            try:
                                os.remove(path)
                                total_cleaned += 1
                            except Exception as e:
                                errors += 1
                                log_action(f"Файл не удален: {path}", status="NO CLEAR", details=str(e))
            
            messagebox.showinfo("Результат", f"Удалено файлов: {total_cleaned}, Ошибок: {errors}")
            log_action("Очистка завершена", details=f"Удалено: {total_cleaned}, Ошибок: {errors}")
            self.scan_temp_files()
        except Exception as e:
            log_action("Ошибка при очистке", status="ERROR", details=str(e))
            messagebox.showerror("Ошибка", str(e))