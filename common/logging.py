import os
import sys
from datetime import datetime

LVL_DEBUG, LVL_INFO, LVL_WARN, LVL_ERROR, LVL_FATAL = range(5)

CFG_MIN_LEVEL = LVL_DEBUG if os.getenv('DEBUG') is not None else LVL_INFO


def _fmt_log_msg(lvl: str, fmt: str, *fmt_args) -> str:
    timestamp = datetime.now().strftime('%H:%M:%S')
    return "[{}] {}: {}".format(timestamp, lvl, fmt.format(*fmt_args))


def debug(fmt, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_DEBUG:
        print(_fmt_log_msg('DEBUG', fmt, *fmt_args))


def info(fmt, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_INFO:
        print(_fmt_log_msg('INFO', fmt, *fmt_args))


def warn(fmt, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_WARN:
        print(_fmt_log_msg('WARN', fmt, *fmt_args), file=sys.stderr)


def error(fmt, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_ERROR:
        print(_fmt_log_msg('ERROR', fmt, *fmt_args), file=sys.stderr)


def fatal(fmt, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_FATAL:
        print(_fmt_log_msg('FATAL', fmt, *fmt_args), file=sys.stderr)
