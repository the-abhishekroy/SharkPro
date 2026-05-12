#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Geolocation Module
Fixed IP geolocation with multiple fallback services
"""

import os
import sys
import json
import socket
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class GeoLocator:
    """IP Geolocation with fallback services"""
    
    def __init__(self):
        self.cache = {}
        self.services = [
            {
                "name": "ip-api.com",
                "url": "http://ip-api.com/json/{ip}",
                "parser": self._parse_ip_api
            },
            {
                "name": "ipapi.co",
                "url": "https://ipapi.co/{ip}/json/",
                "parser": self._parse_ipapi_co
            },
            {
                "name": "ipwho.is",
                "url": "https://ipwho.is/{ip}",
                "parser": self._parse_ipwho
            },
            {
                "name": "ipinfo.io",
                "url": "https://ipinfo.io/{ip}/json",
                "parser": self._parse_ipinfo
            }
        ]
    
    def _is_private_ip(self, ip):
        """Check if IP is private/local"""
        try:
            parts = ip.split('.')
            if len(parts) == 4:
                # Check private ranges
                if parts[0] == '10':
                    return True
                if parts[0] == '192' and parts[1] == '168':
                    return True
                if parts[0] == '172' and 16 <= int(parts[1]) <= 31:
                    return True
                if parts[0] == '127':
                    return True
            if ip in ['localhost', '::1', '0.0.0.0']:
                return True
            return False
        except:
            return True
    
    def _parse_ip_api(self, data):
        """Parse ip-api.com response"""
        if data.get('status') != 'success':
            return None
        return {
            'ip': data.get('query'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('regionName', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'country_code': data.get('countryCode', 'Unknown'),
            'isp': data.get('isp', 'Unknown'),
            'org': data.get('org', 'Unknown'),
            'lat': data.get('lat', 0),
            'lon': data.get('lon', 0),
            'zip': data.get('zip', 'Unknown'),
            'timezone': data.get('timezone', 'Unknown'),
            'loc': f"{data.get('lat', 0)},{data.get('lon', 0)}"
        }
    
    def _parse_ipapi_co(self, data):
        """Parse ipapi.co response"""
        if data.get('error'):
            return None
        return {
            'ip': data.get('ip'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country_name', 'Unknown'),
            'country_code': data.get('country', 'Unknown'),
            'isp': data.get('org', 'Unknown'),
            'org': data.get('org', 'Unknown'),
            'lat': data.get('latitude', 0),
            'lon': data.get('longitude', 0),
            'zip': data.get('postal', 'Unknown'),
            'timezone': data.get('timezone', 'Unknown'),
            'loc': f"{data.get('latitude', 0)},{data.get('longitude', 0)}"
        }
    
    def _parse_ipwho(self, data):
        """Parse ipwho.is response"""
        if not data.get('success', True):
            return None
        return {
            'ip': data.get('ip'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'country_code': data.get('country_code', 'Unknown'),
            'isp': data.get('connection', {}).get('isp', 'Unknown'),
            'org': data.get('connection', {}).get('org', 'Unknown'),
            'lat': data.get('latitude', 0),
            'lon': data.get('longitude', 0),
            'zip': data.get('postal', 'Unknown'),
            'timezone': data.get('timezone', {}).get('id', 'Unknown'),
            'loc': f"{data.get('latitude', 'unknown')},{data.get('longitude', 'unknown')}"
                   if data.get('latitude') else 'Unknown'
        }
    
    def _parse_ipinfo(self, data):
        """Parse ipinfo.io response"""
        loc = data.get('loc', '0,0')
        lat, lon = loc.split(',') if ',' in loc else ('0', '0')
        return {
            'ip': data.get('ip'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('region', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'country_code': data.get('country', 'Unknown'),
            'isp': data.get('org', 'Unknown'),
            'org': data.get('org', 'Unknown'),
            'lat': float(lat) if lat != '0' else 0,
            'lon': float(lon) if lon != '0' else 0,
            'zip': data.get('postal', 'Unknown'),
            'timezone': data.get('timezone', 'Unknown'),
            'loc': loc
        }
    
    def lookup(self, ip):
        """
        Lookup IP geolocation with fallback services
        Returns dict with location data
        """
        # Check cache
        if ip in self.cache:
            return self.cache[ip]
        
        # Handle private IPs
        if self._is_private_ip(ip):
            return {
                'ip': ip,
                'city': 'Private Network',
                'region': 'Local',
                'country': 'Local',
                'country_code': 'LO',
                'isp': 'Private Network',
                'org': 'Local Network',
                'lat': 'N/A',
                'lon': 'N/A',
                'zip': 'N/A',
                'timezone': 'Local',
                'loc': 'Private Network'
            }
        
        # Try each service
        for service in self.services:
            try:
                url = service['url'].format(ip=ip)
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    result = service['parser'](data)
                    
                    if result and result['country'] != 'Unknown':
                        # Cache and return
                        self.cache[ip] = result
                        return result
                        
            except Exception as e:
                continue
        
        # All services failed
        return {
            'ip': ip,
            'city': 'Unknown',
            'region': 'Unknown',
            'country': 'Unknown',
            'country_code': 'XX',
            'isp': 'Unknown',
            'org': 'Unknown',
            'lat': 'Unknown',
            'lon': 'Unknown',
            'zip': 'Unknown',
            'timezone': 'Unknown',
            'loc': 'Unknown'
        }
    
    def display(self, ip):
        """Display formatted geolocation info"""
        data = self.lookup(ip)
        
        print(f"""
{Y}┌────────────────────────────────────────────┐{NC}
{Y}│{C} 📍 LOCATION INTELLIGENCE                  {Y}│{NC}
{Y}├────────────────────────────────────────────┤{NC}
{Y}│{NC} IP:        {W}{data['ip']:<35}{Y}│{NC}
{Y}│{NC} City:      {C}{data['city']:<35}{Y}│{NC}
{Y}│{NC} Region:    {C}{data['region']:<35}{Y}│{NC}
{Y}│{NC} Country:   {C}{data['country']:<35}{Y}│{NC}
{Y}│{NC} ISP:       {M}{data['isp']:<35}{Y}│{NC}
{Y}│{NC} Org:       {M}{data['org']:<35}{Y}│{NC}
{Y}│{NC} Coords:    {G}{data['loc']:<35}{Y}│{NC}
{Y}│{NC} Timezone:  {data['timezone']:<35}{Y}│{NC}
{Y}└────────────────────────────────────────────┘{NC}
""")
        
        return data


if __name__ == "__main__":
    # Test with public IP
    geo = GeoLocator()
    geo.display("8.8.8.8")