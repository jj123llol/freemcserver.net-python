# freemcserver.net-python
Python module to control your freemcserver.net server




# starting

use the network logger (ctrl + shift + i)

hit start, and filter for a request called "start"

goto headers and get authentication (make sure u copy SCOPED too)

get the metrics (probably the last header)

get the id from the topbar url,  https://panel.freemcserver.net/server/(this will be the id!)

```py
import freemc

FreeMc = freemc.FreeMc("auth", "server id", "metrics")

server, console, chat, whitelist = FreeMc.server(), FreeMc.console(), FreeMc.chat(), FreeMc.whitelist()
```
