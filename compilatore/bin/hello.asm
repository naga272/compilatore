

section .bss



section .data
	result db 1         ; variabile che rappresenta lo stato di uscita dalla funzione main
	msg db "Hello", 0

	ciao  db  5
	despacito db "sium", 0

section .text
	%macro GXOR 0
		xor rax, rax
		xor rbx, rbx
		xor rcx, rcx
		xor rdx, rdx
	%endmacro

	%macro PRINT_CHAR 0
		mov rax, 1
		mov rdi, 1
		mov rdx, 1
		syscall
	%endmacro

	Global _start

	_start: 
		call main
		mov [result], rax


	_exit:  
		mov rax, 60
		mov rdi, [result]
		syscall



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



