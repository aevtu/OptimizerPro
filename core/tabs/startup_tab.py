import tkinter as tk
from tkinter import ttk, messagebox
import winreg

class StartupTab:
    """Вкладка управления автозагрузкой"""
    TAB_NAME = "⚡ Автозагрузка"
    
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self._create_widgets()
        self.load_startup()
        
    def _create_widgets(self):
        """Создание элементов интерфейса"""
        # Список элементов автозагрузки
        self.listbox = tk.Listbox(
            self.frame,
            selectmode=tk.SINGLE
        )
        scrollbar = ttk.Scrollbar(self.frame)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Панель управления
        control_frame = ttk.Frame(self.frame)
        ttk.Button(
            control_frame,
            text="Обновить",
            command=self.load_startup
        ).pack(pady=2)
        
        ttk.Button(
            control_frame,
            text="Удалить",
            command=self.remove_item
        ).pack(pady=2)
        
        # Размещение элементов
        self.listbox.pack(side='left', fill='both', expand=True, padx=5)
        scrollbar.pack(side='left', fill='y')
        control_frame.pack(side='right', padx=5)
        
    def load_startup(self):
        """Загрузка списка автозагрузки"""
        self.listbox.delete(0, tk.END)
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run"
            )
            
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    self.listbox.insert(tk.END, f"{name}: {value}")
                    i += 1
                except OSError:
                    break
                    
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            
    def remove_item(self):
        """Удаление выбранного элемента"""
        selection = self.listbox.curselection()
        if not selection:
            return
            
        item = self.listbox.get(selection[0])
        name = item.split(':')[0].strip()
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_WRITE
            )
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            self.load_startup()
            messagebox.showinfo("Успех", "Элемент удален из автозагрузки")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))