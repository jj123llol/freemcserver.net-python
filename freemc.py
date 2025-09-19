import sys
import warnings
import requests
import re
import threading
import time
import os

class FreeMc():

    global auth, idz


    def __init__(self, idx):
        global auth, idz
        if not os.path.exists("cookie.txt"):
            with open("cookie.txt", "w") as f:
                f.write(input("Enter Cookie: "))

        with open("cookie.txt", "r") as f:
            cookie = f.read()

        if '\n' in cookie:
            cookie = cookie.replace('\n', ' ')
            with open("cookie.txt", "w") as f:
                f.write(cookie)

        header = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36 Edg/140.0.0.0",
            "cookie": cookie
        }
        idz = idx
        req = requests.get(f"https://panel.freemcserver.net/server/{idz}/console", headers=header).text

        #auth_rgx = r"window\.fmcs\.api_key(?: )?=(?: )?\"([a-zA-Z0-9]+)\""
        #metrics_rgx = r"window\.fmcs\.metrics(?: )?=(?: )?\"([a-zA-Z0-9]+)\"" # magic!
        auth = req[req.find('window.fmcs.api_key="')+len('window.fmcs.api_key="'):req.find('window.fmcs.api_key="')+364]
        metrics = req[req.find('window.fmcs.metrics = "')+len('window.fmcs.metrics = "'):req.find('window.fmcs.metrics = "')+39]
        # use these if regex fails ^^

        #auth_match = re.search(auth_rgx, req)
        #metrics_match = re.search(metrics_rgx, req)
        
        #auth_group = metrics_group = None

        #if auth_match:
            #auth_group = auth_match.group(1)

        #if metrics_match:
            #metrics_group = metrics_match.group(1)

        #if not auth_group or not metrics_group:
            #print("auth/metrics not found, bye cro")
            #sys.exit(1)
        
        #auth = str(auth_group)
        #metrics = str(metrics_group)

        auth = {
            "authorization" : auth,
            "x-fmcs-metrics-wfkpe9eata": metrics
        }
    class console():
        def write(self, text):
            try:
                payload = {
                    "command": text
                }
                response = requests.post(f"https://api.freemcserver.net/v4/server/{idz}/command", json=payload, headers=auth).json()
                return response
            except Exception as e:
                return e

        def getlogs(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/logs", headers=auth).json()
                return response['log']['lines']
            except Exception as e:
                return e

        def getlatest(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/logs", headers=auth).json()
                latest = response['log']['latest']
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/logs?lines=20&since={latest-4}", headers=auth).json()
                # we return the latest 20 messages as a string, to try and make sure we dont miss any
                string = str(response['log']['lines'])
                return string[string.find("[K[")+2:string.find("'}")]
            except Exception as e:
                return e

    class server():
        def __init__(self):
            rgx = r"<code>([a-zA-Z0-9-]+)\.enderman\.cloud<\/code>"
            req = requests.get(f"https://panel.freemcserver.net/server/{idz}", headers=auth).text
            match = re.search(rgx, req, re.MULTILINE)
            if not match:
                raise ValueError("Couldn't find server ip")
            
            ip = match.group(1)
            if not ip:
                raise ValueError("Couldn't find server ip")
            
            self.ip = f"{ip}.enderman.cloud"

        def getPlayers(self):
            response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/ping", headers=auth).json()
            online = response['data']["players"]['list']
            return [FreeMc.user(plr['name']) for plr in online]

        def status(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/usage",headers=auth).json()
                return response['usage']['is_online']
            except Exception as e:
                return e

        def start(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/start",headers=auth).json()
                return response
            except Exception as e:
                return e

        def stop(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/stop",headers=auth).json()
                return response
            except Exception as e:
                return e

        def usage(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/usage",headers=auth).json()
                return response
            except Exception as e:
                return e

        def restart(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/restart",headers=auth).json()
                return response
            except Exception as e:
                return e

    class chat():
        def say(self, msg):
            if len(msg) > 256:
                raise ValueError("Message is too long!")
            response = FreeMc.console().write(f"say {msg}")
            return response

    class user():
        def __init__(self, user):
            self.name = user
        
        @property
        def user(self):
            raise ValueError("Expected user.name, not user.user 🥀")

        def kick(self):
            response = FreeMc.console().write(f"kick {self.name}")
            return response

        def ban(self):
            response = FreeMc.console().write(f"ban {self.name}")
            return response

        def ip_ban(self):
            response = FreeMc.console().write(f"ban-ip {self.name}")
            return response

        def unban(self):
            FreeMc.console().write(f"pardon {self.name}")
            response = FreeMc.console().write(f"pardon-ip {self.name}")
            return response

        def kill(self):
            response = FreeMc.console().write(f"kill {self.name}")
            return response

        def smite(self):
            response = FreeMc.console().write(f"execute at {self.name} run summon lightning_bolt ~ ~ ~")
            self.kill()
            return response

        def whitelist(self):
            response = FreeMc.console().write(f"whitelist add {self.name}")
            return response

        def unwhitelist(self):
            response = FreeMc.console().write(f"whitelist remove {self.name}")
            return response

        def op(self):
            response = FreeMc.console().write(f"op {self.name}")
            return response  

        def deop(self):
            response = FreeMc.console().write(f"deop {self.name}")
            return response  

        def give(self, item, amount):
            response = FreeMc.console().write(f"give {self.name} {item} {amount}")
            return response  

        def tp(self, x, y, z):
            response = FreeMc.console().write(f"tp {self.name} {x} {y} {z}")
            return response  

    class game():
        def time(self, set):
            response = FreeMc.console().write(f"time set {set}")
            return response 

    class events():
        global watch
        watch = {}
        def __init__(self):
            def check_cons():
                while True:
                    if len(watch) > 0: 
                        time.sleep(1) # if its too high, you will miss messages!, if its too low no one can connect
                        self.trigger_event(FreeMc.console().getlatest())
            loop = threading.Thread(target=check_cons)
            loop.start()
            
        def on_console_message(func):
            def wrapper(self, *args, **kwargs):
                global watch
                watch['on_msg'] = func
                result = func(*args, **kwargs)
                return result
            return wrapper

        def on_join(func):
            def wrapper(self, *args, **kwargs):
                global watch
                watch['on_join'] = func
                result = func(*args, **kwargs)
                return result
            return wrapper

        def on_leave(func):
            def wrapper(self, *args, **kwargs):
                global watch
                watch['on_leave'] = func
                result = func(*args, **kwargs)
                return result
            return wrapper

        def trigger_event(self, msg):
            if self.watch['on_msg']:
                self.watch['on_msg'](msg)

            if self.watch['on_join'] and msg.find("joined the game") > -1: # returns a user instance of the player who joined
                user = FreeMc.user(msg[msg.find('[93m')+4:msg.find("joined the game")-1])
                self.watch['on_join'](user)

            if self.watch['on_leave'] and msg.find("left the game") > -1: # returns a user instance of the player who left
                user = FreeMc.user(msg[msg.find('[93m')+4:msg.find("left the game")-1])
                self.watch['on_leave'](user)
