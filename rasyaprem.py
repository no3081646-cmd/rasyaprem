#!/usr/bin/env python3
# ============================================
#   RASYAPREM v1.2
#   Dev: Rasya
# ============================================

import os
import sys
import time
import requests
from datetime import datetime

# ==== CONFIG ====
API_KEY = "FREE"
ENDPOINT_SEND = "https://am.dapjisync.my.id/api/send"
ENDPOINT_VERIF = "https://am.dapjisync.my.id/api/verif"

LIST_FILE = "list_prem.txt"

# ==== WARNA ====
R = "\033[0;31m"
G = "\033[0;32m"
Y = "\033[1;33m"
C = "\033[0;36m"
M = "\033[0;35m"
W = "\033[1;37m"
P = "\033[1;35m"
NC = "\033[0m"

TEMP_EMAIL = ""


def clear():
    os.system("clear")


def garis(panjang=60, warna=P, char="="):
    print(f"{warna}{char * panjang}{NC}")


def pause():
    input(f"\n{C}  Tekan Enter untuk lanjut...{NC}")


# ============================================
#   ANIMASI
# ============================================
def typing(text, delay=0.04, color=""):
    for ch in text:
        sys.stdout.write(color + ch + NC)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def loading(text="Loading", durasi=1.5):
    end = time.time() + durasi
    i = 0
    while time.time() < end:
        dots = "." * (i % 4)
        sys.stdout.write(f"\r{C}  {text}{dots}   {NC}")
        sys.stdout.flush()
        time.sleep(0.15)
        i += 1
    print()


# ============================================
#   SPLASH SCREEN
# ============================================
def splash_screen():
    clear()

    print()
    loading("  Menyalakan sistem", 1.0)
    loading("  Memuat komponen", 0.9)
    loading("  Menghubungkan server", 1.0)
    clear()

    # ---- Logo ASCII RASYAPREM ----
    logo = [
        "  ██████╗  █████╗ ███████╗██╗   ██╗ █████╗ ",
        "  ██╔══██╗██╔══██╗██╔════╝╚██╗ ██╔╝██╔══██╗",
        "  ██████╔╝███████║███████╗ ╚████╔╝ ███████║",
        "  ██╔══██╗██╔══██║╚════██║  ╚██╔╝  ██╔══██║",
        "  ██║  ██║██║  ██║███████║   ██║   ██║  ██║",
        "  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝",
    ]

    print()
    for line in logo:
        print(f"{P}{line}{NC}")
        time.sleep(0.07)

    print()
    time.sleep(0.3)


    # ---- Flicker "RASYAPREM v1.2" ----
    frames = [
        f"{Y}         R A S Y A P R E M   v 1 . 2{NC}",
        f"{C}         R A S Y A P R E M   v 1 . 2{NC}",
        f"{M}         R A S Y A P R E M   v 1 . 2{NC}",
        f"{R}         R A S Y A P R E M   v 1 . 2{NC}",
        f"{W}         R A S Y A P R E M   v 1 . 2{NC}",
    ]

    for _ in range(4):
        for f in frames:
            sys.stdout.write(f"\r{f}")
            sys.stdout.flush()
            time.sleep(0.08)

    print()
    print()
    garis(60, P)
    typing("           By Rasya", delay=0.06, color=f"{W}")
    garis(60, P)

    print()
    print(f"{G}  [OK] Sistem siap!{NC}")
    time.sleep(0.8)
    print(f"{Y}  [i] Membuka menu utama...{NC}")
    time.sleep(1.2)


# ============================================
#   SIMPAN / BACA LIST PREM
# ============================================
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
                    "status": bagian[2]
                })
    return data


