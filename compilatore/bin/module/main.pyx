
import cython
from libc.stdlib    cimport EXIT_SUCCESS, EXIT_FAILURE, system

from .regole        import *       # syntax_var[]

from .sezioni_asm   import *

from datetime       import datetime
import platform
import time
import sys
import os
import re


def add_varInt_to_data(row:str) -> str:
    '''
        *
        * procedura che aggiunge alla section .data del file assembly la variabile intera creata
        *
    '''
    analisi_row = row.split("=")
    translate_to_asm = f"\t{analisi_row[0]} db {analisi_row[1])}"
    return str(translate_to_asm).replace("//", ";")


def add_varChr_to_data(row:str) -> str:
    '''
        *
        * procedura che aggiunge alla section .data del file assembly la variabile stringa creata
        * e crea un'altra variabile nel file assembly contenente la lunghezza della stringa.
        * Quindi nel programma ci sara:
        *
        * msg db "Hello World", 0       ; vettore
        * msg_size equ $ - msg          ; lunghezza vettore
        *
    '''
    analisi_row = re.split("\s*=\s*", row)
    analisi_row[1] = analisi_row[1][:-1] if analisi_row[1][len(analisi_row[1]) - 1] == "\n" else analisi_row[1] # fixo il \n della stringa che da problemi nel file asm
    translate_to_asm = f"\t{analisi_row[0]} db {analisi_row[1]}, 0" 
    # dichiarazione stringa + lunghezza stringa
    return str(translate_to_asm).replace("//", ";")



cdef unsigned long int to_asm(row, n_row):
    '''
        *
        *   Funzione che ha il compito di tradurre riga per riga il codice sorgente in codice assembly
        *
    '''
    #caso assegnazione di una espressione matematica o a un solo intero a una variabile
    if re.fullmatch(syntax_var[0] + syntax_var[1] + syntax_var[3] + commento, row) != None:
        sezioni_asm[1] += add_varInt_to_data(row)
        print("match")

    #caso assegnazione di una stringa a una variabile
    elif re.fullmatch(syntax_var[0] + syntax_var[1] + syntax_var[2] + commento, row) != None:
        sezioni_asm[1] += add_varChr_to_data(row)
        print("match")
    
    # caso in cui la riga e' vuota
    elif re.fullmatch(void_row, row):
        print("match")

    # caso in cui la riga e' un commento
    elif re.fullmatch(commento, row):
        print("match")

    else:
        print(f"syntax error at line {n_row}:\n {row}")
        return EXIT_FAILURE

    return EXIT_SUCCESS



def main(argc:int, argv:list) -> int:
    """
        argv[0]: nome programma compilatore
        argv[1]: nome programma sorgente
        argv[2]: nome eseguibile in output
        argv[3]: tipo di architettura (per ora si accettano solo cpu con registri x64)
    """
    cdef unsigned long int counter_line
    #try:
    if True:
        sorgente_asm   = argv[1].replace(".sor", ".asm")
        sorgente_obj   = sorgente_asm.replace(".asm", ".o")


        with open(argv[1], "r") as fread:
            counter_line = 0

            for row in fread:
                counter_line += 1

                if to_asm(row, counter_line) != EXIT_SUCCESS: # qui avviene la traduzione della riga in codice asm
                    return EXIT_FAILURE


        with open(sorgente_asm, "w") as fasm:       # crezione file sorgente assembly
            fasm.write(f"\n{sezioni_asm[0]}\n{sezioni_asm[1]}\n{sezioni_asm[2]}\n\n{sezioni_asm[3]}\n\n\n")

        # comandi per la call system
        command_x_compile   = f"nasm -f elf64 -g {sorgente_asm}".encode('utf-8')
        command_x_linking   = f"ld -g -e _start {sorgente_obj} -o {argv[2]}".encode('utf-8')

        #verifica dei risultati delle chiamate
        if system(command_x_compile) == EXIT_SUCCESS:           # compilazione programma assembly
            print("assemblaggio completato")

            if system(command_x_linking) == EXIT_SUCCESS:       # linking del file object
                print("link completato")
            else:
                print("errore durante il linking")
                return EXIT_FAILURE
        else:
            print("errore durante l'assemblaggio")
            return EXIT_FAILURE

        return EXIT_SUCCESS
    '''
    except Exception as e:
        print(f"error in function main: {e}")
        return EXIT_FAILURE
    '''
