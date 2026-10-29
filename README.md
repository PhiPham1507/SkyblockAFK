# SkyblockAFK

A web service that keeps Minecraft AFK bots online 24/7 on Skyblock and economy servers.

Users sign in with their Microsoft account through the official device-code flow, pick the servers
they want a bot on, and set the commands it runs. The bots run in the cloud, so the user's PC can
stay off.

## How it works

1. A user creates an account on the website.
2. They link a Minecraft account with Microsoft's device-code login: the site shows a code, and
   the user approves it on `microsoft.com/link`. The site never sees their password.
3. For each server they want a bot on, they enter the server address, the commands to run on join,
   any timed commands, and the anti-AFK and auto-relog settings.
4. The backend saves this config to the database. The bot manager generates a config file from
   it and launches a [Minecraft Console Client](https://github.com/MCCTeam/Minecraft-Console-Client)
   (MCC) process.
5. The dashboard shows each bot's status. It can also show the bot's recent output ("peek") and
   send it commands.

## Tech stack

| Part        | Tech                                               |
|-------------|----------------------------------------------------|
| Frontend    | React + TypeScript (Vite)                          |
| Backend API | Django + Django REST Framework                     |
| Database    | PostgreSQL                                         |
| Bot manager | Python process that launches and supervises MCC    |
| Bot client  | Minecraft Console Client (official release binary) |

## Repository layout

```
SkyblockAFK/
  frontend/              React + TypeScript app (not started yet)
  backend/               Django API
    config/              Django project settings and URLs
    manage.py
    requirements.txt
    .env.example         environment variables the backend needs (copy to .env)
  bot-manager/           Python service that runs the MCC bots
    main.py
    bin/                 MCC binary, downloaded separately (not committed)
    bots/<account>/      per-account login cache and generated bot configs (not committed)
```

## License

All rights reserved. This source code is public for portfolio purposes only.

This project is not affiliated with Mojang Studios or Microsoft.
