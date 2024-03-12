from ..regex import *
import platform
import os
import sys
import re


"""
    i cicli while in questo linguaggio devono avere la seguente sintassi

    while (condition)
        <instruction>
    endwhile


    if (condition)

    endif

    (condition)

    jz, je      -> jump if zero, jump if equal 
    jnz, jne    -> jump if not zero, jump if not equal
    jc          -> jump if carry flag
    jnc         -> jump if not carry flag
    jo          -> jump if overflow
    jno         -> jump if not overflow
    js          -> jump if signed (Negativo) 
    jns         -> jump if not signed (Negativo)
    jp, jpe     -> jump if parity, jump if parity is even
    jnp, jpo    -> jump if not parity, jump if parity is Odd
"""


signal_start_while = 0


def while_statement(row:str, n_row:int) -> str:

    global signal_start_while

    signal_start_while = n_row

    while_to_asm = f"\n\n\twhile_row_{n_row}:\t"

    condizione = re.sub("\s*while\s*\(", "", row)
    condizione = re.sub("(\)\s*)$", "", condizione)

    stringa = re.search(r"(\>=)|(\<=)|(==)|(\>)|(\<)|(\!=)", condizione)
    print(stringa)
    #memory_register

    # print(row.split(str(stringa)))
    condizione = condizione.split(stringa.group())
    print(condizione)
    uno = condizione[0].strip().split() 
    due = condizione[1].strip().split()
    
    print(uno, due)
    
    
    if stringa.group() == "==":
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjnz while_out_row_{signal_start_while}\n"

    if stringa.group() == ">=":
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjs while_out_row_{signal_start_while}\n"
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjnz while_out_row_{signal_start_while}\n"

    if stringa.group() == ">":
        while_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        while_to_asm += f"\n\tjs while_out_row_{signal_start_while}\n"

    if stringa.group() == "<":
        while_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        while_to_asm += f"\n\tjns while_out_row_{signal_start_while}\n"

    if stringa.group() == "<=":
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjns while_out_row_{signal_start_while}\n"
        while_to_asm += f"\n\tcmp {eval(condizione[0])}, {eval(condizione[1])}"
        while_to_asm += f"\n\tjnz while_out_row_{signal_start_while}\n"

    if stringa.group() == "!=":
        while_to_asm += f"\tcmp {eval(condizione[0])}, {eval(condizione[1])}\n"
        while_to_asm += f"\n\tjz while_out_row_{signal_start_while}\n"

    return while_to_asm

 
def while_statement_end(row:str, n_line:int) -> str:
    global signal_start_while
    repeat = f"\n\n\tjmp while_row_{signal_start_while}\n"
    repeat += f"\twhile_out_row_{signal_start_while}:\n\n"

    signal_start_while = 0
    return repeat

