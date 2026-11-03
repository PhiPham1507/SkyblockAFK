"""
This module is used to generate files and directories. Flow: spawn bot 
calls generate_config, and uses MCC_PATH to run
"""
from pathlib import Path
from config import *
BASE_DIR = Path(__file__).resolve().parent 
BOTS_DIR = BASE_DIR / "bots"
MCC_PATH = BASE_DIR / "bin/MinecraftClient"

#This is an internal function
def _make_account_dir(acc : str)-> Path:
    account_dir = BOTS_DIR / "acc"
    account_dir.mkdir(parents=True, exist_ok=True)
    return account_dir

def _make_account_server_dir(acc : str, server : str) -> Path:
    server_dir = _make_account_dir(acc) / server
    server_dir.mkdir(parents=True, exist_ok=True)
    return server_dir


def generate_config(bot : dict, text : str) -> str:
    config_file = make_account_server_dir(bot["account"], bot["server"]) / "config.ini"
    # Regenerated on every start: the DB is the source of truth
    config_file.write_text(text)
    return str(config_file)
