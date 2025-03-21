import os
import sys
import json
import locale
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psutil
import winreg
import logging
import subprocess
import glob
import threading
import time
import schedule
import requests
import webbrowser
import ctypes
from ttkthemes import ThemedTk
from datetime import datetime

# Определение системной кодировки
system_encoding = locale.getpreferredencoding()

# Проверка прав администратора
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", f'"{sys.executable}"', params, None, 1
    )
    sys.exit()

# Настройка логирования
logging.basicConfig(
    filename='optimizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class ModernOptimizerApp:
    def __init__(self, master):
        self.master = master
        master.title("PC Optimizer Pro")
        master.geometry("1200x800")
        
        self.running = True
        self.style = ttk.Style()
        self.style.theme_use('equilux')
        self.configure_styles()
        
        self.create_notebook()
        self.create_progress_bar()
        self.create_status_bar()
        self.create_resource_monitor()
        
        self.init_about_tab()  # Перемещено после создания notebook
        self.init_cleaner_tab()
        self.init_startup_tab()
        self.init_browser_cache_tab()
        self.init_disk_analysis_tab()
        self.init_services_tab()
        self.init_restore_tab()
        self.init_scheduler_tab()

        self.update_disk_analysis()
        self.update_services()
        self.start_resource_monitor()
        self.check_updates()

        # Запуск планировщика задач в фоне
        self.start_scheduler()

    def configure_styles(self):
        self.style.configure('TNotebook.Tab', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=[10, 5])
        self.style.configure('Red.TButton', 
                       foreground='white',
                       background='#d9534f')
        self.style.map('Red.TButton',
                  background=[('active', '#c9302c')])
        self.style.configure('Green.TButton',
                        foreground='white',
                        background='#5cb85c')
        self.style.configure('Treeview', 
                       font=('Segoe UI', 9),
                       rowheight=25)
        self.style.configure('Treeview.Heading', 
                       font=('Segoe UI', 10, 'bold'))
        self.style.configure('Status.TLabel',
                       font=('Segoe UI', 9),
                       background='#333333',
                       foreground='white')
        # Новые стили для вкладки "О программе"
        self.style.configure('About.Title.TLabel', 
                       font=('Segoe UI', 14, 'bold'),
                       foreground='white')
        self.style.configure('About.Text.TLabel', 
                       font=('Segoe UI', 11),
                       foreground='#cccccc')
        

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.master)
        self.tab_about = ttk.Frame(self.notebook)  # Создаем вкладку первым
        self.tab_cleaner = ttk.Frame(self.notebook)
        self.tab_startup = ttk.Frame(self.notebook)
        self.tab_browser = ttk.Frame(self.notebook)
        self.tab_disk = ttk.Frame(self.notebook)
        self.tab_services = ttk.Frame(self.notebook)
        self.tab_restore = ttk.Frame(self.notebook)
        self.tab_scheduler = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_cleaner, text='🛠 Очистка')
        self.notebook.add(self.tab_startup, text='⚡ Автозагрузка')
        self.notebook.add(self.tab_browser, text='🌐 Браузеры')
        self.notebook.add(self.tab_disk, text='💾 Диски')
        self.notebook.add(self.tab_services, text='🛡 Службы')
        self.notebook.add(self.tab_restore, text='🔙 Восстановление')
        self.notebook.add(self.tab_scheduler, text='⏰ Планировщик')
        self.notebook.add(self.tab_about, text='ℹ️ О программе')
        
        self.notebook.pack(expand=1, fill='both', padx=10, pady=10)

    def create_progress_bar(self):
        self.progress = ttk.Progressbar(self.master, orient='horizontal', mode='determinate')
        self.progress.pack(fill='x', padx=10, pady=5)

    def create_status_bar(self):
        self.status = ttk.Label(self.master, text='Готово', style='Status.TLabel')
        self.status.pack(side='bottom', fill='x')

    def create_resource_monitor(self):
        self.resource_frame = ttk.Frame(self.master)
        self.resource_labels = {
            'cpu': ttk.Label(self.resource_frame, text="CPU: 0%"),
            'ram': ttk.Label(self.resource_frame, text="RAM: 0%"),
            'disk': ttk.Label(self.resource_frame, text="Disk: 0%")
        }
        for label in self.resource_labels.values():
            label.pack(side='left', padx=10)
        self.resource_frame.pack(side='top', fill='x')


    def init_about_tab(self):
        frame = ttk.Frame(self.tab_about)
        frame.pack(fill='both', expand=True, padx=20, pady=20)

        title_label = ttk.Label(
            frame, 
            text="PC Optimizer Pro", 
            style='About.Title.TLabel'
        )
        title_label.pack(pady=10)

        about_text = """
        Версия: 1.0.0
        Разработчик: [Евтухов Андрей Дмитриевич]

        Функционал приложения:
        ✅ Очистка временных файлов системы и браузеров
        ✅ Управление автозагрузкой приложений
        ✅ Анализ использования дискового пространства
        ✅ Управление системными службами
        ✅ Создание точек восстановления
        ✅ Планировщик задач

        Контакты:
        ✉️ Email: andreyevtukhov89@gmail.com
        🌐 GitHub: https://github.com/aedevops
        """

        text_widget = tk.Text(
            frame, 
            wrap=tk.WORD, 
            bg='#333333', 
            fg='white',
            font=('Segoe UI', 10),
            padx=10, 
            pady=10,
            height=15
        )
        text_widget.insert(tk.END, about_text)
        text_widget.configure(state='disabled')
        text_widget.pack(fill='both', expand=True)

        github_link = ttk.Label(
            frame, 
            text="Посетить GitHub репозиторий", 
            cursor="hand2",
            style='About.Text.TLabel'
        )
        github_link.pack(pady=5)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/aedevops"))


    # Вкладка очистки диска
    def init_cleaner_tab(self):
        frame = ttk.LabelFrame(self.tab_cleaner, text="Очистка временных файлов")
        frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        ttk.Button(frame, text="Сканировать", command=self.scan_temp_files).pack(side='left', padx=5)
        ttk.Button(frame, text="Очистить", style='Red.TButton', command=self.clean_temp_files).pack(side='left', padx=5)
        
        self.result_text = tk.Text(self.tab_cleaner, height=15, wrap=tk.WORD)
        self.result_text.pack(pady=10, padx=10, fill='both', expand=True)

    def scan_temp_files(self):
        """Сканирование временных файлов с очисткой кэша перед подсчетом"""
        try:
            self.update_status("Сканирование...")
            temp_dirs = [
                os.environ.get("TEMP"),
                os.environ.get("TMP"),
                "C:/Windows/Temp",
                os.path.expanduser('~/AppData/Local/Temp')
            ]
        
            total_size = 0
            file_count = 0
            self.result_text.delete(1.0, tk.END)
        
            # Удален блок кэширования, прямое сканирование
            for directory in temp_dirs:
                if directory and os.path.exists(directory):
                    for root, _, files in os.walk(directory):
                        for file in files:
                            path = os.path.join(root, file)
                            try:
                                if os.path.exists(path):
                                    size = os.path.getsize(path)
                                    total_size += size
                                    file_count += 1
                                    self.result_text.insert(tk.END, f"{path} - {size//1024} KB\n")
                            except Exception as e:
                                logging.warning(f"Ошибка доступа: {str(e)}")
        
            self.result_text.insert(tk.END, f"\nФайлов: {file_count}, Размер: {total_size//1024//1024} MB")
            self.update_status("Сканирование завершено")
        
        except Exception as e:
            self.handle_error(e)
        finally:
            self.progress['value'] = 0

    def clean_temp_files(self):
        """Удаление временных файлов с улучшенной обработкой ошибок"""
        if not messagebox.askyesno("Подтверждение", "Удалить временные файлы?"):
            return
            
        try:
            self.update_status("Очистка...")
            temp_dirs = [
                os.environ.get("TEMP"),
                os.environ.get("TMP"),
                "C:/Windows/Temp",
                os.path.expanduser('~/AppData/Local/Temp')
            ]
            
            total_cleaned = 0
            file_list = []
            
            for directory in temp_dirs:
                if directory and os.path.exists(directory):
                    for root, _, files in os.walk(directory):
                        for file in files:
                            path = os.path.join(root, file)
                            if os.path.exists(path):
                                file_list.append(path)
            
            total_files = len(file_list)
            for i, path in enumerate(file_list):
                try:
                    # Повторные попытки удаления с закрытием файловых дескрипторов
                    for attempt in range(3):
                        try:
                            os.remove(path)
                            total_cleaned += 1
                            break
                        except PermissionError:
                            # Закрыть файловые дескрипторы
                            for proc in psutil.process_iter():
                                try:
                                    files = proc.open_files()
                                    for f in files:
                                        if f.path == path:
                                            proc.kill()
                                except psutil.AccessDenied:
                                    continue
                            time.sleep(0.5)
                        except Exception as e:
                            if attempt == 2:
                                raise
                            time.sleep(0.5)
                    self.update_progress((i+1)/total_files*100)
                except Exception as e:
                    logging.warning(f"Ошибка удаления {path}: {str(e)}")
            
            messagebox.showinfo("Успех", f"Удалено файлов: {total_cleaned}")
            self.scan_temp_files()
            
        except Exception as e:
            self.handle_error(e)
        finally:
            self.progress['value'] = 0

    # === Вкладка автозагрузки ===
    def init_startup_tab(self):
        """Инициализация вкладки управления автозагрузкой"""
        frame = ttk.Frame(self.tab_startup)  # Исправлено на self.tab_startup
        frame.pack(fill='both', expand=True)
        
        self.startup_list = tk.Listbox(frame, selectmode=tk.SINGLE)
        self.startup_list.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(frame)
        ttk.Button(btn_frame, text="Обновить", command=self.load_startup).pack(pady=2, fill='x')
        ttk.Button(btn_frame, text="Удалить", style='Red.TButton', command=self.remove_startup).pack(pady=2, fill='x')
        btn_frame.pack(side='right', padx=5)
        
        self.load_startup()

    def load_startup(self):
        """Загрузка списка программ в автозагрузке"""
        try:
            self.startup_list.delete(0, tk.END)
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run")
            
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    self.startup_list.insert(tk.END, f"{name}: {value}")
                    i += 1
                except OSError:
                    break
                    
        except Exception as e:
            self.handle_error(e)

    def remove_startup(self):
        """Удаление выбранного элемента из автозагрузки"""
        selection = self.startup_list.curselection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите элемент для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Удалить выбранный элемент из автозагрузки?"):
            selected = self.startup_list.get(selection[0])
            name = selected.split(":")[0].strip()
            
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0, winreg.KEY_WRITE)
                
                winreg.DeleteValue(key, name)
                winreg.CloseKey(key)
                self.load_startup()
                messagebox.showinfo("Успех", "Элемент удален из автозагрузки")
                
            except Exception as e:
                self.handle_error(e)

    # === Вкладка очистки кэша браузеров ===
    def init_browser_cache_tab(self):
        """Инициализация вкладки очистки кэша браузеров"""
        frame = ttk.LabelFrame(self.tab_browser, text="Выберите браузеры для очистки")  # Исправлено
        frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        browsers = [
            ('Google Chrome', self.clean_chrome_cache),
            ('Mozilla Firefox', self.clean_firefox_cache),
            ('Microsoft Edge', self.clean_edge_cache),
            ('Opera', self.clean_opera_cache)
        ]
        
        for name, cmd in browsers:
            btn = ttk.Button(frame, text=f"Очистить {name}", command=cmd)
            btn.pack(pady=5, fill='x')

    def clean_chrome_cache(self):
        """Очистка кэша Chrome"""
        paths = [
            os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
            os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Media Cache')
        ]
        self.clean_browser_cache(paths, 'Chrome')

    def clean_firefox_cache(self):
        """Очистка кэша Firefox"""
        paths = [
            os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles/*/cache2'),
            os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles/*/thumbnails')
        ]
        self.clean_browser_cache(paths, 'Firefox')

    def clean_browser_cache(self, paths, browser_name):
        """Общая функция очистки кэша"""
        try:
            total = 0
            self.progress['value'] = 0
            self.update_status(f"Очистка кэша {browser_name}...")
            
            for path_pattern in paths:
                for path in glob.glob(path_pattern):
                    if os.path.exists(path):
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                try:
                                    os.remove(os.path.join(root, file))
                                    total += 1
                                except Exception as e:
                                    logging.warning(f"Ошибка удаления {file}: {str(e)}")
            
            messagebox.showinfo("Успех", f"Очищен кэш {browser_name}\nУдалено файлов: {total}")
            self.update_status("Очистка кэша завершена")
            
        except Exception as e:
            self.handle_error(e)
        finally:
            self.progress['value'] = 100

    # Добавляем недостающие методы для Edge
    def clean_edge_cache(self):
        """Очистка кэша Microsoft Edge"""
        paths = [
            os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
            os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Media Cache')
        ]
        self.clean_browser_cache(paths, 'Microsoft Edge')

    def clean_opera_cache(self):
        """Очистка кэша Opera"""
        paths = [
            os.path.expanduser('~/AppData/Roaming/Opera Software/Opera Stable/Cache'),
            os.path.expanduser('~/AppData/Roaming/Opera Software/Opera Stable/Media Cache')
        ]
        self.clean_browser_cache(paths, 'Opera')

    # === Вкладка анализа дисков ===
    def init_disk_analysis_tab(self):
        """Инициализация вкладки анализа дискового пространства"""
        frame = ttk.Frame(self.tab_disk)  # Исправлено
        frame.pack(fill='both', expand=True)
        
        self.disk_tree = ttk.Treeview(frame, columns=('Диск', 'Всего', 'Использовано', 'Свободно', 'Использование'), show='headings')
        
        for col in self.disk_tree['columns']:
            self.disk_tree.heading(col, text=col)
            self.disk_tree.column(col, width=150, anchor=tk.CENTER)
            
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.disk_tree.yview)
        self.disk_tree.configure(yscrollcommand=scrollbar.set)
        
        self.disk_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def update_disk_analysis(self):
        """Обновление информации о дисках"""
        for item in self.disk_tree.get_children():
            self.disk_tree.delete(item)
            
        for partition in psutil.disk_partitions():
            if partition.fstype:
                usage = psutil.disk_usage(partition.mountpoint)
                self.disk_tree.insert('', 'end', values=(
                    partition.device,
                    f"{usage.total // (1024**3)} GB",
                    f"{usage.used // (1024**3)} GB",
                    f"{usage.free // (1024**3)} GB",
                    f"{usage.percent}%"
                ))



    # === Вкладка управления службами ===
    def init_services_tab(self):
        """Инициализация вкладки управления службами"""
        frame = ttk.Frame(self.tab_services)  # Исправлено
        frame.pack(fill='both', expand=True)
        
        self.services_tree = ttk.Treeview(frame, columns=('Служба', 'Состояние', 'Тип запуска'), show='headings')
        
        for col in self.services_tree['columns']:
            self.services_tree.heading(col, text=col)
            self.services_tree.column(col, width=200)
            
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.services_tree.yview)
        self.services_tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(frame)
        ttk.Button(btn_frame, text="Обновить", command=self.update_services).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Остановить", command=lambda: self.control_service('stop')).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Запустить", command=lambda: self.control_service('start')).pack(side='left', padx=2)
        
        self.services_tree.pack(side='top', fill='both', expand=True)
        btn_frame.pack(side='bottom', pady=5)
        scrollbar.pack(side='right', fill='y')

    def update_services(self):
        """Обновление списка служб с сортировкой"""
        self.services_tree.delete(*self.services_tree.get_children())
        try:
            services = []
            for service in psutil.win_service_iter():
                s = service.as_dict()
                services.append((s['name'], s['status'], s['start_type']))
            
            # Сортировка по статусу
            services.sort(key=lambda x: x[1], reverse=True)
            
            for service in services:
                self.services_tree.insert('', 'end', values=service)
                
            # Настройка сортировки по клику на заголовки
            for col in self.services_tree['columns']:
                self.services_tree.heading(col, command=lambda _col=col: self.treeview_sort_column(self.services_tree, _col, False))
                
        except Exception as e:
            self.handle_error(e)

    def treeview_sort_column(self, tv, col, reverse):
        """Сортировка столбцов Treeview"""
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def control_service(self, action):
        """Управление службами (запуск/остановка)"""
        selected = self.services_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите службу")
            return
            
        service_name = self.services_tree.item(selected[0])['values'][0]
        try:
            if action == 'stop':
                subprocess.run(['net', 'stop', service_name], check=True)
            elif action == 'start':
                subprocess.run(['net', 'start', service_name], check=True)
                
            self.update_services()
            messagebox.showinfo("Успех", f"Служба {service_name} {action} успешно")
            
        except subprocess.CalledProcessError as e:
            self.handle_error(e)

    # === Общие методы ===
    def handle_error(self, error):
        """Обработка и логирование ошибок"""
        logging.error(f"Ошибка: {str(error)}")
        messagebox.showerror("Ошибка", f"{str(error)}\nПодробности в логах")
        self.update_status("Ошибка выполнения операции")

    def update_status(self, message):
        """Обновление статусной строки"""
        self.status.config(text=message)
        self.master.update_idletasks()

    def update_progress(self, value):
        def animate():
            current = self.progress['value']
            while current < value:
                current += 1
                self.progress['value'] = current
                time.sleep(0.01)
                if not self.running:
                    break
        
        if value > 0:
            threading.Thread(target=animate, daemon=True).start()
        else:
            self.progress['value'] = 0

    def init_restore_tab(self):
        """Вкладка восстановления системы"""
        frame = ttk.LabelFrame(self.tab_restore, text="Точки восстановления")
        frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.restore_list = ttk.Treeview(frame, columns=('Дата', 'Описание'), show='headings')
        self.restore_list.heading('Дата', text='Дата создания')
        self.restore_list.heading('Описание', text='Описание')
        
        btn_frame = ttk.Frame(frame)
        ttk.Button(btn_frame, text="Создать точку", command=self.create_restore_point).pack(pady=5)
        ttk.Button(btn_frame, text="Обновить список", command=self.load_restore_points).pack(pady=5)
        
        self.restore_list.pack(side='left', fill='both', expand=True)
        btn_frame.pack(side='right', padx=10)
        
        self.load_restore_points()

    def create_restore_point(self):
        """Создание точки восстановления с улучшенной обработкой ошибок"""
        try:
            if not is_admin():
                messagebox.showerror("Ошибка", "Требуются права администратора!")
                return

            # Проверка защиты системы через WMI
            sr_check = subprocess.run(
                'powershell -Command "(Get-ComputerRestore -Drive C:).ProtectionEnabled"',
                capture_output=True,
                shell=True,
                encoding=system_encoding,
                errors='replace'
            )

            if sr_check.returncode != 0 or "True" not in sr_check.stdout:
                messagebox.showerror(
                    "Ошибка", 
                    "Защита системы отключена или произошла ошибка!\n"
                    "Включите защиту системы для диска C: в настройках."
                )
                return

            description = simpledialog.askstring("Создание точки", "Введите описание:")
            if description:
                result = subprocess.run(
                    f'powershell -Command "Checkpoint-Computer -Description \'{description}\'"',
                    shell=True,
                    capture_output=True,
                    encoding=system_encoding,
                    errors='replace'
                )

                if result.returncode != 0:
                    error_msg = result.stderr or f"Код ошибки: {result.returncode}"
                    raise Exception(f"Ошибка PowerShell: {error_msg}")
                
                self.load_restore_points()
                messagebox.showinfo("Успех", "Точка восстановления создана")

        except Exception as e:
            self.handle_error(e)

    def load_restore_points(self):
        """Загрузка точек восстановления с улучшенным парсингом"""
        try:
            self.restore_list.delete(*self.restore_list.get_children())
            
            result = subprocess.run(
                'powershell -Command "Get-ComputerRestorePoint | '
                'Select-Object CreationTime, Description | '
                'ConvertTo-Json -Compress"',
                capture_output=True,
                shell=True,
                encoding=system_encoding,
                errors='replace'
            )

            if result.returncode != 0:
                raise Exception(f"Ошибка PowerShell: {result.stderr}")

            try:
                data = json.loads(result.stdout)
                for point in data:
                    creation_time = datetime.strptime(
                        point['CreationTime'].split('.')[0], 
                        '%m/%d/%Y %H:%M:%S'
                    ).strftime('%Y-%m-%d %H:%M:%S')
                    self.restore_list.insert('', 'end', 
                        values=(creation_time, point['Description']))
            except json.JSONDecodeError:
                self.parse_manual_restore_points(result.stdout)
                
        except Exception as e:
            self.handle_error(e)

    def parse_manual_restore_points(self, output):
        """Альтернативный парсинг для старых версий PowerShell"""
        current_point = {}
        for line in output.split('\n'):
            line = line.strip()
            if 'CreationTime' in line:
                current_point['date'] = line.split(':', 1)[1].strip()
            elif 'Description' in line:
                current_point['desc'] = line.split(':', 1)[1].strip()
                if current_point.get('date') and current_point.get('desc'):
                    try:
                        dt = datetime.strptime(
                            current_point['date'].split('.')[0],
                            '%m/%d/%Y %H:%M:%S'
                        )
                        self.restore_list.insert('', 'end', 
                            values=(dt.strftime('%Y-%m-%d %H:%M:%S'), 
                            current_point['desc']))
                    except ValueError:
                        self.restore_list.insert('', 'end', 
                            values=(current_point['date'], current_point['desc']))
                    current_point = {}

    def remove_scheduled_task(self):
        """Удаление выбранной задачи из планировщика"""
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления")
            return
    
        try:
            # Получаем данные задачи
            task_time, task_description = self.schedule_tree.item(selected[0])['values']
        
            # Удаляем задачу из расписания
            schedule.clear(task_description)
        
            # Удаляем из списка
            self.schedule_tree.delete(selected[0])
            messagebox.showinfo("Успех", "Задача успешно удалена")
        
        except Exception as e:
            self.handle_error(e)

    def init_scheduler_tab(self):
        """Вкладка планировщика задач"""
        frame = ttk.Frame(self.tab_scheduler)
        self.schedule_tree = ttk.Treeview(frame, columns=('Время', 'Задача'), show='headings')
        self.schedule_tree.heading('Время', text='Время выполнения')
        self.schedule_tree.heading('Задача', text='Описание задачи')
        
        btn_frame = ttk.Frame(frame)
        ttk.Button(btn_frame, text="Добавить задачу", command=self.add_scheduled_task).pack(pady=5)
        ttk.Button(btn_frame, text="Удалить задачу", command=self.remove_scheduled_task).pack(pady=5)
        
        self.schedule_tree.pack(side='left', fill='both', expand=True)
        btn_frame.pack(side='right', padx=10)
        frame.pack(fill='both', expand=True)

    def add_scheduled_task(self):
        """Добавление новой задачи в планировщик"""
        try:
            time = simpledialog.askstring("Время", "Введите время в формате HH:MM")
            task = simpledialog.askstring("Задача", "Введите описание задачи:")
            if time and task:
                # Добавляем задачу с тегом
                schedule.every().day.at(time).do(self.run_scheduled_task, task).tag(task)
                self.schedule_tree.insert('', 'end', values=(time, task))
        except Exception as e:
            self.handle_error(e)

    def run_scheduled_task(self, task):
        """Выполнение запланированной задачи"""
        try:
            messagebox.showinfo("Планировщик", f"Выполняется задача: {task}")
        except Exception as e:
            logging.error(f"Ошибка показа уведомления: {str(e)}")

    def start_resource_monitor(self):
        """Запуск мониторинга ресурсов в отдельном потоке"""
        def monitor():
            while self.running:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                
                self.resource_labels['cpu'].config(text=f"CPU: {cpu}%")
                self.resource_labels['ram'].config(text=f"RAM: {ram}%")
                self.resource_labels['disk'].config(text=f"Disk: {disk}%")
                time.sleep(1)
        
        threading.Thread(target=monitor, daemon=True).start()

    def start_scheduler(self):
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        threading.Thread(target=run_scheduler, daemon=True).start()

    def check_updates(self):
        """Проверка обновлений с обработкой ошибок"""
        try:
            response = requests.get(
                "https://api.github.com/repos/yourname/pc-optimizer/releases/latest",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            latest_version = data.get('tag_name', '')
            current_version = "1.0.0"
            
            if latest_version > current_version:
                if messagebox.askyesno(
                    "Обновление",
                    f"Доступна новая версия {latest_version}! Обновить?"
                ):
                    webbrowser.open(data.get('html_url', ''))
                    
        except requests.exceptions.RequestException as e:
            logging.warning(f"Ошибка проверки обновлений: {str(e)}")
        except Exception as e:
            logging.error(f"Ошибка обновления: {str(e)}")

    def on_close(self):
        self.running = False
        self.master.destroy()

    def optimize_disk(self):
        """Дефрагментация диска"""
        try:
            self.update_progress(0)
            drives = [partition.device[0] for partition in psutil.disk_partitions()]
            
            for i, drive in enumerate(drives):
                self.update_status(f"Оптимизация диска {drive}...")
                subprocess.run(f'defrag {drive}: /U /V', shell=True, check=True)
                self.update_progress((i+1)/len(drives)*100)
                
            messagebox.showinfo("Успех", "Оптимизация дисков завершена")
        except Exception as e:
            self.handle_error(e)
        finally:
            self.update_progress(0)

    def update_progress(self, value):
        """Обновление прогресс-бара с анимацией"""
        def animate():
            current = self.progress['value']
            while current < value:
                current += 1
                self.progress['value'] = current
                time.sleep(0.01)
        
        if value > 0:
            threading.Thread(target=animate).start()
        else:
            self.progress['value'] = 0

    def handle_error(self, error):
        """Унифицированная обработка ошибок"""
        error_msg = str(error).encode(system_encoding, errors='replace').decode(system_encoding)
        logging.error(f"Ошибка: {error_msg}", exc_info=True)
        self.master.after(0, lambda: messagebox.showerror(
            "Ошибка",
            f"{error_msg}\n\nПодробности в логах",
            parent=self.master
        ))
        self.update_status("Ошибка выполнения операции")

if __name__ == "__main__":
    try:
        root = ThemedTk(theme="equilux")
        app = ModernOptimizerApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_close)
        root.mainloop()
    except Exception as e:
        error_msg = str(e).encode(system_encoding, errors='replace').decode(system_encoding)
        ctypes.windll.user32.MessageBoxW(0, f"Ошибка инициализации: {error_msg}", "Ошибка", 0x10)