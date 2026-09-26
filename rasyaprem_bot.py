#!/usr/bin/env python3
# ============================================
#   RASYAPREM BOT
#   Dev: Rasya
#   Versi: V1.5.0
# ============================================

import os
import sys
import time
import logging
import requests
from datetime import datetime
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# ============================================
#   CONFIG
# ============================================
BOT_TOKEN = "8945124140:AAFt3J8lySAIF4honGXpI55_4wM4dXbtpP8"
API_KEY = "FREE"
ENDPOINT_SEND = "https://am.dapjisync.my.id/api/send"
ENDPOINT_VERIF = "https://am.dapjisync.my.id/api/verif"

BOT_NAME = "RASYAPREM"
BOT_VERSION = "V1.5.0"

FOUNDER_ID = 8760859678

USER_FILE = "users.txt"
LIST_FILE = "list_prem.txt"

START_TIME = time.time()

MAINTENANCE = False
MAINTENANCE_MSG = "Bot sedang dalam perbaikan. Coba lagi nanti."

# ============================================
#   LOGGING
# ============================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

user_state = {}


# ============================================
#   FUNGSI UTIL
# ============================================
def load_users():
    if not os.path.exists(USER_FILE):
        return set()
    with open(USER_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_user(user_id):
    users = load_users()
    if str(user_id) not in users:
        users.add(str(user_id))
        with open(USER_FILE, "a") as f:
            f.write(f"{user_id}\n")


def total_users():
    return len(load_users())


def get_tier(user_id):
    if user_id == FOUNDER_ID:
        return "Founder"
    return "User"


def is_founder(user_id):
    return user_id == FOUNDER_ID


def format_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    return f"{days}d {hours}h {minutes}m"


def simpan_ke_list(email, status="PREMIUM"):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LIST_FILE, "a") as f:
        f.write(f"{waktu}|{email}|{status}\n")


