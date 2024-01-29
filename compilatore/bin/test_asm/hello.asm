section .bss



section .data
	result db 1         ; variabile che rappresenta lo stato di uscita dalla funzione main
	msg db "Hello", 0



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

	_start: GXOR
		call main

		
		mov [result], rax
	_exit:  
		mov rax, 60
		mov rdi, [result]
		syscall



main:   push rbp    
        mov rbp, rsp
        
        push msg
        call print

        mov rax, 0

	mov rsp, rbp
        pop rbp
        ret


print:	push 	rbp
	mov 	rbp, rsp 
	mov 	rsi, [rbp + 16]

	start_chr:	cmp 	byte[rsi], 0
			jz 	end_print

			PRINT_CHAR

			inc 	rsi
			jmp 	start_chr

	end_print:	mov	rsp, rbp
			pop	rbp
        		ret


