import threading
import re
import shutil
import subprocess
from pathlib import Path
from files import BOTS_DIR


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
    account_dir = BOTS_DIR / account
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
