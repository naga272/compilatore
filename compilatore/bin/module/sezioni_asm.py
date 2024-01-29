

sezioni_asm = [

# section .bss
"""
section .bss

""",

# section .data
"""
section .data
\tresult db 1         ; variabile che rappresenta lo stato di uscita dalla funzione main
\tmsg db "Hello", 0

""",

# section .text
"""
section .text
\t%macro GXOR 0
\t\txor rax, rax
\t\txor rbx, rbx
\t\txor rcx, rcx
\t\txor rdx, rdx
\t%endmacro

\t%macro PRINT_CHAR 0
\t\tmov rax, 1
\t\tmov rdi, 1
\t\tmov rdx, 1
\t\tsyscall
\t%endmacro

\tGlobal _start

\t_start: 
\t\tcall main
\t\tmov [result], rax


\t_exit:  
\t\tmov rax, 60
\t\tmov rdi, [result]
\t\tsyscall
""",

# section function
"""
main:   push rbp    
        mov rbp, rsp
        GXOR        

        push msg
        call print

        mov rax, 0          ; valore di ritorno se il programma e' andato a buon fine

        mov rsp, rbp
        pop rbp
        ret


print:  push rbp
        mov rbp, rsp
        xor rcx, rcx        ; come in C la print oltre a stampare in stdout ritorna la lunghezza della stringa stampata

        mov rsi, [rbp + 16]
        start_print:    cmp byte[rsi], 0
                        jz end_print

                        PRINT_CHAR

                        inc rsi
                        inc rcx
                        jmp start_print

        end_print:      mov rax, rcx
                        mov rsp, rbp
                        pop rbp
                        ret
"""
]
