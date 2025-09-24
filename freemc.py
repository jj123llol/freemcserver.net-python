
import requests, re, threading, time, os # noqa: E401
# ant likes putting imports in 1 line but vs code wont stop screaming at me :wilted_rose:

# :middle_finger: IT LOOKS NICER

class FreeMc():
    global auth, idz, header

    def __init__(self, idx):
        global auth, idz, header
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

        if req.find("Your server is currently expired because it was not renewed") > -1:
            raise Exception("Please renew your server before running, we are unable to access important data such as server ip!")

        find_method = "find"
        # find = current method (str.find)
        # regex = experimental - dev

        if find_method == "find":
            auth_found = req.find('window.fmcs.api_key="')
            metrics_found = req.find('window.fmcs.metrics = "')

            auth = req[auth_found+21:auth_found+365]
            metrics = req[metrics_found+23:metrics_found+39]

        elif find_method == "regex":
            auth_rgx = r'window.fmcs.api_key="(SCOPED (?:[a-zA-Z0-9._-]+))"'
            auth_match = re.search(auth_rgx, req, re.MULTILINE)

            metrics_rgx = r'window.fmcs.metrics = "([a-zA-Z0-9]+)"'
            metrics_match = re.search(metrics_rgx, req, re.MULTILINE)

            auth, metrics = (auth_match and auth_match.group(1)), (metrics_match and metrics_match.group(1))

        if not auth or auth.find("SCOPED") < 0:
            raise ValueError("Failed to find auth, maybe the site changed their code and we have to rewrite the finding method\nor the cookie cannot access the server id entered.. did you use the right one?")

        auth = {
            "authorization" : auth,
            "x-fmcs-metrics-wfkpe9eata": metrics,
        }
        print("Connected!")

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

        def getSingleLatest(self):
            try:
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/logs", headers=auth).json()
                latest = response['log']['latest']
                response = requests.get(f"https://api.freemcserver.net/v4/server/{idz}/logs?lines=20&since={latest-3}", headers=auth).json()
                string = str(response['log']['lines'])
                return string[string.find("[K[")+2:string.find("'}")]
            except Exception as e:
                return e

        def writeList(self, lis):
            for cmd in lis:
                try:
                    self.write(cmd)
                except Exception as e:
                    return e

    class server():
        def __init__(self):
            global header
            rgx = r"<code>([a-zA-Z0-9-]+)\.enderman\.cloud</code>"
            req = requests.get(f"https://panel.freemcserver.net/server/{idz}", headers=header).text
            match = re.search(rgx, req, re.MULTILINE)

            ip = match and match.group(1)

            if not ip:
                raise ValueError("Couldn't find server IP")

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
            try:
                if len(msg) > 256:
                    raise ValueError("Message is too long!")
                response = FreeMc.console().write(f"say {msg}")
                return response
            except Exception as e:
                return e

    class user():
        def __init__(self, user):
            self.name = user
            self.jail_info = {}
        
        @property
        def user(self):
            print("[WARNING] user.user is deprecated! Use user.name")
            return self.name

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

        def tp(self, coords: tuple[str, str, str]):
            x, y, z = coords
            response = FreeMc.console().write(f"tp {self.name} {x} {y} {z}")
            return response
        
        def jail(self):
            self.tp(('~', '~', '~'))
            coords_str = FreeMc.console().getSingleLatest()
            rgx = re.compile(f"Teleported {self.name} to ([0-9.]+), ([0-9.]+), ([0-9.]+)")
            match = re.search(rgx, coords_str)
            if not match:
                raise Exception("Couldn't find player coords")
            
            x, y, z = match.groups()
            print(x, y, z)
            if not self.jail_info.get('jailed'):
                self.jail_info['jailed'] = True
                self.jail_info['coords'] = (x, y, z)
                FreeMc.console().writeList([
                f"execute at {self.name} positioned ~ 213 ~ run fill ~-4 ~7 ~-4 ~4 ~-2 ~-2 minecraft:bedrock",
                f"execute at {self.name} positioned ~ 213 ~ run fill ~-4 ~7 ~-4 ~-2 ~-2 ~4 minecraft:bedrock",
                f"execute at {self.name} positioned ~ 213 ~ run fill ~4 ~7 ~-4 ~2 ~-2 ~4 minecraft:bedrock",
                f"execute at {self.name} positioned ~ 213 ~ run fill ~4 ~7 ~4 ~-4 ~5 ~-4 minecraft:bedrock",
                f"execute at {self.name} positioned ~ 213 ~ run fill ~-4 ~-2 ~4 ~4 ~ ~-4 minecraft:bedrock",
                f"execute at {self.name} positioned ~ 213 ~ run fill ~4 ~-2 ~4 ~-4 ~7 ~2 minecraft:bedrock",
                f"tp {self.name} ~ 213 ~"
            ])

        def unjail(self):
            if not self.jail_info.get('jailed'):
                return # not jailed
            
            coords = self.jail_info['coords']
            self.tp(coords)
            self.jail_info['jailed'] = False
            self.jail_info['coords'] = None
            FreeMc.console().write(f"execute at {self.name} positioned ~ 213 ~ run fill ~4 ~-2 ~-4 ~-4 ~7 ~4 air")

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
            
        def on_console_message(self, func):
            def wrapper(self, *args, **kwargs):
                global watch
                watch['on_msg'] = func
                result = func(*args, **kwargs)
                return result
            return wrapper

        def on_join(self, func):
            global watch
            watch['on_join'] = func
            def wrapper(self, *args, **kwargs):
                result = func(*args, **kwargs)
                return result
            return wrapper

        def on_leave(self, func):
            global watch
            watch['on_leave'] = func
            def wrapper(self, *args, **kwargs):
                result = func(*args, **kwargs)
                return result
            return wrapper

        def trigger_event(self, msg):
            global watch
            if not isinstance(msg, str):
                return
            if 'on_msg' in watch:
                watch['on_msg'](msg)

            if 'on_join' in watch and msg.find("joined the game") > -1: # returns a user instance of the player who joined
                reg = r"([a-zA-Z0-9._]+) joined the game"
                match = re.search(reg, msg, re.MULTILINE)

                name = (match and match.group(1))
                user = FreeMc.user(name)
    
                watch['on_join'](user)

            if 'on_leave' in watch and msg.find("left the game") > -1: # returns a user instance of the player who left
                reg = r"([a-zA-Z0-9._]+) left the game"
                match = re.search(reg, msg, re.MULTILINE)

                name = (match and match.group(1))
                user = FreeMc.user(name)
                watch['on_leave'](user)

