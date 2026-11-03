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
    
    [ChatBot.AntiAFK]
    Enabled = true
    Delay = {{ min = 180.0, max = 300.0 }}
    Command = "/help"
    
    [ChatBot.AutoRelog]
    Enabled = true
    Delay = {{ min = 5.0, max = 8.0 }}
    Retries = 10

    [ChatBot.ScriptScheduler]
    Enabled = true
    [[ChatBot.ScriptScheduler.TaskList]]
    Task_Name = "Send on login"
    Trigger_On_Interval = {{ Enable = true, MinTime = 60, MaxTime = 600 }}
    Action = "send hi everyone"

    """