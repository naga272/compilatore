
from .section.text          import text, function_main_end, other_function
from .assegnazione.data     import data
from .section.bss           import bss

from .assegnazione.assegnazione import *
from .statements.statements import while_statement, while_statement_end
from .funzioni.print import *
from .regex import *

import platform
import sys
import os
import re


def to_asm(row:str, n_line:int) -> int:
    global text, data

    if re.fullmatch(r"\s*\n*", row): # caso linea vuota
        return 0

    if re.fullmatch(commento_re, row): # caso commento
        return 0

    if re.match(assegnamento, row): # caso assegnazione valori a variabile
        text += recognize_type_var(row, n_line) # funzione effettiva per creare l'assegnamento in asm
        return 0 

    if re.fullmatch(costanti, row): # caso costanti
        if not re.search(var_name, costanti).group() in memory_register:
            text += "\n\t" + row.replace("//", ";")
            return 0

    if re.fullmatch(fast_add, row): # operation like a += 12 + 25 ...
        text += fast_assigment(row, n_line)
        return 0

    if re.match(r"\s*while\s*\(.+\)\s*\n*", row): # while statement case
        text += while_statement(row, n_line)
        return 0

    if re.match(r"\s*endwhile", row):
        text += while_statement_end(row, n_line)
        return 0

    if re.match(r"\s*fork\s*\(\s*\)\s*\n?", row):
        text += "\n\tmov rax, 57 ; fork()\n"
        text += "\tsyscall\n"
        return 0

    return 1


def translate_to_asm(sorgente_file:str):
    counter = 1
    #try:
    with open(sorgente_file, "r") as sorgente:

        for line in sorgente:
            if to_asm(line, counter) == 0:
                counter += 1
            else:
                return counter

    with open(sorgente_file[:-4] + "asm", "w") as nasm:
        nasm.write(f"{bss}\n{data}\n{text}{function_main_end}{other_function}")

    return 0
