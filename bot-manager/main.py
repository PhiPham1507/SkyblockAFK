import os
from pathlib import Path
import subprocess

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
# "/" here is concatenate path
bot_dir = Path("bots") / bot["id"] 
#parents=True mean create bots/ if doesn't exist
#exist_ok=True means if it has existed, do nothing. If it's false, then crash if file exists
bot_dir.mkdir(parents=True, exist_ok=True)

#Create the config.ini file
config_path = bot_dir / "config.ini"
#If config.ini doens't exist, create and write the above text. If created, then overwrite (allow setting change later on)
#When writing, it takes in the relative path, cwd() 
config_path.write_text(config_text)
#.resolve() give the absolute path while bot_dir is a relative path (to where running program is).
#we need the absolute path because spawning another program requires absolute path, since we're running the program 
#in the directory of /bots/test1 not where main.py runs
mcc_path = Path("bin/MinecraftClient").resolve()

#mcc_path is a Path object, must convert to a string to run
#The first argument of the run() is a list, where the first argument is the program, and the remaining are command line arguments
#subprocess.run([str(mcc_path), "config.ini"], cwd=bot_dir)


#MCC asks for the cursor's position of our terminal so that messages won't get mixed up with what being displayed
#Setting stdin to DEVNULL makes MCC doesn't ask.
proc = subprocess.Popen([str(mcc_path), "config.ini"], cwd=bot_dir, stdin=subprocess.DEVNULL)
#.run() waits until the process ends for main() to continue. While .Popen() returns
#immedietly to the flow of main

print("Hi")
print(proc.pid)