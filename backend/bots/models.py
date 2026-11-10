from django.db import models

# Create your models here.
class MinecraftAccount(model.models):
    #name
    #hashedpass
    #foreign key with user account
    # foreign key with servers

class ConnectedServers(model.models):
    #server  name
    #server ip
    #configurations for the connected server