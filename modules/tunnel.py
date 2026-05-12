#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SharkPro v3.0 - Updated Tunnel Module for Termux/Linux
Supports:
- Ngrok
- Cloudflared
- localhost.run
- Localtunnel
- Localhost
"""

import os
import sys
import re
import time
import subprocess
import requests

# Optional psutil support
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    print("[!] psutil not available, using fallback methods")
    psutil = None
    HAS_PSUTIL = False

# Import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class TunnelManager:

    def __init__(self):
        self.processes = {}
        self.active_url = None

    # ==========================================================
    # Kill existing processes
    # ==========================================================
    def _kill_existing(self, service_name):

        try:
            subprocess.run(
                ['pkill', '-f', service_name.lower()],
                capture_output=True
            )
        except:
            pass

        if HAS_PSUTIL:
            try:
                for proc in psutil.process_iter(['pid', 'name']):

                    try:
                        name = proc.info.get('name')

                        if name and service_name.lower() in name.lower():
                            psutil.Process(proc.info['pid']).terminate()

                    except:
                        pass
            except:
                pass

        time.sleep(1)

    # ==========================================================
    # Check if service installed
    # ==========================================================
    def check_installed(self, service):

        try:
            result = subprocess.run(
                ['which', service],
                capture_output=True,
                text=True
            )

            return result.returncode == 0

        except:
            return False

    # ==========================================================
    # Install service
    # ==========================================================
    def install_service(self, service_name):

        print(f"[*] Installing {service_name}...")

        install_map = {
            'cloudflared': 'pkg install cloudflared -y',
            'ngrok': 'pkg install ngrok -y',
            'localtunnel': 'pkg install nodejs -y && npm install -g localtunnel',
        }

        cmd = install_map.get(service_name)

        if not cmd:
            print("[!] No install command available")
            return False

        try:
            subprocess.run(cmd, shell=True, check=True)

            print(f"[✓] Installed {service_name}")

            return True

        except Exception as e:
            print(f"[!] Install failed: {e}")

            return False

    # ==========================================================
    # NGROK
    # ==========================================================
    def start_ngrok(self, port=PORT):

        self._kill_existing('ngrok')

        if not self.check_installed('ngrok'):
            print("[!] ngrok not installed")
            return None

        print("[*] Starting ngrok tunnel...")

        try:

            proc = subprocess.Popen(
                [
                    'ngrok',
                    'http',
                    str(port),
                    '--log=stdout'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            self.processes['ngrok'] = proc

            time.sleep(5)

            for _ in range(20):

                try:

                    resp = requests.get(
                        'http://127.0.0.1:4040/api/tunnels',
                        timeout=3
                    )

                    data = resp.json()

                    tunnels = data.get('tunnels', [])

                    for tunnel in tunnels:

                        url = tunnel.get('public_url')

                        if url and url.startswith('https://'):

                            self.active_url = url

                            print(f"[✓] Ngrok ready: {url}")

                            return url

                except:
                    pass

                time.sleep(1)

            print("[!] Ngrok failed to provide URL")

            return None

        except Exception as e:
            print(f"[!] Ngrok error: {e}")

            return None

    # ==========================================================
    # CLOUDFLARED
    # ==========================================================
    def start_cloudflared(self, port=PORT):

        self._kill_existing('cloudflared')

        if not self.check_installed('cloudflared'):
            print("[!] cloudflared not installed")
            return None

        print("[*] Starting cloudflared tunnel...")

        try:

            proc = subprocess.Popen(
                [
                    'cloudflared',
                    'tunnel',
                    '--url',
                    f'http://127.0.0.1:{port}'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            self.processes['cloudflared'] = proc

            pattern = re.compile(
                r'https://[-a-zA-Z0-9]+\.trycloudflare\.com'
            )

            start_time = time.time()

            while time.time() - start_time < 30:

                line = proc.stdout.readline()

                if line:

                    print(f"[cloudflared] {line.strip()}")

                    match = pattern.search(line)

                    if match:

                        self.active_url = match.group(0)

                        print(f"[✓] Cloudflared ready: {self.active_url}")

                        return self.active_url

            print("[!] Cloudflared failed to provide URL")

            return None

        except Exception as e:

            print(f"[!] Cloudflared error: {e}")

            return None

    # ==========================================================
    # LOCALHOST.RUN
    # ==========================================================
    def start_localhost_run(self, port=PORT):

        self._kill_existing('localhost.run')

        print("[*] Starting localhost.run tunnel...")

        try:

            proc = subprocess.Popen(
                [
                    'ssh',
                    '-o',
                    'StrictHostKeyChecking=no',
                    '-R',
                    f'80:localhost:{port}',
                    'localhost.run'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            self.processes['localhost-run'] = proc

            pattern = re.compile(
                r'https://[a-zA-Z0-9.-]+\.(lhr\.life|localhost\.run|loca\.lt)'
            )

            start_time = time.time()

            while time.time() - start_time < 40:

                line = proc.stdout.readline()

                if line:

                    clean = line.strip()

                    print(f"[localhost.run] {clean}")

                    match = pattern.search(clean)

                    if match:

                        self.active_url = match.group(0)

                        print(f"[✓] localhost.run ready: {self.active_url}")

                        return self.active_url

            print("[!] localhost.run failed to provide URL")

            return None

        except Exception as e:

            print(f"[!] localhost.run error: {e}")

            return None

    # ==========================================================
    # LOCALTUNNEL
    # ==========================================================
    def start_localtunnel(self, port=PORT):

        self._kill_existing('lt')

        if not self.check_installed('lt'):

            print("[!] localtunnel not installed")

            print("[*] Install using:")
            print("pkg install nodejs")
            print("npm install -g localtunnel")

            return None

        print("[*] Starting localtunnel...")

        try:

            proc = subprocess.Popen(
                [
                    'lt',
                    '--port',
                    str(port)
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            self.processes['localtunnel'] = proc

            pattern = re.compile(
                r'https://[a-zA-Z0-9.-]+\.loca\.lt'
            )

            start_time = time.time()

            while time.time() - start_time < 30:

                line = proc.stdout.readline()

                if line:

                    clean = line.strip()

                    print(f"[localtunnel] {clean}")

                    match = pattern.search(clean)

                    if match:

                        self.active_url = match.group(0)

                        print(f"[✓] Localtunnel ready: {self.active_url}")

                        return self.active_url

            print("[!] Localtunnel failed")

            return None

        except Exception as e:

            print(f"[!] Localtunnel error: {e}")

            return None

    # ==========================================================
    # LOCALHOST
    # ==========================================================
    def start_localhost(self, port=PORT):

        self.active_url = f"http://127.0.0.1:{port}"

        print(f"[✓] Localhost: {self.active_url}")

        return self.active_url

    # ==========================================================
    # STOP ALL
    # ==========================================================
    def stop_all(self):

        print("[*] Stopping tunnels...")

        for name, proc in self.processes.items():

            try:
                proc.terminate()
                proc.wait(timeout=5)

            except:

                try:
                    proc.kill()
                except:
                    pass

        for service in [
            'ngrok',
            'cloudflared',
            'lt',
            'localhost.run'
        ]:
            self._kill_existing(service)

        print("[✓] All tunnels stopped")

    # ==========================================================
    # GET ACTIVE URL
    # ==========================================================
    def get_active_url(self):

        return self.active_url