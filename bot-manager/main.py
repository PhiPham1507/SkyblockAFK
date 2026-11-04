""""
This is the main program, responsible for creating bots that do the afk.
It will loop forever to keep track of the status of the bots. It 
continuously fetches data from the database to check if any 
bot configuration/status has been updated, and will act acccordingly. 
"""
import os
import subprocess
import time
import threading
import re
import shutil
from bot import spawn_bot

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
    #Terminate the process after n seconds, so that stdout reaches EOF and ends loop
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


# Stand-in for a Bot row from the database
# bot = {
#     "account": "Manobee",
#     "login": os.environ["MC_LOGIN"],
#     "server": "survival.manacube.com",
#     "minecraft_version": "26.2",
#     "join_commands": ["/survival", "/home", "hi everyone"],
# }
#login_account(bot["account"], bot["login"])
bot2 = {
    "account": "TheGhost06",
    "login": os.environ["MC_LOGIN2"],
    "server": "survival.manacube.com",
    "minecraft_version": "26.2",
    "join_commands": ["/survival", "/home", "hi everyone"],
}
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
spawn_bot(bot2)
# spawn_bot(bot2)
# spawn_bot(bot3)
# spawn_bot(bot4)