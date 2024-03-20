
text = """

section .text
    Global _start

%macro GXOR 0
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
%endmacro


%macro NEWLINE 0
	mov rax, 1
	mov rdx, 1
	mov rsi, new_line
	mov rdi, 1
	syscall
%endmacro


%macro OPEN 3
	mov rax, 2  ; syscall code open
	mov rdi, %1 ; pathname
	mov rsi, %2 ; 0o101 modalita di apertura (O_WRONLY | O_RDONLY | O_TRUNC) -> base ottale
	mov rdx, %3 ; 0o666 permessi del file (rw-rw-rw-)			 -> base ottale
	syscall
%endmacro


%macro FWRITE 2
	mov rax, 1
	mov rsi, %1	; messaggio da scrivere nel file
	mov rdx, %2	; lunghezza del messaggio
	syscall
%endmacro


%macro FCLOSE 0
	mov rax, 3
	syscall
%endmacro


_start: GXOR
        call main

_exit:  mov rdi, rax
        mov rax, 60
        syscall


main:   push rbp
        mov rbp, rsp

"""


function_main_end = """

        mov rax, 0
        leave
        ret

"""

other_function = """

print:  push rbp
        mov rbp, rsp

        mov rax, 1
        mov rdi, 1
        mov rdx, [rbp + 18] ; la lunghezza del vettore e' il secondo che si pusha nello stack
        mov rsi, [rbp + 24] ; il vettore e' il primo che si pusha nello stack
        syscall

        ; new line
        sub rsp, 1      ; riservo spazio nello stack per il carattere new-line
        mov byte [rsp], 10

        mov rax, 1
        mov rdi, 1
        mov rdx, 1
        mov rsi, rsp
        syscall   

        leave
        ret


strlen: push rbp        ; contatore di lunghezza stringhe
        mov rbp, rsp

        mov rax, 0      ; ritorno la lunghezza del vettore all'interno del registro rax

        cntr:   mov     rsi, [rbp + 8]
                cmp     byte[rsi], 0
                jz      end

                inc     rax
                inc     rsi
                jmp     counter

        end:    leave ; libero lo stack
                ret

"""
