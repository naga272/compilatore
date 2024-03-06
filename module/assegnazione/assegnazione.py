from ..regex                    import *
from ..section.bss              import *
from .data                      import data
from ..section.text             import *
import sys


"""

    creazione variabili in file .volt:
    key = value

    in assembly:
    
    my_byte     db 42       ; byte:         8 bit
    my_word     dw 1000     ; word:         16 bit
    my_dword    dd 100000   ; double word:  32 bit
    my_qword    dq 1000000  ; quad word:    64 bit

"""


KEY = 0
VALUE = 1


def recognize_type_var(row:str, n_line:int) -> str:
    # controllo se nella riga c'è un commento
    commento = ""

    commento_match = re.search(commento_re, row)
    if commento_match:
        commento = commento_match.group().replace("//", " ;")


    row = re.sub(commento_re, "", row)
    tokenize = re.split("\s=\s", row)


    # devo togliere il \n e \s solo alle espressioni matematiche, non anche alle stringhe
    # quindi controllo che VALUE non sia una stringa
    if (not re.fullmatch(stringa, tokenize[VALUE])): 
        tokenize[VALUE] = re.sub("(\s*\n*)*", "", tokenize[VALUE])


    # caso espressioni matematiche only num
    if re.fullmatch(espressione_matematica, tokenize[VALUE]):
        memory_register[tokenize[KEY]] = eval(tokenize[VALUE])

        return f"\t{tokenize[KEY]} dq {memory_register.get(tokenize[KEY], 0)} {commento}\n"


    # caso espressioni matematiche con variabili incorporate
    if re.match(var_name, tokenize[VALUE]):
        
        # Sostituisci solo le variabili esistenti nel dizionario memory_register
        for element in re.match(var_name, tokenize[VALUE]).group():
            if element in memory_register:
                tokenize[VALUE] = tokenize[VALUE].replace(str(element), str(memory_register[element]))
            else:
                print(memory_register)
                print(f"error: at line: {n_line}\n\tundeclared variable: -> {row}")
                sys.exit(1)

        memory_register[tokenize[KEY]] = eval(tokenize[VALUE])
        return f"\t{tokenize[KEY]} dq {memory_register.get(tokenize[KEY], 0)} {commento}\n"


    # caso assegnazione stringa
    if re.fullmatch(stringa, tokenize[VALUE]):
        memory_register[tokenize[KEY]] = tokenize[VALUE] 
        return f"\t{tokenize[KEY]} dq {tokenize[VALUE][:-1]}, 0 {commento}\n"

    print(f"error: at line: {n_line}\n\tunknow command: -> {row}")
    sys.exit(1)



def fast_assigment(row, n_line) -> str:
    """
        ; e' possibile assegnare velocement solo numeri
        x += (n), dove n è una espressione matematica:
        
        add  dword [x], n
    """
    assembly_result = """\n""" # finira tutto all'interno di section .text
    
    
    # controllo se nella riga c'è un commento
    commento = ""

    commento_match = re.search(commento_re, row)
    if commento_match:
        commento = commento_match.group().replace("//", " ;")
        assembly_result + commento + "\n"

    row = re.sub(commento_re, "", row)
    tokenize = re.split("\s*\+=\s*", row)
    
    # controllo se esiste la variabile
    if tokenize[KEY] in memory_register: 

        result = eval(tokenize[VALUE])    
        assembly_result += f"\tadd qword [{tokenize[KEY]}], " + str(result)
        
        return assembly_result

    print("error at line", n_line, ":\n\t", row)
    sys.exit(1)

