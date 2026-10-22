import os
from pathlib import Path
import subprocess
import time
import threading



def read_output(proc):
    for line in proc.stdout:
        text = line.decode("utf-8")
        print(text)
    print("reader thread is done")


# Stand-in for a Bot row from the database
bot = {
    "account": "Manobee",
    "login": os.environ["MC_LOGIN"],
    "server": "survival.manacube.com",
    "minecraft_version": "26.2",
}

#The f""" is to start a big chunk of string, and it allows python code insertion"
config_text = f"""[Main.General]
Account = {{ Login = "{bot['login']}", Password = "" }}
Server = {{ Host = "{bot['server']}" }}
AccountType = "microsoft"
Method = "mcc"

[Main.Advanced]
EnableSentry = false
MinecraftVersion = "{bot['minecraft_version']}"
TerrainAndMovements = false
InventoryHandling = false
EntityHandling = false
SessionCache = "disk"
"""

account_dir = Path("bots") / bot["account"]
account_dir.mkdir(parents=True, exist_ok=True)
bot_dir = account_dir / bot["server"]
bot_dir.mkdir(parents=True, exist_ok=True)

# Regenerated on every start: the DB is the source of truth
config_path = bot_dir / "config.ini"
config_path.write_text(config_text)

# Absolute, because MCC runs with cwd=bot_dir
mcc_path = Path("bin/MinecraftClient").resolve()
argument = str(Path(bot["server"]) / "config.ini")
# stdin=DEVNULL: stops MCC from asking the terminal for the cursor position
proc = subprocess.Popen([str(mcc_path), argument], cwd=account_dir, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
reader = threading.Thread(target=read_output, args=(proc,))
reader.start()
# time.sleep(30)
# proc.terminate()
# reader.join(timeout=5)
# print(reader.is_alive())