def baca_list():
    if not os.path.exists(LIST_FILE):
        return []
    data = []
    with open(LIST_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            bagian = line.split("|")
            if len(bagian) == 3:
                data.append({
                    "waktu": bagian[0],
                    "email": bagian[1],
                    "status": bagian[2],
                })
    return data


def get_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📧 Gmail", callback_data="menu_gmail"),
            InlineKeyboardButton("📬 Temp Mail", callback_data="menu_temp"),
        ],
        [
            InlineKeyboardButton("📊 List Premium", callback_data="menu_list"),
            InlineKeyboardButton("📈 Statistik", callback_data="menu_stat"),
        ],
        [
            InlineKeyboardButton("ℹ️ Info", callback_data="menu_info"),
            InlineKeyboardButton("📞 Kontak Dev", callback_data="menu_dev"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_tampilan_start(update: Update):
    user = update.effective_user
    user_id = user.id
    username = user.username
    name = user.first_name

    save_user(user_id)
    tier = get_tier(user_id)

    if username:
        nama_tampil = f"@{username}"
    else:
        nama_tampil = name

    pesan = (
        f'<b>Bot Information</b> ❞\n'
        f'⬡ Name : {BOT_NAME}\n'
        f'⬡ Version : {BOT_VERSION}\n'
        f'⬡ Uptime : {format_uptime()}\n'
        f'⬡ Total User : {total_users()}\n'
        f'\n'
        f'<b>User Information</b> ❞\n'
        f'⬡ Name : {nama_tampil}\n'
        f'⬡ Tier : {tier}\n'
        f'\n'
        f'Silakan pilih salah satu menu di bawah\n'
        f'untuk melanjutkan.'
    )
    return pesan


# ============================================
#   COMMAND: /start
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if MAINTENANCE and not is_founder(user_id):
        await update.message.reply_text(
            f"⚙️ *MAINTENANCE*\n\n"
            f"{MAINTENANCE_MSG}\n\n"
            f"Silakan coba lagi nanti.",
            parse_mode="Markdown",
        )
        return

    pesan = get_tampilan_start(update)
    keyboard = get_menu_keyboard()

    await update.message.reply_text(
        pesan,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ============================================
#   CALLBACK HANDLER
# ============================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if MAINTENANCE and not is_founder(user_id):
        await query.message.reply_text(
            f"⚙️ *MAINTENANCE*\n\n{MAINTENANCE_MSG}",
            parse_mode="Markdown",
        )
        return

    if data == "menu_gmail":
        user_state[user_id] = {"mode": "gmail", "email": None}
        await query.message.reply_text(
            "📧 *KIRIM EMAIL ANDA*\n\n"
            "Silakan kirim email Gmail kamu.\n"
            "Hanya bisa *@gmail.com*\n\n"
            "Contoh:\n"
            "`target@gmail.com`",
            parse_mode="Markdown",
        )

    elif data == "menu_temp":
        user_state[user_id] = {"mode": "temp", "email": None}
        await query.message.reply_text(
            "📬 *KIRIM EMAIL ANDA*\n\n"
            "Silakan kirim email Temp Mail kamu.\n"
            "Domain apapun bisa.\n\n"
            "Contoh:\n"
            "`user@mail.tm`",
            parse_mode="Markdown",
        )

    elif data == "menu_list":
        data_list = baca_list()

        if not data_list:
            await query.message.reply_text(
                "📊 *LIST PREMIUM*\n\n"
                "Belum ada list tersimpan.",
                parse_mode="Markdown",
            )
            return

        teks = "📊 *LIST PREMIUM*\n\n"
        for i, item in enumerate(data_list[-10:], 1):
            teks += f"{i}. `{item['email']}`\n"
            teks += f"   📅 {item['waktu']}\n\n"

        teks += f"━━━━━━━━━━━━━━━━━━━\n"
        teks += f"Total: *{len(data_list)}* email"

        await query.message.reply_text(teks, parse_mode="Markdown")

    elif data == "menu_stat":
        data_list = baca_list()
        hari_ini = datetime.now().strftime("%Y-%m-%d")
        count_hari_ini = sum(1 for x in data_list if x["waktu"].startswith(hari_ini))

        teks = (
            "📈 *STATISTIK*\n\n"
            f"Hari ini  : {count_hari_ini}\n"
            f"Total     : {len(data_list)}\n"
            f"Total User: {total_users()}\n"
            f"\n"
            f"Bot: {BOT_NAME}\n"
            f"Versi: {BOT_VERSION}\n"
            f"Uptime: {format_uptime()}"
        )
        await query.message.reply_text(teks, parse_mode="Markdown")

    elif data == "menu_info":
        teks = (
            f"ℹ️ *{BOT_NAME}*\n\n"
            f"Versi: {BOT_VERSION}\n"
            f"Dev: Rasya\n"
            f"Uptime: {format_uptime()}\n"
            f"Total User: {total_users()}\n\n"
            f"*Fitur:*\n"
            f"✅ Kirim link ke Gmail\n"
            f"✅ Kirim link ke Temp Mail\n"
            f"✅ Auto-verifikasi\n"
            f"✅ List premium\n\n"
            f"⚠️ Tools ini *TIDAK diperjualbelikan*"
        )
        await query.message.reply_text(teks, parse_mode="Markdown")

    elif data == "menu_dev":
        teks = (
            "📞 *KONTAK DEVELOPER*\n\n"
            "📱 WhatsApp:\n"
            "wa.me/6281549357354\n\n"
            "📧 GitHub:\n"
            "github.com/no3081646-cmd\n\n"
            "💬 Ada pertanyaan? Chat aja!"
        )
        await query.message.reply_text(teks, parse_mode="Markdown")


# ============================================
#   HANDLER PESAN BIASA
# ============================================
async def pesan_biasa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    teks = update.message.text.strip()

    if MAINTENANCE and not is_founder(user_id):
        await update.message.reply_text(
            f"⚙️ *MAINTENANCE*\n\n{MAINTENANCE_MSG}",
            parse_mode="Markdown",
        )
        return

    # ===== KALO ADA LINK =====
    if "http" in teks.lower():
        if user_id not in user_state or not user_state[user_id].get("email"):
            await update.message.reply_text(
                "❌ Kamu belum masukkan email!\n\n"
                "Tekan tombol *📧 Gmail* atau *📬 Temp Mail* dulu.",
                parse_mode="Markdown",
            )
            return

        email = user_state[user_id]["email"]
        idx = teks.lower().find("http")
        link = teks[idx:].strip()

        await update.message.reply_text("⏳ Memverifikasi link...")

        try:
            requests.post(
                ENDPOINT_VERIF,
                json={"gmail": email, "link": link},
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": API_KEY,
                },
                timeout=30,
            )

            simpan_ke_list(email, "PREMIUM")
            del user_state[user_id]

            await update.message.reply_text(
                f"✅ *Verifikasi Berhasil!*\n\n"
                f"📧 Email: `{email}`\n"
                f"💎 Premium 1 tahun aktif!\n\n"
                f"🎬 Buka Alight Motion sekarang!",
                parse_mode="Markdown",
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Gagal: {e}")

        return

    # ===== MODE INPUT EMAIL =====
    if user_id in user_state:
        mode = user_state[user_id]["mode"]

        if mode == "gmail":
            if not teks.endswith("@gmail.com"):
                await update.message.reply_text(
                    "❌ *MENU INI KHUSUS GMAIL.COM*\n\n"
                    "Kirim email kamu dengan format:\n"
                    "`target@gmail.com`",
                    parse_mode="Markdown",
                )
                return

            email = teks.lower()
            user_state[user_id]["email"] = email

            await update.message.reply_text(f"⏳ Mengirim link ke {email}...")

            try:
                requests.post(
                    ENDPOINT_SEND,
                    json={"gmail": email},
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": API_KEY,
                    },
                    timeout=30,
                )

                await update.message.reply_text(
                    f"✅ *Link terkirim ke {email}*\n\n"
                    f"📬 *Langkah selanjutnya:*\n"
                    f"1. Cek inbox / folder spam\n"
                    f"2. Buka email dari Alight Motion\n"
                    f"3. *Copy link verifikasi*\n"
                    f"4. *Kirim link tersebut ke bot ini*\n\n"
                    f"💡 Tinggal paste link-nya di chat ini!",
                    parse_mode="Markdown",
                )
            except Exception as e:
                await update.message.reply_text(f"❌ Gagal: {e}")

            return

        elif mode == "temp":
            if "@" not in teks or "." not in teks.split("@")[-1]:
                await update.message.reply_text(
                    "❌ Format email tidak valid!\n\n"
                    "Contoh:\n"
                    "`user@mail.tm`",
                    parse_mode="Markdown",
                )
                return

            email = teks.lower()
            user_state[user_id]["email"] = email

            await update.message.reply_text(f"⏳ Mengirim link ke {email}...")

            try:
                requests.post(
                    ENDPOINT_SEND,
                    json={"gmail": email},
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": API_KEY,
                    },
                    timeout=30,
                )

                await update.message.reply_text(
                    f"✅ *Link terkirim ke {email}*\n\n"
                    f"📬 *Langkah selanjutnya:*\n"
                    f"1. Buka inbox temp mail\n"
                    f"2. Buka email dari Alight Motion\n"
                    f"3. *Copy link verifikasi*\n"
                    f"4. *Kirim link tersebut ke bot ini*\n\n"
                    f"💡 Tinggal paste link-nya di chat ini!",
                    parse_mode="Markdown",
                )
            except Exception as e:
                await update.message.reply_text(f"❌ Gagal: {e}")

            return

    await update.message.reply_text(
        "❓ *Perintah tidak dikenal*\n\n"
        "Tekan /start dulu,\n"
        "lalu pilih menu dari tombol yang muncul.",
        parse_mode="Markdown",
    )


# ============================================
#   COMMAND: /help
# ============================================
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        "📖 *CARA PAKE BOT*\n\n"
        "*1. Kirim link ke Gmail:*\n"
        "→ Tekan tombol 📧 Gmail\n"
        "→ Kirim email Gmail kamu\n"
        "→ Cek inbox, copy link\n"
        "→ Paste link di bot\n\n"
        "*2. Kirim link ke Temp Mail:*\n"
        "→ Tekan tombol 📬 Temp Mail\n"
        "→ Kirim email temp kamu\n"
        "→ Cek inbox, copy link\n"
        "→ Paste link di bot\n\n"
        "*3. Kontak developer:*\n"
        "wa.me/6281549357354"
    )
    await update.message.reply_text(pesan, parse_mode="Markdown")


