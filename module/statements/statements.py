from ..regex import *
import platform
import os
import sys
import re


"""

    NOTA BENE: risolvere l'espressione è compito della cpu, non tuo

    - Per ora implementate le basi del ciclo while e dell'if.

    ecco un esempio:

    while (condition)
        <instruction>
    endwhile

    if (condition)
        if (condition)
            <instruction>
        endif
    else do
        <instruction>
    endif

"""


"""

    algoritmo per distinguere i tree degli if e dei while 
    []
    if 4 > 10:          [1]
        if 10 < 21:     [1, 2]
            a = 0       [1, 2]
        endif           [1]
    else do             [1]
        if 12 < 13:     [1, 2]
            c = 12      [1, 2]
        else do         [1, 2]
            b = 0       [1, 2]
        endif           [1]
    endif               []

    a ogni endif a signal_if viene estratto il numero identificativo per quel if, 
    che verra usato per l'etichetta

    esempio:
        
        cmp rax, 0
        jz  etichetta   ; se zero va a etichetta altriementi esegue tutte le istruzioni
                        ; e poi quando arriva jmp end_etichetta fa il salto
                        ; sostanzialmente in questa funzione viene implementato questo

        jmp end_etichetta
        etichetta: ; condizione vera (if)

        end_etichetta:

"""

"""

    (condition)

    PROBLEMA:
        E POSSIBILE DARE IN PASTO ALLA CONDIZIONE SOLO ESPRESSIONI 
        MATEMATICHE SENZA VARIABILI AL MOMENTO


    tipi di condizioni implementate

    jz, je      -> jump if zero, jump if equal 
    jnz, jne    -> jump if not zero, jump if not equal
    js          -> jump if signed (Negativo) 
    jns         -> jump if not signed (Negativo)


    tipi di condizioni non implementate
    jc          -> jump if carry flag
    jnc         -> jump if not carry flag
    jo          -> jump if overflow
    jno         -> jump if not overflow
    jp, jpe     -> jump if parity, jump if parity is even
    jnp, jpo    -> jump if not parity, jump if parity is Odd


"""


signal_while = []
signal_if    = []



def while_statement(row:str, n_row:int) -> str:

    global signal_while

    signal_while.append(n_row)

    while_to_asm = f"\n\n\twhile_row_{n_row}:\t"

    condizione = re.sub("\s*while\s*\(", "", row)
    condizione = re.sub("(\)\s*)$", "", condizione)

    stringa = re.search(r"(\>=)|(\<=)|(==)|(\>)|(\<)|(\!=)", condizione)

    condizione = condizione.split(stringa.group())
    uno = condizione[0].strip().split() 
    due = condizione[1].strip().split()
    
    if stringa.group() == "==":
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjnz while_out_row_{n_row}\n"

    if stringa.group() == ">=":
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjs while_out_row_{n_row}\n"
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjnz while_out_row_{n_row}\n"

    if stringa.group() == ">":
        while_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        while_to_asm += f"\n\tjs while_out_row_{n_row}\n"

    if stringa.group() == "<":
        while_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        while_to_asm += f"\n\tjns while_out_row_{n_row}\n"

    if stringa.group() == "<=":
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjns while_out_row_{n_row}\n"
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjnz while_out_row_{n_row}\n"

    if stringa.group() == "!=":
        while_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        while_to_asm += f"\n\tjz while_out_row_{n_row}\n"

    return f"\n\t; ciclo while della riga {n_row}" + while_to_asm

 
def while_statement_end(row:str, n_line:int) -> str:
    global signal_while

    repeat = f"\n\n\tjmp while_row_{signal_while[len(signal_while) - 1]}\n"
    repeat += f"\twhile_out_row_{signal_while.pop()}:\n\n"

    return repeat


def if_tree(row:str, n_row:int) -> str:
    global signal_if

    signal_if.append(n_row)
    if_to_asm = f"\n\t; if del programma sorgente che si trova a riga {n_row}\n"

    condizione = re.sub("\s*if\s*\(", "", row)
    condizione = re.sub("(\)\s*)$", "", condizione)

    stringa = re.search(r"(\>=)|(\<=)|(==)|(\>)|(\<)|(\!=)", condizione)
    #print(stringa)
    #memory_register

    condizione = condizione.split(stringa.group())

    uno = condizione[0].strip().split() 
    due = condizione[1].strip().split()
    
    if stringa.group() == "==":
        if_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        if_to_asm += f"\n\tjnz if_out_row_{n_line}\n"

    if stringa.group() == ">=":
        if_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        if_to_asm += f"\n\tjs if_out_row_{n_row}"
        if_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        if_to_asm += f"\n\tjnz if_out_row_{n_row}\n"

    if stringa.group() == ">":
        if_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        if_to_asm += f"\tjs if_out_row_{n_row}\n"

    if stringa.group() == "<":
        if_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        if_to_asm += f"\tjns if_out_row_{n_row}\n"

    if stringa.group() == "<=":
        if_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        if_to_asm += f"\tjns if_out_row_{n_row}\n"
        if_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        if_to_asm += f"\tjnz if_out_row_{n_row}\n"

    if stringa.group() == "!=":
        if_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        if_to_asm += f"\tjz if_out_row_{n_row}\n"

    return "\n\n" + if_to_asm


def else_do_tree(row:str, n_row:int) -> str:
    #print("sono signal_if:", signal_if)
    before_do_tree_after = f"\n\tjmp if_out_row_{signal_if[len(signal_if) - 1]}\n"
    before_do_tree_after += f"\telse_do_tree_{signal_if[len(signal_if) - 1]}:\n"

    return before_do_tree_after


def endif_statement(row:str, n_row:int) -> str:
    endif = f"\n\tif_out_row_{signal_if.pop()}:\n"
    return endif
