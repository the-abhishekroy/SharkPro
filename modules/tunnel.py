#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Tunnel Module
Handles ngrok, cloudflared, localhost.run, and localtunnel
"""

import os
import sys
import re
import time
import subprocess
import requests
import signal
# Try to import psutil, but make it optional
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print(f"{Y}[!] psutil not available, using fallback methods{NC}")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class TunnelManager:
    """Manage various tunnel services"""
    
    def __init__(self):
        self.processes = {}
        self.active_url = None
    
    def _kill_existing(self, service_name):
        """Kill existing tunnel processes"""
        try:
            # Try pkill first (works on Termux/Linux)
            subprocess.run(['pkill', '-f', service_name.lower()], 
                         capture_output=True, timeout=5)
        except:
            pass
        
        # Fallback to psutil if available
        if HAS_PSUTIL:
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if service_name.lower() in proc.info['name'].lower():
                            psutil.Process(proc.info['pid']).terminate()
                    except:
                        pass
            except:
                pass
        
        time.sleep(1)
    
    def check_installed(self, service):
        """Check if a tunnel service is installed"""
        try:
            subprocess.run([service, '--version'], 
                         capture_output=True, timeout=3)
            return True
        except:
            return False
    
    def install_service(self, service_name):
        """Install a tunnel service"""
        service = TUNNEL_SERVICES[service_name]
        print(f"{Y}[*] Installing {service['name']}...{NC}")
        
        # Detect platform
        termux = os.path.exists('/data/data/com.termux/files/usr/bin')
        platform = "termux" if termux else "linux"
        
        install_cmd = service['install_cmd'].get(platform) or \
                      service['install_cmd'].get('all')
        
        if not install_cmd:
            print(f"{R}[!] No install command for this platform{NC}")
            return False
        
        try:
            subprocess.run(install_cmd, shell=True, check=True)
            print(f"{G}[✓] {service['name']} installed{NC}")
            return True
        except Exception as e:
            print(f"{R}[!] Install failed: {e}{NC}")
            return False
    
    def start_ngrok(self, port=PORT):
        """Start ngrok tunnel"""
        self._kill_existing('ngrok')
        
        if not self.check_installed('ngrok'):
            if not self.install_service('ngrok'):
                return None
        
        print(f"{Y}[*] Starting ngrok tunnel...{NC}")
        
        try:
            proc = subprocess.Popen(
                ['ngrok', 'http', str(port), '--log=stdout'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            self.processes['ngrok'] = proc
            
            # Wait for URL
            time.sleep(3)
            
            for _ in range(15):
                try:
                    resp = requests.get(TUNNEL_SERVICES['ngrok']['api_url'], 
                                      timeout=3)
                    data = resp.json()
                    if data.get('tunnels'):
                        url = [t['public_url'] for t in data['tunnels'] 
                               if 'https' in t['public_url']]
                        if url:
                            self.active_url = url[0]
                            print(f"{G}[✓] Ngrok ready: {W}{self.active_url}{NC}")
                            return self.active_url
                except:
                    pass
                time.sleep(1)
            
            print(f"{R}[!] Ngrok failed to provide URL{NC}")
            return None
            
        except Exception as e:
            print(f"{R}[!] Ngrok error: {e}{NC}")
            return None
    
    def start_cloudflared(self, port=PORT):
        """Start cloudflared tunnel"""
        self._kill_existing('cloudflared')
        
        if not self.check_installed('cloudflared'):
            if not self.install_service('cloudflared'):
                return None
        
        print(f"{Y}[*] Starting cloudflared tunnel...{NC}")
        
        try:
            proc = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            self.processes['cloudflared'] = proc
            
            # Parse output for URL
            pattern = re.compile(TUNNEL_SERVICES['cloudflared']['pattern'])
            start_time = time.time()
            
            while time.time() - start_time < 20:
                line = proc.stdout.readline()
                if line:
                    print(f"{Y}[cloudflared] {line.strip()[:80]}{NC}")
                    match = pattern.search(line)
                    if match:
                        self.active_url = match.group()
                        print(f"{G}[✓] Cloudflared ready: {W}{self.active_url}{NC}")
                        return self.active_url
            
            print(f"{R}[!] Cloudflared failed to provide URL{NC}")
            return None
            
        except Exception as e:
            print(f"{R}[!] Cloudflared error: {e}{NC}")
            return None
    
    def start_localhost_run(self, port=PORT):
        """Start localhost.run tunnel via SSH"""
        self._kill_existing('localhost.run')
        
        # Check if ssh is available
        try:
            subprocess.run(['ssh', '-V'], capture_output=True, timeout=3)
        except:
            print(f"{R}[!] SSH not available. Install openssh-client{NC}")
            return None
        
        print(f"{Y}[*] Starting localhost.run tunnel...{NC}")
        print(f"{Y}[*] Note: First run requires SSH key setup{NC}")
        
        try:
            proc = subprocess.Popen(
                ['ssh', '-o', 'StrictHostKeyChecking=no',
                 '-R', f'80:localhost:{port}', 'localhost.run'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            self.processes['localhost-run'] = proc
            
            # Parse output
            url_pattern = re.compile(r'(https?://[a-zA-Z0-9-]+\.(lhrtunnel\.link|loca\.lt))')
            start_time = time.time()
            
            while time.time() - start_time < 15:
                line = proc.stdout.readline()
                if line:
                    print(f"{Y}[localhost.run] {line.strip()[:80]}{NC}")
                    match = url_pattern.search(line)
                    if match:
                        self.active_url = match.group()
                        print(f"{G}[✓] Localhost.run ready: {W}{self.active_url}{NC}")
                        return self.active_url
            
            print(f"{R}[!] No URL received. Check if SSH works.{NC}")
            return None
            
        except Exception as e:
            print(f"{R}[!] localhost.run error: {e}{NC}")
            return None
    
    def start_localtunnel(self, port=PORT):
        """Start localtunnel (lt)"""
        self._kill_existing('localtunnel')
        
        # Check if npx is available
        try:
            subprocess.run(['which', 'npx'], capture_output=True, timeout=3)
        except:
            print(f"{R}[!] npx not found. Install Node.js{NC}")
            return None
        
        print(f"{Y}[*] Starting localtunnel...{NC}")
        
        try:
            proc = subprocess.Popen(
                ['npx', 'lt', '--port', str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            self.processes['localtunnel'] = proc
            
            # Parse output
            pattern = re.compile(TUNNEL_SERVICES['localtunnel']['pattern'])
            start_time = time.time()
            
            while time.time() - start_time < 15:
                line = proc.stdout.readline()
                if line:
                    print(f"{Y}[localtunnel] {line.strip()[:80]}{NC}")
                    match = pattern.search(line)
                    if match:
                        self.active_url = match.group()
                        print(f"{G}[✓] Localtunnel ready: {W}{self.active_url}{NC}")
                        return self.active_url
            
            print(f"{R}[!] Localtunnel failed{NC}")
            return None
            
        except Exception as e:
            print(f"{R}[!] Localtunnel error: {e}{NC}")
            return None
    
    def start_localhost(self, port=PORT):
        """Return localhost URL"""
        self.active_url = TUNNEL_SERVICES['localhost']['url'].format(port=port)
        print(f"{G}[✓] Localhost: {W}{self.active_url}{NC}")
        return self.active_url
    
    def stop_all(self):
        """Stop all tunnel processes"""
        print(f"{Y}[*] Stopping tunnels...{NC}")
        
        for name, proc in self.processes.items():
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                try:
                    proc.kill()
                except:
                    pass
        
        # Clean up any remaining processes
        for service in ['ngrok', 'cloudflared', 'localtunnel']:
            self._kill_existing(service)
        
        print(f"{G}[✓] All tunnels stopped{NC}")
    
    def get_active_url(self):
        """Get currently active tunnel URL"""
        return self.active_url