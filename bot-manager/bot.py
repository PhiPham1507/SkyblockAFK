from config import make_config
from files import MCC_PATH, BOTS_DIR, generate_config
import subprocess
import time
import threading
JOINED_TEXT = "Server was successfully joined"

def spawn_bot(bot):
    config_text = make_config(bot)
    argument = generate_config(bot, config_text)
    # stdin=DEVNULL: stops MCC from asking the terminal for the cursor position. stdin=subprocess.PIPE so that we could input our 
    # MCC the commands to run when join server
    proc = subprocess.Popen([str(MCC_PATH), argument], cwd=BOTS_DIR / bot["account"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    reader = threading.Thread(target=read_output, args=(proc,bot["join_commands"]))
    reader.start()

#Function for thread. Simply outputting streams of data
def read_output(proc, commands):
    for line in proc.stdout:
        text = line.decode("utf-8")
        print(text)
        #In later runs, we'll have a deque of messages. Checking why joining server fails. 
        #Need to check for potential relogin (if SessionCache.db tokens expire)
        if JOINED_TEXT in text:
            print("this has been executed")
            threading.Thread(target=send_join_commands, args=(proc,commands)).start()
    print("reader thread is done")

def send_join_commands(proc,commands: list[str]) -> None:
    time.sleep(5)
    for command in commands:
        if proc.poll() is not None:
            print("MCC exited with code", proc.returncode)
            return
        send_command(proc, command)
        time.sleep(2)

def send_command(proc, command: str) -> None:
    try:
        print("Sending the command: " + command)
        proc.stdin.write((command + "\n").encode("utf-8"))
        proc.stdin.flush()
    except BrokenPipeError:
        print("Broken pipe")
        pass