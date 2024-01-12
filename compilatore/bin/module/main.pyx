
import cython
from libc.stdlib    cimport EXIT_SUCCESS, EXIT_FAILURE, system


from .regole         import *
from .sezioni_asm    import *       # contiene section_bss, section_data, section_text


from datetime       import datetime
import platform
import time
import sys
import os
import re


def main(argc:int, argv:list) -> int:
    """
        argv[0]: nome programma compilatore
        argv[1]: nome programma sorgente
        argv[2]: nome eseguibile in output
        argv[3]: tipo di architettura (per ora si accettano solo cpu con registri x64)
    """
    try:

        if re.fullmatch(name_file_sr[0], argv[1]) == None:
            print("errore nel nome o estensione del sorgente: ", argv[1])
            return EXIT_FAILURE

        sorgente_asm   = argv[1].replace(".sor", ".asm")
        sorgente_obj   = sorgente_asm.replace(".asm", ".o")

        with open(argv[1], "r") as fread:
            print(fread.readlines())


        print(sorgente_asm)
        with open(sorgente_asm, "w") as fasm:
            fasm.write(f"{section_bss}\n{section_data}\n{section_text}")

        
        command_x_compile   = f"nasm -f elf64 -g {sorgente_asm}".encode('utf-8')
        command_x_linking   = f"ld -g -e _start {sorgente_obj} -o {argv[2]}".encode('utf-8')

        system(command_x_compile)                   # compilazione programma assembly
        system(command_x_linking)                   # linking del file object

        return EXIT_SUCCESS

    except Exception as e:
        print(f"{e}")
        return EXIT_FAILURE


