""""
This is the main program, responsible for creating bots that do the afk.
It will loop forever to keep track of the status of the bots. It 
continuously fetches data from the database to check if any 
bot configuration/status has been updated, and will act acccordingly. 
"""
import os
from bot import spawn_bot
from login import login_account


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