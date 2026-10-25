import os
from pathlib import Path
import subprocess
import time
import threading
import re
import shutil

def login_account(account, email):
    #The default mode has color in its terminal, which makes our regex complicated. Disable it
    input_string = f"""[Main.General]
    Account = {{ Login = "{email}", Password = "" }}
    Server = {{ Host = "" }}
    AccountType = "microsoft"
    Method = "mcc"

    [Console.General]
    ConsoleColorMode = "disable"
    """
    account_dir = Path("bots") / account
    account_dir.mkdir(parents=True, exist_ok=True)
    config_path = account_dir / "login.ini"
    config_path.write_text(input_string)

    mcc_path = Path("bin/MinecraftClient").resolve()
    proc = subprocess.Popen([str(mcc_path), "login.ini"], cwd=account_dir, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
    login = threading.Thread(target=print_login, args=(proc, account_dir))
    login.start()    

def print_login(proc, account_dir):
    timer = threading.Timer(10, proc.terminate)
    timer.start()
    success = False
    for line in proc.stdout:
        text = line.decode("utf-8")
        if("microsoft.com/link" in text):
            match = re.search(r"code:\s+([A-Z0-9]+)", text)
            if(match):
                print("Success")
                print(match[1])
            else:
                print(repr(text))
        elif("Server IP" in text or (account_dir / "SessionCache.db").exists()):
            success = True
            proc.terminate()
        else:
            print(text)
    if(success):
        print("Logged in Successfully")
        #Doesn't need to wait for the timer thread.
        timer.cancel()
    else:
        print("Logged in fail")
        #Doesn't use account_dir.rmdir() because that assumes empty file
        shutil.rmtree(account_dir)

def spawn_bot(bot):
    config_text = make_config(bot)
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

#Set up the configuration file. Content as a string
def make_config(bot) -> str:
    #The f""" is to start a big chunk of string, and it allows python code insertion"
    return f"""[Main.General]
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

#Function for thread. Simply outputting streams of data
def read_output(proc):
    for line in proc.stdout:
        text = line.decode("utf-8")
        print(text)
    print("reader thread is done")


# Stand-in for a Bot row from the database
bot = {
    "account": "logintest",
    "login": os.environ["MC_LOGIN"],
    "server": "survival.manacube.com",
    "minecraft_version": "26.2",
}
login_account(bot["account"], bot["login"])
# bot2 = {
#     "account": "Manobee",
#     "login": os.environ["MC_LOGIN"],
#     "server": "smp.newwind.club",
#     "minecraft_version": "26.3",
# }
# bot3 = {
#     "account": "logintest2",
#     "login": os.environ["MC_LOGIN2"],
#     "server": "survival.manacube.com",
#     "minecraft_version": "26.2",
# }
# login_account(bot3["account"], bot3["login"])
# bot4 = {
#     "account": "Ivoir",
#     "login": os.environ["MC_LOGIN2"],
#     "server": "ml.zetrex.net",
#     "minecraft_version": "26.3",
# }
# spawn_bot(bot)
# spawn_bot(bot2)
# spawn_bot(bot3)
# spawn_bot(bot4)