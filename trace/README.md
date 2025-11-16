# Trace Logs Directory

This directory contains runtime logs for the Feed viral simulation system.

## Directory Structure

- `errors/` - Error and critical issue logs with detailed stack traces
- `warnings/` - Warning messages and potential issues
- `info/` - Informational logs about system operations
- `debug/` - Detailed debug logs for troubleshooting
- `performance/` - Performance metrics and timing data

## Log File Naming

- Main logs: `{module_name}_{YYYYMMDD}.log`
- Error reports: `{module_name}_error_{YYYYMMDD_HHMMSS_microseconds}.json`
- Performance: `{module_name}_performance_{YYYYMMDD_HHMMSS}.json`

## Usage

All modules use the TraceLogger for logging:

```python
from feed.utils.trace_logger import get_trace_logger

logger = get_trace_logger(__name__)

# Log various levels
logger.debug("Debug message", extra_data="value")
logger.info("Info message", user_id="123")
logger.warning("Warning message")
logger.error("Error occurred", exception=e, context="additional info")

# Trace function calls
@logger.trace_decorator
def my_function():
    pass
```

## Debugging Process

1. Reproduce the issue
2. Check the relevant date logs in this directory
3. Review error JSON files for detailed stack traces
4. Examine performance logs for timing issues
5. Cross-reference with specific module logs

## Log Retention

Logs are organized by date. Clean up old logs periodically to manage disk space.
