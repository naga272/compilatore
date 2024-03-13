
section .bss



section .data




section .text
    Global _start

%macro GXOR 0
    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
%endmacro

_start: GXOR
        call main

_exit:  mov rdi, rax
        mov rax, 60
        syscall


main:   push rbp
        mov rbp, rsp


	%define testttttt 1234 	; le macro devono avere nomi diversi rispetto alle variabili

	sub rsp, 8 
	mov qword [rbp - 8], 3
	sub rsp, 8  	 ; ciao

	mov qword [rbp - 16], 15
	sub rsp, 8          	 ; sono un commento

	mov qword [rbp - 24], -3
	sub rsp, 8 
	mov qword [rbp - 32], -3
	add qword [rbp - 8], 136
	add qword [rbp - 0], 32
	add qword [rbp - 24], 18

        mov rax, 0
        leave
        ret



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

