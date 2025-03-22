from tkinter import ttk
from ttkthemes import ThemedTk
from .styles import AppStyles
from .utilities import log_action
from .tabs import (
    AboutTab,
    CleanerTab,
    StartupTab,
    BrowserTab,
    DiskTab,
    ServicesTab,
    RestoreTab,
    SchedulerTab
)

class OptimizerApp:
    """Главный класс приложения."""
    def __init__(self, master):
        """Инициализация приложения."""
        self.master = master
        self.styles = AppStyles()  # Инициализация стилей
        self.running = True
        
        self._configure_window()  # Настройка окна
        self._create_widgets()  # Создание виджетов
        log_action("Приложение запущено")  # Логируем запуск приложения
        
    def _configure_window(self):
        """Настройка главного окна."""
        self.master.title("PC Optimizer Pro")  # Заголовок окна
        self.master.geometry("1200x800")  # Размер окна
        self.master.minsize(800, 600)  # Минимальный размер окна
        self.master.configure(bg="white")  # Белый фон окна
        
    def _create_widgets(self):
        """Создание элементов интерфейса."""
        # Notebook для вкладок
        self.notebook = ttk.Notebook(self.master)
        
        # Инициализация вкладок
        self.tabs = {
            'about': AboutTab(self.notebook),
            'cleaner': CleanerTab(self.notebook),
            'startup': StartupTab(self.notebook),
            'browser': BrowserTab(self.notebook),
            'disk': DiskTab(self.notebook),
            'services': ServicesTab(self.notebook),
            'restore': RestoreTab(self.notebook),
            'scheduler': SchedulerTab(self.notebook)
        }
        
        # Добавление вкладок
        for name, tab in self.tabs.items():
            self.notebook.add(tab.frame, text=tab.TAB_NAME)
            
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Логируем переходы между вкладками
        self.notebook.bind("<<NotebookTabChanged>>", self._log_tab_change)
        
        # Статусная строка
        self.status_bar = ttk.Label(
            self.master,
            text="Готово",
            style='Status.TLabel'
        )
        self.status_bar.pack(side='bottom', fill='x')
        
    def _log_tab_change(self, event):
        """Логирование перехода между вкладками."""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        log_action(f"Переход во вкладку: {selected_tab}")
        
    def on_close(self):
        """Обработчик закрытия приложения."""
        log_action("Приложение закрыто")
        self.running = False
        self.master.destroy()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Используем ThemedTk с темой "arc"
    app = OptimizerApp(root)
    root.mainloop()