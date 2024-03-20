
from module.traduttore import *

import subprocess
import platform
import sys
import os
import re


check = 1


def system(argument:list) -> int:
    '''
        *
        * Funzione che passata una lista di comandi come parametro lo esegue su shell
        * Prototype: int system(const char* string);
        * Ritorna EXIT_FAILURE se qualcosa e' andato storto, EXIT_SUCCESS se e' andato tutto bene 
        *
    '''
    try:
        # avvio un nuovo processo con Popen. Mi restituisce un oggetto che rappresenta il processo in esecuzione
        process = subprocess.Popen(argument, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        """
            Argv di Popen:
                - argument: Specifica il programma da eseguire e i suoi argv. Può esssere una stringa oppure una lista
                - stdin, stdout, stderr: Questi parametri specificano i canali di input, output e errori del processo, rispettivamente.
                                         Se non vengono specificati, vengono utilizzati i valori predefiniti.
                - shell: Se impostato su True, il comando viene eseguito tramite una shell del S.O.
        """
        output, error = process.communicate()

        if process.returncode == 0:
            # diciamo che il risultato delle operazioni del processo creato devono essere codificate in UTF-8, 
            # perchè di default restituisce una sequenza di byte
            print(output.decode('utf-8'))  
            return 0
        else:
            # comunicazione dell'errore
            print("Error:", error.decode('utf-8'))
            return 1
    
    except Exception as e:
        # comunicazione caso speciale
        print(f"Exception: {e}")
        return 0


def main(argc:int, argv:list) -> int:
    """
        argv[0]: compiler.py
        argv[1]: name_file.volt 
        argv[2]: name_file.exe
        argv[3]: architettura cpu x64
    """
    if "x64" in sys.argv and getattr(platform, "architecture")()[0] == "64bit": 

        if re.fullmatch(r".+\.volt", str(argv[1])) == None:
            print(f"errore nel nome o estensione del file sorgente {argv[1]}")
            return 1
        
        else:
            signal_code = translate_to_asm(argv[1])

            if signal_code == 0:
                print("translation from .volt to .asm complete")

                sorgente_asm    = re.sub(r"\.volt", ".asm", argv[1])
                sorgente_o      = re.sub(r"\.volt", ".o", argv[1])
                
                if check == 1:

                    if system(["nasm", "-f", "elf64", "-o", sorgente_o, sorgente_asm]) == 0:
                        if system(["ld", sorgente_o, "-o", argv[2]]) == 0:
                            print("complete linking")
                            return 0

                        print(f"error during the linking of the file {sorgente_o}")
                        sys.exit(1)

                    else:
                        print(f"error during the compilation of the file {sorgente_asm}")
                
                else:
                    print("operazione completata")
                    return 0
            else:
                print(f"error during the translation of the file: {argv[1]} in assembly language, cause source code at line:{signal_code}")

            sys.exit(1)

    else:
        print("error! compiler not compatible for cpu x32")
        sys.exit(1)


if __name__ == "__main__":
    result = 1
    if check == 1:
        if platform.system() == "Linux":
            result = main(len(sys.argv), sys.argv)
        else:
            print("impossibile avviare il programma con sistema operaativo: ", platform.system())
    else:
        result = main(len(sys.argv), sys.argv)
    
    print(f"uscita dal programma con valore {result}")    
    sys.exit(result)
