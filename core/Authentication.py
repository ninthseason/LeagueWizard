import os
import re
import time

import psutil

base_dir = os.path.dirname(__file__)


class ClientData:
    port: int = 0
    pid: int = 0
    password: str = ""
    try:
        with open(base_dir + "/riotgames.pem", "r") as cert:
            certificate: str = cert.read()
    except FileNotFoundError:
        print("[Warning]未找到证书，连接将不安全")
        certificate: str = ""

    def __init__(self):
        self.fetch()

    def fetch(self) -> None:
        """
        Get data from LeagueClient (Game start required)
        """
        for process_id in psutil.pids():
            try:
                process = psutil.Process(process_id)
            except psutil.NoSuchProcess:
                continue
            if process.name() == "LeagueClientUx.exe":
                cmdline = str(process.cmdline())
                self.pid = int(re.findall(r"--app-pid=(.*?)'", cmdline)[0])
                self.port = int(re.findall(r"--app-port=(.*?)'", cmdline)[0])
                self.password = re.findall(r"--remoting-auth-token=(.*?)'", cmdline)[0]
                return

        print("未检测到游戏，将在5秒后重试")
        time.sleep(5)
        self.fetch()

    def __str__(self):
        return f"Port: {self.port}\nPid: {self.pid}\nPassword: {self.password}"


# 单例
ClientData = ClientData()
