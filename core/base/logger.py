import logging
import sys
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import ClassVar


class LogLevel(str, Enum):
    """Уровни логирования."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ColoredFormatter(logging.Formatter):
    """
    Форматтер для цветного вывода логов в консоль.

    Применяет ANSI цветовые коды к уровням логирования для
    улучшения визуального восприятия в терминале.
    """

    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """
        Форматирует запись лога с цветовым выделением.

        Args:
            record: Запись лога для форматирования.

        Returns:
            str: Отформатированная строка с ANSI цветовыми кодами.
        """
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        record.name = f"\033[34m{record.name}{self.RESET}"  # Blue for logger name
        return super().format(record)


class LoggerConfig:
    """
    Конфигуратор системы логирования (Singleton).

    Обеспечивает единую точку настройки логирования для всего приложения.
    Поддерживает вывод в консоль и файл.
    """

    _instance: ClassVar["LoggerConfig | None"] = None
    _initialized: bool = False

    def __new__(cls) -> "LoggerConfig":
        """
        Создаёт или возвращает существующий экземпляр (Singleton паттерн).

        Returns:
            LoggerConfig: Единственный экземпляр конфигуратора.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        level: LogLevel = LogLevel.INFO,
        log_format: str | None = None,
        date_format: str = "%Y-%m-%d %H:%M:%S",
        log_file: Path | str | None = None,
    ) -> None:
        """
        Инициализация конфигуратора логирования.

        Выполняется только один раз благодаря паттерну Singleton.

        Args:
            level: Уровень логирования (по умолчанию INFO).
            log_format: Формат строки лога.
            date_format: Формат даты/времени.
            log_file: Путь к файлу для записи логов (опционально).
        """
        if self._initialized:
            return

        self.level = level
        self.log_format = (
            log_format or "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        self.date_format = date_format
        self.log_file = Path(log_file) if log_file else None

        self._setup_root_logger()
        self._initialized = True

    def _setup_root_logger(self) -> None:
        """
        Настраивает корневой логгер приложения.

        Создаёт обработчики для консоли и файла (если указан),
        применяет форматтеры и устанавливает уровень логирования.
        """
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.level.value))

        root_logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, self.level.value))
        console_handler.setFormatter(
            ColoredFormatter(self.log_format, datefmt=self.date_format)
        )
        root_logger.addHandler(console_handler)

        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
            file_handler.setLevel(getattr(logging, self.level.value))
            file_handler.setFormatter(
                logging.Formatter(self.log_format, datefmt=self.date_format)
            )
            root_logger.addHandler(file_handler)


@lru_cache(maxsize=128)
def get_logger(name: str) -> logging.Logger:
    """
    Получить логгер по имени с кэшированием.

    Кэширует до 128 логгеров для оптимизации производительности.

    Args:
        name: Имя логгера (обычно __name__ модуля).

    Returns:
        logging.Logger: Настроенный экземпляр логгера.
    """
    return logging.getLogger(name)


def setup_logging(
    level: LogLevel = LogLevel.INFO,
    log_file: Path | str | None = None,
) -> LoggerConfig:
    """
    Инициализирует систему логирования приложения.

    Args:
        level: Уровень логирования (по умолчанию INFO).
        log_file: Путь к файлу для записи логов (опционально).

    Returns:
        LoggerConfig: Экземпляр конфигуратора логирования.
    """
    return LoggerConfig(level=level, log_file=log_file)
