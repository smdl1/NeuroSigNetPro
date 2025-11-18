import json
from pathlib import Path

class Config:
    def __init__(self):
        self.config = {
            "system": {
                "name": "NeuroSigNet Pro",
                "version": "2.0.0",
                "max_file_size": 100 * 1024 * 1024
            }
        }
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value else default