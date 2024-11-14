
import subprocess
import time
import sys
import re
import os


macro = """

%macro gxor 0
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
%endmacro

%define stdin 0
%define stdout 1
%define stderr 2
"""

section_bss = """
section .bss
"""

section_data = """
section .data
    errno db 0
    void_print db "print none", 0
"""

section_text = """
section .text
    global _start


_start:  gxor
         call main
_exit(): mov rdi, rax
         mov rax, 60
         syscall

main:   push rbp
        mov rbp, rsp

"""

section_fn = """
; le funzioni vanno aggiunte sempre per ultime alla coda
; int print(const char*) ;
print: push rbp
       mov rbp, rsp
       mov rsi, [rbp + 16]
       xor rcx
       .ciclo:  cmp byte[rsi], 0
                je .dona

                mov rax, 1
                mov rdx, 1
                mov rdi, stdout
                mov rsi, rsi
                syscall

                prefetcht0[rsi + 8]
                inc rsi
                inc rcx
                jmp .ciclo
        .done:  cmp rcx, 0
                je .void_print
        .finish:mov rsp, rbp
                leave
                mov rax, rcx
                ret

        .void_print: mov rax, 1
                     mov rdi, stdout
                     mov rdx, 12
                     mov rsi, void_print
                     syscall
                     mov rax, 0
                     jmp .finish


len:    push rbp
        mov rbp, rsp
        xor rdx, rdx

        mov rsi, [rbp + 16]
        .count: cmp rsi, 0
                je .done
                
                prefetcht0[rsi + 8]
                inc rsi
                inc rdx
                jmp .count

        .done:  mov rsp, rbp
                leave
                mov rax, rdx
                ret

"""

def __init__shell() -> int:
    print("Welcome")
    while 1:
        command = input(">>> ")
        print("comando che hai scritto: ", command)

        if re.match(r"\s*exit\s*\n*", command) != None:
            print("exit from the she of compiler")
            return 0

        elif re.match(r"\s*version\(\s*\)\s*\n*", command) != None:
            print(show_version())

        elif re.match(r"\s*helpMe\(\s*\)\s*\n*", command) != None:
            print("riposta al comando helpMe()")

        else:
            print(f"unknow command: {command} try with helpMe()")

    return 0


def show_versione() -> str:
    return """
Name of the compiler: Volt
Version 1.0.1
Compiler compatibile con architetture intel a 64 bit
    """


def main(argc: int, argv: list) -> int:
    if argc == 1:
        __init__shell()
    elif "--version" in argv or "-version" in argv:
        print(show_versione())
    elif :
    else:
    return 0


if __name__ == "__main__":
    print("analizzando...")
    result = main(len(sys.argv), sys.argv)
    print(f"stato di uscita dal programma: {result}")
    sys.exit(result)
