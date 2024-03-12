
section .bss



section .data

	a dq 3 
	despacito dq 15  	 ; ciao

	b dq -3          	 ; sono un commento

	d dq -3 
	ciao dq  "Hello World", 0  	 ;ciao




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

	add qword [b], 136
	add qword [d], 32
	mov rax, 57 ; fork()
	syscall

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
