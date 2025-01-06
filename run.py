import subprocess
import os
import sys
import re

def addArgument(serverConfig, arguments, key, env, **kwargs):
    if env not in os.environ:
        return
    if "addToServerConfig" not in kwargs or kwargs["addToServerConfig"]:
        serverConfig[key] = os.environ[env]
    if "addToCmd" not in kwargs or kwargs["addToCmd"]:
        value = os.environ[env]
        if " " in value and value[0] != "\"" and value[len(value) - 1 ] != "\"":
            value = "\"" + value + "\""
        arguments.append("+" + key)
        arguments.append(value)


def ReadServerConfig(configFilepath, serverConfig):
    try:
        f = open(configFilepath, "r")
        for line in f.read().split("\n"):
            m = re.match(r"^(\\S+) \"(.+)\"$", line)
            if m == None:
                print("Failed to parse line in config file %s: %s" % (configFilepath, line), file=sys.stderr)
                return False
            serverConfig[m.group(1)] = m.group(2)
        print("Readed server config: %s" % serverConfig, file=sys.stdout)
    except OSError:
        print("Failed to open server config file %s" % configFilepath, file=sys.stderr)
        return False
    return True


def WriteServerConfig(configFilepath, serverConfig):
    try:
        f = open(configFilepath, "w")
        for key, value in serverConfig.items():
            f.write("%s \"%s\"\n" % (key, value))
    except OSError:
        print("Failed to write server config file %s" % configFilepath, file=sys.stderr)
        return False
    return True


if "SERVER_IDENTITY" not in os.environ:
    print("You should specify \"SERVER_IDENTITY\" environment variable.", file=sys.stderr)
    exit(1)

configDirpath = "/data/server/%s/cfg" % os.environ["SERVER_IDENTITY"]
configFilepath = "%s/server.cfg" % configDirpath
ldLibraryPath = os.environ["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in os.environ != None else ""

os.makedirs(configDirpath, exist_ok=True)

while True:

    print("Server updating...", file=sys.stdout)

    subprocess.call([
        "steamcmd", "+force_install_dir", "/data", "+login", "anonymous", "+app_update", "258550", "validate", "+quit"
    ])

    arguments = ["./RustDedicated"]
    serverConfig = {}

    ReadServerConfig(configFilepath, serverConfig)

    addArgument(serverConfig, arguments, "server.hostname", "SERVER_HOSTNAME", addToCmd = False)
    addArgument(serverConfig, arguments, "server.headerimage", "SERVER_HEADER_IMAGE", addToCmd = False)
    addArgument(serverConfig, arguments, "server.level", "SERVER_LEVEL", addToCmd = False)
    addArgument(serverConfig, arguments, "server.url", "SERVER_URL", addToCmd = False)
    addArgument(serverConfig, arguments, "server.description", "SERVER_DESCRIPTION", addToCmd = False)
    addArgument(serverConfig, arguments, "server.tags", "SERVER_TAGS", addToCmd = False)
    addArgument(serverConfig, arguments, "server.logoimage", "SERVER_LOGO_IMAGE", addToCmd = False)
    addArgument(serverConfig, arguments, "server.motd", "SERVER_MOTD", addToCmd = False)

    addArgument(serverConfig, arguments, "server.ip", "SERVER_IP")
    addArgument(serverConfig, arguments, "server.port", "SERVER_PORT")
    addArgument(serverConfig, arguments, "server.queryport", "SERVER_QUERY_PORT")
    addArgument(serverConfig, arguments, "rcon.ip", "RCON_IP")
    addArgument(serverConfig, arguments, "rcon.port", "RCON_PORT")
    addArgument(serverConfig, arguments, "rcon.password", "RCON_PASSWORD")
    addArgument(serverConfig, arguments, "rcon.web", "RCON_WEB")
    addArgument(serverConfig, arguments, "server.tickrate", "SERVER_TICK_RATE")
    addArgument(serverConfig, arguments, "server.identity", "SERVER_IDENTITY")
    addArgument(serverConfig, arguments, "server.seed", "SERVER_SEED")
    addArgument(serverConfig, arguments, "server.maxplayers", "SERVER_MAX_PLAYERS")
    addArgument(serverConfig, arguments, "server.worldsize", "SERVER_WORLD_SIZE")
    addArgument(serverConfig, arguments, "server.saveinterval", "SERVER_SAVE_INTERVAL")
    addArgument(serverConfig, arguments, "app.port", "APP_PORT")

    if not WriteServerConfig(configFilepath, serverConfig):
        exit(1)

    if "ADDITIONAL_PARAMS" in os.environ:
        arguments.append(os.environ["ADDITIONAL_PARAMS"])
        
    print("Server starting...", file=sys.stdout)

    subprocess.call(
        arguments,
        cwd="/data",
        env={"LD_LIBRARY_PATH":  ldLibraryPath + ":/data/RustDedicated_Data/Plugins:/data/RustDedicated_Data/Plugins/x86_64"}
    )

    print("Server stopped.", file=sys.stdout)
