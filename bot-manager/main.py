import os
from pathlib import Path
import subprocess

# Stand-in for a Bot row from the database
bot = {
    "id": "test1",
    "login": os.environ["MC_LOGIN"],
    "server": "manacube.com",
    "minecraft_version": "26.2",
}

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

bot_dir = Path("bots") / bot["id"]
bot_dir.mkdir(parents=True, exist_ok=True)

# Regenerated on every start: the DB is the source of truth
config_path = bot_dir / "config.ini"
config_path.write_text(config_text)

# Absolute, because MCC runs with cwd=bot_dir
mcc_path = Path("bin/MinecraftClient").resolve()

# stdin=DEVNULL: stops MCC from asking the terminal for the cursor position
proc = subprocess.Popen([str(mcc_path), "config.ini"], cwd=bot_dir, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
for line in proc.stdout:
    text = line.decode("utf-8")
    if "microsoft.com/link" in text:
        print(text)

proc.wait()