# ============================================
#   COMMAND: /ping
# ============================================
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_t = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    end_t = time.time()
    response = round((end_t - start_t) * 1000, 2)

    await msg.edit_text(
        f"🏓 *Pong!*\n\n"
        f"Response: `{response} ms`\n"
        f"Uptime: `{format_uptime()}`",
        parse_mode="Markdown",
    )


# ============================================
#   FOUNDER COMMANDS
# ============================================
async def founder_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_founder(user_id):
        await update.message.reply_text("❌ Akses ditolak!")
        return

    data_list = baca_list()
    hari_ini = datetime.now().strftime("%Y-%m-%d")
    count_hari_ini = sum(1 for x in data_list if x["waktu"].startswith(hari_ini))
    status_maint = "🟢 OFF" if not MAINTENANCE else "🔴 ON"

    teks = (
        f"👑 *FOUNDER PANEL*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📛 Name : @{update.effective_user.username or 'Founder'}\n"
        f"🆔 ID   : `{user_id}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 *STATISTIK*\n\n"
        f"👥 Total User     : {total_users()}\n"
        f"💎 Total Premium  : {len(data_list)}\n"
        f"📅 Premium Hari Ini: {count_hari_ini}\n"
        f"⏱️ Uptime         : {format_uptime()}\n"
        f"⚙️ Maintenance    : {status_maint}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛠️ *MENU FOUNDER*\n\n"
        f"📢 /broadcast — Kirim ke semua user\n"
        f"⚙️ /maintenance — Aktifin maintenance\n"
        f"✅ /offmaintenance — Matiin maintenance\n"
        f"👑 /founder — Panel ini"
    )
    await update.message.reply_text(teks, parse_mode="Markdown")


