import json
import logging
import os
import ctypes
from pathlib import Path
from datetime import datetime

def is_admin() -> bool:
    """Проверяет, запущен ли скрипт с правами администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logging.error(f"Admin check error: {str(e)}")
        return False

def format_size(size_bytes: float) -> str:
    """Форматирует размер в удобочитаемый вид (КБ, МБ, ГБ)."""
    units = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
    unit_index = 0
    size = size_bytes

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"

def safe_file_operation(file_path, default_data, mode='read'):
    """Безопасные операции с JSON-файлами."""
    file_path = Path(file_path)
    try:
        if mode == 'write':
            file_path.write_text(
                json.dumps(default_data, indent=2, ensure_ascii=False), 
                encoding='utf-8'
            )
            return True
        
        if not file_path.exists():
            file_path.write_text(json.dumps(default_data), encoding='utf-8')
            return default_data
            
        content = file_path.read_text(encoding='utf-8').strip()
        return json.loads(content) if content else default_data
        
    except Exception as e:
        logging.error(f"File error ({file_path}): {str(e)}")
        return default_data if mode == 'read' else False

def setup_logging():
    """Инициализация системы логирования с гарантией создания файла."""
    log_file = Path("optimizer.log")
    
    # Создаем файл, если его нет
    if not log_file.exists():
        log_file.write_text("", encoding='utf-8')
    
    # Настройка логгера с добавлением записей (filemode='a')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8',
        filemode='a'  # Режим добавления записей
    )

def check_logger():
    """Проверка состояния логгера"""
    logger = logging.getLogger()
    if not logger.handlers:
        print("Логгер не настроен. Настраиваю...")
        setup_logging()
    else:
        print("Логгер настроен и работает.")


def log_action(action, status="OK", details=""):
    """Запись действия в лог-файл с гарантией целостности данных."""
    check_logger()  # Проверяем состояние логгера
    try:
        logging.info(f"[{status}] {action} - {details}")
    except Exception as e:
        print(f"Ошибка записи в лог: {str(e)}")