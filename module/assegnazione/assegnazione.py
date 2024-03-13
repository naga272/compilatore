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


'''
    *
    *   Questa variabile ha il compito di stabile in che posizione all'interno dello stack 
    *   una variabile va creata. Di default ho deciso che gli interi sono composti da 8 byte (qword)
    *
'''
rbp = 0 


def recognize_type_var(row:str, n_line:int) -> str:
    ''' controllo se nella riga c'è un commento '''
    commento = ""

    commento_match = re.search(commento_re, row)
    if commento_match:
        commento = commento_match.group().replace("//", " ;")


    row = re.sub(commento_re, "", row)
    tokenize = re.split(r"\s*=", row)

    tokenize[VALUE] = re.sub("\n$", "", tokenize[VALUE])

    # devo togliere il \n e \s solo alle espressioni matematiche, non anche alle stringhe
    # quindi controllo che VALUE non sia una stringa
    if (not re.fullmatch(stringa, tokenize[VALUE])): 
        tokenize[VALUE] = re.sub("(\s*\n*)*", "", tokenize[VALUE])

    ''' fine controllo se nella riga c'è un commento '''

    global rbp

    # formato memory_register = { chiave : [value, stack_position] }

    # caso espressioni matematiche only num    
    stringa_assembly = ""
    if re.fullmatch(espressione_matematica, tokenize[VALUE]):
        rbp += 8
        memory_register[tokenize[KEY]] = [eval(tokenize[VALUE]), rbp] 

        # mov qword [ebp - 16], [-3, 16]
        stringa_assembly = f"\n\tsub rsp, 8 {commento}\n\t"
        stringa_assembly += f"mov qword [rbp - {memory_register[tokenize[KEY]][1]}], {memory_register[tokenize[KEY]][0]}" 

        return stringa_assembly

    # caso espressioni matematiche con variabili incorporate
    if re.match(var_name, tokenize[VALUE]):
        for element in re.match(var_name, tokenize[VALUE]).group(): 
            if element in memory_register:
                #print(element)
                tokenize[VALUE] = tokenize[VALUE].replace(element, str(memory_register[element][0]))
            else:
                print("error at line", n_line, ":", row)
                sys.exit(1)

        rbp += 8
        memory_register[tokenize[KEY]] = [eval(tokenize[VALUE]), rbp] 
        stringa_assembly = f"\n\tsub rsp, 8 {commento}\n\t"
        stringa_assembly += f"mov qword [rbp - {memory_register[tokenize[KEY]][1]}], {memory_register[tokenize[KEY]][0]}" 
        return stringa_assembly

    # caso assegnazione stringa
    if re.fullmatch(stringa, tokenize[VALUE]):
        return f""


    print(f"error: at line: {n_line}\n\tunknow command: -> {row}")
    sys.exit(1)



def fast_assigment(row, n_line) -> str:
    """
        ; Dichiarazione di variabili locali per la somma
        sub esp, 4    ; Spazio per la prima variabile (4 byte)

        ; Inizializzazione delle variabili
        mov dword [rbp-4], 10       ; Prima variabile

        ; Somma delle variabili
        add dword [rbp-4], 14        ; Carica la prima variabile in eax
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

        if re.match(var_name, tokenize[VALUE]):

            for element in re.match(var_name, tokenize[VALUE]).group():
                if element in memory_register:
                    tokenize[VALUE] = tokenize[VALUE].replace(element, str(memory_register[element][0]))
                else:
                    print("error at line", n_line, "\nundeclared variable:\n\t", row)

        result = eval(tokenize[VALUE])    
        print(memory_register[tokenize[KEY]][1], rbp)
        assembly_result += f"\tadd qword [rbp - {rbp - memory_register[tokenize[KEY]][1]}], " + str(result)

        return assembly_result

    print("error at line", n_line, ":\n\t", row)
    sys.exit(1)

