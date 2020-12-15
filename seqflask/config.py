import os

sec_key = os.urandom(32)

class Config:
    SECRET_KEY = sec_key