# ============================================
#   HEADER
# ============================================
def header():
    clear()
    garis(60, P)
    print(f"{P}  RASYAPREM v1.2{NC}")
    print(f"{W}  Dev: Rasya{NC}")
    garis(60, P)
    print()
    print(f"{R}  W A R N I N G  !!{NC}")
    print(f"{R}  Tools ini tidak diperjualbelikan{NC}")
    print(f"{R}  Kalau ada yang memperjualbelikan{NC}")
    print(f"{R}  harap lapor ke developer.{NC}")
    print(f"{R}  Mohon diperhatikan.{NC}")
    print()
    garis(60, P)
    print(f"{M}  INFO RELEASE v1.2{NC}")
    print(f"{G}  NEW RELEASE:{NC}")
    print(f"  1. SPLASH SCREEN ANIMATION")
    print(f"  2. AUTO-SAVE LIST PREMIUM (REAL)")
    print(f"  3. FITUR CEK LIST AMPREM (LIVE)")
    print(f"  4. VALIDASI GMAIL & TEMP MAIL")
    print(f"{Y}  UNTUK INFO LENGKAP CHAT ME wa.me/6281549357354{NC}")
    garis(60, P)
    print()


# ============================================
#   MENU UTAMA
# ============================================
def menu_utama():
    header()

    print(f"{P}              RASYAPREM - MAIN MENU{NC}")
    print()
    print(f"{P}  +------------------------------------------------------+{NC}")
    print(f"{P}  |{NC}  1.  Masukan Email                                 {P}|{NC}")
    print(f"{P}  |{NC}  2.  Masukan Link Verifikasi                       {P}|{NC}")
    print(f"{P}  |{NC}  3.  Tentang / Info                                {P}|{NC}")
    print(f"{P}  |{NC}  4.  Cek List Amprem                               {P}|{NC}")
    print(f"{P}  |{NC}  5.  Masukan Email Temp Mail                       {P}|{NC}")
    print(f"{P}  |{NC}  6.  Hapus Semua List                              {P}|{NC}")
    print(f"{P}  |{NC}  0.  Keluar                                        {P}|{NC}")
    print(f"{P}  +------------------------------------------------------+{NC}")
    print()
    print(f"{P}  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{NC}")
    print()

    return input(f"{P}  > Pilih menu [0-6]: {NC}").strip()


# ============================================
#   STEP 1 - MASUKAN EMAIL (KHUSUS GMAIL.COM)
# ============================================
def masukan_email():
    global TEMP_EMAIL
    header()

    print(f"{P}              STEP 1 : MASUKAN EMAIL{NC}")
    print()
    print(f"{P}  +------------------------------------------------------+{NC}")
    print(f"{P}  |{NC}  Silakan masukkan Gmail kamu untuk                 {P}|{NC}")
    print(f"{P}  |{NC}  menerima link verifikasi dari server.             {P}|{NC}")
    print(f"{P}  |{NC}  {Y}(Hanya bisa @gmail.com){NC}                          {P}|{NC}")
    print(f"{P}  +------------------------------------------------------+{NC}")
    print()
    print(f"{P}  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{NC}")
    print()

    gmail = input(f"{P}  > Masukkan Gmail kamu: {NC}").strip().lower()

    if not gmail:
        print(f"\n{R}  [!] Gmail tidak boleh kosong!{NC}")
        pause()
        return

    if not gmail.endswith("@gmail.com"):
        clear()
        garis(60, R)
        print(f"{R}  [!] MENU INI KHUSUS GMAIL.COM{NC}")
        garis(60, R)
        print()
        print(f"{Y}  Email yang kamu masukkan:{NC} {gmail}")
        print(f"{Y}  Tidak valid untuk menu ini.{NC}")
        print()
        print(f"{C}  Silakan gunakan email @gmail.com")
        print(f"{C}  Atau gunakan menu Temp Mail")
        print(f"{C}  untuk domain selain gmail.com")
        print()
        input(f"{P}  Tekan Enter untuk otomatis ke menu Masukan Email Temp Mail...{NC}")

        temp_mail()
        return

    TEMP_EMAIL = gmail

    print()
    print(f"{Y}  [*] Mengirim link verifikasi ke {G}{gmail}{NC} ...")
    time.sleep(1.0)

    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }
        requests.post(ENDPOINT_SEND, json={"gmail": gmail}, headers=headers)
    except Exception as e:
        print(f"{R}  [!] Gagal: {e}{NC}")
        pause()
        return

    print()
    print(f"{G}  [OK] Link verifikasi berhasil dikirim!{NC}")
    print(f"{Y}  [i] Cek inbox atau folder spam Gmail kamu.{NC}")
    print()
    input(f"{C}  Tekan Enter untuk lanjut ke menu verifikasi...{NC}")

    print(f"{P}  > Otomatis beralih ke menu 2...{NC}")
    time.sleep(1.2)
    masukan_link()


