# freemcserver.net-python
Python module to control your freemcserver.net server




# starting

use the network logger (ctrl + shift + i)

hit start, and filter for a request called "start"

goto headers and get authentication (make sure u copy SCOPED too)

get the metrics (probably the last header)

get the id from the topbar url,  panel.freemcserver.net/server/(this will be the id!)

```py
import freemc

FreeMc = freemc.FreeMc("auth", "server id", "metrics")

server, console, chat = FreeMc.server(), FreeMc.console(), FreeMc.chat()
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


# console

console.write("command"), executes a slash command in the console.
example:
```py
console.write("kill Plasma_Admin")
```

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
