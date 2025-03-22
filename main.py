import sys
import os
import ctypes
import tkinter as tk
from pathlib import Path
from ctypes import c_int
from ctypes.wintypes import HWND, LPCWSTR
from core.utilities import setup_logging
def setup_environment():
    """Безопасная настройка окружения"""
    try:
        base_path = Path(__file__).resolve().parent
        os.chdir(base_path)
        sys.path.insert(0, str(base_path))
        print(f"[INFO] Рабочая директория: {base_path}")
        return True
    except Exception as e:
        print(f"[ОШИБКА] Ошибка настройки окружения: {str(e)}")
        return False

def is_admin():
    """Проверка прав администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"[ОШИБКА] Проверка прав админа: {str(e)}")
        return False

def run_as_admin():
    """Перезапуск с правами администратора"""
    if is_admin():
        return False

    try:
        ShellExecuteW = ctypes.windll.shell32.ShellExecuteW
        ShellExecuteW.argtypes = [HWND, LPCWSTR, LPCWSTR, LPCWSTR, LPCWSTR, c_int]
        ShellExecuteW.restype = ctypes.c_void_p

        parameters = ' '.join([f'"{x}"' for x in sys.argv])
        result = ShellExecuteW(
            None,
            "runas",
            sys.executable,
            parameters,
            str(Path(__file__).parent.absolute()),
            1
        )

        if result <= 32:
            print(f"[ОШИБКА] Ошибка ShellExecute: {result}")
            return False

        return True
    except Exception as e:
        print(f"[ОШИБКА] Ошибка повышения прав: {str(e)}")
        return False

def main():

    setup_logging()
    """Основная функция"""
    if not setup_environment():
        input("Нажмите Enter для выхода...")
        sys.exit(1)

    try:
        if run_as_admin():
            sys.exit(0)

        from core.app import OptimizerApp

        root = tk.Tk()
        root.title("PC Optimizer Pro")
        root.geometry("1200x800")

        app = OptimizerApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_close)

        print("[ИНФО] Запуск основного цикла")
        root.mainloop()

    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] {str(e)}")
    finally:
        if 'root' in locals():
            root.destroy()

    input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    print("[ЗАПУСК] Приложение стартует...")
    main()