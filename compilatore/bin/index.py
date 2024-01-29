from module.main    import *
from module.regole  import *

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

        # print("architettura macchina:", getattr(platform, 'architecture')()[0])
        '''
            *
            *   Verifico il tipo di architettura (x64), 
            *   i parametri passati al programma, 
            *   nome del file sorgente da analizzare.
            *
        '''
        if "x64" in sys.argv and getattr(platform, "architecture")()[0] == "64bit": 
            if re.fullmatch(name_file_sr[0], sys.argv[1]) == None:
                print("errore nel nome o estensione del sorgente: ", argv[1])
            else:
                result = main(len(sys.argv), sys.argv)
        else:
            print("errore! compilatore solo per cpu con architettura x64")

    sys.exit(result)

