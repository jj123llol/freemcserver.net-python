# freemcserver.net-python
Python module to control your freemcserver.net server


Hello! if you are reading this, that means this is public.
this started as some stupid thing i was making for a discord bot for my school server.
this was not meant to be public but it was always a thought in my mind that i might release it.
i hope this helps you with whatever ur trying todo with your minecraft server


# starting

goto console page

use the network logger (ctrl + shift + i)

refresh page

click the first request (called console)

goto headers and get cookie

get the id from the topbar url,  panel.freemcserver.net/server/(this will be the id!)

make sure you've already downloaded the package
```
pip install freemcserver.py # this isint working atm, as we have not published.
```

```py
import freemc

FreeMc = freemc.FreeMc("server id")

server, console, chat, game, events = FreeMc.server(), FreeMc.console(), FreeMc.chat(), FreeMc.game(), FreeMc.events()
```
this will prompt you for your cookie, paste it into there and hit enter!




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
returns a string of the latest 20 console msgs
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

```py
user.give(item, amount)
```
gives the user the specificed amount of the specified item

```py
user.name
```
returns a string of the players username



# game
```
game.time("arg")
```
this executes the minecraft command "time set (arg)" with arg being the given argument 

# events

```py
events.on_leave
```
and
```py
events.on_join
```
return user class of the player who joined/left
```py
events.on_console_message
```
returns a string of the last 20 console messages every second
```py
@events.on_join
def can_be_anything(user):
    chat.say(f"Hello {user.name}!")
```
