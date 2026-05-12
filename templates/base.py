#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SharkPro v3.0 - Template Base & Generator
"""

import os

class TemplateLoader:
    """Load and manage HTML templates"""
    
    TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    @classmethod
    def load(cls, template_name):
        """Load template content"""
        template_path = os.path.join(cls.TEMPLATE_DIR, template_name)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    @classmethod
    def list_available(cls):
        """List all available templates"""
        templates = []
        for f in os.listdir(cls.TEMPLATE_DIR):
            if f.endswith('.html'):
                templates.append(f)
        return templates