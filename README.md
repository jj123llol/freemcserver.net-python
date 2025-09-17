# freemcserver.net-python
Python module to control your freemcserver.net server


Hello! if you are reading this, that means this is public.
this started as some stupid thing i was making for a discord bot for my school server.
this was not meant to be public but it was always a thought in my mind that i might release it.
i hope this helps you with whatever ur trying todo with your minecraft server


# starting

use the network logger (ctrl + shift + i)

hit start, and filter for a request called "start"

goto headers and get authentication (make sure u copy SCOPED too)

get the metrics (probably the last header), this changes quite a bit so keep it updated!

get the id from the topbar url,  panel.freemcserver.net/server/(this will be the id!)

make sure you've already downloaded the package
```
pip install freemcserver.py
```

```py
import freemc

FreeMc = freemc.FreeMc("auth", "server id", "metrics")

server, console, chatm game = FreeMc.server(), FreeMc.console(), FreeMc.chat(), FreeMc.game()
```




# server

you can do
```py
server.start()
```
to start the server,

```py
server.stop()
```
to stop the server,

```py
server.usage()
```
to return the usage JSON of the server,

```py
server.status()
```
returns true or false. true for online, false for offline.

```py
server.restart()
```
to restart the server.

```py
server.getPlayers()
```
returns a list of active users, in the FreeMc.user() format.
```py
users = server.getPlayers()
for user in user:
  user.smite()
```

# console

console.write("command"), executes a slash command in the console.
example:
```py
console.write("kill Plasma_Admin")
```

```py
console.getlogs()
```
returns a JSON of the console

```py
console.getlatest()
```
returns a string of the latest console msg
# chat

chat.say("message") makes the server say the given message.
example:
```py
chat.say("Dev stinks")
```
in game chat:
```
[Server] Dev stinks
```

# user
this class is a little different, it handles users!

to create a user class:
```py
user = FreeMc.user("Ant") # replace ant with the targets user
```

the functions for users are very understandable,
```py
user.kill()
user.kick()
user.ban()
user.ip_ban()
user.unban()
user.kill()
user.whitelist()
user.unwhitelist()
user.op()
user.deop()
```

```py
user.smite()
```
summons lightning on the target and kills them.



# game
```
game.time("arg")
```
this executes the minecraft command "time set (arg)" with arg being the given argument 
