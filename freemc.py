import requests, re, threading, time, os

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
        auth = req[req.find('window.fmcs.api_key="')+len('window.fmcs.api_key="'):req.find('window.fmcs.api_key="')+364]
        metrics = req[req.find('window.fmcs.metrics = "')+len('window.fmcs.metrics = "'):req.find('window.fmcs.metrics = "')+39]
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

        def tp(self, x, y, z):
            response = FreeMc.console().write(f"teleport {self.user} {x} {y} {z}")
            return response  

    class game():
        def time(self, set):
            response = FreeMc.console().write(f"time set {set}")
            return response 

    class events():
        def __init__(self):
            self.watch = {}
            def check_cons():
                while True:
                    time.sleep(1) # if its too high, you will miss messages!, if its too low no one can connect
                    self.console_sent(FreeMc.console().getlatest())
            loop = threading.Thread(target=check_cons)
            loop.start()
            

        def on_console_message(self, func):
            self.watch['on_msg'] = func

        def on_join(self, func):
            self.watch['on_join'] = func

        def on_leave(self, func):
            self.watch['on_leave'] = func

        def console_sent(self, msg):
            if 'on_msg' in self.watch:
                self.watch['on_msg'](msg)

            if 'on_join' in self.watch and msg.find("joined the game") > -1: # returns a user instance of the player who joined
                user = FreeMc.user(msg[msg.find('[93m')+4:msg.find("joined the game")-1])
                self.watch['on_join'](user)

            if 'on_leave' in self.watch and msg.find("left the game") > -1: # returns a user instance of the player who left
                user = FreeMc.user(msg[msg.find('[93m')+4:msg.find("left the game")-1])
                self.watch['on_leave'](user)