async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_founder(user_id):
        await update.message.reply_text("❌ Akses ditolak!")
        return

    if not context.args:
        await update.message.reply_text(
            "📢 *CARA PAKE BROADCAST*\n\n"
            "`/broadcast <pesan kamu>`\n\n"
            "Contoh:\n"
            "`/broadcast Halo semua!`",
            parse_mode="Markdown",
        )
        return

    pesan = " ".join(context.args)
    users = load_users()

    await update.message.reply_text(f"📢 Mengirim ke {len(users)} user...")

    berhasil = 0
    gagal = 0

    for uid in users:
        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"📢 *BROADCAST dari {BOT_NAME}*\n\n{pesan}",
                parse_mode="Markdown",
            )
            berhasil += 1
        except Exception:
            gagal += 1

    await update.message.reply_text(
        f"✅ *BROADCAST SELESAI*\n\n"
        f"📤 Berhasil : {berhasil}\n"
        f"❌ Gagal    : {gagal}\n"
        f"👥 Total    : {len(users)} user",
        parse_mode="Markdown",
    )


async def maintenance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MAINTENANCE
    user_id = update.effective_user.id

    if not is_founder(user_id):
        await update.message.reply_text("❌ Akses ditolak!")
        return

    MAINTENANCE = True
    await update.message.reply_text(
        "⚙️ *MAINTENANCE: ON*\n\n"
        "Bot dalam mode maintenance.\n"
        "User biasa tidak bisa akses.\n\n"
        "Matikan: `/offmaintenance`",
        parse_mode="Markdown",
    )


async def offmaintenance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MAINTENANCE
    user_id = update.effective_user.id

    if not is_founder(user_id):
        await update.message.reply_text("❌ Akses ditolak!")
        return

    MAINTENANCE = False
    await update.message.reply_text(
        "✅ *MAINTENANCE: OFF*\n\n"
        "Bot sudah normal kembali.",
        parse_mode="Markdown",
    )


# ============================================
#   MAIN
# ============================================
def main():
    print("=" * 50)
    print(f"  {BOT_NAME} {BOT_VERSION}")
    print("=" * 50)
    print()

    try:
        print("[1] Membuat aplikasi bot...")
        app = Application.builder().token(BOT_TOKEN).build()
        print("[2] Aplikasi dibuat ✅")

        print("[3] Daftarkan handler...")
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_cmd))
        app.add_handler(CommandHandler("ping", ping_cmd))
        app.add_handler(CommandHandler("founder", founder_cmd))
        app.add_handler(CommandHandler("broadcast", broadcast_cmd))
        app.add_handler(CommandHandler("maintenance", maintenance_cmd))
        app.add_handler(CommandHandler("offmaintenance", offmaintenance_cmd))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pesan_biasa))
        print("[4] Handler didaftarkan ✅")

        print()
        print(f"🤖 {BOT_NAME} {BOT_VERSION} JALAN!")
        print(f"👑 Founder ID: {FOUNDER_ID}")
        print("⏹️  Tekan CTRL + C buat stop")
        print()

        app.run_polling()

    except Exception as e:
        print()
        print("❌ ERROR TERJADI:")
        print("=" * 50)
        print(f"Tipe  : {type(e).__name__}")
        print(f"Pesan : {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
