import inspect
import sys
from src.main.scripts.functions.core.myExceptions import NoAccessFromFile
import src.main.scripts.functions.core.core as core

if __name__ == '__main__':
    core.coreInitConfig(str(__file__))

    logger = core.getLogger("salu2")
    logger.error("AAAAa")

    config = core.readConfig()
    print(config["DEFAULT"]["os_name"])

    print("OK")
