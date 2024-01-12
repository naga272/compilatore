from module.main import *


import os
import sys
import platform
import re
import time
from datetime import datetime


"""
    *
    *   programma:  Compilatore with python
    *   author:     Bastianello Federico
    *   data:       11 / 01 / 2024
    *
"""



def log(file_log, file_py) -> int:
    """
        *
        * traccio all'interno della cartella log tutte le volte che viene eseguito il compilatore
        *
    """
    try:
        with open(file_log, "a") as flog:
            flog.write(f"data:{datetime.now()};versione py: {sys.version};name program: {file_py};\n")
        return 0
    except Exception as e:
        return 1


if __name__ == "__main__":
    result = 1
    if log("../log/trace.csv", sys.argv[0]) == 0:

        print("architettura macchina:", getattr(platform, 'architecture')()[0])
        
        if "x64" in sys.argv and getattr(platform, "architecture")()[0] == "64bit": 
            result = main(len(sys.argv), sys.argv)
        else:
            print("errore! compilatore solo per cpu con architettura x64")

    if result == 0:
        print("file compilato con successo")
    else:
        print("errore durante la compilazione del file")

    sys.exit(result)

