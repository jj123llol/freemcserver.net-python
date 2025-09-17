import requests, re

class FreeMc():

    global auth, idz, known_metrics

    known_metrics = { # im like 70% sure they just swap between a few, so maybe we can collect them all and make a list so people dont have to manually change it
        "ea481edd605e676d", 
        "db04d5e26046e3e2",
        "1bba7aaf42261ccc",
    }

    def __init__(self, authz, idx, metrics):
        global auth, idz
        auth = {
            "authorization" : authz,
            "x-fmcs-metrics-wfkpe9eata": metrics
        }
        idz = idx
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
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/logs?lines=200&since={latest-2}", headers=auth).json()
                string = str(response['log']['lines'])
                return string[string.find("[K[")+2:string.find("'}")]
            except Exception as e:
                return e

    class server():
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
            response = FreeMc.console().write(f"say {msg}")
            return response

    class user():
        def __init__(self, user):
            self.user = user

        def kick(self):
            response = FreeMc.console().write(f"kick {self.user}")
            return response

        def ban(self):
            response = FreeMc.console().write(f"ban {self.user}")
            return response

        def ip_ban(self):
            response = FreeMc.console().write(f"ban-ip {self.user}")
            return response

        def unban(self):
            FreeMc.console().write(f"pardon {self.user}")
            response = FreeMc.console().write(f"pardon-ip {self.user}")
            return response

        def kill(self):
            response = FreeMc.console().write(f"kill {self.user}")
            return response

        def smite(self):
            response = FreeMc.console().write(f"execute at {self.user} run summon lightning_bolt ~ ~ ~")
            self.kill()
            return response

        def whitelist(self):
            response = FreeMc.console().write(f"whitelist add {self.user}")
            return response

        def unwhitelist(self):
            response = FreeMc.console().write(f"whitelist remove {self.user}")
            return response

        def op(self):
            response = FreeMc.console().write(f"op {self.user}")
            return response  

        def deop(self):
            response = FreeMc.console().write(f"deop {self.user}")
            return response  


        def give(self, item, amount):
            response = FreeMc.console().write(f"give {self.user} {item} {amount}")
            return response  

    class game():
        def time(self, set):
            response = FreeMc.console().write(f"time set {set}")
            return response  
