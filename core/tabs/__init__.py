# Экспорт всех вкладок
from .about_tab import AboutTab
from .cleaner_tab import CleanerTab
from .startup_tab import StartupTab
from .browser_tab import BrowserTab
from .disk_tab import DiskTab
from .services_tab import ServicesTab
from .restore_tab import RestoreTab
from .scheduler_tab import SchedulerTab

__all__ = [
    'AboutTab',
    'CleanerTab',
    'StartupTab',
    'BrowserTab',
    'DiskTab',
    'ServicesTab',
    'RestoreTab',
    'SchedulerTab'
]