# ============================================
#   STEP 2 - MASUKAN LINK VERIFIKASI
# ============================================
def masukan_link():
    global TEMP_EMAIL
    header()

    print(f"{P}              STEP 2 : VERIFIKASI LINK{NC}")
    print()
    print(f"{P}  +------------------------------------------------------+{NC}")
    print(f"{P}  |{NC}  Email tersimpan: {G}{TEMP_EMAIL or '(belum diisi)'}{NC}")
    print(f"{P}  |{NC}  Tempel link verifikasi dari Gmail kamu.           {P}|{NC}")
    print(f"{P}  +------------------------------------------------------+{NC}")
    print()
    print(f"{P}  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{NC}")
    print()

    if not TEMP_EMAIL:
        print(f"{R}  [!] Isi email dulu di menu 1 atau 5!{NC}")
        pause()
        return

    link = input(f"{P}  > Tempel link verifikasi: {NC}").strip()

    if not link:
        print(f"\n{R}  [!] Link tidak boleh kosong!{NC}")
        pause()
        return

    print()
    print(f"{Y}  [*] Memverifikasi link ...{NC}")
    time.sleep(1.5)

    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }
        res = requests.post(
            ENDPOINT_VERIF,
            json={"gmail": TEMP_EMAIL, "link": link},
            headers=headers
        )

        simpan_ke_list(TEMP_EMAIL, "PREMIUM")

        print()
        print(f"{G}  [OK] Verifikasi berhasil!{NC}")
        print(f"{G}  [OK] Premium 1 tahun aktif untuk {TEMP_EMAIL}{NC}")
        print(f"{G}  [OK] Tersimpan di list prem!{NC}")
    except Exception as e:
        print(f"{R}  [!] Gagal: {e}{NC}")

    pause()


# ============================================
#   MENU 3 - TENTANG / INFO
# ============================================
def tentang():
    header()
    print(f"{P}              TENTANG / INFO{NC}")
    print()
    print(f"  {W}Nama Script :{NC} RASYAPREM")
    print(f"  {W}Versi       :{NC} v1.2")
    print(f"  {W}Developer   :{NC} Rasya")
    print(f"  {W}Kontak      :{NC} wa.me/6281549357354")
    print()
    print(f"  {W}Fitur:{NC}")
    print(f"   - Splash screen animation")
    print(f"   - Kirim magic link ke Gmail")
    print(f"   - Verifikasi link premium")
    print(f"   - Auto-save list premium")
    print(f"   - Cek list amprem (live)")
    print(f"   - Temp mail support")
    print()
    pause()


# ============================================
#   MENU 4 - CEK LIST AMPREM (REAL)
# ============================================
def cek_list():
    header()
    print(f"{P}              CEK LIST AMPREM{NC}")
    print()

    data = baca_list()

    if not data:
        print(f"  {R}[!]{NC} Belum ada list tersimpan.")
        print(f"  {Y}[i]{NC} Setelah verifikasi berhasil,")
        print(f"       email otomatis masuk ke sini.")
        print()
        pause()
        return

    print(f"{P}  +-----+------------------------------+---------------------+{NC}")
    print(f"{P}  | {W}No{NC}  | {W}Email{NC}                        | {W}Waktu{NC}               |{NC}")
    print(f"{P}  +-----+------------------------------+---------------------+{NC}")

    for i, item in enumerate(data, 1):
        email = item["email"]
        waktu = item["waktu"]

        if len(email) > 28:
            email = email[:25] + "..."
        if len(waktu) > 19:
            waktu = waktu[:19]

        print(f"{P}  |{NC} {i:<3} {P}|{NC} {G}{email:<28}{NC} {P}|{NC} {Y}{waktu:<19}{NC} {P}|{NC}")

    print(f"{P}  +-----+------------------------------+---------------------+{NC}")
    print()
    print(f"  {G}[OK]{NC} Total: {W}{len(data)}{NC} email berhasil dipremium")
    print(f"  {Y}[i]{NC} Tersimpan di file: {W}{LIST_FILE}{NC}")
    print()
    pause()


