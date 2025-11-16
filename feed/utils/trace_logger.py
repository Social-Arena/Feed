"""
Trace Logger - Comprehensive file-based logging system for debugging
No console logs - all logs stored to files for post-mortem analysis
"""

import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from functools import wraps
import threading


class TraceLogger:
    """
    Centralized trace logger that stores all system logs to files
    Supports multiple log levels, structured logging, and performance tracking
    """

    _instances: Dict[str, 'TraceLogger'] = {}
    _lock = threading.Lock()

    def __init__(self, name: str, trace_dir: str = "./trace"):
        """
        Initialize trace logger

        Args:
            name: Logger name (typically module name)
            trace_dir: Directory to store trace files
        """
        self.name = name
        self.trace_dir = Path(trace_dir)
        self.trace_dir.mkdir(exist_ok=True)

        # Create subdirectories for different log types
        self.errors_dir = self.trace_dir / "errors"
        self.warnings_dir = self.trace_dir / "warnings"
        self.info_dir = self.trace_dir / "info"
        self.debug_dir = self.trace_dir / "debug"
        self.performance_dir = self.trace_dir / "performance"

        for dir_path in [self.errors_dir, self.warnings_dir, self.info_dir,
                         self.debug_dir, self.performance_dir]:
            dir_path.mkdir(exist_ok=True)

        # Setup file handlers
        self._setup_logger()

        # Performance tracking
        self.performance_data = []

    @classmethod
    def get_logger(cls, name: str, trace_dir: str = "./trace") -> 'TraceLogger':
        """
        Get or create a logger instance (singleton per name)

        Args:
            name: Logger name
            trace_dir: Trace directory

        Returns:
            TraceLogger instance
        """
        with cls._lock:
            if name not in cls._instances:
                cls._instances[name] = cls(name, trace_dir)
            return cls._instances[name]

    def _setup_logger(self):
        """Setup file-based logging handlers"""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        # Remove any existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Daily log file with timestamp
        today = datetime.now().strftime("%Y%m%d")

        # Main log file (all levels)
        main_log = self.trace_dir / f"{self.name}_{today}.log"
        main_handler = logging.FileHandler(main_log, encoding='utf-8')
        main_handler.setLevel(logging.DEBUG)
        main_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(main_handler)

        # Error log file (errors only)
        error_log = self.errors_dir / f"{self.name}_errors_{today}.log"
        error_handler = logging.FileHandler(error_log, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(error_handler)

    def debug(self, message: str, **kwargs):
        """Log debug message with optional structured data"""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message with optional structured data"""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message with optional structured data"""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error message with optional exception and structured data"""
        extra_data = kwargs.copy()

        if exception:
            extra_data['exception_type'] = type(exception).__name__
            extra_data['exception_message'] = str(exception)
            extra_data['traceback'] = traceback.format_exc()

        self._log(logging.ERROR, message, **extra_data)

        # Save detailed error report
        self._save_error_report(message, exception, extra_data)

    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log critical message with optional exception and structured data"""
        extra_data = kwargs.copy()

        if exception:
            extra_data['exception_type'] = type(exception).__name__
            extra_data['exception_message'] = str(exception)
            extra_data['traceback'] = traceback.format_exc()

        self._log(logging.CRITICAL, message, **extra_data)

        # Save detailed error report
        self._save_error_report(message, exception, extra_data, level="CRITICAL")

    def _log(self, level: int, message: str, **kwargs):
        """Internal log method with structured data support"""
        # Format message with structured data
        if kwargs:
            try:
                structured_data = json.dumps(kwargs, default=str, indent=2)
                full_message = f"{message}\nStructured Data: {structured_data}"
            except Exception as e:
                full_message = f"{message}\nStructured Data (serialization failed): {kwargs}"
        else:
            full_message = message

        self.logger.log(level, full_message)

    def _save_error_report(self, message: str, exception: Optional[Exception],
                          extra_data: Dict[str, Any], level: str = "ERROR"):
        """Save detailed error report as JSON"""
        timestamp = datetime.now()
        report = {
            "timestamp": timestamp.isoformat(),
            "level": level,
            "logger": self.name,
            "message": message,
            "exception": {
                "type": extra_data.get('exception_type'),
                "message": extra_data.get('exception_message'),
                "traceback": extra_data.get('traceback')
            } if exception else None,
            "context": {k: v for k, v in extra_data.items()
                       if k not in ['exception_type', 'exception_message', 'traceback']}
        }

        # Save to timestamped file
        filename = f"{self.name}_{level.lower()}_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = self.errors_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    def log_performance(self, operation: str, duration_ms: float, **metrics):
        """Log performance metrics"""
        perf_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_ms": duration_ms,
            **metrics
        }

        self.performance_data.append(perf_data)

        # Also log to file
        self.info(f"Performance: {operation} took {duration_ms:.2f}ms", **metrics)

        # Save performance report every 100 operations
        if len(self.performance_data) >= 100:
            self._save_performance_report()

    def _save_performance_report(self):
        """Save accumulated performance data"""
        if not self.performance_data:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.name}_performance_{timestamp}.json"
        filepath = self.performance_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.performance_data, f, indent=2)

        self.performance_data.clear()

    def log_function_call(self, func_name: str, args: tuple, kwargs: dict, result: Any = None,
                         exception: Optional[Exception] = None):
        """Log function call details for debugging"""
        call_data = {
            "function": func_name,
            "args": str(args),
            "kwargs": str(kwargs),
            "result": str(result) if result is not None else None,
            "success": exception is None
        }

        if exception:
            self.error(f"Function call failed: {func_name}", exception=exception, **call_data)
        else:
            self.debug(f"Function call: {func_name}", **call_data)

    def trace_decorator(self, func):
        """Decorator to trace function calls"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            start_time = datetime.now()

            self.debug(f"Entering: {func_name}", args=str(args), kwargs=str(kwargs))

            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds() * 1000

                self.debug(f"Exiting: {func_name}", duration_ms=duration, result=str(result)[:200])
                self.log_performance(func_name, duration)

                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds() * 1000
                self.error(f"Exception in {func_name}", exception=e,
                          args=str(args), kwargs=str(kwargs), duration_ms=duration)
                raise

        return wrapper


# Convenience function to get logger
def get_trace_logger(name: str, trace_dir: str = "./trace") -> TraceLogger:
    """
    Get a trace logger instance

    Args:
        name: Logger name (use __name__ from calling module)
        trace_dir: Directory for trace files

    Returns:
        TraceLogger instance
    """
    return TraceLogger.get_logger(name, trace_dir)


# Example usage in modules:
# logger = get_trace_logger(__name__)
# logger.info("Starting process", user_id="123", action="create_feed")
#
# @logger.trace_decorator
# def my_function():
#     pass
