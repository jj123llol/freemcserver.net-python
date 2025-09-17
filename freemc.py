import requests

class FreeMc():

    global auth, idz

    def __init__(self, authz, idx, metrics):
        global auth, idz
        auth = {
            "authorization" : authz,
            "x-fmcs-metrics-wfkpe9eata": metrics
        }
        idz = idx
        print("with love from Ant, and dev<3")
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

    class server():
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

    class game():
        def time(self, set):
            response = FreeMc.console().write(f"time set {set}")
            return response  
