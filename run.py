import subprocess
import os

arguments = ["./RustDedicated"]

def addArgument(key, value):
    if (os.environ("LD_LIBRARY_PATH") != ""):
        arguments.append(key)
        arguments.append(value)

while True:
    subprocess.call([
        "steamcmd", "+force_install_dir", "/data", "+login", "anonymous", "+app_update", "258550", "validate", "+quit"
    ])

    addArgument("+server.ip", "SERVER_IP")
    addArgument("+server.port", "SERVER_PORT")
    addArgument("+server.queryport", "SERVER_QUERY_PORT")
    addArgument("+rcon.ip", "RCON_IP")
    addArgument("+rcon.port", "RCON_PORT")
    addArgument("+rcon.password", "RCON_PASSWORD")
    addArgument("+rcon.web", "RCON_WEB")
    addArgument("+server.tickrate", "SERVER_TICK_RATE")
    addArgument("+server.hostname", "SERVER_HOSTNAME")
    addArgument("+server.headerimage", "SERVER_HEADER_IMAGE")
    addArgument("+server.identity", "SERVER_IDENTITY")
    addArgument("+server.seed", "SERVER_SEED")
    addArgument("+server.maxplayers", "SERVER_MAX_PLAYERS")
    addArgument("+server.worldsize", "SERVER_WORLD_SIZE")
    addArgument("+server.saveinterval", "SERVER_SAVE_INTERVAL")
    addArgument("+server.level", "SERVER_LEVEL")
    addArgument("+server.url", "SERVER_URL")
    addArgument("+server.description", "SERVER_DESCRIPTION")
    addArgument("+server.tags", "SERVER_TAGS")
    addArgument("+server.logoimage", "SERVER_LOGO_IMAGE")
    addArgument("+app.port", "APP_PORT")

    additionalParams = os.environ("ADDITIONAL_PARAMS")
    if ( additionalParams != ""):
        arguments.append(additionalParams)
    print("Server starting...")

    subprocess.call(
        arguments,
        cwd="/data",
        env={"LD_LIBRARY_PATH": os.environ("LD_LIBRARY_PATH") + ":/data/RustDedicated_Data/Plugins:/data/RustDedicated_Data/Plugins/x86_64"}
    )

    print("Server stopped.")