# ============================================
#   MENU 5 - EMAIL TEMP MAIL (DOMAIN APAPUN)
# ============================================
def temp_mail():
    global TEMP_EMAIL
    header()

    print(f"{P}              MASUKAN EMAIL TEMP MAIL{NC}")
    print()
    print(f"{P}  +------------------------------------------------------+{NC}")
    print(f"{P}  |{NC}  Masukkan email temp mail kamu.                    {P}|{NC}")
    print(f"{P}  |{NC}  {Y}(Domain apapun){NC}                                 {P}|{NC}")
    print(f"{P}  +------------------------------------------------------+{NC}")
    print()
    print(f"{P}  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{NC}")
    print()

    email = input(f"{P}  > Email Temp Mail: {NC}").strip().lower()

    if not email:
        print(f"\n{R}  [!] Email tidak boleh kosong!{NC}")
        pause()
        return

    if "@" not in email or "." not in email.split("@")[-1]:
        print(f"\n{R}  [!] Format email tidak valid!{NC}")
        pause()
        return

    TEMP_EMAIL = email

    print()
    print(f"{Y}  [*] Mengirim link verifikasi ke {G}{email}{NC} ...")
    time.sleep(1.0)

    try:
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }
        requests.post(ENDPOINT_SEND, json={"gmail": email}, headers=headers)
    except Exception as e:
        print(f"{R}  [!] Gagal: {e}{NC}")
        pause()
        return

    print()
    print(f"{G}  [OK] Link verifikasi berhasil dikirim!{NC}")
    print(f"{Y}  [i] Cek inbox atau folder spam Temp Mail kamu.{NC}")
    print()
    input(f"{C}  Tekan Enter untuk lanjut ke menu verifikasi...{NC}")

    print(f"{P}  > Otomatis beralih ke menu 2...{NC}")
    time.sleep(1.2)
    masukan_link()


# ============================================
#   MENU 6 - HAPUS SEMUA LIST
# ============================================
def hapus_list():
    header()
    print(f"{P}              HAPUS SEMUA LIST{NC}")
    print()

    if not os.path.exists(LIST_FILE):
        print(f"  {Y}[i]{NC} File list belum ada.")
        pause()
        return

    konfirm = input(f"  {R}Yakin hapus semua list? (y/n): {NC}").strip().lower()

    if konfirm == "y":
        os.remove(LIST_FILE)
        print()
        print(f"  {G}[OK]{NC} Semua list berhasil dihapus!")
    else:
        print(f"\n  {Y}[i]{NC} Dibatalkan.")

    pause()


# ============================================
#   KELUAR
# ============================================
def keluar():
    clear()
    print()
    print(f"{P}  ============================================{NC}")
    print(f"{W}       TERIMA KASIH SUDAH MENGGUNAKAN{NC}")
    print(f"{P}             RASYAPREM v1.2{NC}")
    print(f"{P}  ============================================{NC}")
    print()
    time.sleep(1.2)
    sys.exit(0)


# ============================================
#   MAIN
# ============================================
def main():
    splash_screen()

    while True:
        pilih = menu_utama()

        if pilih == "1":
            masukan_email()
        elif pilih == "2":
            masukan_link()
        elif pilih == "3":
            tentang()
        elif pilih == "4":
            cek_list()
        elif pilih == "5":
            temp_mail()
        elif pilih == "6":
            hapus_list()
        elif pilih == "0":
            keluar()
        else:
            print(f"\n{R}  [!] Pilihan tidak valid!{NC}")
            time.sleep(1.0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"{P}  Keluar...{NC}")
        sys.exit(0)
