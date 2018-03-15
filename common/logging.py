import os
import sys
from datetime import datetime

LVL_DEBUG, LVL_INFO, LVL_WARN, LVL_ERROR, LVL_FATAL = range(5)

CFG_MIN_LEVEL = LVL_DEBUG if os.getenv('DEBUG') is not None else LVL_INFO


def _fmt_log_msg(lvl: str, fmt: str, *fmt_args) -> str:
    timestamp = datetime.now().strftime('%H:%M:%S')
    formatted = fmt.format(*fmt_args)
    return f"[{timestamp}] {lvl}: {formatted}"


def debug(msg, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_DEBUG:
        print(_fmt_log_msg('DEBUG', msg, *fmt_args))


def info(msg, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_INFO:
        print(_fmt_log_msg('INFO', msg, *fmt_args))


def warn(msg, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_WARN:
        print(_fmt_log_msg('WARN', msg, *fmt_args))


def error(msg, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_ERROR:
        print(_fmt_log_msg('ERROR', msg, *fmt_args), file=sys.stderr)


def fatal(msg, *fmt_args) -> None:
    if CFG_MIN_LEVEL <= LVL_FATAL:
        print(_fmt_log_msg('FATAL', msg, *fmt_args), file=sys.stderr)
