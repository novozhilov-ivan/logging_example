from logging import (
    DEBUG,
    FileHandler,
    Formatter,
    Handler,
    INFO,
    LogRecord,
    NOTSET,
    StreamHandler,
)
from logging.config import dictConfig
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal


@dataclass(kw_only=True)
class CustomFormatter(Formatter):
    fmt: str = (
        "{asctime} - {loggerName} - {levelName:<8} - "
        "{filename:<15} - {funcName:<10} - {message} - "
        "{exceptionInfo} - {stackTrace}"
    )
    datefmt: str = "%Y-%m-%dT%H:%M:%S"
    style: Literal["{"] = "{"

    def __post_init__(self) -> None:
        super().__init__(self.fmt, self.datefmt, self.style)

    def formatTime(
        self,
        record: LogRecord,
        datefmt: str | None = None,
    ) -> str:
        dt = datetime.fromtimestamp(record.created, UTC)
        return dt.strftime(datefmt or self.datefmt)

    def format(self, record: LogRecord) -> str:
        log_dict = {
            "asctime": self.formatTime(record),
            "loggerName": record.name,
            "levelName": record.levelname,
            "levelNumber": record.levelno,
            "message": record.getMessage(),
            "module": record.module,
            "filename": record.filename,
            "filePath": record.pathname,
            "funcName": record.funcName,
            "exceptionInfo": (
                f"Exception: {self.formatException(record.exc_info)}"
                if record.exc_info
                else ""
            ),
            "stackTrace": (
                f"stackTrace: {self.formatStack(record.stack_info)}"
                if record.stack_info
                else ""
            ),
        }
        return self._get_fmt(log_dict)

    def _get_fmt(self, log_dict: dict[str, str]) -> str:
        return self._fmt.format(
            asctime=log_dict.get("asctime", ""),
            loggerName=log_dict.get("loggerName", ""),
            levelName=log_dict.get("levelName", ""),
            levelNumber=log_dict.get("levelNumber", ""),
            message=log_dict.get("message", ""),
            module=log_dict.get("module", ""),
            filename=log_dict.get("filename", ""),
            filePath=log_dict.get("filePath", ""),
            funcName=log_dict.get("funcName", ""),
            exceptionInfo=log_dict.get("exceptionInfo", ""),
            stackTrace=log_dict.get("stackTrace", ""),
        )


@dataclass(kw_only=True)
class BaseHandlerConfig(ABC):
    class_: Handler
    level: int = NOTSET
    formatter: str

    @abstractmethod
    def as_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(kw_only=True)
class FileHandlerConfig(BaseHandlerConfig):
    class_: Handler = FileHandler
    filename: str = "log.log"
    mode: str = "a"
    encoding: str = "utf-8"
    delay: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "class": self.class_,
            "filename": self.filename,
            "mode": self.mode,
            "encoding": self.encoding,
            "delay": self.delay,
            "formatter": self.formatter,
            "level": self.level,
        }


@dataclass(kw_only=True)
class ConsoleHandlerConfig(BaseHandlerConfig):
    class_: Any = StreamHandler

    def as_dict(self) -> dict[str, Any]:
        return {
            "class": self.class_,
            "formatter": self.formatter,
            "level": self.level,
        }


@dataclass(kw_only=True)
class LoggingConfig:
    version: int = 1
    formatters: dict[str, dict[str, str | type[Formatter]]]
    handlers: dict[str, BaseHandlerConfig]
    loggers: dict[str, dict[str, Any]]
    disable_existing_loggers: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "formatters": self.formatters,
            "handlers": {
                name: handler.as_dict() for name, handler in self.handlers.items()
            },
            "loggers": self.loggers,
        }


def get_logging_config() -> dict[str, Any]:
    logging_config = LoggingConfig(
        formatters={"custom": {"()": "config.CustomFormatter"}},
        handlers={
            "file": FileHandlerConfig(
                level=DEBUG,
                formatter="custom",
            ),
            "console": ConsoleHandlerConfig(
                level=INFO,
                formatter="custom",
            ),
        },
        loggers={
            "app": {
                "level": DEBUG,
                "handlers": [],
            },
            "": {
                "level": DEBUG,
                "handlers": ["file", "console"],
            },
        },
    )

    return logging_config.as_dict()


def setup_logging() -> None:
    dictConfig(get_logging_config())
