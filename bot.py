#!/usr/bin/env python3
"""
HBX AUTO SCHEDULER — Telegram Multi-Client Channel Auto-Post Bot
Version: 2.0.1 (Fixed for PythonAnywhere)
"""

import sqlite3, logging, asyncio, os, sys, time, json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler,
    MessageHandler, CallbackQueryHandler, ContextTypes, filters,
)
from telegram.error import TelegramError, InvalidToken, BadRequest

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('hbx_bot.log')]
)
logger = logging.getLogger('HBX_BOT')

MAIN_BOT_TOKEN = "8523107574:AAENmN1g177w-m1v57A1YQ0WMaFyzwyqNY8"
SYSTEM_OWNER_ID = 8385124350

active_schedulers: Dict[str, asyncio.Task] = {}

def get_conn():
    conn = sqlite3.connect("hbx_system.db", check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, username TEXT DEFAULT '', first_name TEXT DEFAULT '',
            lang TEXT DEFAULT 'bn', is_banned INTEGER DEFAULT 0, is_admin INTEGER DEFAULT 0,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS client_bots (
            owner_id INTEGER PRIMARY KEY, bot_token TEXT UNIQUE NOT NULL,
            bot_username TEXT DEFAULT '', bot_name TEXT DEFAULT '', is_active INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT, owner_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL, channel_title TEXT DEFAULT '',
            channel_username TEXT DEFAULT '', added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(owner_id, channel_id)
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT, owner_id INTEGER NOT NULL,
            bot_token TEXT NOT NULL, from_chat_id INTEGER NOT NULL,
            target_chat_id INTEGER NOT NULL, message_id INTEGER NOT NULL,
            interval_seconds INTEGER DEFAULT 3600, is_active INTEGER DEFAULT 1,
            total_posts INTEGER DEFAULT 0, last_posted TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS schedule_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, task_id INTEGER NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, success INTEGER DEFAULT 1,
            error_message TEXT DEFAULT ''
        );
    """)
    conn.commit(); conn.close()
    logger.info("✅ Database ready")

init_db()

# ---- DB Operations ----
class DB:
    @staticmethod
    def reg_user(uid, un, fn):
        conn = get_conn()
        conn.execute("INSERT INTO users (user_id,username,first_name) VALUES (?,?,?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username,first_name=excluded.first_name,last_active=CURRENT_TIMESTAMP", (uid,un,fn))
        conn.commit(); conn.close()
    @staticmethod
    def get_lang(uid):
        conn = get_conn()
        r = conn.execute("SELECT lang FROM users WHERE user_id=?", (uid,)).fetchone()
        conn.close(); return r[0] if r else 'bn'
    @staticmethod
    def set_lang(uid, l):
        conn = get_conn()
        conn.execute("UPDATE users SET lang=?,last_active=CURRENT_TIMESTAMP WHERE user_id=?", (l,uid))
        conn.commit(); conn.close()
    @staticmethod
    def is_banned(uid):
        conn = get_conn()
        r = conn.execute("SELECT is_banned FROM users WHERE user_id=?", (uid,)).fetchone()
        conn.close(); return bool(r[0]) if r else False
    @staticmethod
    def save_bot(oid, tok, un='', nm=''):
        conn = get_conn()
        conn.execute("INSERT INTO client_bots (owner_id,bot_token,bot_username,bot_name) VALUES (?,?,?,?) ON CONFLICT(owner_id) DO UPDATE SET bot_token=excluded.bot_token,bot_username=excluded.bot_username,bot_name=excluded.bot_name,is_active=1", (oid,tok,un,nm))
        conn.commit(); conn.close()
    @staticmethod
    def get_bot(oid):
        conn = get_conn()
        r = conn.execute("SELECT bot_token FROM client_bots WHERE owner_id=? AND is_active=1", (oid,)).fetchone()
        conn.close(); return r[0] if r else None
    @staticmethod
    def save_task(oid, tok, fc, tc, mi, iv):
        conn = get_conn()
        cur = conn.execute("INSERT INTO tasks (owner_id,bot_token,from_chat_id,target_chat_id,message_id,interval_seconds) VALUES (?,?,?,?,?,?)", (oid,tok,fc,tc,mi,iv))
        conn.commit()
        tid = cur.lastrowid; conn.close(); return tid
    @staticmethod
    def get_tasks(oid):
        conn = get_conn()
        r = conn.execute("SELECT id,target_chat_id,interval_seconds,is_active,total_posts,created_at,last_posted FROM tasks WHERE owner_id=? ORDER BY created_at DESC", (oid,)).fetchall()
        conn.close(); return r
    @staticmethod
    def get_task(tid):
        conn = get_conn()
        r = conn.execute("SELECT id,owner_id,bot_token,from_chat_id,target_chat_id,message_id,interval_seconds,is_active FROM tasks WHERE id=?", (tid,)).fetchone()
        conn.close(); return r
    @staticmethod
    def toggle_task(tid, act):
        conn = get_conn()
        conn.execute("UPDATE tasks SET is_active=? WHERE id=?", (1 if act else 0, tid))
        conn.commit(); conn.close()
    @staticmethod
    def del_task(tid):
        conn = get_conn()
        conn.execute("DELETE FROM tasks WHERE id=?", (tid,))
        conn.execute("DELETE FROM schedule_log WHERE task_id=?", (tid,))
        conn.commit(); conn.close()
    @staticmethod
    def inc_post(tid):
        conn = get_conn()
        conn.execute("UPDATE tasks SET total_posts=total_posts+1,last_posted=CURRENT_TIMESTAMP WHERE id=?", (tid,))
        conn.commit(); conn.close()
    @staticmethod
    def add_ch(oid, cid, t='', un=''):
        conn = get_conn()
        conn.execute("INSERT INTO channels (owner_id,channel_id,channel_title,channel_username) VALUES (?,?,?,?) ON CONFLICT(owner_id,channel_id) DO UPDATE SET channel_title=excluded.channel_title,channel_username=excluded.channel_username", (oid,cid,t,un))
        conn.commit(); conn.close()
    @staticmethod
    def get_chs(oid):
        conn = get_conn()
        r = conn.execute("SELECT channel_id,channel_title,channel_username FROM channels WHERE owner_id=?", (oid,)).fetchall()
        conn.close(); return r
    @staticmethod
    def all_users():
        conn = get_conn()
        r = conn.execute("SELECT user_id,username,first_name,lang,is_banned,registered_at,last_active FROM users ORDER BY registered_at DESC").fetchall()
        conn.close(); return r
    @staticmethod
    def sys_stats():
        conn = get_conn()
        d = {
            'users': conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            'bots': conn.execute("SELECT COUNT(*) FROM client_bots").fetchone()[0],
            'tasks': conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            'active': conn.execute("SELECT COUNT(*) FROM tasks WHERE is_active=1").fetchone()[0],
            'posts': conn.execute("SELECT COALESCE(SUM(total_posts),0) FROM tasks").fetchone()[0],
            'chs': conn.execute("SELECT COUNT(*) FROM channels").fetchone()[0],
            'banned': conn.execute("SELECT COUNT(*) FROM users WHERE is_banned=1").fetchone()[0],
        }
        conn.close(); return d

db = DB()

# ---- Strings ----
S = {
    'bn': {
        'welcome': "⚡ **HBX Auto Scheduler** ⚡\n\n👋 স্বাগতম! তোমার Bot Token পাঠাও অথবা নিচের মেনু ব্যবহার করো।",
        'send_token': "🔑 Bot Token পাঠাও:\n`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`",
        'token_ok': "🟢 টোকেন ভ্যালিড! ✅\nবট: `{n}` @{u}\n\nএখন বটকে চ্যানেলে অ্যাডমিন করো,\nতারপর পোস্ট ফরোয়ার্ড করো।",
        'token_bad': "❌ টোকেন ভুল!\n{e}\nআবার চেষ্টা করো।",
        'post_ok': "🎨 পোস্ট সেভড! ✅\n\nইন্টারভাল সিলেক্ট করো:",
        'done': "🎉 শিডিউল তৈরি! ✅\nটাস্ক `#{i}` — প্রতি `{s}` সেকেন্ডে পোস্ট যাবে।",
        'lang': "🌐 ভাষা নির্বাচন করো:",
        'lang_set': "✅ ভাষা সেট: {l}",
        'banned': "❌ ব্যান করা হয়েছো।",
        'owner_only': "⛔ শুধু ওনার পারবেন।",
        'tasks': "📋 তোমার টাস্ক:\n",
        'no_task': "❌ কোনো টাস্ক নেই।",
        'task_pause': "⏸️ টাস্ক `#{i}` পজ করা হয়েছে।",
        'task_resume': "▶️ টাস্ক `#{i}` চালু করা হয়েছে।",
        'task_del': "🗑️ টাস্ক `#{i}` ডিলিট করা হয়েছে।",
        'task_nf': "❌ টাস্ক পাওয়া যায়নি।",
        'chs': "📢 চ্যানেল:\n",
        'no_ch': "❌ কোনো চ্যানেল নেই।",
        'stats': "📊 **তোমার পরিসংখ্যান**\n👤 ID: `{id}`\n🌐 {lang}\n📋 টাস্ক: {t}\n✅ সক্রিয়: {a}\n📢 চ্যানেল: {c}",
        'help': "🤖 **HBX Auto Scheduler**\n/start — শুরু\n/tasks — টাস্ক\n/pause <id> — পজ\n/resume <id> — চালু\n/delete <id> — ডিলিট\n/channels — চ্যানেল\n/stats — পরিসংখ্যান\n/lang — ভাষা\n/help — সাহায্য\n/panel — ওনার প্যানেল",
        'panel': "👑 **Owner Panel**\n\nচলমান শিডিউলার: {s}",
        'broadcast_ask': "📢 ব্রডকাস্ট মেসেজ লিখো:",
        'broadcast_done': "✅ ব্রডকাস্ট সম্পন্ন!\n{s}/{t} ইউজারে পৌঁছেছে।",
        'err': "⚠️ সার্ভার এরর!",
        'err_int': "❌ {min}-{max} সেকেন্ডের মধ্যে দাও।",
    },
    'en': {
        'welcome': "⚡ **HBX Auto Scheduler** ⚡\n\n👋 Welcome! Send Bot Token or use menu below.",
        'send_token': "🔑 Send Bot Token:\n`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`",
        'token_ok': "🟢 Token Valid! ✅\nBot: `{n}` @{u}\n\nAdd bot as admin in channel,\nthen forward a post.",
        'token_bad': "❌ Invalid token!\n{e}\nTry again.",
        'post_ok': "🎨 Post Saved! ✅\n\nSelect interval:",
        'done': "🎉 Schedule Ready! ✅\nTask `#{i}` — posting every `{s}` seconds.",
        'lang': "🌐 Select Language:",
        'lang_set': "✅ Language set: {l}",
        'banned': "❌ You are banned.",
        'owner_only': "⛔ Owner only.",
        'tasks': "📋 Your Tasks:\n",
        'no_task': "❌ No tasks.",
        'task_pause': "⏸️ Task `#{i}` paused.",
        'task_resume': "▶️ Task `#{i}` resumed.",
        'task_del': "🗑️ Task `#{i}` deleted.",
        'task_nf': "❌ Task not found.",
        'chs': "📢 Channels:\n",
        'no_ch': "❌ No channels.",
        'stats': "📊 **Your Stats**\n👤 ID: `{id}`\n🌐 {lang}\n📋 Tasks: {t}\n✅ Active: {a}\n📢 Channels: {c}",
        'help': "🤖 **HBX Auto Scheduler**\n/start — Start\n/tasks — Tasks\n/pause <id> — Pause\n/resume <id> — Resume\n/delete <id> — Delete\n/channels — Channels\n/stats — Stats\n/lang — Language\n/help — Help\n/panel — Owner Panel",
        'panel': "👑 **Owner Panel**\n\nActive schedulers: {s}",
        'broadcast_ask': "📢 Send broadcast message:",
        'broadcast_done': "✅ Broadcast Complete!\nReached {s}/{t} users.",
        'err': "⚠️ Server error!",
        'err_int': "❌ Enter between {min}-{max} seconds.",
    }
}

def txt(k, uid, **kw):
    l = db.get_lang(uid)
    s = S.get(l, S['bn']).get(k, S['bn'].get(k, k))
    return s.format(**kw) if kw else s

# ---- Keyboards ----
def kb_lang():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🇧🇩 বাংলা","lang_bn"),InlineKeyboardButton("🇺🇸 English","lang_en")]])
def kb_main():
    return InlineKeyboardMarkup([[InlineKeyboardButton("📋 Tasks","menu_tasks"),InlineKeyboardButton("📢 Channels","menu_chs")],[InlineKeyboardButton("📊 Stats","menu_stats"),InlineKeyboardButton("🌐 Lang","menu_lang")],[InlineKeyboardButton("❓ Help","menu_help")]])
def kb_int():
    return InlineKeyboardMarkup([[InlineKeyboardButton("5 min","int_300"),InlineKeyboardButton("15 min","int_900")],[InlineKeyboardButton("30 min","int_1800"),InlineKeyboardButton("1 hour","int_3600")],[InlineKeyboardButton("6 hours","int_21600"),InlineKeyboardButton("12 hours","int_43200")],[InlineKeyboardButton("24 hours","int_86400"),InlineKeyboardButton("✏️ Custom","int_custom")]])
def kb_owner():
    return InlineKeyboardMarkup([[InlineKeyboardButton("📢 Broadcast","own_brd"),InlineKeyboardButton("👥 Users","own_usr")],[InlineKeyboardButton("📊 Sys Stats","own_sts"),InlineKeyboardButton("🔄 Refresh","own_ref")]])

# ---- Scheduler (FIXED) ----
async def scheduler(tok, fc, tc, mi, iv, tid):
    client_bot = Bot(token=tok)
    key = str(tid)
    try:
        while True:
            try:
                await client_bot.copy_message(chat_id=tc, from_chat_id=fc, message_id=mi)
                db.inc_post(tid)
                logger.info(f"✅ #{tid}: Posted to {tc}")
            except Exception as e:
                logger.error(f"❌ #{tid}: {e}")
                if "chat not found" in str(e).lower() or "not enough rights" in str(e).lower():
                    break
            await asyncio.sleep(iv)
    except asyncio.CancelledError:
        logger.info(f"⏹️ #{tid} cancelled")
    finally:
        active_schedulers.pop(key, None)

# ---- Handlers ----
async def start(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return await upd.message.reply_text(txt('banned', u.id))
    db.reg_user(u.id, u.username or '', u.first_name or '')
    await upd.message.reply_text(txt('welcome', u.id), reply_markup=kb_main())
    if db.get_bot(u.id):
        await upd.message.reply_text("✅ বট কানেক্টেড আছে! পোস্ট ফরোয়ার্ড করো।")
        ctx.user_data['step'] = 'post'
    else:
        await upd.message.reply_text(txt('send_token', u.id))
        ctx.user_data['step'] = 'token'

async def msg_h(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    s = ctx.user_data.get('step','token')
    
    if s == 'token':
        tok = upd.message.text.strip()
        if ':' not in tok or len(tok) < 20:
            return await upd.message.reply_text("❌ ফরম্যাট ভুল! `123456:ABC-DEF...`")
        await upd.message.reply_text("⏳ ভ্যালিডেট হচ্ছে...")
        try:
            t = Bot(token=tok)
            m = await t.get_me()
            db.save_bot(u.id, tok, m.username or '', m.first_name or '')
            await upd.message.reply_text(txt('token_ok', u.id, n=m.first_name, u=m.username))
            ctx.user_data['step'] = 'post'
        except InvalidToken:
            await upd.message.reply_text(txt('token_bad', u.id, e="Invalid token"))
        except Exception as e:
            await upd.message.reply_text(txt('token_bad', u.id, e=str(e)))
    
    elif s == 'post' and upd.message.forward_from_chat:
        fc = upd.message.forward_from_chat.id
        ct = upd.message.forward_from_chat.title or ''
        cu = upd.message.forward_from_chat.username or ''
        db.add_ch(u.id, fc, ct, cu)
        ctx.user_data['fc'] = fc
        ctx.user_data['mid'] = upd.message.message_id
        await upd.message.reply_text(txt('post_ok', u.id), reply_markup=kb_int())
        ctx.user_data['step'] = 'int'
    
    elif s == 'int' and upd.message.text:
        try:
            iv = int(upd.message.text.strip())
            if iv < 10 or iv > 864000: return await upd.message.reply_text(txt('err_int', u.id, min=10, max=864000))
            tok = db.get_bot(u.id)
            fc = ctx.user_data.get('fc')
            mi = ctx.user_data.get('mid')
            if not tok or not fc or not mi: return
            tid = db.save_task(u.id, tok, fc, u.id, mi, iv)
            task = asyncio.create_task(scheduler(tok, fc, u.id, mi, iv, tid))
            active_schedulers[f"{u.id}_{tid}"] = task
            await upd.message.reply_text(txt('done', u.id, i=tid, s=iv))
            ctx.user_data.clear()
        except: await upd.message.reply_text("❌ সংখ্যা দাও।")

async def cb(upd, ctx):
    q = upd.callback_query; await q.answer(); u = q.from_user; d = q.data
    
    if d.startswith('lang_'):
        l = d.split('_')[1]; db.set_lang(u.id, l)
        await q.edit_message_text(txt('lang_set', u.id, l='বাংলা' if l=='bn' else 'English'))
    
    elif d.startswith('int_'):
        if d == 'int_custom':
            await q.edit_message_text(f"✏️ সেকেন্ড লিখো (10-864000):")
            ctx.user_data['step'] = 'int'; return
        iv = int(d.split('_')[1])
        tok = db.get_bot(u.id)
        fc = ctx.user_data.get('fc'); mi = ctx.user_data.get('mid')
        if not tok or not fc or not mi: return
        tid = db.save_task(u.id, tok, fc, u.id, mi, iv)
        task = asyncio.create_task(scheduler(tok, fc, u.id, mi, iv, tid))
        active_schedulers[f"{u.id}_{tid}"] = task
        await q.edit_message_text(txt('done', u.id, i=tid, s=iv))
        ctx.user_data.clear()
    
    elif d == 'menu_tasks':
        ts = db.get_tasks(u.id)
        if not ts: return await q.edit_message_text(txt('no_task', u.id), reply_markup=kb_main())
        m = txt('tasks', u.id)
        for t in ts[:5]:
            m += f"{'✅' if t[3] else '⏸️'} `{t[0]}` → `{t[1]}` | {t[2]}s | {t[4]} posts\n"
        await q.edit_message_text(m, reply_markup=kb_main())
    
    elif d == 'menu_chs':
        chs = db.get_chs(u.id)
        if not chs: return await q.edit_message_text(txt('no_ch', u.id), reply_markup=kb_main())
        m = txt('chs', u.id)
        for c in chs[:5]: m += f"📢 `{c[0]}` — {c[1] or 'Unknown'}\n"
        await q.edit_message_text(m, reply_markup=kb_main())
    
    elif d == 'menu_stats':
        ts = db.get_tasks(u.id); chs = db.get_chs(u.id)
        l = db.get_lang(u.id); ac = sum(1 for t in ts if t[3])
        await q.edit_message_text(txt('stats', u.id, id=u.id, lang='বাংলা' if l=='bn' else 'English', t=len(ts), a=ac, c=len(chs)), reply_markup=kb_main())
    
    elif d == 'menu_lang': await q.edit_message_text(txt('lang', u.id), reply_markup=kb_lang())
    elif d == 'menu_help': await q.edit_message_text(txt('help', u.id), reply_markup=kb_main())
    
    elif d.startswith('own_'):
        if u.id != SYSTEM_OWNER_ID: return await q.edit_message_text(txt('owner_only', u.id))
        cmd = d.split('_')[1]
        if cmd == 'brd':
            await q.edit_message_text(txt('broadcast_ask', u.id))
            ctx.user_data['broadcast'] = True
        elif cmd == 'usr':
            us = db.all_users()
            m = f"👥 **Users: {len(us)}**\n\n"
            for uu in us[:25]:
                m += f"{'🚫' if uu[4] else '✅'} `{uu[0]}` — {uu[1] or uu[2] or str(uu[0])} [{uu[3].upper()}]\n"
            await q.edit_message_text(m, reply_markup=kb_owner())
        elif cmd == 'sts':
            s = db.sys_stats()
            await q.edit_message_text(f"📊 **System**\n👥 {s['users']} | 🤖 {s['bots']} | 📋 {s['tasks']}\n✅ {s['active']} | 📤 {s['posts']} | 📢 {s['chs']}\n🚫 {s['banned']} | ⚡ {len(active_schedulers)}", reply_markup=kb_owner())
        elif cmd == 'ref':
            await q.edit_message_text(txt('panel', u.id, s=len(active_schedulers)), reply_markup=kb_owner())

async def cmd_tasks(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    ts = db.get_tasks(u.id)
    if not ts: return await upd.message.reply_text(txt('no_task', u.id))
    m = txt('tasks', u.id)
    for t in ts: m += f"{'✅' if t[3] else '⏸️'} `{t[0]}` → `{t[1]}` | {t[2]}s | {t[4]} posts\n"
    await upd.message.reply_text(m)

async def cmd_pause(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    if not ctx.args: return await upd.message.reply_text("`/pause <id>`")
    try:
        tid = int(ctx.args[0]); t = db.get_task(tid)
        if not t or t[1] != u.id: return await upd.message.reply_text(txt('task_nf', u.id))
        k = f"{u.id}_{tid}"
        if k in active_schedulers: active_schedulers[k].cancel(); del active_schedulers[k]
        db.toggle_task(tid, False)
        await upd.message.reply_text(txt('task_pause', u.id, i=tid))
    except: await upd.message.reply_text("❌ ভুল আইডি")

async def cmd_resume(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    if not ctx.args: return await upd.message.reply_text("`/resume <id>`")
    try:
        tid = int(ctx.args[0]); t = db.get_task(tid)
        if not t or t[1] != u.id: return await upd.message.reply_text(txt('task_nf', u.id))
        k = f"{u.id}_{tid}"
        tsk = asyncio.create_task(scheduler(t[2], t[3], t[4], t[5], t[6], tid))
        active_schedulers[k] = tsk
        db.toggle_task(tid, True)
        await upd.message.reply_text(txt('task_resume', u.id, i=tid))
    except: await upd.message.reply_text("❌ ভুল আইডি")

async def cmd_del(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    if not ctx.args: return await upd.message.reply_text("`/delete <id>`")
    try:
        tid = int(ctx.args[0]); t = db.get_task(tid)
        if not t or t[1] != u.id: return await upd.message.reply_text(txt('task_nf', u.id))
        k = f"{u.id}_{tid}"
        if k in active_schedulers: active_schedulers[k].cancel(); del active_schedulers[k]
        db.del_task(tid)
        await upd.message.reply_text(txt('task_del', u.id, i=tid))
    except: await upd.message.reply_text("❌ ভুল আইডি")

async def cmd_chs(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    chs = db.get_chs(u.id)
    if not chs: return await upd.message.reply_text(txt('no_ch', u.id))
    m = txt('chs', u.id)
    for c in chs: m += f"📢 `{c[0]}` — {c[1] or 'Unknown'}\n"
    await upd.message.reply_text(m)

async def cmd_stats(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    ts = db.get_tasks(u.id); chs = db.get_chs(u.id)
    l = db.get_lang(u.id); ac = sum(1 for t in ts if t[3])
    await upd.message.reply_text(txt('stats', u.id, id=u.id, lang='বাংলা' if l=='bn' else 'English', t=len(ts), a=ac, c=len(chs)))

async def cmd_help(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    await upd.message.reply_text(txt('help', u.id))

async def cmd_lang(upd, ctx):
    u = upd.effective_user
    if db.is_banned(u.id): return
    await upd.message.reply_text(txt('lang', u.id), reply_markup=kb_lang())

async def cmd_panel(upd, ctx):
    u = upd.effective_user
    if u.id != SYSTEM_OWNER_ID: return await upd.message.reply_text("⛔ Access Denied")
    await upd.message.reply_text(txt('panel', u.id, s=len(active_schedulers)), reply_markup=kb_owner())

async def broadcast_h(upd, ctx):
    u = upd.effective_user
    if u.id != SYSTEM_OWNER_ID or not ctx.user_data.get('broadcast'): return
    msg = upd.message.text; us = db.all_users()
    suc, tot = 0, len(us)
    st = await upd.message.reply_text(f"📢 0/{tot}")
    for i, uu in enumerate(us):
        try: await ctx.bot.send_message(chat_id=uu[0], text=msg); suc += 1
        except: pass
        if i % 10 == 0: await st.edit_text(f"📢 {i}/{tot}")
        await asyncio.sleep(0.05)
    await st.edit_text(txt('broadcast_done', u.id, s=suc, t=tot))
    ctx.user_data['broadcast'] = False

async def err_h(upd, ctx):
    logger.error(f"Error: {ctx.error}")
    if upd and upd.effective_message:
        try: await upd.effective_message.reply_text(txt('err', upd.effective_user.id))
        except: pass

def build():
    app = ApplicationBuilder().token(MAIN_BOT_TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", cmd_tasks))
    app.add_handler(CommandHandler("pause", cmd_pause))
    app.add_handler(CommandHandler("resume", cmd_resume))
    app.add_handler(CommandHandler("delete", cmd_del))
    app.add_handler(CommandHandler("channels", cmd_chs))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("lang", cmd_lang))
    app.add_handler(CommandHandler("panel", cmd_panel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg_h))
    app.add_handler(MessageHandler(filters.FORWARDED, msg_h))
    app.add_handler(CallbackQueryHandler(cb))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_h))
    app.add_error_handler(err_h)
    return app

def main():
    logger.info("🤖 HBX Bot starting...")
    build().run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: logger.info("⏹️ Stopped")
